import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    DATA_CURVE_COLOR,
    RANDOM_CLASSIFIER_COLOR,
    BETTER_COLOR,
    N_RECORDS,
    make_unit_axes,
    compute_cum_response_points,
    build_data_curve,
)


class Scene07Mixin:
    # ------------------------------------------------------------------
    # Scene 7: the lift ratio and the lift curve, built from the same
    # cumulative response curve as scene 6
    # ------------------------------------------------------------------
    def scene_07(self):
        title = Text("Lift Curve", font_size=32).to_edge(UP, buff=0.4)

        axes_data = self.scene06_axes_data
        cum_curve = self.scene06_cum_curve
        left_group = VGroup(axes_data["group"], cum_curve)
        left_group.scale(0.85).move_to(LEFT * 3.5 + DOWN * 0.2)
        axes = axes_data["axes"]
        cum_points = compute_cum_response_points()

        with self.voiceover(
            text=(
                "The cumulative response curve also lets us quantify "
                "exactly how much better a classifier is than random "
                "guessing. At any point on the x-axis, we divide the "
                "model's cumulative response by the random classifier's "
                "cumulative response at that same point; this ratio is "
                "called the lift ratio. For example, if a model's "
                "cumulative response at the top 20% of data is 1/3 "
                "while the random classifier's is 0.2, the lift ratio "
                "is 1/3 divided by 0.2, or about 1.7 — meaning the "
                "model's top 20% predictions are 1.7 times as good as "
                "random predictions."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(left_group), run_time=1.5)
            self.wait(3.0)

            dashed = DashedLine(axes.c2p(0.2, 0), axes.c2p(0.2, 1), color=GREY_B, stroke_width=2)
            model_dot = Dot(axes.c2p(0.2, cum_points[2][1]), color=DATA_CURVE_COLOR, radius=0.07)
            random_dot = Dot(axes.c2p(0.2, 0.2), color=RANDOM_CLASSIFIER_COLOR, radius=0.07)
            self.play(Create(dashed), run_time=1.0)
            self.play(FadeIn(model_dot), FadeIn(random_dot), run_time=1.0)
            self.wait(1.5)

            ratio_tex = MathTex(r"\frac{1/3}{0.2} \approx 1.7", font_size=30).next_to(axes, DOWN, buff=0.5)
            self.play(Write(ratio_tex), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        lift_axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 2, 0.5], x_length=4.6, y_length=3.9,
            axis_config={"include_numbers": True, "font_size": 14},
        )
        lift_axes.scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.2)
        lift_x_label = lift_axes.get_x_axis_label(Text("% of Data", font_size=16), edge=DOWN, direction=DOWN, buff=0.3)
        lift_y_label = lift_axes.get_y_axis_label(Text("Lift Ratio", font_size=16), edge=LEFT, direction=LEFT, buff=0.25)
        lift_baseline = DashedLine(lift_axes.c2p(0, 1), lift_axes.c2p(1, 1), color=GREY_B, stroke_width=2)

        lift_points = [(k / N_RECORDS, cum_points[k][1] / (k / N_RECORDS)) for k in range(1, N_RECORDS + 1)]

        with self.voiceover(
            text=(
                "We can plot this lift ratio at every point along the "
                "x-axis, which gives us the lift curve. A lift curve "
                "that sits higher and further to the right — closer to "
                "the top-right of the chart — indicates an overall "
                "better classifier."
            )
        ) as tracker:
            self.play(Create(lift_axes), FadeIn(lift_x_label), FadeIn(lift_y_label), run_time=1.5)
            self.play(Create(lift_baseline), run_time=1.0)
            self.wait(1.0)

            first_dot = Dot(lift_axes.c2p(*lift_points[0]), radius=0.06, color=DATA_CURVE_COLOR)
            first_dashed = DashedLine(
                axes.c2p(lift_points[0][0], 0), axes.c2p(lift_points[0][0], 1), color=GREY_B, stroke_width=2
            )
            self.play(Transform(dashed, first_dashed), FadeIn(first_dot), run_time=0.8)
            lift_dots = VGroup(first_dot)
            lift_segments = VGroup()
            for x, y in lift_points[1:]:
                new_dot = Dot(lift_axes.c2p(x, y), radius=0.06, color=DATA_CURVE_COLOR)
                segment = Line(lift_dots[-1].get_center(), new_dot.get_center(), color=DATA_CURVE_COLOR, stroke_width=3.5)
                new_dashed = DashedLine(axes.c2p(x, 0), axes.c2p(x, 1), color=GREY_B, stroke_width=2)
                self.play(Transform(dashed, new_dashed), Create(segment), FadeIn(new_dot), run_time=0.6)
                lift_segments.add(segment)
                lift_dots.add(new_dot)

            better_label = Text("better", font_size=18, color=BETTER_COLOR).next_to(
                lift_axes.c2p(1, 2), UP + LEFT, buff=0.15
            )
            self.play(FadeIn(better_label, shift=DOWN * 0.15), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(left_group), FadeOut(dashed), FadeOut(model_dot), FadeOut(random_dot),
            FadeOut(ratio_tex), FadeOut(lift_axes), FadeOut(lift_x_label), FadeOut(lift_y_label),
            FadeOut(lift_baseline), FadeOut(lift_segments), FadeOut(lift_dots), FadeOut(better_label),
        )


class Scene07(VoiceoverScene, Scene07Mixin):
    """Standalone preview: manim -pql scene_07.py Scene07"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_06()
        self.scene_07()

    def _fixture_scene_06(self):
        # Stand-in for scene_06's cumulative response axes + finished curve
        # so scene_07 can be previewed alone.
        axes_data = make_unit_axes("% of Data Predicted Positive", "Cumulative Response")
        axes_data["group"].scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.3)
        cum_curve = build_data_curve(axes_data["axes"], compute_cum_response_points())
        self.scene06_axes_data = axes_data
        self.scene06_cum_curve = cum_curve
