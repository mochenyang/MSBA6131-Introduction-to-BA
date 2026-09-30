import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text


class Scene01Mixin:
    def scene_01(self):
        title = Text("Numeric Prediction", font_size=48)
        subtitle = Text("Methods and Evaluation", font_size=26, color=YELLOW).next_to(
            title, DOWN, buff=0.4
        )

        with self.voiceover(
            text=(
                "In this video, we will look into the topic of numeric prediction. "
                "We will discuss how common classification techniques can be adapted "
                "for numeric prediction, how to evaluate numeric prediction "
                "performance, and also learn a new technique called linear "
                "regression."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.5)
            self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))


class Scene01(VoiceoverScene, Scene01Mixin):
    """Standalone preview: manim -pql scene_01.py Scene01"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_01()
