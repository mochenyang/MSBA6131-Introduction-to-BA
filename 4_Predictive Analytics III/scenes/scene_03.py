import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    DATA_CURVE_COLOR,
    N_RECORDS,
    make_ranked_table,
    make_cutoff_line,
    predicted_labels_for_cutoff,
    make_unit_axes,
    compute_roc_points,
)


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: sliding the cutoff generates a family of confusion
    # matrices, which trace out the ROC curve
    # ------------------------------------------------------------------
    @staticmethod
    def scene3_fpr_tpr_readout(fpr, tpr, font_size=22):
        fpr_text = Text(f"FPR = {fpr:.2f}", font_size=font_size, color=DATA_CURVE_COLOR)
        tpr_text = Text(f"TPR = {tpr:.2f}", font_size=font_size, color=DATA_CURVE_COLOR)
        return VGroup(fpr_text, tpr_text).arrange(RIGHT, buff=0.5)

    def scene_03(self):
        title = Text("The Receiver Operating Characteristic (ROC) Curve", font_size=32).to_edge(UP, buff=0.4)
        subtitle = Text(
            "A visualization of model performance as cutoff changes", font_size=18, color=GREY_B
        ).next_to(title, DOWN, buff=0.15)
        table = self.scene02_table
        table["group"].move_to(LEFT * 4.3)

        with self.voiceover(
            text=(
                "By picking different cutoff values, we can generate "
                "multiple sets of classification results for the same "
                "classifier, which reveals useful information about the "
                "classifier's quality. The Receiver Operating Characteristic curve, "
                "or R O C curve in short, is an important tool to visualize such information. "
                "Let's demonstrate it using the same 10 data points."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.0)
            self.wait(1.0)
            self.play(FadeIn(subtitle), run_time=2.0)
            self.wait(14.0)
            self.play(FadeIn(table["group"]), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # Bigger than the shared default -- with the confusion matrix gone,
        # the whole right half is free for the ROC plot alone. The axis
        # range extends slightly past 1.0 (rather than stopping exactly at
        # it) so the "1.0" tick and the (1,1) corner both sit clear of the
        # arrowhead instead of crowding it.
        axes_data = make_unit_axes(
            # Wrapped onto two lines -- as one line "True Positive Rate" was
            # wide enough to push the whole axes group further right than
            # it needed to be, eating into the gap next to the table.
            "False Positive Rate (FPR)", "True Positive\nRate (TPR)", x_length=5.4, y_length=4.4, x_max=1.08, y_max=1.08,
        )
        axes_data["group"].move_to(RIGHT * 2.8 + DOWN * 0.4)

        # Definitions of TPR/FPR in terms of recall -- revealed only when
        # the narration actually states them (see the wait()s timed against
        # vo_timing.py estimates below), not shown up front with the axes.
        recall_p_label = Text("Recall(p)", font_size=16, color=YELLOW).next_to(
            axes_data["y_label"], DOWN, buff=0.15
        )
        one_minus_recall_n_label = Text("1 - Recall(n)", font_size=16, color=YELLOW).next_to(
            axes_data["x_label"], DOWN, buff=0.15
        )

        roc_points = compute_roc_points()
        axes = axes_data["axes"]

        with self.voiceover(
            text=(
                "Specifically, the R O C curve plots the true positive "
                "rate against the false positive rate as the cutoff "
                "changes. The true positive rate is the same as the "
                "recall of class p, and the false positive rate is one "
                "minus the recall of class n."
            )
        ) as tracker:
            self.play(Create(axes_data["group"]), run_time=4.0)
            self.wait(3.0)  # "...as the cutoff changes."
            self.play(FadeIn(recall_p_label, shift=UP * 0.1), run_time=0.8)  # "...recall of class p,"
            self.wait(4.8)
            self.play(FadeIn(one_minus_recall_n_label, shift=UP * 0.1), run_time=0.8)  # "...recall of class n."
            self.wait(tracker.get_remaining_duration())
            
        with self.voiceover(
            text=(
                "When cutoff value is the "
                "highest, all 10 records are predicted as negative. "
                "This amounts to 0% recall of positive and 100% recall "
                "of negative, corresponding to (0,0) on the R O C curve. "
                "As we move the cutoff down a notch, the first record "
                "is predicted as positive, producing 1/6 recall of "
                "positive while maintaining recall of negative at 1. "
                "This corresponds to (0, 1/6) on the R O C curve. This "
                "process continues until the cutoff moves below the "
                "smallest probability prediction, and all records are "
                "predicted as positive."
            )
        ) as tracker:
            line = make_cutoff_line(table, 0)
            labels = predicted_labels_for_cutoff(table, 0)
            dot = Dot(axes.c2p(*roc_points[0]), radius=0.06, color=DATA_CURVE_COLOR)
            # Sits just above the plot's top edge -- inside the headroom the
            # extended axis range (x_max/y_max = 1.08) opens up -- so it
            # reads as part of the ROC panel without permanently sitting on
            # top of the curve itself, which eventually reaches TPR = 1.
            readout = self.scene3_fpr_tpr_readout(*roc_points[0])
            readout.move_to(axes.c2p(0.5, 1.0) + UP * 0.35)
            self.play(
                Create(line), *[FadeIn(l) for l in labels], FadeIn(dot), FadeIn(readout),
                run_time=1.8,
            )
            # Timed against the real cached-clip timestamps (vo_timing.py
            # mark), not guessed: "As we move the cutoff down a notch"
            # starts ~13.05s into this block.
            self.wait(11.25)  # "...on the R O C curve." (the (0,0) description)

            # Singled out, not folded into the loop below -- this is the one
            # transition the narration actually describes step by step, so
            # it gets its own slower sequence of beats, one per clause,
            # instead of a single lumped animation.
            new_line = make_cutoff_line(table, 1)
            new_labels = predicted_labels_for_cutoff(table, 1)
            new_dot = Dot(axes.c2p(*roc_points[1]), radius=0.06, color=DATA_CURVE_COLOR)
            segment = Line(dot.get_center(), new_dot.get_center(), color=DATA_CURVE_COLOR, stroke_width=3.5)
            new_readout = self.scene3_fpr_tpr_readout(*roc_points[1])
            new_readout.move_to(readout.get_center())

            self.play(Transform(line, new_line), run_time=1.5)  # "As we move the cutoff down a notch,"
            self.wait(1.0)
            self.play(Transform(labels[0], new_labels[0]), run_time=1.0)  # "the first record is predicted as positive,"
            self.wait(0.5)
            self.play(Transform(readout, new_readout), run_time=1.5)  # "producing 1/6 recall of positive"  
            self.wait(1.0)
            self.play(Create(segment), FadeIn(new_dot), run_time=1.5)  # "while maintaining recall of negative at 1."
            self.wait(0.95)
            self.play(Indicate(new_dot, color=YELLOW), run_time=1.5)  # "This corresponds to (0, 1/6) on the R O C curve."
            self.wait(2.5)  # -> ~27.6s, right as "This process continues..." begins

            # k=2 onward: the rest of the sweep, played during the final,
            # summarizing sentence ("this process continues until...") --
            # fast, since the narration no longer calls out each step.
            segments = VGroup(segment)
            dots = VGroup(dot, new_dot)
            for k in range(2, N_RECORDS + 1):
                new_line = make_cutoff_line(table, k)
                new_labels = predicted_labels_for_cutoff(table, k)
                new_dot = Dot(axes.c2p(*roc_points[k]), radius=0.06, color=DATA_CURVE_COLOR)
                segment = Line(dots[-1].get_center(), new_dot.get_center(), color=DATA_CURVE_COLOR, stroke_width=3.5)
                new_readout = self.scene3_fpr_tpr_readout(*roc_points[k])
                new_readout.move_to(readout.get_center())
                self.play(
                    Transform(line, new_line),
                    *[Transform(labels[i], new_labels[i]) for i in range(len(labels))],
                    Transform(readout, new_readout),
                    Create(segment), FadeIn(new_dot),
                    run_time=0.75,
                )
                segments.add(segment)
                dots.add(new_dot)
            # The choreographed beats above slightly overrun this block's
            # cached narration clip, so get_remaining_duration() can clamp to
            # exactly 0 -- guard with a small floor since Manim's wait()
            # rejects a duration <= 0.
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash for scene_05 (reintroduces this exact ranked list + the
        # completed ROC curve) and scene_08 (shrunk summary snapshot).
        self.scene03_title = title
        self.scene03_table = table
        self.scene03_axes_data = axes_data
        self.scene03_roc_points = roc_points
        self.scene03_roc_curve = VGroup(segments, dots)
        self.scene03_cutoff_line = line
        self.scene03_pred_labels = labels

        # Faded out (not destroyed) so scene_05 can reintroduce the exact
        # same mobjects rather than rebuilding them.
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(table["group"]), FadeOut(axes_data["group"]),
            FadeOut(self.scene03_roc_curve), FadeOut(line), *[FadeOut(l) for l in labels], FadeOut(readout),
            FadeOut(recall_p_label), FadeOut(one_minus_recall_n_label),
        )


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self._fixture_scene_02()
        self.scene_03()

    def _fixture_scene_02(self):
        # Stand-in for scene_02's ranked table so scene_03 can be previewed
        # alone -- the predicted-label column is left blank since scene_03
        # immediately rebuilds it from cutoff k=0 anyway.
        # Not added to the scene here: scene_03's own code FadeIn's the
        # table itself as its first beat, same as the real scene_02 -> 03
        # hand-off.
        table = make_ranked_table()
        table["group"].move_to(LEFT * 4.3)
        self.scene02_table = table
