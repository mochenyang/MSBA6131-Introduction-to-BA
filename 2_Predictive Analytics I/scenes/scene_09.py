import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_tree_node, make_tree_edge

# Axes convention for this scene: X2 is the horizontal axis, X1 the
# vertical axis -- matching the plan's "horizontal line at X1 = alpha" /
# "vertical line at X2 = beta" wording exactly.
SCENE9_YELLOW_PTS = [
    (2, 8), (4, 7.5), (6, 9), (8, 7), (3, 9.5),  # upper region (X1 > alpha)
    (7, 3), (8, 2), (9, 4), (6.5, 1),  # lower-right (X1 <= alpha, X2 > beta)
    (1, 4),  # lower-left outlier
]
SCENE9_PURPLE_PTS = [
    (7, 6.5),  # upper outlier
    (1, 2), (2, 4), (1.5, 1), (3, 3.5),  # lower-left (X1 <= alpha, X2 <= beta)
    (8, 4.5),  # lower-right outlier
]
SCENE9_ALPHA = 6
SCENE9_BETA = 5


class Scene09Mixin:
    # ------------------------------------------------------------------
    # Scene 9: recursive-partitioning intuition
    # ------------------------------------------------------------------
    def scene_09(self):
        title = Text("Building Decision Tree: Intuition", font_size=30).to_edge(UP, buff=0.4)
        subtitle = Text(
            "Intuition: iteratively slicing the data so each sub-region ends up mostly one class",
            font_size=20,
            color=YELLOW,
        ).next_to(title, DOWN, buff=0.25)

        with self.voiceover(
            text=(
                "So how do we actually build a decision tree? Since a tree is "
                "just a collection of decision rules, the real question is how to "
                "construct useful rules. The intuition is: a decision rule \"slices\" "
                "your data into sub-regions based on attribute values, and a good "
                "rule slices the data so each sub-region is mostly one class. Why? "
                "Because if a region is mostly one class, any new, unlabeled "
                "point that lands there can be confidently classified into that "
                "class."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(8.0)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.8)  # "The intuition: a decision rule slices..."
            self.wait(tracker.get_remaining_duration())

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5.6,
            y_length=5.2,
            axis_config={"include_ticks": False},
        ).move_to(LEFT * 3.4 + DOWN * 0.7)
        x_label = axes.get_x_axis_label(Text("X2", font_size=20), edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label(Text("X1", font_size=20), edge=UP, direction=UP)
        yellow_dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=YELLOW, radius=0.08) for x, y in SCENE9_YELLOW_PTS])
        purple_dots = VGroup(*[Dot(axes.coords_to_point(x, y), color=PURPLE, radius=0.08) for x, y in SCENE9_PURPLE_PTS])

        root = make_tree_node("X1 > α?", color=WHITE, font_size=18).move_to(RIGHT * 3.0 + UP * 1.8)

        with self.voiceover(
            text=(
                "Here's an example: suppose we are trying to build a decision "
                "tree to predict whether a data point belongs to the \"yellow\" "
                "class or the \"purple\" class, based on values of two attributes "
                "X1 and X2."
            )
        ) as tracker:
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
            self.play(FadeIn(yellow_dots, lag_ratio=0.05), FadeIn(purple_dots, lag_ratio=0.05), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        h_line = DashedLine(
            axes.coords_to_point(0, SCENE9_ALPHA), axes.coords_to_point(10, SCENE9_ALPHA), color=WHITE
        )
        alpha_label = Text("X1 = α", font_size=18, color=WHITE).next_to(h_line, RIGHT, buff=0.15)

        v_line = DashedLine(
            axes.coords_to_point(SCENE9_BETA, 0), axes.coords_to_point(SCENE9_BETA, SCENE9_ALPHA), color=WHITE
        )
        beta_label = Text("X2 = β", font_size=18, color=WHITE).next_to(v_line, DOWN, buff=0.08)

        yellow_leaf1 = make_tree_node("Yellow", color=YELLOW, font_size=18).move_to(RIGHT * 1.3 + UP * 0.0)
        x2_node = make_tree_node("X2 > β?", color=WHITE, font_size=18).move_to(RIGHT * 4.6 + UP * 0.0)
        yellow_leaf2 = make_tree_node("Yellow", color=YELLOW, font_size=18).move_to(RIGHT * 3.6 + DOWN * 1.8)
        purple_leaf = make_tree_node("Purple", color=PURPLE, font_size=18).move_to(RIGHT * 5.6 + DOWN * 1.8)

        e_root_yellow = make_tree_edge(root, yellow_leaf1, "Yes")
        e_root_x2 = make_tree_edge(root, x2_node, "No")
        e_x2_yellow = make_tree_edge(x2_node, yellow_leaf2, "Yes")
        e_x2_purple = make_tree_edge(x2_node, purple_leaf, "No")        

        with self.voiceover(
            text=(
                "The idea is to find values of X1 and X2 such that, slicing the "
                "space based on them would create sub-regions that mostly "
                "consist of one class. And a collection of such slices uniquely "
                "corresponds to a decision tree."
            )
        ) as tracker:
            self.play(Create(h_line), FadeIn(alpha_label), run_time=1.5)
            self.play(FadeIn(root), Create(e_root_yellow), FadeIn(yellow_leaf1), run_time=1.5)
            self.play(Create(v_line), FadeIn(beta_label), run_time=1)
            self.play(
                Create(e_root_x2), FadeIn(x2_node),
                Create(e_x2_yellow), FadeIn(yellow_leaf2), 
                Create(e_x2_purple), FadeIn(purple_leaf),
                run_time=3,
            )
            self.wait(tracker.get_remaining_duration())

        # A single horizontal row along the very bottom -- below both the
        # plot (axes bottom ~ y=-3.3) and the tree (lowest leaves ~ y=-2.3),
        # so it can't collide with either regardless of where they sit.
        # "Two Questions:" on its own line, the two sub-questions side by
        # side on the line below -- placed bottom-right, under the tree.
        questions_title = Text("Two Questions:", font_size=18, color=YELLOW)
        q1 = Text("1. Where to split?", font_size=16)
        q2 = Text("2. When to stop?", font_size=16)
        questions_row = VGroup(q1, q2).arrange(RIGHT, buff=0.5)
        VGroup(questions_title, questions_row).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.3 + DOWN * 3.3)

        with self.voiceover(
            text=(
                "This example also raises two questions. First, how exactly do "
                "we pick the attribute and the split point?"
            )
        ) as tracker:
            self.play(Write(questions_title), run_time=1)
            self.play(FadeIn(q1, shift=UP * 0.2), run_time=1)
            self.play(Indicate(alpha_label, color=YELLOW), Indicate(beta_label, color=YELLOW), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # Each extra line must actually isolate a single off-class point into
        # its own pure sliver -- not just decorate the plot:
        #  - upper region (X1 > alpha) has one purple outlier at X1=6.5 among
        #    yellows at X1 in [7, 9.5]; a horizontal cut at X1=6.8 splits it off.
        #  - lower-right region (X1 <= alpha, X2 > beta) has one purple outlier
        #    at X1=4.5 among yellows at X1 in [1, 4]; a horizontal cut at
        #    X1=4.2 splits it off. Both extra cuts are X1-based (horizontal),
        #    confined to the X2 in [5, 10] sub-region where each outlier sits.
        extra_lines = VGroup(
            DashedLine(axes.coords_to_point(0, 6.8), axes.coords_to_point(10, 6.8), color=GREY_B, stroke_width=1.5),
            DashedLine(axes.coords_to_point(0, 3.8), axes.coords_to_point(5, 3.8), color=GREY_B, stroke_width=1.5),
            DashedLine(axes.coords_to_point(1.3, 3.8), axes.coords_to_point(1.3, 6), color=GREY_B, stroke_width=1.5),
            DashedLine(axes.coords_to_point(5, 4.2), axes.coords_to_point(10, 4.2), color=GREY_B, stroke_width=1.5),
        )
        overfit_label = Text("Overfit!", font_size=26, color=RED).next_to(axes, RIGHT, buff=0.3).shift(UP * 1.5)

        with self.voiceover(
            text=(
                "Second, when do we stop splitting? In theory, given a finite "
                "dataset, you could keep slicing until every sub-region contains "
                "just a single data point. Left unchecked, a decision tree can "
                "fit its training data perfectly. But as we saw earlier with "
                "overfitting, that's a bad thing. So the rest of this discussion "
                "answers two questions: where to split, and when to stop."
            )
        ) as tracker:
            self.play(FadeIn(q2, shift=UP * 0.2), run_time=1)
            self.play(Create(extra_lines, lag_ratio=0.15), run_time=5)
            self.play(FadeIn(overfit_label, shift=LEFT * 0.2), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(yellow_dots), FadeOut(purple_dots), FadeOut(h_line), FadeOut(alpha_label), 
            FadeOut(v_line), FadeOut(beta_label), FadeOut(root), FadeOut(yellow_leaf1), FadeOut(x2_node),
            FadeOut(purple_leaf), FadeOut(yellow_leaf2), FadeOut(e_root_yellow), FadeOut(e_root_x2),
            FadeOut(e_x2_purple), FadeOut(e_x2_yellow), FadeOut(questions_title), FadeOut(q1), FadeOut(q2),
            FadeOut(extra_lines), FadeOut(overfit_label),
        )


class Scene09(VoiceoverScene, Scene09Mixin):
    """Standalone preview: manim -pql scene_09.py Scene09"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_09()
