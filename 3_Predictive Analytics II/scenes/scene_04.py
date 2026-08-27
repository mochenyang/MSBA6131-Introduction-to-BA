import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text

VANILLA_COLOR = "#D9B36C"
CHOCOLATE_COLOR = "#5C3A21"
BOWL_A_COLOR = BLUE
BOWL_B_COLOR = PURPLE


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: Bayes' theorem refresher -- two bowls of cookies
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_make_bowl(label, n_vanilla, n_chocolate, color=WHITE):
        rim = Circle(radius=1.25, color=color, stroke_width=3)
        colors = [VANILLA_COLOR] * n_vanilla + [CHOCOLATE_COLOR] * n_chocolate
        random.Random(7).shuffle(colors)
        dots = VGroup(*[Dot(radius=0.08, color=c) for c in colors]).arrange_in_grid(rows=5, cols=8, buff=0.11)
        dots.move_to(rim.get_center())
        label_text = Text(label, font_size=22, color=color).next_to(rim, UP, buff=0.2)
        return VGroup(label_text, rim, dots)

    @staticmethod
    def scene4_belief_bar(p_a, height_scale=1.6):
        bar_a = Rectangle(width=0.4, height=max(p_a, 0.02) * height_scale, color=BOWL_A_COLOR, fill_opacity=0.85)
        bar_b = Rectangle(width=0.4, height=max(1 - p_a, 0.02) * height_scale, color=BOWL_B_COLOR, fill_opacity=0.85)
        bars = VGroup(bar_a, bar_b).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        label_a = Text("A", font_size=16, color=BOWL_A_COLOR).next_to(bar_a, DOWN, buff=0.1)
        label_b = Text("B", font_size=16, color=BOWL_B_COLOR).next_to(bar_b, DOWN, buff=0.1)
        return VGroup(bars, label_a, label_b), bar_a, bar_b

    @staticmethod
    def scene4_make_formula():
        """P(Bowl A | Vanilla) = [P(Vanilla | Bowl A) x P(Bowl A)] / P(Vanilla) -- the bowl-specific stand-in
        for common.make_bayes_formula's Ci/X version, previewing the same
        posterior/likelihood/prior/evidence layout used later in scene_05."""
        posterior = MathTex("P(\\text{Bowl A} \\mid \\text{Vanilla})")
        equals = MathTex("=")
        likelihood = MathTex("P(\\text{Vanilla} \\mid \\text{Bowl A})")
        times = MathTex("\\times")
        prior = MathTex("P(\\text{Bowl A})")
        numerator = VGroup(likelihood, times, prior).arrange(RIGHT, buff=0.25)
        evidence = MathTex("P(\\text{Vanilla})")
        frac_line = Line(LEFT, RIGHT, stroke_width=2.5)
        frac_group = VGroup(numerator, frac_line, evidence).arrange(DOWN, buff=0.22)
        frac_line.stretch_to_fit_width(max(numerator.width, evidence.width) + 0.35)
        full = VGroup(posterior, equals, frac_group).arrange(RIGHT, buff=0.4)

        posterior_label = Text("posterior", font_size=16, color=YELLOW).next_to(posterior, DOWN, buff=0.3)
        likelihood_label = Text("likelihood", font_size=16, color=YELLOW).next_to(likelihood, UP, buff=0.5)
        prior_label = Text("prior", font_size=16, color=YELLOW).next_to(prior, UP, buff=0.5)
        evidence_label = Text("evidence", font_size=16, color=YELLOW).next_to(evidence, DOWN, buff=0.3)
        return {
            "posterior": posterior, "equals": equals, "likelihood": likelihood, "times": times,
            "prior": prior, "evidence": evidence, "frac_line": frac_line, "numerator": numerator,
            "posterior_label": posterior_label, "likelihood_label": likelihood_label,
            "prior_label": prior_label, "evidence_label": evidence_label, "group": full,
        }

    def scene4_highlight(self, term, label, all_terms):
        others = [t for t in all_terms if t is not term]
        self.play(
            *[t.animate.set_opacity(0.35) for t in others],
            term.animate.set_color(YELLOW),
            FadeIn(label),
            run_time=1.2,
        )

    def scene_04(self):
        title = Text("A Quick Refresher: Bayes' Theorem", font_size=30).to_edge(UP, buff=0.4)
        bowl_a = self.scene4_make_bowl("Bowl A", 30, 10, color=BOWL_A_COLOR).scale(0.85).move_to(LEFT * 3.6 + UP * 1.5)
        bowl_b = self.scene4_make_bowl("Bowl B", 20, 20, color=BOWL_B_COLOR).scale(0.85).move_to(RIGHT * 3.6 + UP * 1.5)

        # -- Setup: introduce the two bowls -----------------------------
        with self.voiceover(
            text=(
                "You've probably seen Bayes' theorem before in a statistics or "
                "probability course — it relates the conditional probabilities "
                "of two random variables. Here's a puzzle that will give you "
                "the basic idea. Suppose there are two bowls of cookies. Bowl "
                "A has 30 vanilla cookies and 10 chocolate cookies; Bowl B has "
                "20 of each."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.wait(7.0)
            self.play(FadeIn(bowl_a, shift=UP * 0.2), run_time=1.5)
            self.play(FadeIn(bowl_b, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # -- The puzzle: blindfolded pick --------------------------------
        # A solid black disc over each bowl -- a literal "blindfold" -- so
        # dimming never touches the rim's own fill/stroke opacity (a plain
        # `.set_opacity()` on the bowl group would incorrectly fill in the
        # rim circle, since it forces fill_opacity up from its baseline 0).
        blindfold_a = Circle(
            radius=bowl_a[1].width / 2, color=BLACK, fill_opacity=0.9, stroke_width=0
        ).move_to(bowl_a[1].get_center())
        blindfold_b = Circle(
            radius=bowl_b[1].width / 2, color=BLACK, fill_opacity=0.9, stroke_width=0
        ).move_to(bowl_b[1].get_center())
        blindfold_q = Text("?", font_size=44, color=GREY_B).move_to(DOWN * 0.8)

        with self.voiceover(
            text=(
                "You are blindfolded, and you pick one of the two bowls at "
                "random, and then pick out a cookie."
            )
        ) as tracker:
            self.play(FadeIn(blindfold_a), FadeIn(blindfold_b), run_time=1.0)
            self.play(FadeIn(blindfold_q, scale=0.5), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        # -- Reveal: it's vanilla -----------------------------------------
        drawn_dot = Dot(radius=0.22, color=VANILLA_COLOR).move_to(blindfold_q.get_center())

        with self.voiceover(
            text=(
                "Next, you take off the blindfold, and find that the cookie "
                "is vanilla."
            )
        ) as tracker:
            self.play(FadeOut(blindfold_a), FadeOut(blindfold_b), run_time=1.0)
            self.play(FadeOut(blindfold_q), FadeIn(drawn_dot, scale=0.3), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        # -- Pose the question ----------------------------------------------
        question = Text("Bowl A  or  Bowl B?", font_size=24, color=YELLOW).move_to(DOWN * 1.7)

        with self.voiceover(
            text=(
                "The question is: how likely is it that you picked from Bowl "
                "A, versus Bowl B?"
            )
        ) as tracker:
            self.play(FadeIn(question, shift=UP * 0.15), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        # -- Show Bayes' theorem, precisely ---------------------------------
        formula = self.scene4_make_formula()
        # Scale/move the *whole* formula, labels included -- the labels were
        # positioned via next_to() against the terms' pre-transform spots, so
        # scaling/moving formula["group"] alone (which doesn't contain the
        # labels) would leave them stranded at their old coordinates while
        # the terms move away underneath them.
        formula_everything = VGroup(
            formula["group"], formula["posterior_label"], formula["likelihood_label"],
            formula["prior_label"], formula["evidence_label"],
        )
        formula_everything.scale(0.8).move_to(UP * 1.5)
        all_terms = [formula["posterior"], formula["likelihood"], formula["prior"], formula["evidence"]]

        with self.voiceover(
            text=(
                "Bayes' theorem gives us a precise way to answer this. It "
                "says: the probability we picked Bowl A, given that we saw a "
                "vanilla cookie — this is called the posterior — equals the probability of "
                "a vanilla cookie given Bowl A — this is called the likelihood — times the "
                "prior probability of Bowl A, divided by the overall "
                "probability of drawing a vanilla cookie — the evidence."
            )
        ) as tracker:
            self.play(
                FadeOut(bowl_a), FadeOut(bowl_b), FadeOut(drawn_dot), FadeOut(question), run_time=1.0
            )
            self.play(FadeIn(formula["posterior"]), run_time=1.0)
            self.play(FadeIn(formula["equals"]), run_time=0.5)
            self.play(FadeIn(formula["likelihood"]), run_time=0.9)
            self.play(FadeIn(formula["times"]), FadeIn(formula["prior"]), run_time=0.9)
            self.play(Create(formula["frac_line"]), FadeIn(formula["evidence"]), run_time=0.9)
            self.wait(1.0)
            self.scene4_highlight(formula["posterior"], formula["posterior_label"], all_terms)
            self.wait(3.0)
            self.scene4_highlight(formula["likelihood"], formula["likelihood_label"], all_terms)
            self.wait(3.0)
            self.scene4_highlight(formula["prior"], formula["prior_label"], all_terms)
            self.wait(3.0)
            self.play(
                *[t.animate.set_opacity(1).set_color(WHITE) for t in all_terms],
                FadeIn(formula["evidence_label"]),
                run_time=1.0,
            )
            self.wait(tracker.get_remaining_duration())

        self.play(
            *[FadeOut(formula[k]) for k in (
                "posterior_label", "likelihood_label", "prior_label", "evidence_label"
            )],
            formula["group"].animate.scale(0.85).to_edge(UP, buff=1.1),
            run_time=1.2,
        )

        # -- Worked calculation ---------------------------------------------
        row_a = MathTex(
            "P(\\text{Bowl A})", "\\times", "P(\\text{Vanilla} \\mid \\text{Bowl A})", "=", "0.5", "\\times", "0.75", "=", "0.375"
        ).scale(0.75).move_to(DOWN * 0.3)
        prior_label_a = Text("prior", font_size=15, color=YELLOW).next_to(row_a[4], DOWN, buff=0.2)
        likelihood_label_a = Text("likelihood", font_size=15, color=YELLOW).next_to(row_a[6], DOWN, buff=0.2)

        belief_bars_prior, bar_a, bar_b = self.scene4_belief_bar(0.5)
        belief_bars_prior.move_to(RIGHT * 5.6)
        belief_title_prior = Text("Belief", font_size=14, color=GREY_B).next_to(belief_bars_prior, UP, buff=0.15)

        with self.voiceover(
            text=(
                "Let's actually work out the number. Before drawing, the "
                "probability of Bowl A is 0.5 because you picked a bowl at random."
                "That reflects our prior belief. Given Bowl "
                "A, the probability of drawing a vanilla cookie is 0.75 — "
                "that's the likelihood. Multiplying them gives 0.375 "
            )
        ) as tracker:
            self.play(Write(row_a[:4]), run_time=1.3)
            self.play(FadeIn(belief_bars_prior), FadeIn(belief_title_prior), run_time=1.3)
            self.play(FadeIn(row_a[4]), FadeIn(prior_label_a), run_time=1.2)
            self.wait(5.0)
            self.play(FadeIn(row_a[5]), FadeIn(row_a[6]), FadeIn(likelihood_label_a), run_time=1.3)
            self.wait(2.0)
            self.play(FadeIn(row_a[7]), FadeIn(row_a[8]), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        row_b = MathTex(
            "P(\\text{Bowl B})", "\\times", "P(\\text{Vanilla} \\mid \\text{Bowl B})", "=", "0.5", "\\times", "0.5", "=", "0.25"
        ).scale(0.6).set_opacity(0.7).next_to(row_a, DOWN, buff=0.55, aligned_edge=LEFT)

        with self.voiceover(
            text=(
                "We do the same for Bowl B: prior 0.5, likelihood of vanilla "
                "0.5, giving 0.25."
            )
        ) as tracker:
            self.play(FadeIn(row_b, shift=UP * 0.15), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        sum_row = MathTex("P(\\text{Vanilla}) = ", "0.375", " + ", "0.25", " = ", "0.625").scale(0.75).next_to(
            row_b, DOWN, buff=0.55, aligned_edge=LEFT
        )
        total_label = Text("total probability, both bowls", font_size=14, color=GREY_B).next_to(
            sum_row, DOWN, buff=0.15
        )

        with self.voiceover(
            text=(
                "Adding these two together, 0.375 plus 0.25, gives 0.625 — "
                "the overall probability of drawing a vanilla cookie, "
                "regardless of which bowl it came from."
            )
        ) as tracker:
            self.play(
                TransformFromCopy(row_a[8], sum_row[1]),
                TransformFromCopy(row_b[8], sum_row[3]),
                FadeIn(sum_row[0]), FadeIn(sum_row[2]),
                run_time=1.8,
            )
            self.play(FadeIn(sum_row[4]), FadeIn(sum_row[5]), FadeIn(total_label), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        final_row = MathTex(
            "P(\\text{Bowl A} \\mid \\text{Vanilla}) = \\dfrac{0.375}{0.625} = ", "0.6"
        ).scale(0.8).next_to(sum_row, DOWN, buff=0.6, aligned_edge=LEFT)
        posterior_box = SurroundingRectangle(final_row[1], color=YELLOW, buff=0.12, corner_radius=0.06)
        posterior_label = Text("posterior", font_size=16, color=YELLOW).next_to(posterior_box, RIGHT, buff=0.2)

        with self.voiceover(
            text=(
                "Finally, to get the updated probability that we picked Bowl "
                "A given that we saw a vanilla cookie, we divide Bowl A's "
                "piece, 0.375, by the total, 0.625, which comes out to 0.6."
            )
        ) as tracker:
            self.play(FadeIn(final_row), run_time=2.0)
            self.wait(3.0)
            self.play(Create(posterior_box), FadeIn(posterior_label), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        new_bars, _, _ = self.scene4_belief_bar(0.6)
        new_bars.move_to(belief_bars_prior.get_center())

        with self.voiceover(
            text=(
                "So after seeing the vanilla cookie, we should believe "
                "there's a 60 percent chance we picked Bowl A — up from the 50% we "
                "believed before."
            )
        ) as tracker:
            self.play(Transform(belief_bars_prior, new_bars), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(formula["group"]), FadeOut(belief_title_prior), FadeOut(belief_bars_prior),
            FadeOut(row_a), FadeOut(prior_label_a), FadeOut(likelihood_label_a), FadeOut(row_b),
            FadeOut(sum_row), FadeOut(total_label), FadeOut(final_row), FadeOut(posterior_box), FadeOut(posterior_label),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
