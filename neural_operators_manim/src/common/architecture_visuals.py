"""Reusable architecture visuals for neural-operator scenes."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Circle,
    Dot,
    Line,
    Rectangle,
    RoundedRectangle,
    Square,
    VGroup,
    VMobject,
)

from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING


def make_wave_panel(
    label: str,
    color=INPUT,
    width: float = 3.0,
    height: float = 1.55,
    phase: float = 0.0,
    freq: float = 1.35,
) -> VGroup:
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.25,
        fill_color=CARD_BG,
        fill_opacity=0.72,
    )
    axes = Axes(
        x_range=[0, 4, 1],
        y_range=[-1.2, 1.2, 1],
        x_length=width - 0.46,
        y_length=height - 0.62,
        tips=False,
        axis_config={"color": GRID, "stroke_width": 0.8, "include_ticks": False},
    )
    curve = axes.plot(
        lambda x: 0.58 * np.sin(freq * x + phase) + 0.18 * np.cos(2.6 * x),
        x_range=[0, 4],
        color=color,
        stroke_width=2.7,
    )
    label_mob = SafeText(label, max_width=width - 0.28, max_height=0.26, font_size=17, color=TEXT)
    content = VGroup(axes, curve).move_to(frame.get_center() + UP * 0.09)
    label_mob.move_to(frame.get_bottom() + UP * 0.17)
    group = VGroup(frame, content, label_mob)
    group.frame = frame
    group.curve = curve
    group.label = label_mob
    return group


def make_point_cloud(
    n: int = 24,
    width: float = 4.5,
    height: float = 2.8,
    seed: int = 10,
    color=INPUT,
) -> VGroup:
    rng = np.random.default_rng(seed)
    points = [
        np.array([
            rng.uniform(-width / 2, width / 2),
            rng.uniform(-height / 2, height / 2),
            0.0,
        ])
        for _ in range(n)
    ]
    dots = VGroup(*[Dot(point, radius=0.055, color=color, fill_opacity=0.90) for point in points])
    lines = VGroup()
    for i, point in enumerate(points):
        nearest = sorted(
            [(np.linalg.norm(point - other), other) for j, other in enumerate(points) if i != j],
            key=lambda item: item[0],
        )[:2]
        for dist, other in nearest:
            if dist < 1.25:
                lines.add(Line(point, other, color=GRID, stroke_width=1.0, stroke_opacity=0.45))
    query = Dot(np.array([width * 0.21, height * 0.11, 0.0]), radius=0.085, color=OUTPUT)
    radius = Circle(radius=1.05, color=OPERATOR, stroke_width=1.4, stroke_opacity=0.60).move_to(query)
    group = VGroup(lines, dots, radius, query)
    group.dots = dots
    group.lines = lines
    group.radius = radius
    group.query = query
    group.sample_points = points
    return group


def make_message_edges(point_cloud: VGroup, max_edges: int = 7) -> VGroup:
    query_center = point_cloud.query.get_center()
    ranked = sorted(
        [(np.linalg.norm(dot.get_center() - query_center), dot) for dot in point_cloud.dots],
        key=lambda item: item[0],
    )[:max_edges]
    return VGroup(
        *[
            Arrow(
                dot.get_center(),
                query_center,
                buff=0.10,
                color=OPERATOR,
                stroke_width=2.0,
                max_tip_length_to_length_ratio=0.08,
            )
            for _, dot in ranked
        ]
    )


def make_spectrum_bars(
    n: int = 13,
    width: float = 4.3,
    height: float = 1.9,
    selected: int = 5,
) -> VGroup:
    bars = VGroup()
    spacing = width / n
    for index in range(n):
        distance = abs(index - (n - 1) / 2)
        bar_height = height * (0.18 + 0.74 * np.exp(-0.25 * distance))
        color = OPERATOR if distance <= selected / 2 else GRID
        bar = Rectangle(
            width=spacing * 0.58,
            height=bar_height,
            stroke_color=color,
            stroke_width=1.0,
            fill_color=color,
            fill_opacity=0.72 if color == OPERATOR else 0.40,
        )
        bar.move_to(LEFT * width / 2 + RIGHT * (spacing * (index + 0.5)) + DOWN * (height - bar_height) / 2)
        bars.add(bar)
    axis = Line(LEFT * width / 2, RIGHT * width / 2, color=GRID, stroke_width=1.0)
    label = SafeText("selected modes", max_width=2.2, max_height=0.24, font_size=16, color=OPERATOR)
    label.next_to(bars, DOWN, buff=0.10)
    group = VGroup(axis, bars, label)
    group.bars = bars
    group.label = label
    return group


def make_coefficient_bars(values: list[float], color=PURPLE, width: float = 3.2, height: float = 1.7) -> VGroup:
    n = len(values)
    bars = VGroup()
    spacing = width / n
    for index, value in enumerate(values):
        bar_height = max(0.10, abs(value) * height)
        bar = Rectangle(
            width=spacing * 0.56,
            height=bar_height,
            stroke_color=color,
            stroke_width=1.0,
            fill_color=color,
            fill_opacity=0.66,
        )
        y_shift = bar_height / 2 if value >= 0 else -bar_height / 2
        bar.move_to(LEFT * width / 2 + RIGHT * (spacing * (index + 0.5)) + UP * y_shift)
        bars.add(bar)
    axis = Line(LEFT * width / 2, RIGHT * width / 2, color=GRID, stroke_width=1.0)
    return VGroup(axis, bars)


def make_attention_matrix(size: int = 6, cell: float = 0.34) -> VGroup:
    matrix = VGroup()
    for row in range(size):
        for col in range(size):
            weight = np.exp(-abs(row - col) / 1.8)
            color = OPERATOR if weight > 0.45 else GRID
            square = Square(
                side_length=cell,
                stroke_color=GRID,
                stroke_width=0.6,
                fill_color=color,
                fill_opacity=0.18 + 0.56 * weight,
            )
            square.move_to(RIGHT * (col - (size - 1) / 2) * cell + DOWN * (row - (size - 1) / 2) * cell)
            matrix.add(square)
    frame = RoundedRectangle(
        width=size * cell + 0.18,
        height=size * cell + 0.18,
        corner_radius=0.06,
        stroke_color=OPERATOR,
        stroke_width=1.1,
        fill_opacity=0,
    )
    label = SafeText("attention weights", max_width=2.5, max_height=0.24, font_size=16, color=OPERATOR)
    label.next_to(frame, DOWN, buff=0.10)
    group = VGroup(frame, matrix, label)
    group.cells = matrix
    return group


def make_variable_card(name: str, color=INPUT, width: float = 2.15, height: float = 1.22) -> VGroup:
    panel = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.15,
        fill_color=CARD_BG,
        fill_opacity=0.78,
    )
    title = SafeText(name, max_width=width - 0.24, max_height=0.24, font_size=16, color=TEXT)
    wave = VMobject(color=color, stroke_width=2.0)
    xs = np.linspace(-width / 2 + 0.24, width / 2 - 0.24, 22)
    wave.set_points_smoothly([[x, 0.18 * np.sin(4.4 * x + len(name)), 0] for x in xs])
    wave.move_to(panel.get_center() + UP * 0.03)
    title.move_to(panel.get_bottom() + UP * 0.17)
    group = VGroup(panel, wave, title)
    group.panel = panel
    group.wave = wave
    group.title = title
    return group


def make_stencil_grid(
    label: str,
    color=INPUT,
    cell: float = 0.36,
    center_color=OUTPUT,
    scale_label: str | None = None,
) -> VGroup:
    cells = VGroup()
    for row in range(3):
        for col in range(3):
            is_center = row == 1 and col == 1
            is_cross = is_center or row == 1 or col == 1
            square = Square(
                side_length=cell,
                stroke_color=color if is_cross else GRID,
                stroke_width=1.2 if is_cross else 0.7,
                fill_color=center_color if is_center else CARD_BG,
                fill_opacity=0.62 if is_center else 0.32,
            )
            square.move_to(RIGHT * (col - 1) * cell + DOWN * (row - 1) * cell)
            cells.add(square)
    title = SafeText(label, max_width=2.4, max_height=0.28, font_size=18, color=TEXT)
    title.next_to(cells, DOWN, buff=0.16)
    group = VGroup(cells, title)
    if scale_label:
        scale = Chip(scale_label, max_width=1.50, height=0.36, stroke_color=WARNING, font_size=14)
        scale.next_to(cells, UP, buff=0.12)
        group.add(scale)
        group.scale_label = scale
    group.cells = cells
    group.title = title
    return group.move_to(ORIGIN)


def make_kernel_formula(tex: str, color=OPERATOR, max_width: float = 3.6) -> VGroup:
    formula = SafeMathTex(tex, max_width=max_width - 0.28, max_height=0.48, font_size=27, color=color)
    box = RoundedRectangle(
        width=max_width,
        height=0.68,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.15,
        fill_color=CARD_BG,
        fill_opacity=0.80,
    )
    formula.move_to(box)
    return VGroup(box, formula)
