import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, make_knn_visual, make_tree_visual


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: classification as a probability-prediction problem
    # ------------------------------------------------------------------
    def scene_03(self):
        title = Text("Classification as a Probability Prediction", font_size=28).to_edge(UP, buff=0.4)
        notation = VGroup(
            Text("Data point ", font_size=22, color=GREY_B),
            MathTex("X = (x_1, \\dots, x_n)", font_size=34, color=GREY_B),
            Text(";  Classes ", font_size=22, color=GREY_B),
            MathTex("(C_1, \\dots, C_m)", font_size=34, color=GREY_B),
        ).arrange(RIGHT, buff=0.15).next_to(title, DOWN, buff=0.3)

        with self.voiceover(
            text=(
                "More generally, a classification task can be thought of as "
                "predicting class probabilities, and then picking the class "
                "with the highest probability as the prediction. Suppose each "
                "data point X is represented by a vector of features, and "
                "there are m possible classes, C1 through Cm."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(6.0)
            self.play(FadeIn(notation, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        box_line1 = VGroup(
            Text("Classification = estimate ", font_size=22),
            MathTex("P(C_i \\mid X)", font_size=34),
            Text(" for each class", font_size=22),
        ).arrange(RIGHT, buff=0.1)
        box_line2 = Text("→ predict the class with highest probability", font_size=22)
        box_text = VGroup(box_line1, box_line2).arrange(DOWN, buff=0.2).move_to(UP * 1.05)
        box = SurroundingRectangle(box_text, color=WHITE, buff=0.2, corner_radius=0.15)
        
        knn_icon = self.scene02_knn_group.copy().scale(0.7).move_to(LEFT * 3 + DOWN * 1.7)
        tree_icon = self.scene02_tree_group.copy().scale(0.7).move_to(DOWN * 1.7)
        arrow_knn = Arrow(knn_icon.get_top(), box.get_bottom(), color=WHITE, buff=0.15, tip_length=0.15, stroke_width=6, max_stroke_width_to_length_ratio=10)
        arrow_tree = Arrow(tree_icon.get_top(), box.get_bottom(), color=WHITE, buff=0.15, tip_length=0.15, stroke_width=6, max_stroke_width_to_length_ratio=10)
        proportions_label = Text("estimated via simple proportions", font_size=16, color=GREY_B).next_to(
            VGroup(knn_icon, tree_icon), DOWN, buff=0.35
        )
        
        with self.voiceover(
            text=(
                "Our goal is to estimate the conditional probability of class "
                "Ci given the features X — in other words, given X, what's the "
                "probability that it belongs to class Ci? Both k-NN and "
                "decision tree estimate this conditional probability using "
                "simple proportions, and then predict whichever class has the "
                "highest estimated probability."
            )
        ) as tracker:
            self.play(Create(box), Write(box_text), run_time=3)
            self.wait(10.0)
            self.play(
                FadeIn(knn_icon, shift=DOWN * 0.2), FadeIn(tree_icon, shift=DOWN * 0.2),
                run_time=1.3,
            )
            self.play(GrowArrow(arrow_knn), GrowArrow(arrow_tree), run_time=1.2)
            self.play(FadeIn(proportions_label), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        nb_question = Text("?", font_size=32, color=YELLOW)
        nb_icon = VGroup(
            Text("Naive Bayes", font_size=18, color=YELLOW),
            nb_question,
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 3 + DOWN * 1.7)
        arrow_nb = Arrow(nb_icon.get_top(), box.get_bottom(), color=YELLOW, buff=0.15, tip_length=0.15, stroke_width=6, max_stroke_width_to_length_ratio=10)
        bayes_text = Text("Bayes' Theorem", font_size=26, color=YELLOW).move_to(nb_question.get_center())

        with self.voiceover(
            text=(
                "Naive Bayes follows the same logic in making predictions — "
                "pick the class with the highest probability — except that it "
                "uses Bayes' theorem to estimate those class probabilities."
            )
        ) as tracker:
            self.play(FadeIn(nb_icon, shift=UP * 0.2), run_time=1.3)
            self.play(GrowArrow(arrow_nb), run_time=1.0)
            self.wait(3.0)            
            self.play(Transform(nb_question, bayes_text), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(notation), FadeOut(box), FadeOut(box_text),
            FadeOut(knn_icon), FadeOut(tree_icon), FadeOut(arrow_knn), FadeOut(arrow_tree),
            FadeOut(proportions_label), FadeOut(nb_icon), FadeOut(nb_question), FadeOut(arrow_nb),
        )


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_02()
        self.scene_03()

    def _fixture_scene_02(self):
        # Stand-in for scene_02's ending state (k-NN and decision-tree
        # visuals, faded out) so scene_03 can be previewed alone.
        self.scene02_knn_group = make_knn_visual()["group"]
        self.scene02_tree_group = make_tree_visual()["group"]
