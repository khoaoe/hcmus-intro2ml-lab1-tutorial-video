"""
Scene 3.2 - Darcy flow as the clean toy example
Script: ../docs/full_voice_manim_script.md
Global time: 17:20.0-19:35.0
Local duration: 135.0s

Darcy flow as a clean PDE example: permeability function a(x), solution
field u(x), solution operator G, finite-difference discretization, and
accuracy/compute trade-off.
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

ASCII_FINAL_SUBTITLE = "better solution ~= more computation"


def make_field_cells(width, height, rows, cols, seed, palette, opacity_base=0.38):
    rng = np.random.default_rng(seed)
    cells = VGroup()
    dx = width / cols
    dy = height / rows
    for row in range(rows):
        for col in range(cols):
            x = col / max(cols - 1, 1)
            y = row / max(rows - 1, 1)
            value = (
                0.9 * np.sin(2.2 * TAU * x + 0.55 * np.cos(4 * y))
                + 0.7 * np.cos(1.6 * TAU * y + 0.4 * np.sin(3 * x))
                + rng.normal(0.0, 0.18)
            )
            index = int(abs(value) * 2.4 + row + col) % len(palette)
            cell = Rectangle(
                width=dx,
                height=dy,
                stroke_width=0.25,
                stroke_color=CARD_BG,
                fill_color=palette[index],
                fill_opacity=opacity_base + 0.22 * (0.5 + 0.5 * np.sin(value)),
            )
            cell.move_to(
                [
                    -width / 2 + dx / 2 + col * dx,
                    height / 2 - dy / 2 - row * dy,
                    0,
                ]
            )
            cells.add(cell)
    return cells


class RandomField(VGroup):
    """Deterministic permeability field a(x)."""

    def __init__(self, width=4.05, height=2.6, rows=10, cols=16, seed=32, **kwargs):
        super().__init__(**kwargs)
        self.frame = RoundedRectangle(
            width=width + 0.18,
            height=height + 0.18,
            corner_radius=0.09,
            stroke_color=INPUT,
            stroke_width=1.4,
            fill_color="#09243A",
            fill_opacity=0.42,
        )
        self.cells = make_field_cells(
            width,
            height,
            rows,
            cols,
            seed,
            [INPUT, SCIENCE, OUTPUT, OPERATOR, PURPLE, NVIDIA_GREEN],
            opacity_base=0.42,
        )
        self.mesh = make_mesh_overlay(width=width, height=height, nx=max(4, cols // 2), ny=max(3, rows // 2), color=TEXT)
        self.mesh.set_stroke(opacity=0.18, width=0.45)
        self.symbol = SafeMathTex(r"a(x)", max_width=0.9, max_height=0.42, font_size=32, color=INPUT)
        self.symbol.move_to(self.frame.get_corner(UR) + LEFT * 0.42 + DOWN * 0.28)
        self.add(self.frame, self.cells, self.mesh, self.symbol)


class SolutionField(VGroup):
    """Smooth pressure/potential field u(x)."""

    def __init__(self, width=4.05, height=2.6, rows=10, cols=16, seed=51, **kwargs):
        super().__init__(**kwargs)
        self.frame = RoundedRectangle(
            width=width + 0.18,
            height=height + 0.18,
            corner_radius=0.09,
            stroke_color=OUTPUT,
            stroke_width=1.4,
            fill_color="#102A1E",
            fill_opacity=0.42,
        )
        self.cells = make_field_cells(
            width,
            height,
            rows,
            cols,
            seed,
            [OUTPUT, SCIENCE, INPUT, NVIDIA_GREEN, OPERATOR],
            opacity_base=0.36,
        )
        self.contours = VGroup()
        for index, y in enumerate(np.linspace(-height * 0.36, height * 0.36, 6)):
            points = []
            for x in np.linspace(-width * 0.43, width * 0.43, 36):
                points.append([x, y + 0.11 * np.sin(2.2 * x + index * 0.7), 0])
            self.contours.add(smooth_path(points, color=TEXT, stroke_width=1.15, stroke_opacity=0.58))
        self.symbol = SafeMathTex(r"u(x)", max_width=0.9, max_height=0.42, font_size=32, color=OUTPUT)
        self.symbol.move_to(self.frame.get_corner(UR) + LEFT * 0.42 + DOWN * 0.28)
        self.add(self.frame, self.cells, self.contours, self.symbol)


class ComputeMeter(VGroup):
    """Small vertical meter for time, memory, energy cost."""

    def __init__(self, level=0.25, width=2.55, height=2.35, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            stroke_color=WARNING,
            stroke_width=1.25,
            fill_color=CARD_BG,
            fill_opacity=0.68,
        )
        self.title = SafeText("compute", max_width=1.6, max_height=0.24, font_size=17, color=WARNING, weight="BOLD")
        self.title.move_to(self.box.get_top() + DOWN * 0.32)
        labels = [("time", INPUT), ("memory", OPERATOR), ("energy", WARNING)]
        self.bars = VGroup()
        for index, (label, color) in enumerate(labels):
            slot = RoundedRectangle(
                width=0.34,
                height=1.16,
                corner_radius=0.05,
                stroke_color=GRID,
                stroke_width=0.8,
                fill_color="#0F172A",
                fill_opacity=0.8,
            )
            fill_height = 0.14 + 0.88 * min(1.0, level * (0.78 + 0.16 * index))
            fill = Rectangle(
                width=0.25,
                height=fill_height,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.78,
            )
            fill.move_to(slot.get_bottom() + UP * (fill_height / 2 + 0.05))
            text = SafeText(label, max_width=0.72, max_height=0.22, font_size=13, min_font_size=11, color=TEXT)
            text.next_to(slot, DOWN, buff=0.08)
            group = VGroup(slot, fill, text)
            self.bars.add(group)
        self.bars.arrange(RIGHT, buff=0.18)
        self.bars.move_to(self.box.get_center() + DOWN * 0.18)
        self.add(self.box, self.title, self.bars)


def make_field_panel(title, subtitle, field, color):
    caption = VGroup(
        SafeText(title, max_width=2.4, max_height=0.32, font_size=21, color=color, weight="BOLD"),
        SafeText(subtitle, max_width=3.7, max_height=0.32, font_size=16, min_font_size=13, color=TEXT),
    ).arrange(DOWN, buff=0.08)
    body = VGroup(field, caption).arrange(DOWN, buff=0.22)
    return PanelCard(title, body=body, width=4.75, height=4.15, accent_color=color, title_font_size=24)


class Scene0302DarcyFlowCleanToyExample(TimedScene):
    SCRIPT_ID = "3.2"
    SCRIPT_TITLE = "Darcy flow as the clean toy example"
    SCRIPT_START = 17 * 60 + 20
    SCRIPT_END = 19 * 60 + 35
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def make_porous_medium(self):
        frame = RoundedRectangle(
            width=9.2,
            height=4.7,
            corner_radius=0.14,
            stroke_color=SCIENCE,
            stroke_width=1.45,
            fill_color="#0E2430",
            fill_opacity=0.68,
        )
        rng = np.random.default_rng(12)
        pores = VGroup()
        for _ in range(58):
            pore = Circle(
                radius=rng.uniform(0.035, 0.09),
                stroke_color=GRID,
                stroke_width=0.55,
                fill_color=GRID,
                fill_opacity=rng.uniform(0.22, 0.48),
            )
            pore.move_to([rng.uniform(-4.2, 4.2), rng.uniform(-1.85, 1.65), 0])
            pores.add(pore)
        flow_lines = VGroup()
        for index, y in enumerate(np.linspace(-1.55, 1.35, 7)):
            points = []
            for x in np.linspace(-4.05, 4.05, 42):
                points.append([x, y + 0.12 * np.sin(1.8 * x + index * 0.65), 0])
            flow_lines.add(smooth_path(points, color=[INPUT, SCIENCE, OUTPUT][index % 3], stroke_width=2.0, stroke_opacity=0.62))
        label = Chip("flow through porous media", max_width=3.25, height=0.46, stroke_color=SCIENCE, font_size=18)
        label.next_to(frame, DOWN, buff=0.22)
        return VGroup(frame, pores, flow_lines, label)

    def make_random_field(self):
        field = RandomField()
        return make_field_panel("input function", "a(x): permeability / diffusion coefficient", field, INPUT)

    def make_solution_field(self):
        field = SolutionField()
        return make_field_panel("output function", "u(x): pressure / potential", field, OUTPUT)

    def make_pde_pipeline(self, left_panel, right_panel):
        pde_formula = SafeMathTex(
            r"-\nabla\cdot(a(x)\nabla u(x))=f(x)",
            max_width=3.1,
            max_height=0.6,
            font_size=30,
            min_font_size=22,
            color=OPERATOR,
        )
        pde_box = RoundedRectangle(
            width=3.55,
            height=2.08,
            corner_radius=0.11,
            stroke_color=OPERATOR,
            stroke_width=1.5,
            fill_color="#1A2336",
            fill_opacity=0.86,
        )
        pde_formula.move_to(pde_box.get_center() + UP * 0.12)
        pde_title = SafeText("PDE / solver", max_width=1.7, max_height=0.3, font_size=19, color=TEXT, weight="BOLD")
        pde_title.move_to(pde_box.get_top() + DOWN * 0.28)
        chip_top = VGroup(
            Chip("equation", max_width=1.15, height=0.42, stroke_color=OPERATOR, font_size=13),
            Chip("boundary conditions", max_width=2.05, height=0.42, stroke_color=WARNING, font_size=13),
        ).arrange(RIGHT, buff=0.10)
        chip_bottom = Chip("solver finds u", max_width=1.72, height=0.42, stroke_color=OUTPUT, font_size=13)
        chips = VGroup(chip_top, chip_bottom).arrange(DOWN, buff=0.08)
        chips.move_to(pde_box.get_bottom() + UP * 0.48)
        pde = VGroup(pde_box, pde_title, pde_formula, chips)
        pde.move_to(ORIGIN + DOWN * 0.08)
        arrows = VGroup(
            Arrow(left_panel.get_right() + RIGHT * 0.08, pde_box.get_left() + LEFT * 0.08, color=OPERATOR, stroke_width=2.5, stroke_opacity=0.52, buff=0.0),
            Arrow(pde_box.get_right() + RIGHT * 0.08, right_panel.get_left() + LEFT * 0.08, color=OPERATOR, stroke_width=2.5, stroke_opacity=0.52, buff=0.0),
        )
        return VGroup(arrows, pde)

    def make_operator_view(self):
        left_blob = Ellipse(width=3.5, height=2.4, stroke_color=INPUT, stroke_width=1.5, fill_color=CARD_BG, fill_opacity=0.46)
        right_blob = Ellipse(width=3.5, height=2.4, stroke_color=OUTPUT, stroke_width=1.5, fill_color=CARD_BG, fill_opacity=0.46)
        left_blob.shift(LEFT * 4.2)
        right_blob.shift(RIGHT * 4.2)
        left_label = SafeMathTex(r"\mathcal{A}", max_width=0.8, max_height=0.5, font_size=38, color=INPUT).move_to(left_blob.get_top() + DOWN * 0.38)
        right_label = SafeMathTex(r"\mathcal{U}", max_width=0.8, max_height=0.5, font_size=38, color=OUTPUT).move_to(right_blob.get_top() + DOWN * 0.38)
        a_symbol = SafeMathTex(r"a", max_width=0.6, max_height=0.45, font_size=38, color=INPUT).move_to(left_blob)
        u_symbol = SafeMathTex(r"u", max_width=0.6, max_height=0.45, font_size=38, color=OUTPUT).move_to(right_blob)
        operator = Circle(radius=0.7, stroke_color=OPERATOR, stroke_width=2.2, fill_color="#2C2414", fill_opacity=0.55)
        operator_symbol = SafeMathTex(r"\mathcal{G}", max_width=0.85, max_height=0.62, font_size=48, color=OPERATOR).move_to(operator)
        arrow_1 = Arrow(left_blob.get_right() + RIGHT * 0.18, operator.get_left() + LEFT * 0.1, color=OPERATOR, stroke_width=3.0, stroke_opacity=0.65, buff=0)
        arrow_2 = Arrow(operator.get_right() + RIGHT * 0.1, right_blob.get_left() + LEFT * 0.18, color=OPERATOR, stroke_width=3.0, stroke_opacity=0.65, buff=0)
        title = SafeText("Solution operator", max_width=3.3, max_height=0.46, font_size=30, color=TEXT, weight="BOLD")
        title.to_edge(UP, buff=0.58)
        formula = SafeMathTex(r"\mathcal{G}: a \mapsto u", max_width=3.1, max_height=0.55, font_size=36, color=OPERATOR)
        formula.next_to(operator, DOWN, buff=0.42)
        return VGroup(title, left_blob, right_blob, left_label, right_label, a_symbol, u_symbol, arrow_1, arrow_2, operator, operator_symbol, formula)

    def make_finite_difference_demo(self):
        panel = PanelCard("finite difference", width=12.5, height=5.6, accent_color=PURPLE, title_font_size=27)
        curve_axes = VGroup(
            Line(LEFT * 2.45 + DOWN * 1.05, RIGHT * 2.45 + DOWN * 1.05, color=GRID, stroke_width=1.2),
            Line(LEFT * 2.45 + DOWN * 1.05, LEFT * 2.45 + UP * 1.15, color=GRID, stroke_width=1.2),
        )
        curve_points = []
        for t in np.linspace(0, 1, 50):
            x = -2.2 + 4.4 * t
            y = -0.25 + 0.75 * np.sin(PI * t) + 0.18 * np.sin(3 * PI * t)
            curve_points.append([x, y, 0])
        curve = smooth_path(curve_points, color=OUTPUT, stroke_width=3.0, stroke_opacity=0.9)
        xi = Dot([-0.2, 0.72, 0], radius=0.055, color=OPERATOR)
        xip1 = Dot([0.72, 0.82, 0], radius=0.055, color=OPERATOR)
        brace = BraceBetweenPoints([-0.2, -1.05, 0], [0.72, -1.05, 0], color=OPERATOR)
        brace_label = SafeMathTex(r"\Delta x", max_width=0.65, max_height=0.32, font_size=25, color=OPERATOR)
        brace_label.next_to(brace, DOWN, buff=0.06)
        point_labels = VGroup(
            SafeMathTex(r"x_i", max_width=0.4, max_height=0.26, font_size=21, color=TEXT).next_to(xi, UP, buff=0.08),
            SafeMathTex(r"x_{i+1}", max_width=0.65, max_height=0.26, font_size=21, color=TEXT).next_to(xip1, UP, buff=0.08),
        )
        curve_group = VGroup(curve_axes, curve, xi, xip1, brace, brace_label, point_labels).shift(LEFT * 3.15 + DOWN * 0.16)
        formula = SafeMathTex(r"\frac{u_{i+1}-u_i}{\Delta x}", max_width=2.25, max_height=0.88, font_size=40, color=OPERATOR)
        formula.move_to(RIGHT * 0.3 + UP * 0.78)
        stencil_grid = make_mesh_overlay(width=2.05, height=2.05, nx=4, ny=4, color=TEXT)
        stencil_dots = VGroup(
            Dot(ORIGIN, radius=0.06, color=OPERATOR),
            Dot(LEFT * 0.5, radius=0.045, color=INPUT),
            Dot(RIGHT * 0.5, radius=0.045, color=INPUT),
            Dot(UP * 0.5, radius=0.045, color=INPUT),
            Dot(DOWN * 0.5, radius=0.045, color=INPUT),
        )
        stencil = VGroup(stencil_grid, stencil_dots).move_to(RIGHT * 3.75 + UP * 0.15)
        stencil_label = SafeText("2D stencil", max_width=1.45, max_height=0.28, font_size=18, color=MUTED)
        stencil_label.next_to(stencil, DOWN, buff=0.14)
        message = SafeText(
            "continuum PDE -> finite-dimensional system",
            max_width=6.9,
            max_height=0.44,
            font_size=27,
            color=TEXT,
            weight="BOLD",
        )
        message.move_to(panel.box.get_bottom() + UP * 0.55)
        content = VGroup(curve_group, formula, stencil, stencil_label, message)
        return VGroup(panel, content)

    def make_refinement_panels(self):
        panels = VGroup()
        specs = [
            ("coarse", 5, 4, 0.24),
            ("medium", 9, 6, 0.48),
            ("fine", 15, 10, 0.72),
        ]
        for index, (label, nx, ny, smoothness) in enumerate(specs):
            field = SolutionField(width=2.45, height=1.45, rows=5 + index * 2, cols=8 + index * 4, seed=71)
            mesh = make_mesh_overlay(width=2.45, height=1.45, nx=nx, ny=ny, color=TEXT)
            mesh.set_stroke(opacity=0.42, width=0.55)
            blur_note = SafeText(label, max_width=1.2, max_height=0.28, font_size=18, color=TEXT, weight="BOLD")
            quality = Line(LEFT * 0.8, RIGHT * (0.8 * smoothness), color=OUTPUT, stroke_width=4.0, stroke_opacity=0.76)
            body = VGroup(field, mesh, quality).arrange(DOWN, buff=0.12)
            panel = PanelCard(label, body=body, width=3.35, height=3.05, accent_color=[WARNING, OPERATOR, OUTPUT][index], title_font_size=22)
            panels.add(panel)
        panels.arrange(RIGHT, buff=0.38)
        message = SafeText("finer mesh -> better approximation", max_width=5.4, max_height=0.4, font_size=27, color=OUTPUT, weight="BOLD")
        message.next_to(panels, DOWN, buff=0.28)
        return VGroup(panels, message)

    def make_compute_meter(self, level=0.25):
        return ComputeMeter(level=level)

    def construct(self):
        background = make_background_network(seed=42, n=76, dot_opacity=0.15, line_opacity=0.13)
        title = SafeText("Darcy flow: clean toy example", max_width=8.8, max_height=0.62, font_size=40, color=TEXT, weight="BOLD")
        title.to_edge(UP, buff=0.45)
        porous = self.make_porous_medium().move_to(ORIGIN + DOWN * 0.1)
        assert_in_frame(VGroup(title, porous), margin=0.35, label="porous_intro")

        self.add(background)
        self.play_timed(
            "porous_medium_intro",
            0.0,
            11.0,
            FadeIn(title, shift=DOWN * 0.15),
            FadeIn(porous[0], shift=UP * 0.12),
            LaggedStart(FadeIn(porous[1]), Create(porous[2]), FadeIn(porous[3], shift=UP * 0.1), lag_ratio=0.24),
        )

        input_panel = self.make_random_field().move_to(LEFT * 4.65 + DOWN * 0.05)
        assert_in_frame(input_panel, margin=0.35, label="input_panel")
        self.play_timed(
            "permeability_field",
            11.0,
            24.0,
            FadeOut(porous, shift=LEFT * 0.28),
            title.animate.scale(0.78).to_corner(UP + LEFT, buff=0.42),
            FadeIn(input_panel, shift=RIGHT * 0.22),
        )

        output_panel = self.make_solution_field().move_to(RIGHT * 4.65 + DOWN * 0.05)
        assert_in_frame(VGroup(input_panel, output_panel), margin=0.35, label="input_output")
        self.play_timed(
            "solution_field",
            24.0,
            36.5,
            FadeIn(output_panel, shift=LEFT * 0.22),
        )
        self.wait_timed("pause_hold_fields", 36.5, 37.5)

        pipeline = self.make_pde_pipeline(input_panel, output_panel)
        assert_in_frame(VGroup(input_panel, pipeline, output_panel), margin=0.35, label="pde_pipeline")
        self.play_timed(
            "pde_relation",
            37.5,
            50.5,
            FadeIn(pipeline[0], shift=UP * 0.05),
            FadeIn(pipeline[1][0:3], scale=0.98),
            FadeIn(pipeline[1][3], shift=UP * 0.08),
        )

        operator_view = self.make_operator_view()
        assert_in_frame(operator_view, margin=0.35, label="operator_view")
        self.play_timed(
            "zoom_to_operator_map",
            50.5,
            63.0,
            FadeOut(VGroup(title, input_panel, pipeline, output_panel), shift=DOWN * 0.25),
            FadeIn(operator_view[1:9], shift=UP * 0.08),
            FadeIn(operator_view[9:11], scale=0.94),
        )
        self.play_timed(
            "solution_operator_highlight",
            63.0,
            74.5,
            FadeIn(operator_view[0], shift=DOWN * 0.1),
            FadeIn(operator_view[11], shift=UP * 0.1),
            operator_view[9].animate.set_stroke(width=3.4, opacity=1.0),
        )

        fd_demo = self.make_finite_difference_demo()
        fd_demo.move_to(ORIGIN + DOWN * 0.04)
        assert_in_frame(fd_demo, margin=0.35, label="finite_difference_demo")
        self.play_timed(
            "finite_difference_demo",
            74.5,
            93.0,
            FadeOut(operator_view, shift=LEFT * 0.28),
            FadeIn(fd_demo[0], shift=DOWN * 0.1),
            LaggedStart(*[FadeIn(mob, shift=UP * 0.08) for mob in fd_demo[1]], lag_ratio=0.12),
        )

        refinement = self.make_refinement_panels().move_to(LEFT * 1.35 + DOWN * 0.05)
        meter_low = self.make_compute_meter(level=0.32).move_to(RIGHT * 5.9 + DOWN * 0.05)
        assert_in_frame(VGroup(refinement, meter_low), margin=0.35, label="refinement_low_compute")
        self.play_timed(
            "mesh_refinement",
            93.0,
            109.5,
            FadeOut(fd_demo, shift=DOWN * 0.18),
            FadeIn(refinement, shift=UP * 0.12),
            FadeIn(meter_low, shift=LEFT * 0.1),
        )

        meter_high = self.make_compute_meter(level=0.92).move_to(meter_low)
        final_message = SafeText("Accuracy is not free.", max_width=4.1, max_height=0.5, font_size=34, color=WARNING, weight="BOLD")
        subtitle = SafeText("better solution ≈ more computation", max_width=4.6, max_height=0.34, font_size=21, color=TEXT)
        final_text = VGroup(final_message, subtitle).arrange(DOWN, buff=0.1)
        final_text.move_to(DOWN * 3.45)
        assert_in_frame(VGroup(refinement, meter_high, final_text), margin=0.32, label="final_tradeoff")
        self.play_timed(
            "accuracy_compute_tradeoff",
            109.5,
            135.0,
            Transform(meter_low, meter_high),
            FadeIn(final_text, shift=UP * 0.12),
            refinement[0][2].animate.set_stroke(width=2.0),
            refinement[1].animate.set_color(WARNING),
        )
        self.pad_to(self.SCENE_DURATION)
