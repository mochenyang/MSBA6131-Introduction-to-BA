import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import CLUSTER_POINTS_2D, KMEANS_COLORS, kmeans_final_centroids

N_POINTS = len(CLUSTER_POINTS_2D)
SCATTER_CENTER = LEFT * 3.3 + DOWN * 0.3
SCATTER_SCALE = 0.62
RIGHT_COL = RIGHT * 3.2  # x-anchor for the formula/text column


class Scene14Mixin:
    # ------------------------------------------------------------------
    # Scene 14: Evaluating cluster quality -- SSE and Silhouette
    # ------------------------------------------------------------------
    @staticmethod
    def scene14_scatter_pos(i):
        x, y = CLUSTER_POINTS_2D[i]
        return SCATTER_CENTER + np.array([x, y, 0]) * SCATTER_SCALE

    @staticmethod
    def centroid_pos(centers, k):
        x, y = centers[k]
        return SCATTER_CENTER + np.array([x, y, 0]) * SCATTER_SCALE

    @staticmethod
    def cluster_members(assign, k):
        # K-Means' internal cluster numbering (0/1/2) doesn't necessarily
        # line up with any fixed group ordering -- always derive membership
        # from the assignment array itself, never assume an index mapping.
        return [j for j in range(len(assign)) if assign[j] == k]

    def scene_14(self):
        title = Text("Evaluating Cluster Quality", font_size=34).to_edge(UP, buff=0.4)
        centers, assign = kmeans_final_centroids()
        dots = VGroup(
            *[Dot(self.scene14_scatter_pos(i), radius=0.08, color=KMEANS_COLORS[assign[i]]) for i in range(N_POINTS)]
        )

        # The point with the largest distance to its own centroid -- gives
        # the "error" arrow real visible length instead of a tiny stub.
        errors = [np.linalg.norm(np.array(CLUSTER_POINTS_2D[i]) - centers[assign[i]]) for i in range(N_POINTS)]
        X_IDX = int(np.argmax(errors))

        with self.voiceover(
            text="Besides visual inspection, cohesion and separation can also be quantitatively calculated from data."
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="The first metric, sum-of-squared-errors, or SSE, measures cohesion.") as tracker:
            sse_header = Text("SSE measures cohesion", font_size=24, color=WHITE).move_to(
                RIGHT_COL + UP * 2.5
            )
            self.play(Write(sse_header), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="Suppose you have the following 3 clusters, C1 through C3, with centroids m1 through m3."
        ) as tracker:
            crosses = VGroup()
            cluster_labels = VGroup()
            centroid_labels = VGroup()
            for k in range(3):
                members = self.cluster_members(assign, k)
                crosses.add(Cross(scale_factor=0.14, stroke_color=KMEANS_COLORS[k]).move_to(
                    self.centroid_pos(centers, k)
                ))
                member_dots = VGroup(*[dots[j] for j in members])
                cluster_labels.add(
                    Text(f"C{k + 1}", font_size=20, color=KMEANS_COLORS[k]).next_to(
                        member_dots, UP, buff=0.15
                    )
                )
                centroid_labels.add(
                    Text(f"m{k + 1}", font_size=18, color=KMEANS_COLORS[k]).next_to(
                        member_dots, DOWN, buff=0.15
                    )
                )
            self.play(FadeIn(crosses), run_time=1)
            self.play(Write(cluster_labels), Write(centroid_labels), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "For any data point, we define its error as the distance "
                "between the data point and its cluster's centroid."
            )
        ) as tracker:
            error_line = DashedLine(
                self.scene14_scatter_pos(X_IDX), self.centroid_pos(centers, assign[X_IDX]),
                color=WHITE, stroke_width=3,
            )
            # Anchor near the data-point end of the line (not its midpoint --
            # the centroid end sits inside the crowded cluster interior,
            # close to other members and the centroid cross), then offset
            # perpendicular to whichever side is farther from every dot and
            # centroid cross. The centroid itself can't be used to pick a
            # side (it's on the line, equidistant from both), and a fixed
            # "UP" offset could land the label on a neighboring point
            # depending on the line's angle.
            line_vec = error_line.get_end() - error_line.get_start()
            perp = np.array([-line_vec[1], line_vec[0], 0])
            perp = perp / np.linalg.norm(perp)
            anchor = error_line.get_start() * 0.7 + error_line.get_end() * 0.3
            side_a, side_b = anchor + perp * 0.5, anchor - perp * 0.5

            avoid_points = [self.scene14_scatter_pos(i) for i in range(N_POINTS)] + [
                c.get_center() for c in crosses
            ]

            def min_dist_to_avoid(p):
                return min(np.linalg.norm(p - q) for q in avoid_points)

            label_pos = max((side_a, side_b), key=min_dist_to_avoid)
            x_label = Text("error", font_size=18, color=WHITE).move_to(label_pos)
            self.play(Create(error_line), run_time=1.3)
            self.play(Write(x_label), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="SSE is then the sum of squared errors across all data points.") as tracker:
            sse_formula = MathTex(
                r"SSE = \sum_i \|x_i - m_{c(i)}\|^2", font_size=32, color=WHITE
            ).next_to(sse_header, DOWN, buff=0.4)
            self.play(Write(sse_formula), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "A lower SSE means data points are generally close to their "
                "cluster centers, indicating high cohesion."
            )
        ) as tracker:
            sse_note = Text(
                "lower SSE → higher cohesion", font_size=20, color=GRAY
            ).next_to(sse_formula, DOWN, buff=0.3)
            self.play(FadeIn(sse_note, shift=UP * 0.2), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="However, SSE doesn't tell us about separation.") as tracker:
            # Kept in place (not shrunk/moved) per feedback -- Silhouette
            # content is appended below it instead of replacing it.
            sse_block = VGroup(sse_header, sse_formula, sse_note)
            self.play(FadeOut(x_label), run_time=0.4)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="The metric that captures both cohesion and separation is the Silhouette coefficient."
        ) as tracker:
            sil_header = Text("Silhouette Coefficient", font_size=22, color=WHITE).next_to(
                sse_note, DOWN, buff=0.35
            )
            self.play(Write(sil_header), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Given a data point X in cluster C, we define two quantities.") as tracker:
            self.play(FadeOut(error_line), run_time=0.5)
            big_x_label = Text("X", font_size=22, color=WHITE).next_to(
                dots[X_IDX], LEFT, buff=0.15
            )
            self.play(Indicate(dots[X_IDX], scale_factor=1.6), Write(big_x_label), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "A(x) measures the average distance between X and other data "
                "points in the same cluster C -- a measure of cohesion, where "
                "a smaller A(x) indicates a tighter, more cohesive cluster."
            )
        ) as tracker:
            x_cluster = assign[X_IDX]
            same_cluster = [j for j in self.cluster_members(assign, x_cluster) if j != X_IDX]
            a_arrows = VGroup(
                *[
                    Arrow(
                        self.scene14_scatter_pos(X_IDX), self.scene14_scatter_pos(j), buff=0.12,
                        color=KMEANS_COLORS[x_cluster], stroke_width=3,
                        max_tip_length_to_length_ratio=0.1, tip_length=0.12,
                    )
                    for j in same_cluster
                ]
            )
            a_label = Text(
                "A(x): avg. distance within cluster", font_size=16, color=KMEANS_COLORS[x_cluster]
            ).next_to(sil_header, DOWN, buff=0.3)
            self.play(Create(a_arrows, lag_ratio=0.15), run_time=1.8)
            self.play(Write(a_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "B(x) measures the smallest average distance between X and "
                "all data points in another cluster -- it captures how close "
                "X is to its nearest neighboring cluster; a larger B(x) means "
                "X is well separated from other clusters."
            )
        ) as tracker:
            other_ks = [k for k in range(3) if k != x_cluster]
            dists_to_centroids = [
                np.linalg.norm(np.array(CLUSTER_POINTS_2D[X_IDX]) - centers[k]) for k in other_ks
            ]
            nearest_k = other_ks[int(np.argmin(dists_to_centroids))]
            nearest_members = self.cluster_members(assign, nearest_k)
            b_arrows = VGroup(
                *[
                    Arrow(
                        self.scene14_scatter_pos(X_IDX), self.scene14_scatter_pos(j), buff=0.12,
                        color=KMEANS_COLORS[nearest_k], stroke_width=3,
                        max_tip_length_to_length_ratio=0.1, tip_length=0.12,
                    )
                    for j in nearest_members
                ]
            )
            b_label = Text(
                "B(x): avg. distance to nearest cluster", font_size=16, color=KMEANS_COLORS[nearest_k]
            ).next_to(a_label, DOWN, buff=0.25)
            self.play(Create(b_arrows, lag_ratio=0.15), run_time=1.8)
            self.play(Write(b_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="The Silhouette coefficient of X is then calculated from A(x) and B(x).") as tracker:
            sil_formula = MathTex(
                r"s(x) = \frac{B(x) - A(x)}{\max(A(x), B(x))}", font_size=28, color=WHITE
            ).next_to(b_label, DOWN, buff=0.35)
            self.play(Write(sil_formula), run_time=2.2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "We can aggregate the Silhouette coefficients of all points "
                "in a cluster to reflect that cluster's quality, or average "
                "across all points to capture the quality of the entire "
                "clustering solution."
            )
        ) as tracker:
            agg_note = Text(
                "aggregate: per-cluster or overall average", font_size=16, color=GRAY
            ).next_to(sil_formula, DOWN, buff=0.3)
            self.play(FadeIn(agg_note, shift=UP * 0.2), run_time=2.2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "A higher Silhouette coefficient implies B(x) is higher, A(x) "
                "is lower, or both -- meaning the clustering solution has both "
                "high cohesion and good separation."
            )
        ) as tracker:
            final_note = Text(
                "higher s(x) → better cohesion + separation", font_size=16, color=GREEN
            ).next_to(agg_note, DOWN, buff=0.3)
            self.play(FadeIn(final_note, shift=UP * 0.2), run_time=2.2)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(dots), FadeOut(crosses), FadeOut(cluster_labels), FadeOut(centroid_labels),
            FadeOut(big_x_label), FadeOut(a_arrows), FadeOut(a_label), FadeOut(b_arrows), FadeOut(b_label),
            FadeOut(sse_block), FadeOut(sil_header), FadeOut(sil_formula), FadeOut(agg_note), FadeOut(final_note),
        )


class Scene14(VoiceoverScene, Scene14Mixin):
    """Standalone preview: manim -pql scene_14.py Scene14"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_14()
