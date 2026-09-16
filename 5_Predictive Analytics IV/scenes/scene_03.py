import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, NEUTRAL_COLOR, SCORE_COLOR, make_fold_bar


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: two ways to report cross-validation performance results
    # ------------------------------------------------------------------
    def scene_03(self):
        title = Text("Cross Validation: Reporting Evaluation Results", font_size=28).to_edge(UP, buff=0.4)

        fold_bar = self.scene02_fold_bar
        scores = self.scene02_scores
        # Only the fold bar itself is shown as the "recap" anchor -- the
        # scores stay off in their scene_02 resting position and are first
        # revealed via TransformFromCopy into each panel below.
        recap_group = fold_bar["group"]

        with self.voiceover(
            text=(
                "So how do we obtain performance results from cross validation? "
                "There are two ways to do it. First, we can aggregate the "
                "performance measures across rounds: in each of the k rounds we "
                "obtain a performance score (such as accuracy) — we can then "
                "report the mean and standard deviation of those k performance "
                "scores."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.2)
            self.play(FadeIn(recap_group), run_time=0.8)
            self.play(
                recap_group.animate.scale(0.6).next_to(title, DOWN, buff=0.35),
                run_time=0.9,
            )
            self.wait(2.0)

            panel_row_y = recap_group.get_bottom()[1] - 0.55
            left_title = Text("Aggregate Per-Round Measures", font_size=22, color=YELLOW)
            left_title.move_to(np.array([-3.3, panel_row_y, 0]))
            self.play(FadeIn(left_title), run_time=0.8)

            score_copies = VGroup(*[s.copy() for s in scores]).arrange(DOWN, buff=0.25)
            score_copies.next_to(left_title, DOWN, buff=0.4).align_to(left_title, LEFT).shift(RIGHT * 0.6)
            self.play(
                *[TransformFromCopy(s, sc) for s, sc in zip(scores, score_copies)],
                run_time=1.3,
            )
            self.wait(2.0)

            mean_label = Text("Mean", font_size=18, color=SCORE_COLOR)
            mean_eq = MathTex(r"=\ \dfrac{s_1+s_2+s_3+s_4+s_5}{5}", font_size=26)
            mean_row = VGroup(mean_label, mean_eq).arrange(RIGHT, buff=0.2)
            mean_row.next_to(score_copies, DOWN, buff=0.45).align_to(left_title, LEFT)
            self.play(TransformFromCopy(score_copies, mean_eq), FadeIn(mean_label), run_time=1.2)

            sd_label = Text("SD", font_size=18, color=SCORE_COLOR)
            sd_eq = MathTex(r"=\ \sigma(s_1, s_2, s_3, s_4, s_5)", font_size=26)
            sd_row = VGroup(sd_label, sd_eq).arrange(RIGHT, buff=0.2)
            sd_row.next_to(mean_row, DOWN, buff=0.3).align_to(left_title, LEFT)
            self.play(FadeIn(sd_row, shift=UP * 0.1), run_time=1.2)
            
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Second, we can combine the predictions from each round's "
                "validation fold into one pooled set of predictions, and then "
                "calculate the performance measure directly on that combined "
                "set. Either approach is valid for reporting cross-validation "
                "performance, though they may not necessarily give the same "
                "results."
            )
        ) as tracker:
            
            right_title = Text("Pool Predictions First", font_size=22, color=YELLOW)
            right_title.move_to(np.array([3.3, panel_row_y, 0]))
            self.play(FadeIn(right_title), run_time=0.8)

            fold_icons = VGroup(
                *[
                    RoundedRectangle(width=0.55, height=0.4, corner_radius=0.05, color=GREY_B)
                    for _ in range(5)
                ]
            ).arrange(RIGHT, buff=0.15)
            fold_icons.next_to(right_title, DOWN, buff=0.4)
            self.play(FadeIn(fold_icons, shift=DOWN * 0.1), run_time=0.8)
            self.wait(1.0)

            combined_box = RoundedRectangle(width=2.7, height=0.7, corner_radius=0.08, color=WHITE)
            combined_label = Text("Pooled Predictions", font_size=14).move_to(combined_box.get_center())
            combined = VGroup(combined_box, combined_label).next_to(fold_icons, DOWN, buff=0.4)
            icon_copies = fold_icons.copy()
            self.play(
                *[ic.animate.move_to(combined_box.get_center()).scale(0.3) for ic in icon_copies],
                run_time=1.0,
            )
            self.play(FadeOut(icon_copies), FadeIn(combined_box), FadeIn(combined_label), run_time=0.6)
            self.wait(2.0)

            accuracy_eq = MathTex(r"\text{Directly Calculate Performance}", font_size=24, color=SCORE_COLOR).next_to(
                combined, DOWN, buff=0.35
            )
            self.play(FadeIn(accuracy_eq, shift=DOWN * 0.1), run_time=0.8)

            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_02()
        self.scene_03()

    def _fixture_scene_02(self):
        # Stand-in for scene_02's ending state (the 5-fold bar and its 5
        # scores, faded out) so scene_03 can be previewed alone, without
        # replaying scene_02's narration/animation.
        fold_bar = make_fold_bar(n_folds=5)
        # Matches scene_02's real settled score row -- see scene_02.py's
        # run_round()/scores_row_y for the real computation.
        scores = []
        for i in range(5):
            score = MathTex(f"s_{{{i + 1}}}", color=SCORE_COLOR, font_size=30)
            score.move_to(fold_bar["rects"][i].get_bottom() + DOWN * 2.5)
            scores.append(score)
        self.scene02_fold_bar = fold_bar
        self.scene02_scores = scores
