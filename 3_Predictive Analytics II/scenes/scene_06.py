import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, ERROR_COLOR, make_bayes_formula, annotate_bayes_formula, make_factorized_likelihood

TABLE_CLASSES = ["C1", "C1", "C1", "C2", "C2"]
TABLE_X1 = ["1", "0", "1", "0", "1"]  # binary/categorical feature
TABLE_XK = ["1.2", "3.4", "2.1", "0.5", "2.8"]  # continuous feature

# The formula lives permanently centered under the title at this height --
# it never shrinks or moves to a corner. Growing wider later (when the
# likelihood term is replaced by the factorized product) just re-centers
# around this same x=0/y=FORMULA_Y spot.
FORMULA_Y = 2.15


class Scene06Mixin:
    # ------------------------------------------------------------------
    # Scene 6: estimating priors and (naive) likelihoods
    # ------------------------------------------------------------------
    @staticmethod
    def scene6_make_dataset_table():
        # Built as a flat grid (arrange_in_grid), not per-column .arrange(DOWN)
        # -- Text's bounding box crops to ink extent, and "⋯" has far less
        # vertical ink than a digit/letter, so arranging each column
        # independently made the dots column's cumulative row spacing drift
        # out of alignment with the other columns by the last row.
        header = [
            MathTex("X_1").scale(0.55), Text("⋯", font_size=16),
            MathTex("X_k").scale(0.55), Text("Class", font_size=16),
        ]
        row_cells = [
            [
                Text(x1, font_size=16), Text("⋯", font_size=16, color=GREY_B),
                Text(xk, font_size=16), Text(c, font_size=16, color=YELLOW),
            ]
            for x1, xk, c in zip(TABLE_X1, TABLE_XK, TABLE_CLASSES)
        ]
        all_cells = header + [cell for row in row_cells for cell in row]
        grid = VGroup(*all_cells).arrange_in_grid(rows=6, cols=4, buff=(0.5, 0.28))
        rows = VGroup(*[VGroup(*r) for r in row_cells])
        cols = VGroup(*[VGroup(header[i], *[r[i] for r in row_cells]) for i in range(4)])
        box = SurroundingRectangle(grid, color=WHITE, buff=0.25, corner_radius=0.1)
        table_title = Text("Training Data", font_size=18, color=GREY_B).next_to(box, UP, buff=0.2)
        group = VGroup(table_title, box, grid)
        return {
            "group": group, "title": table_title, "box": box, "cols": cols, "header": VGroup(*header),
            "rows": rows,
            "x1_col": cols[0], "dots_col": cols[1], "xk_col": cols[2], "class_col": cols[3],
        }

    @staticmethod
    def scene6_center_formula(mobj):
        """Re-center mobj at x=0, FORMULA_Y -- used whenever the formula's
        width changes, so it grows symmetrically in place, not off-screen."""
        mobj.move_to([0, FORMULA_Y, 0])

    def scene6_singled_out_copy(self, source_term, anchor):
        """A large, boxed copy of a factorized term (kept invisible in the
        compact formula) sprung out to `anchor` for a close-up walkthrough."""
        big = source_term.copy().scale(1.8).move_to(anchor)
        box = SurroundingRectangle(big, color=YELLOW, buff=0.15)
        return big, box

    def scene_06(self):
        title = Text("Naive Bayes: Calculation Details", font_size=28).to_edge(UP, buff=0.4)
        formula = self.bayes_formula_parts

        with self.voiceover(
            text=(
                "So how do we get the different pieces in order to "
                "calculate the posterior probabilities?"
            )
        ) as tracker:
            self.play(Write(title), run_time=1.0)

            # Fresh reveal -- not a leftover carried in from scene_05 (which
            # now fades everything out at its own end) -- big, centered right
            # under the title, and it stays there for the whole scene (no
            # shrink-to-corner). annot is rebuilt from scratch here (rather
            # than reusing scene_05's), since it's tied to this position.
            formula["group"].scale_to_fit_width(7.0)
            self.scene6_center_formula(formula["group"])
            annot = annotate_bayes_formula(formula)
            self.bayes_formula_annot = annot
            formula_display = VGroup(formula["group"], annot["cross"])
            self.play(FadeIn(formula_display, scale=0.8), run_time=1.0)

            self.wait(tracker.get_remaining_duration())

        # -- Prior: count(Ci) / total, highlighted against the Class column --
        tbl = self.scene6_make_dataset_table()
        table, rows = tbl["group"], tbl["rows"]
        table.move_to(LEFT * 3.8 + DOWN * 1.3)
        class_box = SurroundingRectangle(tbl["class_col"], color=YELLOW, buff=0.1)
        prior_formula = MathTex(
            "\\text{e.g., } P(C_1) = \\dfrac{\\text{count}(C_1)}{\\text{total}} = \\dfrac{3}{5} = 0.6"
        ).scale(0.7).next_to(table, RIGHT, buff=0.5)

        with self.voiceover(
            text=(
                "Start with the prior probabilities. One straightforward way to get the probability "
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
            self.wait(4.0)
            self.play(FadeIn(table, shift=UP * 0.2), run_time=1.0)
            self.play(Create(class_box), run_time=0.8)
            self.wait(2.0)
            self.play(FadeIn(prior_formula, shift=UP * 0.15), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            formula["prior"].animate.set_color(WHITE),
            FadeOut(class_box), FadeOut(prior_formula),
            run_time=0.8,
        )

        # -- Likelihood setup: X as a vector, then "too many combinations" --
        x_vec_label = MathTex(
            "\\text{e.g., } P(X = (x_1, \\ldots, x_k) \\mid C_1)"
            ).scale(0.7).next_to(table, RIGHT, buff=0.5)

        with self.voiceover(
            text=(
                "Next, how do we estimate the likelihood — the probability "
                "of observing a particular X given class Ci? By definition, we could "
                "estimate it by counting the fraction of data points with "
                "exactly same feature values as X among those in class Ci. But when there "
                "are many features, this becomes computationally very "
                "costly, because we'd need to locate one very specific "
                "feature vector among many many possible combinations."
            )
        ) as tracker:
            self.play(formula["likelihood"].animate.set_color(YELLOW), run_time=1.0)
            self.wait(4.5)
            self.play(FadeIn(x_vec_label), run_time=1.0)
            self.wait(1.5)

            # A horizontal box spanning the 3 feature columns scans down
            # through the table's rows, like a search beam hunting for one
            # exact matching row -- dramatizing "locate one specific vector
            # among many combinations." Paced (2 slow passes over all 5
            # rows) to last through the rest of the narration instead of
            # bursting through 3 rows early and then sitting idle for the
            # ~12s remaining -- that idle stretch was the "did not move for
            # a long time" gap.
            feature_cells = VGroup(tbl["x1_col"][0], tbl["dots_col"][0], tbl["xk_col"][0])
            scan_box = SurroundingRectangle(feature_cells, color=ERROR_COLOR, buff=0.08)
            self.play(Create(scan_box), run_time=0.5)
            for _ in range(3):
                for i in range(3):
                    row_cells = VGroup(tbl["x1_col"][i + 1], tbl["dots_col"][i + 1], tbl["xk_col"][i + 1])
                    self.play(
                        scan_box.animate.become(SurroundingRectangle(row_cells, color=ERROR_COLOR, buff=0.08)),
                        run_time=0.9,
                    )
            explode_label = Text("exponentially many combinations", font_size=15, color=ERROR_COLOR).next_to(
                table, DOWN, buff=0.3
            )
            self.wait(1.0)
            self.play(FadeIn(explode_label), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        # -- Class-conditional independence: factorize the likelihood term,
        # replacing it in place inside the (still small) formula. -----------
        factorized = make_factorized_likelihood(
            k=3, labels=["P(x_1 \\mid C_i)", "\\cdots", "P(x_k \\mid C_i)"]
        )
        factorized["group"].scale_to_fit_height(formula["likelihood"].height)
        factorized["group"].move_to(formula["likelihood"].get_center())

        cci_label = Text("Class-Conditional Independence", font_size=18, color=YELLOW).next_to(
            formula_display, DOWN, buff=0.4
        )
        naive_label = Text("⟵ a \"naive\" assumption", font_size=18, color=YELLOW).next_to(
            cci_label, RIGHT, buff=0.1
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
            self.play(FadeOut(scan_box), FadeOut(explode_label), FadeOut(x_vec_label), run_time=0.8)

            # Build the *entire* end-state (factorized term substituted,
            # numerator/fraction reflowed around it, re-centered at x=0) as a
            # standalone copy first, then Transform the whole formula group
            # into it in one motion -- previously only the likelihood term
            # itself was animated, while the rest of the formula (times,
            # prior, frac_line, evidence) sat still and then snapped to their
            # reflowed positions the instant the term-morph finished. This
            # way every piece glides to its final spot together.
            end_group = formula["group"].copy()
            end_numerator, end_frac_line, end_evidence = end_group[2]
            end_likelihood = end_numerator[0]
            end_likelihood.become(factorized["group"])
            end_numerator.arrange(RIGHT, buff=0.2)
            end_frac_line.stretch_to_fit_width(max(end_numerator.width, end_evidence.width) + 0.3)
            end_group[2].arrange(DOWN, buff=0.22)
            end_group.arrange(RIGHT, buff=0.4)
            end_group.move_to([0, FORMULA_Y, 0])
            end_cross = annot["cross"].copy().shift(end_evidence.get_center() - formula["evidence"].get_center())

            self.play(
                Transform(formula["group"], end_group),
                Transform(annot["cross"], end_cross),
                run_time=1.5,
            )
            # factorized["group"] (and its terms) were only ever a Transform
            # *source* for end_likelihood above -- they never moved, so their
            # stored position is now stale. Re-sync it to the visible
            # (morphed) likelihood term's new spot, since later beats use
            # factorized["terms"][0]/[2] purely as position/size references
            # for highlight boxes and TransformFromCopy sources.
            factorized["group"].move_to(formula["likelihood"].get_center())
            
            self.play(formula["likelihood"].animate.set_color(YELLOW), run_time=1.0)
            self.play(FadeIn(cci_label), run_time=1.0)
            self.wait(16.0)
            self.play(FadeIn(naive_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Now the question of estimating the likelihood term becomes "
                "how do we estimate the conditional probability of one "
                "specific feature value given class Ci."
            )
        ) as tracker:
            self.play(FadeOut(cci_label), FadeOut(naive_label))
            self.play(formula["likelihood"].animate.set_color(WHITE))
            self.wait(tracker.get_remaining_duration())

        # -- Single out P(x1 | Ci): categorical feature
        x1_exp = MathTex(
            "\\text{e.g., } P(x_1 = 1 \\mid C_1) = \\dfrac{2}{3}"
            ).scale(0.7).next_to(table, RIGHT, buff=1.5).move_to(RIGHT * 1.0 + UP * 0.5)
        x1_box = SurroundingRectangle(tbl["x1_col"][1:4], color=YELLOW, buff=0.1)

        with self.voiceover(
            text=(
                "If the feature is categorical, like with x1, "
                "this is easy: we simply find the fraction "
                "of data points in class Ci that have the same feature value."
            )
        ) as tracker:
            # Color, not a box -- consistent with how prior/likelihood are
            # highlighted elsewhere in the formula. formula["likelihood"] is
            # addressable term-by-term after the CCI transform above: [0] is
            # the x1 term, [4] is the xk term (index 2, "cdots", is between).
            self.play(formula["likelihood"][0].animate.set_color(YELLOW), run_time=1.0)
            self.play(FadeIn(x1_exp), run_time=1.0)
            self.play(Create(x1_box), run_time=1.0)            
            self.wait(tracker.get_remaining_duration())

        frac_expr = MathTex(
            "\\text{what if } P(x_1 \\mid C_i) = \\dfrac{\\text{count}(x_1, C_i)}{\\text{count}(C_i)} = "
        ).scale(0.5).next_to(x1_exp, DOWN, buff=0.45)
        zero_big = Text("0", font_size=30, color=ERROR_COLOR).next_to(frac_expr, RIGHT, buff=0.2)

        with self.voiceover(
            text=(
                "One issue to watch for: what if that fraction happens to be "
                "zero — no data points in class Ci have the same feature value? "
                "Then the entire likelihood calculation, which is a product, "
                "collapses to zero."
            )
        ) as tracker:
            self.play(FadeIn(frac_expr), run_time=1.5)
            self.play(FadeIn(zero_big, scale=1.5), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        laplace_expr = MathTex("\\dfrac{\\text{count}(x_1, C_i) + 1}{\\text{count}(C_i) + 2}").scale(0.6)
        laplace_note = Text(
            "+1: one pretend count in this category\n"
            "+2: number of possible values the feature can take",
            font_size=13, color=YELLOW, line_spacing=1.3,
        ).next_to(laplace_expr, DOWN, buff=0.25)
        laplace_box_group = VGroup(laplace_expr, laplace_note)
        laplace_box = SurroundingRectangle(laplace_box_group, color=YELLOW, buff=0.2, corner_radius=0.08)
        # Stacked below frac_expr, in the same column -- placing it beside
        # big_x1/frac_expr instead kept colliding with them given how little
        # horizontal room is left once the formula's own width is accounted
        # for. zero_big has already faded by the time this is shown.
        laplace_label = Text("Laplace Correction", font_size=16, color=YELLOW).next_to(frac_expr, DOWN, buff=0.25)
        laplace_display = VGroup(laplace_box, laplace_box_group).next_to(laplace_label, DOWN, buff=0.15)

        with self.voiceover(
            text=(
                "The fix is called Laplace correction: we simply add small "
                "non-zero values to both the numerator and denominator of "
                "the fraction. Concretely, we add 1 to the numerator, as if "
                "we'd observed one extra data point in that category, and "
                "add the number of possible values the feature can take -- 2 here, since x1 "
                "is binary -- to the denominator."
            )
        ) as tracker:
            self.play(FadeIn(laplace_label), Create(laplace_box), run_time=1.0)
            self.play(FadeIn(laplace_box_group, shift=UP * 0.1), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(frac_expr), FadeOut(laplace_display), FadeOut(laplace_label),
            FadeOut(x1_exp), FadeOut(x1_box), FadeOut(zero_big),
            formula["likelihood"][0].animate.set_color(WHITE),
        )

        # -- Single out P(xk | Ci): continuous feature ------
        xk_exp = MathTex(
            "\\text{e.g., } P(x_k \\mid C_1)"
            ).scale(0.7).next_to(table, RIGHT, buff=1.5).move_to(RIGHT * 1.0 + UP * 0.5)
        xk_box = SurroundingRectangle(tbl["xk_col"][1:4], color=YELLOW, buff=0.1)
        xk_label1 = Text("• Discretize the feature, or", font_size=14, color=YELLOW).next_to(xk_exp, DOWN, buff=0.25)
        xk_label2 = Text("• Use the distribution density function", font_size=14, color=YELLOW).next_to(xk_label1, DOWN, buff=0.2, aligned_edge=LEFT)
                
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 1, 0.5], x_length=5.5, y_length=1.9,
            axis_config={"include_ticks": False, "tip_height": 0.1, "tip_width": 0.1},
        ).move_to(RIGHT * 2.3 + DOWN * 1.8)
        curve = axes.plot(lambda x: 0.9 * np.exp(-((x - 2.2) ** 2) / 1.2), color=GREEN, x_range=[0, 6])
        highlight_x = 2.1
        dashed = DashedLine(
            axes.coords_to_point(highlight_x, 0),
            axes.coords_to_point(highlight_x, 0.9 * np.exp(-((highlight_x - 2.2) ** 2) / 1.2)),
            color=GREEN,
        )
        
        with self.voiceover(
            text=(
                "If the feature is numerical, like x_k, we can't compute a simple "
                "fraction, since a numerical feature can take infinitely many possible "
                "values. In that case, we either discretize the feature and "
                "treat it as categorical, or assume it follows some "
                "distribution and use that distribution's density function "
                "to compute the conditional probability. Specifically, suppose the curve "
                "represents the probability density function of the feature's distribution. "
                "The curve's height at a given x_k value can stand in for the conditional probability there."
            )
        ) as tracker:
            self.play(formula["likelihood"][4].animate.set_color(YELLOW), run_time=0.8)
            self.play(FadeIn(xk_exp), run_time=1.0)
            self.play(Create(xk_box), run_time=1.0)
            self.wait(7.0)
            self.play(FadeIn(xk_label1), run_time=1.0)
            self.wait(2.0)
            self.play(FadeIn(xk_label2), run_time=1.0)
            self.wait(8.0)
            self.play(Create(axes), run_time=1.0)
            self.play(Create(curve), run_time=1.0)
            self.play(Create(dashed), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(table), FadeOut(formula_display),
            FadeOut(xk_label1), FadeOut(xk_label2),
            FadeOut(xk_exp), FadeOut(xk_box),
            FadeOut(axes), 
            FadeOut(curve), FadeOut(dashed),
        )

        # Stash for scene_07 (append an irrelevant-feature term). These
        # factorized-term mobjects were never added to the scene directly
        # (only used as Transform targets / copy sources), but they carry
        # valid, up-to-date position/size data, which is all scene_07 needs.
        self.factorized_likelihood = factorized


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_05()
        self.scene_06()

    def _fixture_scene_05(self):
        # Stand-in for scene_05's ending state so scene_06 can be previewed
        # alone. scene_06 now does its own fresh reveal (position, scale,
        # and annotation) rather than inheriting scene_05's on-screen state,
        # so this just needs to hand it the formula parts -- nothing to add
        # to the scene here, matching scene_05's now fully-faded-out ending.
        parts = make_bayes_formula()
        parts["evidence"].set_color(GREY_B)
        self.bayes_formula_parts = parts
