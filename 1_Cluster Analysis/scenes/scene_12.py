import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import encircle, make_mini_dendrogram, make_mini_kmeans_scatter

# Generic two-cluster illustration reused by both boxes in this scene only.
CLUSTER_P_COLOR = BLUE
CLUSTER_Q_COLOR = ORANGE
_RNG = np.random.default_rng(5)
CLUSTER_P_PTS = [np.array([-0.7 + _RNG.normal(0, 0.35), 0.3 + _RNG.normal(0, 0.35), 0]) for _ in range(4)]
CLUSTER_Q_PTS = [np.array([0.7 + _RNG.normal(0, 0.35), -0.2 + _RNG.normal(0, 0.35), 0]) for _ in range(4)]


class Scene12Mixin:
    # ------------------------------------------------------------------
    # Scene 12: Cohesion and separation (how many clusters?)
    # ------------------------------------------------------------------
    @staticmethod
    def build_box_clusters(box_center, scale=1.0):
        dots_p = VGroup(
            *[Dot(box_center + p * scale, radius=0.07, color=CLUSTER_P_COLOR) for p in CLUSTER_P_PTS]
        )
        dots_q = VGroup(
            *[Dot(box_center + p * scale, radius=0.07, color=CLUSTER_Q_COLOR) for p in CLUSTER_Q_PTS]
        )
        return dots_p, dots_q

    @staticmethod
    def inward_arrows(dots_group, color, n=2):
        """A couple of short arrows from edge points toward the group's own
        center -- cohesion: points pulling toward their own cluster."""
        center = dots_group.get_center()
        arrows = VGroup()
        for dot in list(dots_group)[:n]:
            p = dot.get_center()
            start = p + (center - p) * 0.15
            end = center + (p - center) * 0.15
            arrows.add(
                Arrow(start, end, buff=0, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.35)
            )
        return arrows

    @staticmethod
    def cross_arrows(dots_p, dots_q, color=WHITE):
        """One arrow per point pair across the two clusters -- separation:
        every point is far from every point in the other cluster."""
        arrows = VGroup()
        for p_dot, q_dot in zip(dots_p, dots_q):
            arrows.add(
                DoubleArrow(
                    p_dot.get_center(), q_dot.get_center(), buff=0.12, color=color,
                    stroke_width=2, stroke_opacity=0.7, max_tip_length_to_length_ratio=0.12,
                )
            )
        return arrows

    def scene_12(self):
        title = Text("How to Determine Number of Clusters", font_size=32).to_edge(UP, buff=0.4)

        with self.voiceover(
            text=(
                "Let's take a pause here. Regardless of which method you are "
                "using in practice, you need to determine the number of "
                "clusters."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "In hierarchical clustering, you need to determine the number "
                "of clusters to read out the cluster solutions."
            )
        ) as tracker:
            # A real dendrogram of the shared data, not an abstract glyph.
            tree_icon = make_mini_dendrogram(width=2.6, height=1.3, color=BLUE).move_to(
                LEFT * 3 + UP * 1.3
            )
            tree_note = Text("cut the dendrogram", font_size=20, color=GRAY).next_to(
                tree_icon, DOWN, buff=0.3
            )
            self.play(Create(tree_icon, lag_ratio=0.1), run_time=1)
            self.play(Write(tree_note), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="In k-means, you need to explicitly specify number of clusters as an input to the algorithm."
        ) as tracker:
            # A real K-Means result on the shared data, not an abstract glyph.
            kboxes_icon = make_mini_kmeans_scatter(width=2.4, height=1.3).move_to(
                RIGHT * 3 + UP * 1.3
            )
            kboxes_note = Text("specify K upfront", font_size=20, color=GRAY).next_to(
                kboxes_icon, DOWN, buff=0.3
            )
            self.play(FadeIn(kboxes_icon, lag_ratio=0.08), run_time=1)
            self.play(Write(kboxes_note), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="So, how should we determine the number of clusters?") as tracker:
            self.play(
                FadeOut(tree_icon), FadeOut(tree_note), FadeOut(kboxes_icon), FadeOut(kboxes_note),
                run_time=1,
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "This is fundamentally an evaluation question. Ideally, we want "
                "to pick the cluster number that produces the \"best\" "
                "clustering solution."
            )
        ) as tracker:
            subtitle = Text("→ an evaluation question", font_size=26, color=YELLOW).next_to(
                title, DOWN, buff=0.4
            )
            self.play(Write(subtitle), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="But what is the \"best\" clustering solution?") as tracker:
            self.wait(tracker.get_remaining_duration())

        left_center = LEFT * 3.4 + DOWN * 0.6
        right_center = RIGHT * 3.4 + DOWN * 0.6

        with self.voiceover(
            text=(
                "Remember, we want clusters to have high intra-similarity, "
                "meaning that data points in the same clusters are similar to "
                "each other. This is known as cohesion."
            )
        ) as tracker:
            self.play(FadeOut(subtitle), run_time=0.5)

            left_box = RoundedRectangle(
                width=5.4, height=4.0, corner_radius=0.15, color=GRAY
            ).move_to(left_center)
            left_title = Text("High Intra-Similarity", font_size=22, color=YELLOW).next_to(
                left_box, UP, buff=0.15
            )
            self.play(Create(left_box), Write(left_title), run_time=1.3)

            dots_p1, dots_q1 = self.build_box_clusters(left_center + UP * 0.3)
            self.play(FadeIn(dots_p1), FadeIn(dots_q1), run_time=1)

            circle_p1 = encircle(dots_p1, CLUSTER_P_COLOR)
            circle_q1 = encircle(dots_q1, CLUSTER_Q_COLOR)
            self.play(Create(circle_p1), Create(circle_q1), run_time=1)

            # Cohesion: inward arrows within EACH cluster, not just one.
            arrows_in_p = self.inward_arrows(dots_p1, CLUSTER_P_COLOR)
            arrows_in_q = self.inward_arrows(dots_q1, CLUSTER_Q_COLOR)
            self.play(Create(arrows_in_p), Create(arrows_in_q), run_time=1)
            cohesion_label = Text("Cohesion", font_size=24, color=YELLOW).next_to(
                left_box, DOWN, buff=0.2
            )
            self.play(Write(cohesion_label), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "We also want clusters to have low inter-similarity, meaning "
                "that different clusters should be well separated from one "
                "another. This is known as separation."
            )
        ) as tracker:
            right_box = RoundedRectangle(
                width=5.4, height=4.0, corner_radius=0.15, color=GRAY
            ).move_to(right_center)
            right_title = Text("Low Inter-Similarity", font_size=22, color=YELLOW).next_to(
                right_box, UP, buff=0.15
            )
            self.play(Create(right_box), Write(right_title), run_time=1.3)

            dots_p2, dots_q2 = self.build_box_clusters(right_center + UP * 0.3)
            self.play(FadeIn(dots_p2), FadeIn(dots_q2), run_time=1)

            circle_p2 = encircle(dots_p2, CLUSTER_P_COLOR)
            circle_q2 = encircle(dots_q2, CLUSTER_Q_COLOR)
            self.play(Create(circle_p2), Create(circle_q2), run_time=1)

            # Separation: cross-cluster arrows, not a single double-arrow.
            cross = self.cross_arrows(dots_p2, dots_q2)
            self.play(Create(cross, lag_ratio=0.15), run_time=1.2)
            separation_label = Text("Separation", font_size=24, color=YELLOW).next_to(
                right_box, DOWN, buff=0.2
            )
            self.play(Write(separation_label), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title),
            FadeOut(left_box), FadeOut(left_title), FadeOut(dots_p1), FadeOut(dots_q1),
            FadeOut(circle_p1), FadeOut(circle_q1), FadeOut(arrows_in_p), FadeOut(arrows_in_q),
            FadeOut(cohesion_label),
            FadeOut(right_box), FadeOut(right_title), FadeOut(dots_p2), FadeOut(dots_q2),
            FadeOut(circle_p2), FadeOut(circle_q2), FadeOut(cross), FadeOut(separation_label),
        )


class Scene12(VoiceoverScene, Scene12Mixin):
    """Standalone preview: manim -pql scene_12.py Scene12"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_12()
