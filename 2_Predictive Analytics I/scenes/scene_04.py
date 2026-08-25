import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text

SIMPLE_MODEL_COLOR = BLUE
OVERFIT_MODEL_COLOR = RED


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: overfitting
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_data():
        rng = np.random.default_rng(7)
        xs = np.sort(rng.uniform(1, 9, 6))
        ys = 0.5 * xs + 2 + rng.normal(0, 0.4, size=6)
        return xs, ys

    def scene_04(self):
        word1 = Text("Overfitting", font_size=40).to_edge(UP, buff=0.6)
        word2 = Text("fits the data too well", font_size=28).next_to(word1, DOWN, buff=0.25)
        word3 = Text(
            "...including the noise, anomaly, and outlier", font_size=26, color=RED
        ).next_to(word2, DOWN, buff=0.2)

        with self.voiceover(
            text=(
                "Now let's talk about a very important issue in predictive "
                "analytics: overfitting. A lot of the design choices and "
                "techniques in predictive machine learning exist specifically to "
                "avoid or mitigate it. Overfitting is when a predictive model fits "
                "the data too well."
            )
        ) as tracker:
            self.play(Write(word1), run_time=1.2)
            self.wait(12.3)
            self.play(FadeIn(word2, shift=UP * 0.2), run_time=1.3)  # "...fits the data too well"
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "At first that might not sound like a bad thing -- after all, the "
                "whole point of building a model is to fit it to the data. But "
                "overfitting means the model fits the data too faithfully, taking "
                "into account noise, anomalies, and outliers -- patterns that "
                "aren't actually meaningful. And that's dangerous, because the "
                "model won't make accurate predictions on new data, since new data "
                "likely doesn't share those same quirks. In other words, "
                "overfitting hurts a model's generalizability."
            )
        ) as tracker:
            self.wait(12)
            self.play(FadeIn(word3, shift=UP * 0.2), run_time=1.5)  # "...noise, anomalies, and outliers"
            self.wait(tracker.get_remaining_duration())

        definition = VGroup(word1, word2, word3)

        xs, ys = self.scene4_data()
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-2, 12, 3],
            x_length=8,
            y_length=4.3,
            axis_config={"include_ticks": False},
        ).to_edge(DOWN, buff=0.7)
        x_label = axes.get_x_axis_label(Text("Input", font_size=22), edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label(Text("Outcome", font_size=22), edge=UP, direction=UP)
        dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=WHITE) for x, y in zip(xs, ys)])

        with self.voiceover(
            text=(
                "Here's an intuitive picture of overfitting. In this "
                "two-dimensional plot, the x-axis is the input variable, and the "
                "y-axis is the outcome we're predicting. The dots are your labeled "
                "data."
            )
        ) as tracker:
            self.play(definition.animate.scale(0.55).to_corner(UL, buff=0.4), run_time=1.0)
            self.play(Create(axes), run_time=1.5)
            self.wait(1.9)
            self.play(Write(x_label), run_time=0.6)  # "the x-axis is the input variable"
            self.wait(2.36)
            self.play(Write(y_label), run_time=0.6)  # "the y-axis is the outcome"
            self.wait(2.24)
            self.play(FadeIn(dots, lag_ratio=0.1), run_time=0.7)  # "the dots are your labeled data"
            self.wait(tracker.get_remaining_duration())

        deg1 = np.polyfit(xs, ys, 1)
        simple_curve = axes.plot(
            lambda x: np.polyval(deg1, x), x_range=[0.5, 9.5], color=SIMPLE_MODEL_COLOR
        )
        simple_label = Text("Simple Model", font_size=22, color=SIMPLE_MODEL_COLOR).next_to(
            simple_curve, UP, buff=0.15
        ).shift(LEFT * 1.5)

        with self.voiceover(
            text=(
                "The straight line is a simple linear model fit to the data -- it "
                "doesn't pass through every point perfectly, but it captures the "
                "overall trend and isn't thrown off by small changes in the data."
            )
        ) as tracker:
            self.play(Create(simple_curve), run_time=2)
            self.play(FadeIn(simple_label, shift=UP * 0.1), run_time=1)
            self.wait(tracker.get_remaining_duration())

        deg_high = np.polyfit(xs, ys, len(xs) - 1)
        overfit_curve = axes.plot(
            lambda x: np.polyval(deg_high, x), x_range=[xs[0], xs[-1]], color=OVERFIT_MODEL_COLOR, use_smoothing=False
        )
        overfit_label = Text("Overfit Model", font_size=22, color=OVERFIT_MODEL_COLOR).next_to(
            axes, UP, buff=0.15
        ).align_to(axes, RIGHT)

        with self.voiceover(
            text=(
                "The curve, on the other hand, is a complex polynomial model that "
                "fits the data perfectly, passing through every single point."
            )
        ) as tracker:
            self.play(Create(overfit_curve), run_time=3)
            self.play(FadeIn(overfit_label, shift=UP * 0.1), run_time=1)
            self.wait(tracker.get_remaining_duration())

        nudged_ys = ys.copy()
        nudged_ys[-1] += 3.0
        new_dot_pos = axes.coords_to_point(xs[-1], nudged_ys[-1])
        new_deg1 = np.polyfit(xs, nudged_ys, 1)
        new_simple_curve = axes.plot(
            lambda x: np.polyval(new_deg1, x), x_range=[0.5, 9.5], color=SIMPLE_MODEL_COLOR
        )
        new_deg_high = np.polyfit(xs, nudged_ys, len(xs) - 1)
        new_overfit_curve = axes.plot(
            lambda x: np.polyval(new_deg_high, x), x_range=[xs[0], xs[-1]], color=OVERFIT_MODEL_COLOR, use_smoothing=False
        )

        with self.voiceover(
            text=(
                "But it's unlikely to predict new data well -- even a small change "
                "in the positions of the data points would drastically reshape "
                "that curve. That's what it means for a complex model to overfit."
            )
        ) as tracker:
            self.wait(3.3)
            self.play(dots[-1].animate.move_to(new_dot_pos), run_time=0.8)  # "a tiny change in the positions"
            self.wait(1.9)
            self.play(
                Transform(simple_curve, new_simple_curve),
                Transform(overfit_curve, new_overfit_curve),
                run_time=2.0,
            )  # "drastically reshape that curve"
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(definition), FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(dots), FadeOut(simple_curve), FadeOut(overfit_curve),
            FadeOut(simple_label), FadeOut(overfit_label),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
