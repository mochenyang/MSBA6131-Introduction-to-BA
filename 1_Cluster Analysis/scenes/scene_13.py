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
    HIER_COLORS,
    NATURAL_GROUPS,
    compute_dendrogram,
    dendrogram_cut_height,
)

# Independently reconstructs the same dendrogram scene_10 builds (both call
# common.compute_dendrogram(), which is deterministic) at this scene's own,
# larger layout -- no dependency on scene_10 having actually run.
DEND_X_SCALE = 0.11
DEND_Y_SCALE = 0.9
DEND_BASE_Y = -3.0


class Scene13Mixin:
    # ------------------------------------------------------------------
    # Scene 13: Reading cohesion/separation off a dendrogram (the gap)
    # ------------------------------------------------------------------
    def scene13_dend_xy(self, xval, yval):
        return np.array(
            [(xval - self.dend_x_mid) * DEND_X_SCALE, DEND_BASE_Y + yval * DEND_Y_SCALE, 0]
        )

    def scene13_make_dend_u(self, icoord_row, dcoord_row, color=WHITE, stroke_width=3):
        pts = [self.scene13_dend_xy(x, y) for x, y in zip(icoord_row, dcoord_row)]
        u = VMobject(color=color, stroke_width=stroke_width)
        u.set_points_as_corners(pts)
        return u

    def scene_13(self):
        title = Text("Reading Cohesion & Separation off a Dendrogram", font_size=30).to_edge(
            UP, buff=0.4
        )
        Z, icoord, dcoord = compute_dendrogram()
        icoord_arr = np.array(icoord)
        self.dend_x_mid = (icoord_arr.min() + icoord_arr.max()) / 2
        dend_us = [self.scene13_make_dend_u(icoord[i], dcoord[i]) for i in range(len(Z))]
        dend_group = VGroup(*dend_us)

        with self.voiceover(
            text=(
                "For hierarchical clustering, the cohesion and separation of "
                "clusters can be visually gauged by inspecting the dendrogram."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(Create(dend_group, lag_ratio=0.15), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        cut_height, trunks = dendrogram_cut_height(Z, icoord)

        with self.voiceover(
            text=(
                "Take the following dendrogram as an example: after three "
                "clusters form during the merging process, there's a large gap "
                "before two of those three clusters merge into a bigger one."
            )
        ) as tracker:
            markers = VGroup()
            for gi, group in enumerate(NATURAL_GROUPS):
                row, trunk_x = trunks[tuple(group)]
                marker_y = Z[row][2]
                markers.add(Dot(self.scene13_dend_xy(trunk_x, marker_y), color=HIER_COLORS[gi], radius=0.08))
            self.play(FadeIn(markers, scale=1.5), run_time=1.3)

            # The next merge (index 4) is the "3 clusters -> 2 clusters" step
            # -- highlight its two risers, which visually carry the big jump.
            gap_row = max(row for row, _ in trunks.values()) + 1
            self.play(
                dend_us[gap_row].animate.set_color(RED).set_stroke(width=5), run_time=1.5
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "This is good evidence that there are 3 natural clusters in "
                "the data, because going from 3 clusters to 2 means merging "
                "clusters that are very far apart."
            )
        ) as tracker:
            left_riser_bottom = self.scene13_dend_xy(icoord[gap_row][0], dcoord[gap_row][0])
            left_riser_top = self.scene13_dend_xy(icoord[gap_row][1], dcoord[gap_row][1])
            brace = Brace(
                Line(left_riser_bottom, left_riser_top), direction=LEFT, color=RED
            )
            gap_label = Text(
                "large gap →\nnatural cluster solution", font_size=22, color=RED, line_spacing=1.1
            ).next_to(brace, LEFT, buff=0.2)
            self.play(GrowFromCenter(brace), run_time=1)
            self.play(Write(gap_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(dend_group), FadeOut(markers), FadeOut(brace), FadeOut(gap_label),
        )


class Scene13(VoiceoverScene, Scene13Mixin):
    """Standalone preview: manim -pql scene_13.py Scene13"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_13()
