import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import CLUSTER_POINTS_2D, HIER_COLORS, NATURAL_GROUPS, Text

# Reuse one of the three shared groups (rather than a fresh one-off cluster)
# so this scene's illustration is literally the same running example.
FEATURED_GROUP = NATURAL_GROUPS[0]
FEATURED_COLOR = HIER_COLORS[0]
DISPLAY_CENTER = LEFT * 2.2
DISPLAY_SCALE = 2.3


class Scene16Mixin:
    # ------------------------------------------------------------------
    # Scene 16: Interpreting clusters (cluster profile + domain knowledge)
    # ------------------------------------------------------------------
    def scene_16(self):
        title = Text("Interpreting Clustering Results", font_size=34).to_edge(UP, buff=0.4)

        raw = np.array([CLUSTER_POINTS_2D[j] for j in FEATURED_GROUP])
        raw_center = raw.mean(axis=0)
        pts = [
            DISPLAY_CENTER + np.array([(x - raw_center[0]) * DISPLAY_SCALE, (y - raw_center[1]) * DISPLAY_SCALE, 0])
            for x, y in raw
        ]
        dots = VGroup(*[Dot(p, radius=0.09, color=FEATURED_COLOR) for p in pts])
        centroid = np.mean(pts, axis=0)

        with self.voiceover(
            text=(
                "Finally, suppose we have carried out clustering analysis and "
                "decided on a particular clustering solution, how do we "
                "interpret what each cluster means?"
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(FadeIn(dots, lag_ratio=0.08), run_time=1.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Typically, we can interpret each cluster by its \"average\" "
                "data point, which is the centroid of the cluster -- formally, "
                "the mean of all data points in that cluster."
            )
        ) as tracker:
            centroid_mark = Cross(scale_factor=0.22, stroke_color=YELLOW, stroke_width=5).move_to(
                centroid
            )
            self.play(FadeIn(centroid_mark, scale=1.5), run_time=1.5)
            # Anchored to the whole point group's bounding box (not just the
            # centroid mark) so it can't land on top of a data point.
            profile_label = Text("Cluster Profile", font_size=24, color=YELLOW).next_to(
                dots, DOWN, buff=0.4
            )
            self.play(Write(profile_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "It may or may not be an actual data point itself, but it "
                "nonetheless represents the average characteristics of the "
                "data in that cluster."
            )
        ) as tracker:
            formula = MathTex(
                r"m = \frac{1}{n}\sum_{i=1}^{n} x_i", font_size=32, color=YELLOW
            ).next_to(profile_label, DOWN, buff=0.55)
            self.play(Write(formula), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "More importantly, given the exploratory nature of clustering "
                "analysis, interpreting clustering results must be combined "
                "with domain knowledge."
            )
        ) as tracker:
            bubble = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.3, color=GRAY).move_to(
                RIGHT * 3 + UP * 0.5
            )
            bubble_title = Text("Domain Knowledge Check", font_size=20, color=GRAY).next_to(
                bubble, UP, buff=0.2
            )
            self.play(Create(bubble), Write(bubble_title), run_time=2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Think about whether the clusters make sense to you as a data "
                "scientist, and whether they help you solve the problem you "
                "set out to answer."
            )
        ) as tracker:
            q1 = Text(
                "Does this make sense given\nwhat I know about the business?",
                font_size=18, color=WHITE, line_spacing=1.3,
            ).move_to(bubble.get_center() + UP * 0.4)
            self.play(Write(q1), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Instead of trying to find the objectively best solution, "
                "keep in mind that there is no absolute \"correct\" clustering "
                "result -- your interpretation and evaluation depend on your "
                "business problem and goals."
            )
        ) as tracker:
            q2 = Text(
                "No single \"correct\" answer --\nit depends on your goals.",
                font_size=18, color=YELLOW, line_spacing=1.3,
            ).next_to(q1, DOWN, buff=0.3)
            self.play(Write(q2), run_time=2.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(dots), FadeOut(centroid_mark), FadeOut(profile_label), FadeOut(formula),
            FadeOut(bubble), FadeOut(bubble_title), FadeOut(q1), FadeOut(q2),
        )


class Scene16(VoiceoverScene, Scene16Mixin):
    """Standalone preview: manim -pql scene_16.py Scene16"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_16()
