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
        title = Text("Naive Bayes: Calculation Details", font_size=28).to_edge(UP, buff=0.4)
        bullet1 = Text("1. Irrelevant features don't hurt predictions", font_size=20).move_to(LEFT * 4.0 + UP * 2.0)
        bullet2 = Text(
            "2. Rankings stay accurate even when\n   probabilities themselves are off", font_size=20, line_spacing=1.2
        ).next_to(bullet1, DOWN, buff=0.9, aligned_edge=LEFT)

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
        prod_group = VGroup(*ordered).copy().arrange(RIGHT, buff=0.22).scale(0.9).move_to(RIGHT * 1.5 + UP * 1.8)

        with self.voiceover(
            text=(
                "First, Naive Bayes has a property that not every predictive "
                "technique enjoys: having irrelevant features in the data "
                "doesn't hurt its predictive performance. Imagine x0 is an "
                "irrelevant feature — one that carries no useful information "
                "for prediction."
            )
        ) as tracker:
            self.play(FadeIn(bullet1, shift=RIGHT * 0.2), run_time=1.2)
            self.play(FadeIn(prod_group, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        x0_term = MathTex("\\times", "P(x_0 \\mid C_i)").scale(0.9).next_to(prod_group, RIGHT, buff=0.22)
        mini_bars = VGroup(*[
            VGroup(
                Rectangle(width=0.4, height=0.55 + 0.02 * i, color=GREY_B, fill_opacity=0.8),
                Text(f"C{i+1}", font_size=13),
            ).arrange(DOWN, buff=0.08)
            for i in range(3)
        ]).arrange(RIGHT, buff=0.3).next_to(x0_term, DOWN, buff=0.4)
        mini_label = Text("~ same value for every class", font_size=14, color=GREY_B).next_to(mini_bars, DOWN, buff=0.15)

        winner_before = VGroup(
            Rectangle(width=0.5, height=1.4, color=CLASS1_COLOR, fill_opacity=0.85),
            Text("C1", font_size=14),
        ).arrange(DOWN, buff=0.1)
        loser_before = VGroup(
            Rectangle(width=0.5, height=0.8, color=CLASS0_COLOR, fill_opacity=0.85),
            Text("C2", font_size=14),
        ).arrange(DOWN, buff=0.1)
        scores_before = VGroup(winner_before, loser_before).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).next_to(
            prod_group, DOWN, buff=2.2
        ).align_to(prod_group, LEFT)
        win_box = SurroundingRectangle(winner_before, color=YELLOW, buff=0.08)
        score_label = Text("score = likelihood x prior", font_size=14, color=GREY_B).next_to(scores_before, UP, buff=0.15)

        with self.voiceover(
            text=(
                "Then the conditional probability of x0 given class Ci "
                "should be roughly the same across all classes, so "
                "multiplying it into the likelihood doesn't change which "
                "class has the highest probability, and it doesn't affect "
                "the prediction."
            )
        ) as tracker:
            self.play(FadeIn(x0_term), run_time=1.0)
            self.play(FadeIn(mini_bars, lag_ratio=0.1), FadeIn(mini_label), run_time=1.3)
            self.wait(0.5)
            self.play(FadeIn(score_label), FadeIn(scores_before), run_time=1.2)
            self.play(Create(win_box), run_time=1.0)
            self.play(
                scores_before.animate.scale(0.85), win_box.animate.scale(0.85).move_to(winner_before.get_center()),
                run_time=1.2,
            )
            self.wait(tracker.get_remaining_duration())

        knn = make_knn_visual()
        knn["group"].scale(0.55).move_to(LEFT * 4.5 + DOWN * 1.6)

        with self.voiceover(
            text=(
                "This robustness sets Naive Bayes apart from models like "
                "k-NN, which can be vulnerable to irrelevant features."
            )
        ) as tracker:
            self.play(FadeIn(knn["group"], shift=UP * 0.2), run_time=1.3)
            shifted_new_dot = knn["new_dot"].copy().shift(RIGHT * 1.3 + DOWN * 0.3)
            flipped_circle = Circle(radius=1.05, color=WHITE, stroke_width=2.2).move_to(shifted_new_dot.get_center())
            self.play(
                Transform(knn["new_dot"], shifted_new_dot),
                Transform(knn["neighbor_circle"], flipped_circle),
                run_time=1.5,
            )
            self.play(knn["new_dot"].animate.set_color(CLASS0_COLOR), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(prod_group), FadeOut(x0_term), FadeOut(mini_bars), FadeOut(mini_label),
            FadeOut(scores_before), FadeOut(win_box), FadeOut(score_label), FadeOut(knn["group"]),
        )

        pred_bars = VGroup(*[
            Rectangle(width=0.6, height=h, color=WHITE, fill_opacity=0.85)
            for h in (1.8, 1.2, 0.6)
        ]).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        true_bars = VGroup(*[
            Rectangle(width=0.6, height=h, color=GREY_B, fill_opacity=0.25, stroke_opacity=0.5)
            for h in (1.5, 1.35, 0.75)
        ]).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        true_bars.move_to(pred_bars.get_center())
        bars_group = VGroup(true_bars, pred_bars).move_to(RIGHT * 1.5 + UP * 0.3)
        bar_labels = VGroup(*[Text(f"C{i+1}", font_size=16).next_to(pred_bars[i], DOWN, buff=0.15) for i in range(3)])
        legend = VGroup(
            Text("predicted", font_size=14, color=WHITE),
            Text("true", font_size=14, color=GREY_B),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(bars_group, RIGHT, buff=0.5)
        rank_label = Text("ranking preserved", font_size=18, color=YELLOW).next_to(bars_group, UP, buff=0.4)

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
