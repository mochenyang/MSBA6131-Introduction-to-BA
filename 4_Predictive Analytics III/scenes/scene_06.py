import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import (
    Text,
    BETTER_COLOR,
    REGULAR_CLASSIFIER_COLOR,
    CURVE_C_COLOR,
    RANDOM_CLASSIFIER_COLOR,
    DATA_CURVE_COLOR,
    N_RECORDS,
    make_ranked_table,
    make_cutoff_line,
    predicted_labels_for_cutoff,
    make_unit_axes,
    make_illustrative_curves,
    compute_cum_response_points,
)


class Scene06Mixin:
    # ------------------------------------------------------------------
    # Scene 6: the cumulative response curve -- built the same way as the
    # ROC curve (same table, same cutoff-sweep mechanic), and compared
    # across models the same way (same illustrative-curves component)
    # ------------------------------------------------------------------
    def scene_06(self):
        title = Text("Cumulative Response Curve", font_size=30).to_edge(UP, buff=0.4)

        table = make_ranked_table()
        table["group"].move_to(LEFT * 4.3)

        cum_axes_data = make_unit_axes("% of Validation Data", "Cumulative\nResponse", x_length=4.2, y_length=3.9, x_max=1.08, y_max=1.08)
        cum_axes_data["group"].move_to(RIGHT * 3.0)
        axes = cum_axes_data["axes"]
        cum_points = compute_cum_response_points()

        # Cumulative response = recall rate of the positive class at the
        # cutoff -- revealed when the narration actually states that.
        recall_p_label = Text("Recall(p)", font_size=16, color=YELLOW).next_to(
            cum_axes_data["y_label"], DOWN, buff=0.15
        )

        with self.voiceover(
            text=(
                "Let's now turn to another model evaluation technique built "
                "on class probability predictions: the cumulative "
                "response curve. Like the R O C curve, the cumulative "
                "response curve is built from predicted class "
                "probabilities on a validation dataset, sorted from high to low. "
                "As we gradually move the cutoff threshold, more and more "
                "instances are predicted as the positive class. The "
                "x-axis of the curve is the percentage of validation "
                "data predicted as positive, and the y-axis is the "
                "cumulative response, which is the actual recall rate "
                "of the positive class at the given cutoff."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.wait(3.0)
            self.play(FadeIn(table["group"]), run_time=1.5)
            self.play(Create(cum_axes_data["group"]), run_time=1.8)
            self.wait(5.0)

            line = make_cutoff_line(table, 0)
            labels = predicted_labels_for_cutoff(table, 0)
            dot0 = Dot(axes.c2p(*cum_points[0]), radius=0.06, color=DATA_CURVE_COLOR)
            self.play(Create(line), *[FadeIn(l) for l in labels], FadeIn(dot0), run_time=1.3)

            dots = VGroup(dot0)
            segments = VGroup()
            for k in range(1, N_RECORDS + 1):
                new_line = make_cutoff_line(table, k)
                new_labels = predicted_labels_for_cutoff(table, k)
                new_dot = Dot(axes.c2p(*cum_points[k]), radius=0.06, color=DATA_CURVE_COLOR)
                segment = Line(dots[-1].get_center(), new_dot.get_center(), color=DATA_CURVE_COLOR, stroke_width=3.5)
                self.play(
                    Transform(line, new_line),
                    *[Transform(labels[i], new_labels[i]) for i in range(len(labels))],
                    Create(segment), FadeIn(new_dot),
                    run_time=0.9,
                )
                segments.add(segment)
                dots.add(new_dot)
                self.wait(0.75)
            self.wait(1.0)
            self.play(FadeIn(recall_p_label, shift=UP * 0.1), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        # Only the real curve fades here (it would otherwise overlap the
        # illustrative comparison curves drawn onto this same axes below).
        # The table/cutoff-line/labels stay on screen through the model-
        # comparison block too -- they're the worked example this scene
        # keeps referring back to -- and fade out only in the final
        # cleanup at the very end of the scene.
        self.play(
            FadeOut(VGroup(segments, dots)),
            run_time=1.0,
        )

        # common.make_illustrative_curves' curve "a" is a right-angle
        # (0,0)->(0,1)->(1,1) shape -- a valid ROC curve (a classifier can
        # rank every positive above every negative, hitting TPR=1 at
        # FPR=0), but not a valid cumulative response curve: reaching
        # cumulative response 1 at x=0 would mean finding every positive
        # instance while reviewing 0% of the data, which is impossible.
        # So this scene skips curve "a" entirely (never Create'd/FadeIn'd
        # below) and relabels b/c/d as A/B/C locally -- common.py itself
        # is untouched, since scene_04 and scene_05 both still need the
        # full A-D set for the ROC comparison, where curve A is valid.
        illustrative = make_illustrative_curves(axes)
        label_a = Text("A", font_size=18, color=REGULAR_CLASSIFIER_COLOR).move_to(illustrative["labels"]["b"].get_center())
        label_b = Text("B", font_size=18, color=CURVE_C_COLOR).move_to(illustrative["labels"]["c"].get_center())
        label_c = Text("C", font_size=18, color=RANDOM_CLASSIFIER_COLOR).move_to(illustrative["labels"]["d"].get_center())

        arrow = Arrow(
            axes.c2p(0.5, 0.45), axes.c2p(0.1, 0.9), color=YELLOW, buff=0.1, stroke_width=3,
        )
        better_label = Text("better", font_size=16, color=YELLOW).next_to(arrow.get_end(), UP, buff=0.05)

        with self.voiceover(
            text=(
                "Just like the R O C curve, the cumulative response curve "
                "can also be used to compare multiple models. Every "
                "cumulative response curve starts at (0,0) and ends at "
                "one one, and the curve that sits closer to the top-left "
                "corner indicates a better classifier — it's able to "
                "\"catch\" more of the true positives within less of "
                "the data, meaning its probability predictions more "
                "effectively rank positive instances ahead of "
                "negative ones. The 45-degree diagonal line represents "
                "the random classifier, where class predictions are "
                "made by flipping a coin."
            )
        ) as tracker:
            self.wait(3.5)
            self.play(
                Create(illustrative["curves"]["b"]), FadeIn(label_a),
                Create(illustrative["curves"]["c"]), FadeIn(label_b),
                run_time=2.0,
            )
            self.wait(4.5)
            self.play(GrowArrow(arrow), FadeIn(better_label), run_time=1.2)
            self.wait(14.0)
            self.play(Create(illustrative["curves"]["d"]), FadeIn(label_c), run_time=1.3)
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash for scene_07 (reuses this exact cumulative response curve
        # for the lift-ratio worked example) and scene_08's summary.
        self.scene06_table = table
        self.scene06_axes_data = cum_axes_data
        self.scene06_cum_points = cum_points
        self.scene06_cum_curve = VGroup(segments, dots)

        # Everything still on screen fades out here, at the very end of the
        # scene -- the table/cutoff-line/labels included, since they stayed
        # up through the model-comparison block above. Not
        # illustrative["group"] -- it still contains curve "a" and its
        # original "B"/"C"/"D" labels, none of which were ever
        # Create'd/FadeIn'd above.
        self.play(
            FadeOut(title), FadeOut(table["group"]), FadeOut(line), *[FadeOut(l) for l in labels],
            FadeOut(cum_axes_data["group"]), FadeOut(recall_p_label),
            FadeOut(illustrative["curves"]["b"]), FadeOut(illustrative["curves"]["c"]), FadeOut(illustrative["curves"]["d"]),
            FadeOut(label_a), FadeOut(label_b), FadeOut(label_c),
            FadeOut(arrow), FadeOut(better_label),
        )


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_06()
