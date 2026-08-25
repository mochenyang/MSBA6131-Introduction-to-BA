import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text

CLASS1_COLOR = ORANGE
CLASS2_COLOR = TEAL

# Hand-placed so the new (grey) point's 3 nearest neighbors are a 2-1 mix
# (2x CLASS1, 1x CLASS2) -- a genuine majority vote, not a trivial 3-0 one.
SCENE7_CLASS1_PTS = [(-1.8, 1.6), (-0.9, 1.9), (-0.3, 0.9), (0.4, -0.3), (-1.5, -0.5), (1.6, 1.3)]
SCENE7_CLASS2_PTS = [(1.8, -1.6), (0.9, -1.9), (-1.9, -1.8), (0.5, 1.0)]
SCENE7_NEW_PT = (0.0, 1.1)
SCENE7_NEIGHBOR_KEY = {(-0.3, 0.9), (-0.9, 1.9), (0.5, 1.0)}  # the 3 nearest to SCENE7_NEW_PT
# Radius must clear the 3rd-nearest point's distance (~1.204) but stay below
# the 4th-nearest (~1.456) -- otherwise the circle only visually encloses 2
# points (a 1-1 tie) even though the k=3 majority-vote math assumes 3.
SCENE7_NEIGHBOR_RADIUS = 1.3


class Scene07Mixin:
    # ------------------------------------------------------------------
    # Scene 7: k-nearest neighbors
    # ------------------------------------------------------------------
    @staticmethod
    def scene7_pos(x, y, center):
        return center + RIGHT * x + UP * y

    @staticmethod
    def scene7_list_item(number, text, anchor, font_size=19):
        content = text if number == "" else f"{number}. {text}"
        return Text(content, font_size=font_size).next_to(anchor, DOWN, buff=0.2, aligned_edge=LEFT)

    def scene_07(self):
        title = Text("First Predictive Algorithm: k-NN", font_size=32).to_edge(UP, buff=0.4)

        with self.voiceover(
            text=(
                "Now that we know the overall predictive modeling pipeline, let's "
                "discuss two simple and commonly used classification algorithms. "
                "Our first algorithm is called k-nearest neighbors, or k-NN."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(tracker.get_remaining_duration())

        # -- Naive majority rule box --------------------------------------
        # All inner elements are laid out up front (so the border can be
        # sized to fit everything), but the 60/40 strip and the row of
        # points are only actually animated in once the narration reaches
        # the matching clause.
        box_title = Text("Naive Majority Rule", font_size=26, color=YELLOW)
        inner_desc = Text(
            "Predict the majority class for everyone", font_size=20
        ).next_to(box_title, DOWN, buff=0.35)
        bar = VGroup(
            Rectangle(width=3.6, height=0.7, color=CLASS1_COLOR, fill_opacity=0.8),
            Rectangle(width=2.4, height=0.7, color=CLASS2_COLOR, fill_opacity=0.8),
        ).arrange(RIGHT, buff=0).next_to(inner_desc, DOWN, buff=0.35)
        bar_labels = VGroup(
            Text("60%", font_size=20).move_to(bar[0].get_center()),
            Text("40%", font_size=20).move_to(bar[1].get_center()),
        )
        naive_group = VGroup(box_title, inner_desc, bar, bar_labels).move_to(UP * 1.1)
        box_border = SurroundingRectangle(naive_group, color=WHITE, buff=0.3, corner_radius=0.15)

        new_row = VGroup(*[Dot(radius=0.18, color=WHITE) for _ in range(6)]).arrange(RIGHT, buff=0.25).next_to(box_border, DOWN, buff=0.5)

        # Timing keyed to the ~19s clip: the 60/40 numbers and the "labels
        # every record" payoff both land in the back half of the sentence.
        with self.voiceover(
            text=(
                "To understand k-NN, it's worth first thinking about the simplest "
                "possible classifier: the naive majority rule. It simply "
                "classifies every point as the majority class. For example, if "
                "your training data is 60% class \"Orange\" and 40% class \"Green,\" the "
                "naive rule labels every single record as class \"Orange.\""
            )
        ) as tracker:
            self.wait(3.3)
            self.play(Create(box_border), Write(box_title), run_time=1.8)
            self.wait(1.5)
            self.play(Write(inner_desc), run_time=1.3)  # "classifies every point as the majority class"
            self.wait(4.1)
            self.play(FadeIn(bar), FadeIn(bar_labels), run_time=1.3)  # "60% class 1 and 40% class 0"
            self.wait(1.5)
            self.play(FadeIn(new_row, lag_ratio=0.1), run_time=0.8)
            self.wait(0.3)
            self.play(new_row.animate.set_color(CLASS1_COLOR), run_time=1.0)  # "labels every record as class 1"
            self.wait(tracker.get_remaining_duration())

        naive_all = VGroup(box_border, box_title, inner_desc, bar, bar_labels, new_row)

        scatter_center = LEFT * 3.6 + DOWN * 0.6
        c1_dots = VGroup(*[Dot(self.scene7_pos(x, y, scatter_center), color=CLASS1_COLOR) for x, y in SCENE7_CLASS1_PTS])
        c2_dots = VGroup(*[Dot(self.scene7_pos(x, y, scatter_center), color=CLASS2_COLOR) for x, y in SCENE7_CLASS2_PTS])
        all_train_dots = VGroup(*c1_dots, *c2_dots)
        new_dot = Dot(self.scene7_pos(*SCENE7_NEW_PT, scatter_center), color=GREY_B, radius=0.12)

        with self.voiceover(
            text=(
                "So, can we make the naive rule less naive? One elegant idea: "
                "instead of looking at the majority class among all training "
                "data, what if we only look at the majority class among training "
                "data that's similar to the new point? That's the gist of k-NN. "
                "The intuition is \"birds of a feather flock together\" -- data "
                "points near each other tend to be similar in their attributes, "
                "and similar points tend to share the same class."
            )
        ) as tracker:
            self.play(FadeOut(naive_all), run_time=1)
            self.play(FadeIn(all_train_dots, lag_ratio=0.08), run_time=1.5)
            self.play(FadeIn(new_dot, scale=0.5), run_time=1)
            self.play(all_train_dots.animate.set_opacity(0.25), run_time=1)
            neighbor_dots = VGroup(
                *[d for d, (x, y) in zip(c1_dots, SCENE7_CLASS1_PTS) if (x, y) in SCENE7_NEIGHBOR_KEY],
                *[d for d, (x, y) in zip(c2_dots, SCENE7_CLASS2_PTS) if (x, y) in SCENE7_NEIGHBOR_KEY],
            )
            neighbor_circle = Circle(radius=SCENE7_NEIGHBOR_RADIUS, color=WHITE, stroke_width=2.5).move_to(new_dot.get_center())
            self.play(Create(neighbor_circle), run_time=1.5)
            self.play(neighbor_dots.animate.set_opacity(1), run_time=1)
            self.wait(tracker.get_remaining_duration())

        # -- k-NN procedure list -------------------------------------------
        proc_title = Text("k-NN Procedure", font_size=22, color=YELLOW).move_to(RIGHT * 2.6 + UP * 2.7)
        step1 = self.scene7_list_item(1, "Pick k (e.g., k = 3)", proc_title)
        step2 = self.scene7_list_item(2, "Find k nearest training points", step1)
        step3 = self.scene7_list_item(3, "Find majority class among them", step2)
        step3b = self.scene7_list_item("", "(Tie? Pick randomly)", step3, font_size=17)

        with self.voiceover(
            text=(
                "The k-NN procedure is simple. You pick a value of k. Then, for "
                "every new data point, you find the k nearest points in the "
                "training data, and predict the majority class among those k "
                "neighbors. If there's a tie, you just pick a class at random."
            )
        ) as tracker:
            self.play(Write(proc_title), run_time=1.5)
            self.play(FadeIn(step1, shift=RIGHT * 0.2), run_time=2)
            self.play(FadeIn(step2, shift=RIGHT * 0.2), run_time=2)
            self.play(Indicate(neighbor_circle, color=YELLOW), run_time=1.5)
            self.play(FadeIn(step3, shift=RIGHT * 0.2), run_time=2)
            self.play(new_dot.animate.set_color(CLASS1_COLOR), run_time=1)  # majority vote -> predicted class
            self.play(FadeIn(step3b, shift=RIGHT * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        footnote = Text(
            "Requires normalized data --\ndistance-based, just like clustering.",
            font_size=15,
            color=GREY_B,
            line_spacing=1.0,
        ).next_to(step3b, DOWN, buff=0.35, aligned_edge=LEFT)

        with self.voiceover(
            text=(
                "Keep in mind that k-NN relies on distance calculations to find "
                "the nearest neighbors, so you need to normalize your data when "
                "necessary -- the same distance-metric and normalization ideas "
                "covered in the clustering video apply here."
            )
        ) as tracker:
            self.play(FadeIn(footnote, shift=UP * 0.1), run_time=2)
            self.wait(tracker.get_remaining_duration())

        # -- Choosing k list -------------------------------------------------
        tune_title = Text("Choosing k: Model Tuning", font_size=22, color=YELLOW).next_to(
            footnote, DOWN, buff=0.5, aligned_edge=LEFT
        )
        tune1 = self.scene7_list_item(1, "Try different k values", tune_title)
        tune2 = self.scene7_list_item(2, "Pick best validation performance", tune1)
        tune3 = self.scene7_list_item(3, "Small k: local structure", tune2, font_size=17)
        tune4 = self.scene7_list_item(4, "Large k: global structure", tune3, font_size=17)

        with self.voiceover(
            text=(
                "A natural question is how do we pick k? This is a model tuning "
                "question -- and the standard, general-purpose approach in "
                "predictive machine learning is to try different parameter values "
                "and pick whichever gives the best performance on the validation "
                "data. For k-NN specifically, you try different k values and pick "
                "the one that makes the most accurate predictions on the "
                "validation set."
            )
        ) as tracker:
            self.play(Write(tune_title), run_time=2)
            self.wait(8.0)
            self.play(FadeIn(tune1, shift=RIGHT * 0.2), run_time=2)
            self.play(FadeIn(tune2, shift=RIGHT * 0.2), run_time=2)
            self.wait(tracker.get_remaining_duration())

        small_circle = Circle(radius=0.7, color=WHITE, stroke_width=2.5).move_to(new_dot.get_center())
        large_circle = Circle(radius=1.9, color=WHITE, stroke_width=2.5).move_to(new_dot.get_center())
        huge_circle = Circle(radius=3.6, color=WHITE, stroke_width=2.5).move_to(new_dot.get_center())
        orig_circle = Circle(radius=SCENE7_NEIGHBOR_RADIUS, color=WHITE, stroke_width=2.5).move_to(new_dot.get_center())

        with self.voiceover(
            text=(
                "As a rule of thumb: small k values focus on local structure but "
                "are more sensitive to noise -- even one noisy point can flip a "
                "prediction. Large k values are more robust to noise but wash out "
                "local structure. In fact, if k equals the size of the entire "
                "training set, k-NN becomes identical to the naive rule. The good "
                "news is you don't have to guess -- you can just try a range of k "
                "values and pick whichever objectively performs best on "
                "validation data."
            )
        ) as tracker:
            self.wait(2.0)
            self.play(Transform(neighbor_circle, small_circle), run_time=2.0)  # "small k values"
            self.play(FadeIn(tune3, shift=RIGHT * 0.2), run_time=1.2)
            self.wait(3.0)
            self.play(Transform(neighbor_circle, large_circle), run_time=2.0)  # "Large k values"
            self.play(FadeIn(tune4, shift=RIGHT * 0.2), run_time=1.2)
            self.wait(2.5)
            self.play(
                Transform(neighbor_circle, huge_circle), all_train_dots.animate.set_opacity(1), run_time=2.0
            )  # "k equals the size of the entire training set"
            self.wait(2.0)
            self.play(
                Transform(neighbor_circle, orig_circle),
                all_train_dots.animate.set_opacity(0.25),
                neighbor_dots.animate.set_opacity(1),
                run_time=1.2,
            )
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(all_train_dots), FadeOut(new_dot), FadeOut(neighbor_circle),
            FadeOut(proc_title), FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(step3b), FadeOut(footnote),
            FadeOut(tune_title), FadeOut(tune1), FadeOut(tune2), FadeOut(tune3), FadeOut(tune4),
        )


class Scene07(VoiceoverScene, Scene07Mixin):
    """Standalone preview: manim -pql scene_07.py Scene07"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_07()
