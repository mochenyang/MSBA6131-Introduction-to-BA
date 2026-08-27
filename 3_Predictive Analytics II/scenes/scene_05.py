import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import Text, make_bayes_formula, annotate_bayes_formula


class Scene05Mixin:
    # ------------------------------------------------------------------
    # Scene 5: Bayes' theorem applied to classification
    # ------------------------------------------------------------------
    def scene5_highlight(self, term, label, all_terms):
        others = [t for t in all_terms if t is not term]
        self.play(
            *[t.animate.set_opacity(0.35) for t in others],
            term.animate.set_color(YELLOW),
            FadeIn(label),
            run_time=1.2,
        )

    def scene_05(self):
        title = Text("Naive Bayes: Bayes' Theorem for Classification", font_size=28).to_edge(UP, buff=0.4)

        parts = make_bayes_formula()
        # Scale/move the *whole* formula, labels included -- the labels were
        # positioned via next_to() against the terms' pre-transform spots, so
        # scaling/moving parts["group"] alone (which doesn't contain the
        # labels) would leave them stranded at their old coordinates once
        # FadeIn'd later, instead of tracking the terms they're supposed to
        # label.
        parts_everything = VGroup(
            parts["group"], parts["posterior_label"], parts["likelihood_label"],
            parts["prior_label"], parts["evidence_label"],
        )
        parts_everything.scale(1.3).move_to(UP * 0.8)

        with self.voiceover(
            text=(
                "Now back to the classification task. We want the "
                "conditional probability of being in class Ci given the "
                "features X."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.8)
            self.play(FadeIn(parts["posterior"]), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "Bayes' theorem lets us express that as the conditional "
                "probability of observing features X given class Ci, "
                "multiplied by the unconditional probability of being in "
                "class Ci, divided by the unconditional probability of "
                "observing X."
            )
        ) as tracker:
            self.play(FadeIn(parts["equals"]), run_time=0.8)
            self.play(FadeIn(parts["likelihood"]), run_time=1.2)
            self.play(FadeIn(parts["times"]), FadeIn(parts["prior"]), run_time=1.2)
            self.play(Create(parts["frac_line"]), FadeIn(parts["evidence"]), run_time=1.2)
            self.wait(tracker.get_remaining_duration())

        all_terms = [parts["posterior"], parts["likelihood"], parts["prior"], parts["evidence"]]

        with self.voiceover(
            text=(
                "The probability of Ci given X is the posterior probability. "
                "The probability of X given Ci is the likelihood. And the "
                "unconditional probability of Ci is the prior probability. "
            )
        ) as tracker:
            self.wait(2.0)
            self.scene5_highlight(parts["posterior"], parts["posterior_label"], all_terms)
            self.wait(2.4)
            self.scene5_highlight(parts["likelihood"], parts["likelihood_label"], all_terms)
            self.wait(2.0)
            self.scene5_highlight(parts["prior"], parts["prior_label"], all_terms)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "The prior describes what we know about the class "
                "distribution before seeing any specific data point; the "
                "likelihood describes how likely it is to observe a data "
                "point like X given a particular class; together they "
                "combine into the posterior, the class probability "
                "conditional on the data."
            )
        ) as tracker:
            self.play(
                *[t.animate.set_opacity(1).set_color(WHITE) for t in all_terms],
                run_time=1.0,
            )
            self.play(Indicate(parts["prior_label"], color=YELLOW, scale_factor=1.2), run_time=1.0)
            self.wait(4.4)
            self.play(Indicate(parts["likelihood_label"], color=YELLOW, scale_factor=1.2), run_time=1.0)
            self.wait(7.0)
            self.play(Indicate(parts["posterior_label"], color=YELLOW, scale_factor=1.2), run_time=1.0)
            self.wait(tracker.get_remaining_duration())

        annot = annotate_bayes_formula(parts)
        goal_statement = MathTex(
            "\\text{Goal: find } C^{*} \\text{ that has the highest } P(C^{*} \\mid X)"
        ).scale(0.85).move_to(DOWN * 2.3)

        with self.voiceover(
            text=(
                "Going back to the classification task, our goal is to find "
                "the class that maximizes the posterior probability — which "
                "is the same as maximizing the product of likelihood and "
                "prior. Notice we don't need the denominator, the "
                "probability of observing X, at all: its value is the same "
                "constant regardless of which class we're considering, so we "
                "don't need to calculate it."
            )
        ) as tracker:
            self.wait(2.0)
            self.play(FadeIn(goal_statement, shift=UP * 0.15), run_time=1.3)
            self.wait(2.0)
            self.play(Create(annot["box"]), FadeIn(annot["maximize_label"]), run_time=1.5)
            self.wait(3.0)
            self.play(
                parts["evidence"].animate.set_color(GREY_B),
                Create(annot["cross"]),
                FadeIn(annot["ignore_label"]),
                run_time=1.8,
            )            
            self.wait(tracker.get_remaining_duration())

        self.wait()

        # Stash the formula parts (not their on-screen state) for scene_06,
        # which does its own fresh reveal rather than inheriting a leftover
        # -- so everything here fades out, leaving a clean scene.
        self.bayes_formula_parts = parts

        self.play(
            FadeOut(title),
            FadeOut(VGroup(parts["posterior_label"], parts["likelihood_label"], parts["prior_label"])),
            FadeOut(annot["ignore_label"]), FadeOut(annot["maximize_label"]), FadeOut(goal_statement),
            FadeOut(parts["group"]), FadeOut(annot["box"]), FadeOut(annot["cross"]),
        )


class Scene05(VoiceoverScene, Scene05Mixin):
    """Standalone preview: manim -pql scene_05.py Scene05"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_05()
