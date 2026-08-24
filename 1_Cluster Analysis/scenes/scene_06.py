import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service


class Scene06Mixin:
    # ------------------------------------------------------------------
    # Scene 6: Distance metrics
    # ------------------------------------------------------------------
    @staticmethod
    def add_bullet(bullet_list, text, color=WHITE):
        dot = Text("•", font_size=26, color=color)
        label = Text(text, font_size=24, color=color)
        item = VGroup(dot, label).arrange(RIGHT, buff=0.15)
        item.to_edge(LEFT, buff=0.5)
        if len(bullet_list) > 0:
            item.next_to(bullet_list[-1], DOWN, aligned_edge=LEFT, buff=0.3)
        else:
            item.set_y(bullet_list.reference_y)
        bullet_list.add(item)
        return item

    def scene_06(self):
        # Each of the 5 metrics gets its own dedicated color, distinct from
        # the Walmart entity colors (RED/BLUE/GREEN) used elsewhere in the
        # video and distinct from each other -- Manhattan and Matching used
        # to both be ORANGE, Max-Coordinate and Jaccard both TEAL, which
        # falsely implied a relationship between unrelated metrics.
        EUCLIDEAN_COLOR = PURPLE
        MANHATTAN_COLOR = ORANGE
        MAXCOORD_COLOR = TEAL
        MATCHING_COLOR = PINK
        JACCARD_COLOR = GOLD

        title = Text("Distance Metrics", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            text=(
                "Defining proper distance metrics is often the first step of running any clustering algorithm. "
                "There are a number of distance metrics available, "
                )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(tracker.get_remaining_duration())

        subtitle1 = Text("Depends on your data type", font_size=24, color=GRAY)
        subtitle2 = Text("& your application", font_size=24, color=GRAY)
        subtitle = VGroup(subtitle1, subtitle2).arrange(RIGHT, buff=0.2).next_to(title, DOWN, buff=0.3)
        with self.voiceover(
            text=(
                "and picking the appropriate one depends jointly on the type of your data and on "
                "the particular application."
            )
        ) as tracker:
            self.play(FadeIn(subtitle1, shift=UP * 0.2), run_time=1.5)
            self.play(FadeIn(subtitle2, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        divider = Line(UP * 2.9, DOWN * 3.2, color=GRAY).shift(LEFT * 1.5)

        plane = NumberPlane(
            x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=4.2, y_length=3.2,
            background_line_style={"stroke_opacity": 0.4},
        ).move_to(RIGHT * 2.6 + UP * 0.7)
        point_a = plane.coords_to_point(1, 1)
        point_b = plane.coords_to_point(4, 3)
        dot_a = Dot(point_a, color=YELLOW)
        dot_b = Dot(point_b, color=YELLOW)
        label_a = Text("A", font_size=26, color=YELLOW).next_to(dot_a, DOWN, buff=0.15)
        label_b = Text("B", font_size=26, color=YELLOW).next_to(dot_b, UP, buff=0.15)

        with self.voiceover(
            text=(
                "Let's consider the problem of measuring the distance between two "
                "data points, A and B, each characterized by a vector of k "
                "attributes, or features."
            )
        ) as tracker:
            self.play(FadeOut(subtitle), Create(divider), run_time=1)
            self.play(Create(plane), run_time=1.5)
            self.play(FadeIn(dot_a), FadeIn(dot_b), Write(label_a), Write(label_b), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        bullets = VGroup()
        with self.voiceover(text="If your data is numeric or continuous, there are a few choices of distance metrics.") as tracker:
            numeric_header = Text("Numeric /\nContinuous Data", font_size=24, color=YELLOW, line_spacing=1.1)
            numeric_header.to_edge(LEFT, buff=0.5).set_y(1.9)
            self.play(Write(numeric_header), run_time=1.5)
            self.wait(tracker.get_remaining_duration())
        bullets.reference_y = numeric_header.get_bottom()[1] - 0.45

        formula_pos = RIGHT * 2.6 + DOWN * 2.7

        with self.voiceover(
            text=(
                "First, Euclidean distance simply measures the straight-line "
                "distance between A and B -- it's perhaps the most common choice."
            )
        ) as tracker:
            self.add_bullet(bullets, "Euclidean Distance", color=EUCLIDEAN_COLOR)
            self.play(FadeIn(bullets[-1]), run_time=1)
            euclid_line = Line(point_a, point_b, color=EUCLIDEAN_COLOR, stroke_width=4)
            euclid_formula = MathTex(
                r"d(A,B)=\sqrt{\sum_{i=1}^{k}(a_i-b_i)^2}", font_size=32, color=EUCLIDEAN_COLOR
            ).move_to(formula_pos)
            self.play(Create(euclid_line), run_time=1.5)
            self.play(Write(euclid_formula), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="Second, Manhattan distance is calculated as the sum of absolute differences across all features."
        ) as tracker:
            self.add_bullet(bullets, "Manhattan Distance", color=MANHATTAN_COLOR)
            self.play(FadeIn(bullets[-1]), run_time=1)
            manhattan_formula = MathTex(
                r"d(A,B)=\sum_{i=1}^{k}|a_i-b_i|", font_size=32, color=MANHATTAN_COLOR
            ).move_to(formula_pos)
            self.play(FadeOut(euclid_line), FadeTransform(euclid_formula, manhattan_formula), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        corner = np.array([point_b[0], point_a[1], 0])
        manhattan_path = VGroup(
            Line(point_a, corner, color=MANHATTAN_COLOR, stroke_width=4),
            Line(corner, point_b, color=MANHATTAN_COLOR, stroke_width=4),
        )
        with self.voiceover(
            text=(
                "To understand this metric, imagine A and B are placed on a grid, "
                "and you want to travel from A to B: you can only move along the "
                "grid, horizontally or vertically, but not diagonally."
            )
        ) as tracker:
            # "not diagonally" -- concretely show the forbidden shortcut first,
            # crossed out, before revealing the actual grid-only path.
            forbidden = Line(point_a, point_b, color=RED, stroke_width=3)
            # Anchored to the whole plane, not the line itself -- the line's
            # upper endpoint sits exactly at B, so next_to(forbidden, UP)
            # collides with B's own label.
            forbidden_label = Text("No diagonal shortcuts!", font_size=22, color=RED).next_to(
                plane, UP, buff=0.15
            )
            forbidden_cross = Cross(stroke_color=RED, scale_factor=0.25).move_to(forbidden.get_center())
            self.play(Create(forbidden), Write(forbidden_label), run_time=1.3)
            self.play(Create(forbidden_cross), run_time=0.8)
            self.play(FadeOut(forbidden), FadeOut(forbidden_cross), FadeOut(forbidden_label), run_time=0.6)

            # Literally travel the grid-only path -- directly visualizes
            # "you want to travel from A to B... horizontally or vertically."
            traveler = Dot(point_a, color=MANHATTAN_COLOR, radius=0.1)
            self.play(FadeIn(traveler), run_time=0.5)
            self.play(Create(manhattan_path[0]), MoveAlongPath(traveler, Line(point_a, corner)), run_time=1.8)
            self.play(Create(manhattan_path[1]), MoveAlongPath(traveler, Line(corner, point_b)), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="The distance you'd need to travel is the Manhattan distance.") as tracker:
            self.play(FadeOut(traveler), run_time=0.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "The third metric, max-coordinate distance, is the largest "
                "difference among all features. Compared to Euclidean and "
                "Manhattan distance, it's used less often."
            )
        ) as tracker:
            self.add_bullet(bullets, "Max-Coordinate Distance", color=MAXCOORD_COLOR)
            self.play(FadeIn(bullets[-1]), run_time=1)
            max_formula = MathTex(
                r"d(A,B)=\max_i |a_i-b_i|", font_size=32, color=MAXCOORD_COLOR
            ).move_to(formula_pos)
            self.play(FadeOut(manhattan_path), FadeTransform(manhattan_formula, max_formula), run_time=1)
            highlight_seg = Line(point_a, corner, color=MAXCOORD_COLOR, stroke_width=6)
            self.play(Create(highlight_seg), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        numeric_group = VGroup(
            plane, dot_a, dot_b, label_a, label_b, numeric_header, bullets, max_formula, highlight_seg
        )
        with self.voiceover(
            text=(
                "If the data is categorical, and in particular if all attributes "
                "are binary, you can consider using matching distance or Jaccard "
                "distance."
            )
        ) as tracker:
            self.play(FadeOut(numeric_group), run_time=1.5)
            binary_header = Text("Binary /\nCategorical Data", font_size=24, color=YELLOW, line_spacing=1.1)
            binary_header.to_edge(LEFT, buff=0.5).set_y(1.9)
            self.play(Write(binary_header), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        attrs_a = [1, 0, 1, 1, 0, 0]
        attrs_b = [1, 1, 1, 0, 0, 0]

        def make_vector_row(values, label_text, y):
            row = VGroup()
            boxes = VGroup()
            for v in values:
                sq = Square(side_length=0.6, color=WHITE).set_fill(BLACK, opacity=1)
                num = Text(str(v), font_size=26).move_to(sq)
                boxes.add(VGroup(sq, num))
            boxes.arrange(RIGHT, buff=0.15)
            row_label = Text(label_text, font_size=26, color=YELLOW)
            row.add(row_label, boxes)
            row.arrange(RIGHT, buff=0.4)
            row.move_to(RIGHT * 2.6 + UP * y)
            return row, boxes

        row_a, boxes_a = make_vector_row(attrs_a, "A =", 1.4)
        row_b, boxes_b = make_vector_row(attrs_b, "B =", 0.5)

        bullets2 = VGroup()
        bullets2.reference_y = binary_header.get_bottom()[1] - 0.45

        with self.voiceover(
            text=(
                "Under matching distance, the distance between A and B is simply "
                "the fraction of attributes on which A and B have different values"
            )
        ) as tracker:
            self.add_bullet(bullets2, "Matching Distance", color=MATCHING_COLOR)
            self.play(FadeIn(bullets2[-1]), run_time=1)
            self.play(FadeIn(row_a), FadeIn(row_b), run_time=1.5)
            mismatch_boxes = VGroup(*[boxes_a[i] for i in range(6) if attrs_a[i] != attrs_b[i]])
            mismatch_boxes.add(*[boxes_b[i] for i in range(6) if attrs_a[i] != attrs_b[i]])
            self.play(*[sq[0].animate.set_color(RED) for sq in mismatch_boxes], run_time=1.5)
            self.play(Indicate(mismatch_boxes), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "the number of attributes on which A and B mismatch, divided by "
                "the total number of attributes."
            )
        ) as tracker:
            matching_formula = MathTex(
                r"d_{match}(A,B)=\frac{2}{6}=0.33", font_size=32, color=MATCHING_COLOR
            ).move_to(RIGHT * 2.6 + DOWN * 0.5)
            self.play(Write(matching_formula), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Jaccard distance is almost the same as matching distance, except "
                "for a small difference in the denominator:"
            )
        ) as tracker:
            self.add_bullet(bullets2, "Jaccard Distance", color=JACCARD_COLOR)
            self.play(FadeIn(bullets2[-1]), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "instead of counting all attributes, Jaccard distance excludes "
                "the attributes where both A and B take the value 0."
            )
        ) as tracker:
            zero_zero_boxes = VGroup(
                *[boxes_a[i] for i in range(6) if attrs_a[i] == 0 and attrs_b[i] == 0],
                *[boxes_b[i] for i in range(6) if attrs_a[i] == 0 and attrs_b[i] == 0],
            )
            self.play(
                *[sq[0].animate.set_stroke(opacity=0.25).set_fill(GRAY, opacity=0.5) for sq in zero_zero_boxes],
                run_time=1.5,
            )
            jaccard_formula = MathTex(
                r"d_{jaccard}(A,B)=\frac{2}{6-2}=0.5", font_size=32, color=JACCARD_COLOR
            ).move_to(RIGHT * 2.6 + DOWN * 1.3)
            self.play(Write(jaccard_formula), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        contrast_row = VGroup()
        with self.voiceover(
            text=(
                "The reason to do so is that, in many real-world scenarios, a 0-0 "
                "match is less informative than a 1-1 match about two data "
                "points' similarity."
            )
        ) as tracker:
            # Ground the claim concretely: contrast one already-dimmed 0-0 pair
            # against a highlighted 1-1 pair, right where it's narrated.
            one_one_boxes = VGroup(boxes_a[0], boxes_b[0])
            less_label = Text("0-0: less informative", font_size=20, color=GRAY)
            more_label = Text("1-1: more informative", font_size=20, color=JACCARD_COLOR)
            contrast_row.add(more_label, less_label)
            contrast_row.arrange(RIGHT, buff=0.6).next_to(row_a, UP, buff=0.3)
            self.play(Indicate(zero_zero_boxes, scale_factor=1.1), run_time=1.2)
            self.play(FadeIn(less_label), run_time=1)
            self.play(Indicate(one_one_boxes, color=JACCARD_COLOR, scale_factor=1.2), run_time=1.2)
            self.play(FadeIn(more_label), run_time=1)
            self.wait(tracker.get_remaining_duration())

        rng = np.random.default_rng(3)
        long_x = rng.integers(0, 2, 14)
        long_x[:2] = 1
        long_x[2:] = 0
        rng.shuffle(long_x)
        long_y = long_x.copy()
        flip_idx = rng.choice(np.where(long_x == 0)[0], size=1, replace=False)
        long_y[flip_idx] = 1

        def make_long_row(values, label_text, y):
            boxes = VGroup()
            for v in values:
                sq = Square(side_length=0.38, color=WHITE).set_fill(
                    GREEN if v == 1 else BLACK, opacity=1 if v == 1 else 1
                )
                boxes.add(sq)
            boxes.arrange(RIGHT, buff=0.08)
            lab = Text(label_text, font_size=24, color=YELLOW).next_to(boxes, LEFT, buff=0.3)
            return VGroup(lab, boxes).move_to(RIGHT * 2.6 + UP * y), boxes

        with self.voiceover(
            text=(
                "Think about a typical supermarket shopping scenario. A typical "
                "supermarket sells thousands of products,"
            )
        ) as tracker:
            self.play(
                FadeOut(row_a), FadeOut(row_b), FadeOut(matching_formula), FadeOut(jaccard_formula),
                FadeOut(contrast_row),
                run_time=1.3,
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "and each customer usually only buys a handful of them, so each "
                "customer's shopping-history vector will have a lot of 0s and "
                "relatively few 1s."
            )
        ) as tracker:
            long_row_x, long_boxes_x = make_long_row(long_x, "Cust X:", 1.1)
            long_row_y, long_boxes_y = make_long_row(long_y, "Cust Y:", 0.3)
            self.play(FadeIn(long_row_x), run_time=2.5)
            self.play(FadeIn(long_row_y), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Under matching distance, any two arbitrary customers would seem "
                "very similar to each other, simply because there are thousands of "
                "products neither of them purchased."
            )
        ) as tracker:
            zero_pairs = VGroup(
                *[long_boxes_x[i] for i in range(14) if long_x[i] == 0 and long_y[i] == 0],
                *[long_boxes_y[i] for i in range(14) if long_x[i] == 0 and long_y[i] == 0],
            )
            self.play(Indicate(zero_pairs, color=RED, scale_factor=1.15), run_time=2)
            note = Text("Matching distance ≈ 0 → looks \"similar\"", font_size=24, color=RED).next_to(
                long_row_y, DOWN, buff=0.5
            )
            self.play(FadeIn(note), run_time=1.5)
            self.play(Indicate(note), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "But in a supermarket context, it's really the handful of things "
                "people do buy that characterizes who they are -- not the "
                "thousands of things they don't buy."
            )
        ) as tracker:
            one_boxes = VGroup(
                *[long_boxes_x[i] for i in range(14) if long_x[i] == 1],
                *[long_boxes_y[i] for i in range(14) if long_y[i] == 1],
            )
            self.play(FadeOut(note), run_time=1)
            self.play(Wiggle(one_boxes), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Jaccard distance solves this asymmetry by ignoring 0-0 matches.") as tracker:
            note2 = Text("Jaccard ignores 0-0 → focuses on the 1s", font_size=24, color=JACCARD_COLOR).next_to(
                long_row_y, DOWN, buff=0.5
            )
            self.play(FadeIn(note2), run_time=1.5)
            self.play(Indicate(note2), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(divider), FadeOut(binary_header), FadeOut(bullets2),
            FadeOut(long_row_x), FadeOut(long_row_y), FadeOut(note2),
        )


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_06()
