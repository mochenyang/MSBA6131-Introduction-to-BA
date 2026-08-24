import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_tree_node, make_tree_edge


class Scene10Mixin:
    # ------------------------------------------------------------------
    # Scene 10: recursive partitioning algorithm -- where to split (entropy
    # / information gain), when to stop (pre/post pruning)
    # ------------------------------------------------------------------
    def scene_10(self):
        title_part1 = Text("Building Decision Tree:", font_size=28)
        title_part2 = Text("Recursive Partitioning", font_size=28, color=YELLOW)
        title = VGroup(title_part1, title_part2).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.4)

        # Manim's Code mobject (pygments-backed) turned out to badly overlap
        # and drop lines in this version -- confirmed by rendering it alone,
        # so pseudocode is built from plain Text lines instead, with t2c for
        # lightweight keyword coloring instead of full syntax highlighting.
        # Text's bounding box crops to ink extents, so leading spaces carry no
        # width and aligned_edge=LEFT ignores them -- indentation is instead
        # applied as an explicit shift per line, after a flush-left arrange.
        keyword_color = PURPLE_B
        INDENT = 0.35
        line1 = VGroup(
            Text("pick attribute ", font_size=22),
            MathTex("X_i", font_size=28),
            Text(", split value ", font_size=22),
            MathTex("s_i", font_size=28),
        ).arrange(RIGHT, buff=0.06)
        code_lines = VGroup(
            Text("while True:", font_size=22, t2c={"while": keyword_color, "True": keyword_color}),
            line1,
            Text("split data into two parts", font_size=22),
            Text("if stopping criteria met:", font_size=22, t2c={"if": keyword_color}),
            Text("break", font_size=22, t2c={"break": keyword_color}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for line in code_lines[1:4]:
            line.shift(RIGHT * INDENT)
        code_lines[4].shift(RIGHT * INDENT * 2)
        code_box = SurroundingRectangle(code_lines, color=WHITE, buff=0.3, corner_radius=0.1)
        pseudocode = VGroup(code_box, code_lines).scale(0.85).move_to(LEFT * 3.6 + DOWN * 0.6)
        code_note = Text("No normalization needed (unlike k-NN)", font_size=16, color=GREY_B).next_to(
            pseudocode, DOWN, buff=0.35
        )

        # Timing keyed to the ~22.9s clip: "recursive partitioning" is named
        # early, but the algorithm box itself shouldn't appear until the
        # narration actually starts describing it ("In each round, we pick
        # one attribute...") -- each code line then reveals with its own
        # matching clause instead of the whole block dropping in at once.
        with self.voiceover(
            text=(
                "Let's now formalize the intuition into an algorithm for "
                "building a decision tree. It's called recursive partitioning. "
                "In each round, we pick one attribute Xi and a split value si. "
                "This divides the data into two portions: one where Xi is larger "
                "than si, and one where it's smaller. Then we repeat this "
                "process on each new portion, until we hit some stopping "
                "criterion."
            )
        ) as tracker:
            self.play(Write(title), run_time=1.5)
            self.wait(3.0)
            self.play(Indicate(title_part2, color=YELLOW), run_time=1.0)  # "recursive partitioning"
            self.wait(1.0)
            self.play(Create(code_box), run_time=0.8)
            self.play(Write(code_lines[0]), run_time=0.8)
            self.wait(2.0)
            self.play(Write(code_lines[1]), run_time=1.0)  # "pick one attribute Xi and a split value si"
            self.wait(1.3)
            self.play(Write(code_lines[2]), run_time=1.0)  # "divides the data into two portions"
            self.wait(5.4)
            self.play(Write(code_lines[3]), run_time=0.9)  # "until we hit some stopping criterion"
            self.play(Write(code_lines[4]), run_time=0.8)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "One side note: unlike k-NN, you don't need to normalize your "
                "data for decision trees, since we're not measuring distances "
                "between points -- just comparing single attribute values."
            )
        ) as tracker:
            self.wait(1.0)
            self.play(FadeIn(code_note, shift=UP * 0.1), run_time=2)
            self.wait(tracker.get_remaining_duration())

        # Built manually rather than via SurroundingRectangle -- same
        # .height/.width bug as stop_highlight below (content sits entirely
        # below y=0, so manim's max-reduction gets polluted to 0).
        split_buff = 0.08
        split_top = code_lines[1].get_top()[1]
        split_bottom = code_lines[1].get_bottom()[1]
        split_left = code_lines[1].get_left()[0]
        split_right = code_lines[1].get_right()[0]
        split_highlight = Rectangle(
            width=(split_right - split_left) + 2 * split_buff,
            height=(split_top - split_bottom) + 2 * split_buff,
            color=YELLOW,
        ).move_to([(split_left + split_right) / 2, (split_top + split_bottom) / 2, 0])
        goal_text = Text("Goal of split: create pure subsets", font_size=22, color=YELLOW).move_to(
            RIGHT * 3.6 + UP * 2.2
        )
        entropy_title = Text("Measure purity by Entropy", font_size=22, color=YELLOW).move_to(RIGHT * 3.6 + UP * 2.2)
        entropy_formula = MathTex(
            r"H(p) = -p\log_2 p - (1-p)\log_2(1-p)", font_size=30
        ).next_to(entropy_title, DOWN, buff=0.35)

        with self.voiceover(
            text=(
                "Now, where to split. The goal of each split is to make both "
                "resulting subsets as \"pure\" as possible -- meaning each "
                "subset contains mostly one class rather than a mix. "
                "One commonly used purity metric is entropy, or Shannon entropy, "
                "from information theory. Let p be the proportion of one class in a subset, "
                "Entropy, H(p), is a number between 0 and 1: the higher the value, the "
                "more the classes are \"mixed up.\""
            )
        ) as tracker:
            self.play(Create(split_highlight), run_time=1.0)
            self.play(FadeIn(goal_text), run_time=1.2)  # "goal of each split is..."
            self.wait(8.0)
            self.play(FadeOut(goal_text), Write(entropy_title), run_time=1.2)  # "purity metric is entropy..."
            self.wait(3.0)
            self.play(Write(entropy_formula), run_time=3.0)  # "let p be the proportion... H(p)..."
            self.wait(tracker.get_remaining_duration())

        entropy_max = Text("p = 0.5  →  H = 1  (perfectly mixed)", font_size=18, color=RED).next_to(
            entropy_formula, DOWN, buff=0.4
        )
        entropy_min = Text("p = 0 or 1  →  H = 0  (completely pure)", font_size=18, color=GREEN).next_to(
            entropy_max, DOWN, buff=0.25
        )

        with self.voiceover(
            text=(
                "When the two classes are perfectly balanced -- 50/50 -- entropy "
                "is at its highest, 1. When entropy is 0, the data contains only "
                "one class -- it's completely pure. So, smaller entropy means "
                "purer data."
            )
        ) as tracker:
            self.wait(1.5)
            self.play(FadeIn(entropy_max, shift=UP * 0.1), run_time=1.5)  # "entropy is at its highest, 1"
            self.wait(4.0)
            self.play(FadeIn(entropy_min, shift=UP * 0.1), run_time=1.5)  # "entropy is 0...completely pure"
            self.wait(tracker.get_remaining_duration())

        info_gain_title = Text("Information Gain", font_size=22, color=YELLOW).next_to(entropy_min, DOWN, buff=0.4)
        info_gain_formula = MathTex(
            r"\Delta H = H(\text{before split}) - H(\text{after split})", font_size=26
        ).next_to(info_gain_title, DOWN, buff=0.3)
        pick_split_line1 = VGroup(
            Text("Pick ", font_size=20),
            MathTex("X_i", font_size=24),
            Text(" and ", font_size=20),
            MathTex("s_i", font_size=24),
            Text(" that gives", font_size=20),
        ).arrange(RIGHT, buff=0.06)
        pick_split_line2 = Text("highest information gain", font_size=20)
        pick_split_text = VGroup(pick_split_line1, pick_split_line2).arrange(DOWN, buff=0.12).next_to(
            info_gain_formula, DOWN, buff=0.3
        )

        with self.voiceover(
            text=(
                "Based on entropy, we get a metric called information gain, "
                "which measures how much entropy would drop if we split on a "
                "particular point -- in other words, how much benefit that split "
                "gives us. In each round of recursive partitioning, we pick "
                "whichever split gives the highest information gain."
            )
        ) as tracker:
            self.play(Write(info_gain_title), run_time=1.0)
            self.wait(3.0)
            self.play(Write(info_gain_formula), run_time=2.5)  # "measures how much entropy would drop"
            self.wait(9.0)
            self.play(Write(pick_split_text), run_time=1.5)  # "we pick whichever split gives the highest information gain"
            self.wait(tracker.get_remaining_duration())

        right_content = VGroup(
            goal_text,
            entropy_title,
            entropy_formula,
            entropy_max,
            entropy_min,
            info_gain_title,
            info_gain_formula,
            pick_split_text,
        )
        # SurroundingRectangle sizes itself from .height/.width, which manim
        # miscomputes for a group whose content lies entirely on one side of
        # the local origin (both lines sit below y=0 here) -- get_top() /
        # get_bottom() / get_left() / get_right() aren't affected, so the
        # rectangle is built from those directly instead.
        stop_buff = 0.04
        stop_top = max(code_lines[3].get_top()[1], code_lines[4].get_top()[1])
        stop_bottom = min(code_lines[3].get_bottom()[1], code_lines[4].get_bottom()[1])
        stop_left = min(code_lines[3].get_left()[0], code_lines[4].get_left()[0])
        stop_right = max(code_lines[3].get_right()[0], code_lines[4].get_right()[0])
        stop_highlight = Rectangle(
            width=(stop_right - stop_left) + 2 * stop_buff,
            height=(stop_top - stop_bottom) + 2 * stop_buff,
            color=YELLOW,
        ).move_to([(stop_left + stop_right) / 2, (stop_top + stop_bottom) / 2, 0])
        stop_note = Text(
            "Natural stop: all data in a node is one class\n→ no need for further splits",
            font_size=20,
            color=YELLOW,
        ).move_to(RIGHT * 2.0 + UP * 1.5)

        with self.voiceover(
            text=(
                "Now that we know how to split, when do we stop growing the "
                "tree? Naturally, if all the data in a node is already one "
                "class, then it becomes a leaf node of that class and no further "
                "split is needed."
            )
        ) as tracker:
            self.play(FadeOut(split_highlight), FadeOut(right_content), run_time=1)
            self.play(Create(stop_highlight), run_time=1.5)
            self.play(FadeIn(stop_note, shift=UP * 0.1), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        prune_note = Text(
                    "Tree Pruning Techniques",
                    font_size=26,
                    color=YELLOW,
                ).move_to(RIGHT * 3.6 + UP * 1.5)
        
        with self.voiceover(
            text=(
                "In practice, if you keep splitting until all leaf nodes are "
                "pure, you would still likely get a very deep tree that is prone "
                "to overfitting. Therefore, we rely on tree pruning techniques "
                "to manage that."
            )
        ) as tracker:            
            self.wait(6.0)
            self.play(FadeOut(stop_note), FadeOut(stop_highlight), FadeOut(code_note), run_time=1)
            self.wait(1.0)
            self.play(FadeIn(prune_note, shift=UP * 0.1), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        # -- pre / post pruning -- both confined to the right side, since the
        # pseudocode stays put at its original size (per feedback: don't
        # shrink it once we start talking about pruning) -----------------
        pre_center = RIGHT * 1.5 + DOWN * 1.4
        post_center = RIGHT * 5.0 + DOWN * 1.4

        pre_title = Text("Pre-Pruning", font_size=20, color=BLUE).move_to(pre_center + UP * 1.9)
        pre_root = make_tree_node("X1?", color=WHITE, font_size=15).move_to(pre_center + UP * 1.0)
        pre_c1 = make_tree_node("X2?", color=WHITE, font_size=15).move_to(pre_center + LEFT * 0.8)
        pre_c2 = make_tree_node("Leaf", color=GREEN, font_size=15).move_to(pre_center + RIGHT * 0.8)
        pre_tree = VGroup(pre_root, pre_c1, pre_c2)
        pre_edges = VGroup(make_tree_edge(pre_root, pre_c1), make_tree_edge(pre_root, pre_c2))
        pre_gate = Rectangle(width=1.9, height=0.3, color=RED, fill_opacity=0.5).next_to(pre_c1, DOWN, buff=0.25)
        pre_gate_label = Text("e.g., min info gain / max depth", font_size=11, color=RED).next_to(pre_gate, DOWN, buff=0.08)

        post_title = Text("Post-Pruning", font_size=20, color=BLUE).move_to(post_center + UP * 2.1)
        post_root = make_tree_node("X1?", color=WHITE, font_size=15).move_to(post_center + UP * 1.2)
        post_c1 = make_tree_node("X2?", color=WHITE, font_size=15).move_to(post_center + UP * 0.2 + LEFT * 0.9)
        post_c2 = make_tree_node("X3?", color=WHITE, font_size=15).move_to(post_center + UP * 0.2 + RIGHT * 0.9)
        post_l1 = make_tree_node("Leaf", color=GREEN, font_size=13).move_to(post_center + DOWN * 0.8 + LEFT * 1.4)
        post_l2 = make_tree_node("Leaf", color=GREEN, font_size=13).move_to(post_center + DOWN * 0.8 + LEFT * 0.3)
        post_l3 = make_tree_node("Leaf", color=GREEN, font_size=13).move_to(post_center + DOWN * 0.8 + RIGHT * 0.9)
        post_tree = VGroup(post_root, post_c1, post_c2, post_l1, post_l2, post_l3)
        e_post_root_c1 = make_tree_edge(post_root, post_c1)
        e_post_root_c2 = make_tree_edge(post_root, post_c2)
        e_post_c1_l1 = make_tree_edge(post_c1, post_l1)
        e_post_c1_l2 = make_tree_edge(post_c1, post_l2)
        e_post_c2_l3 = make_tree_edge(post_c2, post_l3)
        post_edges = VGroup(e_post_root_c1, e_post_root_c2, e_post_c1_l1, e_post_c1_l2, e_post_c2_l3)
        scissors = Text("✂", font_size=24, color=RED)

        with self.voiceover(
            text=(
                "There are two types of pruning techniques: pre-pruning, which "
                "restricts how large the tree is allowed to grow while it's "
                "being built -- for example, thresholds on the minimum "
                "information gain for a split, the minimum number of data "
                "points per node, the maximum depth, or the maximum number of "
                "decision nodes."
            )
        ) as tracker:
            self.play(Write(pre_title), run_time=1)
            self.play(FadeIn(pre_edges), FadeIn(pre_tree), run_time=1.5)
            self.play(FadeIn(pre_gate, scale=0.8), FadeIn(pre_gate_label), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        with self.voiceover(
            text=(
                "And post-pruning, which lets the tree grow freely first, then "
                "cuts back nodes afterward based on how much each node actually "
                "reduces expected error -- essentially evaluating each node's "
                "usefulness and removing not very useful ones."
            )
        ) as tracker:
            self.play(Write(post_title), run_time=1)
            self.play(FadeIn(post_edges), FadeIn(post_tree), run_time=1.5)
            cut_point = VGroup(e_post_c1_l1, e_post_c1_l2).get_center()
            scissors.move_to(post_c1.get_center() + UP * 0.5)
            self.play(FadeIn(scissors), run_time=0.5)
            self.play(scissors.animate.move_to(cut_point), run_time=0.8)  # scissors travel to the cut
            new_leaf = make_tree_node("Leaf", color=GREEN, font_size=15).move_to(post_c1.get_center())
            self.play(
                FadeOut(e_post_c1_l1), FadeOut(e_post_c1_l2), FadeOut(post_l1), FadeOut(post_l2),
                FadeOut(scissors), Transform(post_c1, new_leaf),
                run_time=1.0,
            )  # the snip: subtree collapses into a single leaf
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(pseudocode),
            FadeOut(pre_title), FadeOut(pre_tree), FadeOut(pre_edges), FadeOut(pre_gate), FadeOut(pre_gate_label),
            FadeOut(post_title), FadeOut(post_root), FadeOut(post_c1), FadeOut(post_c2), FadeOut(post_l3),
            FadeOut(e_post_root_c1), FadeOut(e_post_root_c2), FadeOut(e_post_c2_l3), FadeOut(prune_note),
        )


class Scene10(VoiceoverScene, Scene10Mixin):
    """Standalone preview: manim -pql scene_10.py Scene10"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_10()
