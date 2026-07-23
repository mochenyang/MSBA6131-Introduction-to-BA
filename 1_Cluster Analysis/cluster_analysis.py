import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import Text, Write
from manim_voiceover import VoiceoverScene

from tts import get_speech_service


class ClusterAnalysis(VoiceoverScene):
    def construct(self):
        self.set_speech_service(get_speech_service())

        title = Text("Cluster Analysis")
        with self.voiceover(text="This video discusses Cluster Analysis") as tracker:
            self.play(Write(title), run_time=tracker.duration)
        self.wait()
