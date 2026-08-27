import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, CLASS1_COLOR, CLASS0_COLOR, make_cutoff_number_line

CANCER_COLOR = RED
HEALTHY_COLOR = GREEN


class Scene08Mixin:
    # ------------------------------------------------------------------
    # Scene 8: cost-sensitive classification -- cancer detection
    # ------------------------------------------------------------------
    @staticmethod
    def scene8_case_icon(label, color):
        box = RoundedRectangle(width=1.8, height=0.9, color=color, corner_radius=0.15)
        text = Text(label, font_size=18, color=color).move_to(box.get_center())
        return VGroup(box, text)

    def scene_08(self):
        title = Text("Probability Prediction Application: Cost-Sensitive Classification", font_size=24).to_edge(
            UP, buff=0.4
        )

        with self.voiceover(
            text=(
                "Having probability predictions from a classification model "
                "not only allows you to obtain class predictions, it also "
                "creates new applications with practical importance. Here, I "
                "want to introduce one such application: cost-sensitive "
                "classification."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.2)
            self.wait(tracker.get_remaining_duration())

        cancer_icon = self.scene8_case_icon("Cancerous", CANCER_COLOR).move_to(LEFT * 4.5 + UP * 1.6)
        healthy_icon = self.scene8_case_icon("Healthy", HEALTHY_COLOR).move_to(RIGHT * 4.5 + UP * 1.6)

        fn_arrow = Arrow(cancer_icon.get_bottom(), cancer_icon.get_bottom() + DOWN * 1.3, color=CANCER_COLOR, buff=0.1)
        fn_label = Text("predicted Healthy\n(false negative)", font_size=16, color=CANCER_COLOR, line_spacing=1.1).next_to(
            fn_arrow, DOWN, buff=0.15
        )
        fn_cost = RoundedRectangle(width=2.4, height=1.0, color=CANCER_COLOR, corner_radius=0.15).next_to(
            fn_label, DOWN, buff=0.25
        )
        fn_cost_label = Text("HIGH COST", font_size=20, color=CANCER_COLOR).move_to(fn_cost.get_center())

        fp_arrow = Arrow(healthy_icon.get_bottom(), healthy_icon.get_bottom() + DOWN * 1.3, color=HEALTHY_COLOR, buff=0.1)
        fp_label = Text("predicted Cancerous\n(false positive)", font_size=16, color=HEALTHY_COLOR, line_spacing=1.1).next_to(
            fp_arrow, DOWN, buff=0.15
        )
        fp_cost = RoundedRectangle(width=1.3, height=0.5, color=HEALTHY_COLOR, corner_radius=0.1).next_to(
            fp_label, DOWN, buff=0.25
        )
        fp_cost_label = Text("low cost", font_size=15, color=HEALTHY_COLOR).move_to(fp_cost.get_center())

        with self.voiceover(
            text=(
                "In many real-world problems, different types of prediction "
                "errors carry different costs. In cancer detection, for "
                "example, misclassifying a cancerous case as healthy — a "
                "false negative — can be extremely costly: the patient "
                "misses out on early treatment while the disease continues "
                "to progress. Misclassifying a healthy case as cancerous — a "
                "false positive — is comparatively far less dangerous: it "
                "typically just leads to some extra follow-up testing, which "
                "is stressful and inconvenient but nowhere near as costly as "
                "missing an actual cancer."
            )
        ) as tracker:
            self.play(FadeIn(cancer_icon), FadeIn(healthy_icon), run_time=1.3)
            self.play(GrowArrow(fn_arrow), FadeIn(fn_label), run_time=1.3)
            self.play(FadeIn(fn_cost), FadeIn(fn_cost_label), run_time=1.3)
            self.wait(1.0)
            self.play(GrowArrow(fp_arrow), FadeIn(fp_label), run_time=1.2)
            self.play(FadeIn(fp_cost), FadeIn(fp_cost_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        cost_scene_group = VGroup(
            cancer_icon, healthy_icon, fn_arrow, fn_label, fn_cost, fn_cost_label,
            fp_arrow, fp_label, fp_cost, fp_cost_label,
        )
        self.play(cost_scene_group.animate.scale(0.55).to_edge(UP, buff=1.0), run_time=1.3)

        num_line = self.scene02_number_line
        num_line["group"].move_to(DOWN * 1.6)

        flip_dot1 = Dot(num_line["line"].n2p(0.35), color=CLASS0_COLOR, radius=0.08)
        flip_dot2 = Dot(num_line["line"].n2p(0.45), color=CLASS0_COLOR, radius=0.08)

        with self.voiceover(
            text=(
                "Because of this asymmetry, our goal in classification is "
                "sometimes not to maximize accuracy but to minimize the cost "
                "of misclassifications — and a simple way to do that is to "
                "leverage the cutoff value on the predicted class "
                "probabilities. Suppose class 1 is \"cancer\" and class 0 is "
                "\"healthy,\" and misclassifying class 1 as class 0 is far "
                "more costly than the reverse, so we want the model to be "
                "more conservative when predicting class 0 — we want it to "
                "be very sure before predicting \"healthy,\" since being "
                "wrong there is expensive. We can do this by lowering the "
                "cutoff for classifying a point as class 1, which is "
                "equivalent to raising the cutoff for classifying it as "
                "class 0. This means we risk misclassifying some healthy "
                "cases as cancerous, in order to avoid the far more costly "
                "mistake of missing an actual cancer."
            )
        ) as tracker:
            self.play(FadeIn(num_line["group"]), run_time=1.3)
            self.play(FadeIn(flip_dot1), FadeIn(flip_dot2), run_time=1.0)
            self.wait(8.0)
            new_marker = num_line["marker"].copy().next_to(num_line["line"].n2p(0.3), UP, buff=0.02)
            new_cutoff_label = Text("cutoff = 0.3", font_size=16, color=RED).next_to(new_marker, UP, buff=0.12)
            self.play(
                Transform(num_line["marker"], new_marker),
                Transform(num_line["cutoff_label"], new_cutoff_label),
                run_time=1.5,
            )
            self.play(
                flip_dot1.animate.set_color(CLASS1_COLOR),
                flip_dot2.animate.set_color(CLASS1_COLOR),
                run_time=1.3,
            )
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(num_line["group"]), FadeOut(flip_dot1), FadeOut(flip_dot2), FadeOut(cost_scene_group))

        axes = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 10, 5], x_length=7, y_length=3.5,
            axis_config={"include_ticks": True, "font_size": 16},
        ).move_to(DOWN * 0.3)
        x_label = axes.get_x_axis_label(Text("cutoff", font_size=18), edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label(Text("avg. cost", font_size=18), edge=LEFT, direction=LEFT)
        curve = axes.plot(lambda t: 5 * (t - 0.3) ** 2 + 2, x_range=[0.02, 0.98], color=YELLOW)
        min_point = Dot(axes.coords_to_point(0.3, 2), color=RED, radius=0.09)
        min_line = DashedLine(axes.coords_to_point(0.3, 0), axes.coords_to_point(0.3, 2), color=RED)
        chosen_label = Text("chosen on validation data", font_size=16, color=RED).next_to(min_point, UP, buff=0.3)

        with self.voiceover(
            text=(
                "If we know the cost of each type of misclassification, we "
                "can quantify this directly: assign a cost to false "
                "positives and false negatives respectively, sum the cost "
                "across all misclassified points, and divide by the total "
                "number of data points to get the average misclassification "
                "cost. In a cost-sensitive classification task, we then pick "
                "the cutoff value that minimizes this average cost on the "
                "validation data."
            )
        ) as tracker:
            self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)
            self.play(Create(curve), run_time=2.0)
            self.wait(1.5)
            self.play(Create(min_line), FadeIn(min_point), run_time=1.2)
            self.play(FadeIn(chosen_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(curve),
            FadeOut(min_line), FadeOut(min_point), FadeOut(chosen_label),
        )


class Scene08(VoiceoverScene, Scene08Mixin):
    """Standalone preview: manim -pql scene_08.py Scene08"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_02()
        self.scene_08()

    def _fixture_scene_02(self):
        # Stand-in for scene_02's cutoff-number-line visual so scene_08 can
        # be previewed alone.
        self.scene02_number_line = make_cutoff_number_line(cutoff=0.5, width=8.5)
