import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, TRAIN_COLOR, VALIDATION_COLOR, SCORE_COLOR, NEUTRAL_COLOR, make_fold_bar


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: cross validation -- intuition (recap + generalization) and
    # the k-fold procedure, illustrated concretely with k = 5.
    # ------------------------------------------------------------------
    @staticmethod
    def scene2_make_gear(radius=0.32, label_text="Model", font_size=13):
        circle = Circle(radius=radius, color=WHITE, stroke_width=2.5)
        teeth = VGroup(
            *[
                Rectangle(width=radius * 0.22, height=radius * 0.32, color=WHITE, fill_opacity=1)
                .move_to(circle.get_center() + (radius + 0.09) * np.array([np.cos(a), np.sin(a), 0]))
                .rotate(a)
                for a in np.linspace(0, 2 * PI, 8, endpoint=False)
            ]
        )
        label = Text(label_text, font_size=font_size).move_to(circle.get_center())
        return VGroup(teeth, circle, label)

    def scene_02(self):
        title = Text("Cross Validation: Intuition and Procedure", font_size=30).to_edge(UP, buff=0.4)

        # -- Block 1: recap of the training-validation split ------------
        labeled_box = RoundedRectangle(width=2.4, height=0.9, color=WHITE, corner_radius=0.12)
        labeled_label = Text("Labeled Data", font_size=20).move_to(labeled_box.get_center())
        labeled_group = VGroup(labeled_box, labeled_label).next_to(title, DOWN, buff=0.55)

        train_box = RoundedRectangle(width=2.3, height=1.0, color=TRAIN_COLOR, corner_radius=0.12)
        train_label = Text("Training Data", font_size=18, color=TRAIN_COLOR).move_to(train_box.get_center())
        train_group = VGroup(train_box, train_label).move_to(labeled_group.get_bottom() + DOWN * 1.1 + LEFT * 2.2)

        val_box = RoundedRectangle(width=2.3, height=1.0, color=VALIDATION_COLOR, corner_radius=0.12)
        val_label = Text("Validation Data", font_size=18, color=VALIDATION_COLOR).move_to(val_box.get_center())
        val_group = VGroup(val_box, val_label).move_to(labeled_group.get_bottom() + DOWN * 1.1 + RIGHT * 2.2)

        split_lines = VGroup(
            Line(labeled_group.get_bottom(), train_group.get_top(), color=GREY_B, stroke_width=2),
            Line(labeled_group.get_bottom(), val_group.get_top(), color=GREY_B, stroke_width=2),
        )

        recap_gear = self.scene2_make_gear(radius=0.38).move_to(
            VGroup(train_group, val_group).get_bottom() + DOWN * 1.1
        )
        recap_arrow1 = Arrow(train_group.get_bottom(), recap_gear.get_left(), color=WHITE, buff=0.12)
        recap_arrow2 = Arrow(recap_gear.get_right(), val_group.get_bottom(), color=WHITE, buff=0.12)
        recap_eval_label = Text("Performance Eval", font_size=16, color=YELLOW).next_to(
            recap_arrow2, RIGHT, buff=0.12
        )

        recap_group = VGroup(
            labeled_group, split_lines, train_group, val_group,
            recap_gear, recap_arrow1, recap_arrow2, recap_eval_label,
        )

        with self.voiceover(
            text=(
                "In a previous video, we talked about using the training-validation "
                "split to evaluate the performance of a predictive model: we split "
                "the labeled data randomly into a training set and a validation "
                "set, build the model on the training set, and evaluate it on the "
                "validation set to get a performance measure that's less affected "
                "by overfitting."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.3)
            self.play(FadeIn(labeled_group), run_time=0.8)
            self.play(Create(split_lines), run_time=0.7)
            self.play(FadeIn(train_group, shift=DOWN * 0.15), FadeIn(val_group, shift=DOWN * 0.15), run_time=1.0)
            self.play(GrowArrow(recap_arrow1), FadeIn(recap_gear, scale=0.7), run_time=0.9)
            self.play(GrowArrow(recap_arrow2), FadeIn(recap_eval_label), run_time=0.9)
            self.wait(tracker.get_remaining_duration())

        # -- Block 2: the general k-fold procedure -----------------------
        pseudo_title = Text("k-Fold Cross Validation", font_size=22, color=YELLOW)
        line0 = Text("Input: k (number of folds)", font_size=20)
        line1 = Text("1. Partition data into k folds", font_size=20)
        line2 = Text("2. For each round i = 1..k:", font_size=20)
        line3 = Text("     Train on the other k-1 folds", font_size=18, color=TRAIN_COLOR)
        line4 = Text("     Validate on fold i", font_size=18, color=VALIDATION_COLOR)
        line5 = Text("3. Repeat for all k rounds", font_size=20)
        code_lines = VGroup(line0, line1, line2, line3, line4, line5).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22
        )
        code_box = SurroundingRectangle(code_lines, color=WHITE, buff=0.3, corner_radius=0.12)
        pseudo_title.next_to(code_box, UP, buff=0.2)
        pseudocode = VGroup(pseudo_title, code_box, code_lines)
        pseudocode.move_to(LEFT * 3.4 + DOWN * 0.4)

        fold_bar = make_fold_bar(n_folds=5)
        fold_bar["group"].scale(0.85).move_to(RIGHT * 3.0 + UP * 0.4)

        gear = self.scene2_make_gear().next_to(fold_bar["group"], DOWN, buff=0.9)
        scores_row_y = gear.get_bottom()[1] - 0.55

        def score_slot_pos(i):
            return np.array([fold_bar["rects"][i].get_center()[0], scores_row_y, 0])

        def run_round(i, run_time_scale=1.0):
            """Highlight fold i as validation, the rest as training, show
            the model gear building on the training folds and producing a
            score, then settle that score under fold i and reset colors."""
            others = [j for j in range(5) if j != i]
            self.play(
                *[fold_bar["rects"][j].animate.set_color(TRAIN_COLOR) for j in others],
                *[fold_bar["dots"][j].animate.set_color(TRAIN_COLOR) for j in others],
                fold_bar["rects"][i].animate.set_color(VALIDATION_COLOR),
                fold_bar["dots"][i].animate.set_color(VALIDATION_COLOR),
                run_time=0.5 * run_time_scale,
            )
            gear.move_to(
                VGroup(*[fold_bar["rects"][j] for j in others]).get_center() + DOWN * 0.9
            )
            arrow = Arrow(gear.get_top(), fold_bar["rects"][i].get_bottom(), color=WHITE, buff=0.1, stroke_width=2.5)
            score = MathTex(f"s_{{{i + 1}}}", color=SCORE_COLOR, font_size=30)
            score.move_to(fold_bar["rects"][i].get_bottom() + DOWN * 0.35)
            self.play(FadeIn(gear, scale=0.7), run_time=0.35 * run_time_scale)
            self.play(GrowArrow(arrow), FadeIn(score, shift=DOWN * 0.1), run_time=0.45 * run_time_scale)
            self.wait(0.15 * run_time_scale)
            self.play(
                score.animate.move_to(score_slot_pos(i)),
                FadeOut(arrow), FadeOut(gear),
                *[fold_bar["rects"][j].animate.set_color(NEUTRAL_COLOR) for j in range(5)],
                *[fold_bar["dots"][j].animate.set_color(NEUTRAL_COLOR) for j in range(5)],
                run_time=0.5 * run_time_scale,
            )
            return score

        scores = [None] * 5

        with self.voiceover(
            text=(
                "Cross validation is a generalization of the same idea. It relies "
                "on a user-chosen parameter, k, that determines the number of "
                "random subsets to create — one subset is often called a "
                "\"fold\". During a k-fold cross validation, we randomly partition "
                "the labeled dataset into k equal-sized subsets. In each round, we "
                "use k-1 folds to build the predictive model, and evaluate its "
                "performance on the remaining fold. This process is then repeated "
                "for k rounds."
            )
        ) as tracker:
            self.play(FadeOut(recap_group), run_time=1.0)
            self.wait(2.5)
            self.play(Write(pseudo_title), Create(code_box), FadeIn(line0), run_time=1.2)
            self.wait(6.5)
            self.play(FadeIn(fold_bar["group"], shift=UP * 0.15), FadeIn(line1), run_time=1.2)
            self.wait(4.5)
            self.play(FadeIn(line2), run_time=0.6)
            self.play(FadeIn(line3), run_time=0.6)
            self.play(FadeIn(line4), run_time=0.6)
            scores[0] = run_round(0)
            self.wait(3.0)
            self.play(FadeIn(line5), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        # -- Block 3: the concrete 5-fold example -------------------------
        with self.voiceover(
            text=(
                "For example, in a 5-fold cross validation, the labeled data is "
                "first partitioned into 5 subsets. In each round, 4 folds are "
                "used to build a decision tree, and the remaining fold is used "
                "to evaluate the performance of that tree."
            )
        ) as tracker:
            self.wait(0.8)
            scores[1] = run_round(1, run_time_scale=0.75)
            self.wait(1.8)
            scores[2] = run_round(2, run_time_scale=0.75)
            self.wait(2.2)
            scores[3] = run_round(3, run_time_scale=0.75)
            self.wait(1.5)
            scores[4] = run_round(4, run_time_scale=0.75)
            all_scores = VGroup(*scores)
            self.play(Circumscribe(VGroup(fold_bar["group"], all_scores), color=YELLOW), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(
            FadeOut(title), FadeOut(pseudocode), FadeOut(fold_bar["group"]), FadeOut(VGroup(*scores)),
        )

        # Stash for scene_03's reuse of the same 5-fold setup.
        self.scene02_fold_bar = fold_bar
        self.scene02_scores = scores


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_02()
