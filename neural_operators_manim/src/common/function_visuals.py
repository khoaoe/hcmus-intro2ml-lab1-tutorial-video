import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Circle,
    Dot,
    Ellipse,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    VMobject,
    interpolate_color,
)

from src.common.theme import (
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    PHYSICS,
    PURPLE,
    SCIENCE,
    TEXT,
    WARNING,
)


def smooth_path(points, color=INPUT, stroke_width=2.4, stroke_opacity=1.0):
    path = VMobject(color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
    path.set_points_smoothly([np.array(point, dtype=float) for point in points])
    return path


def make_mesh_overlay(width=2.4, height=1.55, nx=8, ny=5, color=TEXT):
    lines = VGroup()
    for i in range(nx + 1):
        x = -width / 2 + width * i / nx
        lines.add(
            Line(
                [x, -height / 2, 0],
                [x, height / 2, 0],
                color=color,
                stroke_width=0.75,
                stroke_opacity=0.38,
            )
        )
    for j in range(ny + 1):
        y = -height / 2 + height * j / ny
        lines.add(
            Line(
                [-width / 2, y, 0],
                [width / 2, y, 0],
                color=color,
                stroke_width=0.75,
                stroke_opacity=0.38,
            )
        )
    return lines


def make_weather_sphere_icon(radius=0.68):
    sphere = Circle(radius=radius, stroke_color=SCIENCE, stroke_width=1.8)
    sphere.set_fill("#092F3F", opacity=0.74)
    latitudes = VGroup(
        *[
            Ellipse(
                width=2 * radius * (0.92 - 0.08 * abs(i)),
                height=0.18,
                stroke_color=GRID,
                stroke_width=0.8,
                stroke_opacity=0.7,
            ).shift(UP * i * radius * 0.26)
            for i in range(-2, 3)
        ]
    )
    longitudes = VGroup(
        *[
            Ellipse(
                width=0.34 + 0.12 * abs(i),
                height=2 * radius,
                stroke_color=GRID,
                stroke_width=0.8,
                stroke_opacity=0.68,
            )
            for i in range(-2, 3)
        ]
    )
    bands = VGroup()
    for j, y in enumerate(np.linspace(-0.42, 0.42, 6)):
        length = 2 * np.sqrt(max(radius**2 - y**2, 0)) * 0.82
        color = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, WARNING, PURPLE][j]
        bands.add(
            Line(
                [-length / 2, y, 0],
                [length / 2, y, 0],
                color=color,
                stroke_width=5.0,
                stroke_opacity=0.36,
            )
        )
    arrows = VGroup()
    for x, y, dx, dy in [
        (-0.36, 0.32, 0.34, 0.04),
        (-0.18, -0.12, 0.32, 0.11),
        (0.18, 0.1, 0.26, -0.08),
    ]:
        arrows.add(
            Arrow(
                [x, y, 0],
                [x + dx, y + dy, 0],
                buff=0,
                color=TEXT,
                stroke_width=1.4,
                max_tip_length_to_length_ratio=0.22,
            )
        )
    label = MathTex(r"u(x,t)", color=TEXT, font_size=24).next_to(sphere, DOWN, buff=0.08)
    return VGroup(sphere, bands, latitudes, longitudes, arrows, label)


def make_seismic_wave_icon(width=1.8, height=1.15):
    frame = Rectangle(width=width, height=height, stroke_color=OPERATOR, stroke_width=1.5)
    frame.set_fill("#211B32", opacity=0.68)
    layers = VGroup()
    for j in range(4):
        y = -height / 2 + height * (j + 1) / 5
        layer = smooth_path(
            [
                [-width / 2, y + 0.06 * np.sin(j), 0],
                [-width / 4, y + 0.08 * np.cos(j + 0.2), 0],
                [0, y - 0.04 * np.sin(j + 0.5), 0],
                [width / 4, y + 0.07 * np.cos(j + 1), 0],
                [width / 2, y + 0.04 * np.sin(j + 2), 0],
            ],
            color=GRID,
            stroke_width=1.4,
            stroke_opacity=0.85,
        )
        layers.add(layer)
    source = Dot([-0.44, -0.26, 0], radius=0.045, color=WARNING)
    waves = VGroup()
    for radius in (0.22, 0.42, 0.62):
        wave = Arc(
            radius=radius,
            start_angle=0.08,
            angle=2.38,
            color=OPERATOR,
            stroke_width=2.0,
            stroke_opacity=0.7,
        )
        wave.shift(source.get_center())
        waves.add(wave)
    label = MathTex(r"p(x,t)", color=TEXT, font_size=24).next_to(frame, DOWN, buff=0.08)
    return VGroup(frame, layers, source, waves, label)


def make_car_cfd_icon(width=2.0, height=1.0):
    tunnel = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.06,
        stroke_color=INPUT,
        stroke_width=1.4,
        fill_color="#09243A",
        fill_opacity=0.62,
    )
    body = Polygon(
        [-0.48, -0.09, 0],
        [-0.32, 0.12, 0],
        [0.22, 0.16, 0],
        [0.48, -0.02, 0],
        [0.42, -0.14, 0],
        [-0.48, -0.14, 0],
        color=TEXT,
        fill_color=CARD_BG,
        fill_opacity=0.92,
        stroke_width=1.3,
    )
    wheels = VGroup(
        Circle(radius=0.07, color=MUTED, fill_color=MUTED, fill_opacity=0.9).shift(LEFT * 0.25 + DOWN * 0.14),
        Circle(radius=0.07, color=MUTED, fill_color=MUTED, fill_opacity=0.9).shift(RIGHT * 0.28 + DOWN * 0.14),
    )
    streamlines = VGroup()
    for y, color in [(-0.32, SCIENCE), (-0.14, INPUT), (0.04, NVIDIA_GREEN), (0.26, OPERATOR)]:
        streamlines.add(
            smooth_path(
                [
                    [-0.9, y, 0],
                    [-0.44, y + 0.08, 0],
                    [-0.02, y + 0.15 * np.cos(3 * y), 0],
                    [0.46, y - 0.08, 0],
                    [0.9, y + 0.03, 0],
                ],
                color=color,
                stroke_width=2.1,
                stroke_opacity=0.82,
            )
        )
    label = MathTex(r"u(x,t)", color=TEXT, font_size=24).next_to(tunnel, DOWN, buff=0.08)
    return VGroup(tunnel, streamlines, body, wheels, label)


def make_molecule_trajectory_icon(seed=7):
    rng = np.random.default_rng(seed)
    points = []
    for i in range(6):
        angle = i * 0.95
        points.append([0.46 * np.cos(angle), 0.32 * np.sin(angle) + rng.normal(0, 0.035), 0])
    bonds = VGroup(*[Line(points[i], points[i + 1], color=GRID, stroke_width=1.6) for i in range(len(points) - 1)])
    atoms = VGroup(
        *[
            Dot(point, radius=0.055 + 0.012 * (i % 2), color=[PURPLE, SCIENCE, INPUT][i % 3])
            for i, point in enumerate(points)
        ]
    )
    trajectory = smooth_path(
        [[-0.7, -0.36, 0], [-0.38, 0.28, 0], [0.04, -0.08, 0], [0.38, 0.34, 0], [0.76, -0.12, 0]],
        color=PURPLE,
        stroke_width=2.2,
        stroke_opacity=0.86,
    )
    label = MathTex(r"q(t)", color=TEXT, font_size=24).next_to(atoms, DOWN, buff=0.24)
    return VGroup(trajectory, bonds, atoms, label)


def make_deformation_mesh_icon(width=1.55, height=1.05, nx=5, ny=4):
    frame = Rectangle(width=width, height=height, stroke_color=NVIDIA_GREEN, stroke_width=1.4)
    frame.set_fill("#102A1E", opacity=0.48)

    def warp(x, y):
        push = 0.13 * np.exp(-((x - 0.2) ** 2 + (y - 0.12) ** 2) / 0.22)
        return np.array([x + 0.08 * np.sin(4 * y), y - push + 0.04 * np.sin(5 * x), 0])

    lines = VGroup()
    for i in range(nx + 1):
        x = -width / 2 + width * i / nx
        pts = [warp(x, -height / 2 + height * j / 18) for j in range(19)]
        lines.add(smooth_path(pts, color=NVIDIA_GREEN, stroke_width=1.1, stroke_opacity=0.72))
    for j in range(ny + 1):
        y = -height / 2 + height * j / ny
        pts = [warp(-width / 2 + width * i / 18, y) for i in range(19)]
        lines.add(smooth_path(pts, color=NVIDIA_GREEN, stroke_width=1.1, stroke_opacity=0.72))
    pressure = Arrow(UP * 0.72, UP * 0.32, color=OPERATOR, stroke_width=2.0, max_tip_length_to_length_ratio=0.22)
    label = MathTex(r"\sigma(x,t)", color=TEXT, font_size=22).next_to(frame, DOWN, buff=0.08)
    return VGroup(frame, lines, pressure, label)


def make_query_point_with_interpolation(width=2.6, height=1.65):
    mesh = make_mesh_overlay(width, height, 7, 5, color=TEXT)
    point = Dot([0.29, 0.18, 0], radius=0.055, color=OPERATOR)
    patch = smooth_path(
        [[-0.12, -0.05, 0], [0.12, 0.25, 0], [0.42, 0.28, 0], [0.62, -0.06, 0]],
        color=OPERATOR,
        stroke_width=2.0,
        stroke_opacity=0.82,
    )
    value = MathTex(r"u(y)", color=OPERATOR, font_size=24).next_to(point, UP, buff=0.08)
    return VGroup(mesh, patch, point, value)
