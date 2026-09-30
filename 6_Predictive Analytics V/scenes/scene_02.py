import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    CLASS_YES_COLOR,
    CLASS_NO_COLOR,
    NUMERIC_COLOR,
    HIGHLIGHT_COLOR,
    ERROR_COLOR,
    GOOD_COLOR,
    make_tree_node,
    make_tree_edge,
)


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: adapting k-NN and decision tree for numeric prediction
    # ------------------------------------------------------------------
    def scene_02(self):
        title = Text(
            "Adapting k-NN and Decision Tree for Numeric Prediction", font_size=26
        ).to_edge(UP, buff=0.3)

        # ---- Part A: classification vs. numeric prediction contrast ----
        class_title = Text("Classification", font_size=24, color=CLASS_YES_COLOR).move_to(
            LEFT * 3.4 + UP * 1.6
        )
        numeric_title = Text("Numeric Prediction", font_size=24, color=NUMERIC_COLOR).move_to(
            RIGHT * 3.4 + UP * 1.6
        )

        class_bins = VGroup()
        class_bin_labels = VGroup()
        class_dots = VGroup()
        for name, color, center in [
            ("Class A", CLASS_YES_COLOR, LEFT * 4.4 + DOWN * 0.5),
            ("Class B", CLASS_NO_COLOR, LEFT * 2.4 + DOWN * 0.5),
        ]:
            bin_box = Rectangle(width=1.6, height=1.0, color=color).move_to(center)
            class_bins.add(bin_box)
            class_bin_labels.add(Text(name, font_size=18, color=color).next_to(bin_box, DOWN, buff=0.15))
            dots = VGroup(*[Dot(color=color, radius=0.09) for _ in range(6)]).arrange_in_grid(
                rows=2, cols=3, buff=0.3
            )
            class_dots.add(dots.move_to(center))
        number_line = NumberLine(x_range=[0, 10, 2], length=5.0, color=GREY_B).move_to(
            RIGHT * 3.4 + DOWN * 0.6
        )
        num_values = [1.5, 3.2, 4.8, 6.0, 7.5, 8.8]
        num_dots = VGroup(*[Dot(number_line.n2p(v), color=NUMERIC_COLOR) for v in num_values])

        contrast_group = VGroup(
            class_title, numeric_title, class_bins, class_bin_labels, class_dots, number_line, num_dots
        )

        divider = Line(UP * 2.8, DOWN * 3.6, color=GREY_B)
        left_title = Text("k-NN for Numeric Prediction", font_size=22, color=HIGHLIGHT_COLOR).move_to(
            LEFT * 3.5 + UP * 2.7
        )
        right_title = Text(
            "Decision Tree for Numeric Prediction\n(aka Regression Tree)",
            font_size=20,
            color=HIGHLIGHT_COLOR,
            line_spacing=0.7,
        ).move_to(RIGHT * 3.5).align_to(left_title, UP)

        with self.voiceover(
            text=(
                "So far, we have been focusing on classification, which is the "
                "task of predicting categorical outcomes. Numeric prediction "
                "instead tries to predict numeric or continuous outcomes. However, "
                "that does not mean we need to invent everything from scratch. "
                "Some of the classification techniques, including k-nearest-neighbor "
                "and decision tree, can be naturally extended to serve the purpose "
                "of numeric prediction."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.2)
            self.wait(1.0)
            self.play(FadeIn(class_title, shift=UP * 0.2), run_time=1.2)
            self.wait(1.0)
            self.play(Create(class_bins), FadeIn(class_bin_labels), run_time=0.8)
            self.play(FadeIn(class_dots, lag_ratio=0.08), run_time=0.8)
            self.wait(1.0)
            self.play(FadeIn(numeric_title, shift=UP * 0.2), run_time=1.2)
            self.wait(1.0)
            self.play(Create(number_line), run_time=0.8)
            self.play(FadeIn(num_dots, lag_ratio=0.08), run_time=1.0)
            self.wait(2.0)
            self.play(FadeOut(contrast_group), run_time=0.8)
            self.play(Create(divider), run_time=0.8)
            self.play(Write(left_title), Write(right_title), run_time=1.2)
            self.wait(tracker.get_remaining_duration())    
        

        # ---- Part B: k-NN, left half ----
        focal = Star(color=WHITE, fill_opacity=1).scale(0.18).move_to(LEFT * 3.6 + UP * 0.4)
        # The 41 point sits outside the circle, so only the other three count (k = 3).
        neighbor_specs = [
            (LEFT * 0.9 + UP * 0.6, 32, NUMERIC_COLOR),
            (RIGHT * 1.4 + UP * 1.4, 41, GREY_B),
            (LEFT * 0.6 + DOWN * 0.9, 29, NUMERIC_COLOR),
            (RIGHT * 0.9 + DOWN * 0.6, 36, NUMERIC_COLOR),
        ]
        neighbors = VGroup()
        neighbor_labels = VGroup()
        for off, val, color in neighbor_specs:
            dot = Dot(focal.get_center() + off, color=color, radius=0.09)
            label = Text(str(val), font_size=16, color=color).next_to(dot, UP, buff=0.08)
            neighbors.add(dot)
            neighbor_labels.add(label)
        circle = Circle(radius=1.4, color=HIGHLIGHT_COLOR).move_to(focal.get_center())
        k_label = Text("k = 3", font_size=16, color=HIGHLIGHT_COLOR).next_to(circle, LEFT, buff=0.15)

        avg_text = Text("Average = (32 + 29 + 36) / 3 ≈ 32.3 is prediction", font_size=16)
        avg_box = SurroundingRectangle(avg_text, color=GOOD_COLOR, buff=0.15)
        avg_group = VGroup(avg_box, avg_text).move_to(LEFT * 3.6 + DOWN * 2.6)
        arrow_avg = Arrow(circle.get_bottom(), avg_group.get_top(), color=WHITE, buff=0.1, stroke_width=3)

        with self.voiceover(
            text=(
                "Using k-NN for numeric prediction is very straightforward. After "
                "finding the k nearest neighbors, instead of using the majority "
                "class as the prediction, we take the average of outcome values "
                "and use that as prediction."
            )
        ) as tracker:
            self.play(FadeIn(focal, scale=0.6), run_time=0.8)
            self.wait(2.4)
            self.play(FadeIn(neighbors, lag_ratio=0.15), FadeIn(neighbor_labels, lag_ratio=0.15), run_time=1.8)
            self.play(Create(circle), FadeIn(k_label), run_time=1.0)
            self.wait(5.2)
            self.play(GrowArrow(arrow_avg), FadeIn(avg_group), run_time=1.4)
            self.wait(tracker.get_remaining_duration())

        # ---- Part C: regression tree, right half ----
        root = make_tree_node("Split?", color=WHITE, font_size=16).move_to(RIGHT * 3.5 + UP * 1.2)
        leaf_left = make_tree_node("Leaf", color=WHITE, font_size=16, width=1.0).move_to(RIGHT * 2.3 + DOWN * 0.2)
        leaf_right = make_tree_node("Leaf", color=WHITE, font_size=16, width=1.0).move_to(RIGHT * 4.7 + DOWN * 0.2)
        edge_left = make_tree_edge(root, leaf_left, color=WHITE)
        edge_right = make_tree_edge(root, leaf_right, color=WHITE)

        leaf_dots = VGroup(*[Dot(color=NUMERIC_COLOR, radius=0.06) for _ in range(5)]).arrange(RIGHT, buff=0.18)
        leaf_dots.next_to(leaf_left, DOWN, buff=0.3)
        leaf_avg_label = Text("Avg", font_size=16, color=NUMERIC_COLOR).move_to(leaf_left[1])

        purity_label = Text("Splitting Criteria:", font_size=16).move_to(RIGHT * 3.5 + DOWN * 1.4)
        entropy_label = Text("Entropy (under classification)", font_size=16, color=ERROR_COLOR).next_to(purity_label, DOWN, buff=0.2)
        entropy_x = Cross(entropy_label, stroke_color=ERROR_COLOR, stroke_width=3)
        ssd_label = Text("Sum of Squared Deviations (SSD)", font_size=15, color=GOOD_COLOR).move_to(
            entropy_label.get_center()
        )

        mini_line = NumberLine(x_range=[-2, 2, 1], length=3.2, include_numbers=False, color=GREY_B).move_to(
            RIGHT * 3.5 + DOWN * 2.8
        )
        avg_tick = Line(UP * 0.15, DOWN * 0.15, color=HIGHLIGHT_COLOR).move_to(mini_line.n2p(0))
        compact_pts = [-0.3, -0.1, 0.1, 0.35]
        sparse_pts = [-1.7, -0.6, 0.5, 1.8]
        compact_dots = VGroup(*[Dot(mini_line.n2p(v), color=GOOD_COLOR, radius=0.06) for v in compact_pts])
        sparse_dots = VGroup(*[Dot(mini_line.n2p(v), color=ERROR_COLOR, radius=0.06) for v in sparse_pts])
        better_label = Text("lower SSD -> better split", font_size=14, color=GOOD_COLOR).next_to(
            mini_line, DOWN, buff=0.15
        )
        worse_label = Text("higher SSD -> worse split", font_size=14, color=ERROR_COLOR).next_to(
            mini_line, DOWN, buff=0.15
        )

        with self.voiceover(
            text=(
                "Similarly, decision tree can also be adapted for numeric "
                "prediction, and it is sometimes referred to as the regression "
                "tree. It follows the same recursive partitioning algorithm. "
                "There are only two key differences. First, at each leaf node, "
                "instead of using the majority class as prediction, we again rely "
                "on the average of the outcome variable as prediction. Second, the "
                "metric of data purity, which is needed to determine how to split "
                "the tree, is different. We cannot use entropy anymore, because "
                "entropy is only defined for categorical outcome variables. "
                "Instead, we rely on sum of squared deviations as a measure of "
                "purity. When deciding how to split the tree, we will look at the "
                "sum of squared deviations from the average outcome values in each "
                "resulting leaf node, and choose the split that gives the smallest "
                "sum of squared deviations. This is because, intuitively, smaller "
                "sum of squared deviations indicates that the outcome values are "
                "closer to their average, which means they are closer to each "
                "other, and therefore the data is more pure."
            )
        ) as tracker:
            # "...regression tree." -- build the tree skeleton
            self.play(FadeIn(root), run_time=1.0)
            self.play(Create(edge_left), Create(edge_right), FadeIn(leaf_left), FadeIn(leaf_right), run_time=1.5)
            self.wait(3.5)

            # "...recursive partitioning... two key differences." -- brief pause
            self.wait(6.5)

            # "First, at each leaf node... average... as prediction."
            self.play(FadeIn(leaf_dots, lag_ratio=0.15), run_time=1.5)
            self.play(leaf_dots.animate.move_to(leaf_left.get_center()).scale(0.3), run_time=1.2)
            self.play(FadeOut(leaf_dots), Transform(leaf_left[1], leaf_avg_label), run_time=0.6)
            self.wait(7.5)

            # "Second, the metric of data purity... is different."
            self.play(FadeIn(purity_label), FadeIn(entropy_label), run_time=1.0)
            self.wait(6.2)

            # "We cannot use entropy anymore..."
            self.play(Create(entropy_x), run_time=0.8)
            self.wait(4.8)

            # "Instead, we rely on sum of squared deviations..."
            self.play(FadeOut(entropy_label), FadeOut(entropy_x), FadeIn(ssd_label), run_time=1.0)
            self.wait(4.2)

            # "When deciding how to split... smallest sum of squared deviations."
            self.play(Create(mini_line), Create(avg_tick), run_time=1.2)
            self.play(FadeIn(compact_dots, lag_ratio=0.1), FadeIn(better_label), run_time=1.5)
            self.wait(8.0)

            # "...closer to their average... the data is more pure."
            self.play(
                Transform(compact_dots, sparse_dots),
                ReplacementTransform(better_label, worse_label),
                run_time=1.5,
            )
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(divider), FadeOut(left_title), FadeOut(right_title),
            FadeOut(focal), FadeOut(neighbors), FadeOut(neighbor_labels), FadeOut(circle), FadeOut(k_label),
            FadeOut(arrow_avg), FadeOut(avg_group),
            FadeOut(root), FadeOut(leaf_left), FadeOut(leaf_right), FadeOut(edge_left), FadeOut(edge_right),
            FadeOut(purity_label), FadeOut(ssd_label),
            FadeOut(mini_line), FadeOut(avg_tick),
            FadeOut(compact_dots), FadeOut(worse_label),
        )


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_02()
