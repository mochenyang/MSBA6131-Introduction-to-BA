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
    CURVE_A_COLOR,
    CURVE_D_COLOR,
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

        cum_axes_data = make_unit_axes("% of Data Predicted Positive", "Cumulative Response")
        cum_axes_data["group"].scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.3)
        axes = cum_axes_data["axes"]
        cum_points = compute_cum_response_points()

        with self.voiceover(
            text=(
                "Let's turn to another model evaluation technique built "
                "on class probability predictions: the cumulative "
                "response curve. Like the ROC curve, the cumulative "
                "response curve is built from predicted class "
                "probabilities on a validation dataset. We first sort "
                "the data by predicted probability of being in the "
                "positive class, from high to low. Then, as we "
                "gradually move the cutoff threshold, more and more "
                "instances are predicted as the positive class. The "
                "x-axis of the curve is the percentage of validation "
                "data predicted as positive, and the y-axis is the "
                "cumulative response, which is the actual recall rate "
                "of the positive class at the given cutoff."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(table["group"]), run_time=1.5)
            self.play(Create(cum_axes_data["group"]), run_time=1.8)
            self.wait(1.5)

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
            self.wait(tracker.get_remaining_duration())

        illustrative = make_illustrative_curves(axes)
        best_tag = Text("best", font_size=15, color=CURVE_A_COLOR).next_to(illustrative["labels"]["a"], UP, buff=0.05)
        random_tag = Text("random classifier", font_size=14, color=CURVE_D_COLOR).next_to(
            illustrative["curves"]["d"], DOWN, buff=0.15
        )
        arrow = Arrow(
            axes.c2p(0.5, 0.45), axes.c2p(0.1, 0.9), color=BETTER_COLOR, buff=0.1, stroke_width=3,
        )
        better_label = Text("better", font_size=16, color=BETTER_COLOR).next_to(arrow.get_end(), UP, buff=0.05)

        with self.voiceover(
            text=(
                "Just like the ROC curve, the cumulative response curve "
                "can also be used to compare multiple models. Every "
                "cumulative response curve starts at (0,0) and ends at "
                "(1,1), and the curve that sits closer to the top-left "
                "corner indicates a better classifier — it's able to "
                "\"catch\" more of the true positives within less of "
                "the data, meaning its probability predictions are more "
                "effectively ranking positive instances ahead of "
                "negative ones. The diagonal, 45-degree line represents "
                "the random classifier, where class predictions are "
                "made by flipping a coin."
            )
        ) as tracker:
            self.play(
                Create(illustrative["curves"]["a"]), FadeIn(illustrative["labels"]["a"]),
                Create(illustrative["curves"]["b"]), FadeIn(illustrative["labels"]["b"]),
                Create(illustrative["curves"]["c"]), FadeIn(illustrative["labels"]["c"]),
                run_time=1.8,
            )
            self.wait(2.0)
            self.play(FadeIn(best_tag), run_time=1.0)
            self.wait(2.0)
            self.play(Create(illustrative["curves"]["d"]), FadeIn(illustrative["labels"]["d"]), run_time=1.3)
            self.play(FadeIn(random_tag), run_time=1.0)
            self.wait(1.0)
            self.play(GrowArrow(arrow), FadeIn(better_label), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash for scene_07 (reuses this exact cumulative response curve
        # for the lift-ratio worked example) and scene_08's summary.
        self.scene06_table = table
        self.scene06_axes_data = cum_axes_data
        self.scene06_cum_points = cum_points
        self.scene06_cum_curve = VGroup(segments, dots)

        self.play(
            FadeOut(title), FadeOut(table["group"]), FadeOut(cum_axes_data["group"]), FadeOut(line),
            *[FadeOut(l) for l in labels], FadeOut(self.scene06_cum_curve),
            FadeOut(illustrative["group"]), FadeOut(best_tag), FadeOut(random_tag),
            FadeOut(arrow), FadeOut(better_label),
        )


class Scene06(VoiceoverScene, Scene06Mixin):
    """Standalone preview: manim -pql scene_06.py Scene06"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_06()
