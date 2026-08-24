import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service

YES_CLASS_COLOR = ORANGE
NO_CLASS_COLOR = PURPLE


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: applications of predictive analytics; classification vs.
    # numeric prediction
    # ------------------------------------------------------------------
    @staticmethod
    def scene2_make_icon(kind):
        """Simple, generic geometric stand-ins for each application icon."""
        if kind == "bank":
            roof = Triangle(color=WHITE).scale(0.3).shift(UP * 0.25)
            base = Rectangle(width=0.6, height=0.3, color=WHITE).shift(DOWN * 0.05)
            cols = VGroup(*[Line(UP * 0.12, DOWN * 0.12, color=WHITE) for _ in range(3)])
            cols.arrange(RIGHT, buff=0.12).move_to(base.get_center())
            return VGroup(roof, base, cols)
        if kind == "card":
            card = RoundedRectangle(width=0.7, height=0.45, corner_radius=0.06, color=WHITE)
            stripe = Rectangle(width=0.7, height=0.1, color=WHITE, fill_opacity=1).move_to(
                card.get_center() + UP * 0.08
            )
            return VGroup(card, stripe)
        if kind == "gauge":
            arc = Arc(radius=0.35, start_angle=PI, angle=-PI, color=WHITE)
            needle = Line(ORIGIN, UP * 0.3, color=WHITE).rotate(-PI / 5, about_point=ORIGIN)
            needle.shift(arc.get_center())
            return VGroup(arc, needle)
        if kind == "stock":
            pts = [LEFT * 0.35 + DOWN * 0.1, LEFT * 0.1 + DOWN * 0.2, RIGHT * 0.1 + UP * 0.05, RIGHT * 0.35 + UP * 0.3]
            zigzag = VMobject(color=WHITE).set_points_as_corners(pts)
            arrow = Triangle(color=WHITE, fill_opacity=1).scale(0.08).move_to(pts[-1]).rotate(-PI / 2)
            return VGroup(zigzag, arrow)
        if kind == "images":
            sq1 = Square(0.35, color=WHITE).shift(DOWN * 0.08 + LEFT * 0.08)
            sq2 = Square(0.35, color=WHITE).shift(UP * 0.08 + RIGHT * 0.08)
            return VGroup(sq1, sq2)
        if kind == "speech":
            bubble = RoundedRectangle(width=0.7, height=0.45, corner_radius=0.12, color=WHITE)
            tail = Polygon(
                bubble.get_bottom() + LEFT * 0.18,
                bubble.get_bottom() + LEFT * 0.03,
                bubble.get_bottom() + LEFT * 0.16 + DOWN * 0.18,
                color=WHITE,
            )
            return VGroup(bubble, tail)
        if kind == "docs":
            d1 = Rectangle(width=0.45, height=0.55, color=WHITE).shift(LEFT * 0.08 + DOWN * 0.08)
            d2 = Rectangle(width=0.45, height=0.55, color=WHITE).shift(RIGHT * 0.08 + UP * 0.08)
            lines = VGroup(*[Line(LEFT * 0.14, RIGHT * 0.14, color=WHITE, stroke_width=1.5) for _ in range(2)])
            lines.arrange(DOWN, buff=0.08).move_to(d2.get_center())
            return VGroup(d1, d2, lines)
        return Dot()

    @staticmethod
    def scene2_make_icon_label(kind, text, color=WHITE):
        icon = Scene02Mixin.scene2_make_icon(kind).set_color(color)
        label = Text(text, font_size=18).next_to(icon, DOWN, buff=0.18)
        return VGroup(icon, label)

    def scene_02(self):
        center_label = Text("Predictive Analytics", font_size=30, color=YELLOW)

        apps = [
            ("bank", "Loan Default"),
            ("card", "Fraud Detection"),
            ("gauge", "Credit Scores"),
            ("stock", "Stock Prices"),
            ("images", "Image Recognition"),
            ("speech", "Speech Recognition"),
            ("docs", "Language Understanding"),
        ]
        n = len(apps)
        radius = 2.7
        satellites = []
        for i, (kind, text) in enumerate(apps):
            angle = PI / 2 - i * (2 * PI / n)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            satellites.append(self.scene2_make_icon_label(kind, text).move_to(pos))

        # Timing below is keyed to where each named item actually falls in the
        # ~28.5s clip (measured from the cached TTS audio) -- the four finance
        # examples are all named in the back third of the sentence, so the
        # icons stay clustered there instead of popping in all at once up front.
        with self.voiceover(
            text=(
                "Predictive analytics is used across a huge range of practical "
                "applications. In fact, a lot of what people call \"data mining,\" "
                "\"machine learning,\" or even \"artificial intelligence\" is really "
                "predictive analytics under the hood. For example, predicting "
                "loan default from loan applications, flagging fraudulent "
                "transactions from transaction characteristics, estimating credit "
                "scores from consumption records, and forecasting stock prices from "
                "past prices."
            )
        ) as tracker:
            self.play(FadeOut(self.title_scene_01), run_time=0.8)
            self.play(Write(center_label), run_time=1.3)
            self.wait(8.0)
            self.play(Indicate(center_label), run_time=1.0)
            self.wait(6.0)
            self.play(FadeIn(satellites[0], scale=0.7), run_time=0.6)  # loan default
            self.wait(2.16)
            self.play(FadeIn(satellites[1], scale=0.7), run_time=0.6)  # fraud detection
            self.wait(2.17)
            self.play(FadeIn(satellites[2], scale=0.7), run_time=0.6)  # credit scores
            self.wait(2.64)
            self.play(FadeIn(satellites[3], scale=0.7), run_time=0.6)  # stock prices
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Even more advanced applications often labeled \"AI\" -- image "
                "recognition, speech recognition, natural language understanding -- "
                "are primarily driven by predictive machine learning underneath."
            )
        ) as tracker:
            self.wait(4.0)
            self.play(FadeIn(satellites[4], scale=0.7), run_time=0.6)  # image recognition
            self.wait(0.7)
            self.play(FadeIn(satellites[5], scale=0.7), run_time=0.6)  # speech recognition
            self.wait(1.0)
            self.play(FadeIn(satellites[6], scale=0.7), run_time=0.6)  # language understanding
            self.wait(tracker.get_remaining_duration())

        applications_group = VGroup(center_label, *satellites)
        class_title = Text("Classification", font_size=26, color=YES_CLASS_COLOR).move_to(
                    LEFT * 3.5 + DOWN * 1.6)
        numeric_title = Text("Numeric Prediction", font_size=26, color=BLUE).move_to(
                    RIGHT * 3.5 + DOWN * 1.6)
        
        with self.voiceover(
            text=(
                "Broadly speaking, there are two types of predictive analytics: "
                "classification and numeric prediction. The difference is the type "
                "of outcome you're trying to predict."
            )
        ) as tracker:
            self.play(
                applications_group.animate.scale(0.55).to_edge(UP, buff=0.4),
                run_time=2,
            )
            divider = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY_B).move_to(DOWN * 1.0)
            self.play(Create(divider), run_time=1)
            self.play(Write(class_title), run_time=0.8)
            self.play(Write(numeric_title), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        legend_yes = VGroup(
            Dot(color=YES_CLASS_COLOR, radius=0.08), Text("Yes Class", font_size=16, color=YES_CLASS_COLOR)
        ).arrange(RIGHT, buff=0.15)
        legend_no = VGroup(
            Dot(color=NO_CLASS_COLOR, radius=0.08), Text("No Class", font_size=16, color=NO_CLASS_COLOR)
        ).arrange(RIGHT, buff=0.15)
        legend = VGroup(legend_yes, legend_no).arrange(RIGHT, buff=0.6).next_to(class_title, DOWN, buff=0.3)

        rng = np.random.default_rng(3)
        dot_center = LEFT * 3.5 + DOWN * 3.2
        yes_dots = VGroup(
            *[
                Dot(dot_center + np.array([rng.uniform(-1.4, 1.4), rng.uniform(-0.6, 0.6), 0]), color=YES_CLASS_COLOR)
                for _ in range(5)
            ]
        )
        no_dots = VGroup(
            *[
                Dot(dot_center + np.array([rng.uniform(-1.4, 1.4), rng.uniform(-0.6, 0.6), 0]), color=NO_CLASS_COLOR)
                for _ in range(5)
            ]
        )

        with self.voiceover(
            text=(
                "Classification predicts categorical outcomes, also called "
                "\"classes\"."
            )
        ) as tracker:
            self.play(FadeIn(legend), run_time=0.8)
            self.play(FadeIn(yes_dots, lag_ratio=0.1), FadeIn(no_dots, lag_ratio=0.1), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        number_line = NumberLine(x_range=[0, 10, 2], length=5.5, color=GREY_B).move_to(
            RIGHT * 3.5 + DOWN * 2.9
        )
        values = [1.5, 3.2, 4.8, 6.0, 7.5, 8.8]
        num_dots = VGroup(*[Dot(number_line.n2p(v), color=BLUE) for v in values])

        with self.voiceover(
            text="Numeric prediction predicts numeric, continuous outcomes."
        ) as tracker:
            self.play(Create(number_line), run_time=0.8)
            self.play(FadeIn(num_dots, lag_ratio=0.1), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(applications_group), FadeOut(divider),
            FadeOut(class_title), FadeOut(legend), FadeOut(yes_dots), FadeOut(no_dots),
            FadeOut(numeric_title), FadeOut(number_line), FadeOut(num_dots),
        )


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_01()
        self.scene_02()

    def _fixture_scene_01(self):
        title = Text("Predictive Analytics", font_size=48)
        subtitle = Text(
            "Standard Pipeline, k-Nearest Neighbors, and Decision Trees", font_size=26, color=YELLOW
        ).next_to(title, DOWN, buff=0.4)
        self.title_scene_01 = VGroup(title, subtitle)
        self.add(self.title_scene_01)
