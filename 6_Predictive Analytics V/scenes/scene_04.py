import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    NUMERIC_COLOR,
    HIGHLIGHT_COLOR,
    LINREG_POINTS,
    LINREG_BEST_SLOPE,
    LINREG_BEST_INTERCEPT,
)


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: linear regression -- model form and coefficient meaning
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_plane_plot_at(theta, center, scale=0.95, elevation=0.45):
        """3D scatter + fitted plane, projected onto the 2D frame at rotation
        angle `theta` about the vertical axis. (Not a real ThreeDScene --
        those don't mix cleanly with VoiceoverScene -- just an orthographic
        projection with a raised camera, rebuilt each frame while rotating.)"""

        def proj(x1, y, x2):
            x1, y, x2 = x1 - 1.0, y - 1.0, x2 - 1.0
            xr = x1 * np.cos(theta) + x2 * np.sin(theta)
            zr = -x1 * np.sin(theta) + x2 * np.cos(theta)
            sx = xr
            sy = y * np.cos(elevation) + zr * np.sin(elevation)
            return center + scale * np.array([sx, sy, 0.0]), zr

        def plane_y(x1, x2):
            return 0.9 + 0.3 * x1 + 0.35 * x2

        def axis_arrow(end3, label, direction):
            start, _ = proj(0, 0, 0)
            end, _ = proj(*end3)
            arrow = Arrow(start, end, buff=0, color=WHITE, stroke_width=2, tip_length=0.12,
                          max_tip_length_to_length_ratio=0.15)
            return arrow, MathTex(label, font_size=18).next_to(end, direction, buff=0.05)

        x1_axis, x1_label = axis_arrow((2.5, 0, 0), "X_1", DOWN)
        x2_axis, x2_label = axis_arrow((0, 0, 2.5), "X_2", RIGHT)
        y_axis, y_label = axis_arrow((0, 2.5, 0), "Y", UP)

        corners = [proj(a, plane_y(a, b), b)[0] for a, b in [(0, 0), (2, 0), (2, 2), (0, 2)]]
        plane = Polygon(*corners, color=NUMERIC_COLOR, fill_color=NUMERIC_COLOR, fill_opacity=0.25, stroke_width=2)
        grid = VGroup()
        for t in (2 / 3, 4 / 3):
            grid.add(
                Line(proj(t, plane_y(t, 0), 0)[0], proj(t, plane_y(t, 2), 2)[0], stroke_width=1, color=NUMERIC_COLOR),
                Line(proj(0, plane_y(0, t), t)[0], proj(2, plane_y(2, t), t)[0], stroke_width=1, color=NUMERIC_COLOR),
            )

        rng = np.random.default_rng(11)
        dots = VGroup()
        for _ in range(9):
            a, b = rng.uniform(0.15, 1.85), rng.uniform(0.15, 1.85)
            pos, depth = proj(a, plane_y(a, b) + rng.uniform(-0.4, 0.4), b)
            dots.add(Dot(pos, color=NUMERIC_COLOR, radius=0.055 - 0.015 * depth))

        return VGroup(x1_axis, x2_axis, y_axis, x1_label, x2_label, y_label, plane, grid, dots)

    def scene_04(self):
        title = Text("Linear Regression for Numeric Prediction", font_size=26).to_edge(UP, buff=0.3)
        subtitle = Text(
            "A tool for both statistical estimation and prediction", font_size=18, color=YELLOW
        ).next_to(title, DOWN, buff=0.2)

        stats_label = Text("Linear Regression in statistics: Inference & Hypothesis Testing", font_size=20, color=GREY_B).move_to(
            UP * 1.6
        )
        pred_label = Text("Also a predictive tool", font_size=20, color=NUMERIC_COLOR).move_to(UP * 1.6)

        with self.voiceover(
            text=(
                "Next, we will discuss linear regression as a numeric prediction "
                "technique. Typically, linear regression is introduced in a "
                "statistics course, as one of the most important tools to "
                "estimate a statistical model and draw inferences or test "
                "hypotheses. However, the same mechanics of linear regression can "
                "be used for predictive purposes."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.0)
            self.wait(2.4)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
            self.wait(2.0)
            self.play(FadeIn(stats_label), run_time=1.0)
            self.wait(6.8)
            self.play(ReplacementTransform(stats_label, pred_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        # Split into parts so the coefficient parts (indices 1, 3, 6, 11) can be colored later.
        formula = MathTex(
            r"\hat{Y} =", "b_0", "+", "b_1", "X_1", "+", "b_2", "X_2", "+", r"\dots", "+", "b_n", "X_n",
            font_size=30,
        ).move_to(UP * 1.6)
        coefficients = [formula[i] for i in (1, 3, 6, 11)]
        b1_term = VGroup(formula[3], formula[4])

        left_axes = Axes(
            x_range=[0, 9, 3], y_range=[0, 25, 10], x_length=3.6, y_length=2.6,
            axis_config={"include_ticks": False, "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(LEFT * 3.5 + DOWN * 1.1)
        left_axis_labels = VGroup(
            MathTex("X_1", font_size=22).next_to(left_axes.x_axis.get_end(), DOWN, buff=0.12),
            MathTex("Y", font_size=22).next_to(left_axes.y_axis.get_end(), LEFT, buff=0.12),
        )
        left_dots = VGroup(*[Dot(left_axes.coords_to_point(x, y), color=NUMERIC_COLOR, radius=0.06)
                              for x, y in LINREG_POINTS])
        left_line = Line(
            left_axes.coords_to_point(0, LINREG_BEST_INTERCEPT),
            left_axes.coords_to_point(8, LINREG_BEST_SLOPE * 8 + LINREG_BEST_INTERCEPT),
            color=HIGHLIGHT_COLOR, stroke_width=3,
        )
        left_label = Text("1 feature = fitting a line", font_size=15).next_to(left_axes, DOWN, buff=0.15)

        plane_center = RIGHT * 3.6 + DOWN * 1.75
        rotation = ValueTracker(0.6)
        rotation.add_updater(lambda t, dt: t.increment_value(0.45 * dt))
        self.add(rotation)
        right_visual = always_redraw(lambda: self.scene4_plane_plot_at(rotation.get_value(), plane_center))
        right_label = Text("2+ features = fitting a plane", font_size=15).move_to(RIGHT * 3.5 + DOWN * 3.6)

        coef_tag = Text("Coefficients", font_size=16, color=HIGHLIGHT_COLOR).next_to(formula, DOWN, buff=0.45)
        coef_arrows = VGroup(
            *[Arrow(coef_tag.get_top(), term.get_bottom(), buff=0.08, color=HIGHLIGHT_COLOR, stroke_width=2,
                    tip_length=0.12, max_tip_length_to_length_ratio=0.3)
              for term in coefficients]
        )

        coef_demo_left = MathTex(r"X_1 \;\; +1 \text{ unit}", font_size=20, color=NUMERIC_COLOR)
        coef_arrow = Arrow(LEFT * 0.6, RIGHT * 0.6, buff=0, stroke_width=3, color=WHITE, tip_length=0.18)
        coef_demo_right = MathTex(r"\hat{Y} \;\; +\, b_1 \text{ units}", font_size=20, color=HIGHLIGHT_COLOR)
        coef_demo = VGroup(coef_demo_left, coef_arrow, coef_demo_right).arrange(RIGHT, buff=0.3).move_to(UP * 2.45)
        b1_box = SurroundingRectangle(b1_term, color=HIGHLIGHT_COLOR, buff=0.1)

        with self.voiceover(
            text=(
                "In a linear regression, the predicted outcome variable, Y-hat, is "
                "simply a linear combination of all the features. When there is "
                "only 1 feature, linear regression is the same as fitting a line "
                "through training data points. When there are more than one "
                "features, this becomes fitting a plane through space. The "
                "parameters of a linear regression are called the coefficients, "
                "and they represent the individual weights of each feature in "
                "determining the outcome variable. Each coefficient carries a "
                "straightforward interpretation. For instance, consider the "
                "coefficient b_1 on feature X_1: it means that 1 unit change in "
                "X_1 is associated with b_1 units change in the predicted value "
                "Y-hat, holding everything else unchanged."
            )
        ) as tracker:
            self.play(FadeOut(pred_label), run_time=0.5)
            self.play(Write(formula), run_time=2.0)
            self.wait(4.0)

            self.play(Create(left_axes), FadeIn(left_axis_labels), run_time=0.6)
            self.play(FadeIn(left_dots, lag_ratio=0.1), run_time=0.8)
            self.play(Create(left_line), run_time=0.6)
            self.play(FadeIn(left_label), run_time=0.4)
            self.wait(5.2)

            self.play(FadeIn(right_visual, lag_ratio=0.1), run_time=1.6)
            self.play(FadeIn(right_label), run_time=0.4)
            self.wait(3.6)

            self.play(FadeIn(coef_tag), Create(coef_arrows), run_time=1.5)
            self.play(
                AnimationGroup(*[c.animate.set_color(HIGHLIGHT_COLOR) for c in coefficients], lag_ratio=0.4),
                run_time=2.0,
            )
            self.wait(7.0)

            self.play(Create(b1_box), run_time=0.8)
            self.wait(1.6)

            self.play(FadeIn(coef_demo_left), run_time=1.0)
            self.play(GrowArrow(coef_arrow), run_time=0.6)
            self.play(FadeIn(coef_demo_right), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        rotation.clear_updaters()
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(formula),
            FadeOut(left_axes), FadeOut(left_axis_labels), FadeOut(left_dots), FadeOut(left_line), FadeOut(left_label),
            FadeOut(right_visual), FadeOut(right_label),
            FadeOut(coef_tag), FadeOut(coef_arrows), FadeOut(coef_demo), FadeOut(b1_box),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
