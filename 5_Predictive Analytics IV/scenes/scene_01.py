import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text


class Scene01Mixin:
    # ------------------------------------------------------------------
    # Scene 1: title card
    # ------------------------------------------------------------------
    def scene_01(self):
        title = Text("Predictive Analytics", font_size=48)
        subtitle = Text("Cross Validation & Feature Selection", font_size=24, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)

        with self.voiceover(
            text=(
                "In this video, we'll cover two important topics in predictive "
                "analytics: cross validation, a robust way to evaluate the "
                "performance of a predictive model, and feature selection, a "
                "set of techniques for choosing which features to include in "
                "a predictive model."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(1.0)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(FadeOut(title), FadeOut(subtitle))


class Scene01(VoiceoverScene, Scene01Mixin):
    """Standalone preview: manim -pql scene_01.py Scene01"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_01()
