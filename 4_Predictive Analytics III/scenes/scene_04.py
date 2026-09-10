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
    CURVE_B_COLOR,
    BETTER_COLOR,
    make_unit_axes,
    make_illustrative_curves,
)

# Same points as common.make_illustrative_curves' "b" curve -- reused here
# (not imported, since this is the only scene that needs it as a smooth
# plotted function rather than a hand-drawn VMobject) to illustrate AUC as
# a literal area under one representative, imperfect-but-good ROC curve.
AUC_ILLUSTRATION_POINTS = [(0, 0), (0.15, 0.55), (0.4, 0.8), (0.7, 0.93), (1, 1)]


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: comparing ROC curves across models, and the AUC summary
    # number
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_auc_curve_and_area(axes):
        xs = [p[0] for p in AUC_ILLUSTRATION_POINTS]
        ys = [p[1] for p in AUC_ILLUSTRATION_POINTS]
        graph = axes.plot(lambda x: float(np.interp(x, xs, ys)), x_range=[0, 1, 0.01], color=CURVE_B_COLOR)
        area = axes.get_area(graph, x_range=[0, 1], color=CURVE_B_COLOR, opacity=0.35)
        return graph, area

    def scene_04(self):
        title = Text("ROC and AUC for Model Comparison", font_size=28).to_edge(UP, buff=0.4)

        left_axes = make_unit_axes("False Positive Rate", "True Positive Rate", x_length=4.2, y_length=3.9)
        left_axes["group"].scale(0.85).move_to(LEFT * 3.6 + DOWN * 0.4)
        illustrative = make_illustrative_curves(left_axes["axes"])

        arrow = Arrow(
            left_axes["axes"].c2p(0.45, 0.4), left_axes["axes"].c2p(0.08, 0.9),
            color=BETTER_COLOR, buff=0.1, stroke_width=3,
        )
        better_label = Text("better", font_size=16, color=BETTER_COLOR).next_to(arrow.get_end(), UP, buff=0.05)

        with self.voiceover(
            text=(
                "Why is the ROC curve useful? Because it gives us a way "
                "to compare multiple classification models, both "
                "visually and quantitatively. Consider the ROC curves of "
                "four different classifiers, A through D. Curve A shoots "
                "straight up and then straight right — it corresponds to "
                "a perfect classifier, one that always assigns higher "
                "probabilities to every positive instance than to every "
                "negative instance. Curve D, close to the 45-degree "
                "diagonal line, corresponds to a random classifier that "
                "makes predictions based on a coin flip. A classifier "
                "that's better than random but not perfect will have an "
                "ROC curve that falls somewhere between A and D, and in "
                "general, the closer the curve sits to the top-left "
                "corner, the better the classifier."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(Create(left_axes["group"]), run_time=1.5)
            self.wait(2.0)
            self.play(
                Create(illustrative["curves"]["a"]), FadeIn(illustrative["labels"]["a"]),
                run_time=1.5,
            )
            self.wait(1.0)
            self.play(
                Create(illustrative["curves"]["d"]), FadeIn(illustrative["labels"]["d"]),
                run_time=1.3,
            )
            self.wait(1.0)
            self.play(
                Create(illustrative["curves"]["b"]), FadeIn(illustrative["labels"]["b"]),
                Create(illustrative["curves"]["c"]), FadeIn(illustrative["labels"]["c"]),
                run_time=1.6,
            )
            self.wait(1.5)
            self.play(GrowArrow(arrow), FadeIn(better_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        right_title = Text("Area under the Curve (AUC)", font_size=20).move_to(RIGHT * 3.6 + UP * 2.9)
        right_axes = make_unit_axes("FPR", "TPR", x_length=3.6, y_length=3.2)
        right_axes["group"].scale(0.85).move_to(RIGHT * 3.6 + UP * 0.3)
        auc_graph, auc_area = self.scene4_auc_curve_and_area(right_axes["axes"])

        b1 = Text("AUC = 1 → perfect classifier", font_size=16)
        b2 = Text("AUC = 0.5 → random classifier", font_size=16)
        b3 = Text("higher AUC → better separation of the classes", font_size=16)
        bullets = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullets.next_to(right_axes["group"], DOWN, buff=0.35)

        with self.voiceover(
            text=(
                "In addition to visual comparison, the ROC curve also "
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
            self.wait(1.0)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bullets], lag_ratio=0.4), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash for scene_05 (brings back this exact four-curve comparison
        # plot during its third paragraph).
        self.scene04_title = title
        self.scene04_left_axes = left_axes
        self.scene04_illustrative = illustrative
        self.scene04_arrow_group = VGroup(arrow, better_label)
        self.scene04_right_group = VGroup(right_title, right_axes["group"], auc_graph, auc_area, bullets)

        # Faded out (not destroyed) so scene_05 can bring the left-side
        # four-curve comparison back rather than rebuilding it.
        self.play(
            FadeOut(title), FadeOut(left_axes["group"]), FadeOut(illustrative["group"]),
            FadeOut(arrow), FadeOut(better_label), FadeOut(self.scene04_right_group),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
