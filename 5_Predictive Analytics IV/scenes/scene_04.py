import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: summary -- why cross validation is more robust than a
    # single training-validation split
    # ------------------------------------------------------------------
    @staticmethod
    def scene4_checkbox_item(text, font_size=24):
        box = Square(side_length=0.32, color=WHITE, stroke_width=2.5)
        label = Text(text, font_size=font_size)
        label.next_to(box, RIGHT, buff=0.25)
        c = box.get_center()
        # Checkmark vertex sits near the box's bottom (not its vertical
        # center) so the two strokes actually read as a "V" dip -> upstroke
        # (same construction as scene_05 in unit 1, scaled to this box size).
        check = VGroup(
            Line(c + LEFT * 0.1 + UP * 0.015, c + DOWN * 0.1, color=GREEN),
            Line(c + DOWN * 0.1, c + RIGHT * 0.12 + UP * 0.12, color=GREEN),
        ).set_stroke(width=3.5)
        return VGroup(box, label, check)

    @staticmethod
    def scene4_sub_bullet(text, font_size=19, color=GREY_B):
        dash = Text("–", font_size=font_size, color=color)
        label = Text(text, font_size=font_size, color=color)
        label.next_to(dash, RIGHT, buff=0.15)
        return VGroup(dash, label)

    def scene_04(self):
        title = Text("Cross Validation: Summary", font_size=30).to_edge(UP, buff=0.4)

        item1 = self.scene4_checkbox_item("Single training-validation split can produce unstable results")
        sub1a = self.scene4_sub_bullet("Validation set too easy → overestimate performance")
        sub1b = self.scene4_sub_bullet("Validation set too hard → underestimate performance")
        sub1a.next_to(item1, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.15)
        sub1b.next_to(sub1a, DOWN, buff=0.2).align_to(sub1a, LEFT)
        block1 = VGroup(item1, sub1a, sub1b)
        block1.next_to(title, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)

        with self.voiceover(
            text=(
                "To summarize, compared to a single training-validation split, "
                "cross validation tends to produce a more robust and stable "
                "estimate of a model's performance. In a single split, we might "
                "happen to get a validation dataset that's too easy or too hard "
                "to predict, simply due to random chance — and as a result, the "
                "model's performance can be under- or overestimated because of "
                "an unlucky split."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.2)
            self.wait(2.0)
            self.play(FadeIn(item1, shift=RIGHT * 0.2), run_time=1.0)
            self.wait(3.0)
            self.play(FadeIn(sub1a, shift=RIGHT * 0.1), run_time=0.9)
            self.wait(2.5)
            self.play(FadeIn(sub1b, shift=RIGHT * 0.1), run_time=0.9)
            self.wait(tracker.get_remaining_duration())

        item2 = self.scene4_checkbox_item("Cross validation provides more robust performance evaluation")
        sub2a = self.scene4_sub_bullet("Every data point is in the validation fold exactly once")
        sub2b = self.scene4_sub_bullet("Aggregating performance across rounds gives a stable measure")
        sub2c = self.scene4_sub_bullet("High variance across rounds signals noisy or small data")
        sub2a.next_to(item2, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.15)
        sub2b.next_to(sub2a, DOWN, buff=0.2).align_to(sub2a, LEFT)
        sub2c.next_to(sub2b, DOWN, buff=0.2).align_to(sub2a, LEFT)
        block2 = VGroup(item2, sub2a, sub2b, sub2c)
        block2.next_to(block1, DOWN, buff=0.55).align_to(block1, LEFT)

        with self.voiceover(
            text=(
                "Cross validation is much more robust against this problem, "
                "because every data point ends up in the validation fold at "
                "exactly one round, and aggregating performance across all "
                "rounds gives a more stable measure. As a bonus, if we observe "
                "that performance varies dramatically across rounds, that's "
                "actually a useful signal — it suggests the labeled data may be "
                "too noisy or too small."
            )
        ) as tracker:
            self.play(FadeIn(item2, shift=RIGHT * 0.2), run_time=1.0)
            self.wait(3.0)
            self.play(FadeIn(sub2a, shift=RIGHT * 0.1), run_time=0.8)
            self.wait(3.0)
            self.play(FadeIn(sub2b, shift=RIGHT * 0.1), run_time=0.8)
            self.wait(3.0)
            self.play(FadeIn(sub2c, shift=RIGHT * 0.1), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(block1), FadeOut(block2))


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
