"""Reusable visuals for Section 13 closing scenes."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Dot,
    Line,
    RoundedRectangle,
    Square,
    VGroup,
    VMobject,
)

from src.common.architecture_visuals import make_attention_matrix, make_spectrum_bars, make_wave_panel
from src.common.open_problem_visuals import make_open_problems_board
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING


FLOW_LABELS = (
    "finite vectors",
    "functions",
    "solvers",
    "solution operator",
    "NO architectures",
    "domains",
    "open problems",
)


def _make_flow_node(label: str, color, width: float = 1.82) -> VGroup:
    body = RoundedRectangle(
        width=width,
        height=0.72,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.3,
        fill_color=CARD_BG,
        fill_opacity=0.78,
    )
    text = SafeText(label, max_width=width - 0.20, max_height=0.24, font_size=15, color=TEXT)
    text.move_to(body)
    group = VGroup(body, text)
    group.box = body
    group.label = text
    return group


def make_grand_summary_flow() -> VGroup:
    colors = (INPUT, OUTPUT, SCIENCE, OPERATOR, PURPLE, INPUT, WARNING)
    nodes = VGroup(*[_make_flow_node(label, color) for label, color in zip(FLOW_LABELS, colors)])
    nodes.arrange(RIGHT, buff=0.26)
    arrows = VGroup(
        *[
            Arrow(
                nodes[i].get_right(),
                nodes[i + 1].get_left(),
                buff=0.08,
                color=GRID,
                stroke_width=1.8,
                max_tip_length_to_length_ratio=0.18,
            )
            for i in range(len(nodes) - 1)
        ]
    )
    group = VGroup(arrows, nodes)
    group.nodes = nodes
    group.arrows = arrows
    return group


def make_vector_icon() -> VGroup:
    bars = VGroup()
    heights = (0.28, 0.52, 0.38, 0.72, 0.44)
    for index, height in enumerate(heights):
        bar = RoundedRectangle(
            width=0.18,
            height=height,
            corner_radius=0.03,
            stroke_color=INPUT,
            stroke_width=0.8,
            fill_color=INPUT,
            fill_opacity=0.62,
        )
        bar.move_to(LEFT * 0.52 + RIGHT * index * 0.26 + DOWN * (0.72 - height) / 2)
        bars.add(bar)
    label = SafeText("R^n -> R^m", max_width=1.65, max_height=0.24, font_size=15, color=INPUT)
    label.next_to(bars, DOWN, buff=0.12)
    return VGroup(bars, label)


def make_function_icon() -> VGroup:
    panel = make_wave_panel("function space", color=OUTPUT, width=2.25, height=1.12, phase=0.3, freq=1.8)
    return panel


def make_solver_icon() -> VGroup:
    grid = VGroup()
    for row in range(4):
        for col in range(5):
            square = Square(side_length=0.20, stroke_color=GRID, stroke_width=0.7, fill_color=SCIENCE, fill_opacity=0.10)
            square.move_to(RIGHT * (col - 2) * 0.22 + DOWN * (row - 1.5) * 0.22)
            grid.add(square)
    formula = SafeMathTex(r"\Delta u=f", max_width=1.45, max_height=0.34, font_size=25, color=SCIENCE)
    formula.next_to(grid, DOWN, buff=0.14)
    return VGroup(grid, formula)


def make_solution_operator_icon() -> VGroup:
    left = SafeMathTex(r"a(x)", max_width=0.70, max_height=0.32, font_size=24, color=INPUT)
    right = SafeMathTex(r"u(x)", max_width=0.70, max_height=0.32, font_size=24, color=OUTPUT)
    right.next_to(left, RIGHT, buff=1.24)
    arrow = Arrow(left.get_right(), right.get_left(), buff=0.12, color=OPERATOR, stroke_width=3.0)
    label = SafeMathTex(r"\mathcal{G}", max_width=0.62, max_height=0.32, font_size=28, color=OPERATOR)
    label.next_to(arrow, UP, buff=0.08)
    return VGroup(left, arrow, label, right)


def make_architecture_motifs() -> VGroup:
    gno = Chip("GNO", max_width=0.92, height=0.42, stroke_color=INPUT, font_size=15)
    fno = Chip("FNO", max_width=0.88, height=0.42, stroke_color=OPERATOR, font_size=15)
    tno = Chip("Transformer NO", max_width=2.12, height=0.42, stroke_color=PURPLE, font_size=15)
    coda = Chip("CoDA-NO", max_width=1.34, height=0.42, stroke_color=SCIENCE, font_size=15)
    chips = VGroup(gno, fno, tno, coda).arrange(RIGHT, buff=0.16)
    spectrum = make_spectrum_bars(n=9, width=2.15, height=0.86, selected=3).scale(0.72)
    attention = make_attention_matrix(size=4, cell=0.22).scale(0.70)
    mini = VGroup(spectrum, attention).arrange(RIGHT, buff=0.42)
    return VGroup(chips, mini).arrange(DOWN, buff=0.18)


def make_domain_motifs() -> VGroup:
    labels = (
        ("weather", INPUT),
        ("CFD", OPERATOR),
        ("geophysics", PURPLE),
        ("materials", OUTPUT),
    )
    chips = VGroup(*[Chip(label, max_width=1.38 if len(label) > 3 else 0.82, height=0.42, stroke_color=color, font_size=14) for label, color in labels])
    chips.arrange(RIGHT, buff=0.18)
    orbit = Circle(radius=0.86, color=GRID, stroke_width=1.1, stroke_opacity=0.48)
    center = SafeMathTex(r"\mathcal{A}\to\mathcal{U}", max_width=1.36, max_height=0.34, font_size=24, color=TEXT)
    center.move_to(orbit)
    dots = VGroup()
    for index, (_, color) in enumerate(labels):
        angle = 2 * np.pi * index / len(labels)
        dots.add(Dot(orbit.get_center() + RIGHT * np.cos(angle) * 0.86 + UP * np.sin(angle) * 0.86, radius=0.045, color=color))
    return VGroup(chips, VGroup(orbit, center, dots)).arrange(DOWN, buff=0.16)


def make_open_problem_motifs() -> VGroup:
    board = make_open_problems_board().scale(0.72)
    extra = VGroup(
        Chip("chaos", max_width=1.02, height=0.42, stroke_color=WARNING, font_size=14),
        Chip("physics", max_width=1.12, height=0.42, stroke_color=OPERATOR, font_size=14),
        Chip("multi-dataset", max_width=1.90, height=0.42, stroke_color=PURPLE, font_size=14),
    ).arrange(RIGHT, buff=0.16)
    return VGroup(board, extra).arrange(DOWN, buff=0.18)


def make_motif_replay_tile(label: str, icon: VGroup, color, width: float = 3.12, height: float = 1.86) -> VGroup:
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.15,
        fill_color=CARD_BG,
        fill_opacity=0.70,
    )
    title = SafeText(label, max_width=width - 0.24, max_height=0.26, font_size=16, color=TEXT, weight="BOLD")
    title.move_to(frame.get_top() + DOWN * 0.22)
    icon.scale(min(1.0, (width - 0.38) / max(icon.width, 0.01), (height - 0.64) / max(icon.height, 0.01)))
    icon.move_to(frame.get_center() + DOWN * 0.14)
    group = VGroup(frame, title, icon)
    group.icon = icon
    return group


def make_motif_replays() -> VGroup:
    tiles = VGroup(
        make_motif_replay_tile("finite vectors", make_vector_icon(), INPUT),
        make_motif_replay_tile("functions", make_function_icon(), OUTPUT),
        make_motif_replay_tile("solvers", make_solver_icon(), SCIENCE),
        make_motif_replay_tile("solution operator", make_solution_operator_icon(), OPERATOR),
        make_motif_replay_tile("NO architectures", make_architecture_motifs(), PURPLE, width=3.85),
        make_motif_replay_tile("domains", make_domain_motifs(), INPUT, width=3.55),
        make_motif_replay_tile("open problems", make_open_problem_motifs(), WARNING, width=3.75),
    )
    return tiles


def make_final_operator_arrow() -> VGroup:
    left = RoundedRectangle(width=2.35, height=1.10, corner_radius=0.09, stroke_color=INPUT, stroke_width=1.7, fill_color=CARD_BG, fill_opacity=0.76)
    right = RoundedRectangle(width=2.35, height=1.10, corner_radius=0.09, stroke_color=OUTPUT, stroke_width=1.7, fill_color=CARD_BG, fill_opacity=0.76)
    left_label = SafeMathTex(r"\mathcal{A}", max_width=0.85, max_height=0.50, font_size=42, color=INPUT).move_to(left)
    right.next_to(left, RIGHT, buff=2.50)
    right_label = SafeMathTex(r"\mathcal{U}", max_width=0.85, max_height=0.50, font_size=42, color=OUTPUT).move_to(right)
    arrow = Arrow(left.get_right(), right.get_left(), buff=0.22, color=OPERATOR, stroke_width=5.0)
    label = SafeMathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}", max_width=3.45, max_height=0.50, font_size=38, color=OPERATOR)
    label.next_to(arrow, UP, buff=0.18)
    group = VGroup(left, left_label, arrow, label, right, right_label)
    group.formula_label = label
    return group.move_to(ORIGIN)


def make_learning_in_infinite_dimensions_title() -> VGroup:
    title = SafeText("Learning in infinite dimensions.", max_width=8.8, max_height=0.62, font_size=42, color=TEXT, weight="BOLD")
    underline = Line(LEFT * 3.0, RIGHT * 3.0, color=OPERATOR, stroke_width=2.0, stroke_opacity=0.86)
    underline.next_to(title, DOWN, buff=0.18)
    return VGroup(title, underline)


def make_beginning_line() -> VGroup:
    line = VMobject(color=SCIENCE, stroke_width=2.2, stroke_opacity=0.82)
    xs = np.linspace(-3.0, 3.0, 32)
    line.set_points_smoothly([[x, 0.18 * np.sin(1.7 * x), 0] for x in xs])
    text = SafeText("field này mới chỉ bắt đầu", max_width=5.0, max_height=0.36, font_size=24, color=SCIENCE)
    text.next_to(line, DOWN, buff=0.22)
    return VGroup(line, text)
