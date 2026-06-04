"""Reusable visuals for Section 12 open-problem scenes."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Circle,
    Dot,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Square,
    Triangle,
    VGroup,
    VMobject,
    PI,
)

from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING


def make_loss_bar() -> VGroup:
    frame = RoundedRectangle(width=3.0, height=1.25, corner_radius=0.08, stroke_color=OUTPUT, stroke_width=1.2, fill_color=CARD_BG, fill_opacity=0.75)
    axis = Line(LEFT * 1.15, RIGHT * 1.15, color=GRID, stroke_width=1.0)
    bar = Rectangle(width=0.45, height=0.30, stroke_color=OUTPUT, fill_color=OUTPUT, fill_opacity=0.75).move_to(axis.get_left() + RIGHT * 0.36 + UP * 0.15)
    label = Chip("MSE low", max_width=1.24, height=0.40, stroke_color=OUTPUT, font_size=14)
    label.next_to(frame, DOWN, buff=0.12)
    group = VGroup(frame, axis, bar, label)
    group.bar = bar
    return group


def make_rare_event_miss() -> VGroup:
    field = RoundedRectangle(width=3.2, height=1.55, corner_radius=0.08, stroke_color=WARNING, stroke_width=1.2, fill_color=CARD_BG, fill_opacity=0.75)
    curve = VMobject(color=INPUT, stroke_width=2.4)
    xs = np.linspace(-1.35, 1.35, 34)
    curve.set_points_smoothly([[x, 0.20 * np.sin(3.2 * x), 0] for x in xs])
    spike = Triangle(color=WARNING, fill_color=WARNING, fill_opacity=0.72).scale(0.16).move_to(RIGHT * 0.72 + UP * 0.35)
    miss = Line(LEFT * 0.22 + UP * 0.58, RIGHT * 0.22 + DOWN * 0.10, color=WARNING, stroke_width=2.4).move_to(spike)
    label = Chip("rare event missed", max_width=2.15, height=0.40, stroke_color=WARNING, font_size=14)
    label.next_to(field, DOWN, buff=0.12)
    group = VGroup(field, curve, spike, miss, label)
    group.spike = spike
    return group


def make_metric_gauges(labels: tuple[str, ...]) -> VGroup:
    gauges = VGroup()
    colors = (INPUT, OPERATOR, OUTPUT, SCIENCE, WARNING, PURPLE)
    for index, label in enumerate(labels):
        arc = Arc(radius=0.34, start_angle=PI, angle=-PI, color=colors[index % len(colors)], stroke_width=2.2)
        needle = Line(ORIGIN, RIGHT * 0.27 + UP * (0.08 - 0.025 * index), color=TEXT, stroke_width=1.5)
        caption = SafeText(label, max_width=2.50, max_height=0.50, font_size=14, color=TEXT)
        caption.next_to(arc, DOWN, buff=0.06)
        gauges.add(VGroup(arc, needle, caption))
    gauges.arrange_in_grid(rows=2, cols=3, buff=(0.32, 0.26))
    return gauges


def make_problem_formulation_card() -> VGroup:
    body = VGroup(
        Chip("metric", max_width=1.10, height=0.38, stroke_color=OUTPUT, font_size=14),
        Chip("domain value", max_width=1.65, height=0.38, stroke_color=SCIENCE, font_size=14),
        Chip("risk", max_width=0.82, height=0.38, stroke_color=WARNING, font_size=14),
    ).arrange(DOWN, buff=0.10)
    return PanelCard("problem formulation", body, width=3.15, height=2.10, accent_color=SCIENCE)


def make_mesh_error_plot() -> VGroup:
    meshes = VGroup()
    for i, n in enumerate((3, 5, 8)):
        grid = VGroup()
        for row in range(n):
            for col in range(n):
                grid.add(Square(side_length=0.12, stroke_color=GRID, stroke_width=0.45, fill_color=INPUT, fill_opacity=0.10 + 0.04 * i))
        grid.arrange_in_grid(rows=n, cols=n, buff=0.008)
        frame = RoundedRectangle(width=grid.width + 0.10, height=grid.height + 0.10, corner_radius=0.04, stroke_color=(INPUT, OPERATOR, OUTPUT)[i], stroke_width=1.0)
        frame.move_to(grid)
        meshes.add(VGroup(frame, grid))
    meshes.arrange(RIGHT, buff=0.42)
    curve_box = Rectangle(width=3.25, height=1.25, stroke_color=GRID, stroke_width=1.0)
    curve = VMobject(color=WARNING, stroke_width=2.3)
    xs = np.linspace(-1.35, 1.35, 28)
    curve.set_points_smoothly([[x, -0.35 + 0.70 * np.exp(-1.3 * (x + 1.35)), 0] for x in xs])
    label = SafeText("mesh change -> error behavior", max_width=3.4, max_height=0.26, font_size=17, color=TEXT)
    label.next_to(curve_box, DOWN, buff=0.12)
    plot = VGroup(curve_box, curve, label)
    group = VGroup(meshes, plot).arrange(RIGHT, buff=0.62)
    group.meshes = meshes
    group.plot = plot
    return group


def make_chaotic_trajectories() -> VGroup:
    curves = VGroup()
    colors = (INPUT, OUTPUT, OPERATOR, WARNING)
    for i, color in enumerate(colors):
        curve = VMobject(color=color, stroke_width=2.2, stroke_opacity=0.78)
        ts = np.linspace(-1.65, 1.65, 40)
        curve.set_points_smoothly([[t, 0.12 * np.sin(2.5 * t) + (0.06 * i) * np.exp(0.8 * (t + 0.6)), 0] for t in ts])
        curves.add(curve)
    label = SafeText("nearby initial states diverge", max_width=3.5, max_height=0.28, font_size=18, color=WARNING)
    label.next_to(curves, DOWN, buff=0.16)
    return VGroup(curves, label)


def make_probability_cone() -> VGroup:
    cone = Polygon(LEFT * 1.45 + DOWN * 0.62, LEFT * 1.45 + UP * 0.62, RIGHT * 1.55 + UP * 0.95, RIGHT * 1.55 + DOWN * 0.95, color=PURPLE, stroke_width=1.2, fill_color=PURPLE, fill_opacity=0.14)
    center = VMobject(color=OUTPUT, stroke_width=2.4)
    xs = np.linspace(-1.35, 1.35, 34)
    center.set_points_smoothly([[x, 0.18 * np.sin(1.8 * x), 0] for x in xs])
    label = Chip("distribution, not one line", max_width=2.90, height=0.40, stroke_color=PURPLE, font_size=14)
    label.next_to(cone, DOWN, buff=0.14)
    return VGroup(cone, center, label)


def make_uncertainty_stack() -> VGroup:
    chips = VGroup(
        Chip("calibrated uncertainty", max_width=2.55, height=0.40, stroke_color=PURPLE, font_size=14),
        Chip("probabilistic NO", max_width=2.20, height=0.40, stroke_color=INPUT, font_size=14),
        Chip("ensembles", max_width=1.35, height=0.40, stroke_color=OUTPUT, font_size=14),
        Chip("conformal prediction", max_width=2.45, height=0.40, stroke_color=SCIENCE, font_size=14),
        Chip("sampling in function space", max_width=2.90, height=0.40, stroke_color=OPERATOR, font_size=14),
    ).arrange(RIGHT, buff=0.18)
    return chips


def make_dataset_tile(name: str, color, variables: tuple[str, ...], width: float = 2.35) -> VGroup:
    chips = VGroup(
        *[
            Chip(
                var,
                max_width=width - 0.34,
                height=0.42,
                stroke_color=color,
                font_size=13,
            )
            for var in variables
        ]
    )
    chips.arrange(DOWN, buff=0.06)
    tile = PanelCard(name, chips, width=width, height=2.35, accent_color=color, title_font_size=18)
    return tile


def make_dataset_tiles() -> VGroup:
    tiles = VGroup(
        make_dataset_tile("weather", INPUT, ("temp", "wind", "humidity")),
        make_dataset_tile("CFD", OPERATOR, ("pressure", "velocity", "mesh")),
        make_dataset_tile("seismic", PURPLE, ("source", "sensors", "waves")),
        make_dataset_tile("materials", OUTPUT, ("stress", "strain", "geometry")),
    ).arrange(RIGHT, buff=0.26)
    return tiles


def make_variable_alignment_graph() -> VGroup:
    left = VGroup(
        Chip("pressure", max_width=1.35, height=0.42, stroke_color=OPERATOR, font_size=13),
        Chip("velocity", max_width=1.32, height=0.42, stroke_color=OUTPUT, font_size=13),
        Chip("temp", max_width=0.98, height=0.42, stroke_color=INPUT, font_size=13),
    ).arrange(DOWN, buff=0.18)
    right = VGroup(
        Chip("metadata", max_width=1.48, height=0.42, stroke_color=SCIENCE, font_size=13),
        Chip("geometry", max_width=1.42, height=0.42, stroke_color=PURPLE, font_size=13),
        Chip("codomain attention", max_width=2.48, height=0.42, stroke_color=OPERATOR, font_size=13),
    ).arrange(DOWN, buff=0.18)
    right.next_to(left, RIGHT, buff=1.20)
    edges = VGroup(*[Line(left[i].get_right(), right[min(i, len(right) - 1)].get_left(), color=GRID, stroke_width=1.1, stroke_opacity=0.62) for i in range(len(left))])
    group = VGroup(edges, left, right)
    group.edges = edges
    return group


def make_foundation_silhouette() -> VGroup:
    core = RoundedRectangle(width=3.20, height=1.40, corner_radius=0.10, stroke_color=SCIENCE, stroke_width=1.5, fill_color=SCIENCE, fill_opacity=0.12)
    title = SafeText("operator foundation model", max_width=2.90, max_height=0.30, font_size=18, color=TEXT, weight="BOLD").move_to(core.get_center() + UP * 0.20)
    tags = VGroup(
        Chip("function spaces", max_width=1.88, height=0.42, stroke_color=INPUT, font_size=13),
        Chip("geometry", max_width=1.42, height=0.42, stroke_color=PURPLE, font_size=13),
        Chip("physics", max_width=1.12, height=0.42, stroke_color=OPERATOR, font_size=13),
        Chip("uncertainty", max_width=1.52, height=0.42, stroke_color=WARNING, font_size=13),
    ).arrange(RIGHT, buff=0.08)
    tags.move_to(core.get_center() + DOWN * 0.35)
    return VGroup(core, title, tags)


def make_balance_scale() -> VGroup:
    base = Line(LEFT * 2.2, RIGHT * 2.2, color=GRID, stroke_width=2.0)
    pivot = Triangle(color=SCIENCE, fill_color=SCIENCE, fill_opacity=0.45).scale(0.22).rotate(PI).move_to(DOWN * 0.36)
    beam = Line(LEFT * 1.95 + UP * 0.38, RIGHT * 1.95 + UP * 0.12, color=TEXT, stroke_width=2.2)
    left_pan = RoundedRectangle(width=1.65, height=0.50, corner_radius=0.06, stroke_color=INPUT, fill_color=INPUT, fill_opacity=0.12).move_to(LEFT * 1.55 + DOWN * 0.10)
    right_pan = RoundedRectangle(width=1.65, height=0.50, corner_radius=0.06, stroke_color=OPERATOR, fill_color=OPERATOR, fill_opacity=0.12).move_to(RIGHT * 1.55 + DOWN * 0.10)
    left_label = SafeText("flexibility", max_width=1.45, max_height=0.22, font_size=15, color=INPUT).move_to(left_pan)
    right_label = SafeText("physics prior", max_width=1.45, max_height=0.22, font_size=15, color=OPERATOR).move_to(right_pan)
    return VGroup(base, pivot, beam, left_pan, right_pan, left_label, right_label)


def make_physics_prior_blocks() -> VGroup:
    blocks = VGroup(
        Chip("symmetry", max_width=1.38, height=0.42, stroke_color=PURPLE, font_size=14),
        Chip("conservation", max_width=1.80, height=0.42, stroke_color=SCIENCE, font_size=14),
        Chip("boundary", max_width=1.36, height=0.42, stroke_color=WARNING, font_size=14),
        Chip("basis", max_width=0.94, height=0.42, stroke_color=INPUT, font_size=14),
        Chip("local kernels", max_width=1.70, height=0.42, stroke_color=OPERATOR, font_size=14),
        Chip("PDE loss", max_width=1.22, height=0.42, stroke_color=OUTPUT, font_size=14),
    ).arrange_in_grid(rows=2, cols=3, buff=(0.15, 0.14))
    operator = RoundedRectangle(width=3.9, height=0.72, corner_radius=0.08, stroke_color=SCIENCE, stroke_width=1.3, fill_color=CARD_BG, fill_opacity=0.72)
    label = SafeText("neural operator block", max_width=3.5, max_height=0.26, font_size=18, color=TEXT).move_to(operator)
    return VGroup(blocks, VGroup(operator, label)).arrange(DOWN, buff=0.28)


def make_collaboration_network() -> VGroup:
    names = ("ML", "applied math", "physics", "engineering", "domain expert")
    colors = (INPUT, PURPLE, OPERATOR, OUTPUT, SCIENCE)
    nodes = VGroup()
    for i, (name, color) in enumerate(zip(names, colors)):
        angle = 2 * np.pi * i / len(names)
        chip = Chip(name, max_width=1.68 if len(name) < 8 else 2.30, height=0.42, stroke_color=color, font_size=13)
        chip.move_to(np.array([1.75 * np.cos(angle), 1.0 * np.sin(angle), 0]))
        nodes.add(chip)
    edges = VGroup()
    for i in range(len(nodes)):
        edges.add(Line(nodes[i].get_center(), nodes[(i + 1) % len(nodes)].get_center(), color=GRID, stroke_width=1.0, stroke_opacity=0.55))
    return VGroup(edges, nodes)


def make_open_problems_board() -> VGroup:
    items = VGroup(
        Chip("accuracy", max_width=1.38, height=0.42, stroke_color=WARNING, font_size=14),
        Chip("metrics", max_width=1.20, height=0.42, stroke_color=OUTPUT, font_size=14),
        Chip("scaling", max_width=1.18, height=0.42, stroke_color=PURPLE, font_size=14),
        Chip("OOD behavior", max_width=1.78, height=0.42, stroke_color=WARNING, font_size=14),
        Chip("uncertainty", max_width=1.58, height=0.42, stroke_color=INPUT, font_size=14),
        Chip("discretization", max_width=1.96, height=0.42, stroke_color=SCIENCE, font_size=14),
    ).arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.18))
    board = PanelCard("open problems", items, width=5.6, height=2.35, accent_color=WARNING)
    return board


def make_function_space_diagram() -> VGroup:
    left = RoundedRectangle(width=2.15, height=1.16, corner_radius=0.08, stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.72)
    right = RoundedRectangle(width=2.15, height=1.16, corner_radius=0.08, stroke_color=OUTPUT, fill_color=CARD_BG, fill_opacity=0.72)
    left_label = SafeMathTex(r"\mathcal{A}", max_width=0.75, max_height=0.45, font_size=34, color=INPUT).move_to(left)
    right_label = SafeMathTex(r"\mathcal{U}", max_width=0.75, max_height=0.45, font_size=34, color=OUTPUT).move_to(right)
    right.next_to(left, RIGHT, buff=2.35)
    right_label.move_to(right)
    arrow = Arrow(left.get_right(), right.get_left(), buff=0.20, color=OPERATOR, stroke_width=4.0)
    label = SafeMathTex(r"\mathcal{G}", max_width=0.8, max_height=0.42, font_size=34, color=OPERATOR)
    label.next_to(arrow, UP, buff=0.12)
    return VGroup(left, left_label, arrow, label, right, right_label)


def make_domain_orbit() -> VGroup:
    center = make_function_space_diagram().scale(0.72)
    domains = VGroup(
        Chip("weather", max_width=1.18, height=0.42, stroke_color=INPUT, font_size=13),
        Chip("CFD", max_width=0.82, height=0.42, stroke_color=OPERATOR, font_size=13),
        Chip("molecules", max_width=1.42, height=0.42, stroke_color=OUTPUT, font_size=13),
        Chip("geophysics", max_width=1.58, height=0.42, stroke_color=PURPLE, font_size=13),
    )
    positions = [UP * 1.55, RIGHT * 3.0, DOWN * 1.55, LEFT * 3.0]
    for chip, pos in zip(domains, positions):
        chip.move_to(pos)
    orbit = Circle(radius=2.55, color=GRID, stroke_width=1.0, stroke_opacity=0.45)
    return VGroup(orbit, center, domains)
