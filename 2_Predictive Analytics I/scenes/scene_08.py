import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_voiceover import VoiceoverScene

from tts import get_speech_service
from common import make_tree_node, make_tree_edge, Text

DECISION_NODE_COLOR = BLUE
LEAF_NODE_COLOR = GREEN
HIGHLIGHT_COLOR = RED


class Scene08Mixin:
    # ------------------------------------------------------------------
    # Scene 8: decision trees -- PC-buying example
    # ------------------------------------------------------------------
    def scene_08(self):
        title = Text("Second Predictive Algorithm: Decision Tree", font_size=30).to_edge(UP, buff=0.4)
        subtitle = Text(
            "A set of if-then rules, organized into the structure of a tree",
            font_size=22,
            color=YELLOW,
        ).next_to(title, DOWN, buff=0.25)

        with self.voiceover(
            text=(
                "Now let's talk about the second classification algorithm: the "
                "decision tree. It's a foundational techniques in machine "
                "learning and the basis for several more advanced, popular "
                "algorithms such as random forest and gradient boosting trees. A "
                "decision tree is a set of if-then decision rules organized into "
                "the structure of a tree."
            )
        ) as tracker:
            self.play(Write(title), run_time=2)
            self.wait(10.7)
            self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.8)  # "A decision tree is a set of if-then rules..."
            self.wait(tracker.get_remaining_duration())

        root = make_tree_node("Age < 30?", color=DECISION_NODE_COLOR).move_to(UP * 2.0)
        student_node = make_tree_node("Student?", color=DECISION_NODE_COLOR).move_to(UP * 0.4 + LEFT * 3.4)
        children_node = make_tree_node("Children?", color=DECISION_NODE_COLOR).move_to(UP * 0.4 + RIGHT * 2.8)

        leaf_student_pc = make_tree_node("PC", color=LEAF_NODE_COLOR).move_to(DOWN * 1.3 + LEFT * 4.6)
        leaf_student_no = make_tree_node("No PC", color=LEAF_NODE_COLOR).move_to(DOWN * 1.3 + LEFT * 2.3)
        leaf_children_pc = make_tree_node("PC", color=LEAF_NODE_COLOR).move_to(DOWN * 1.3 + RIGHT * 1.1)
        college_node = make_tree_node("College Ed.?", color=DECISION_NODE_COLOR).move_to(DOWN * 1.3 + RIGHT * 4.3)

        leaf_college_pc = make_tree_node("PC", color=LEAF_NODE_COLOR).move_to(DOWN * 3.0 + RIGHT * 3.3)
        leaf_college_no = make_tree_node("No PC", color=LEAF_NODE_COLOR).move_to(DOWN * 3.0 + RIGHT * 5.3)

        tree_group = VGroup(
            root, student_node, children_node, leaf_student_pc, leaf_student_no,
            leaf_children_pc, college_node, leaf_college_pc, leaf_college_no,
        ).scale(0.82).next_to(subtitle, DOWN, buff=0.5)

        e_root_student = make_tree_edge(root, student_node, "Yes")
        e_root_children = make_tree_edge(root, children_node, "No")
        e_student_pc = make_tree_edge(student_node, leaf_student_pc, "Yes")
        e_student_no = make_tree_edge(student_node, leaf_student_no, "No")
        e_children_pc = make_tree_edge(children_node, leaf_children_pc, "Yes")
        e_children_college = make_tree_edge(children_node, college_node, "No")
        e_college_pc = make_tree_edge(college_node, leaf_college_pc, "Yes")
        e_college_no = make_tree_edge(college_node, leaf_college_no, "No")
        edges = VGroup(
            e_root_student, e_root_children, e_student_pc, e_student_no,
            e_children_pc, e_children_college, e_college_pc, e_college_no,
        )

        pc_context = Text("Predicting: will a person buy a PC?", font_size=20, color=GREY_B).next_to(
            tree_group, UP, buff=0.15
        )

        with self.voiceover(
            text=(
                "For example, here's a tree built to predict whether someone "
                "will buy a PC, based on demographic information. Each branch "
                "corresponds to one decision rule -- this highlighted branch, for "
                "instance, says: if the person is younger than 30 and is not a "
                "student, the model predicts they will not buy a PC."
            )
        ) as tracker:
            self.play(FadeIn(pc_context), run_time=1)
            self.play(Create(root), run_time=1)
            self.play(
                Create(e_root_student), Create(e_root_children),
                FadeIn(student_node), FadeIn(children_node), run_time=2,
            )
            self.play(
                Create(e_student_pc), Create(e_student_no),
                FadeIn(leaf_student_pc), FadeIn(leaf_student_no), run_time=2,
            )
            self.play(
                Create(e_children_pc), Create(e_children_college),
                FadeIn(leaf_children_pc), FadeIn(college_node), run_time=2,
            )
            self.play(
                Create(e_college_pc), Create(e_college_no),
                FadeIn(leaf_college_pc), FadeIn(leaf_college_no), run_time=2,
            )
            highlight_path = VGroup(root, e_root_student, student_node, e_student_no, leaf_student_no)
            self.play(Indicate(highlight_path, color=HIGHLIGHT_COLOR), run_time=1.5)
            self.wait(tracker.get_remaining_duration())

        legend_decision = VGroup(
            RoundedRectangle(width=0.4, height=0.25, color=DECISION_NODE_COLOR, corner_radius=0.05),
            Text("Decision Node", font_size=18),
        ).arrange(RIGHT, buff=0.15)
        legend_leaf = VGroup(
            RoundedRectangle(width=0.4, height=0.25, color=LEAF_NODE_COLOR, corner_radius=0.05),
            Text("Leaf Node", font_size=18),
        ).arrange(RIGHT, buff=0.15)
        legend = VGroup(legend_decision, legend_leaf).arrange(RIGHT, buff=0.6).next_to(
            tree_group, DOWN, buff=0.3
        )

        decision_nodes = VGroup(root, student_node, children_node, college_node)
        with self.voiceover(
            text=(
                "A decision tree has two kinds of nodes. A decision node "
                "contains the attribute the tree is splitting on -- in this "
                "example, age, student status, children at home, and college "
                "education are all decision nodes."
            )
        ) as tracker:
            self.wait(1.0)
            self.play(FadeIn(legend_decision), run_time=1)
            self.play(Indicate(decision_nodes, color=DECISION_NODE_COLOR), run_time=2)
            self.wait(tracker.get_remaining_duration())

        leaf_nodes = VGroup(leaf_student_pc, leaf_student_no, leaf_children_pc, leaf_college_pc, leaf_college_no)
        with self.voiceover(
            text=(
                "A leaf node contains the final prediction. Every path through "
                "the tree passes through some decision nodes and ends in a leaf "
                "node."
            )
        ) as tracker:
            self.play(FadeIn(legend_leaf), run_time=1)
            self.play(Indicate(leaf_nodes, color=LEAF_NODE_COLOR), run_time=2)
            self.wait(tracker.get_remaining_duration())

        self.wait()
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(pc_context), FadeOut(tree_group), FadeOut(edges), FadeOut(legend),
        )


class Scene08(VoiceoverScene, Scene08Mixin):
    """Standalone preview: manim -pql scene_08.py Scene08"""

    def construct(self):
        self.set_speech_service(get_speech_service())
        self.scene_08()
