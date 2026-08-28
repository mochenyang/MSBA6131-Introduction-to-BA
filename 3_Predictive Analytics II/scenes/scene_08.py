import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, CLASS1_COLOR, CLASS0_COLOR, make_cutoff_number_line

CANCER_COLOR = CLASS1_COLOR
HEALTHY_COLOR = CLASS0_COLOR


class Scene08Mixin:
    # ------------------------------------------------------------------
    # Scene 8: cost-sensitive classification -- cancer detection
    # ------------------------------------------------------------------
    @staticmethod
    def scene8_case_icon(label, color):
        box = RoundedRectangle(width=1.8, height=0.9, color=color, corner_radius=0.15)
        text = Text(label, font_size=18, color=color).move_to(box.get_center())
        return VGroup(box, text)

    @staticmethod
    def scene8_make_confusion_matrix(pred_labels, actual_labels, cell_size=1.7, label_font_size=15):
        """2x2 grid: cells[0][0]=TP, cells[0][1]=FP, cells[1][0]=FN, cells[1][1]=TN
        -- same layout convention as the Predictive Analytics I unit's
        common.make_confusion_matrix, trimmed down (no cell_texts) since this
        scene only needs to point at the FN/FP cells, not show full counts."""
        cells = [[None, None], [None, None]]
        for i in range(2):
            for j in range(2):
                rect = Square(side_length=cell_size, color=WHITE, stroke_width=2)
                rect.move_to(RIGHT * cell_size * j + DOWN * cell_size * i)
                cells[i][j] = rect
        grid = VGroup(*[cells[i][j] for i in range(2) for j in range(2)])
        col_labels = VGroup(*[
            Text(actual_labels[j], font_size=label_font_size, color=GREY_B).next_to(cells[0][j], UP, buff=0.2)
            for j in range(2)
        ])
        row_labels = VGroup(*[
            Text(pred_labels[i], font_size=label_font_size, color=GREY_B).next_to(cells[i][0], LEFT, buff=0.3)
            for i in range(2)
        ])
        group = VGroup(grid, col_labels, row_labels)
        return {"cells": cells, "col_labels": col_labels, "row_labels": row_labels, "group": group}

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

        cm = self.scene8_make_confusion_matrix(
            ("Predicted:\nCancer", "Predicted:\nHealthy"), ("Actual:\nCancer", "Actual:\nHealthy")
        )
        cm["group"].move_to(UP * 0.2)

        fn_outline = SurroundingRectangle(cm["cells"][1][0], color=CANCER_COLOR, buff=0, stroke_width=3)
        fn_label = Text("False Negative", font_size=15, color=CANCER_COLOR)
        fn_cost_label = Text("High Cost", font_size=18, color=CANCER_COLOR)
        VGroup(fn_label, fn_cost_label).arrange(DOWN, buff=0.15).move_to(cm["cells"][1][0].get_center())

        fp_outline = SurroundingRectangle(cm["cells"][0][1], color=HEALTHY_COLOR, buff=0, stroke_width=3)
        fp_label = Text("False Positive", font_size=15, color=HEALTHY_COLOR)
        fp_cost_label = Text("Low Cost", font_size=18, color=HEALTHY_COLOR)
        VGroup(fp_label, fp_cost_label).arrange(DOWN, buff=0.15).move_to(cm["cells"][0][1].get_center())

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
            self.play(FadeIn(cm["group"]), run_time=1.3)
            self.wait(4.0)
            self.play(Create(fn_outline), FadeIn(fn_label), run_time=1.3)
            self.play(FadeIn(fn_cost_label), run_time=1.0)
            self.wait(9.0)
            self.play(Create(fp_outline), FadeIn(fp_label), run_time=1.2)
            self.play(FadeIn(fp_cost_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        cost_scene_group = VGroup(
            cm["group"], fn_outline, fn_label, fn_cost_label, fp_outline, fp_label, fp_cost_label,
        )
        
        num_line = self.scene02_number_line
        num_line["group"].move_to(DOWN * 1.6)

        healthy_label = Text("(Healthy)", font_size=16, color=HEALTHY_COLOR).next_to(
            num_line["class0_label"], DOWN, buff=0.15
        )
        cancerous_label = Text("(Cancer)", font_size=16, color=CANCER_COLOR).next_to(
            num_line["class1_label"], DOWN, buff=0.15
        )

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
                "cutoff for classifying a point as class 1. "
                "This means we risk misclassifying some healthy "
                "cases as cancerous, in order to avoid the far more costly "
                "mistake of missing an actual cancer."
            )
        ) as tracker:
            self.play(cost_scene_group.animate.scale(0.7).to_edge(UP, buff=1.0), run_time=1.3)
            self.wait(5.0)
            self.play(FadeIn(num_line["group"]), FadeIn(healthy_label), FadeIn(cancerous_label), run_time=1.3)
            self.wait(2.0)
            self.play(Indicate(num_line["cutoff_label"], color=YELLOW), run_time=1.0)
            self.wait(24.0)
            self.play(FadeIn(flip_dot1), FadeIn(flip_dot2), run_time=1.0)
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

        # The confusion matrix stays on screen (shrunk, top of frame) -- only
        # the number line and its cutoff-sliding pieces go away here.
        self.play(
            FadeOut(num_line["group"]), FadeOut(flip_dot1), FadeOut(flip_dot2),
            FadeOut(healthy_label), FadeOut(cancerous_label),
        )

        # Built from separate numerator/line/denominator pieces (matching
        # common.make_bayes_formula's approach) rather than splitting a
        # single \dfrac{...}{...} across multiple MathTex string args --
        # the latter doesn't actually lay out as a fraction, since LaTeX
        # can't parse \dfrac's braces correctly once they're split across
        # separately-tracked submobject boundaries.
        cost_label = MathTex(r"\text{Avg. Cost} = ")
        fp_term = MathTex(r"\text{cost}_{FP} \times \#FP", color=HEALTHY_COLOR)
        cost_plus = MathTex("+")
        fn_term = MathTex(r"\text{cost}_{FN} \times \#FN", color=CANCER_COLOR)
        cost_numerator = VGroup(fp_term, cost_plus, fn_term).arrange(RIGHT, buff=0.25)
        cost_denominator = MathTex("N")
        cost_frac_line = Line(LEFT, RIGHT, stroke_width=2.5)
        cost_frac_group = VGroup(cost_numerator, cost_frac_line, cost_denominator).arrange(DOWN, buff=0.2)
        cost_frac_line.stretch_to_fit_width(cost_numerator.width + 0.3)
        cost_formula = VGroup(cost_label, cost_frac_group).arrange(RIGHT, buff=0.3).scale(0.9)
        cost_formula.move_to(DOWN * 1.3)

        takeaway = Text(
            "Try different cutoffs to minimize misclassification cost on validation data",
            font_size=20, color=YELLOW,
        ).next_to(cost_formula, DOWN, buff=0.7)

        with self.voiceover(
            text=(
                "If we know the cost of each type of misclassification, we "
                "can quantify this directly: assign a cost to false "
                "positives and false negatives respectively, sum the cost "
                "across all misclassified points, and divide by the size "
                "of validation data to get the average misclassification "
                "cost. In a cost-sensitive classification task, we then pick "
                "the cutoff value that minimizes this average cost on the "
                "validation data."
            )
        ) as tracker:
            self.wait(4.0)
            self.play(FadeIn(fp_term), run_time=1.5)
            self.play(FadeIn(fn_term), run_time=1.5)
            self.play(FadeIn(cost_plus), run_time=1.5)
            self.play(Create(cost_frac_line), FadeIn(cost_denominator), run_time=1.5)  # "...divide by the total number of data points"
            self.play(Write(cost_label), run_time=1.5)  # "sum the cost..."  
            self.wait(4.0)
            self.play(FadeIn(takeaway, shift=UP * 0.15), run_time=1.3)  # "pick the cutoff value that minimizes..."
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(cost_scene_group), FadeOut(cost_formula), FadeOut(takeaway),
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
