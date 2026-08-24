import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_pipeline_diagram, make_gear


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: the standard predictive modeling pipeline
    # ------------------------------------------------------------------
    def scene_03(self):
        title, left_box, right_box, whole = make_pipeline_diagram()

        with self.voiceover(
            text=(
                "Regardless of the prediction target or learning algorithm, "
                "building a predictive model typically follows a standard "
                "pipeline."
            )
        ) as tracker:
            self.play(Write(title), run_time=tracker.duration * 0.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "First, training a predictive model requires a labeled dataset, "
                "containing data for which you already know the outcome you're "
                "trying to predict; this could be historical data with observed "
                "outcomes, or a manually labeled sample."
            )
        ) as tracker:
            self.play(FadeIn(left_box, shift=UP * 0.3), run_time=2.5)
            self.play(Circumscribe(left_box, color=YELLOW), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Second, deployment of the predictive model is typically done on "
                "the unlabeled dataset, with the data for which you want to "
                "predict the outcome."
            )
        ) as tracker:
            self.play(FadeIn(right_box, shift=UP * 0.3), run_time=2.5)
            self.play(Circumscribe(right_box, color=YELLOW), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        gear = make_gear("Model").scale(0.9).move_to(DOWN * 2.3)
        arrow_to_gear = Arrow(left_box.get_bottom(), gear.get_left(), color=WHITE, buff=0.15)
        arrow_from_gear = Arrow(gear.get_right(), right_box.get_bottom(), color=WHITE, buff=0.15)

        with self.voiceover(
            text=(
                "Both stages of the pipeline center on the same predictive "
                "model: it's built using the labeled training data, and once "
                "trained, that same model is applied to generate predictions on "
                "the unlabeled data."
            )
        ) as tracker:
            self.play(FadeIn(gear, scale=0.7), run_time=1.2)
            self.play(GrowArrow(arrow_to_gear), run_time=1.2)
            self.play(GrowArrow(arrow_from_gear), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(FadeOut(whole), FadeOut(gear), FadeOut(arrow_to_gear), FadeOut(arrow_from_gear))

        self.pipeline_title = title
        self.pipeline_left_box = left_box
        self.pipeline_right_box = right_box
        self.pipeline_whole = whole


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_03()
