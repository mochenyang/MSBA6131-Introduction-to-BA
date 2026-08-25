import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    CLUSTER_POINTS_2D,
    HIER_COLORS,
    NATURAL_GROUPS,
    compute_dendrogram,
    dendrogram_cut_height,
    dendrogram_merge_members,
    encircle,
)

N_POINTS = len(CLUSTER_POINTS_2D)

# Layout constants for mapping the shared point data and scipy's raw
# dendrogram coordinates into this scene's screen space.
SCATTER_CENTER = UP * 1.5
SCATTER_SCALE = 0.62
DEND_X_SCALE = 0.095
DEND_Y_SCALE = 0.58
DEND_BASE_Y = -3.3

# Color for merges beyond the 3 natural groups -- once two differently
# colored groups merge, both take on this neutral color, so color keeps
# tracking cluster membership all the way to a single, unicolor cluster.
MERGED_COLOR = GRAY


class Scene10Mixin:
    # ------------------------------------------------------------------
    # Scene 10: Hierarchical clustering + dendrogram
    # ------------------------------------------------------------------
    @staticmethod
    def scene10_scatter_pos(i):
        x, y = CLUSTER_POINTS_2D[i]
        return SCATTER_CENTER + np.array([x, y, 0]) * SCATTER_SCALE

    def scene10_dend_xy(self, xval, yval):
        return np.array(
            [(xval - self.dend_x_mid) * DEND_X_SCALE, DEND_BASE_Y + yval * DEND_Y_SCALE, 0]
        )

    def scene10_make_dend_u(self, icoord_row, dcoord_row, color=WHITE):
        pts = [self.scene10_dend_xy(x, y) for x, y in zip(icoord_row, dcoord_row)]
        u = VMobject(color=color, stroke_width=3)
        u.set_points_as_corners(pts)
        return u

    @staticmethod
    def merge_group_index(members):
        """Which NATURAL_GROUPS index this fully-merged member set belongs
        to (if it's still entirely within one natural group), else None."""
        s = set(members)
        for gi, g in enumerate(NATURAL_GROUPS):
            if s.issubset(set(g)):
                return gi
        return None

    def scene_10(self):
        title = Text("Hierarchical Clustering", font_size=36).to_edge(UP, buff=0.4)
        dots = VGroup(*[Dot(self.scene10_scatter_pos(i), radius=0.08, color=WHITE) for i in range(N_POINTS)])

        with self.voiceover(
            text=(
                "Let's start with hierarchical clustering, which can be "
                "understood intuitively. The idea is to take a bottom-up "
                "approach: starting from individual data points or smaller "
                "clusters, we form larger clusters in a hierarchical manner."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text="More specifically, in step 1, we assign each data point to be its own cluster."
        ) as tracker:
            self.play(
                LaggedStart(*[Indicate(d, scale_factor=1.6) for d in dots], lag_ratio=0.08),
                run_time=2,
            )
            self.wait(tracker.get_remaining_duration())

        Z, icoord, dcoord = compute_dendrogram()
        icoord_arr = np.array(icoord)
        self.dend_x_mid = (icoord_arr.min() + icoord_arr.max()) / 2
        merge_members = dendrogram_merge_members(Z)
        dend_group = VGroup()

        def do_merge(i, run_time):
            left, right = merge_members[i]
            combined = left + right
            gi = self.merge_group_index(combined)
            # Beyond the 3 natural groups, color still tracks membership --
            # it just switches to the shared neutral color, so two merged
            # groups (and eventually all 12 points) read as one cluster.
            color = HIER_COLORS[gi] if gi is not None else MERGED_COLOR
            u = self.scene10_make_dend_u(icoord[i], dcoord[i])
            dend_group.add(u)
            # Mark the merge by color, not by a connecting line: both halves
            # being merged take on the (eventual) cluster's color.
            self.play(
                *[dots[j].animate.set_color(color) for j in combined],
                Create(u),
                run_time=run_time,
            )

        with self.voiceover(
            text=(
                "In step 2, we merge the two clusters that are closest to each "
                "other, based on our choice of a distance metric, so that a "
                "larger cluster is formed."
            )
        ) as tracker:
            do_merge(0, 1.8)
            # Explain the dendrogram the first time it appears, rather than
            # only naming it once the whole tree is already built.
            dend_explain = Text(
                "↑ this is a \"dendrogram\": each step's height = distance at merge",
                font_size=16, color=GRAY,
            ).next_to(dend_group, DOWN, buff=0.25)
            self.play(Write(dend_explain), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "We then simply repeat step 2, each time merging the two "
                "closest clusters into a larger one, until there is only one "
                "cluster left containing all the data points."
            )
        ) as tracker:
            for i in range(1, len(Z)):
                do_merge(i, 0.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "The output of the hierarchical clustering algorithm is a "
                "graph called a dendrogram. The dendrogram records the entire "
                "cluster-merging process, and therefore contains solutions for "
                "any number of clusters you may want."
            )
        ) as tracker:
            dend_title = Text("Dendrogram", font_size=24, color=GRAY).next_to(
                dend_group, UP, buff=0.25
            )
            self.play(FadeOut(dend_explain), Write(dend_title), run_time=2)
            self.play(Indicate(dend_group, scale_factor=1.05), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "To read a dendrogram, imagine it as a tree with many branches "
                "that you want to cut to read out a clustering solution."
            )
        ) as tracker:
            # Top sits inside the gap between the last intra-group merge and
            # the first inter-group merge (recomputed for CLUSTER_POINTS_2D's
            # current spread); bottom sits below the smallest merge height.
            sweep_top_y = self.scene10_dend_xy(self.dend_x_mid, 3.2)[1]
            sweep_bottom_y = self.scene10_dend_xy(self.dend_x_mid, 0.4)[1]
            sweep_line = DashedLine(
                LEFT * 5.5 + UP * sweep_top_y, RIGHT * 5.5 + UP * sweep_top_y, color=GRAY, stroke_width=3
            )
            self.play(Create(sweep_line), run_time=1)
            self.play(sweep_line.animate.shift(DOWN * (sweep_top_y - sweep_bottom_y)), run_time=2)
            self.play(FadeOut(sweep_line), run_time=0.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "For example, in this case, if I want a 3-cluster solution, I "
                "can cut the dendrogram here, and obtain the data points that "
                "belong to each of the three clusters."
            )
        ) as tracker:
            cut_height, trunks = dendrogram_cut_height(Z, icoord)
            cut_y = self.scene10_dend_xy(self.dend_x_mid, cut_height)[1]
            cut_line = DashedLine(
                np.array([-5.8, cut_y, 0]), np.array([5.8, cut_y, 0]), color=WHITE, stroke_width=3
            )
            self.play(Create(cut_line), run_time=1)

            cut_dots = VGroup()
            group_circles = VGroup()
            for gi, group in enumerate(NATURAL_GROUPS):
                _, trunk_x = trunks[tuple(group)]
                cut_dots.add(Dot(self.scene10_dend_xy(trunk_x, cut_height), color=HIER_COLORS[gi], radius=0.08))
            self.play(FadeIn(cut_dots), run_time=0.8)

            # By now the scatter points have merged all the way to a single
            # color -- recover the 3-cluster coloring the cut recovers.
            recolor_anims = [
                dots[j].animate.set_color(HIER_COLORS[gi])
                for gi, group in enumerate(NATURAL_GROUPS)
                for j in group
            ]
            self.play(*recolor_anims, run_time=1)

            for gi, group in enumerate(NATURAL_GROUPS):
                member_dots = VGroup(*[dots[j] for j in group])
                group_circles.add(encircle(member_dots, HIER_COLORS[gi]))
            self.play(*[Create(c) for c in group_circles], run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(dots), FadeOut(dend_group), FadeOut(dend_title),
            FadeOut(cut_line), FadeOut(cut_dots), FadeOut(group_circles),
        )


class Scene10(VoiceoverScene, Scene10Mixin):
    """Standalone preview: manim -pql scene_10.py Scene10"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_10()
