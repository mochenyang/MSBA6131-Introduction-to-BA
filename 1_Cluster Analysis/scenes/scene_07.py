import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service


class Scene07Mixin:
    # ------------------------------------------------------------------
    # Scene 7: Normalization
    # ------------------------------------------------------------------
    def scene_07(self):
        with self.voiceover(
            text="Another very important topic when calculating distances between data points is normalization."
        ) as tracker:
            title = Text("Normalization", font_size=36).to_edge(UP, buff=0.4)
            self.play(Write(title), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "If two attributes of your data take values from very different "
                "ranges, the attribute with the wider range can distort the "
                "distance calculation."
            )
        ) as tracker:
            subtitle = Text(
                "Different scales can distort distance calculations", font_size=26, color=YELLOW
            ).next_to(title, DOWN, buff=0.5)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=2)
            self.play(Indicate(subtitle), run_time=1)
            self.wait(tracker.get_remaining_duration())

        age_bar = Line(LEFT * 4.5, LEFT * 1.5, color=BLUE, stroke_width=6).shift(UP * 2.5)
        age_bar_label = Text("Age: 0 to 100", font_size=24, color=BLUE).next_to(age_bar, UP, buff=0.2)
        income_bar = Line(LEFT * 4.5, RIGHT * 5.5, color=ORANGE, stroke_width=6).shift(UP * 0.9)
        income_bar_label = Text(
            "Income: $0 to $1,000,000+", font_size=24, color=ORANGE
        ).next_to(income_bar, UP, buff=0.2)

        with self.voiceover(
            text=(
                "Consider two common attributes: age and income. Age takes values "
                "from a small range, say 0 to 100, whereas income takes values from "
                "a much wider range, from thousands to millions or more."
            )
        ) as tracker:
            self.play(FadeOut(subtitle), run_time=1)
            self.play(Create(age_bar), Write(age_bar_label), run_time=1.8)
            self.play(Create(income_bar), Write(income_bar_label), run_time=1.8)
            self.play(Indicate(VGroup(age_bar_label, income_bar_label)), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        AGE_1, AGE_2 = 30, 35
        INCOME_1, INCOME_2 = 20000, 320000

        age_p1 = age_bar.get_start() + RIGHT * (AGE_1 / 100) * age_bar.get_length()
        age_p2 = age_bar.get_start() + RIGHT * (AGE_2 / 100) * age_bar.get_length()
        income_p1 = income_bar.get_start() + RIGHT * (INCOME_1 / 1000000) * income_bar.get_length()
        income_p2 = income_bar.get_start() + RIGHT * (INCOME_2 / 1000000) * income_bar.get_length()

        age_dot1, age_dot2 = Dot(age_p1, color=WHITE), Dot(age_p2, color=WHITE)
        income_dot1, income_dot2 = Dot(income_p1, color=WHITE), Dot(income_p2, color=WHITE)
        age_diff_label = Text("diff = 5", font_size=20, color=BLUE).next_to(
            VGroup(age_dot1, age_dot2), DOWN, buff=0.25
        )
        income_diff_brace = Brace(Line(income_p1, income_p2), DOWN, color=ORANGE)
        income_diff_label = income_diff_brace.get_text("diff = 300,000").set_color(ORANGE)

        # Raw feature values of the two illustrative data points, kept visible
        # in the corner so viewers can later compare them to their normalized
        # counterparts once the bars rescale.
        # Pinned to a fixed y below the title (not to_corner(UR), which
        # anchors by each line's own width -- the wider raw-value text with
        # dollar signs/commas would then horizontally collide with the
        # centered title, even though the narrower normalized text wouldn't).
        raw_values = VGroup(
            Text(f"Point 1: Age={AGE_1}, Income=${INCOME_1:,}", font_size=20, color=WHITE),
            Text(f"Point 2: Age={AGE_2}, Income=${INCOME_2:,}", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).set_y(2.7)

        with self.voiceover(
            text=(
                "When calculating the distance between two individuals based on "
                "age and income, the difference in income, simply by virtue of its "
                "wider range, will dominate the calculation and render the "
                "difference in age too small to matter."
            )
        ) as tracker:
            self.play(
                FadeIn(age_dot1), FadeIn(age_dot2), FadeIn(income_dot1), FadeIn(income_dot2), run_time=1
            )
            self.play(FadeIn(raw_values), run_time=1)
            self.play(
                Write(age_diff_label),
                GrowFromCenter(income_diff_brace), Write(income_diff_label),
                run_time=1.5,
            )
            # Both bars grow from a shared baseline, like a real bar chart --
            # previously their bottoms were off by several hundredths of a
            # unit and didn't quite line up.
            baseline_y = -3.0
            age_sq = Rectangle(width=0.6, height=0.3, color=BLUE, fill_color=BLUE, fill_opacity=0.7).move_to(
                LEFT * 2 + UP * (baseline_y + 0.3 / 2)
            )
            age_sq_label = Text("age term ≈ 25", font_size=22, color=BLUE).next_to(age_sq, DOWN, buff=0.2)
            income_sq = Rectangle(
                width=0.6, height=2.2, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7
            ).move_to(RIGHT * 2 + UP * (baseline_y + 2.2 / 2))
            income_sq_label = Text(
                "income term ≈ 9×10¹⁰", font_size=22, color=ORANGE
            ).next_to(income_sq, DOWN, buff=0.2)
            self.play(GrowFromEdge(age_sq, DOWN), GrowFromEdge(income_sq, DOWN), run_time=1.5)
            self.play(Write(age_sq_label), Write(income_sq_label), run_time=1.5)
            self.play(Indicate(income_sq, scale_factor=1.15, color=RED), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Normalization is a simple technique to solve this issue, by "
                "rescaling each attribute so that they fall into the same range."
            )
        ) as tracker:
            self.play(
                FadeOut(age_dot1), FadeOut(age_dot2), FadeOut(income_dot1), FadeOut(income_dot2),
                FadeOut(age_diff_label), FadeOut(income_diff_brace), FadeOut(income_diff_label),
                FadeOut(age_sq), FadeOut(age_sq_label), FadeOut(income_sq), FadeOut(income_sq_label),
                run_time=1.5,
            )
            self.wait(tracker.get_remaining_duration())

        formula = MathTex(
            r"x' = \frac{x - \min}{\max - \min}", font_size=40
        ).next_to(title, DOWN, buff=0.6)
        with self.voiceover(
            text=(
                "A common method is min-max normalization: for each attribute, "
                "find the max and min values, and rescale any value x to x minus "
                "min, divided by max minus min. This ensures the normalized value "
                "always falls within 0 to 1."
            )
        ) as tracker:
            self.play(Write(formula), run_time=2)

            # Literally rescale the SAME two bars into the [0,1] range instead
            # of cutting to fresh, already-normalized ones -- this is the
            # scene's core payoff: watch the income bar shrink down to match
            # age's width as both bars slide into their new row.
            new_age_bar = Line(LEFT * 3, RIGHT * 3, color=BLUE, stroke_width=6).shift(UP * 0.3)
            new_age_label = Text("Age (normalized)", font_size=22, color=BLUE).next_to(new_age_bar, UP, buff=0.2)
            new_income_bar = Line(LEFT * 3, RIGHT * 3, color=ORANGE, stroke_width=6).shift(DOWN * 1.3)
            new_income_label = Text("Income (normalized)", font_size=22, color=ORANGE).next_to(
                new_income_bar, UP, buff=0.2
            )
            norm_values = VGroup(
                Text(f"Point 1: Age={AGE_1 / 100:.2f}, Income={INCOME_1 / 1000000:.2f}", font_size=20, color=WHITE),
                Text(f"Point 2: Age={AGE_2 / 100:.2f}, Income={INCOME_2 / 1000000:.2f}", font_size=20, color=WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).set_y(2.7)
            self.play(
                ReplacementTransform(age_bar, new_age_bar),
                ReplacementTransform(income_bar, new_income_bar),
                FadeTransform(age_bar_label, new_age_label),
                FadeTransform(income_bar_label, new_income_label),
                FadeTransform(raw_values, norm_values),
                run_time=2,
            )

            zero_label_a = Text("0", font_size=20).next_to(new_age_bar, LEFT, buff=0.15)
            one_label_a = Text("1", font_size=20).next_to(new_age_bar, RIGHT, buff=0.15)
            zero_label_i = Text("0", font_size=20).next_to(new_income_bar, LEFT, buff=0.15)
            one_label_i = Text("1", font_size=20).next_to(new_income_bar, RIGHT, buff=0.15)
            self.play(
                Write(zero_label_a), Write(one_label_a), Write(zero_label_i), Write(one_label_i),
                run_time=1,
            )

            norm_age_p1 = new_age_bar.get_start() + RIGHT * 0.30 * new_age_bar.get_length()
            norm_age_p2 = new_age_bar.get_start() + RIGHT * 0.35 * new_age_bar.get_length()
            norm_income_p1 = new_income_bar.get_start() + RIGHT * 0.02 * new_income_bar.get_length()
            norm_income_p2 = new_income_bar.get_start() + RIGHT * 0.32 * new_income_bar.get_length()
            n_age_dot1, n_age_dot2 = Dot(norm_age_p1, color=WHITE), Dot(norm_age_p2, color=WHITE)
            n_income_dot1, n_income_dot2 = Dot(norm_income_p1, color=WHITE), Dot(norm_income_p2, color=WHITE)
            self.play(
                FadeIn(n_age_dot1), FadeIn(n_age_dot2), FadeIn(n_income_dot1), FadeIn(n_income_dot2), run_time=1
            )

            new_age_sq = Rectangle(
                width=0.5, height=0.4, color=BLUE, fill_color=BLUE, fill_opacity=0.7
            ).move_to(LEFT * 2 + UP * (baseline_y + 0.4 / 2))
            new_age_sq_label = Text("0.0025", font_size=22, color=BLUE).next_to(new_age_sq, DOWN, buff=0.2)
            new_income_sq = Rectangle(
                width=0.5, height=1.0, color=ORANGE, fill_color=ORANGE, fill_opacity=0.7
            ).move_to(RIGHT * 2 + UP * (baseline_y + 1.0 / 2))
            new_income_sq_label = Text("0.09", font_size=22, color=ORANGE).next_to(
                new_income_sq, DOWN, buff=0.2
            )
            balance_note = Text("Now comparable!", font_size=24, color=GREEN).move_to(DOWN * 1.65)
            self.play(GrowFromEdge(new_age_sq, DOWN), GrowFromEdge(new_income_sq, DOWN), run_time=1.5)
            # Bug fix: these labels were previously created but never animated
            # onto screen -- "0.0025"/"0.09" would silently never appear.
            self.play(Write(new_age_sq_label), Write(new_income_sq_label), run_time=1)
            self.play(Write(balance_note), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(formula),
            FadeOut(new_age_bar), FadeOut(new_age_label), FadeOut(zero_label_a), FadeOut(one_label_a),
            FadeOut(new_income_bar), FadeOut(new_income_label), FadeOut(zero_label_i), FadeOut(one_label_i),
            FadeOut(n_age_dot1), FadeOut(n_age_dot2), FadeOut(n_income_dot1), FadeOut(n_income_dot2),
            FadeOut(new_age_sq), FadeOut(new_age_sq_label), FadeOut(new_income_sq), FadeOut(new_income_sq_label),
            FadeOut(balance_note), FadeOut(norm_values),
        )


class Scene07(VoiceoverScene, Scene07Mixin):
    """Standalone preview: manim -pql scene_07.py Scene07"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_07()
