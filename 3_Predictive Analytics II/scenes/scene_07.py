import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, CLASS1_COLOR, CLASS0_COLOR, make_factorized_likelihood, make_knn_visual


class Scene07Mixin:
    # ------------------------------------------------------------------
    # Scene 7: two closing remarks on Naive Bayes
    # ------------------------------------------------------------------
    def scene_07(self):
        title = Text("Naive Bayes: Two Remarks", font_size=28).to_edge(UP, buff=0.4)
        bullet1 = Text("1. Irrelevant features don't hurt predictions", font_size=24).move_to(LEFT * 3.0 + UP * 2.0)
        bullet2 = Text(
            "2. Rankings stay accurate even when probabilities themselves are off", font_size=24).next_to(bullet1, DOWN, buff=0.9, aligned_edge=LEFT)

        with self.voiceover(
            text=(
                "I want to conclude the discussion of Naive Bayes on two "
                "remarks."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        factorized = self.factorized_likelihood
        terms, signs = factorized["terms"], factorized["signs"]
        ordered = [terms[0], signs[0], terms[1], signs[1], terms[2]]
        prod_group = VGroup(*ordered).copy().arrange(RIGHT, buff=0.22).scale(0.8).move_to(UP * 0.5)
        x0_term = MathTex("\\times", "P(x_0 \\mid C_i)").scale(0.8).next_to(prod_group, RIGHT, buff=0.22)
        x0_label = Text("same value for every class", font_size=14, color=YELLOW).next_to(x0_term, DOWN, buff=0.15)        

        with self.voiceover(
            text=(
                "First, Naive Bayes has a property that not every predictive "
                "technique enjoys: having irrelevant features in the data "
                "doesn't hurt its predictive performance. Imagine x0 is an "
                "irrelevant feature — one that carries no useful information "
                "for prediction. Then the conditional probability of x0 given class Ci "
                "should be roughly the same across all classes, so "
                "multiplying it into the likelihood doesn't change which "
                "class has the highest probability, and it doesn't affect "
                "the prediction. "
                "This robustness sets Naive Bayes apart from models like "
                "k-NN, which can be vulnerable to irrelevant features."
            )
        ) as tracker:
            self.play(FadeIn(bullet1, shift=RIGHT * 0.2), run_time=1.2)
            self.wait(5.0)
            self.play(FadeIn(prod_group, shift=UP * 0.2), run_time=1.5)
            self.wait(2.0)
            self.play(FadeIn(x0_term), run_time=1.2)
            self.play(Indicate(x0_term, color=YELLOW), run_time=1.2)
            self.wait(4.0)
            self.play(FadeIn(x0_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())
               
        self.play(
            FadeOut(prod_group), FadeOut(x0_term), FadeOut(x0_label),
        )

        PRED_COLOR = RED
        TRUE_COLOR = TEAL
        pred_bars = VGroup(*[
            Rectangle(width=0.5, height=h, color=PRED_COLOR, fill_opacity=0.85)
            for h in (1.8, 1.2, 0.6)
        ])
        true_bars = VGroup(*[
            Rectangle(width=0.5, height=h, color=TRUE_COLOR, fill_opacity=0.85)
            for h in (1.5, 1.35, 0.75)
        ])
        # Each class gets its own true/predicted pair, side by side, instead
        # of the two bars sharing a center and overlapping.
        bars_group = VGroup(*[
            VGroup(t, p).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
            for t, p in zip(true_bars, pred_bars)
        ]).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        rank_label = Text("ranking preserved", font_size=18, color=YELLOW).next_to(
            bullet2, DOWN, buff=0.5, aligned_edge=LEFT
        )
        bars_group.next_to(rank_label, DOWN, buff=0.4, aligned_edge=LEFT)
        bar_labels = VGroup(*[Text(f"C{i+1}", font_size=16).next_to(bars_group[i], DOWN, buff=0.15) for i in range(3)])
        legend = VGroup(
            Text("predicted probabilities", font_size=14, color=PRED_COLOR),
            Text("true probabilities", font_size=14, color=TRUE_COLOR),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(bars_group, RIGHT, buff=0.5)
        # Shift the whole assembly horizontally only (set_x leaves y alone)
        # so it's centered on screen instead of left-aligned under bullet2.
        VGroup(rank_label, bars_group, bar_labels, legend).set_x(0)

        with self.voiceover(
            text=(
                "Second, the class-independence assumption can make Naive "
                "Bayes' probability predictions inaccurate, but the rankings "
                "of those probabilities are often still reasonably good. "
                "This is a big part of why Naive Bayes still works well in "
                "practice despite the unrealistic assumption behind it."
            )
        ) as tracker:
            self.play(FadeIn(bullet2, shift=RIGHT * 0.2), run_time=1.3)
            self.wait(4.0)
            self.play(FadeIn(true_bars, lag_ratio=0.1), run_time=1.3)
            self.play(FadeIn(pred_bars, lag_ratio=0.1), FadeIn(bar_labels), FadeIn(legend), run_time=1.5)
            self.play(FadeIn(rank_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(bullet1), FadeOut(bullet2), FadeOut(bars_group), FadeOut(bar_labels),
            FadeOut(legend), FadeOut(rank_label),
        )


class Scene07(VoiceoverScene, Scene07Mixin):
    """Standalone preview: manim -pql scene_07.py Scene07"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_06()
        self.scene_07()

    def _fixture_scene_06(self):
        # Stand-in for scene_06's factorized-likelihood product so scene_07
        # can be previewed alone.
        self.factorized_likelihood = make_factorized_likelihood(k=3)
