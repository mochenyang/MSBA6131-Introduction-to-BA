import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    ERROR_COLOR,
    make_unit_axes,
    make_confusion_matrix,
    compute_roc_points,
    compute_cum_response_points,
    build_data_curve,
)


class Scene08Mixin:
    # ------------------------------------------------------------------
    # Scene 8: summary -- ranking-based methods (ROC / AUC, cumulative
    # response) vs. cutoff-dependent metrics (accuracy, precision,
    # recall, F-measure)
    # ------------------------------------------------------------------
    def scene_08(self):
        title = Text("Summary: Ranking-based Evaluation Methods", font_size=26).to_edge(UP, buff=0.4)

        left_title = Text("Ranking-based Methods", font_size=20, color=YELLOW).move_to(LEFT * 3.5 + UP * 2.3)

        roc_axes = make_unit_axes("FPR", "TPR", x_length=2.6, y_length=2.4, x_max=1.08, y_max=1.08, font_size=12)
        roc_axes["group"].scale(0.8).move_to(LEFT * 5.0 + DOWN * 0.25)
        roc_curve = build_data_curve(roc_axes["axes"], compute_roc_points(), dot_radius=0.03, stroke_width=2.5)
        # next_to roc_axes["axes"] (just the plot box), not roc_axes["group"]
        # (which also includes the "TPR" y-axis label sticking out to the
        # left) -- centering on the group skewed the label left of the
        # actual curve.
        roc_label = Text("ROC Curve", font_size=14, color=GREY_B).next_to(roc_axes["axes"], UP, buff=0.1)

        cum_axes = make_unit_axes("% Data", "Cum.\nResp.", x_length=2.6, y_length=2.4, x_max=1.08, y_max=1.08, font_size=12)
        cum_axes["group"].scale(0.8).move_to(LEFT * 2.0 + DOWN * 0.25)
        cum_curve = build_data_curve(cum_axes["axes"], compute_cum_response_points(), dot_radius=0.03, stroke_width=2.5)
        cum_label = Text("Cumulative Response", font_size=14, color=GREY_B).next_to(cum_axes["axes"], UP, buff=0.1)

        left_group = VGroup(left_title, roc_axes["group"], roc_curve, roc_label, cum_axes["group"], cum_curve, cum_label)

        right_title = Text("Cutoff-Dependent Metrics", font_size=20, color=YELLOW).move_to(RIGHT * 3.5 + UP * 2.3)
        cm = make_confusion_matrix(cell_size=1.0, label_font_size=13)
        cm["group"].move_to(RIGHT * 3.5 + UP * 0.25)
        # next_to the 2x2 cell grid itself, not cm["group"] (which also
        # includes the "Pred: P"/"Pred: N" row labels sticking out to the
        # left of the cells) -- centering on the group skewed this left of
        # the actual cells.
        cm_grid = VGroup(*[cm["cells"][i][j] for i in range(2) for j in range(2)])
        metric_names = VGroup(*[
            Text(name, font_size=15) for name in ("Accuracy", "Precision", "Recall", "F-measure")
        ]).arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.3)).next_to(cm_grid, DOWN, buff=0.4)

        right_group = VGroup(right_title, cm["group"], metric_names)

        # Row-aligned on the lower of the two groups' bottoms -- left_group
        # (two small plots) is noticeably shorter than right_group
        # (confusion matrix + 4-line metric list), so anchoring each
        # caption to its own group via next_to(..., DOWN) independently, or
        # aligning the right one to the shorter left one, left the red
        # caption sitting too high and overlapping "Precision".
        caption_y = min(left_group.get_bottom()[1], right_group.get_bottom()[1]) - 0.4
        left_caption = Text("Do not change w.r.t. cutoff", font_size=16, color=GREEN).move_to(
            [left_group.get_center()[0], caption_y, 0]
        )
        right_caption = Text("Depend on specific cutoff", font_size=16, color=ERROR_COLOR).move_to(
            [right_group.get_center()[0], caption_y, 0]
        )

        divider = Line(UP * 3.0, DOWN * 3.0, color=GREY_D, stroke_width=4)

        with self.voiceover(
            text=(
                "To summarize, R O C curve and cumulative response curve "
                "are two representative examples of the so-called "
                "\"ranking-based\" evaluation methods. They both reflect "
                "how well a classification model ranks data instances "
                "based on predicted probabilities. It's useful to keep "
                "in mind that they differ from the evaluation metrics "
                "we discussed in a prior video, namely accuracy, "
                "precision, recall, and F-measure. To calculate these "
                "metrics, we need to first select a specific cutoff "
                "threshold to convert probability predictions into "
                "class predictions. In comparison, R O C curve (and by "
                "extension the AUC measure) as well as the cumulative "
                "response curve are \"threshold-agnostic\" because their "
                "construction requires the enumeration of all possible "
                "cutoff values. Changing the cutoff threshold in a "
                "classification model does not change its R O C curve or "
                "cumulative response curve."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.wait(4.0)
            self.play(FadeIn(left_title), run_time=1.0)
            self.play(
                Create(roc_axes["group"]), FadeIn(roc_label), Create(roc_curve),
                Create(cum_axes["group"]), FadeIn(cum_label), Create(cum_curve),
                run_time=1.8,
            )
            self.wait(7.0)
            self.play(Create(divider), run_time=0.8)
            self.play(FadeIn(right_title), run_time=1.0)
            self.play(FadeIn(cm["group"]), FadeIn(metric_names), run_time=1.5)
            self.wait(6.0)
            self.play(FadeIn(right_caption, shift=UP * 0.1), run_time=1.2)
            self.wait(6.0)
            self.play(FadeIn(left_caption, shift=UP * 0.1), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(divider), FadeOut(left_group), FadeOut(right_group),
            FadeOut(left_caption), FadeOut(right_caption),
        )


class Scene08(VoiceoverScene, Scene08Mixin):
    """Standalone preview: manim -pql scene_08.py Scene08"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_08()
