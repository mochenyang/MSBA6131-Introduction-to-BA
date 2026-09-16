import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, SELECTED_COLOR, REJECTED_COLOR


class Scene06Mixin:
    # ------------------------------------------------------------------
    # Scene 6: the filter approach to feature selection
    # ------------------------------------------------------------------
    @staticmethod
    def scene6_check_icon(color=SELECTED_COLOR, size=0.28):
        check = VMobject(color=color, stroke_width=5)
        check.set_points_as_corners(
            [np.array([-0.5, 0.0, 0]), np.array([-0.15, -0.35, 0]), np.array([0.5, 0.45, 0])]
        )
        return check.scale(size)

    def scene_06(self):
        # Full title is wider than the screen -- it's written out in full
        # first (centered as a whole), then morphs into the shorter
        # "Filter Approach"-only title that stays up for the rest of the
        # scene, rather than being built from two separately-positioned
        # Text mobjects (which pushed " and Wrapper Approach" off-screen).
        title_full = Text(
            "General-Purpose Feature Selection: Filter Approach and Wrapper Approach", font_size=24
        ).to_edge(UP, buff=0.4)
        title_short = Text("General-Purpose Feature Selection: Filter Approach", font_size=24).to_edge(
            UP, buff=0.4
        )
        subtitle = Text("Select by feature importance measure before building the model", font_size=20, color=GREY_B)
        subtitle.next_to(title_short, DOWN, buff=0.3)

        feature_ys = [1.2, 0.6, 0.0, -0.6, -1.2]

        # -- funnel geometry -------------------------------------------------
        funnel = Polygon(
            np.array([-1.5, 1.05, 0]), np.array([-1.5, -1.05, 0]),
            np.array([1.1, -0.24, 0]), np.array([1.1, 0.24, 0]),
            color=WHITE, stroke_width=3,
        ).move_to(UP * feature_ys[2])  # vertically level with X_3
        exit_point = funnel.get_center()
        icon_spot = funnel.get_top() + UP * 0.35
        # Shared anchor for the two below-funnel panels (bullets on the
        # left, ranked bars on the right), so they sit side by side under
        # the funnel with a gap between them instead of stacking/overlapping.
        # aligned_edge=UP (used below) top-aligns both panels to this point
        # regardless of their own height, so the taller one (the ranked
        # bars, with a title above and a label below) can't poke back up
        # into the funnel the way center-alignment did.
        below_funnel = funnel.get_bottom() + DOWN * 0.35

        features = VGroup(
            *[MathTex(f"X_{i + 1}", font_size=30).move_to(LEFT * 3.4 + UP * y) for i, y in enumerate(feature_ys)]
        )
        pass_mask = [True, False, True, False, True]
        selected_slots = [UP * 0.7, UP * 0.0, DOWN * 0.7]
        selected_area_center = RIGHT * 3.3

        with self.voiceover(
            text=(
                "More generally, feature selection approaches fall into two "
                "types: the filter approach and the wrapper approach. We will "
                "focus on the filter approach first. The idea is to filter out "
                "uninformative features before the model is built, and doing so "
                "requires having a good definition of feature informativeness, "
                "or feature importance."
            )
        ) as tracker:
            self.play(Write(title_full), run_time=1.5)
            self.wait(5.5)
            self.play(Transform(title_full, title_short), run_time=1.0)
            self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.8)
            self.play(Create(funnel), run_time=1.0)
            self.play(FadeIn(features, shift=RIGHT * 0.2), run_time=1.0)
            selected_count = 0
            for i, feat in enumerate(features):
                self.play(feat.animate.move_to(exit_point), run_time=0.3)
                if pass_mask[i]:
                    check = self.scene6_check_icon(color=SELECTED_COLOR).move_to(icon_spot)
                    target = selected_area_center + selected_slots[selected_count]
                    selected_count += 1
                    self.play(FadeIn(check, scale=0.6), feat.animate.set_color(SELECTED_COLOR), run_time=0.3)
                    self.play(feat.animate.move_to(target), FadeOut(check), run_time=0.35)
                else:
                    cross = Cross(stroke_color=REJECTED_COLOR, stroke_width=5, scale_factor=0.18).move_to(icon_spot)
                    self.play(FadeIn(cross, scale=0.6), feat.animate.set_color(REJECTED_COLOR), run_time=0.3)
                    self.play(FadeOut(cross), FadeOut(feat, shift=DOWN * 0.3), run_time=0.35)
            self.wait(tracker.get_remaining_duration())
        
        with self.voiceover(
            text=(
                "A number of importance measures are available: information "
                "gain, which is used by the decision tree algorithm; "
                "correlation between a feature and the outcome, where higher "
                "correlation indicates a more predictive feature; and the "
                "chi-squared statistic, which indicates a feature's ability to "
                "separate different outcome classes."
            )
        ) as tracker:
            bullets = VGroup(
                Text("• Information Gain / Gain Ratio", font_size=19),
                Text("• Correlation with Outcome", font_size=19),
                Text("• Chi-Squared Statistic", font_size=19),
            ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            bullets.next_to(below_funnel, LEFT, buff=0.3, aligned_edge=UP)
            self.wait(2.0)
            self.play(FadeIn(bullets[0], shift=UP * 0.1), run_time=1.0)
            self.wait(3.0)
            self.play(FadeIn(bullets[1], shift=UP * 0.1), run_time=1.0)
            self.wait(5.0)
            self.play(FadeIn(bullets[2], shift=UP * 0.1), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "After choosing an importance measure, we rank all features "
                "and pick the top K to build the predictive model."
            )
        ) as tracker:
            rank_title = Text("Ranked by Importance", font_size=18, color=YELLOW)
            heights = [0.8, 0.65, 0.55, 0.35, 0.2]
            bars = VGroup()
            for i, h in enumerate(heights):
                bar = Rectangle(width=0.32, height=h, color=SELECTED_COLOR if i < 3 else GREY_B, fill_opacity=0.8)
                bars.add(bar)
            bars.arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
            bars.next_to(rank_title, DOWN, buff=0.3)
            topk_label = Text("Top K", font_size=15, color=SELECTED_COLOR).next_to(
                VGroup(*bars[:3]), DOWN, buff=0.15
            )
            rank_group = VGroup(rank_title, bars, topk_label)
            rank_group.next_to(below_funnel, RIGHT, buff=0.3, aligned_edge=UP)
            self.play(FadeIn(rank_title), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), run_time=1.5)
            self.play(FadeIn(topk_label), run_time=0.6)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_06()
