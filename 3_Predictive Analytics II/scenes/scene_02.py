import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    CLASS1_COLOR,
    CLASS0_COLOR,
    make_knn_visual,
    make_tree_visual,
    make_cutoff_number_line,
)


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: probability predictions from k-NN and the decision tree
    # ------------------------------------------------------------------
    @staticmethod
    def scene2_prob_bar(class1_count, class0_count, width=2.6, height=0.45):
        total = class1_count + class0_count
        p1 = class1_count / total
        bar1 = Rectangle(width=width * p1, height=height, color=CLASS1_COLOR, fill_opacity=0.85, stroke_width=1)
        bar0 = Rectangle(width=width * (1 - p1), height=height, color=CLASS0_COLOR, fill_opacity=0.85, stroke_width=1)
        bar = VGroup(bar1, bar0).arrange(RIGHT, buff=0)
        label1 = Text(f"{p1:.0%}", font_size=16).move_to(bar1.get_center())
        label0 = Text(f"{1 - p1:.0%}", font_size=16).move_to(bar0.get_center())
        return VGroup(bar, label1, label0), p1

    def scene_02(self):
        title = Text("Probability Predictions from k-NN and Decision Tree", font_size=30).to_edge(UP, buff=0.4)
        bullet1 = Text("A feature shared by most classification techniques:", font_size=24)
        bullet2 = Text("• Can predict class probabilities", font_size=24)
        bullet3 = Text("• Higher probability = more confidence", font_size=24)
        bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.3)

        with self.voiceover(
            text=(
                "From the last video, we've already learned two classification "
                "techniques, k-nearest-neighbors and the decision tree. Although "
                "they are very different models, they share an important "
                "characteristic: both k-NN, the decision tree, and in fact most "
                "other classification techniques can produce not just a class "
                "prediction, but also the probability of a data point belonging "
                "to a certain class. A higher predicted "
                "probability means the model is more confident in its prediction."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(7.8)
            self.play(FadeIn(bullet1, shift=UP * 0.15), run_time=1)
            self.wait(4.6)
            self.play(FadeIn(bullet2, shift=UP * 0.15), run_time=1)
            self.wait(7.2)
            self.play(FadeIn(bullet3, shift=UP * 0.15), run_time=1)
            self.wait(3.0)
            self.play(FadeOut(bullets), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        knn = make_knn_visual()
        tree = make_tree_visual()
        knn["group"].scale(0.85).move_to(LEFT * 3.5 + UP * 0.7)
        tree["group"].scale(0.85).move_to(RIGHT * 3.5 + UP * 0.7)

        knn_bar, knn_p1 = self.scene2_prob_bar(knn["class1_count"], knn["class0_count"])
        knn_bar.next_to(knn["group"], DOWN, buff=0.35)
        tree_bar, tree_p1 = self.scene2_prob_bar(tree["class1_count"], tree["class0_count"])
        tree_bar.next_to(tree["group"], DOWN, buff=0.35)

        with self.voiceover(
            text=(
                "For k-NN and the decision tree, obtaining a class probability "
                "is straightforward. In k-NN, the percentage of a given class "
                "among the k neighbors is the predicted probability of that "
                "class. In the decision tree, the percentage of a given class "
                "among the training data in the leaf node that the new data point "
                "falls into is the predicted probability."
            )
        ) as tracker:
            self.wait(4.0)
            self.play(FadeIn(knn["group"], shift=UP * 0.2), run_time=1.3)
            self.wait(2.7)
            self.play(Indicate(VGroup(knn["neighbor_dots"], knn["neighbor_circle"]), color=YELLOW), run_time=1.2)
            self.play(TransformFromCopy(knn["neighbor_dots"], knn_bar), run_time=1.0)
            self.wait(2.0)
            self.play(FadeIn(tree["group"], shift=UP * 0.2), run_time=1.3)
            self.wait(3.1)
            self.play(Indicate(tree["counts_label"], color=YELLOW), run_time=1.2)
            self.play(TransformFromCopy(tree["mixed_leaf"], tree_bar), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)

        num_line = make_cutoff_number_line(cutoff=0.5, width=8.5)
        num_line["group"].to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text=(
                "Discrete class predictions are actually generated from these "
                "probabilities using a cutoff value. Take binary classification "
                "as an example: the cutoff is usually 0.5 by default. If the "
                "probability of belonging to class 1 is greater than 0.5, the "
                "data point is predicted to be in class 1; otherwise, it's "
                "predicted to be in class 0. This is equivalent to a majority "
                "vote: the majority class is, by definition, the class with "
                "more than 50% proportion."
            )
        ) as tracker:
            self.play(FadeIn(num_line["group"]), run_time=1.3)
            slider = Dot(color=WHITE, radius=0.09).move_to(num_line["line"].n2p(0.2))
            self.play(FadeIn(slider), run_time=0.6)
            self.wait(0.5)
            slider_label = Text("Class 0", font_size=18, color=CLASS0_COLOR).next_to(slider, UP, buff=0.2)
            self.play(FadeIn(slider_label), run_time=0.6)
            self.wait(11.66)
            new_label = Text("Class 1", font_size=18, color=CLASS1_COLOR).next_to(
                num_line["line"].n2p(0.8), UP, buff=0.2
            )
            self.play(
                slider.animate.move_to(num_line["line"].n2p(0.8)),
                Transform(slider_label, new_label),
                run_time=1.5,
            )
            majority_label = Text("Majority Vote", font_size=18, color=GREY_B).next_to(
                VGroup(num_line["class1_label"], num_line["class0_label"]), DOWN, buff=0.1
            )
            self.wait(5.45)
            self.play(FadeIn(majority_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(knn["group"]), FadeOut(tree["group"]), FadeOut(knn_bar), FadeOut(tree_bar),
            FadeOut(slider), FadeOut(slider_label), FadeOut(majority_label), FadeOut(num_line["group"]),
        )

        # Stash for scene_03 (shrunk icons, taken via .copy() there so fading
        # the originals out above doesn't affect scene_03's reuse) and
        # scene_08 (cutoff line reuse).
        self.scene02_knn_group = knn["group"]
        self.scene02_tree_group = tree["group"]
        self.scene02_number_line = num_line


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_02()
