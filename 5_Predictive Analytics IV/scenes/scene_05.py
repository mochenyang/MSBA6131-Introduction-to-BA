import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text

# Local to this scene only: the two hypothetical classes in the k-NN
# scatter (not reused elsewhere in this unit).
SCENE5_CLASS_A = ORANGE
SCENE5_CLASS_B = TEAL


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: why feature selection matters -- more features isn't
    # always better (k-NN distance distortion), and we've already seen
    # one feature selection approach in the decision tree.
    # ------------------------------------------------------------------
    @staticmethod
    def scene5_knn_visual():
        class_a_pts = [(-1.0, 0.8), (-0.5, 1.1), (-1.2, -0.5), (0.9, -0.9)]
        class_b_pts = [(1.1, -0.1), (-0.8, -1.0), (1.2, 0.9)]
        new_pt = (0.05, 0.4)
        a_dots = VGroup(*[Dot(RIGHT * x + UP * y, color=SCENE5_CLASS_A, radius=0.09) for x, y in class_a_pts])
        b_dots = VGroup(*[Dot(RIGHT * x + UP * y, color=SCENE5_CLASS_B, radius=0.09) for x, y in class_b_pts])
        new_dot = Dot(RIGHT * new_pt[0] + UP * new_pt[1], color=GREY_B, radius=0.1)
        neighbor_circle = Circle(radius=1.15, color=WHITE, stroke_width=2.2).move_to(new_dot.get_center())
        label = Text("k-Nearest Neighbors", font_size=18).next_to(
            VGroup(a_dots, b_dots, neighbor_circle), UP, buff=0.3
        )
        return VGroup(label, a_dots, b_dots, new_dot, neighbor_circle)

    @staticmethod
    def scene5_tree_visual():
        root = Text("X > t?", font_size=18)
        root_box = RoundedRectangle(width=root.width + 0.4, height=root.height + 0.35, corner_radius=0.1, color=WHITE)
        root_group = VGroup(root_box, root.move_to(root_box.get_center())).move_to(UP * 0.9)

        leaf_a_txt = Text("Class A", font_size=16, color=SCENE5_CLASS_A)
        leaf_a_box = RoundedRectangle(
            width=leaf_a_txt.width + 0.4, height=leaf_a_txt.height + 0.35, corner_radius=0.1, color=SCENE5_CLASS_A
        )
        leaf_a = VGroup(leaf_a_box, leaf_a_txt.move_to(leaf_a_box.get_center())).move_to(DOWN * 0.6 + LEFT * 1.3)

        leaf_b_txt = Text("Class B", font_size=16, color=SCENE5_CLASS_B)
        leaf_b_box = RoundedRectangle(
            width=leaf_b_txt.width + 0.4, height=leaf_b_txt.height + 0.35, corner_radius=0.1, color=SCENE5_CLASS_B
        )
        leaf_b = VGroup(leaf_b_box, leaf_b_txt.move_to(leaf_b_box.get_center())).move_to(DOWN * 0.6 + RIGHT * 1.3)

        edge_a = Line(root_group.get_bottom(), leaf_a.get_top(), color=GREY_B, stroke_width=2.2)
        edge_b = Line(root_group.get_bottom(), leaf_b.get_top(), color=GREY_B, stroke_width=2.2)
        label = Text("Decision Tree", font_size=18).next_to(root_group, UP, buff=0.3)
        return VGroup(label, root_group, leaf_a, leaf_b, edge_a, edge_b)

    def scene_05(self):
        title = Text("Feature Selection", font_size=40)
        subtitle = Text("Selecting the best features for predictive modeling", font_size=24, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.3)
        header = VGroup(title, subtitle)

        with self.voiceover(
            text=(
                "Another important topic in predictive analytics is feature "
                "selection. The goal of feature selection is to select only the "
                "best, most predictive features to use in building a predictive "
                "model. The first question worth asking is, why bother? Isn't "
                "more information always better?"
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.play(header.animate.scale(0.6).to_edge(UP, buff=0.35), run_time=0.8)

        knn = self.scene5_knn_visual().scale(0.8).move_to(LEFT * 3.4 + DOWN * 0.3)
        knn_caption = Text("distances are sensitive to irrelevant features", font_size=17, color=YELLOW)
        knn_caption.next_to(knn, DOWN, buff=0.3)

        with self.voiceover(
            text=(
                "Actually, more features isn't always better. Having irrelevant "
                "or low-quality features can hurt a predictive model's "
                "performance. Consider the k-nearest neighbor model as an "
                "example: if some features aren't useful for prediction, "
                "including them in the data can distort the distance "
                "calculations and cause the model to perform poorly."
            )
        ) as tracker:
            self.play(FadeIn(knn, shift=UP * 0.2), run_time=1.5)
            self.wait(3.0)
            self.play(Circumscribe(knn, color=YELLOW), run_time=1.3)
            self.play(FadeIn(knn_caption), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        tree = self.scene5_tree_visual().scale(0.8).move_to(RIGHT * 3.4 + DOWN * 0.3)
        tree_caption = Text("choosing splits by information gain is feature selection", font_size=17, color=YELLOW)
        tree_caption.next_to(tree, DOWN, buff=0.3)

        with self.voiceover(
            text=(
                "We've actually already seen one feature selection approach in "
                "action: the recursive partitioning algorithm behind decision "
                "trees automatically selects the best feature to split on at "
                "each step, based on the information gain metric."
            )
        ) as tracker:
            self.play(FadeIn(tree, shift=UP * 0.2), run_time=1.5)
            self.wait(2.0)
            self.play(FadeIn(tree_caption), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(
            FadeOut(header), FadeOut(knn), FadeOut(knn_caption), FadeOut(tree), FadeOut(tree_caption)
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_05()
