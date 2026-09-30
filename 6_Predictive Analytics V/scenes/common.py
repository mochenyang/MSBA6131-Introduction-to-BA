from manim import *
from manim import Text as _ManimText

# ----------------------------------------------------------------------
# Manim's Text (Pango-backed) renders visible glyph-spacing artifacts at
# small font sizes. This drop-in replacement always renders at a safe base
# size and scales down to whatever font_size was actually requested, so
# every call site keeps its exact `Text(..., font_size=14)` signature --
# only the import needs to change. Import `Text` from `common` (after
# `from manim import *`, so it shadows manim's) in every scene file.
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
CLASS_YES_COLOR = ORANGE
CLASS_NO_COLOR = PURPLE
NUMERIC_COLOR = BLUE
ERROR_COLOR = RED
GOOD_COLOR = GREEN
HIGHLIGHT_COLOR = YELLOW

# ----------------------------------------------------------------------
# Shared linear-regression example: one running (x, y) dataset, reused
# small in scene 4's side-by-side line-fit sketch and big in scene 5's
# SSE-minimization walkthrough. Roughly linear with mild noise.
# ----------------------------------------------------------------------
LINREG_POINTS = [
    (1, 7.1), (2, 4.6), (3, 11.0), (3.5, 7.8), (4.5, 15.4),
    (5.5, 13.8), (6.5, 20.0), (7.5, 18.2), (8, 23.4),
]
LINREG_BEST_SLOPE = 2.426
LINREG_BEST_INTERCEPT = 2.292
LINREG_BEST_SSE = 43.14


# ----------------------------------------------------------------------
# Generic decision-tree node/edge drawing (same shape as used in
# 2_Predictive Analytics I -- reimplemented here since scene files must
# not import across unit folders).
# ----------------------------------------------------------------------
def make_tree_node(text, color=WHITE, font_size=22, width=None):
    label = Text(text, font_size=font_size)
    box = RoundedRectangle(
        width=width if width else label.width + 0.5,
        height=label.height + 0.4,
        corner_radius=0.12,
        color=color,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_tree_edge(node_a, node_b, label=None, color=WHITE):
    line = Line(node_a.get_bottom(), node_b.get_top(), color=color, buff=0.05, stroke_width=2.5)
    if label is None:
        return line
    tag = Text(label, font_size=16, color=GREY_B).move_to(line.get_center()).shift(RIGHT * 0.55)
    return VGroup(line, tag)
