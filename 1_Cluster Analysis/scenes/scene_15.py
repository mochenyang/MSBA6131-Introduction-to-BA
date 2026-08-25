import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene
from scipy.cluster.vq import kmeans2

from tts import get_speech_service
from common import CLUSTER_POINTS_2D, HIER_COLORS, NATURAL_GROUPS, Text

N_POINTS = len(CLUSTER_POINTS_2D)
MINI_CENTER = LEFT * 5.5
MINI_SCALE = 0.24


def compute_real_sse_curve():
    """Actual SSE at each K from 1 to N, via K-Means on the shared data --
    not a synthetic function. SSE is exactly 0 at K = N (each point its own
    cluster)."""
    pts = np.array(CLUSTER_POINTS_2D)
    sse_vals = []
    for k in range(1, N_POINTS + 1):
        if k == N_POINTS:
            sse_vals.append(0.0)
            continue
        centers, labels = kmeans2(pts, k, seed=42, minit="++")
        sse = sum(
            float(np.linalg.norm(pts[i] - centers[labels[i]]) ** 2) for i in range(N_POINTS)
        )
        sse_vals.append(sse)
    return sse_vals


class Scene15Mixin:
    # ------------------------------------------------------------------
    # Scene 15: The elbow method
    # ------------------------------------------------------------------
    def scene_15(self):
        title = Text("Choosing K: the Elbow Method", font_size=32).to_edge(UP, buff=0.4)

        # The actual data points, shown on the side throughout -- this is
        # the same dataset every K in the plot is computed from.
        mini_dots = VGroup()
        for gi, group in enumerate(NATURAL_GROUPS):
            for j in group:
                x, y = CLUSTER_POINTS_2D[j]
                pos = MINI_CENTER + np.array([x, y, 0]) * MINI_SCALE
                mini_dots.add(Dot(pos, radius=0.06, color=HIER_COLORS[gi]))
        mini_label = Text("Our data", font_size=18, color=GRAY).next_to(mini_dots, UP, buff=0.3)

        axes = Axes(
            x_range=[1, N_POINTS + 0.001, 1], y_range=[0, 170, 20], x_length=7.8, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 18},
        ).move_to(RIGHT * 1.3 + DOWN * 0.5)
        x_label = axes.get_x_axis_label(
            Text("Number of Clusters (K)", font_size=20), edge=DOWN, direction=DOWN, buff=0.35
        )
        y_label = axes.get_y_axis_label(Text("SSE", font_size=20), edge=LEFT, direction=LEFT, buff=0.3)

        with self.voiceover(
            text=(
                "With objective clustering quality metrics such as SSE, we can "
                "also pick the number of clusters by trying different numbers "
                "and plot the SSE measure against the number of clusters."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.6)
            self.play(FadeIn(mini_dots, lag_ratio=0.05), Write(mini_label), run_time=1.5)
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        sse_vals = compute_real_sse_curve()
        k_values = list(range(1, N_POINTS + 1))
        graph = axes.plot_line_graph(
            x_values=k_values, y_values=sse_vals, line_color=YELLOW,
            vertex_dot_radius=0.05, add_vertex_dots=True,
        )

        with self.voiceover(
            text=(
                "Importantly, the best cluster solution is not the one that "
                "minimizes SSE -- when number of clusters equal number of data "
                "points, the SSE reduces to 0."
            )
        ) as tracker:
            self.play(Create(graph), run_time=3.5)
            end_note = Text("SSE → 0 here, but not the goal!", font_size=18, color=GRAY).next_to(
                axes.c2p(N_POINTS, 0), UP + LEFT, buff=0.3
            )
            self.play(FadeIn(end_note, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        elbow_k = 3
        elbow_point = axes.c2p(elbow_k, sse_vals[elbow_k - 1])

        with self.voiceover(
            text=(
                "Instead, we look for an \"elbow\" shape in the SSE plot -- a "
                "point where SSE drops sharply before, then becomes fairly "
                "flat after."
            )
        ) as tracker:
            self.play(FadeOut(end_note), run_time=0.6)
            elbow_circle = Circle(radius=0.35, color=RED).move_to(elbow_point)
            self.play(Create(elbow_circle), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Because SSE tends to drop as we increase the number of "
                "clusters, hitting an elbow point typically means we've found "
                "a natural number of clusters."
            )
        ) as tracker:
            dashed = DashedLine(elbow_point, axes.c2p(elbow_k, 0), color=RED, stroke_width=3)
            elbow_label = Text(f"Elbow point (K = {elbow_k})", font_size=22, color=RED).next_to(
                elbow_circle, UP + RIGHT, buff=0.3
            )
            self.play(Create(dashed), run_time=1.3)
            self.play(Write(elbow_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(graph),
            FadeOut(mini_dots), FadeOut(mini_label),
            FadeOut(elbow_circle), FadeOut(dashed), FadeOut(elbow_label),
        )


class Scene15(VoiceoverScene, Scene15Mixin):
    """Standalone preview: manim -pql scene_15.py Scene15"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_15()
