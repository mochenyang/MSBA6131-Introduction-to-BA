import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service


class Scene01Mixin:
    def scene_01(self):
        title = Text("Cluster Analysis")
        with self.voiceover(text="This video will discuss cluster analysis.") as tracker:
            self.play(Write(title), run_time=tracker.duration)
        self.wait()
        self.title_scene_01 = title


class Scene01(VoiceoverScene, Scene01Mixin):
    """Standalone preview: manim -pql scene_01.py Scene01"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_01()
