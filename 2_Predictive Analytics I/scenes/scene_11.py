import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_confusion_matrix, CORRECT_COLOR, ERROR_COLOR

CM_PRED_LABELS = ("Predicted: Positive", "Predicted: Negative")
CM_ACTUAL_LABELS = ("Actual:\nPositive", "Actual:\nNegative")
CM_TYPE_NAMES = [["True\nPositive", "False\nPositive"], ["False\nNegative", "True\nNegative"]]


class Scene11Mixin:
    # ------------------------------------------------------------------
    # Scene 11: evaluating classification models -- the confusion matrix
    # ------------------------------------------------------------------
    def scene_11(self):
        title = Text("Prediction Performance Evaluation", font_size=32).to_edge(UP, buff=0.4)

        with self.voiceover(
            text=(
                "Finally, let's learn how to evaluate the performance of "
                "predictive machine learning models. The basic idea is to "
                "deploy the model on the validation or testing data, then "
                "compare its predictions against the actual observed outcomes."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        # -- split-screen: classification vs. numeric prediction -----------
        # Only the two titles appear up front; each side's detail builds
        # in once the narration actually starts talking about that side.
        class_title = Text("Classification", font_size=24, color=YELLOW).move_to(LEFT * 3.5 + UP * 1.4)
        row1 = VGroup(
            Text("Predicted: Positive", font_size=18), Text("Actual: Positive", font_size=18), Text("✓", font_size=22, color=CORRECT_COLOR)
        ).arrange(RIGHT, buff=0.3).next_to(class_title, DOWN, buff=0.4)
        row2 = VGroup(
            Text("Predicted: Positive", font_size=18), Text("Actual: Negative", font_size=18), Text("✗", font_size=22, color=ERROR_COLOR)
        ).arrange(RIGHT, buff=0.3).next_to(row1, DOWN, buff=0.3)
        class_group = VGroup(class_title, row1, row2)

        numeric_title = Text("Numeric Prediction", font_size=24, color=BLUE).move_to(RIGHT * 3.5 + UP * 1.4)
        number_line = NumberLine(x_range=[0, 10, 2], length=5, color=GREY_B).next_to(numeric_title, DOWN, buff=0.6)
        pred_dot = Dot(number_line.n2p(7.2), color=BLUE)
        actual_dot = Dot(number_line.n2p(8.5), color=WHITE)
        pred_label = Text("Predicted", font_size=14, color=BLUE).next_to(pred_dot, DOWN, buff=0.15)
        actual_label = Text("Actual", font_size=14).next_to(actual_dot, UP, buff=0.15)
        gap_arrow = DoubleArrow(pred_dot.get_center(), actual_dot.get_center(), color=YELLOW, buff=0.05, stroke_width=2)
        numeric_group = VGroup(numeric_title, number_line, pred_dot, actual_dot, pred_label, actual_label, gap_arrow)

        with self.voiceover(
            text=(
                "Because classification and numeric prediction have different "
                "types of outcomes, they need different evaluation strategies. "
                "For a classification model, the outcome is categorical, so "
                "performance depends on whether the model puts each point in the "
                "right category. For a numeric prediction model, the outcome is "
                "continuous, so performance depends on how close the predictions "
                "are to the actual values."
            )
        ) as tracker:
            self.play(Write(class_title), run_time=0.8)
            self.play(Write(numeric_title), run_time=0.8)
            self.wait(5.5)
            self.play(FadeIn(row1), FadeIn(row2), run_time=1.3)  # "classification model...right category"
            self.wait(7.7)
            self.play(
                Create(number_line), FadeIn(pred_dot), FadeIn(actual_dot), FadeIn(pred_label), FadeIn(actual_label),
                run_time=2.0,
            )  # "numeric prediction model...continuous"
            self.play(GrowFromCenter(gap_arrow), run_time=0.8)  # "how close the predictions are to actual"
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Here, we'll focus on evaluating classification models.") as tracker:
            self.play(numeric_group.animate.set_opacity(0.25), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(numeric_group), FadeOut(class_group))

        cm_title = Text(
            "Confusion Matrix: Binary Classification (Positive / Negative)", font_size=24, color=YELLOW
        ).next_to(title, DOWN, buff=0.35)
        cm = make_confusion_matrix(CM_PRED_LABELS, CM_ACTUAL_LABELS)
        cm["group"].next_to(cm_title, DOWN, buff=0.55)

        with self.voiceover(
            text=(
                "A standard tool that summarizes a model's prediction "
                "correctness is confusion matrix, and several common "
                "performance metrics are defined based on the confusion matrix. "
                "Here's an example confusion matrix for a binary classification "
                "task, where the outcome is either positive or negative."
            )
        ) as tracker:
            self.play(FadeIn(cm_title), run_time=1.0)
            self.wait(1.5)
            self.play(Create(VGroup(*[cm["cells"][i][j] for i in range(2) for j in range(2)])), run_time=1.5)
            self.play(FadeIn(cm["row_labels"]), FadeIn(cm["col_labels"]), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        tp_name = Text(CM_TYPE_NAMES[0][0], font_size=16, color=CORRECT_COLOR).move_to(cm["cells"][0][0].get_center())
        fp_name = Text(CM_TYPE_NAMES[0][1], font_size=16, color=ERROR_COLOR).move_to(cm["cells"][0][1].get_center())

        with self.voiceover(
            text=(
                "Each row represents a predicted class, each column represents "
                "an actual class, and each of the four cells counts how many "
                "points fall into that combination. The upper-left cell, for "
                "example, counts points predicted positive that are actually "
                "positive. The upper-right cell counts points predicted "
                "positive that are actually negative."
            )
        ) as tracker:
            self.wait(0.5)
            self.play(Indicate(cm["row_labels"], color=YELLOW), run_time=1.0)  # "each row represents a predicted class"
            self.wait(1.5)
            self.play(Indicate(cm["col_labels"], color=YELLOW), run_time=1.0)  # "each column represents an actual class"
            self.wait(6.8)
            self.play(Indicate(cm["cells"][0][0], color=CORRECT_COLOR), run_time=1.0)  # "the upper-left cell..."
            self.play(FadeIn(tp_name), run_time=1.0)
            self.wait(3.5)
            self.play(Indicate(cm["cells"][0][1], color=ERROR_COLOR), run_time=1.0)  # "the upper-right cell..."
            self.play(FadeIn(fp_name), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        fn_name = Text(CM_TYPE_NAMES[1][0], font_size=16, color=ERROR_COLOR).move_to(cm["cells"][1][0].get_center())
        tn_name = Text(CM_TYPE_NAMES[1][1], font_size=16, color=CORRECT_COLOR).move_to(cm["cells"][1][1].get_center())
        diag_outline = VGroup(
            SurroundingRectangle(cm["cells"][0][0], color=CORRECT_COLOR, buff=0.03),
            SurroundingRectangle(cm["cells"][1][1], color=CORRECT_COLOR, buff=0.03),
        )
        offdiag_outline = VGroup(
            SurroundingRectangle(cm["cells"][0][1], color=ERROR_COLOR, buff=0.03),
            SurroundingRectangle(cm["cells"][1][0], color=ERROR_COLOR, buff=0.03),
        )

        with self.voiceover(
            text=(
                "The two diagonal cells hold the correct predictions; the two "
                "off-diagonal cells hold the misclassifications. These four "
                "cells are commonly labeled true positive, false positive, "
                "false negative, and true negative."
            )
        ) as tracker:
            self.play(Create(diag_outline), run_time=1.2)  # "diagonal cells hold the correct predictions"
            self.wait(1.5)
            self.play(Create(offdiag_outline), run_time=1.2)  # "off-diagonal cells hold the misclassifications"
            self.wait(3.0)
            self.play(FadeIn(fn_name), run_time=0.8)
            self.play(FadeIn(tn_name), run_time=0.8)  # "...false negative, and true negative"
            self.wait(tracker.get_remaining_duration())

        self.wait()
        cell_names = VGroup(tp_name, fp_name, fn_name, tn_name)
        self.play(FadeOut(diag_outline), FadeOut(offdiag_outline))

        self.cm_title_group = VGroup(title, cm_title)
        self.cm = cm
        self.cm_cell_names = cell_names
        self.cm_pred_labels = CM_PRED_LABELS
        self.cm_actual_labels = CM_ACTUAL_LABELS


class Scene11(VoiceoverScene, Scene11Mixin):
    """Standalone preview: manim -pql scene_11.py Scene11"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_11()
