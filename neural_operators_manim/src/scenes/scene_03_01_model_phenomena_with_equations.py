"""
Scene 3.1 - Model phenomena with equations
Script: ../docs/full_voice_manim_script.md
Global time: 15:45.0-17:20.0
Local duration: 95.0s

Traditional scientific computing starts from first principles, turns continuum
models into discretized meshes, then uses numerical solvers as part of the
broader scientific-computing toolbox.
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
    BG,
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
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_icon_dot(label, color):
    dot = Circle(radius=0.12, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.46)
    text = SafeText(label, max_width=1.15, max_height=0.24, font_size=15, color=TEXT)
    return VGroup(dot, text).arrange(RIGHT, buff=0.12)


def make_board_card(label, color, width=3.5):
    box = RoundedRectangle(
        width=width,
        height=0.68,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.15,
        fill_color="#142033",
        fill_opacity=0.74,
    )
    text = SafeText(label, max_width=width - 0.24, max_height=0.34, font_size=18, min_font_size=14, color=TEXT)
    text.move_to(box)
    return VGroup(box, text)


class EquationBoard(VGroup):
    """Chalkboard for first-principles equations."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = RoundedRectangle(
            width=12.9,
            height=5.9,
            corner_radius=0.12,
            stroke_color=GRID,
            stroke_width=1.6,
            fill_color="#101827",
            fill_opacity=0.86,
        )
        self.glow = RoundedRectangle(
            width=13.05,
            height=6.05,
            corner_radius=0.14,
            stroke_color=INPUT,
            stroke_width=7.0,
            stroke_opacity=0.08,
            fill_opacity=0,
        )

        self.principles = SafeText(
            "First principles",
            max_width=4.8,
            max_height=0.52,
            font_size=34,
            color=TEXT,
            weight="BOLD",
        )
        self.principles.move_to(self.frame.get_top() + DOWN * 0.74)
        self.principle_chips = VGroup(
            make_icon_dot("physics", PHYSICS),
            make_icon_dot("geometry", SCIENCE),
            make_icon_dot("constraints", OPERATOR),
        ).arrange(RIGHT, buff=0.42)
        self.principle_chips.next_to(self.principles, DOWN, buff=0.24)

        card_labels = [
            ("Differential equations", INPUT),
            ("Algebraic equations", PURPLE),
            ("Conservation laws", OUTPUT),
            ("Boundary conditions", WARNING),
            ("Initial conditions", OPERATOR),
        ]
        cards = VGroup(*[make_board_card(label, color) for label, color in card_labels])
        top_row = VGroup(cards[0], cards[1], cards[2]).arrange(RIGHT, buff=0.38)
        bottom_row = VGroup(cards[3], cards[4]).arrange(RIGHT, buff=0.44)
        self.equation_cards = VGroup(top_row, bottom_row).arrange(DOWN, buff=0.34)
        self.equation_cards.move_to(self.frame.get_center() + DOWN * 0.72)

        self.center_formula = SafeMathTex(
            r"\mathcal{E}(u; a, f)=0",
            max_width=3.35,
            max_height=0.78,
            font_size=43,
            color=OPERATOR,
        )
        self.center_formula.move_to(self.frame.get_center() + DOWN * 0.24)
        domain_labels = [
            ("Navier-Stokes", INPUT, [-3.05, 0.98, 0]),
            ("Maxwell", SCIENCE, [-1.0, 1.32, 0]),
            ("Schrodinger", PURPLE, [1.2, 1.25, 0]),
            ("Darcy", OUTPUT, [3.05, 0.86, 0]),
            ("Helmholtz", OPERATOR, [-2.55, -1.35, 0]),
            ("Heat", WARNING, [0.0, -1.62, 0]),
            ("Wave", INPUT, [2.45, -1.35, 0]),
        ]
        self.domain_chips = VGroup()
        for label, color, offset in domain_labels:
            chip = Chip(label, max_width=1.82, height=0.38, stroke_color=color, font_size=15, min_font_size=12)
            chip.move_to(self.center_formula.get_center() + np.array(offset))
            self.domain_chips.add(chip)
        self.domain_group = VGroup(self.center_formula, self.domain_chips)

        self.add(self.glow, self.frame, self.principles, self.principle_chips, self.equation_cards, self.domain_group)


class Mesh(VGroup):
    """Continuum field plus coarse and fine discretization overlays."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.panel = PanelCard(
            "continuum",
            width=6.1,
            height=4.55,
            accent_color=INPUT,
            title_font_size=28,
        )
        self.panel.move_to(LEFT * 3.15 + DOWN * 0.1)
        field = self._make_field_blob()
        field.move_to(self.panel.box.get_center() + DOWN * 0.12)
        self.field = field
        self.coarse_grid = make_mesh_overlay(width=4.55, height=2.75, nx=6, ny=4, color=TEXT)
        self.coarse_grid.move_to(self.field)
        self.fine_grid = make_mesh_overlay(width=4.55, height=2.75, nx=14, ny=9, color=TEXT)
        self.fine_grid.move_to(self.field)
        self.fine_grid.set_stroke(opacity=0.46, width=0.55)
        self.label = Chip(
            "discretize domain -> mesh / grid",
            max_width=4.15,
            height=0.44,
            stroke_color=OPERATOR,
            font_size=17,
            min_font_size=14,
        )
        self.label.next_to(self.panel, DOWN, buff=0.25)
        self.arrow = Arrow(
            self.field.get_right() + RIGHT * 0.22,
            self.field.get_right() + RIGHT * 1.62,
            color=OPERATOR,
            stroke_width=3.0,
            stroke_opacity=0.62,
            buff=0.0,
        )
        self.mesh_caption = SafeText("mesh / grid", max_width=1.4, max_height=0.28, font_size=18, color=MUTED)
        self.mesh_caption.next_to(self.arrow, UP, buff=0.12)
        self.add(self.panel, self.field, self.coarse_grid, self.fine_grid, self.label, self.arrow, self.mesh_caption)

    def _make_field_blob(self):
        boundary = RoundedRectangle(
            width=4.65,
            height=2.85,
            corner_radius=0.2,
            stroke_color=INPUT,
            stroke_width=1.6,
            fill_color="#09243A",
            fill_opacity=0.56,
        )
        waves = VGroup()
        for index, y in enumerate(np.linspace(-0.84, 0.84, 7)):
            points = []
            for x in np.linspace(-2.05, 2.05, 36):
                points.append([x, y + 0.14 * np.sin(2.2 * x + index * 0.7), 0])
            color = [INPUT, SCIENCE, OUTPUT, OPERATOR, PURPLE, NVIDIA_GREEN, WARNING][index]
            waves.add(smooth_path(points, color=color, stroke_width=2.0, stroke_opacity=0.72))
        dots = VGroup(
            *[
                Dot([x, 0.62 * np.sin(1.3 * x), 0], radius=0.035, color=TEXT, fill_opacity=0.65)
                for x in np.linspace(-1.8, 1.8, 9)
            ]
        )
        return VGroup(boundary, waves, dots)


class SolverBox(VGroup):
    """Numerical solver machinery with small moving parts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=3.3,
            height=1.72,
            corner_radius=0.12,
            stroke_color=OPERATOR,
            stroke_width=1.5,
            fill_color="#1A2336",
            fill_opacity=0.88,
        )
        self.label = SafeText("Numerical Solver", max_width=2.75, max_height=0.38, font_size=24, color=TEXT, weight="BOLD")
        self.label.move_to(self.box.get_top() + DOWN * 0.36)
        self.gears = VGroup()
        for x, radius, color in [(-0.52, 0.2, INPUT), (0.0, 0.25, OPERATOR), (0.55, 0.18, OUTPUT)]:
            gear = RegularPolygon(n=8, radius=radius, color=color, stroke_width=1.4, fill_color=color, fill_opacity=0.16)
            gear.shift(RIGHT * x + DOWN * 0.2)
            self.gears.add(gear)
        self.scanline = Line(
            self.box.get_left() + RIGHT * 0.18 + DOWN * 0.38,
            self.box.get_right() + LEFT * 0.18 + DOWN * 0.38,
            color=SCIENCE,
            stroke_width=2.2,
            stroke_opacity=0.64,
        )
        self.dots = VGroup(
            *[
                Dot([-1.0 + index * 0.4, -0.62, 0], radius=0.035, color=SCIENCE, fill_opacity=0.8)
                for index in range(6)
            ]
        )
        self.add(self.box, self.label, self.gears, self.scanline, self.dots)


class Toolbox(VGroup):
    """Final toolbox: classical PDE solvers and ML/neural operators together."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame = RoundedRectangle(
            width=12.2,
            height=5.15,
            corner_radius=0.16,
            stroke_color=GRID,
            stroke_width=1.6,
            fill_color="#111827",
            fill_opacity=0.88,
        )
        self.handle = RoundedRectangle(
            width=3.1,
            height=0.55,
            corner_radius=0.1,
            stroke_color=GRID,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.92,
        )
        self.handle.next_to(self.frame, UP, buff=-0.05)

        pde_icon = self._make_tool_icon("PDE Solvers", OPERATOR, r"\Delta u=f")
        ml_icon = self._make_tool_icon("Machine Learning / Neural Operators", INPUT, r"\mathcal{G}:a\mapsto u")
        self.tools = VGroup(pde_icon, ml_icon).arrange(RIGHT, buff=0.75)
        self.tools.move_to(self.frame.get_center() + UP * 0.34)
        self.message = SafeText(
            "Not replacement. Complementary tool.",
            max_width=6.6,
            max_height=0.46,
            font_size=30,
            min_font_size=22,
            color=OUTPUT,
            weight="BOLD",
        )
        self.message.move_to(self.frame.get_bottom() + UP * 0.82)
        self.glow = RoundedRectangle(
            width=12.35,
            height=5.3,
            corner_radius=0.18,
            stroke_color=OUTPUT,
            stroke_width=8.0,
            stroke_opacity=0.08,
            fill_opacity=0,
        )
        self.add(self.glow, self.frame, self.handle, self.tools, self.message)

    def _make_tool_icon(self, title, color, formula_tex):
        formula = SafeMathTex(formula_tex, max_width=2.65, max_height=0.54, font_size=31, color=color)
        dots = VGroup(
            Dot(LEFT * 0.46 + DOWN * 0.2, radius=0.06, color=color),
            Dot(DOWN * 0.02, radius=0.06, color=color),
            Dot(RIGHT * 0.46 + DOWN * 0.2, radius=0.06, color=color),
        )
        links = VGroup(
            Line(dots[0].get_center(), dots[1].get_center(), color=color, stroke_width=1.5, stroke_opacity=0.5),
            Line(dots[1].get_center(), dots[2].get_center(), color=color, stroke_width=1.5, stroke_opacity=0.5),
        )
        body = VGroup(formula, VGroup(links, dots)).arrange(DOWN, buff=0.2)
        return PanelCard(title, body=body, width=5.0, height=2.45, accent_color=color, title_font_size=22)


def make_solution_field(width=3.35, height=1.72):
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=OUTPUT,
        stroke_width=1.25,
        fill_color="#102A1E",
        fill_opacity=0.72,
    )
    cells = VGroup()
    rows, cols = 6, 11
    dx, dy = width / cols, height / rows
    palette = [INPUT, SCIENCE, OUTPUT, OPERATOR, WARNING, PURPLE]
    for row in range(rows):
        for col in range(cols):
            value = np.sin(row * 0.7) + np.cos(col * 0.55)
            color = palette[int(abs(value) * 2 + row + col) % len(palette)]
            cell = Rectangle(
                width=dx,
                height=dy,
                stroke_width=0.25,
                stroke_color=CARD_BG,
                fill_color=color,
                fill_opacity=0.36 + 0.2 * ((row + col) % 2),
            )
            cell.move_to(
                [
                    -width / 2 + dx / 2 + col * dx,
                    height / 2 - dy / 2 - row * dy,
                    0,
                ]
            )
            cells.add(cell)
    return VGroup(frame, cells)


class Scene0301ModelPhenomenaWithEquations(TimedScene):
    SCRIPT_ID = "3.1"
    SCRIPT_TITLE = "Model phenomena with equations"
    SCRIPT_START = 15 * 60 + 45
    SCRIPT_END = 17 * 60 + 20
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def make_equation_board(self):
        return EquationBoard()

    def make_continuum_mesh(self):
        return Mesh()

    def make_solver_pipeline(self):
        input_card = PanelCard(
            "Equation + Mesh",
            body=SafeMathTex(r"\mathcal{E}(u; a, f)=0", max_width=2.8, max_height=0.48, font_size=28, color=OPERATOR),
            width=3.35,
            height=1.72,
            accent_color=INPUT,
            title_font_size=22,
        )
        solver = SolverBox()
        output_card = PanelCard(
            "Discrete Solution",
            body=make_solution_field(width=2.65, height=1.25),
            width=3.35,
            height=1.72,
            accent_color=OUTPUT,
            title_font_size=22,
        )
        boxes = VGroup(input_card, solver, output_card).arrange(RIGHT, buff=0.8)
        arrows = VGroup()
        for left, right in ((input_card, solver), (solver, output_card)):
            arrows.add(
                Arrow(
                    left.get_right() + RIGHT * 0.08,
                    right.get_left() + LEFT * 0.08,
                    color=OPERATOR,
                    stroke_width=2.5,
                    stroke_opacity=0.5,
                    buff=0.0,
                    max_tip_length_to_length_ratio=0.16,
                )
            )
        method_chips = VGroup(
            Chip("finite difference", max_width=2.15, height=0.42, stroke_color=INPUT, font_size=16),
            Chip("finite volume", max_width=1.85, height=0.42, stroke_color=SCIENCE, font_size=16),
            Chip("finite element", max_width=1.9, height=0.42, stroke_color=OUTPUT, font_size=16),
            Chip("spectral", max_width=1.35, height=0.42, stroke_color=PURPLE, font_size=16),
        ).arrange(RIGHT, buff=0.18)
        method_chips.next_to(boxes, DOWN, buff=0.42)
        pipeline = VGroup(arrows, boxes, method_chips)
        pipeline.move_to(ORIGIN + DOWN * 0.05)
        return pipeline

    def make_toolbox(self):
        return Toolbox()

    def construct(self):
        background = make_background_network(seed=31, n=78, dot_opacity=0.16, line_opacity=0.13)
        title = SafeText(
            "Traditional Scientific Computing",
            max_width=9.6,
            max_height=0.64,
            font_size=40,
            color=TEXT,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.42)
        board = self.make_equation_board().shift(DOWN * 0.18)
        board_shell = VGroup(board.glow, board.frame)
        board_intro = VGroup(board.principles, board.principle_chips)
        board_cards = board.equation_cards
        board_domains = board.domain_group

        assert_in_frame(VGroup(title, board_shell, board_intro, board_cards, board_domains), margin=0.35, label="equation_board")

        self.add(background)
        self.play_timed(
            "first_principles_board",
            0.0,
            10.0,
            FadeIn(title, shift=DOWN * 0.15),
            FadeIn(board_shell, shift=UP * 0.12),
            LaggedStart(Write(board.principles), FadeIn(board.principle_chips, shift=UP * 0.1), lag_ratio=0.28),
        )
        self.play_timed(
            "equation_cards",
            10.0,
            22.0,
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in board_cards], lag_ratio=0.16),
        )
        self.play_timed(
            "domain_equation_names",
            22.0,
            35.0,
            FadeOut(board_cards, shift=DOWN * 0.12),
            LaggedStart(Write(board.center_formula), *[FadeIn(chip, scale=0.96) for chip in board.domain_chips], lag_ratio=0.11),
        )
        self.wait_timed("pause_hold_equations", 35.0, 36.0)

        mesh = self.make_continuum_mesh()
        mesh.coarse_grid.set_opacity(0)
        mesh.fine_grid.set_opacity(0)
        mesh.arrow.set_opacity(0)
        mesh.mesh_caption.set_opacity(0)
        mesh.shift(RIGHT * 0.72)
        assert_in_frame(mesh, margin=0.35, label="mesh")

        self.play_timed(
            "discretize_continuum",
            36.0,
            50.5,
            FadeOut(VGroup(title, board_shell, board_intro, board_domains), shift=LEFT * 0.35),
            FadeIn(mesh.panel, shift=RIGHT * 0.2),
            FadeIn(mesh.field, scale=0.98),
            FadeIn(mesh.label, shift=UP * 0.1),
            mesh.coarse_grid.animate.set_opacity(0.8),
            mesh.fine_grid.animate.set_opacity(0.46),
            mesh.arrow.animate.set_opacity(0.62),
            mesh.mesh_caption.animate.set_opacity(1.0),
        )

        pipeline_title = SafeText(
            "From continuum model to numerical solution",
            max_width=8.4,
            max_height=0.45,
            font_size=28,
            color=MUTED,
        )
        pipeline_title.to_edge(UP, buff=0.55)
        pipeline = self.make_solver_pipeline()
        solver = pipeline[1][1]
        assert_in_frame(VGroup(pipeline_title, pipeline), margin=0.35, label="solver_pipeline")

        self.play_timed(
            "solver_pipeline",
            50.5,
            66.0,
            FadeOut(mesh, shift=LEFT * 0.28),
            FadeIn(pipeline_title, shift=DOWN * 0.12),
            FadeIn(pipeline[1][0], shift=RIGHT * 0.16),
            LaggedStart(*[Create(arrow) for arrow in pipeline[0]], lag_ratio=0.28),
            FadeIn(solver, scale=0.98),
            FadeIn(pipeline[1][2], shift=LEFT * 0.16),
            FadeIn(pipeline[2], shift=UP * 0.1),
            Rotate(solver.gears[0], angle=PI),
            Rotate(solver.gears[1], angle=-PI),
            Rotate(solver.gears[2], angle=PI),
            solver.scanline.animate.shift(UP * 0.72),
            solver.dots.animate.shift(RIGHT * 0.18),
        )

        toolbox = self.make_toolbox()
        assert_in_frame(toolbox, margin=0.35, label="toolbox")
        ambient_orbit = Circle(radius=3.25, color=OUTPUT, stroke_width=1.1, stroke_opacity=0.16)
        ambient_orbit.move_to(toolbox.frame)

        self.play_timed(
            "toolbox_intro",
            66.0,
            72.0,
            FadeOut(VGroup(pipeline_title, pipeline), shift=DOWN * 0.2),
            FadeIn(toolbox, shift=UP * 0.18),
            Create(ambient_orbit),
        )
        self.play_timed(
            "toolbox_complement_hold",
            72.0,
            95.0,
            toolbox.glow.animate.set_stroke(opacity=0.16),
            Rotate(ambient_orbit, angle=TAU),
        )
        self.pad_to(self.SCENE_DURATION)
