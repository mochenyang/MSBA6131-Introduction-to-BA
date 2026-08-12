import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    BRAND_LOYALIST_COLOR,
    BUDGET_CONSTRAINED_COLOR,
    PRICE_SENSITIVE_COLOR,
    make_customer_axes,
    make_customer_clusters,
)


class Scene04Mixin:
    # ------------------------------------------------------------------
    # Scene 4: Clustering (exploratory) vs classification (predictive)
    # ------------------------------------------------------------------
    def scene_04(self):
        title = Text("Clustering vs Classification", font_size=36).to_edge(UP, buff=0.4)
        divider = Line(UP * 3, DOWN * 3.2, color=GRAY)
        left_title = Text("Clustering (Exploratory)", font_size=26, color=YELLOW).move_to(
            LEFT * 3.5 + UP * 2.6
        )
        right_title = Text("Classification (Predictive)", font_size=26, color=YELLOW).move_to(
            RIGHT * 3.5 + UP * 2.6
        )

        with self.voiceover(
            text=(
                "Clustering analysis is a type of exploratory analytics. "
                "To make this point clear, it's worth "
                "differentiating clustering from classification, which is a "
                "type of predictive analytics."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(Create(divider), run_time=1)
            self.play(Write(left_title), run_time=2)
            self.play(Write(right_title), run_time=2)
            self.play(Indicate(left_title), run_time=1)
            self.play(Indicate(right_title), run_time=1)
            self.wait(tracker.get_remaining_duration())

        # Reuse the exact same customer scatter from the Walmart example
        # (common.py's deterministic rng) rather than inventing new points.
        # These dots never move again -- "discovering" the clusters is done
        # purely by highlighting them in place, one at a time.
        axes, _, _ = make_customer_axes()
        group_a, group_b, group_c = make_customer_clusters(axes)
        walmart_dots = VGroup(*group_a, *group_b, *group_c).scale(0.55).move_to(LEFT * 3.5 + DOWN * 0.1)
        # Start neutral -- membership colors are revealed cluster-by-cluster
        # below, which is what actually sells "cluster discovery."
        walmart_dots.set_color(GRAY)

        bucket_shape = [LEFT * 1 + UP * 0.55, RIGHT * 1 + UP * 0.55, RIGHT * 0.7 + DOWN * 0.55, LEFT * 0.7 + DOWN * 0.55]
        pos_bucket = Polygon(*bucket_shape, color=GREEN, stroke_width=4).move_to(RIGHT * 1.9 + DOWN * 2.2)
        pos_label = Text("Positive", font_size=22, color=GREEN).next_to(pos_bucket, UP, buff=0.15)
        neg_bucket = Polygon(*bucket_shape, color=RED, stroke_width=4).move_to(RIGHT * 4.3 + DOWN * 2.2)
        neg_label = Text("Negative", font_size=22, color=RED).next_to(neg_bucket, UP, buff=0.15)

        with self.voiceover(
            text=(
                "The difference is that clustering aims to discover groups from "
                "data, whereas classification aims to put data into pre-defined "
                "groups."
            )
        ) as tracker:
            self.play(FadeIn(walmart_dots, lag_ratio=0.05), run_time=2)
            self.wait(3)
            self.play(
                Create(pos_bucket), Write(pos_label), Create(neg_bucket), Write(neg_label), run_time=2
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Take the Walmart market segmentation case as an example. Before "
                "conducting the analysis, Walmart does not know there would be "
                "three groups of customers -- the three groups are a result of the "
                "segmentation analysis."
            )
        ) as tracker:
            colors = [BRAND_LOYALIST_COLOR, BUDGET_CONSTRAINED_COLOR, PRICE_SENSITIVE_COLOR]
            groups = [group_a, group_b, group_c]

            # Highlight one cluster at a time (progressive disclosure) -- the
            # dots themselves stay exactly where they already were; only their
            # color changes, from neutral gray to their true membership color.
            self.wait(2)
            discovered_circles = VGroup()
            for group, color in zip(groups, colors):
                circle = SurroundingRectangle(group, color=color, buff=0.15, corner_radius=0.2)
                discovered_circles.add(circle)
                self.play(group.animate.set_color(color), Create(circle), run_time=1.6)
                self.play(Indicate(group, scale_factor=1.2), run_time=0.6)

            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "In a predictive classification task, by contrast, the groups, also "
                "called classes, must be pre-specified."
            )
        ) as tracker:
            self.play(
                Indicate(pos_bucket), Indicate(neg_bucket), Indicate(pos_label), Indicate(neg_label), run_time=2
            )
            self.wait(tracker.get_remaining_duration())

        post_texts = ["Love this store!", "Best prices ever!", "Terrible customer service", "Way too expensive today"]
        post_sentiment = [1, 1, 0, 0]  # 1 = positive, 0 = negative
        posts_start = [
            RIGHT * 3.5 + LEFT * 1.8 + UP * 1.9,
            RIGHT * 3.5 + RIGHT * 1.8 + UP * 1.9,
            RIGHT * 3.5 + LEFT * 1.8 + UP * 0.7,
            RIGHT * 3.5 + RIGHT * 1.8 + UP * 0.7,
        ]
        posts = VGroup(
            *[
                Text(t, font_size=15, color=GRAY).move_to(p)
                for t, p in zip(post_texts, posts_start)
            ]
        )
        with self.voiceover(
            text=(
                "For example, classifying social media posts as having positive or "
                "negative sentiment is classification, because the two "
                "groups are pre-specified."
            )
        ) as tracker:
            self.play(FadeIn(posts, lag_ratio=0.15), run_time=1.5)
            anims = []
            slot_offset = {1: 0, 0: 0}
            for post, sentiment in zip(posts, post_sentiment):
                target_bucket = pos_bucket if sentiment == 1 else neg_bucket
                target_color = GREEN if sentiment == 1 else RED
                dy = UP * 0.22 if slot_offset[sentiment] == 0 else DOWN * 0.22
                slot_offset[sentiment] += 1
                anims.append(
                    post.animate.scale(0.55)
                    .move_to(target_bucket.get_center() + dy)
                    .set_color(target_color)
                )
            self.play(*anims, run_time=2.5)
            positive_posts = VGroup(*[p for p, s in zip(posts, post_sentiment) if s == 1])
            negative_posts = VGroup(*[p for p, s in zip(posts, post_sentiment) if s == 0])
            self.play(Indicate(positive_posts), Indicate(negative_posts), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(title), FadeOut(divider), FadeOut(left_title), FadeOut(right_title),
            FadeOut(walmart_dots), FadeOut(discovered_circles),
            FadeOut(pos_bucket), FadeOut(pos_label), FadeOut(neg_bucket), FadeOut(neg_label), FadeOut(posts),
        )


class Scene04(VoiceoverScene, Scene04Mixin):
    """Standalone preview: manim -pql scene_04.py Scene04"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_04()
