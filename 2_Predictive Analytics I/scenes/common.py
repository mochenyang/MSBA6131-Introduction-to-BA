import numpy as np
from manim import *
from manim import Text as _ManimText

# ----------------------------------------------------------------------
# Semantic colors shared across scenes
# ----------------------------------------------------------------------
TRAIN_COLOR = GREEN
VALIDATION_COLOR = YELLOW
CORRECT_COLOR = GREEN
ERROR_COLOR = RED

# Manim's Text (Pango-backed) renders visible glyph-spacing artifacts at
# small font sizes -- confirmed empirically: font_size=40 renders "Training
# Error" cleanly, font_size=14 renders it as "Train in g Error" (gaps mid-
# word, not at word boundaries). Root cause is glyph-cluster advance-width
# rounding in the Pango/SVG pipeline, which is a much bigger fraction of a
# small letter's width than a large one.
#
# This drop-in replacement always renders at a safe base size and scales
# down to whatever font_size was actually requested, so every call site
# keeps its exact `Text(..., font_size=14)` signature -- only the import
# needs to change. Every scene file should get `Text` from here (import it
# from `common` *after* `from manim import *`, so it shadows manim's), and
# every Text(...) call inside this module's own helpers below picks it up
# automatically too, since this class definition already shadows manim's
# Text for the rest of this file.
TEXT_SAFE_BASE_SIZE = 40


class Text(_ManimText):
    def __init__(self, text, font_size=48, **kwargs):
        if font_size < TEXT_SAFE_BASE_SIZE:
            super().__init__(text, font_size=TEXT_SAFE_BASE_SIZE, **kwargs)
            self.scale(font_size / TEXT_SAFE_BASE_SIZE)
        else:
            super().__init__(text, font_size=font_size, **kwargs)


# ----------------------------------------------------------------------
# Predictive Modeling Pipeline diagram -- built in scene_03, echoed
# (same layout, faded back in from a fixture) at the top of scene_05.
# ----------------------------------------------------------------------
def make_data_table(outcome_filled, n_rows=4, width=2.6, height=2.0):
    """A tiny mock spreadsheet: an 'Attributes' column of grey bars and an
    'Outcome' column that's either filled with colored value bars
    (outcome_filled=True) or empty question marks (outcome_filled=False).
    Returns a VGroup centered on the origin."""
    row_h = height / (n_rows + 1)
    header = VGroup(
        Text("Attributes", font_size=16, color=GREY_B).move_to(
            UP * height / 2 + LEFT * width / 4
        ),
        Text("Outcome", font_size=16, color=GREY_B).move_to(
            UP * height / 2 + RIGHT * width / 3
        ),
    )
    rows = VGroup()
    for i in range(n_rows):
        y = height / 2 - row_h * (i + 1)
        attr_cells = VGroup(
            *[
                Rectangle(width=width / 4 * 0.8, height=row_h * 0.6, color=GREY_B, fill_opacity=0.4)
                .move_to(LEFT * width / 2 + RIGHT * width / 4 * (j + 0.5) + UP * y)
                for j in range(2)
            ]
        )
        if outcome_filled:
            outcome_cell = Rectangle(
                width=width / 3 * 0.7, height=row_h * 0.6, color=BLUE, fill_opacity=0.7
            ).move_to(RIGHT * width / 3 + UP * y)
        else:
            outcome_cell = Text("?", font_size=20, color=GREY_B).move_to(RIGHT * width / 3 + UP * y)
        rows.add(VGroup(attr_cells, outcome_cell))
    return VGroup(header, rows)


def make_pipeline_box(box_title, subtitle, outcome_filled):
    table = make_data_table(outcome_filled)
    title_txt = Text(box_title, font_size=26, color=YELLOW)
    subtitle_txt = Text(subtitle, font_size=20, color=GREY_B).next_to(title_txt, DOWN, buff=0.15)
    header = VGroup(title_txt, subtitle_txt)
    table.next_to(header, DOWN, buff=0.35)
    border = SurroundingRectangle(VGroup(header, table), color=WHITE, buff=0.3, corner_radius=0.15)
    return VGroup(border, header, table)


def make_pipeline_diagram():
    """Returns (title, left_box, right_box, whole_group). left_box is
    "Model Training / Labeled Data" (outcome filled in); right_box is
    "Model Deployment / Unlabeled Data" (outcome shown as '?')."""
    title = Text("Predictive Modeling Pipeline", font_size=34).to_edge(UP, buff=0.5)
    left_box = make_pipeline_box("Model Training", "Labeled Data", outcome_filled=True)
    right_box = make_pipeline_box("Model Deployment", "Unlabeled Data", outcome_filled=False)
    left_box.next_to(title, DOWN, buff=0.6).shift(LEFT * 3.4)
    right_box.next_to(title, DOWN, buff=0.6).shift(RIGHT * 3.4)
    whole = VGroup(title, left_box, right_box)
    return title, left_box, right_box, whole


def make_gear(label_text="Model"):
    """The recurring "Model" gear icon -- introduced in scene_03 alongside
    the pipeline diagram, and reused (same look) in scene_05 when the
    pipeline is split into training/validation."""
    circle = Circle(radius=0.55, color=WHITE)
    teeth = VGroup(
        *[
            Rectangle(width=0.12, height=0.18, color=WHITE, fill_opacity=1).move_to(
                circle.get_center() + 0.63 * np.array([np.cos(a), np.sin(a), 0])
            ).rotate(a)
            for a in np.linspace(0, 2 * PI, 8, endpoint=False)
        ]
    )
    label = Text(label_text, font_size=18).move_to(circle.get_center())
    return VGroup(teeth, circle, label)


# ----------------------------------------------------------------------
# Generic decision-tree node/edge drawing -- shared shape by scenes 8, 9,
# 10 (each scene picks its own node text/colors, only the geometry repeats).
# ----------------------------------------------------------------------
def make_tree_node(text, color=WHITE, font_size=22, width=None):
    label = Text(text, font_size=font_size)
    box = RoundedRectangle(
        width=width if width else label.width + 0.5,
        height=label.height + 0.4,
        corner_radius=0.12,
        color=color,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_tree_edge(node_a, node_b, label=None, color=WHITE):
    line = Line(node_a.get_bottom(), node_b.get_top(), color=color, buff=0.05, stroke_width=2.5)
    if label is None:
        return line
    tag = Text(label, font_size=16, color=GREY_B).move_to(line.get_center()).shift(RIGHT * 0.55)
    return VGroup(line, tag)


# ----------------------------------------------------------------------
# Confusion matrix grid -- built (abstract Positive/Negative) in scene_11,
# rebuilt concrete (Fraudulent/Non-Fraudulent, with counts) in scene_12.
# ----------------------------------------------------------------------
def make_confusion_matrix(pred_labels, actual_labels, cell_texts=None, cell_size=2.3, label_font_size=18):
    """2x2 grid. cells[0][0]=TP (pred[0] & actual[0]), cells[0][1]=FP
    (pred[0] & actual[1]), cells[1][0]=FN (pred[1] & actual[0]),
    cells[1][1]=TN (pred[1] & actual[1]). cell_texts, if given, is a 2x2
    list of strings drawn inside each cell.

    actual_labels should be short (e.g. "Positive"/"Negative") -- they sit
    directly above adjacent cells, so anything much longer than that
    collides with its neighbor even at cell_size's default width."""
    cells = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            rect = Square(side_length=cell_size, color=WHITE, stroke_width=2)
            rect.move_to(RIGHT * cell_size * j + DOWN * cell_size * i)
            cells[i][j] = rect
    grid = VGroup(*[cells[i][j] for i in range(2) for j in range(2)])

    col_labels = VGroup(
        *[
            Text(actual_labels[j], font_size=label_font_size, color=GREY_B).next_to(
                cells[0][j], UP, buff=0.2
            )
            for j in range(2)
        ]
    )
    row_labels = VGroup(
        *[
            Text(pred_labels[i], font_size=label_font_size, color=GREY_B).next_to(
                cells[i][0], LEFT, buff=0.3
            )
            for i in range(2)
        ]
    )

    cell_text_mobs = [[None, None], [None, None]]
    if cell_texts is not None:
        for i in range(2):
            for j in range(2):
                cell_text_mobs[i][j] = Text(
                    str(cell_texts[i][j]), font_size=label_font_size + 4
                ).move_to(cells[i][j].get_center())

    group = VGroup(grid, col_labels, row_labels)
    if cell_texts is not None:
        group.add(*[cell_text_mobs[i][j] for i in range(2) for j in range(2)])

    return {
        "cells": cells,
        "col_labels": col_labels,
        "row_labels": row_labels,
        "cell_texts": cell_text_mobs,
        "group": group,
    }
