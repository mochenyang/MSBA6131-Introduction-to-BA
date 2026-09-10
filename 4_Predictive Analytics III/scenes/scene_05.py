import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    POS_COLOR,
    NEG_COLOR,
    HIGHLIGHT_COLOR,
    DATA_CURVE_COLOR,
    PERFECT_CLASSIFIER_COLOR,
    REGULAR_CLASSIFIER_COLOR,
    N_RECORDS,
    NUM_POS,
    NUM_NEG,
    RANKED_DATA,
    confusion_counts,
    compute_roc_points,
    make_ranked_table,
    make_cutoff_line,
    make_unit_axes,
)
from scene_04 import Scene04Mixin


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: the intuition behind why ROC position and AUC both track
    # model performance -- the "movement game" and the grid-cell count
    # ------------------------------------------------------------------
    @staticmethod
    def scene5_grid_lines(axes):
        lines = VGroup()
        for i in range(1, NUM_NEG):
            x = i / NUM_NEG
            lines.add(Line(axes.c2p(x, 0), axes.c2p(x, 1), color=GREY_D, stroke_width=1, stroke_opacity=0.6))
        for j in range(1, NUM_POS):
            y = j / NUM_POS
            lines.add(Line(axes.c2p(0, y), axes.c2p(1, y), color=GREY_D, stroke_width=1, stroke_opacity=0.6))
        return lines

    @staticmethod
    def scene5_shaded_cell(axes, tp_before, fp_before):
        """The grid cells to the right of an 'up' move: this positive
        instance out-ranked every negative not yet crossed (NUM_NEG minus
        fp_before of them)."""
        y0, y1 = tp_before / NUM_POS, (tp_before + 1) / NUM_POS
        x0, x1 = fp_before / NUM_NEG, 1.0
        rect = Polygon(
            axes.c2p(x0, y0), axes.c2p(x1, y0), axes.c2p(x1, y1), axes.c2p(x0, y1),
            color=DATA_CURVE_COLOR, fill_color=DATA_CURVE_COLOR, fill_opacity=0.35, stroke_width=1,
        )
        return rect

    def scene_05(self):
        title = Text("ROC and AUC: Intuitive Understanding", font_size=26).to_edge(UP, buff=0.4)
        table = self.scene03_table
        axes_data = self.scene03_axes_data
        axes = axes_data["axes"]
        roc_points = compute_roc_points()

        with self.voiceover(
            text=(
                "At this point, it is worth pausing to ask the question "
                "of \"WHY\". Why can we look at the positions of the ROC "
                "curve to infer model performance, and why is the area "
                "under the ROC curve also associated with performance? "
                "Here's a useful way to think about ROC and AUC that "
                "will give you more intuition."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.0)
            self.wait(3.0)
            self.play(FadeIn(table["group"]), FadeIn(axes_data["group"]), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Remember how we built the ROC curve: sweeping down the "
                "ranked validation data points from highest predicted "
                "probability to lowest. Pay attention to the movements "
                "of the ROC curve, it moves up on every positive "
                "instance and moves right on every negative instance. "
                "This is expected, because moving cutoff below a "
                "positive instance would lead to one more true positive "
                "prediction, whereas moving cutoff below a negative "
                "instance would lead to one more false positive "
                "prediction."
            )
        ) as tracker:
            line = make_cutoff_line(table, 0)
            dot0 = Dot(axes.c2p(*roc_points[0]), radius=0.06, color=DATA_CURVE_COLOR)
            self.play(Create(line), FadeIn(dot0), run_time=1.2)

            dots = VGroup(dot0)
            segments = VGroup()
            for k in range(1, N_RECORDS + 1):
                row = table["rows"][k - 1]
                is_pos = row["class"] == "P"
                move_word = "up" if is_pos else "right"
                move_color = POS_COLOR if is_pos else NEG_COLOR
                box = SurroundingRectangle(row["actual"], color=move_color, buff=0.05, stroke_width=2.5)
                move_label = Text(move_word, font_size=14, color=move_color).next_to(box, RIGHT, buff=0.15)
                new_line = make_cutoff_line(table, k)
                new_dot = Dot(axes.c2p(*roc_points[k]), radius=0.06, color=DATA_CURVE_COLOR)
                segment = Line(dots[-1].get_center(), new_dot.get_center(), color=DATA_CURVE_COLOR, stroke_width=3.5)
                beat = 1.3 if k <= 2 else 0.7
                self.play(Create(box), FadeIn(move_label), Transform(line, new_line), run_time=beat * 0.5)
                self.play(Create(segment), FadeIn(new_dot), FadeOut(box), FadeOut(move_label), run_time=beat * 0.5)
                segments.add(segment)
                dots.add(new_dot)
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(VGroup(table["group"], axes_data["group"], line, segments, dots)), run_time=1.0)

        left_axes = self.scene04_left_axes
        illustrative = self.scene04_illustrative

        with self.voiceover(
            text=(
                "This explains why an ROC curve positioned closer to "
                "the top-left corner indicates a better model. "
                "Intuitively, being closer to the top-left corner means "
                "the curve can go up for more steps before having to go "
                "right, which implies that it correctly ranks more "
                "positive instances ahead of negative instances based "
                "on probability predictions. If the ROC curve goes up "
                "all the way and then go right, it means that the model "
                "correctly ranks all positive instances ahead of "
                "negative ones, indicating a perfect classifier."
            )
        ) as tracker:
            self.play(FadeIn(left_axes["group"]), FadeIn(illustrative["group"]), run_time=1.3)
            self.wait(2.0)
            self.play(
                Circumscribe(VGroup(illustrative["curves"]["b"], illustrative["labels"]["b"]), color=REGULAR_CLASSIFIER_COLOR),
                run_time=2.0,
            )
            self.wait(3.5)
            self.play(
                Circumscribe(VGroup(illustrative["curves"]["a"], illustrative["labels"]["a"]), color=PERFECT_CLASSIFIER_COLOR),
                run_time=2.0,
            )
            self.wait(tracker.get_remaining_duration())

        self.play(FadeOut(left_axes["group"]), FadeOut(illustrative["group"]), run_time=1.0)

        with self.voiceover(
            text=(
                "Now, to understand what exactly AUC measures, imagine "
                "the space under the curve as a grid, with one column "
                "for every negative instance and one row for every "
                "positive instance. Every time the curve moves \"up\", "
                "it corresponds to a positive instance, and all the "
                "\"right turns\" to the right of this \"up turn\" "
                "correspond to the negative instances that have "
                "received lower probability predictions than the focal "
                "positive instance. So the shaded area under the curve "
                "is literally counting, across all positive-negative "
                "pairs, how often the positive instance scored higher "
                "than the negative one. Divide that count by the total "
                "number of pairs, and you get exactly the AUC. That's "
                "why AUC has such a clean interpretation: given one "
                "randomly chosen instance from class p and one from "
                "class n, call them X_1 and X_2, and let p(X_1) and "
                "p(X_2) denote the predicted probability of each "
                "instance belonging to the p class. Then AUC is the "
                "probability that p(X_1) is bigger than p(X_2) — in "
                "other words, it measures how well the model ranks "
                "truly positive instances ahead of truly negative ones."
            )
        ) as tracker:
            self.play(FadeIn(table["group"]), FadeIn(axes_data["group"]), FadeIn(segments), FadeIn(dots), FadeIn(line), run_time=1.3)
            grid = self.scene5_grid_lines(axes)
            self.play(Create(grid), run_time=1.5)
            self.wait(1.0)

            shaded = VGroup()
            for k in range(N_RECORDS):
                tp_before, fp_before, _, _ = confusion_counts(k)
                cls, _ = RANKED_DATA[k]
                if cls == "P":
                    rect = self.scene5_shaded_cell(axes, tp_before, fp_before)
                    row_box = SurroundingRectangle(table["rows"][k]["actual"], color=HIGHLIGHT_COLOR, buff=0.05)
                    self.play(FadeIn(rect), Create(row_box), run_time=0.8)
                    self.play(FadeOut(row_box), run_time=0.3)
                    shaded.add(rect)
            self.wait(1.5)

            x1_def = Text("X₁ = random instance from class P", font_size=16, color=POS_COLOR)
            x2_def = Text("X₂ = random instance from class N", font_size=16, color=NEG_COLOR)
            defs = VGroup(x1_def, x2_def).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(DOWN * 2.9 + LEFT * 3.7)
            self.play(FadeIn(defs), run_time=1.3)

            formula = MathTex(
                r"AUC = \dfrac{\text{shaded cells}}{\text{total cells}} = P\big(p(X_1) > p(X_2)\big)",
                font_size=26,
            ).move_to(DOWN * 3.2 + RIGHT * 1.5)
            self.play(Write(formula), run_time=2.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(table["group"]), FadeOut(axes_data["group"]), FadeOut(segments), FadeOut(dots),
            FadeOut(line), FadeOut(grid), FadeOut(shaded), FadeOut(defs), FadeOut(formula),
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_03()
        self._fixture_scene_04()
        self.scene_05()

    def _fixture_scene_03(self):
        # Stand-in for scene_03's ranked table + ROC axes so scene_05 can be
        # previewed alone -- scene_05's own code re-sweeps the cutoff from
        # scratch, so no curve/cutoff-line state needs to be pre-built here.
        table = make_ranked_table()
        table["group"].move_to(LEFT * 4.3)
        axes_data = make_unit_axes("False Positive Rate", "True Positive Rate")
        axes_data["group"].scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.3)
        self.scene03_table = table
        self.scene03_axes_data = axes_data

    def _fixture_scene_04(self):
        # Stand-in for scene_04's three-curve (A, B, C) ROC comparison plot --
        # reuses scene_04's own curve builder so this preview always matches
        # the real hand-off instead of duplicating its construction.
        left_axes = make_unit_axes("FPR", "TPR", x_length=4.2, y_length=3.9, x_max=1.08, y_max=1.08)
        left_axes["group"].scale(0.85).move_to(LEFT * 3.6 + DOWN * 0.4)
        illustrative = Scene04Mixin.scene4_illustrative_curves(left_axes["axes"])
        self.scene04_left_axes = left_axes
        self.scene04_illustrative = illustrative
