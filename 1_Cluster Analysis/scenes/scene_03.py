import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    BRAND_LOYALIST_COLOR,
    BUDGET_CONSTRAINED_COLOR,
    PRICE_SENSITIVE_COLOR,
    make_customer_axes,
    make_customer_clusters,
    encircle,
)


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: Formal definition of clustering (intra/inter-similarity)
    # ------------------------------------------------------------------
    def scene_03(self):
        group_a, group_b, group_c = self.customer_dots
        all_dots = VGroup(*group_a, *group_b, *group_c)

        with self.voiceover(
            text="This is an example of Market segmentation, which is a representative application of cluster analysis."
        ) as tracker:
            headline = Text("Market Segmentation", font_size=36, color=YELLOW)
            sub = Text("→ an application of Cluster Analysis", font_size=30).next_to(headline, DOWN, buff=0.4)
            self.play(FadeOut(self.customer_plot), FadeOut(all_dots), run_time=1)
            self.play(Write(headline), run_time=1.5)
            self.play(FadeIn(sub, shift=UP * 0.3), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        definition_line1 = Text("Clustering: organize data points into", font_size=32)
        definition_line2 = Text(
            "homogeneous, meaningful groups (clusters).", font_size=32
        ).next_to(definition_line1, DOWN, buff=0.25)
        definition = VGroup(definition_line1, definition_line2).move_to(ORIGIN)
        with self.voiceover(
            text=(
                "Formally, the goal of clustering analysis is to organize data points, "
                "or objects in general, into homogeneous and hopefully meaningful "
                "groups. Each group is called a cluster."
            )
        ) as tracker:
            self.play(FadeOut(headline), FadeOut(sub), run_time=1)
            self.play(Write(definition_line1), run_time=2.5)
            self.play(Write(definition_line2), run_time=2)
            self.play(Circumscribe(definition_line2, color=YELLOW), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(text="There are two objectives of clustering.") as tracker:
            self.play(definition.animate.scale(0.7).to_edge(UP, buff=0.4), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        circle_a = encircle(group_a, BRAND_LOYALIST_COLOR)
        circle_b = encircle(group_b, BUDGET_CONSTRAINED_COLOR)
        circle_c = encircle(group_c, PRICE_SENSITIVE_COLOR)

        with self.voiceover(
            text=(
                "First, we want data points that belong to the same cluster to be "
                "similar to each other -- this is called high intra-similarity."
            )
        ) as tracker:
            self.play(FadeIn(self.customer_plot), FadeIn(all_dots), run_time=1.5)
            self.play(Create(circle_a), Create(circle_b), Create(circle_c), run_time=1.5)

            pairwise_lines = VGroup(
                *[
                    Line(p1, p2, color=BRAND_LOYALIST_COLOR, stroke_width=1.5, stroke_opacity=0.6)
                    for p1, p2 in itertools.combinations(
                        [dot.get_center() for dot in group_a], 2
                    )
                ]
            )
            intra_label = Text("High Intra-Similarity", font_size=22, color=BRAND_LOYALIST_COLOR).next_to(
                circle_a, DOWN, buff=0.2
            )
            self.play(Create(pairwise_lines, lag_ratio=0.05), run_time=1.5)
            self.play(Write(intra_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Second, we want data points that belong to different clusters to be "
                "different from each other -- this is called low inter-similarity."
            )
        ) as tracker:
            inter_arrow = DoubleArrow(
                circle_a.get_right(), circle_c.get_left(), color=WHITE, buff=0.1, stroke_width=3
            )
            inter_label = Text("Low Inter-Similarity", font_size=22, color=WHITE).next_to(
                VGroup(circle_a, circle_c), UP, buff=0.2
            )
            self.play(GrowFromCenter(inter_arrow), run_time=1.5)
            self.play(Write(inter_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        checkmark = Text(
            "Natural Grouping Structure", font_size=26, color=YELLOW
        ).next_to(definition, DOWN, buff=0.35)
        with self.voiceover(
            text=(
                "In general, high intra-similarity and low inter-similarity together "
                "indicate that we have discovered natural grouping structures in the "
                "data: each group is sufficiently homogeneous, and different groups "
                "are sufficiently separated."
            )
        ) as tracker:
            self.play(Indicate(VGroup(circle_a, pairwise_lines, intra_label)), run_time=1.5)
            self.play(Indicate(VGroup(inter_arrow, inter_label)), run_time=1.5)
            self.wait(2.0)
            self.play(FadeIn(checkmark, shift=UP * 0.3), run_time=1.5)
            # Circumscribe(checkmark, ...) would size the box off checkmark.height,
            # which manim misreports for Text mobjects shifted off the y=0 axis
            # (space-glyph placeholders have zero points, so the bounding-box
            # reducer falls back to a literal 0 and pollutes the min/max) --
            # get_top()/get_bottom() aren't affected, so build the box from those.
            checkmark_box = Rectangle(
                width=checkmark.width + 0.2,
                height=(checkmark.get_top()[1] - checkmark.get_bottom()[1]) + 0.2,
                color=YELLOW,
                stroke_width=4,
            ).move_to(checkmark.get_center())
            self.play(ShowPassingFlash(checkmark_box, time_width=0.3), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(definition), FadeOut(all_dots), FadeOut(circle_a), FadeOut(circle_b), FadeOut(circle_c),
            FadeOut(pairwise_lines), FadeOut(intra_label), FadeOut(inter_arrow), FadeOut(inter_label),
            FadeOut(checkmark), FadeOut(self.customer_plot),
        )


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_02()
        self.scene_03()

    def _fixture_scene_02(self):
        # Stand-in for scene_02's ending state so scene_03 can be previewed
        # alone, without replaying scene_02's animations/voiceover.
        axes, x_label, y_label = make_customer_axes()
        plot = VGroup(axes, x_label, y_label).scale(0.95).to_edge(DOWN, buff=0.6)
        group_a, group_b, group_c = make_customer_clusters(axes)
        all_dots = VGroup(*group_a, *group_b, *group_c)
        self.add(plot, all_dots)

        self.customer_plot = plot
        self.customer_axes = axes
        self.customer_dots = (group_a, group_b, group_c)
