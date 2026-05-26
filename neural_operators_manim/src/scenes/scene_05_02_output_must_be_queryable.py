"""
Scene 5.2 - Output must be queryable
Script: ../docs/full_voice_manim_script.md
Global time: 31:20.0-33:05.0
Local duration: 105.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import make_mesh_overlay, smooth_path
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    PURPLE,
    SCIENCE,
    TEXT,
    WARNING,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


VO_LINES = (
    (0.0, 11.0, "Requirement thứ hai: output của model nên có thể query ở bất kỳ điểm nào ta cần."),
    (11.0, 24.5, "Không phải vì ta thích đẹp. Mà vì physics thường hỏi local derivative, boundary value, surface integral, hoặc average over region."),
    (24.5, 37.0, "Trong car design, drag liên quan đến tích phân pressure trên bề mặt xe."),
    (37.0, 49.0, "Trong weather, energy và flux cũng là các đại lượng tích phân trên domain."),
    (49.0, 50.0, "Pause: 1.0s."),
    (50.0, 65.5, "Nếu output chỉ là một tensor cố định, ta có thể interpolate sau đó. Nhưng khi đó interpolation không còn là phần được học và kiểm soát trong architecture."),
    (65.5, 105.0, "Neural operator muốn output thật sự là một function approximation: ta đưa query point `y` vào, và model trả ra giá trị `u(y)`."),
)


def value_at_point(point):
    x = float(point[0])
    y = float(point[1])
    return np.sin(1.4 * x) + 0.5 * np.cos(1.8 * y) + 0.15 * x * y


def _field_color(value):
    normalized = np.clip((value + 1.7) / 3.4, 0.0, 0.999)
    colors = [PURPLE, INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR]
    return colors[int(normalized * (len(colors) - 1))]


def make_output_field(width=7.2, height=3.9, resolution=(18, 10)):
    nx, ny = resolution
    cells = VGroup()
    for ix in range(nx):
        for iy in range(ny):
            x = -width / 2 + width * (ix + 0.5) / nx
            y = -height / 2 + height * (iy + 0.5) / ny
            value = value_at_point([x, y, 0])
            cells.add(
                Rectangle(
                    width=width / nx + 0.01,
                    height=height / ny + 0.01,
                    stroke_width=0,
                    fill_color=_field_color(value),
                    fill_opacity=0.58,
                ).move_to([x, y, 0])
            )
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=SCIENCE,
        stroke_width=1.3,
        stroke_opacity=0.75,
        fill_opacity=0,
    )
    grid = make_mesh_overlay(width=width, height=height, nx=8, ny=5, color=TEXT)
    grid.set_opacity(0.55)
    field = VGroup(cells, grid, frame)
    field.cells = cells
    field.grid = grid
    field.frame = frame
    return field


def make_query_label(dot):
    def _label():
        value = value_at_point(dot.get_center())
        label = Chip(f"u(y) = {value:+.2f}", max_width=2.10, height=0.46, stroke_color=OPERATOR, font_size=18)
        label.next_to(dot, UP + RIGHT, buff=0.14)
        return label

    return always_redraw(_label)


def make_derivative_stencil(center):
    offsets = [LEFT * 0.44, RIGHT * 0.44, UP * 0.44, DOWN * 0.44]
    samples = VGroup(*[Dot(center + offset, radius=0.055, color=OPERATOR) for offset in offsets])
    cross = VGroup(
        Line(center + LEFT * 0.56, center + RIGHT * 0.56, color=OPERATOR, stroke_width=2.0),
        Line(center + DOWN * 0.56, center + UP * 0.56, color=OPERATOR, stroke_width=2.0),
    )
    arrows = VGroup(
        Arrow(center + LEFT * 0.70, center + LEFT * 0.30, buff=0, color=INPUT, stroke_width=1.8, max_tip_length_to_length_ratio=0.22),
        Arrow(center + DOWN * 0.70, center + DOWN * 0.30, buff=0, color=INPUT, stroke_width=1.8, max_tip_length_to_length_ratio=0.22),
    )
    label = Chip("local derivative", max_width=2.35, height=0.48, stroke_color=INPUT, font_size=18)
    label.next_to(center + DOWN * 0.70 + RIGHT * 0.20, DOWN, buff=0.14)
    return VGroup(cross, samples, arrows, label)


def make_initial_output_view():
    field = make_output_field()
    not_tensor = SafeText("output ≠ fixed tensor", max_width=4.8, max_height=0.46, font_size=32, color=WARNING, weight="BOLD")
    as_function = SafeText("output ≈ function u(y)", max_width=5.4, max_height=0.46, font_size=32, color=OPERATOR, weight="BOLD")
    title_group = VGroup(not_tensor, as_function).arrange(DOWN, buff=0.14)
    title_group.next_to(field, UP, buff=0.30)
    view = VGroup(field, title_group).move_to(ORIGIN)
    view.field = field
    view.not_tensor = not_tensor
    view.as_function = as_function
    return view


def make_query_motion_view():
    field = make_output_field()
    field.grid.set_opacity(0.12)
    dot = Dot([-2.25, -0.65, 0], radius=0.085, color=OPERATOR)
    path = smooth_path(
        [
            [-2.25, -0.65, 0],
            [-1.20, 1.05, 0],
            [0.55, 0.58, 0],
            [1.78, -0.82, 0],
        ],
        color=OPERATOR,
        stroke_width=2.0,
        stroke_opacity=0.38,
    )
    label = make_query_label(dot)
    y_label = SafeMathTex(r"y", max_width=0.45, max_height=0.34, font_size=26, color=TEXT)
    y_label.add_updater(lambda mob: mob.next_to(dot, DOWN, buff=0.08))
    group = VGroup(field, path, dot, label, y_label).move_to(ORIGIN)
    group.field = field
    group.path = path
    group.dot = dot
    group.value_label = label
    group.y_label = y_label
    return group


def make_surface_integral_demo():
    body = Polygon(
        [-2.85, -0.28, 0],
        [-2.35, 0.18, 0],
        [-1.40, 0.36, 0],
        [-0.40, 0.35, 0],
        [0.68, 0.18, 0],
        [2.18, 0.04, 0],
        [2.72, -0.22, 0],
        [1.90, -0.42, 0],
        [-2.55, -0.46, 0],
        stroke_color=TEXT,
        stroke_width=1.7,
        fill_color=CARD_BG,
        fill_opacity=0.70,
    )
    path_points = [
        [-2.50, -0.44, 0],
        [-1.60, -0.45, 0],
        [-0.40, -0.44, 0],
        [0.85, -0.38, 0],
        [2.05, -0.30, 0],
        [2.48, -0.18, 0],
        [1.65, 0.03, 0],
        [0.42, 0.18, 0],
        [-0.70, 0.31, 0],
        [-1.80, 0.26, 0],
        [-2.48, 0.02, 0],
    ]
    surface_path = smooth_path(path_points, color=OPERATOR, stroke_width=4.0, stroke_opacity=0.96)
    pressure_dots = VGroup()
    for i, point in enumerate(path_points):
        pressure_dots.add(Dot(point, radius=0.045 + 0.010 * (i % 3), color=[INPUT, SCIENCE, WARNING][i % 3]))
    flow = VGroup(
        Arrow(LEFT * 3.40 + UP * 0.90, LEFT * 2.62 + UP * 0.72, buff=0, color=INPUT, stroke_width=2.0),
        Arrow(LEFT * 3.40, LEFT * 2.62 + UP * 0.02, buff=0, color=INPUT, stroke_width=2.0),
        Arrow(LEFT * 3.40 + DOWN * 0.90, LEFT * 2.62 + DOWN * 0.72, buff=0, color=INPUT, stroke_width=2.0),
    )
    formula = SafeMathTex(
        r"\text{drag} \propto \int_{\text{surface}} p(y)n(y)\,dS",
        max_width=6.8,
        max_height=0.54,
        font_size=31,
        color=TEXT,
    )
    strip = RoundedRectangle(width=7.35, height=0.74, corner_radius=0.08, stroke_color=OPERATOR, stroke_width=1.2, fill_color=CARD_BG, fill_opacity=0.82)
    formula.move_to(strip)
    formula_strip = VGroup(strip, formula)
    formula_strip.next_to(body, DOWN, buff=0.46)
    title = SafeText("car design: pressure along boundary", max_width=6.6, max_height=0.44, font_size=29, color=TEXT, weight="BOLD")
    title.next_to(body, UP, buff=0.40)
    demo = VGroup(title, flow, body, pressure_dots, surface_path, formula_strip).move_to(ORIGIN)
    demo.surface_path = surface_path
    demo.formula_strip = formula_strip
    return demo


def make_weather_integral_demo():
    disk = Circle(radius=1.58, stroke_color=SCIENCE, stroke_width=1.5, fill_color="#0A3142", fill_opacity=0.70)
    bands = VGroup()
    for j, y in enumerate(np.linspace(-1.00, 1.00, 7)):
        length = 2.0 * np.sqrt(max(1.58**2 - y**2, 0)) * 0.88
        bands.add(Line([-length / 2, y, 0], [length / 2, y, 0], color=[INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, PURPLE, SCIENCE, INPUT][j], stroke_width=6, stroke_opacity=0.34))
    arrows = VGroup()
    for x, y, dx, dy in [(-0.88, 0.74, 0.46, 0.05), (-0.68, -0.20, 0.42, 0.18), (0.16, 0.42, 0.38, -0.08), (0.44, -0.72, 0.36, 0.10)]:
        arrows.add(Arrow([x, y, 0], [x + dx, y + dy, 0], buff=0, color=TEXT, stroke_width=1.6, max_tip_length_to_length_ratio=0.24))
    region = Circle(radius=0.48, stroke_color=OPERATOR, stroke_width=2.2, fill_color=OPERATOR, fill_opacity=0.16).shift(LEFT * 0.40 + UP * 0.20)
    boundary = Arc(radius=1.08, start_angle=-0.55, angle=1.65, color=WARNING, stroke_width=4.2).shift(RIGHT * 0.02)
    chips = VGroup(
        Chip("average over region", max_width=3.0, height=0.48, stroke_color=OPERATOR, font_size=17),
        Chip("flux across boundary", max_width=3.0, height=0.48, stroke_color=WARNING, font_size=17),
        Chip("energy integral", max_width=3.0, height=0.48, stroke_color=SCIENCE, font_size=17),
    ).arrange(DOWN, buff=0.18)
    weather = VGroup(disk, bands, arrows, region, boundary)
    row = VGroup(weather, chips).arrange(RIGHT, buff=0.80)
    title = SafeText("weather: integrals over domain", max_width=6.4, max_height=0.44, font_size=30, color=TEXT, weight="BOLD")
    demo = VGroup(title, row).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    demo.region = region
    demo.boundary = boundary
    demo.chips = chips
    return demo


def make_fixed_tensor_vs_callable_panel():
    tensor_grid = VGroup()
    for i in range(6):
        for j in range(4):
            tensor_grid.add(
                Rectangle(
                    width=0.32,
                    height=0.32,
                    stroke_color=GRID,
                    stroke_width=0.55,
                    fill_color=INPUT if (i + j) % 2 == 0 else SCIENCE,
                    fill_opacity=0.28,
                ).move_to([i * 0.32, j * 0.32, 0])
            )
    tensor_grid.center()
    left_body = VGroup(
        tensor_grid,
        Arrow(LEFT * 0.86, RIGHT * 0.86, color=MUTED, stroke_width=1.8),
        Chip("post interpolation", max_width=2.70, height=0.46, stroke_color=MUTED, font_size=16),
        Chip("warning: interpolation outside architecture", max_width=4.20, height=0.46, stroke_color=WARNING, font_size=14),
    ).arrange(DOWN, buff=0.18)
    left = PanelCard("fixed tensor output", body=left_body, width=5.35, height=4.35, accent_color=WARNING, title_font_size=24)

    query = VGroup(Dot(ORIGIN, radius=0.075, color=OPERATOR), SafeMathTex(r"y", max_width=0.35, max_height=0.28, font_size=24, color=TEXT)).arrange(RIGHT, buff=0.10)
    model = RoundedRectangle(width=2.20, height=1.02, corner_radius=0.09, stroke_color=OPERATOR, stroke_width=1.5, fill_color="#211B32", fill_opacity=0.88)
    model_label = SafeText("model returns u(y)", max_width=1.92, max_height=0.34, font_size=18, color=OPERATOR, weight="BOLD").move_to(model)
    tools = Chip("derivative / integral tools", max_width=3.28, height=0.48, stroke_color=SCIENCE, font_size=16)
    right_body = VGroup(query, VGroup(model, model_label), tools).arrange(DOWN, buff=0.26)
    right = PanelCard("query point y", body=right_body, width=5.35, height=4.35, accent_color=OPERATOR, title_font_size=24)

    row = VGroup(left, right).arrange(RIGHT, buff=0.60)
    sentence = SafeText(
        "Neural operator output: callable approximation of a function",
        max_width=10.8,
        max_height=0.50,
        font_size=31,
        color=OPERATOR,
        weight="BOLD",
    )
    return VGroup(row, sentence).arrange(DOWN, buff=0.35).move_to(ORIGIN)


class Scene0502OutputMustBeQueryable(TimedScene):
    SCRIPT_ID = "5.2"
    SCRIPT_TITLE = "Output must be queryable"
    SCRIPT_START = 31 * 60 + 20
    SCRIPT_END = 33 * 60 + 5
    SCENE_DURATION = 105.0

    KEYFRAMES = (
        "KF01 0.0s output field, faint grid, output not fixed tensor",
        "KF02 11.0s moving query point with deterministic u(y)",
        "KF03 24.5s derivative stencil around stopped query",
        "KF04 37.0s car boundary pressure and surface integral path",
        "KF05 50.0s weather field region, boundary, energy/flux chips",
        "KF06 65.5s fixed tensor interpolation contrasted with callable output",
    )

    def construct(self):
        background = make_background_network(seed=502, n=70, dot_opacity=0.10, line_opacity=0.08)
        self.add(background)

        output_view = make_initial_output_view()
        self.add(output_view)
        output_view.as_function.set_opacity(0.0)
        assert_in_frame(output_view, margin=0.35, label="output_view")

        # VO exact: Requirement thứ hai: output của model nên có thể query ở bất kỳ điểm nào ta cần.
        # Global 31:20.0-31:31.0 => 31:20.0 -> local 0.0, 31:31.0 -> local 11.0
        self.play_timed(
            "output_field_grid_fades_to_function",
            0.0,
            10.6,
            output_view.field.grid.animate.set_opacity(0.13),
            output_view.not_tensor.animate.set_opacity(0.0),
            output_view.as_function.animate.set_opacity(1.0),
        )
        self.wait_timed("hold_function_output_label", 10.6, 11.0)

        query_view = make_query_motion_view()
        assert_in_frame(query_view, margin=0.35, label="query_view")

        # VO exact: Không phải vì ta thích đẹp. Mà vì physics thường hỏi local derivative, boundary value, surface integral, hoặc average over region.
        # Global 31:31.0-31:44.5 => 31:31.0 -> local 11.0, 31:44.5 -> local 24.5
        self.play_timed(
            "moving_query_point_returns_value",
            11.0,
            24.5,
            FadeOut(output_view, shift=UP * 0.08),
            FadeIn(query_view.field, shift=DOWN * 0.06),
            FadeIn(query_view.path),
            MoveAlongPath(query_view.dot, query_view.path),
            FadeIn(query_view.value_label),
            FadeIn(query_view.y_label),
        )
        query_view.y_label.clear_updaters()

        center = query_view.dot.get_center()
        stencil = make_derivative_stencil(center)
        assert_in_frame(VGroup(query_view, stencil), margin=0.35, label="derivative_view")

        # VO exact: Trong car design, drag liên quan đến tích phân pressure trên bề mặt xe.
        # Global 31:44.5-31:57.0 => 31:44.5 -> local 24.5, 31:57.0 -> local 37.0
        self.play_timed(
            "local_derivative_stencil_attaches_to_query",
            24.5,
            37.0,
            FadeIn(stencil, shift=UP * 0.06),
            Circumscribe(stencil[-1], color=INPUT, buff=0.08),
        )

        surface_demo = make_surface_integral_demo()
        assert_in_frame(surface_demo, margin=0.35, label="surface_demo")

        # VO exact: Trong weather, energy và flux cũng là các đại lượng tích phân trên domain.
        # Global 31:57.0-32:09.0 => 31:57.0 -> local 37.0, 32:09.0 -> local 49.0
        self.play_timed(
            "car_surface_pressure_integral_path",
            37.0,
            49.0,
            FadeOut(VGroup(query_view, stencil), shift=UP * 0.10),
            FadeIn(surface_demo[0], shift=DOWN * 0.08),
            FadeIn(surface_demo[1], shift=RIGHT * 0.08),
            FadeIn(surface_demo[2], shift=UP * 0.05),
            LaggedStart(*[FadeIn(dot, scale=0.90) for dot in surface_demo[3]], lag_ratio=0.04),
            ShowPassingFlash(surface_demo.surface_path.copy().set_stroke(width=7.0), time_width=0.55),
            FadeIn(surface_demo.formula_strip, shift=UP * 0.08),
        )

        # VO exact: Pause: 1.0s.
        # Global 32:09.0-32:10.0 => 32:09.0 -> local 49.0, 32:10.0 -> local 50.0
        self.play_timed(
            "pause_surface_integral_path_pulse",
            49.0,
            49.8,
            Indicate(surface_demo.surface_path, color=OPERATOR, scale_factor=1.01),
        )
        self.wait_timed("hold_after_surface_integral_pulse", 49.8, 50.0)

        weather_demo = make_weather_integral_demo()
        assert_in_frame(weather_demo, margin=0.35, label="weather_demo")

        # VO exact: Nếu output chỉ là một tensor cố định, ta có thể interpolate sau đó. Nhưng khi đó interpolation không còn là phần được học và kiểm soát trong architecture.
        # Global 32:10.0-32:25.5 => 32:10.0 -> local 50.0, 32:25.5 -> local 65.5
        self.play_timed(
            "weather_region_boundary_energy_flux_integrals",
            50.0,
            65.5,
            FadeOut(surface_demo, shift=UP * 0.10),
            FadeIn(weather_demo[0], shift=DOWN * 0.08),
            FadeIn(weather_demo[1], shift=UP * 0.08),
            Circumscribe(weather_demo.region, color=OPERATOR, buff=0.05),
            Circumscribe(weather_demo.boundary, color=WARNING, buff=0.06),
        )

        split_view = make_fixed_tensor_vs_callable_panel()
        assert_in_frame(split_view, margin=0.35, label="split_view")

        # VO exact: Neural operator muốn output thật sự là một function approximation: ta đưa query point `y` vào, và model trả ra giá trị `u(y)`.
        # Global 32:25.5-33:05.0 => 32:25.5 -> local 65.5, 33:05.0 -> local 105.0
        self.play_timed(
            "fixed_tensor_interpolation_vs_callable_function_output",
            65.5,
            85.0,
            FadeOut(weather_demo, shift=UP * 0.10),
            FadeIn(split_view[0], shift=UP * 0.08),
        )

        # Global 32:45.0-33:05.0 => local 85.0-105.0, 33:05.0 -> local 105.0
        self.play_timed(
            "final_callable_function_sentence",
            85.0,
            105.0,
            FadeIn(split_view[1], shift=UP * 0.08),
            Circumscribe(split_view[1], color=OPERATOR, buff=0.12),
        )

        self.pad_to(self.SCENE_DURATION)
