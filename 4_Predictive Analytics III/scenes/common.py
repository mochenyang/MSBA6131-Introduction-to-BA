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
POS_COLOR = ORANGE            # class "P" (positive), actual-class column
NEG_COLOR = TEAL              # class "N" (negative), actual-class column
PRED_POS_COLOR = ORANGE        # "Predicted: Positive" tag
PRED_NEG_COLOR = TEAL       # "Predicted: Negative" tag
HIGHLIGHT_COLOR = YELLOW
ERROR_COLOR = RED
BETTER_COLOR = GREEN
DATA_CURVE_COLOR = "#58C4DD"  # the one running example's ROC / cumulative
                               # response curve, used throughout the unit

# Illustrative "four hypothetical classifiers" palette -- shared between the
# ROC comparison (scene 4) and the cumulative response comparison (scene 6),
# since both live on the same 0-1 by 0-1 axes with the same "closer to
# top-left = better" reading. Deliberately distinct from DATA_CURVE_COLOR so
# the one running example is never visually confused with these generic
# stand-ins.
CURVE_A_COLOR = GREEN         # near-perfect
CURVE_B_COLOR = PURPLE        # good
CURVE_C_COLOR = MAROON        # mediocre
CURVE_D_COLOR = GREY_B        # random / diagonal


# ----------------------------------------------------------------------
# The one running example used throughout the unit: 10 validation records,
# already sorted by predicted probability of class P from high to low.
# Chosen so that stepping the cutoff down one row at a time reproduces the
# exact numbers referenced in the narration (e.g. the cumulative response
# of 1/3 at the top 20% of data in scene 7), which is why the top two
# records are both P and the total P/N split stays 6/4 -- only the order
# of the remaining 8 records was adjusted.
#
# The first version of this table (2 N's at ranks 3-4, right after the top
# two P's) worked out to an AUC of exactly 0.5 -- mathematically a random
# classifier, despite the ROC curve visibly bowing above the diagonal. This
# arrangement pushes the N's later instead, for an AUC of 0.875 (21 of the
# 24 P/N pairs correctly ranked): comfortably better than random without
# being the perfect classifier illustrated separately as curve A.
# ----------------------------------------------------------------------
RANKED_DATA = [
    ("P", 0.99),
    ("P", 0.98),
    ("P", 0.96),
    ("P", 0.90),
    ("N", 0.88),
    ("P", 0.87),
    ("N", 0.85),
    ("P", 0.80),
    ("N", 0.70),
    ("N", 0.65),
]
NUM_POS = sum(1 for cls, _ in RANKED_DATA if cls == "P")   # 6
NUM_NEG = sum(1 for cls, _ in RANKED_DATA if cls == "N")   # 4
N_RECORDS = len(RANKED_DATA)                                # 10


def confusion_counts(k):
    """Counts when the top k ranked records (by probability) are predicted
    P and the rest are predicted N. Returns (TP, FP, FN, TN)."""
    top, rest = RANKED_DATA[:k], RANKED_DATA[k:]
    tp = sum(1 for cls, _ in top if cls == "P")
    fp = sum(1 for cls, _ in top if cls == "N")
    fn = sum(1 for cls, _ in rest if cls == "P")
    tn = sum(1 for cls, _ in rest if cls == "N")
    return tp, fp, fn, tn


def compute_roc_points():
    """(FPR, TPR) at every cutoff position k = 0..N_RECORDS, sweep order."""
    points = []
    for k in range(N_RECORDS + 1):
        tp, fp, _, _ = confusion_counts(k)
        points.append((fp / NUM_NEG, tp / NUM_POS))
    return points


def compute_cum_response_points():
    """(% of data, cumulative response) at every cutoff k = 0..N_RECORDS."""
    points = []
    for k in range(N_RECORDS + 1):
        tp, _, _, _ = confusion_counts(k)
        points.append((k / N_RECORDS, tp / NUM_POS))
    return points


# ----------------------------------------------------------------------
# Ranked validation table -- built in scene_02, reused (same construction,
# via this same function) in scene_03, scene_06, scene_08's fixture, and
# scene_05's fixture. Column x-offsets are relative to the table's own
# local origin; move the returned group wherever the caller needs it.
# ----------------------------------------------------------------------
TABLE_COL_X = (-1.7, 0.0, 1.9)
TABLE_ROW_HEIGHT = 0.42


def make_ranked_table(font_size=18):
    n = N_RECORDS
    top_y = TABLE_ROW_HEIGHT * (n / 2 + 0.7)
    headers = ("Actual", "Pred. Prob.", "Pred. Class")
    header = VGroup(*[
        Text(h, font_size=font_size, color=GREY_B).move_to([x, top_y, 0])
        for h, x in zip(headers, TABLE_COL_X)
    ])
    divider = Line(
        [TABLE_COL_X[0] - 0.7, top_y - TABLE_ROW_HEIGHT * 0.55, 0],
        [TABLE_COL_X[2] + 0.7, top_y - TABLE_ROW_HEIGHT * 0.55, 0],
        stroke_width=1, color=GREY_D,
    )
    rows = []
    for i, (cls, prob) in enumerate(RANKED_DATA):
        y = top_y - (i + 1) * TABLE_ROW_HEIGHT
        actual = Text(cls, font_size=font_size, color=POS_COLOR if cls == "P" else NEG_COLOR)
        actual.move_to([TABLE_COL_X[0], y, 0])
        prob_t = Text(f"{prob:.2f}", font_size=font_size).move_to([TABLE_COL_X[1], y, 0])
        # A tiny invisible Dot, not an empty Text -- an empty-string Text has
        # no glyph points, so get_center()/get_y() raise once something else
        # (make_cutoff_line, predicted_labels_for_cutoff) reads its position
        # before any real label has been placed there.
        pred_t = Dot(radius=0.001, fill_opacity=0, stroke_opacity=0).move_to([TABLE_COL_X[2], y, 0])
        rows.append({"actual": actual, "prob": prob_t, "pred": pred_t, "class": cls, "y": y})
    group = VGroup(header, divider, *[VGroup(r["actual"], r["prob"], r["pred"]) for r in rows])
    return {
        "header": header, "divider": divider, "rows": rows, "group": group,
        "top_y": top_y, "col_x": TABLE_COL_X,
    }


def cutoff_boundary_y(table, k):
    """Y-coordinate of the cutoff line sitting between row k and row k+1
    (k=0 is above row 1, k=N_RECORDS is below the last row), read off the
    table's *actual current* on-screen position -- robust to the table
    having been translated (e.g. `table["group"].move_to(...)`) after
    construction, unlike computing it from the construction-time formula."""
    rows = table["rows"]
    if k <= 0:
        return rows[0]["pred"].get_y() + TABLE_ROW_HEIGHT / 2
    if k >= N_RECORDS:
        return rows[-1]["pred"].get_y() - TABLE_ROW_HEIGHT / 2
    return (rows[k - 1]["pred"].get_y() + rows[k]["pred"].get_y()) / 2


def make_cutoff_line(table, k, color=RED, width=0.5):
    y = cutoff_boundary_y(table, k)
    left_x = table["group"].get_left()[0] - width
    right_x = table["group"].get_right()[0] + width
    return Line([left_x, y, 0], [right_x, y, 0], color=color, stroke_width=3)


def predicted_labels_for_cutoff(table, k, font_size=16):
    """New 'Predicted' cell mobjects (Positive/Negative, colored) for cutoff
    k, positioned to replace table['rows'][i]['pred'] via Transform/FadeIn."""
    labels = []
    for i, row in enumerate(table["rows"]):
        if i < k:
            word, color = "P", PRED_POS_COLOR
        else:
            word, color = "N", PRED_NEG_COLOR
        labels.append(Text(word, font_size=font_size, color=color).move_to(row["pred"].get_center()))
    return labels


# ----------------------------------------------------------------------
# Confusion matrix -- same 2x2 convention used across earlier units'
# common.py (cells[0][0]=TP, [0][1]=FP, [1][0]=FN, [1][1]=TN). Built
# live-updating in scene_02/scene_03 (counts change as the cutoff sweeps)
# and as a static snapshot in scene_08's summary.
# ----------------------------------------------------------------------
def make_confusion_matrix(cell_size=1.0, label_font_size=14):
    pred_labels = ("Pred: P", "Pred: N")
    actual_labels = ("Actual: P", "Actual: N")
    cells = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            rect = Square(side_length=cell_size, color=WHITE, stroke_width=2)
            rect.move_to(RIGHT * cell_size * j + DOWN * cell_size * i)
            cells[i][j] = rect
    grid = VGroup(*[cells[i][j] for i in range(2) for j in range(2)])
    col_labels = VGroup(*[
        Text(actual_labels[j], font_size=label_font_size, color=GREY_B).next_to(cells[0][j], UP, buff=0.15)
        for j in range(2)
    ])
    row_labels = VGroup(*[
        Text(pred_labels[i], font_size=label_font_size, color=GREY_B).next_to(cells[i][0], LEFT, buff=0.2)
        for i in range(2)
    ])
    group = VGroup(grid, col_labels, row_labels)
    return {"cells": cells, "col_labels": col_labels, "row_labels": row_labels, "group": group}


def confusion_matrix_texts(cm, k, font_size=20):
    """New centered Text mobjects (tp/fp/fn/tn) for cutoff k, ready to
    FadeIn/Transform into cm['cells'] positions."""
    tp, fp, fn, tn = confusion_counts(k)
    vals = {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
    positions = {
        "tp": cm["cells"][0][0], "fp": cm["cells"][0][1],
        "fn": cm["cells"][1][0], "tn": cm["cells"][1][1],
    }
    return {
        key: Text(str(val), font_size=font_size).move_to(positions[key].get_center())
        for key, val in vals.items()
    }


# ----------------------------------------------------------------------
# Unit-square (0-1 by 0-1) axes -- shared shape for both the ROC curve
# (FPR vs TPR) and the cumulative response curve (% data vs cumulative
# response): identical construction, only the axis labels differ.
# ----------------------------------------------------------------------
def make_unit_axes(x_label_text, y_label_text, x_length=4.6, y_length=4.2, font_size=16, x_max=1.0, y_max=1.0):
    """x_max/y_max default to 1.0 (ticks land exactly at 0, 0.2, ..., 1.0,
    with the axis line ending right there). Pass e.g. 1.08 to extend the
    axis line a bit past the last tick -- the tick step stays 0.2, so the
    same 0/0.2/.../1.0 ticks still show, just with breathing room between
    the "1.0" label/corner and the arrowhead instead of the two crowding
    each other."""
    axes = Axes(
        x_range=[0, x_max, 0.2], y_range=[0, y_max, 0.2], x_length=x_length, y_length=y_length,
        # tip_width/tip_height belong inside axis_config -- that's the dict
        # Axes actually forwards to each underlying NumberLine. manim's
        # default tip is 0.35, oversized next to a plot this size.
        axis_config={
            "include_numbers": True, "font_size": 14, "decimal_number_config": {"num_decimal_places": 1},
            "tip_width": 0.15, "tip_height": 0.15,
        },
    )
    x_label = axes.get_x_axis_label(Text(x_label_text, font_size=font_size), edge=DOWN, direction=DOWN, buff=0.3)
    y_label = axes.get_y_axis_label(Text(y_label_text, font_size=font_size), edge=LEFT, direction=LEFT, buff=0.25)
    return {"axes": axes, "x_label": x_label, "y_label": y_label, "group": VGroup(axes, x_label, y_label)}


def make_diagonal(axes, color=GREY_B):
    return DashedLine(axes.c2p(0, 0), axes.c2p(1, 1), color=color, stroke_width=2)


def points_to_curve(axes, points, color=DATA_CURVE_COLOR, stroke_width=3.5):
    coords = [axes.c2p(x, y) for x, y in points]
    curve = VMobject(color=color, stroke_width=stroke_width)
    curve.set_points_as_corners(coords)
    return curve


def build_data_curve(axes, points, color=DATA_CURVE_COLOR, dot_radius=0.05, stroke_width=3.5):
    """Already-drawn piecewise curve through `points` on `axes` -- a VGroup
    of connecting segments plus vertex dots, i.e. the finished look of the
    live cutoff-sweep animation in scene_03 / scene_06. Used directly by
    those scenes' own final state, and by scene_05's and scene_08's
    standalone-preview fixtures to reconstruct that end-state in one call
    without replaying the sweep."""
    coords = [axes.c2p(x, y) for x, y in points]
    segments = VGroup(*[
        Line(coords[i], coords[i + 1], color=color, stroke_width=stroke_width)
        for i in range(len(coords) - 1)
    ])
    dots = VGroup(*[Dot(c, radius=dot_radius, color=color) for c in coords])
    return VGroup(segments, dots)


# ----------------------------------------------------------------------
# Four illustrative "hypothetical classifier" curves (A-D) for comparing
# models on a 0-1 by 0-1 axes -- reused as-is between the ROC comparison
# (scene 4) and the cumulative response comparison (scene 6): both share
# the exact same axes shape and the same "closer to top-left = better"
# reading, only the axis labels differ. Also reconstructed (not replayed)
# by scene_05's fixture to preview its "bring back scene 4's four curves"
# beat in isolation.
# ----------------------------------------------------------------------
def make_illustrative_curves(axes):
    curve_defs = {
        "a": ([(0, 0), (0, 0.95), (0.05, 1), (1, 1)], CURVE_A_COLOR, "A"),
        "b": ([(0, 0), (0.15, 0.55), (0.4, 0.8), (0.7, 0.93), (1, 1)], CURVE_B_COLOR, "B"),
        "c": ([(0, 0), (0.25, 0.35), (0.5, 0.58), (0.75, 0.82), (1, 1)], CURVE_C_COLOR, "C"),
    }
    curves = {}
    labels = {}
    for key, (pts, color, name) in curve_defs.items():
        coords = [axes.c2p(x, y) for x, y in pts]
        curve = VMobject(color=color, stroke_width=3.5)
        curve.set_points_smoothly(coords)
        curves[key] = curve
        labels[key] = Text(name, font_size=18, color=color).next_to(coords[-2], UP, buff=0.12)
    curves["d"] = make_diagonal(axes, color=CURVE_D_COLOR)
    labels["d"] = Text("D", font_size=18, color=CURVE_D_COLOR).next_to(axes.c2p(0.5, 0.5), DOWN, buff=0.35)
    group = VGroup(*curves.values(), *labels.values())
    return {"curves": curves, "labels": labels, "group": group}
