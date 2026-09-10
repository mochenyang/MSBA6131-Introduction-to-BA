import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    PERFECT_CLASSIFIER_COLOR,
    REGULAR_CLASSIFIER_COLOR,
    CURVE_B_POINTS,
    RANDOM_CLASSIFIER_COLOR,
    make_unit_axes,
)


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: comparing ROC curves across models, and the AUC summary
    # number
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_illustrative_curves(axes):
        """Three classifier curves for this scene's comparison: A (perfect),
        B (good but imperfect), C (near- but not exactly-random). Built
        directly rather than via common.make_illustrative_curves' shared
        four-curve (A-D) set -- that set's C/D semantics (mediocre curve,
        exact diagonal) don't match what this scene needs, which is only
        three curves with the third one close to, but not literally on,
        the diagonal."""
        curve_a = VMobject(color=PERFECT_CLASSIFIER_COLOR, stroke_width=3.5)
        curve_a.set_points_as_corners([axes.c2p(x, y) for x, y in [(0, 0), (0, 1), (1, 1)]])
        # Labeled beside the vertical segment's midpoint, not the (0,1)
        # corner -- that corner sits right under the y-axis arrowhead, which
        # would otherwise hide the label behind/underneath the arrow tip.
        label_a = Text("A", font_size=18, color=PERFECT_CLASSIFIER_COLOR).next_to(axes.c2p(0.5, 1.1), RIGHT, buff=0.12)

        curve_b = VMobject(color=REGULAR_CLASSIFIER_COLOR, stroke_width=3.5)
        curve_b.set_points_as_corners([axes.c2p(x, y) for x, y in CURVE_B_POINTS])
        label_b = Text("B", font_size=18, color=REGULAR_CLASSIFIER_COLOR).next_to(
            axes.c2p(0.5, 0.7), UP, buff=0.12
        )

        near_diagonal_pts = [(0, 0), (0.25, 0.29), (0.5, 0.47), (0.75, 0.71), (1, 1)]
        curve_c = VMobject(color=RANDOM_CLASSIFIER_COLOR, stroke_width=3.5)
        curve_c.set_points_as_corners([axes.c2p(x, y) for x, y in near_diagonal_pts])
        label_c = Text("C", font_size=18, color=RANDOM_CLASSIFIER_COLOR).next_to(axes.c2p(0.5, 0.5), DOWN, buff=0.35)

        curves = {"a": curve_a, "b": curve_b, "c": curve_c}
        labels = {"a": label_a, "b": label_b, "c": label_c}
        group = VGroup(*curves.values(), *labels.values())
        return {"curves": curves, "labels": labels, "group": group}

    @staticmethod
    def scene4_auc_curve_and_area(axes):
        # Copies curve B's own points (common.CURVE_B_POINTS), rather than a
        # separately-guessed shape, so the AUC illustration shades under the
        # exact same "good, imperfect" curve introduced on the left.
        xs = [p[0] for p in CURVE_B_POINTS]
        ys = [p[1] for p in CURVE_B_POINTS]
        graph = axes.plot(lambda x: float(np.interp(x, xs, ys)), x_range=[0, 1, 0.01], color=REGULAR_CLASSIFIER_COLOR)
        area = axes.get_area(graph, x_range=[0, 1], color=REGULAR_CLASSIFIER_COLOR, opacity=0.35)
        return graph, area

    def scene_04(self):
        title = Text("ROC and AUC for Model Comparison", font_size=28).to_edge(UP, buff=0.4)

        left_axes = make_unit_axes("FPR", "TPR", x_length=4.2, y_length=3.9, x_max=1.08, y_max=1.08)
        left_axes["group"].move_to(LEFT * 3.6)
        illustrative = self.scene4_illustrative_curves(left_axes["axes"])

        arrow = Arrow(
            left_axes["axes"].c2p(0.4, 0.4), left_axes["axes"].c2p(0.08, 0.9),
            color=YELLOW, buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.35
        )
        better_label = Text("better", font_size=14, color=YELLOW).next_to(arrow.get_end(), UP, buff=0.05)

        with self.voiceover(
            text=(
                "Why is the R O C curve useful? Because it gives us a way "
                "to compare multiple classification models, both "
                "visually and quantitatively. Consider the R O C curves of "
                "three different classifiers, A, B, and C. Curve A shoots "
                "straight up and then straight right — it corresponds to "
                "a perfect classifier, one that always assigns higher "
                "probabilities to every positive instance than to every "
                "negative instance. Curve C, close to the 45-degree "
                "diagonal line, corresponds to a random classifier that "
                "makes predictions based on a coin flip. A classifier "
                "that's better than random but not perfect will have an "
                "R O C curve that falls somewhere between A and C, and in "
                "general, the closer the curve sits to the top-left "
                "corner, the better the classifier."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.wait(6.0)
            self.play(Create(left_axes["group"]), run_time=1.5)
            self.wait(3.0)
            self.play(
                Create(illustrative["curves"]["a"]), FadeIn(illustrative["labels"]["a"]),
                run_time=1.5,
            )
            self.wait(10.0)
            self.play(
                Create(illustrative["curves"]["c"]), FadeIn(illustrative["labels"]["c"]),
                run_time=1.3,
            )
            self.wait(7.0)
            self.play(
                Create(illustrative["curves"]["b"]), FadeIn(illustrative["labels"]["b"]),
                run_time=1.6,
            )
            self.wait(8.0)
            self.play(GrowArrow(arrow), FadeIn(better_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        right_title = Text("Area under the Curve (AUC)", font_size=20).move_to(RIGHT * 3.6 + UP * 2.65)
        right_axes = make_unit_axes("FPR", "TPR", x_length=4.2, y_length=3.9, x_max=1.08, y_max=1.08)
        right_axes["group"].move_to(RIGHT * 3.6)
        auc_graph, auc_area = self.scene4_auc_curve_and_area(right_axes["axes"])

        b1 = Text("AUC = 1 → perfect classifier", font_size=16)
        b2 = Text("AUC = 0.5 → random classifier", font_size=16)
        b3 = Text("higher AUC → better separation of the classes", font_size=16)
        bullets = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.next_to(right_axes["group"], DOWN, buff=0.35)

        with self.voiceover(
            text=(
                "In addition to visual comparison, the R O C curve also "
                "gives us a single-number measure of classifier "
                "performance: the area under the curve, or AUC. AUC is "
                "a number between 0 and 1 — 1 means a perfect "
                "classifier, 0.5 means a random classifier, and a "
                "reasonably good classifier should score somewhere "
                "between 0.5 and 1."
            )
        ) as tracker:
            self.play(FadeIn(right_title), run_time=1.0)
            self.play(Create(right_axes["group"]), run_time=1.5)
            self.play(Create(auc_graph), run_time=1.5)
            self.play(FadeIn(auc_area), run_time=1.3)
            self.wait(4.0)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bullets], lag_ratio=0.4), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash for scene_05 (brings back this exact three-curve comparison
        # plot during its third paragraph).
        self.scene04_title = title
        self.scene04_left_axes = left_axes
        self.scene04_illustrative = illustrative
        self.scene04_arrow_group = VGroup(arrow, better_label)
        self.scene04_right_group = VGroup(right_title, right_axes["group"], auc_graph, auc_area, bullets)

        # Faded out (not destroyed) so scene_05 can bring the left-side
        # three-curve comparison back rather than rebuilding it.
        self.play(
            FadeOut(title), FadeOut(left_axes["group"]), FadeOut(illustrative["group"]),
            FadeOut(arrow), FadeOut(better_label), FadeOut(self.scene04_right_group),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
