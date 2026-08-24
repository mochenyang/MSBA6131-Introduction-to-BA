import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_confusion_matrix, CORRECT_COLOR, ERROR_COLOR

FRAUD_PRED_LABELS = ("Predicted: Fraudulent", "Predicted: Non-Fraudulent")
# Short column labels -- "Actual: Non-Fraudulent" would collide with its
# neighbor above adjacent cells, same issue fixed in common.make_confusion_matrix.
FRAUD_ACTUAL_LABELS = ("Fraud", "Non-Fraud")
# TP, FP / FN, TN -- sums to 100 validation points
FRAUD_COUNTS = [[15, 5], [10, 70]]


class Scene12Mixin:
    # ------------------------------------------------------------------
    # Scene 12: performance metrics -- accuracy, precision, recall, F-measure
    # ------------------------------------------------------------------
    def scene_12(self):
        title_group = self.cm_title_group
        old_cm = self.cm
        old_cell_names = self.cm_cell_names

        cm = make_confusion_matrix(
            FRAUD_PRED_LABELS, FRAUD_ACTUAL_LABELS, cell_texts=FRAUD_COUNTS, cell_size=2.0, label_font_size=16
        )
        cm["group"].move_to(LEFT * 3.6 + DOWN * 0.6)

        # All four metric blocks are laid out up front, as one vertical
        # stack, before any of them are shown -- each is only *revealed*
        # later in its own narration block, but never moved or resized
        # again once shown (previously accuracy shrank into a corner and
        # the rest were scattered across the frame).
        acc_formula = MathTex(r"\text{Accuracy} = \frac{TP + TN}{\text{Total}}", font_size=26)
        acc_sub = MathTex(r"= \frac{15 + 70}{100} = 85\%", font_size=26)
        acc_group = VGroup(acc_formula, acc_sub).arrange(DOWN, buff=0.2)

        prec_formula = MathTex(r"\text{Precision}_{\text{fraud}} = \frac{TP}{TP + FP}", font_size=24)
        prec_sub = MathTex(r"= \frac{15}{15 + 5} = 0.75", font_size=24)
        prec_group = VGroup(prec_formula, prec_sub).arrange(DOWN, buff=0.2)

        rec_formula = MathTex(r"\text{Recall}_{\text{fraud}} = \frac{TP}{TP + FN}", font_size=24)
        rec_sub = MathTex(r"= \frac{15}{15 + 10} = 0.6", font_size=24)
        rec_group = VGroup(rec_formula, rec_sub).arrange(DOWN, buff=0.2)

        precision_val = 15 / 20
        recall_val = 15 / 25
        f_val = 2 * precision_val * recall_val / (precision_val + recall_val)
        f_formula = MathTex(
            r"F_{\text{fraud}} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}",
            font_size=22,
        )
        f_sub = MathTex(rf"= \frac{{2 (0.75)(0.6)}}{{0.75 + 0.6}} \approx {f_val:.2f}", font_size=22)
        f_group = VGroup(f_formula, f_sub).arrange(DOWN, buff=0.2)

        VGroup(acc_group, prec_group, rec_group, f_group).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.6 + DOWN * 0.2)

        with self.voiceover(
            text=(
                "For concreteness, let's think about the following confusion "
                "matrix from a fraud detection model. The two outcome classes "
                "respectively represent fraudulent transactions and non-fraudulent "
                "transaction."
            )
        ) as tracker:
            self.play(FadeOut(old_cm["group"]), FadeOut(old_cell_names), run_time=1)
            self.play(FadeIn(cm["group"]), run_time=2)
            self.wait(tracker.get_remaining_duration())

        acc_diag = VGroup(
            SurroundingRectangle(cm["cells"][0][0], color=CORRECT_COLOR, buff=0.03),
            SurroundingRectangle(cm["cells"][1][1], color=CORRECT_COLOR, buff=0.03),
        )

        with self.voiceover(
            text=(
                "From the confusion matrix, we can now define several common "
                "performance metrics. The first is accuracy: simply the "
                "percentage of correct predictions across all classes -- this is "
                "an overall measure of performance."
            )
        ) as tracker:
            self.play(Create(acc_diag), run_time=1.5)
            self.play(Write(acc_formula), run_time=1.5)
            self.play(Write(acc_sub), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(acc_diag))

        row_outline = SurroundingRectangle(
            VGroup(cm["cells"][0][0], cm["cells"][0][1]), color=YELLOW, buff=0.05
        )
        tp_highlight = SurroundingRectangle(cm["cells"][0][0], color=CORRECT_COLOR, buff=0.03)

        with self.voiceover(
            text=(
                "Beyond accuracy, there's precision and recall -- both "
                "class-specific measures, meaning they're defined separately for "
                "each class. Take the fraudulent class as an example. Precision "
                "of the fraudulent class asks: among all the predictions the "
                "model labeled fraudulent, what percentage were actually "
                "correct?"
            )
        ) as tracker:
            self.play(Create(row_outline), run_time=1.5)
            self.play(Create(tp_highlight), run_time=1)
            self.play(Write(prec_formula), run_time=1.5)
            self.play(Write(prec_sub), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(row_outline), FadeOut(tp_highlight))

        col_outline = SurroundingRectangle(
            VGroup(cm["cells"][0][0], cm["cells"][1][0]), color=YELLOW, buff=0.05
        )
        tp_highlight2 = SurroundingRectangle(cm["cells"][0][0], color=CORRECT_COLOR, buff=0.03)

        with self.voiceover(
            text=(
                "Meanwhile, recall of the fraudulent class asks: among all the "
                "data points that are actually fraudulent, what percentage did "
                "the model correctly catch? The key difference is the "
                "denominator: precision looks across all predictions of a "
                "class, while recall looks across all actual data points of "
                "that class. The same definitions apply for the non-fraudulent "
                "class."
            )
        ) as tracker:
            self.play(Create(col_outline), run_time=1.5)
            self.play(Create(tp_highlight2), run_time=1)
            self.play(Write(rec_formula), run_time=1.5)
            self.play(Write(rec_sub), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(col_outline), FadeOut(tp_highlight2))

        with self.voiceover(
            text=(
                "Because precision and recall capture different aspects of "
                "performance, we often combine them into a single number: the "
                "F-measure. Like precision and recall, it's a class-specific "
                "metric -- a particular way of averaging a class's precision and "
                "recall into one score."
            )
        ) as tracker:
            self.play(Indicate(prec_group, color=YELLOW), Indicate(rec_group, color=YELLOW), run_time=1.5)
            self.play(Write(f_formula), run_time=2)
            self.play(Write(f_sub), run_time=2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title_group), FadeOut(cm["group"]), FadeOut(acc_group),
            FadeOut(prec_group), FadeOut(rec_group), FadeOut(f_group),
        )


class Scene12(VoiceoverScene, Scene12Mixin):
    """Standalone preview: manim -pql scene_12.py Scene12"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_11()
        self.scene_12()

    def _fixture_scene_11(self):
        # Stand-in for scene_11's ending state (abstract Positive/Negative
        # confusion matrix with TP/FP/FN/TN labels) so scene_12 can be
        # previewed alone, without replaying scene_11.
        from common import make_confusion_matrix as _mcm

        title = Text("Prediction Performance Evaluation", font_size=32).to_edge(UP, buff=0.4)
        cm_title = Text(
            "Confusion Matrix: Binary Classification (Positive / Negative)", font_size=24, color=YELLOW
        ).next_to(title, DOWN, buff=0.35)
        cm = _mcm(("Predicted: Positive", "Predicted: Negative"), ("Positive", "Negative"))
        cm["group"].next_to(cm_title, DOWN, buff=0.55)
        names = ["True\nPositive", "False\nPositive", "False\nNegative", "True\nNegative"]
        cells_flat = [cm["cells"][0][0], cm["cells"][0][1], cm["cells"][1][0], cm["cells"][1][1]]
        colors = [CORRECT_COLOR, ERROR_COLOR, ERROR_COLOR, CORRECT_COLOR]
        cell_names = VGroup(
            *[
                Text(n, font_size=16, color=c).move_to(cell.get_center())
                for n, cell, c in zip(names, cells_flat, colors)
            ]
        )
        self.add(title, cm_title, cm["group"], cell_names)
        self.cm_title_group = VGroup(title, cm_title)
        self.cm = cm
        self.cm_cell_names = cell_names
