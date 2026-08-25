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


class Scene02Mixin:
    # ------------------------------------------------------------------
    # Scene 2: Walmart market segmentation motivating example
    # ------------------------------------------------------------------
    def scene_02(self):
        axes, x_label, y_label = make_customer_axes()
        plot = VGroup(axes, x_label, y_label).scale(0.95).to_edge(DOWN, buff=0.6)
        group_a, group_b, group_c = make_customer_clusters(axes)
        all_dots = VGroup(*group_a, *group_b, *group_c)
        # Neutral until each group's identity is narrated below, so the
        # "eyeball three distinct groups" line is a spatial discovery rather
        # than an already-colored answer.
        all_dots.set_color(GRAY)

        title = Text("A Motivating Example", font_size=40)
        subtitle = Text(
            "Identify Customer Groups for Walmart", font_size=28, color=YELLOW
        ).next_to(title, DOWN, buff=0.3)
        title_card = VGroup(title, subtitle)

        with self.voiceover(
            text=(
                "Imagine you are a data scientist working for Walmart, and you want to "
                "understand if Walmart's 280 million customers fall into any distinct "
                "groups."
            )
        ) as tracker:
            self.play(FadeOut(self.title_scene_01), run_time=1)
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "For concreteness, say you describe each customer based on their "
                "shopping budget -- how much money they want to spend shopping at "
                "Walmart -- and price sensitivity -- how sensitive they are with "
                "respect to price changes. Looking at this plot, we can eyeball at "
                "least three distinct groups, or \"clusters\", of customers."
            )
        ) as tracker:
            self.play(title_card.animate.scale(0.5).to_edge(UP, buff=0.4), run_time=1)
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
            self.play(Indicate(y_label), run_time=1)
            self.wait(3)
            self.play(Indicate(x_label), run_time=1)
            self.play(FadeIn(all_dots, lag_ratio=0.05), run_time=2)
            self.wait(tracker.get_remaining_duration())

        circle_a = encircle(group_a, BRAND_LOYALIST_COLOR)
        label_a = Text("Brand Loyalists", font_size=24, color=BRAND_LOYALIST_COLOR).next_to(
            circle_a, UP, buff=0.2
        )
        with self.voiceover(
            text=(
                "One group has a relatively high budget and low price sensitivity. "
                "They are willing and are able to spend more money if needed, perhaps "
                "because they are loyal to certain brands."
            )
        ) as tracker:
            self.play(group_a.animate.set_color(BRAND_LOYALIST_COLOR), Create(circle_a), run_time=1.5)
            self.play(Write(label_a), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        circle_b = encircle(group_b, BUDGET_CONSTRAINED_COLOR)
        label_b = Text("Budget Constrained", font_size=24, color=BUDGET_CONSTRAINED_COLOR).next_to(
            circle_b, RIGHT, buff=0.2
        )
        with self.voiceover(
            text=(
                "A second group has relatively low budget and high sensitivity. "
                "Because they don't have a big budget, they may stop buying certain "
                "things if the price increase."
            )
        ) as tracker:
            self.play(group_b.animate.set_color(BUDGET_CONSTRAINED_COLOR), Create(circle_b), run_time=1.5)
            self.play(Write(label_b), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        circle_c = encircle(group_c, PRICE_SENSITIVE_COLOR)
        label_c = Text("Price Sensitive", font_size=24, color=PRICE_SENSITIVE_COLOR).next_to(
            circle_c, RIGHT, buff=0.2
        )
        with self.voiceover(
            text=(
                "A third group has comparatively higher budget than the second group, "
                "but similarly high price sensitivity. These are people who are very "
                "careful with their money."
            )
        ) as tracker:
            self.play(group_c.animate.set_color(PRICE_SENSITIVE_COLOR), Create(circle_c), run_time=1.5)
            self.play(Write(label_c), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Having such information can help executives at Walmart customize "
                "their marketing strategy to customers of each group."
            )
        ) as tracker:
            self.play(
                Indicate(
                    VGroup(circle_a, label_a, circle_b, label_b, circle_c, label_c),
                    scale_factor=1.03,
                ),
                run_time=2,
            )
            self.wait(tracker.get_remaining_duration())

        strategy_a = Text("Brand Promotions", font_size=22, color=BRAND_LOYALIST_COLOR)
        strategy_b = Text("Low-Price Ads", font_size=22, color=BUDGET_CONSTRAINED_COLOR)
        strategy_c = Text("Discount Coupons", font_size=22, color=PRICE_SENSITIVE_COLOR)

        with self.voiceover(
            text="For the brand loyalist, brand promotions campaigns may get them to spend more money."
        ) as tracker:
            self.play(
                FadeTransform(label_a, strategy_a.move_to(label_a)),
                run_time=1.5,
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "For the budget constrained customers, advertising low-price options "
                "can be a good way to keep their businesses."
            )
        ) as tracker:
            self.play(
                FadeTransform(label_b, strategy_b.move_to(label_b)),
                run_time=1.5,
            )
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "For the price sensitive shoppers, sending them discount coupons can "
                "meaningfully boost spending."
            )
        ) as tracker:
            self.play(
                FadeTransform(label_c, strategy_c.move_to(label_c)),
                run_time=1.5,
            )
            self.wait(tracker.get_remaining_duration())

        self.play(
            FadeOut(strategy_a), FadeOut(strategy_b), FadeOut(strategy_c),
            FadeOut(circle_a), FadeOut(circle_b), FadeOut(circle_c),
            FadeOut(title_card),
        )

        # Kept around so later scenes can reuse the exact same scatter plot.
        self.customer_plot = plot
        self.customer_axes = axes
        self.customer_dots = (group_a, group_b, group_c)


class Scene02(VoiceoverScene, Scene02Mixin):
    """Standalone preview: manim -pql scene_02.py Scene02"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_01()
        self.scene_02()

    def _fixture_scene_01(self):
        # Stand-in for scene_01's output so scene_02 can be previewed alone.
        self.title_scene_01 = Text("Cluster Analysis")
        self.add(self.title_scene_01)
