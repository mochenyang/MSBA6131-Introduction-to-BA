import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, NUMERIC_COLOR, ERROR_COLOR, GOOD_COLOR, HIGHLIGHT_COLOR


class Scene03Mixin:
    # ------------------------------------------------------------------
    # Scene 3: performance measures for numeric prediction
    # ------------------------------------------------------------------
    def scene_03(self):
        title = Text("Performance Measures for Numeric Prediction", font_size=26).to_edge(UP, buff=0.3)

        metric_words = ["Accuracy", "Precision", "Recall", "F-measure"]
        metric_texts = VGroup(*[Text(w, font_size=18) for w in metric_words]).arrange(RIGHT, buff=0.6)
        metric_texts.move_to(UP * 2.3)
        strike = Line(
            metric_texts.get_left() + LEFT * 0.15,
            metric_texts.get_right() + RIGHT * 0.15,
            color=ERROR_COLOR,
            stroke_width=4,
        )

        error_formula = MathTex("e_i = p_i - a_i", font_size=28)
        error_text = Text("Prediction Error = Prediction − Actual", font_size=15).next_to(
            error_formula, DOWN, buff=0.2
        )
        error_group = VGroup(error_formula, error_text).move_to(LEFT * 3.5 + UP * 1.1)

        number_line = NumberLine(x_range=[0, 10, 2], length=5.2, color=GREY_B).move_to(RIGHT * 3.0 + UP * 1.1)
        a_dot = Dot(number_line.n2p(4.0), color=NUMERIC_COLOR)
        p_dot = Dot(number_line.n2p(7.0), color=ERROR_COLOR)
        a_label = MathTex("a_i", font_size=22, color=NUMERIC_COLOR).next_to(a_dot, DOWN, buff=0.15)
        p_label = MathTex("p_i", font_size=22, color=ERROR_COLOR).next_to(p_dot, DOWN, buff=0.15)
        gap_ref = Line(a_dot.get_center(), p_dot.get_center())
        gap_brace = Brace(gap_ref, UP, color=HIGHLIGHT_COLOR)
        gap_label = gap_brace.get_tex("e_i").set_color(HIGHLIGHT_COLOR)

        mae = MathTex(r"\text{MAE} = \dfrac{1}{n}\sum_i |e_i|", font_size=24)
        mape = MathTex(
            r"\text{MAPE} = \dfrac{1}{n}\sum_i \left| \dfrac{e_i}{a_i} \right| \times 100\%", font_size=24
        )
        rmse = MathTex(r"\text{RMSE} = \sqrt{\dfrac{1}{n}\sum_i e_i^2}", font_size=24)
        sse = MathTex(r"\text{SSE} = \sum_i e_i^2", font_size=24)
        avg_err = MathTex(r"\text{Average Error} = \dfrac{1}{n}\sum_i e_i", font_size=24)
        # 2x2 grid for the first four metrics; average error sits centered in its own row below.
        metric_grid = VGroup(mae, mape, rmse, sse).arrange_in_grid(
            rows=2, cols=2, buff=(0.9, 0.55), col_alignments="ll"
        )
        formula_rows = VGroup(metric_grid, avg_err).arrange(DOWN, buff=0.55)
        if formula_rows.width > 11:
            formula_rows.scale_to_fit_width(11)
        formula_rows.move_to(DOWN * 1.25)

        mae_box = SurroundingRectangle(mae, color=GOOD_COLOR, buff=0.1)
        rmse_box = SurroundingRectangle(rmse, color=GOOD_COLOR, buff=0.1)
        common_tag_1 = Text("common", font_size=14, color=GOOD_COLOR).next_to(mae_box, UP, buff=0.08)
        common_tag_2 = Text("common", font_size=14, color=GOOD_COLOR).next_to(rmse_box, UP, buff=0.08)

        with self.voiceover(
            text=(
                "A major difference between numeric prediction and classification is "
                "performance measurement. Because we are no longer predicting "
                "categorical outcomes, the concepts of accuracy, precision, recall, "
                "and f-measure no longer apply. In numeric prediction, the goal is "
                "for the prediction to be as close to the true value as possible. "
                "Therefore, we define the prediction error to be the difference "
                "between prediction and the actual outcome. Based on prediction "
                "error, we can define a number of performance metrics, including "
                "mean absolute error, mean absolute percentage error, rooted mean "
                "squared error, total sum of squared error, and average error. "
                "Among them, RMSE and MAE are the most commonly used ones."
            )
        ) as tracker:
            self.play(Write(title), run_time=2.0)
            self.wait(4.0)
            self.play(FadeIn(metric_texts), run_time=1.0)
            self.wait(1.0)
            self.play(Create(strike), run_time=0.8)
            self.wait(5.4)
            self.play(Create(number_line), run_time=0.8)
            self.play(FadeIn(a_dot), FadeIn(p_dot), FadeIn(a_label), FadeIn(p_label), run_time=0.8)
            self.play(GrowFromCenter(gap_brace), FadeIn(gap_label), run_time=0.8)
            self.wait(3.6)
            self.play(FadeIn(error_group), run_time=1.2)
            self.wait(7.0)
            self.play(Write(mae), run_time=1.5)
            self.play(Write(mape), run_time=1.5)
            self.play(Write(rmse), run_time=1.5)
            self.play(Write(sse), run_time=1.5)
            self.play(Write(avg_err), run_time=1.5)
            self.wait(4.0)
            self.play(
                Create(mae_box), Create(rmse_box), FadeIn(common_tag_1), FadeIn(common_tag_2), run_time=1.5
            )
            self.wait(max(tracker.get_remaining_duration(), 0.05))

        cancel_line = NumberLine(x_range=[-3, 3, 1], length=4.4, include_numbers=False, color=GREY_B).move_to(
            DOWN * 3.0
        )
        pos_dot = Dot(cancel_line.n2p(2), color=GOOD_COLOR)
        neg_dot = Dot(cancel_line.n2p(-2), color=ERROR_COLOR)
        pos_label = MathTex("+e", font_size=20, color=GOOD_COLOR).next_to(pos_dot, UP, buff=0.1)
        neg_label = MathTex("-e", font_size=20, color=ERROR_COLOR).next_to(neg_dot, UP, buff=0.1)
        zero_target = Dot(cancel_line.n2p(0), radius=0.001)
        cancel_caption = Text("cancels out -> uninformative", font_size=16, color=ERROR_COLOR).next_to(
            cancel_line, DOWN, buff=0.3
        )

        with self.voiceover(
            text=(
                "Notice that average error is typically not an informative "
                "performance measure, because positive error can cancel out with "
                "negative error. Therefore, a small average error does not mean "
                "that the model is more accurate in its predictions. This is also "
                "why all the other performance metrics either take the absolute "
                "value or the square of the error, so that error direction does "
                "not matter anymore."
            )
        ) as tracker:
            self.play(Circumscribe(avg_err, color=HIGHLIGHT_COLOR), run_time=1.5)
            self.play(Create(cancel_line), run_time=1.0)
            self.play(FadeIn(pos_dot), FadeIn(neg_dot), FadeIn(pos_label), FadeIn(neg_label), run_time=1.0)
            self.wait(3.0)
            self.play(
                pos_dot.animate.move_to(zero_target), neg_dot.animate.move_to(zero_target),
                FadeOut(pos_label), FadeOut(neg_label),
                run_time=1.5,
            )
            self.play(FadeOut(pos_dot), FadeOut(neg_dot), run_time=0.4)
            self.play(FadeIn(cancel_caption), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(metric_texts), FadeOut(strike), FadeOut(error_group),
            FadeOut(number_line), FadeOut(a_dot), FadeOut(p_dot), FadeOut(a_label), FadeOut(p_label),
            FadeOut(gap_brace), FadeOut(gap_label), FadeOut(formula_rows),
            FadeOut(mae_box), FadeOut(rmse_box), FadeOut(common_tag_1), FadeOut(common_tag_2),
            FadeOut(cancel_line), FadeOut(cancel_caption),
        )


class Scene03(VoiceoverScene, Scene03Mixin):
    """Standalone preview: manim -pql scene_03.py Scene03"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_03()
