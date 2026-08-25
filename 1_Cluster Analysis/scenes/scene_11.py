import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import CLUSTER_POINTS_2D, KMEANS_COLORS, KMEANS_INIT_IDX, kmeans_iterations, Text

N_POINTS = len(CLUSTER_POINTS_2D)
SCATTER_CENTER = UP * 0.3
SCATTER_SCALE = 0.75


class Scene11Mixin:
    # ------------------------------------------------------------------
    # Scene 11: K-Means clustering
    # ------------------------------------------------------------------
    @staticmethod
    def scene11_scatter_pos(i):
        x, y = CLUSTER_POINTS_2D[i]
        return SCATTER_CENTER + np.array([x, y, 0]) * SCATTER_SCALE

    @staticmethod
    def scatter_pos_from_xy(xy):
        x, y = xy[0], xy[1]
        return SCATTER_CENTER + np.array([x, y, 0]) * SCATTER_SCALE

    def scene_11(self):
        title = Text("K-Means Clustering", font_size=36).to_edge(UP, buff=0.4)
        dots = VGroup(*[Dot(self.scene11_scatter_pos(i), radius=0.08, color=WHITE) for i in range(N_POINTS)])

        with self.voiceover(
            text=(
                "In comparison, K-Means is a completely different approach. The "
                "idea of K-Means is to directly partition the data into K "
                "clusters, then make incremental adjustments to improve the "
                "partition. Here's an illustration."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Suppose we want to find 3 clusters in this data.") as tracker:
            k_label = Text("K = 3", font_size=26, color=GRAY).next_to(title, DOWN, buff=0.3)
            self.play(Write(k_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # 4 rounds: an initial bad assignment, two real correction rounds,
        # then one round confirming nothing changes further.
        steps = kmeans_iterations()

        with self.voiceover(
            text=(
                "We start by randomly choosing 3 data points, colored red, "
                "green, and yellow, and pretend they're the centers of the "
                "three clusters."
            )
        ) as tracker:
            centers0, assign0 = steps[0]
            crosses = VGroup(
                *[
                    Cross(scale_factor=0.16, stroke_color=KMEANS_COLORS[k]).move_to(
                        self.scatter_pos_from_xy(centers0[k])
                    )
                    for k in range(3)
                ]
            )
            init_recolor = [
                dots[idx].animate.set_color(KMEANS_COLORS[k]) for k, idx in enumerate(KMEANS_INIT_IDX)
            ]
            self.play(*init_recolor, run_time=1)
            self.play(FadeIn(crosses), run_time=1.2)
            init_label = Text("Initial centers (random)", font_size=22, color=GRAY).next_to(
                dots, DOWN, buff=0.6
            )
            self.play(Write(init_label), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Next, we assign each remaining data point to a cluster based "
                "on which center it is closest to."
            )
        ) as tracker:
            recolor0 = [
                dots[j].animate.set_color(KMEANS_COLORS[assign0[j]])
                for j in range(N_POINTS)
                if j not in KMEANS_INIT_IDX
            ]
            self.play(*recolor0, run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Since we chose the three initial points at random, the result "
                "at the end of this step doesn't look very good."
            )
        ) as tracker:
            self.play(FadeOut(init_label), run_time=0.5)
            not_great = Text("Not great...", font_size=24, color=GRAY).next_to(dots, DOWN, buff=0.6)
            self.play(FadeIn(not_great, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        def move_and_reassign(step_idx, run_time):
            centers, assign = steps[step_idx]
            targets = [self.scatter_pos_from_xy(centers[k]) for k in range(3)]
            self.play(*[crosses[k].animate.move_to(targets[k]) for k in range(3)], run_time=run_time)
            self.play(
                *[dots[j].animate.set_color(KMEANS_COLORS[assign[j]]) for j in range(N_POINTS)],
                run_time=run_time,
            )

        with self.voiceover(
            text=(
                "No need to worry, because we'll next find the new centroids "
                "of each of the three clusters and re-assign all data points "
                "to the three clusters."
            )
        ) as tracker:
            self.play(FadeOut(not_great), run_time=0.5)
            move_and_reassign(1, 1.3)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="Comparing this step to the previous one, you can already see some improvements."
        ) as tracker:
            # A second real correction round -- this is where the "moving
            # process" keeps visibly improving rather than being done in one
            # shot.
            move_and_reassign(2, 0.9)
            better = Text("Better!", font_size=24, color=GREEN).next_to(dots, DOWN, buff=0.6)
            self.play(FadeIn(better, shift=UP * 0.2), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="We repeat this process multiple times until the clusters no longer change."
        ) as tracker:
            # One more round: centroids settle to their true final positions,
            # but the color assignment no longer changes -- convergence.
            move_and_reassign(3, 0.9)
            converged = Text("Converged!", font_size=24, color=GREEN).move_to(better)
            self.play(FadeTransform(better, converged), run_time=1)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(k_label), FadeOut(dots), FadeOut(crosses), FadeOut(converged),
        )


class Scene11(VoiceoverScene, Scene11Mixin):
    """Standalone preview: manim -pql scene_11.py Scene11"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_11()
