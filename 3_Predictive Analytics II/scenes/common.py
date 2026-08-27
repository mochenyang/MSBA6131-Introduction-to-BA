import numpy as np
from manim import *
from manim import Text as _ManimText

# ----------------------------------------------------------------------
# Small-font-safe Text -- see references/visual_techniques.md. Manim's
# Text (Pango-backed) renders visible glyph-spacing artifacts at small
# font sizes; this always renders at a safe base size and scales down.
# ----------------------------------------------------------------------
TEXT_SAFE_BASE_SIZE = 40


class Text(_ManimText):
    def __init__(self, text, font_size=48, **kwargs):
        if font_size < TEXT_SAFE_BASE_SIZE:
            super().__init__(text, font_size=TEXT_SAFE_BASE_SIZE, **kwargs)
            self.scale(font_size / TEXT_SAFE_BASE_SIZE)
        else:
            super().__init__(text, font_size=font_size, **kwargs)


# ----------------------------------------------------------------------
# Semantic colors shared across scenes
# ----------------------------------------------------------------------
CLASS1_COLOR = ORANGE  # "Class 1" throughout the unit (matches k-NN's
CLASS0_COLOR = TEAL    # CLASS1_COLOR in the Predictive Analytics I unit)
HIGHLIGHT_COLOR = YELLOW
ERROR_COLOR = RED


# ----------------------------------------------------------------------
# Generic decision-tree node/edge drawing (same shape as the Predictive
# Analytics I unit's common.py) -- used by scene_02 to build a compact
# decision-tree visual, and scene_02's fixture in scene_03.
# ----------------------------------------------------------------------
def make_tree_node(text, color=WHITE, font_size=20, width=None):
    label = Text(text, font_size=font_size)
    box = RoundedRectangle(
        width=width if width else label.width + 0.4,
        height=label.height + 0.35,
        corner_radius=0.1,
        color=color,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_tree_edge(node_a, node_b, label=None, color=WHITE):
    line = Line(node_a.get_bottom(), node_b.get_top(), color=color, buff=0.05, stroke_width=2.5)
    if label is None:
        return line
    tag = Text(label, font_size=14, color=GREY_B).move_to(line.get_center()).shift(RIGHT * 0.45)
    return VGroup(line, tag)


# ----------------------------------------------------------------------
# Compact k-NN visual: a scatter of two classes with a neighbor circle
# showing a 2-1 majority vote -- built in scene_02 (with a probability bar
# added below it), shrunk further into an icon in scene_03.
# ----------------------------------------------------------------------
KNN_CLASS1_PTS = [(-1.1, 0.9), (-0.5, 1.15), (-1.3, -0.6), (1.0, -1.0)]
KNN_CLASS0_PTS = [(1.2, -0.15), (-0.9, -1.1), (1.3, 1.0), (0.7, 0.8)]
KNN_NEW_PT = (0.0, 0.55)
KNN_NEIGHBOR_KEY = {(-0.5, 1.15), (0.7, 0.8), (-1.1, 0.9)}  # 2 class1 + 1 class0
KNN_NEIGHBOR_RADIUS = 1.25


def make_knn_visual():
    """Returns dict with the full VGroup plus the neighbor dots/circle/new
    dot, so a caller can build a probability bar keyed to the same 2-1 split."""
    c1_dots = VGroup(*[Dot(RIGHT * x + UP * y, color=CLASS1_COLOR, radius=0.09) for x, y in KNN_CLASS1_PTS])
    c0_dots = VGroup(*[Dot(RIGHT * x + UP * y, color=CLASS0_COLOR, radius=0.09) for x, y in KNN_CLASS0_PTS])
    all_dots = VGroup(*c1_dots, *c0_dots)
    new_dot = Dot(RIGHT * KNN_NEW_PT[0] + UP * KNN_NEW_PT[1], color=GREY_B, radius=0.1)
    neighbor_dots = VGroup(
        *[d for d, (x, y) in zip(c1_dots, KNN_CLASS1_PTS) if (x, y) in KNN_NEIGHBOR_KEY],
        *[d for d, (x, y) in zip(c0_dots, KNN_CLASS0_PTS) if (x, y) in KNN_NEIGHBOR_KEY],
    )
    neighbor_circle = Circle(radius=KNN_NEIGHBOR_RADIUS, color=WHITE, stroke_width=2.2).move_to(new_dot.get_center())
    label = Text("3-Nearest Neighbors", font_size=18).next_to(
        VGroup(all_dots, neighbor_circle), UP, buff=0.25
    )
    group = VGroup(all_dots, new_dot, neighbor_circle, label)
    return {
        "group": group,
        "all_dots": all_dots,
        "new_dot": new_dot,
        "neighbor_dots": neighbor_dots,
        "neighbor_circle": neighbor_circle,
        "label": label,
        "class1_count": 2,
        "class0_count": 1,
    }


# ----------------------------------------------------------------------
# Compact decision-tree visual: a root split into a pure leaf and a mixed
# leaf (6 class1 : 2 class0) -- the mixed leaf is what lets scene_02 build
# a probability bar from leaf class counts.
# ----------------------------------------------------------------------
def make_tree_visual():
    root = make_tree_node("X > t?", color=WHITE, font_size=18).move_to(UP * 1.1)
    pure_leaf = make_tree_node("Leaf A", color=CLASS0_COLOR, font_size=16).move_to(DOWN * 0.7 + LEFT * 1.3)
    mixed_leaf = make_tree_node("Leaf B", color=CLASS1_COLOR, font_size=16).move_to(DOWN * 0.7 + RIGHT * 1.3)
    e_left = make_tree_edge(root, pure_leaf, "Yes")
    e_right = make_tree_edge(root, mixed_leaf, "No")
    counts_label = VGroup(
        Text("6", font_size=15, color=CLASS1_COLOR),
        Text(" : ", font_size=15, color=GREY_B),
        Text("2", font_size=15, color=CLASS0_COLOR),
    ).arrange(RIGHT, buff=0.05).next_to(mixed_leaf, DOWN, buff=0.15)
    label = Text("Decision Tree", font_size=18).next_to(
        VGroup(root, pure_leaf, mixed_leaf), UP, buff=0.25
    )
    group = VGroup(label, root, pure_leaf, mixed_leaf, e_left, e_right, counts_label)
    return {
        "group": group,
        "root": root,
        "pure_leaf": pure_leaf,
        "mixed_leaf": mixed_leaf,
        "counts_label": counts_label,
        "label": label,
        "class1_count": 6,
        "class0_count": 2,
    }


# ----------------------------------------------------------------------
# Probability number line with a cutoff marker -- built in scene_02,
# faded out (not destroyed) at the end of it, then faded back in and slid
# in scene_08 for cost-sensitive classification.
# ----------------------------------------------------------------------
def make_cutoff_number_line(cutoff=0.5, width=8.0):
    line = NumberLine(x_range=[0, 1, 0.25], length=width, include_numbers=True, font_size=22)
    marker = Triangle(fill_opacity=1, color=RED, stroke_width=0).scale(0.16).rotate(PI)
    marker.next_to(line.n2p(cutoff), UP, buff=0.02)
    cutoff_label = Text(f"cutoff = {cutoff}", font_size=16, color=RED).next_to(marker, UP, buff=0.12)
    class1_label = Text("Class 1", font_size=20, color=CLASS1_COLOR).next_to(line, DOWN, buff=0.35).align_to(line, RIGHT)
    class0_label = Text("Class 0", font_size=20, color=CLASS0_COLOR).next_to(line, DOWN, buff=0.35).align_to(line, LEFT)
    group = VGroup(line, marker, cutoff_label, class1_label, class0_label)
    return {
        "line": line, "marker": marker, "cutoff_label": cutoff_label,
        "class1_label": class1_label, "class0_label": class0_label,
        "group": group,
    }


# ----------------------------------------------------------------------
# Naive Bayes formula: P(Ci|X) = [P(X|Ci) x P(Ci)] / P(X) -- built term by
# term in scene_05, reused (with the "ignore the denominator" treatment
# already applied) in scene_06.
# ----------------------------------------------------------------------
def make_bayes_formula():
    posterior = MathTex("P(C_i \\mid X)")
    equals = MathTex("=")
    likelihood = MathTex("P(X \\mid C_i)")
    times = MathTex("\\times")
    prior = MathTex("P(C_i)")
    numerator = VGroup(likelihood, times, prior).arrange(RIGHT, buff=0.25)
    evidence = MathTex("P(X)")
    frac_line = Line(LEFT, RIGHT, stroke_width=2.5)
    frac_group = VGroup(numerator, frac_line, evidence).arrange(DOWN, buff=0.22)
    frac_line.stretch_to_fit_width(max(numerator.width, evidence.width) + 0.35)
    full = VGroup(posterior, equals, frac_group).arrange(RIGHT, buff=0.4)

    posterior_label = Text("posterior", font_size=18, color=HIGHLIGHT_COLOR).next_to(posterior, DOWN, buff=0.3)
    likelihood_label = Text("likelihood", font_size=18, color=HIGHLIGHT_COLOR).next_to(likelihood, UP, buff=0.55)
    prior_label = Text("prior", font_size=18, color=HIGHLIGHT_COLOR).next_to(prior, UP, buff=0.55)
    evidence_label = Text("evidence", font_size=18, color=HIGHLIGHT_COLOR).next_to(evidence, DOWN, buff=0.3)

    return {
        "posterior": posterior, "equals": equals, "likelihood": likelihood, "times": times,
        "prior": prior, "evidence": evidence, "frac_line": frac_line, "numerator": numerator,
        "posterior_label": posterior_label, "likelihood_label": likelihood_label,
        "prior_label": prior_label, "evidence_label": evidence_label,
        "group": full,
    }


def annotate_bayes_formula(parts):
    """Grey out + strike the denominator, box the numerator -- the "we only
    need to maximize likelihood x prior" end-state built at the end of
    scene_05 and reused as-is at the start of scene_06."""
    cross = Line(
        parts["evidence"].get_corner(DL), parts["evidence"].get_corner(UR), color=ERROR_COLOR, stroke_width=3
    )
    ignore_label = Text("same for every class -- ignore", font_size=14, color=GREY_B).next_to(
        parts["evidence"], DOWN, buff=0.55
    )
    box = SurroundingRectangle(parts["numerator"], color=HIGHLIGHT_COLOR, buff=0.15, corner_radius=0.08)
    maximize_label = Text("maximize this", font_size=16, color=HIGHLIGHT_COLOR).next_to(box, UP, buff=0.2)
    return {"cross": cross, "ignore_label": ignore_label, "box": box, "maximize_label": maximize_label}


# ----------------------------------------------------------------------
# Factorized likelihood P(x1|Ci) x P(x2|Ci) x ... x P(xk|Ci) -- built in
# scene_06 under the class-conditional-independence assumption, extended
# with one more term (an irrelevant feature) in scene_07.
# ----------------------------------------------------------------------
def make_factorized_likelihood(k=3, ci_label="C_i"):
    terms = [MathTex(f"P(x_{{{i}}} \\mid {ci_label})") for i in range(1, k + 1)]
    signs = [MathTex("\\times") for _ in range(k - 1)]
    parts = []
    for i, t in enumerate(terms):
        parts.append(t)
        if i < len(signs):
            parts.append(signs[i])
    group = VGroup(*parts).arrange(RIGHT, buff=0.2)
    return {"terms": terms, "signs": signs, "group": group}
