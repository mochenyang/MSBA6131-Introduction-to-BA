import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    NUMERIC_COLOR,
    ERROR_COLOR,
    GOOD_COLOR,
    HIGHLIGHT_COLOR,
    LINREG_POINTS,
    LINREG_BEST_SLOPE,
    LINREG_BEST_INTERCEPT,
    LINREG_BEST_SSE,
)

# Intermediate (slope, intercept, SSE) guesses shown before the best fit --
# SSE values are the actual sum of squared errors on LINREG_POINTS for each
# guess, so the on-screen counter is accurate, not just decorative.
SCENE5_GUESSES = [
    (1.0, 2.0, 564.86),
    (1.8, 3.0, 104.58),
    (2.4, 3.3, 50.28),
    (LINREG_BEST_SLOPE, LINREG_BEST_INTERCEPT, LINREG_BEST_SSE),
]


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: fitting a linear regression by minimizing SSE
    # ------------------------------------------------------------------
    def scene_05(self):
        title = Text("Fitting a Linear Regression", font_size=26).to_edge(UP, buff=0.3)
        caption = Text("Find Coefficients that Best Fit Training Data", font_size=18, color=YELLOW).next_to(
            title, DOWN, buff=0.2
        )

        big_axes = Axes(
            x_range=[0, 9, 3], y_range=[0, 25, 5], x_length=7.4, y_length=4.6,
            axis_config={"include_ticks": False, "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(LEFT * 1.6 + DOWN * 0.7)
        big_axis_labels = VGroup(
            MathTex("X_1", font_size=26).next_to(big_axes.x_axis.get_end(), DOWN, buff=0.12),
            MathTex("Y", font_size=26).next_to(big_axes.y_axis.get_end(), LEFT, buff=0.12),
        )
        big_dots = VGroup(
            *[Dot(big_axes.coords_to_point(x, y), color=NUMERIC_COLOR, radius=0.07) for x, y in LINREG_POINTS]
        )

        def make_line(slope, intercept):
            return Line(
                big_axes.coords_to_point(0, intercept),
                big_axes.coords_to_point(8.8, slope * 8.8 + intercept),
                color=HIGHLIGHT_COLOR, stroke_width=3,
            )

        # Fixed dash count keeps every dashed segment's structure identical, so
        # Transform between different fits morphs cleanly.
        def make_dev_lines(slope, intercept):
            return VGroup(
                *[
                    DashedVMobject(
                        Line(
                            big_axes.coords_to_point(x, y),
                            big_axes.coords_to_point(x, slope * x + intercept),
                            color=ERROR_COLOR,
                            stroke_width=2.5,
                        ),
                        num_dashes=8,
                    )
                    for x, y in LINREG_POINTS
                ]
            )

        first_slope, first_intercept, first_sse = SCENE5_GUESSES[0]
        line = make_line(first_slope, first_intercept)
        dev_lines = make_dev_lines(first_slope, first_intercept)

        sse_formula = MathTex(r"SSE = \sum_i (a_i - p_i)^2", font_size=28).move_to(RIGHT * 4.5 + UP * 1.5)
        sse_label = Text("SSE =", font_size=24).move_to(RIGHT * 4.5 + UP * 0.5)
        sse_value = DecimalNumber(first_sse, num_decimal_places=1, font_size=26, color=HIGHLIGHT_COLOR).next_to(
            sse_label, RIGHT, buff=0.15
        )
        sse_group = VGroup(sse_label, sse_value)
        minimized_tag = Text("minimized!", font_size=16, color=GOOD_COLOR).next_to(sse_group, DOWN, buff=0.3)
        sse_box = SurroundingRectangle(sse_group, color=GOOD_COLOR, buff=0.15)

        with self.voiceover(
            text=(
                "How do we fit a linear regression? The idea is to find the "
                "coefficient values that fit the training data as well as "
                "possible. Typically, this is done by minimizing the so-called "
                "sum of squared error (SSE in short) on the training dataset. "
                "Take a look at this example for illustration. Given a regression "
                "line through these data points, we can measure how far each "
                "data point is from the predicted value given by the regression "
                "line. Adding up the squared value of these distances would "
                "produce the SSE. Different coefficient value correspond to "
                "different positions of this line, and we want to choose the "
                "coefficient values such that the SSE measure is the smallest."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.wait(2.0)
            self.play(FadeIn(caption), run_time=1.0)
            self.wait(4.0)
            self.play(FadeIn(sse_formula), run_time=1.0)
            self.wait(8.0)
            self.play(Create(big_axes), FadeIn(big_axis_labels), run_time=0.8)
            self.play(FadeIn(big_dots, lag_ratio=0.1), run_time=1.0)
            self.wait(1.0)
            self.play(Create(line), run_time=1.2)
            self.wait(1.0)
            self.play(Create(dev_lines, lag_ratio=0.1), run_time=1.5)
            self.wait(3.0)
            self.play(FadeIn(sse_group), run_time=0.8)
            self.wait(4.0)            
            for slope, intercept, sse in SCENE5_GUESSES[1:]:
                new_line = make_line(slope, intercept)
                new_dev = make_dev_lines(slope, intercept)
                self.play(
                    Transform(line, new_line),
                    Transform(dev_lines, new_dev),
                    ChangeDecimalToValue(sse_value, sse),
                    run_time=2.0,
                )
            self.play(Create(sse_box), FadeIn(minimized_tag), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(caption), FadeOut(big_axes), FadeOut(big_axis_labels), FadeOut(big_dots),
            FadeOut(line), FadeOut(dev_lines), FadeOut(sse_formula), FadeOut(sse_group),
            FadeOut(sse_box), FadeOut(minimized_tag),
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_05()
