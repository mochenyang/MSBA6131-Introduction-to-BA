import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_mini_dendrogram, make_mini_kmeans_scatter


class Scene09Mixin:
    # ------------------------------------------------------------------
    # Scene 9: Clustering methods taxonomy
    # ------------------------------------------------------------------
    def scene_09(self):
        title = Text("Clustering Methods", font_size=40).to_edge(UP, buff=0.5)

        with self.voiceover(
            text=(
                "We now have all the ingredients needed for doing clustering "
                "analyses. There are many different types of clustering methods."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(tracker.get_remaining_duration())

        left_box = RoundedRectangle(width=4.8, height=1.0, corner_radius=0.15, color=BLUE).move_to(
            LEFT * 3.5 + UP * 0.9
        )
        left_label = Text("Hierarchical Methods", font_size=26, color=BLUE).move_to(left_box)
        right_box = RoundedRectangle(width=4.8, height=1.0, corner_radius=0.15, color=TEAL).move_to(
            RIGHT * 3.5 + UP * 0.9
        )
        right_label = Text("Partition-Based Methods", font_size=26, color=TEAL).move_to(right_box)
        branch_left = Line(title.get_bottom() + DOWN * 0.1, left_box.get_top(), color=GRAY)
        branch_right = Line(title.get_bottom() + DOWN * 0.1, right_box.get_top(), color=GRAY)

        with self.voiceover(
            text=(
                "One type is the hierarchical method, where the algorithm forms "
                "larger clusters from smaller ones, or breaks larger clusters "
                "into smaller ones, in a hierarchical fashion -- we'll talk "
                "about a specific technique called hierarchical clustering."
            )
        ) as tracker:
            self.play(Create(branch_left), run_time=1.2)
            self.play(Create(left_box), Write(left_label), run_time=1.8)
            # A real dendrogram of the shared dataset, not an abstract tree
            # glyph -- this is the actual structure scene_10 will build.
            tree_icon = make_mini_dendrogram(width=2.6, height=1.3, color=BLUE).next_to(
                left_box, DOWN, buff=0.5
            )
            self.play(Create(tree_icon, lag_ratio=0.1), run_time=1.3)
            technique_left = Text("Hierarchical Clustering", font_size=22, color=WHITE).next_to(
                tree_icon, DOWN, buff=0.35
            )
            self.play(Write(technique_left), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Another type is the partition-based method, where the idea is "
                "to directly partition the data into K groups, K being the "
                "desired number of clusters. K-Means belongs to this category."
            )
        ) as tracker:
            self.play(Create(branch_right), run_time=1.2)
            self.play(Create(right_box), Write(right_label), run_time=1.8)
            # A real K-Means result on the shared dataset (colored by its
            # actual converged assignment), not an abstract "K boxes" glyph.
            kboxes_icon = make_mini_kmeans_scatter(width=2.4, height=1.3).next_to(
                right_box, DOWN, buff=0.5
            )
            self.play(FadeIn(kboxes_icon, lag_ratio=0.08), run_time=1.3)
            technique_right = Text("K-Means", font_size=22, color=WHITE).next_to(
                kboxes_icon, DOWN, buff=0.35
            )
            self.play(Write(technique_right), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(branch_left), FadeOut(branch_right),
            FadeOut(left_box), FadeOut(left_label), FadeOut(tree_icon), FadeOut(technique_left),
            FadeOut(right_box), FadeOut(right_label), FadeOut(kboxes_icon), FadeOut(technique_right),
        )


class Scene09(VoiceoverScene, Scene09Mixin):
    """Standalone preview: manim -pql scene_09.py Scene09"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_09()
