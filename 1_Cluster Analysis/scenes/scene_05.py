import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_customer_axes, make_customer_clusters, Text


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: Ingredients needed for clustering
    # ------------------------------------------------------------------
    @staticmethod
    def make_checklist_item(text, y_pos):
        box = Square(side_length=0.4, color=WHITE).move_to(LEFT * 5.2 + UP * y_pos)
        label = Text(text, font_size=28).next_to(box, RIGHT, buff=0.3)
        c = box.get_center()
        # Checkmark vertex sits near the box's bottom (not its vertical
        # center) so the two strokes actually read as a "V" dip -> upstroke.
        check = VGroup(
            Line(c + LEFT * 0.13 + UP * 0.02, c + DOWN * 0.12, color=GREEN),
            Line(c + DOWN * 0.12, c + RIGHT * 0.15 + UP * 0.15, color=GREEN),
        ).set_stroke(width=4)
        return box, label, check

    def scene_05(self):
        with self.voiceover(
            text="So, how do we conduct clustering analysis? Let's first lay out the ingredients we need."
        ) as tracker:
            title = Text("Ingredients for Clustering", font_size=36).to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=2)
            self.wait(1.0)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "If the dataset has low dimensions -- in other words, a small number "
                "of variables describing each data point -- clustering can be as "
                "simple as plotting the data and visually identifying clusters."
            )
        ) as tracker:
            note1 = Text(
                "Low dimensions? Just plot the data and eyeball the clusters.",
                font_size=26,
                color=YELLOW,
            ).next_to(title, DOWN, buff=0.8)
            self.play(FadeIn(note1, shift=UP * 0.2), run_time=2)

            # Concretely re-show the Walmart scatter plot, small, as the
            # "just plot it and eyeball the clusters" example being narrated.
            mini_axes, _, _ = make_customer_axes()
            mini_groups = make_customer_clusters(mini_axes)
            mini_plot = VGroup(mini_axes, *mini_groups).scale(0.35).next_to(note1, DOWN, buff=0.5)
            self.play(Create(mini_axes), run_time=1.3)
            self.play(FadeIn(VGroup(*mini_groups), lag_ratio=0.05), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "In general, however, once there are more than three variables in "
                "the dataset, we need a systematic approach to clustering."
            )
        ) as tracker:
            note2 = Text(
                "More than 3 variables? We need a systematic approach:",
                font_size=26,
                color=YELLOW,
            ).next_to(title, DOWN, buff=0.8)
            self.play(FadeOut(mini_plot), run_time=1)
            self.play(FadeTransform(note1, note2), run_time=2.0)
            self.wait(tracker.get_remaining_duration())

        box1, label1, check1 = self.make_checklist_item("Measure similarity between data points", 1.3)
        box2, label2, check2 = self.make_checklist_item(
            "Apply certain clustering algorithms", -0.4
        )
        box3, label3, check3 = self.make_checklist_item("Interpret clustering results", -2.1)

        sub1 = Text(
            "→ similar data points, same cluster", font_size=20, color=GRAY
        ).next_to(label1, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.voiceover(
            text=(
                "First, we need to be able to measure the similarity between data "
                "points, because we want to put similar data points in the same "
                "cluster and dissimilar ones in different clusters."
            )
        ) as tracker:
            self.play(Create(box1), Write(label1), run_time=1.5)
            self.play(Create(check1), run_time=1)
            self.play(FadeIn(sub1, shift=UP * 0.1), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        sub2 = Text(
            "→ also evaluate clustering quality", font_size=20, color=GRAY
        ).next_to(label2, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.voiceover(
            text=(
                "Second, we need to apply certain clustering algorithms  "
                "and be able to evaluate the quality of a clustering solution. "
            )
        ) as tracker:
            self.play(Create(box2), Write(label2), run_time=1.5)
            self.play(Create(check2), run_time=1)
            self.play(FadeIn(sub2, shift=UP * 0.1), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        sub3 = Text(
            "→ what does each cluster represent?", font_size=20, color=GRAY
        ).next_to(label3, DOWN, buff=0.15, aligned_edge=LEFT)
        with self.voiceover(
            text=(
                "Finally, we need to be able to interpret clustering results and "
                "make sense of each cluster."
            )
        ) as tracker:
            self.play(Create(box3), Write(label3), run_time=1.5)
            self.play(Create(check3), run_time=0.8)
            self.play(FadeIn(sub3, shift=UP * 0.1), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(note2),
            FadeOut(box1), FadeOut(label1), FadeOut(check1), FadeOut(sub1),
            FadeOut(box2), FadeOut(label2), FadeOut(check2), FadeOut(sub2),
            FadeOut(box3), FadeOut(label3), FadeOut(check3), FadeOut(sub3),
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_05()
