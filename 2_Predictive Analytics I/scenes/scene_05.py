import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_pipeline_diagram, make_gear, TRAIN_COLOR, VALIDATION_COLOR


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: the training-validation split
    # ------------------------------------------------------------------
    def scene_05(self):
        pipeline = self.pipeline_whole
        left_box = self.pipeline_left_box
        right_box = self.pipeline_right_box

        with self.voiceover(
            text=(
                "So how do we deal with overfitting? A simple yet effective "
                "solution is the training-validation split."
            )
        ) as tracker:
            self.play(FadeIn(pipeline), run_time=1.5)
            self.play(pipeline.animate.scale(0.6).to_edge(UP, buff=0.3), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # Equal-sized boxes -- same width/height for Training and Validation,
        # since the plan's "larger / smaller portion" distinction is carried
        # by the narration, not by mismatched box sizes (which clipped the
        # "Validation Data" label before).
        train_box = RoundedRectangle(width=2.4, height=1.3, color=TRAIN_COLOR, corner_radius=0.15)
        train_label = Text("Training Data", font_size=20, color=TRAIN_COLOR).move_to(train_box.get_center())
        train_group = VGroup(train_box, train_label).move_to(left_box.get_bottom() + DOWN * 1.1 + LEFT * 1.5)

        val_box = RoundedRectangle(width=2.4, height=1.3, color=VALIDATION_COLOR, corner_radius=0.15)
        val_label = Text("Validation Data", font_size=20, color=VALIDATION_COLOR).move_to(val_box.get_center())
        val_group = VGroup(val_box, val_label).move_to(left_box.get_bottom() + DOWN * 1.1 + RIGHT * 1.5)

        split_lines = VGroup(
            Line(left_box.get_bottom(), train_group.get_top(), color=GREY_B, stroke_width=2),
            Line(left_box.get_bottom(), val_group.get_top(), color=GREY_B, stroke_width=2),
        )

        with self.voiceover(
            text=(
                "Given a set of labeled data, we randomly split it into two "
                "parts: training data and validation data -- sometimes also "
                "called \"testing data\"."
            )
        ) as tracker:
            self.play(Create(split_lines), run_time=1)
            self.play(FadeIn(train_group, shift=DOWN * 0.2), FadeIn(val_group, shift=DOWN * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # Gear sits centered below both data boxes, well clear of them
        # vertically -- same look/scale as scene_03's gear so "Model" reads
        # as the same recurring element. Train is up-left of it, Validation
        # up-right, symmetric.
        gear = make_gear("Model").scale(0.9).move_to(VGroup(train_group, val_group).get_bottom() + DOWN * 1.3)
        arrow1 = Arrow(train_group.get_bottom(), gear.get_left(), color=WHITE, buff=0.15)

        with self.voiceover(
            text=(
                "We use the training data to build the model."
                "But we don't evaluate the model's performance on the training "
                "data, since it may have overfit that data. "
            )
        ) as tracker:
            self.play(GrowArrow(arrow1), run_time=0.7)
            self.play(FadeIn(gear, scale=0.7), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        arrow2 = Arrow(gear.get_right(), val_group.get_bottom(), color=WHITE, buff=0.15)
        eval_label = Text("Performance Eval", font_size=18, color=YELLOW).next_to(arrow2, RIGHT, buff=0.15)

        with self.voiceover(
            text=(
                "Instead, we evaluate performance on the validation data"
                " -- data the model hasn't seen during training."
            )
        ) as tracker:
            self.play(GrowArrow(arrow2), run_time=1.5)
            self.play(FadeIn(eval_label), run_time=1)
            self.play(Circumscribe(val_group, color=YELLOW), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # A right-angle polyline (out from the gear, then up into the
        # deployment box) instead of a single diagonal arrow -- stays clear
        # of Validation Data since the horizontal leg runs well below it and
        # the vertical leg only turns upward once past its right edge.
        elbow = np.array([right_box.get_bottom()[0], gear.get_right()[1], 0])
        arrow3_leg1 = Line(gear.get_right(), elbow, color=WHITE)
        arrow3_leg2 = Arrow(elbow, right_box.get_bottom(), color=WHITE, buff=0)
        arrow3 = VGroup(arrow3_leg1, arrow3_leg2)
        deploy_label = Text("Generalizes to Deployment", font_size=18, color=GREEN).next_to(arrow3_leg1, DOWN, buff=0.25).shift(RIGHT * 0.2)

        with self.voiceover(
            text=(
                "If the model performs well there, it probably learned something "
                "genuinely generalizable, and it should also perform well on new, "
                "unseen data at deployment."
            )
        ) as tracker:
            self.play(Create(arrow3_leg1), run_time=0.6)
            self.play(GrowArrow(arrow3_leg2), run_time=0.9)
            self.play(FadeIn(deploy_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(pipeline), FadeOut(right_box), FadeOut(train_group), FadeOut(val_group),
            FadeOut(split_lines), FadeOut(gear), FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
            FadeOut(eval_label), FadeOut(deploy_label),
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_03()
        self.scene_05()

    def _fixture_scene_03(self):
        # Stand-in for scene_03's ending state (pipeline diagram, faded out)
        # so scene_05 can be previewed alone, without replaying scene_03.
        title, left_box, right_box, whole = make_pipeline_diagram()
        self.pipeline_title = title
        self.pipeline_left_box = left_box
        self.pipeline_right_box = right_box
        self.pipeline_whole = whole
