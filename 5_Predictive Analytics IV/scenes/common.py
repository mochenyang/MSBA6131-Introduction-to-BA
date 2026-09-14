from manim import *
from manim import Text as _ManimText

# ----------------------------------------------------------------------
# Small-font-safe Text -- see references/visual_techniques.md. Manim's
# Text (Pango-backed) renders visible glyph-spacing artifacts at small
# font sizes; this always renders at a safe base size and scales down.
# ----------------------------------------------------------------------
TEXT_SAFE_BASE_SIZE = 40


class Text(_ManimText):
    def __init__(self, text, font_size=48, **kwargs):
        if font_size < TEXT_SAFE_BASE_SIZE:
            super().__init__(text, font_size=TEXT_SAFE_BASE_SIZE, **kwargs)
            self.scale(font_size / TEXT_SAFE_BASE_SIZE)
        else:
            super().__init__(text, font_size=font_size, **kwargs)


# ----------------------------------------------------------------------
# Semantic colors shared across scenes
# ----------------------------------------------------------------------
TRAIN_COLOR = GREEN            # a fold used for training, in a given round
VALIDATION_COLOR = ORANGE      # a fold used for validation, in a given round
SCORE_COLOR = YELLOW           # per-round performance scores (s_1 .. s_k)
NEUTRAL_COLOR = GREY_B         # a fold not yet assigned a role this round

SELECTED_COLOR = GREEN         # a feature kept / passing the filter
REJECTED_COLOR = RED           # a feature dropped / filtered out
CURRENT_COLOR = YELLOW         # the feature currently being tried


# ----------------------------------------------------------------------
# k-fold bar -- a row of k folds (rounded boxes with a few dots inside,
# a "Fold i" label below), all starting neutral-colored. Built in scene_02,
# then reused (colors re-driven) in scene_03's reporting visuals.
# ----------------------------------------------------------------------
def make_fold_bar(n_folds=5, dots_per_fold=3, fold_width=1.15, fold_height=0.9, gap=0.3):
    fold_groups = VGroup()
    rects, dot_groups, labels = [], [], []
    for i in range(n_folds):
        rect = RoundedRectangle(
            width=fold_width, height=fold_height, corner_radius=0.12,
            color=NEUTRAL_COLOR, stroke_width=3,
        )
        dots = VGroup(
            *[Dot(radius=0.06, color=NEUTRAL_COLOR) for _ in range(dots_per_fold)]
        ).arrange(RIGHT, buff=0.1).move_to(rect.get_center())
        label = Text(f"Fold {i + 1}", font_size=16, color=GREY_B).next_to(rect, DOWN, buff=0.15)
        one_fold = VGroup(rect, dots, label)
        fold_groups.add(one_fold)
        rects.append(rect)
        dot_groups.append(dots)
        labels.append(label)
    fold_groups.arrange(RIGHT, buff=gap)
    return {
        "group": fold_groups,
        "rects": rects,
        "dots": dot_groups,
        "labels": labels,
        "n_folds": n_folds,
    }
