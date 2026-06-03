"""Domain-focused visuals for Section 11 scenes."""

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
    Ellipse,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Square,
    Triangle,
    VGroup,
    VMobject,
    PI,
    TAU,
)

from src.common.architecture_visuals import make_wave_panel
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING


def make_domain_pillar(title: str, color, labels: tuple[str, ...], width: float = 2.35) -> VGroup:
    icon = Circle(radius=0.30, stroke_color=color, stroke_width=1.4, fill_color=color, fill_opacity=0.18)
    title_mob = SafeText(title, max_width=width - 0.22, max_height=0.28, font_size=18, color=TEXT, weight="BOLD")
    body = VGroup(*[Chip(label, max_width=width - 0.18, height=0.38, stroke_color=color, font_size=13) for label in labels])
    body.arrange(DOWN, buff=0.06)
    column = VGroup(icon, title_mob, body).arrange(DOWN, buff=0.13)
    base = RoundedRectangle(
        width=width,
        height=column.height + 0.36,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.2,
        fill_color=CARD_BG,
        fill_opacity=0.70,
    )
    column.move_to(base)
    group = VGroup(base, column)
    group.icon = icon
    group.title_mob = title_mob
    group.body = body
    return group


def make_sphere_field(label: str = "sphere domain", radius: float = 1.25) -> VGroup:
    globe = Circle(radius=radius, stroke_color=SCIENCE, stroke_width=1.6, fill_color=INPUT, fill_opacity=0.16)
    latitudes = VGroup(*[
        Ellipse(width=2 * radius * np.cos(lat), height=0.30, color=GRID, stroke_width=0.8, stroke_opacity=0.62).shift(UP * radius * np.sin(lat))
        for lat in np.linspace(-0.75, 0.75, 4)
    ])
    longitudes = VGroup(*[
        Ellipse(width=2 * radius * (0.22 + 0.18 * i), height=2 * radius, color=GRID, stroke_width=0.7, stroke_opacity=0.52)
        for i in range(4)
    ])
    bands = VGroup()
    for i, y in enumerate(np.linspace(-0.52, 0.52, 4)):
        curve = VMobject(color=[INPUT, SCIENCE, OPERATOR, OUTPUT][i], stroke_width=3.4, stroke_opacity=0.78)
        xs = np.linspace(-radius * 0.82, radius * 0.82, 24)
        curve.set_points_smoothly([[x, y + 0.06 * np.sin(4 * x + i), 0] for x in xs])
        bands.add(curve)
    label_mob = SafeText(label, max_width=2.7, max_height=0.28, font_size=18, color=TEXT)
    label_mob.next_to(globe, DOWN, buff=0.18)
    group = VGroup(globe, latitudes, longitudes, bands, label_mob)
    group.globe = globe
    group.bands = bands
    return group


def make_ensemble_futures(count: int = 6, width: float = 3.3, height: float = 1.75) -> VGroup:
    curves = VGroup()
    for i in range(count):
        curve = VMobject(color=OUTPUT, stroke_width=1.6, stroke_opacity=0.28 + 0.08 * i)
        xs = np.linspace(-width / 2, width / 2, 30)
        curve.set_points_smoothly([[x, 0.18 * np.sin(2.2 * x + i * 0.55) + (i - count / 2) * height / (count * 2.4), 0] for x in xs])
        curves.add(curve)
    band = RoundedRectangle(width=width + 0.35, height=height, corner_radius=0.08, stroke_color=OUTPUT, stroke_width=1.1, fill_color=OUTPUT, fill_opacity=0.08)
    label = SafeText("ensemble futures", max_width=2.6, max_height=0.28, font_size=18, color=OUTPUT)
    label.next_to(band, DOWN, buff=0.14)
    group = VGroup(band, curves, label)
    group.curves = curves
    return group


def make_subsurface_panel(label: str = "subsurface field", width: float = 4.2, height: float = 2.35) -> VGroup:
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.08, stroke_color=SCIENCE, stroke_width=1.25, fill_color=CARD_BG, fill_opacity=0.75)
    layers = VGroup()
    colors = [GRID, PURPLE, SCIENCE, OPERATOR]
    for i in range(4):
        y = frame.get_top()[1] - 0.42 - i * 0.45
        curve = VMobject(color=colors[i], stroke_width=2.0, stroke_opacity=0.75)
        xs = np.linspace(-width / 2 + 0.25, width / 2 - 0.25, 22)
        curve.set_points_smoothly([[x, y + 0.07 * np.sin(2.4 * x + i), 0] for x in xs])
        layers.add(curve)
    label_mob = SafeText(label, max_width=width - 0.25, max_height=0.28, font_size=18, color=TEXT)
    label_mob.move_to(frame.get_bottom() + UP * 0.18)
    group = VGroup(frame, layers, label_mob)
    group.layers = layers
    return group


def make_surface_sensors(count: int = 7) -> VGroup:
    sensors = VGroup()
    for i in range(count):
        base = Triangle(color=OUTPUT, fill_color=OUTPUT, fill_opacity=0.75, stroke_width=0.8).scale(0.11)
        base.rotate(PI)
        base.shift(RIGHT * (i - (count - 1) / 2) * 0.42)
        sensors.add(base)
    label = SafeText("surface sensors", max_width=2.2, max_height=0.24, font_size=15, color=OUTPUT)
    label.next_to(sensors, UP, buff=0.12)
    return VGroup(sensors, label)


def make_reservoir_cross_section() -> VGroup:
    section = make_subsurface_panel("reservoir cross-section", width=5.2, height=2.55)
    well = Line(UP * 1.05, DOWN * 0.75, color=WARNING, stroke_width=4.0).move_to(section.get_center() + LEFT * 1.35)
    cap = Triangle(color=WARNING, fill_color=WARNING, fill_opacity=0.85).scale(0.12).move_to(well.get_top() + UP * 0.12)
    plume = Circle(radius=0.45, stroke_color=OPERATOR, stroke_width=1.4, fill_color=OPERATOR, fill_opacity=0.28).move_to(section.get_center() + LEFT * 0.58 + DOWN * 0.45)
    label = Chip("CO2 plume", max_width=1.65, height=0.40, stroke_color=OPERATOR, font_size=14)
    label.next_to(plume, RIGHT, buff=0.10)
    group = VGroup(section, well, cap, plume, label)
    group.section = section
    group.well = VGroup(well, cap)
    group.plume = plume
    return group


def make_scenario_grid(rows: int = 2, cols: int = 4) -> VGroup:
    panels = VGroup()
    for i in range(rows * cols):
        plume = Circle(radius=0.12 + 0.018 * (i % 4), stroke_color=OPERATOR, fill_color=OPERATOR, fill_opacity=0.24 + 0.05 * (i % 3))
        panel = RoundedRectangle(width=0.82, height=0.54, corner_radius=0.05, stroke_color=GRID, stroke_width=0.8, fill_color=CARD_BG, fill_opacity=0.75)
        plume.move_to(panel)
        panels.add(VGroup(panel, plume))
    panels.arrange_in_grid(rows=rows, cols=cols, buff=0.10)
    label = SafeText("many scenarios", max_width=2.2, max_height=0.24, font_size=15, color=TEXT)
    label.next_to(panels, DOWN, buff=0.12)
    return VGroup(panels, label)


def make_molecule_graph() -> VGroup:
    positions = [LEFT * 0.75, LEFT * 0.22 + UP * 0.42, RIGHT * 0.28 + UP * 0.12, RIGHT * 0.74 + DOWN * 0.36, LEFT * 0.30 + DOWN * 0.46]
    bonds = VGroup(*[Line(positions[i], positions[(i + 1) % len(positions)], color=GRID, stroke_width=2.0) for i in range(len(positions))])
    atoms = VGroup(*[Dot(point, radius=0.095, color=[INPUT, OUTPUT, OPERATOR, PURPLE, SCIENCE][i]) for i, point in enumerate(positions)])
    label = SafeText("molecule frames", max_width=2.2, max_height=0.26, font_size=17, color=TEXT)
    label.next_to(VGroup(bonds, atoms), DOWN, buff=0.16)
    return VGroup(bonds, atoms, label)


def make_trajectory_tube() -> VGroup:
    tube = VGroup()
    for i, color in enumerate((INPUT, OUTPUT, OPERATOR)):
        curve = VMobject(color=color, stroke_width=3.0, stroke_opacity=0.72)
        ts = np.linspace(-2.1, 2.1, 32)
        curve.set_points_smoothly([[t, 0.36 * np.sin(1.3 * t + i * 0.8) + 0.22 * i - 0.25, 0] for t in ts])
        tube.add(curve)
    label = SafeText("continuous trajectory function", max_width=3.7, max_height=0.28, font_size=18, color=OUTPUT)
    label.next_to(tube, DOWN, buff=0.16)
    return VGroup(tube, label)


def make_car_mesh() -> VGroup:
    body = Polygon(LEFT * 1.8 + DOWN * 0.2, LEFT * 1.35 + UP * 0.35, RIGHT * 0.55 + UP * 0.45, RIGHT * 1.65 + DOWN * 0.05, RIGHT * 1.35 + DOWN * 0.38, LEFT * 1.65 + DOWN * 0.38, color=INPUT, stroke_width=2.0, fill_color=INPUT, fill_opacity=0.13)
    wheels = VGroup(Circle(radius=0.22, color=GRID).shift(LEFT * 1.15 + DOWN * 0.42), Circle(radius=0.22, color=GRID).shift(RIGHT * 0.95 + DOWN * 0.42))
    mesh = VGroup()
    for x in np.linspace(-1.7, 1.5, 8):
        mesh.add(Line([x, -0.65, 0], [x + 0.18, 0.60, 0], color=GRID, stroke_width=0.7, stroke_opacity=0.55))
    label = SafeText("car geometry + mesh", max_width=3.2, max_height=0.28, font_size=18, color=TEXT)
    label.next_to(VGroup(body, wheels, mesh), DOWN, buff=0.16)
    return VGroup(mesh, body, wheels, label)


def make_pressure_field() -> VGroup:
    panel = make_wave_panel("pressure / velocity field", color=OUTPUT, width=3.5, height=1.45, freq=2.6)
    boundary = RoundedRectangle(width=1.25, height=0.38, corner_radius=0.05, stroke_color=WARNING, stroke_width=1.6, fill_color=WARNING, fill_opacity=0.12)
    boundary.move_to(panel.get_top() + DOWN * 0.45 + RIGHT * 0.42)
    badge = Chip("sharp boundary", max_width=1.95, height=0.40, stroke_color=WARNING, font_size=14)
    badge.next_to(boundary, UP, buff=0.08)
    return VGroup(panel, boundary, badge)


def make_conservation_gauge(label: str = "conservation") -> VGroup:
    arc = Arc(radius=0.82, start_angle=PI, angle=-PI, color=SCIENCE, stroke_width=4.0)
    needle = Line(ORIGIN, RIGHT * 0.62 + UP * 0.18, color=WARNING, stroke_width=3.0)
    title = Chip(label, max_width=1.85, height=0.38, stroke_color=SCIENCE, font_size=14)
    title.next_to(arc, DOWN, buff=0.12)
    return VGroup(arc, needle, title)


def make_tipping_curve() -> VGroup:
    axes = Rectangle(width=3.4, height=1.7, stroke_color=GRID, stroke_width=1.0)
    curve = VMobject(color=WARNING, stroke_width=2.8)
    xs = np.linspace(-1.45, 1.45, 32)
    curve.set_points_smoothly([[x, -0.52 + 1.05 / (1 + np.exp(-5 * (x - 0.15))), 0] for x in xs])
    threshold = Line(UP * 0.82, DOWN * 0.82, color=OPERATOR, stroke_width=1.4, stroke_opacity=0.75).shift(RIGHT * 0.22)
    label = SafeText("tipping point", max_width=2.2, max_height=0.26, font_size=17, color=WARNING)
    label.next_to(axes, DOWN, buff=0.12)
    return VGroup(axes, curve, threshold, label)


def make_leaderboard_card() -> VGroup:
    rows = VGroup(
        Chip("L2 snapshot: low", max_width=2.35, height=0.42, stroke_color=OUTPUT, font_size=14),
        Chip("residual: FAIL", max_width=2.35, height=0.42, stroke_color=WARNING, font_size=14),
        Chip("calibration: unknown", max_width=2.35, height=0.42, stroke_color=PURPLE, font_size=14),
    ).arrange(DOWN, buff=0.08)
    crack = Line(LEFT * 0.20 + UP * 0.62, RIGHT * 0.15 + DOWN * 0.62, color=WARNING, stroke_width=2.0)
    return PanelCard("leaderboard", VGroup(rows, crack), width=2.85, height=2.05, accent_color=WARNING)
