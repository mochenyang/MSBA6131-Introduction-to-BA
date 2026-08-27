import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from scenes.scene_01 import Scene01Mixin
from scenes.scene_02 import Scene02Mixin
from scenes.scene_03 import Scene03Mixin
from scenes.scene_04 import Scene04Mixin
from scenes.scene_05 import Scene05Mixin
from scenes.scene_06 import Scene06Mixin
from scenes.scene_07 import Scene07Mixin
from scenes.scene_08 import Scene08Mixin


class PredictiveAnalyticsII(
    VoiceoverScene,
    Scene01Mixin,
    Scene02Mixin,
    Scene03Mixin,
    Scene04Mixin,
    Scene05Mixin,
    Scene06Mixin,
    Scene07Mixin,
    Scene08Mixin,
):
    def construct(self):
        self.set_speech_service(get_speech_service())

        self.scene_01()
        self.scene_02()
        self.scene_03()
        self.scene_04()
        self.scene_05()
        self.scene_06()
        self.scene_07()
        self.scene_08()
