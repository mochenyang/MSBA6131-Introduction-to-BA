import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, SELECTED_COLOR, REJECTED_COLOR, CURRENT_COLOR


class Scene07Mixin:
    # ------------------------------------------------------------------
    # Scene 7: the wrapper approach -- forward selection and backward
    # elimination, illustrated side by side with the same X_1..X_5 set.
    # ------------------------------------------------------------------
    @staticmethod
    def scene7_feature_row(n=5, box_width=0.65, box_height=0.55):
        boxes, labels, group = [], [], VGroup()
        for i in range(n):
            box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.08, color=WHITE)
            label = MathTex(f"X_{i + 1}", font_size=24).move_to(box.get_center())
            one = VGroup(box, label)
            boxes.append(box)
            labels.append(label)
            group.add(one)
        group.arrange(RIGHT, buff=0.2)
        return {"group": group, "boxes": boxes, "labels": labels}

    def scene_07(self):
        title = Text("General-Purpose Feature Selection: Wrapper Approach", font_size=26).to_edge(UP, buff=0.4)
        subtitle = Text("Select features based on actual model performance", font_size=20, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.25)

        left_title = Text("Forward Selection", font_size=24, color=YELLOW)
        right_title = Text("Backward Elimination", font_size=24, color=YELLOW)
        left_title.move_to(LEFT * 3.4 + UP * 1.6)
        right_title.move_to(RIGHT * 3.4 + UP * 1.6)
        divider = Line(UP * 1.3, DOWN * 3.0, color=GREY_D, stroke_width=1.5)

        fwd = self.scene7_feature_row()
        fwd["group"].scale(0.85).next_to(left_title, DOWN, buff=0.5)
        bwd = self.scene7_feature_row()
        bwd["group"].scale(0.85).next_to(right_title, DOWN, buff=0.5)

        with self.voiceover(
            text=(
                "Compared to the filter approach, the wrapper approach relies "
                "on the performance of actual models to determine which "
                "features to use. There are two standard wrapper approaches: "
                "forward selection and backward elimination. The idea behind "
                "them is the same, except they work in opposite directions."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.3)
            self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.8)
            self.wait(5.0)
            self.play(Create(divider), run_time=0.6)
            self.play(FadeIn(left_title), run_time=1.0)
            self.play(FadeIn(right_title), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        round_label_pos = fwd["group"].get_bottom() + DOWN * 0.55 + LEFT * 0.5

        # ---------------- Forward selection ---------------------------------
        with self.voiceover(
            text=(
                "Forward selection starts with a single feature and adds one "
                "more feature at a time until performance stops improving. "
                "More specifically, say the set of all features is X_1 through "
                "X_5. Under forward selection, we start by using each single "
                "feature on its own to build a model, and select whichever "
                "feature produces the best-performing model."
            )
        ) as tracker:
            self.wait(5.0)
            self.play(FadeIn(fwd["group"], shift=DOWN * 0.15), run_time=1.0)
            self.wait(5.0)
            for box in fwd["boxes"]:
                self.play(Indicate(box, color=CURRENT_COLOR), run_time=1.0)
            self.play(fwd["boxes"][2].animate.set_color(SELECTED_COLOR), run_time=0.5)
            fwd_round_label1 = VGroup(
                Text("Round 1: ", font_size=17, color=CURRENT_COLOR),
                MathTex("X_3", font_size=22, color=CURRENT_COLOR),
                Text(" selected", font_size=17, color=CURRENT_COLOR),
            ).arrange(RIGHT, buff=0.08)
            fwd_round_label1.move_to(round_label_pos)
            self.play(FadeIn(fwd_round_label1), run_time=0.6)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Next, we use that selected feature together with each of the "
                "other remaining features, one at a time, to build a model, "
                "and keep whichever combination performs best."
            )
        ) as tracker:
            others = [0, 1, 3, 4]
            for j in others:
                self.play(Indicate(fwd["boxes"][j], color=CURRENT_COLOR), run_time=1.0)
            self.play(fwd["boxes"][0].animate.set_color(SELECTED_COLOR), run_time=0.5)
            fwd_round_label2 = VGroup(
                Text("Round 2: ", font_size=17, color=CURRENT_COLOR),
                MathTex(r"\{X_3, X_1\}", font_size=22, color=CURRENT_COLOR),
                Text(" selected", font_size=17, color=CURRENT_COLOR),
            ).arrange(RIGHT, buff=0.08)
            fwd_round_label2.next_to(fwd_round_label1, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(FadeIn(fwd_round_label2), run_time=0.6)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "We repeat this process, adding one feature at a time, until "
                "performance no longer improves."
            )
        ) as tracker:
            fwd_round_label3 = Text("Repeat until performance does not improve", font_size=16, color=CURRENT_COLOR)
            fwd_round_label3.next_to(fwd_round_label2, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(FadeIn(fwd_round_label3), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        # ---------------- Backward elimination -------------------------------
        bwd_round_pos = bwd["group"].get_bottom() + DOWN * 0.55 + LEFT * 0.5
        with self.voiceover(
            text=(
                "In backward elimination, we go the oppposite way. "
                "We start with all the features, then try dropping each "
                "feature one at a time and rebuilding the model, eliminating "
                "whichever feature's removal results in the best performance "
                "improvement."
            )
        ) as tracker:
            bwd_round_label1 = Text("Round 1: Full Model", font_size=17, color=CURRENT_COLOR).move_to(
                bwd_round_pos
            )
            self.play(FadeIn(bwd["group"], shift=DOWN * 0.15), run_time=1.0)
            self.wait(1.0)
            self.play(
                *[box.animate.set_color(SELECTED_COLOR) for box in bwd["boxes"]],
                run_time=1.0,
            )
            self.play(FadeIn(bwd_round_label1), run_time=0.6)
            for box in bwd["boxes"]:
                self.play(Indicate(box, color=CURRENT_COLOR), run_time=1.0)
            drop_cross = Cross(stroke_color=REJECTED_COLOR, stroke_width=5, scale_factor=0.22).move_to(
                bwd["boxes"][1].get_center()
            )
            self.play(bwd["boxes"][1].animate.set_color(REJECTED_COLOR), FadeIn(drop_cross), run_time=0.6)
            bwd_round_label2 = VGroup(
                Text("Round 2: ", font_size=17, color=CURRENT_COLOR),
                MathTex("X_2", font_size=22, color=CURRENT_COLOR),
                Text(" dropped", font_size=17, color=CURRENT_COLOR),
            ).arrange(RIGHT, buff=0.08)
            bwd_round_label2.next_to(bwd_round_label1, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(FadeIn(bwd_round_label2), run_time=0.6)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "We again repeat this process, dropping one feature at a "
                "time, until performance no longer improves."
            )
        ) as tracker:
            bwd_round_label3 = Text("Repeat until performance does not improve", font_size=16, color=CURRENT_COLOR)
            bwd_round_label3.next_to(bwd_round_label2, DOWN, buff=0.15, aligned_edge=LEFT)
            self.play(FadeIn(bwd_round_label3), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


class Scene07(VoiceoverScene, Scene07Mixin):
    """Standalone preview: manim -pql scene_07.py Scene07"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_07()
