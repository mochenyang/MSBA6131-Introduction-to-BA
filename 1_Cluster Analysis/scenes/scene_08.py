import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene


from tts import get_speech_service


class Scene08Mixin:
    # ------------------------------------------------------------------
    # Scene 8: Distance between clusters (linkage methods)
    # ------------------------------------------------------------------
    @staticmethod
    def to_box(pt, box_center):
        # Maps a point from the original big two-cluster layout into a small
        # scaled-down position inside a given grid box, all six boxes reusing
        # the exact same underlying point positions.
        ORIG_CENTER = np.array([0, 0.3, 0])
        MINI_SCALE = 0.38
        return box_center + DOWN * 0.35 + (np.array(pt) - ORIG_CENTER) * MINI_SCALE

    def make_box(self, box_center, label_text, label_color, subtitle_text):
        box_rect = RoundedRectangle(
            width=4.2, height=3.0, corner_radius=0.15, color=GRAY, stroke_width=2
        ).move_to(box_center)
        label = Text(label_text, font_size=16, color=label_color, line_spacing=1.0).move_to(
            box_center + UP * 1.15
        )
        subtitle = Text(subtitle_text, font_size=13, color=GRAY).next_to(label, DOWN, buff=0.12)
        return box_rect, label, subtitle

    def scene_08(self):
        # Color used once the two clusters are conceptually merged into one:
        # both clusters' dots and every connecting line drawn after the
        # merge all share this single color.
        MERGED_COLOR = YELLOW

        title = Text("Distance Between Clusters", font_size=36).to_edge(UP, buff=0.4)

        # 2 rows x 3 columns of boxes, filling the space under the title.
        # Each box appears once, when its method is introduced, and then
        # stays on screen (no more fade-in/fade-out between methods).
        col_xs = [-4.6, 0, 4.6]
        row_ys = [1.4, -2.1]
        pos_single = np.array([col_xs[0], row_ys[0], 0])
        pos_complete = np.array([col_xs[1], row_ys[0], 0])
        pos_average = np.array([col_xs[2], row_ys[0], 0])
        pos_centroid = np.array([col_xs[0], row_ys[1], 0])
        pos_agl = np.array([col_xs[1], row_ys[1], 0])
        pos_ward = np.array([col_xs[2], row_ys[1], 0])

        # The underlying two-cluster point layout is still generated (every
        # box's mini visualization is derived from these same positions) --
        # it's just never displayed full-size on screen anymore.
        rng = np.random.default_rng(11)
        c1_centers = LEFT * 3 + UP * 0.3
        c2_centers = RIGHT * 3 + UP * 0.3
        cluster1 = VGroup(
            *[
                Dot(c1_centers + np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0]), color=BLUE)
                for _ in range(5)
            ]
        )
        cluster2 = VGroup(
            *[
                Dot(c2_centers + np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0]), color=GREEN)
                for _ in range(5)
            ]
        )

        with self.voiceover(
            text=(
                "So far we've talked about how to measure the distance between "
                "data points. We also need to know how to measure the distance "
                "between clusters."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Fortunately, distance between clusters is basically defined by "
                "selecting or aggregating certain distances between the data "
                "points in each cluster. Here are some commonly used metrics."
            )
        ) as tracker:
            metric_note1 = Text("Selecting or aggregating", font_size=26, color=YELLOW)
            metric_note2 = Text("point-to-point distances", font_size=26, color=YELLOW)
            metric_note = VGroup(metric_note1, metric_note2).arrange(DOWN, buff=0.15).next_to(
                title, DOWN, buff=0.4
            )
            self.play(FadeIn(metric_note1, shift=UP * 0.2), run_time=1.5)
            self.play(FadeIn(metric_note2, shift=UP * 0.2), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        pts1 = np.array([d.get_center() for d in cluster1])
        pts2 = np.array([d.get_center() for d in cluster2])
        dists = np.linalg.norm(pts1[:, None, :] - pts2[None, :, :], axis=2)
        i_min, j_min = np.unravel_index(np.argmin(dists), dists.shape)
        i_max, j_max = np.unravel_index(np.argmax(dists), dists.shape)
        centroid1 = pts1.mean(axis=0)
        centroid2 = pts2.mean(axis=0)
        all_pts = np.vstack([pts1, pts2])
        merged_centroid = all_pts.mean(axis=0)

        with self.voiceover(
            text=(
                "Single linkage measures the distance between two clusters as "
                "the shortest distance between one data point in each cluster."
            )
        ) as tracker:
            self.play(FadeOut(metric_note), run_time=0.6)

            box_single, label_single, sub_single = self.make_box(
                pos_single, "Single Linkage", YELLOW, "closest pair"
            )
            mini1_s = VGroup(*[Dot(self.to_box(p, pos_single), radius=0.045, color=BLUE) for p in pts1])
            mini2_s = VGroup(*[Dot(self.to_box(p, pos_single), radius=0.045, color=GREEN) for p in pts2])
            line_single = Line(
                self.to_box(pts1[i_min], pos_single), self.to_box(pts2[j_min], pos_single),
                color=WHITE, stroke_width=3,
            )
            self.play(
                Create(box_single), FadeIn(mini1_s), FadeIn(mini2_s),
                Write(label_single), Write(sub_single),
                run_time=1.6,
            )
            self.play(Create(line_single), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="Complete linkage instead looks at the longest such distance.") as tracker:
            box_complete, label_complete, sub_complete = self.make_box(
                pos_complete, "Complete Linkage", RED, "farthest pair"
            )
            mini1_c = VGroup(*[Dot(self.to_box(p, pos_complete), radius=0.045, color=BLUE) for p in pts1])
            mini2_c = VGroup(*[Dot(self.to_box(p, pos_complete), radius=0.045, color=GREEN) for p in pts2])
            line_complete = Line(
                self.to_box(pts1[i_max], pos_complete), self.to_box(pts2[j_max], pos_complete),
                color=WHITE, stroke_width=3,
            )
            self.play(
                Create(box_complete), FadeIn(mini1_c), FadeIn(mini2_c),
                Write(label_complete), Write(sub_complete),
                run_time=1.3,
            )
            self.play(Create(line_complete), run_time=0.7)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Average linkage measures all pairwise distances between data "
                "points in the two clusters and takes the average."
            )
        ) as tracker:
            box_average, label_average, sub_average = self.make_box(
                pos_average, "Average Linkage", TEAL, "mean of all pairs"
            )
            mini1_a = VGroup(*[Dot(self.to_box(p, pos_average), radius=0.045, color=BLUE) for p in pts1])
            mini2_a = VGroup(*[Dot(self.to_box(p, pos_average), radius=0.045, color=GREEN) for p in pts2])
            lines_average = VGroup(
                *[
                    Line(
                        self.to_box(p1, pos_average), self.to_box(p2, pos_average),
                        color=WHITE, stroke_width=1, stroke_opacity=0.5,
                    )
                    for p1 in pts1
                    for p2 in pts2
                ]
            )
            self.play(
                Create(box_average), FadeIn(mini1_a), FadeIn(mini2_a),
                Write(label_average), Write(sub_average),
                run_time=1.6,
            )
            self.play(Create(lines_average, lag_ratio=0.02), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Centroid distance measures the distance between the centroid of "
                "each cluster, which is the geometric center of a cluster."
            )
        ) as tracker:
            box_centroid, label_centroid, sub_centroid = self.make_box(
                pos_centroid, "Centroid Distance", PURPLE, "center to center"
            )
            mini1_ce = VGroup(*[Dot(self.to_box(p, pos_centroid), radius=0.045, color=BLUE) for p in pts1])
            mini2_ce = VGroup(*[Dot(self.to_box(p, pos_centroid), radius=0.045, color=GREEN) for p in pts2])
            cross1_mini = Cross(scale_factor=0.1, stroke_color=BLUE).move_to(
                self.to_box(centroid1, pos_centroid)
            )
            cross2_mini = Cross(scale_factor=0.1, stroke_color=GREEN).move_to(
                self.to_box(centroid2, pos_centroid)
            )
            line_centroid = Line(
                self.to_box(centroid1, pos_centroid), self.to_box(centroid2, pos_centroid),
                color=WHITE, stroke_width=3,
            )
            self.play(
                Create(box_centroid), FadeIn(mini1_ce), FadeIn(mini2_ce),
                Write(label_centroid), Write(sub_centroid),
                run_time=1.6,
            )
            self.play(FadeIn(cross1_mini), FadeIn(cross2_mini), run_time=0.8)
            self.play(Create(line_centroid), run_time=1)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Finally, average group linkage and Ward's method both first "
                "imagine that the two clusters are merged into a single, bigger "
                "cluster."
            )
        ) as tracker:
            # The last two grid slots are still empty at this point -- use
            # that space for the bridging idea instead of overlapping the
            # four boxes already on screen.
            merge_caption = Text(
                "Imagine both clusters\nmerged into one",
                font_size=22, color=MERGED_COLOR, line_spacing=1.2,
            ).move_to((pos_agl + pos_ward) / 2)
            self.play(FadeIn(merge_caption, shift=UP * 0.2), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Average group linkage measures the average pairwise distance "
                "between all data points in that merged cluster,"
            )
        ) as tracker:
            self.play(FadeOut(merge_caption), run_time=0.5)

            box_agl, label_agl, sub_agl = self.make_box(
                pos_agl, "Average Group Linkage", TEAL, "merged cluster pairwise average"
            )
            mini_agl = VGroup(
                *[Dot(self.to_box(p, pos_agl), radius=0.045, color=MERGED_COLOR) for p in all_pts]
            )
            lines_agl = VGroup(
                *[
                    Line(
                        self.to_box(all_pts[a], pos_agl), self.to_box(all_pts[b], pos_agl),
                        color=MERGED_COLOR, stroke_width=1, stroke_opacity=0.4,
                    )
                    for a in range(len(all_pts))
                    for b in range(a + 1, len(all_pts))
                ]
            )
            self.play(Create(box_agl), FadeIn(mini_agl), Write(label_agl), Write(sub_agl), run_time=1.6)
            self.play(Create(lines_agl, lag_ratio=0.01), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "whereas Ward's method measures the sum of squared distances "
                "between each data point and the centroid of the merged cluster."
            )
        ) as tracker:
            box_ward, label_ward, sub_ward = self.make_box(
                pos_ward, "Ward's Method", ORANGE, "sum of squared distances to center"
            )
            mini_ward = VGroup(
                *[Dot(self.to_box(p, pos_ward), radius=0.045, color=MERGED_COLOR) for p in all_pts]
            )
            cross_ward = Cross(scale_factor=0.12, stroke_color=MERGED_COLOR).move_to(
                self.to_box(merged_centroid, pos_ward)
            )
            lines_ward = VGroup(
                *[
                    Line(
                        self.to_box(p, pos_ward), self.to_box(merged_centroid, pos_ward),
                        color=MERGED_COLOR, stroke_width=1.2,
                    )
                    for p in all_pts
                ]
            )
            self.play(Create(box_ward), FadeIn(mini_ward), Write(label_ward), Write(sub_ward), run_time=1.6)
            self.play(FadeIn(cross_ward), run_time=0.5)
            self.play(Create(lines_ward, lag_ratio=0.05), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title),
            FadeOut(box_single), FadeOut(label_single), FadeOut(sub_single),
            FadeOut(mini1_s), FadeOut(mini2_s), FadeOut(line_single),
            FadeOut(box_complete), FadeOut(label_complete), FadeOut(sub_complete),
            FadeOut(mini1_c), FadeOut(mini2_c), FadeOut(line_complete),
            FadeOut(box_average), FadeOut(label_average), FadeOut(sub_average),
            FadeOut(mini1_a), FadeOut(mini2_a), FadeOut(lines_average),
            FadeOut(box_centroid), FadeOut(label_centroid), FadeOut(sub_centroid),
            FadeOut(mini1_ce), FadeOut(mini2_ce),
            FadeOut(cross1_mini), FadeOut(cross2_mini), FadeOut(line_centroid),
            FadeOut(box_agl), FadeOut(label_agl), FadeOut(sub_agl), FadeOut(mini_agl), FadeOut(lines_agl),
            FadeOut(box_ward), FadeOut(label_ward), FadeOut(sub_ward),
            FadeOut(mini_ward), FadeOut(cross_ward), FadeOut(lines_ward),
        )


class Scene08(VoiceoverScene, Scene08Mixin):
    """Standalone preview: manim -pql scene_08.py Scene08"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_08()
