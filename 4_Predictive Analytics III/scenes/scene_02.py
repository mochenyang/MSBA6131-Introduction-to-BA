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
    make_ranked_table,
    make_cutoff_line,
    predicted_labels_for_cutoff,
    make_confusion_matrix,
    confusion_matrix_texts,
)


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: recap of probability predictions, and the effect of the
    # cutoff value on classification results
    # ------------------------------------------------------------------
    @staticmethod
    def scene2_recap_visual():
        formula = MathTex("P(\\text{Class} \\mid X)", font_size=44)
        note = Text("predicted class probability", font_size=20, color=GREY_B).next_to(formula, DOWN, buff=0.3)
        num_line = NumberLine(x_range=[0, 1, 0.25], length=6.5, include_numbers=True, font_size=18)
        num_line.next_to(VGroup(formula, note), DOWN, buff=0.9)
        marker = Triangle(fill_opacity=1, color=RED, stroke_width=0).scale(0.14).rotate(PI)
        marker.next_to(num_line.n2p(0.5), UP, buff=0.02)
        cutoff_label = Text("Cutoff", font_size=16, color=RED).next_to(marker, UP, buff=0.12)
        group = VGroup(formula, note, num_line, marker, cutoff_label).move_to(ORIGIN)
        return {
            "formula": formula, "note": note, "num_line": num_line,
            "marker": marker, "cutoff_label": cutoff_label, "group": group,
        }

    def scene_02(self):
        title = Text("Probability Cutoff and Classifier Performance", font_size=26).to_edge(UP, buff=0.4)
        recap = self.scene2_recap_visual()

        with self.voiceover(
            text=(
                "As a quick reminder, many classification algorithms, "
                "including k-NN, decision tree, and naive Bayes, produce "
                "not only categorical predictions but also class "
                "probability predictions. Categorical predictions are generated "
                "from these probabilities using a user-chosen cutoff, "
                "and a higher predicted probability means the classifier "
                "is more certain about its prediction."
                "The choice of the cutoff value has some interesting "
                "implications, because classification results can look "
                "different under different cutoff values."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.0)
            self.wait(3.0)
            self.play(Write(recap["formula"]), run_time=1.5)
            self.play(FadeIn(recap["note"], shift=UP * 0.15), run_time=1.5)
            self.wait(3.0)
            self.play(Create(recap["num_line"]), run_time=1.3)
            self.play(FadeIn(recap["marker"]), FadeIn(recap["cutoff_label"]), run_time=1.0)
            self.wait(10.0)
            # A plain horizontal shift (not move_to/next_to, which recompute
            # each mobject's position from its own height and a hardcoded
            # buff) -- that mismatch was making the marker drift up and the
            # label drift down instead of both sliding sideways together.
            shift_x = recap["num_line"].n2p(0.7)[0] - recap["num_line"].n2p(0.5)[0]
            self.play(
                recap["marker"].animate.shift(RIGHT * shift_x),
                recap["cutoff_label"].animate.shift(RIGHT * shift_x),
                run_time=2.0,
            )
            self.wait(1.0)
            shift_x = recap["num_line"].n2p(0.7)[0] - recap["num_line"].n2p(0.25)[0]
            self.play(
                recap["marker"].animate.shift(LEFT * shift_x),
                recap["cutoff_label"].animate.shift(LEFT * shift_x),
                run_time=2.0,
            )
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(recap["group"]), run_time=0.8)

        table = make_ranked_table()
        table["group"].move_to(LEFT * 4.3)

        cm = make_confusion_matrix()
        cm["group"].move_to(RIGHT * 3.3 + UP * 0.4)

        with self.voiceover(
            text=(                
                "Take this table as an example: 10 data points with their actual "
                "class labels and predicted probability of being in the "
                "positive class, ranked from high to low. Picking "
                "different cutoff values gives different classification "
                "results. If we pick the default cutoff of 0.5, all 10 "
                "records are predicted positive. The classifier has 60% accuracy. "
                "If we instead pick a higher cutoff, say 0.8, only the top 7 records — the "
                "ones with probability higher than 0.8 — are predicted "
                "positive, and the classifier has 70% accuracy. "
                "The cutoff controls how aggressive or "
                "conservative the classifier behaves: a high cutoff "
                "means the classifier needs to be very certain before "
                "predicting positive, while a low cutoff lets it predict "
                "positive with relatively low confidence."
            )
        ) as tracker:
            self.play(FadeIn(table["group"]), run_time=1.5)

            cutoff_line = make_cutoff_line(table, 10)
            # Anchored off the line's right endpoint (the gap between the
            # table and the confusion matrix), not next_to(line, DOWN) --
            # the line spans the whole table width, so a label centered
            # under its midpoint lands squarely on the "Pred. Prob." column.
            cutoff_label = Text("Cutoff = 0.5", font_size=16, color=ERROR_COLOR).next_to(
                cutoff_line.get_right(), RIGHT, buff=0.15
            )
            pred_labels = predicted_labels_for_cutoff(table, 10)
            self.wait(12.0)
            self.play(Create(cutoff_line), FadeIn(cutoff_label), run_time=1.2)
            self.wait(1.0)
            self.play(*[FadeIn(lbl) for lbl in pred_labels], run_time=1.3)
            self.wait(1.5)
            cm_texts = confusion_matrix_texts(cm, 10)
            self.play(FadeIn(cm["group"]), *[FadeIn(t) for t in cm_texts.values()], run_time=1.0)            
            self.wait(5.0)

            new_cutoff_line = make_cutoff_line(table, 7)
            new_cutoff_label = Text("Cutoff = 0.8", font_size=16, color=ERROR_COLOR).next_to(
                new_cutoff_line.get_right(), RIGHT, buff=0.15
            )
            new_pred_labels = predicted_labels_for_cutoff(table, 7)
            new_cm_texts = confusion_matrix_texts(cm, 7)
            self.play(
                Transform(cutoff_line, new_cutoff_line),
                Transform(cutoff_label, new_cutoff_label),
                *[Transform(pred_labels[i], new_pred_labels[i]) for i in range(len(pred_labels))],
                *[Transform(cm_texts[key], new_cm_texts[key]) for key in cm_texts],
                run_time=1.8,
            )
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(table["group"]), FadeOut(cm["group"]), FadeOut(cutoff_line),
            FadeOut(cutoff_label), *[FadeOut(lbl) for lbl in pred_labels],
            *[FadeOut(t) for t in cm_texts.values()],
        )

        # Stash for scene_03 (same table reused for the full ROC sweep) and
        # scene_08's summary fixture.
        self.scene02_table = table


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_02()
