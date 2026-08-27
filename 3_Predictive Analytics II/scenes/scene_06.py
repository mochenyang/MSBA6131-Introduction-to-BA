import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, make_bayes_formula, annotate_bayes_formula, make_factorized_likelihood

TABLE_CLASSES = ["C1", "C1", "C1", "C2", "C2"]
TABLE_X1 = ["Y", "N", "Y", "N", "Y"]  # categorical feature
TABLE_X2 = ["1.2", "3.4", "2.1", "0.5", "2.8"]  # numerical feature


class Scene06Mixin:
    # ------------------------------------------------------------------
    # Scene 6: estimating priors and (naive) likelihoods
    # ------------------------------------------------------------------
    @staticmethod
    def scene6_make_dataset_table():
        header = VGroup(Text("X1", font_size=16), Text("X2", font_size=16), Text("Class", font_size=16))
        rows = VGroup()
        for x1, x2, c in zip(TABLE_X1, TABLE_X2, TABLE_CLASSES):
            rows.add(VGroup(Text(x1, font_size=16), Text(x2, font_size=16), Text(c, font_size=16, color=YELLOW)))
        cols = VGroup(*[VGroup(header[i], *[r[i] for r in rows]) for i in range(3)])
        for col in cols:
            col.arrange(DOWN, buff=0.28)
        cols.arrange(RIGHT, buff=0.5)
        box = SurroundingRectangle(cols, color=WHITE, buff=0.25, corner_radius=0.1)
        return VGroup(box, cols), rows

    def scene_06(self):
        title = Text("Naive Bayes: Calculation Details", font_size=28).to_edge(UP, buff=0.4)
        table, rows = self.scene6_make_dataset_table()
        table.scale(0.85).move_to(LEFT * 4.6 + UP * 1.3)

        formula = self.bayes_formula_parts
        annot = self.bayes_formula_annot
        formula["group"].generate_target()
        formula["group"].target.scale(0.5).move_to(RIGHT * 4.3 + UP * 2.6)

        with self.voiceover(
            text=(
                "So how do we calculate the pieces we need, starting with the "
                "prior class probabilities?"
            )
        ) as tracker:
            self.play(Write(title), run_time=1.2)
            self.play(FadeIn(table, shift=UP * 0.2), run_time=1.0)
            # The "ignore the denominator" box/cross from scene_05 are
            # separate mobjects from formula["group"] -- fade them out
            # before moving the formula, or they're left behind on screen.
            self.play(FadeOut(annot["box"]), FadeOut(annot["cross"]), run_time=0.5)
            self.play(MoveToTarget(formula["group"]), run_time=0.9)
            self.wait(tracker.get_remaining_duration())

        brace = Brace(VGroup(rows[0], rows[1], rows[2]), LEFT)
        prior_formula = MathTex("\\dfrac{\\text{count}(C_1)}{\\text{total}} = \\dfrac{3}{5} = 0.6").scale(0.65).next_to(
            table, DOWN, buff=0.35
        )

        with self.voiceover(
            text=(
                "One straightforward, data-driven way to get the probability "
                "of class Ci is to estimate it from the training data: take "
                "the number of data points in Ci and divide by the total "
                "size of the training data. This approximates the "
                "probability of being in Ci regardless of feature values. If "
                "training data is somehow insufficient or unreliable, people "
                "sometimes also estimate this from domain knowledge, or "
                "simply assume a uniform probability across classes."
            )
        ) as tracker:
            self.play(formula["prior"].animate.set_color(YELLOW), run_time=1.0)
            self.play(Create(brace), run_time=1.0)
            self.wait(3.0)
            self.play(FadeIn(prior_formula, shift=UP * 0.15), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(formula["prior"].animate.set_color(WHITE), run_time=0.6)

        feature_boxes = VGroup(*[
            VGroup(Square(0.55, color=WHITE), Text(f"x{i}", font_size=16)) for i in range(1, 4)
        ])
        for box in feature_boxes:
            box[1].move_to(box[0].get_center())
        # buff=0.8 (not the tighter spacing you'd use for the boxes alone)
        # leaves enough room for the wider factorized MathTex terms placed
        # under each box below -- a tighter buff makes adjacent terms overlap.
        feature_boxes.arrange(RIGHT, buff=0.8).move_to(DOWN * 1.0 + RIGHT * 1.0)
        x_label = Text("X = (x1, x2, x3)", font_size=18, color=GREY_B).next_to(feature_boxes, UP, buff=0.3)

        with self.voiceover(
            text=(
                "Next, how do we estimate the likelihood — the probability "
                "of observing X given class Ci? By definition, we could "
                "estimate it by counting the fraction of data points with "
                "exactly features X among those in class Ci. But when there "
                "are many features, this becomes computationally very "
                "costly, because we'd need to locate one very specific "
                "feature vector among many many possible combinations."
            )
        ) as tracker:
            self.play(formula["likelihood"].animate.set_color(YELLOW), run_time=1.0)
            self.play(FadeIn(x_label), FadeIn(feature_boxes, lag_ratio=0.1), run_time=1.5)
            self.wait(1.0)

            root_pt = feature_boxes.get_bottom() + DOWN * 0.5
            mid_pts = [root_pt + DOWN * 0.7 + RIGHT * dx for dx in (-1.4, -0.5, 0.5, 1.4)]
            leaf_pts = [m + DOWN * 0.6 + RIGHT * dx for m in mid_pts for dx in (-0.25, 0.25)]
            branch_lines = VGroup(*[Line(root_pt, m, color=GREY_B, stroke_width=1.5) for m in mid_pts])
            leaf_lines = VGroup(*[
                Line(mid_pts[i], leaf_pts[2 * i + j], color=GREY_B, stroke_width=1.5)
                for i in range(4) for j in range(2)
            ])
            explode_label = Text("exponentially many combinations", font_size=15, color=RED).next_to(
                VGroup(branch_lines, leaf_lines), DOWN, buff=0.15
            )
            cross = Cross(VGroup(branch_lines, leaf_lines), color=RED, stroke_width=4)
            self.play(Create(branch_lines), Create(leaf_lines), run_time=1.3)
            self.play(FadeIn(explode_label), run_time=0.8)
            self.play(Create(cross), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        factorized = make_factorized_likelihood(k=3)
        for i, term in enumerate(factorized["terms"]):
            term.scale(0.6).next_to(feature_boxes[i], DOWN, buff=1.6)
        for i, sign in enumerate(factorized["signs"]):
            sign.scale(0.6).move_to(
                (factorized["terms"][i].get_right() + factorized["terms"][i + 1].get_left()) / 2
            )
        cci_label = Text("Class-Conditional Independence", font_size=16, color=YELLOW).next_to(
            VGroup(*factorized["terms"]), DOWN, buff=0.3
        )

        with self.voiceover(
            text=(
                "To deal with this, Naive Bayes makes a \"naive\" assumption "
                "— class-conditional independence: conditional on the class "
                "label Ci, the features are assumed independent of each "
                "other. This lets us rewrite the probability of the whole "
                "feature vector X given Ci as the product of the conditional "
                "probabilities of each individual feature given Ci. The "
                "assumption is unrealistic in many settings — this is "
                "actually where Naive Bayes gets its name — but it turns an "
                "exponentially complex computation into a simple "
                "multiplication of individual probabilities, each of which "
                "is easy to estimate from data."
            )
        ) as tracker:
            self.play(FadeOut(branch_lines), FadeOut(leaf_lines), FadeOut(explode_label), FadeOut(cross), run_time=1.0)
            self.play(
                *[TransformFromCopy(feature_boxes[i], factorized["terms"][i]) for i in range(3)],
                run_time=1.8,
            )
            self.play(*[FadeIn(s) for s in factorized["signs"]], FadeIn(cci_label), run_time=1.2)
            self.play(formula["likelihood"].animate.set_color(WHITE), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        target_term = factorized["terms"][0]
        self.play(
            FadeOut(title), FadeOut(table), FadeOut(brace), FadeOut(prior_formula), FadeOut(x_label),
            FadeOut(feature_boxes), FadeOut(cci_label), FadeOut(formula["group"]),
            FadeOut(factorized["terms"][1]), FadeOut(factorized["terms"][2]), FadeOut(VGroup(*factorized["signs"])),
        )

        # -- Act 2: estimating one feature's conditional probability --------
        title2 = Text("Estimating a Single Feature's Likelihood", font_size=26).to_edge(UP, buff=0.4)

        with self.voiceover(
            text=(
                "Now the question of estimating the likelihood term becomes "
                "how do we estimate the conditional probability of one "
                "specific feature value, xk, given class Ci. If the feature "
                "is categorical, this is easy: we simply find the fraction "
                "of data points in class Ci that have feature value xk."
            )
        ) as tracker:
            self.play(FadeIn(title2), run_time=1.2)
            self.play(target_term.animate.move_to(UP * 1.6 + LEFT * 3.5).scale(1.4), run_time=1.3)
            highlight_box = SurroundingRectangle(target_term, color=YELLOW, buff=0.1)
            self.play(Create(highlight_box), run_time=1.0)
            cat_table, cat_rows = self.scene6_make_dataset_table()
            cat_table.scale(0.75).move_to(UP * 1.6 + RIGHT * 2.5)
            self.play(FadeIn(cat_table), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        frac_expr = MathTex(
            "P(x_1{=}Z \\mid C_1) = \\dfrac{\\text{count}(x_1{=}Z, C_1)}{\\text{count}(C_1)} = \\dfrac{0}{3}"
        ).scale(0.6).move_to(DOWN * 0.6)
        zero_big = Text("0", font_size=60, color=RED).next_to(frac_expr, DOWN, buff=0.3)

        with self.voiceover(
            text=(
                "One issue to watch for: what if that fraction happens to be "
                "zero — no data points in class Ci have feature value xk? "
                "Then the entire likelihood calculation, which is a product, "
                "collapses to zero."
            )
        ) as tracker:
            self.play(FadeIn(frac_expr), run_time=1.5)
            self.play(FadeIn(zero_big, scale=1.5), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        laplace_expr = MathTex(
            "\\dfrac{0 + 1}{3 + 2} = 0.2"
        ).scale(0.75).next_to(frac_expr, DOWN, buff=0.5)
        laplace_label = Text("Laplace correction", font_size=16, color=YELLOW).next_to(laplace_expr, DOWN, buff=0.2)

        with self.voiceover(
            text=(
                "The fix is called Laplace correction: we simply add small "
                "non-zero values to both the numerator and denominator of "
                "the fraction."
            )
        ) as tracker:
            self.play(FadeOut(zero_big), run_time=0.6)
            self.play(FadeIn(laplace_expr, shift=UP * 0.15), FadeIn(laplace_label), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(frac_expr), FadeOut(laplace_expr), FadeOut(laplace_label),
            FadeOut(cat_table), FadeOut(highlight_box),
        )

        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1, 0.5], x_length=6, y_length=2.2,
            axis_config={"include_ticks": False},
        ).move_to(DOWN * 1.0)
        x2_dot_vals = [1.2, 3.4, 2.1, 0.5, 2.8]
        num_dots = VGroup(*[Dot(axes.coords_to_point(v, 0), color=GREY_B, radius=0.06) for v in x2_dot_vals])
        num_label = Text("Feature x2 (numerical)", font_size=16, color=GREY_B).next_to(axes, UP, buff=0.15)

        bins = VGroup(*[
            Rectangle(width=axes.x_length / 3, height=0.5, color=BLUE, fill_opacity=0.25, stroke_width=1)
            .move_to(axes.coords_to_point(1 + 2 * i, 0.25))
            for i in range(3)
        ])
        bin_label = Text("discretize into bins", font_size=15, color=BLUE).next_to(axes, DOWN, buff=0.2)

        with self.voiceover(
            text=(
                "If the feature is numerical, we can't compute a simple "
                "fraction, since it can take infinitely many possible "
                "values. In that case, we either discretize the feature and "
                "treat it as categorical, or assume it follows some "
                "distribution and use that distribution's density function "
                "to compute the conditional probability."
            )
        ) as tracker:
            self.play(FadeIn(num_label), Create(axes), run_time=1.3)
            self.play(FadeIn(num_dots, lag_ratio=0.1), run_time=1.0)
            self.play(FadeIn(bins), FadeIn(bin_label), run_time=1.3)
            self.wait(1.0)

            curve = axes.plot(lambda x: 0.9 * np.exp(-((x - 2.2) ** 2) / 1.2), color=GREEN, x_range=[0, 6])
            density_label = Text("or a density curve", font_size=15, color=GREEN).next_to(bin_label, DOWN, buff=0.15)
            highlight_x = 2.1
            dashed = DashedLine(
                axes.coords_to_point(highlight_x, 0), axes.coords_to_point(highlight_x, 0.9 * np.exp(-((highlight_x - 2.2) ** 2) / 1.2)),
                color=GREEN,
            )
            self.play(FadeOut(bins), FadeOut(bin_label), Create(curve), FadeIn(density_label), run_time=1.5)
            self.play(Create(dashed), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title2), FadeOut(target_term), FadeOut(highlight_box), FadeOut(axes), FadeOut(num_dots),
            FadeOut(num_label), FadeOut(curve), FadeOut(density_label), FadeOut(dashed),
        )

        # Stash for scene_07 (append an irrelevant-feature term).
        self.factorized_likelihood = factorized


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_05()
        self.scene_06()

    def _fixture_scene_05(self):
        # Stand-in for scene_05's ending state (Bayes formula, denominator
        # already greyed/crossed, numerator boxed) so scene_06 can be
        # previewed alone.
        parts = make_bayes_formula()
        # Match scene_05's real end-state transform (scale 1.3, moved to
        # UP * 0.8) so this fixture's formula sits where the combined-run
        # version would actually be by the time scene_06 picks it up.
        VGroup(
            parts["group"], parts["posterior_label"], parts["likelihood_label"],
            parts["prior_label"], parts["evidence_label"],
        ).scale(1.3).move_to(UP * 0.8)
        annot = annotate_bayes_formula(parts)
        parts["evidence"].set_color(GREY_B)
        # The formula's own text (parts["group"]) needs adding too -- in the
        # combined run it's already on screen by the time scene_06 starts
        # (scene_05 faded it in), but a fixture has to add it explicitly or
        # scene_06's opening beat plays out with just the empty annotation
        # box/cross and no formula inside it.
        self.add(parts["group"], annot["cross"], annot["box"])
        self.bayes_formula_parts = parts
        self.bayes_formula_annot = annot
