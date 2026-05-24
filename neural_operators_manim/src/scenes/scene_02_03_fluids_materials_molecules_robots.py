"""
Scene 2.3 - Fluids, materials, molecules, robots
Script: docs/full_voice_manim_script.md
Global time: 10:45.0-12:55.0
Local duration: 130.0s

Asset-free generated Manim scene: four scientific domains are drawn as
animated mathematical objects, then distilled into function notation and
continuous-domain constraints.
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_chip
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    TEXT,
    MUTED,
    INPUT,
    OUTPUT,
    OPERATOR,
    WARNING,
    PURPLE,
    NVIDIA_GREEN,
    PHYSICS,
    SCIENCE,
)
from src.common.timing import TimedScene


apply_global_config()


def smooth_path(points, color=TEXT, stroke_width=2.0, stroke_opacity=1.0):
    """Return a smooth VMobject through explicit points."""
    curve = VMobject(color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
    curve.set_points_smoothly([np.array(p) for p in points])
    return curve


def make_panel_frame(title, subtitle, accent, width=3.35, height=2.55):
    """Small reusable panel frame used by the four-domain montage."""
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=accent,
        stroke_width=1.35,
        fill_color=CARD_BG,
        fill_opacity=0.82,
    )
    title_text = Text(title, font_size=23, color=TEXT)
    subtitle_text = Text(subtitle, font_size=13, color=MUTED)
    header = VGroup(title_text, subtitle_text).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
    header.next_to(frame.get_corner(UL), DOWN + RIGHT, buff=0.16)
    return VGroup(frame, header)


class FlowField(VGroup):
    """Car CFD panel: velocity field, pressure field, turbulence field."""

    def __init__(self, **kwargs):
        frame = make_panel_frame("CFD", "velocity / pressure / turbulence", INPUT)

        car_body = RoundedRectangle(
            width=1.35,
            height=0.42,
            corner_radius=0.18,
            stroke_color=TEXT,
            stroke_width=1.4,
            fill_color=GRID,
            fill_opacity=0.8,
        ).shift(DOWN * 0.2)
        cabin = Polygon(
            [-0.28, 0.02, 0],
            [0.12, 0.36, 0],
            [0.5, 0.32, 0],
            [0.68, 0.02, 0],
            color=TEXT,
            fill_color=GRID,
            fill_opacity=0.75,
            stroke_width=1.2,
        ).shift(DOWN * 0.2)
        wheels = VGroup(
            Circle(radius=0.11, color=MUTED, stroke_width=1.2).move_to([-0.47, -0.46, 0]),
            Circle(radius=0.11, color=MUTED, stroke_width=1.2).move_to([0.48, -0.46, 0]),
        )

        streamlines = VGroup()
        for y in np.linspace(-0.75, 0.75, 7):
            pts = []
            for x in np.linspace(-1.45, 1.45, 24):
                bump = 0.25 * np.exp(-((x + 0.05) ** 2) / 0.33)
                curl = 0.08 * np.sin(3.2 * x + 4.0 * y)
                pts.append([x, y + np.sign(y if y != 0 else 1) * bump + curl, 0])
            streamlines.add(smooth_path(pts, color=SCIENCE, stroke_width=1.15, stroke_opacity=0.72))

        wake = VGroup(
            *[
                Dot([1.0 + 0.18 * i, 0.24 * np.sin(i), 0], radius=0.028, color=OPERATOR, fill_opacity=0.74)
                for i in range(8)
            ]
        )
        equation = Text("CFD: v(x,t), p(x,t)", color=TEXT, font_size=21).next_to(frame[0], DOWN, buff=0.12)
        chips = VGroup(
            make_chip("geometry", color=SCIENCE, width=1.2, font_size=13),
            make_chip("boundary", color=OPERATOR, width=1.2, font_size=13),
        ).arrange(RIGHT, buff=0.12)
        chips.move_to(frame[0].get_top() + DOWN * 0.52 + RIGHT * 0.6)

        visual = VGroup(streamlines, car_body, cabin, wheels, wake).move_to(frame[0].get_center() + DOWN * 0.05)
        visual.scale(0.68)
        super().__init__(frame, visual, chips, equation, **kwargs)


class DeformationMesh(VGroup):
    """Material deformation panel: mesh field with warped geometry."""

    def __init__(self, **kwargs):
        frame = make_panel_frame("Material", "deformation field", OUTPUT)

        width, height = 2.55, 1.42

        def warp(x, y):
            punch = 0.33 * np.exp(-((x - 0.05) ** 2 + (y - 0.18) ** 2) / 0.26)
            shear = 0.08 * np.sin(4.5 * y)
            return np.array([x + shear, y - punch + 0.04 * np.sin(4.0 * x), 0])

        mesh_lines = VGroup()
        for i in range(8):
            x = -width / 2 + width * i / 7
            pts = [warp(x, -height / 2 + height * j / 20) for j in range(21)]
            mesh_lines.add(smooth_path(pts, color=NVIDIA_GREEN, stroke_width=1.0, stroke_opacity=0.75))
        for j in range(6):
            y = -height / 2 + height * j / 5
            pts = [warp(-width / 2 + width * i / 22, y) for i in range(23)]
            mesh_lines.add(smooth_path(pts, color=NVIDIA_GREEN, stroke_width=1.0, stroke_opacity=0.75))

        press_plate = Rectangle(width=0.7, height=0.2, color=OPERATOR, fill_color=OPERATOR, fill_opacity=0.32)
        press_plate.move_to(UP * 0.83)
        force_arrow = Arrow(UP * 1.08, UP * 0.78, color=OPERATOR, stroke_width=2.1, max_tip_length_to_length_ratio=0.22)
        boundary = DashedVMobject(
            RoundedRectangle(width=2.72, height=1.55, corner_radius=0.05, color=WARNING, stroke_width=1.0),
            num_dashes=36,
        )

        visual = VGroup(mesh_lines, press_plate, force_arrow, boundary).move_to(frame[0].get_center() + DOWN * 0.04)
        visual.scale(0.72)
        equation = Text("deformation: d(x,t)", color=TEXT, font_size=21).next_to(frame[0], DOWN, buff=0.12)
        chips = VGroup(
            make_chip("stress", color=NVIDIA_GREEN, width=0.9, font_size=13),
            make_chip("discontinuity", color=WARNING, width=1.32, font_size=13),
        ).arrange(RIGHT, buff=0.12)
        chips.move_to(frame[0].get_top() + DOWN * 0.52 + RIGHT * 0.52)
        super().__init__(frame, visual, chips, equation, **kwargs)


class TrajectoryCurve(VGroup):
    """Molecular dynamics panel: continuous trajectories in time."""

    def __init__(self, **kwargs):
        frame = make_panel_frame("Molecules", "continuous state over time", PURPLE)

        rng = np.random.default_rng(23)
        atoms = VGroup()
        bonds = VGroup()
        centers = [
            np.array([-0.72, -0.25, 0]),
            np.array([-0.18, 0.24, 0]),
            np.array([0.42, 0.02, 0]),
            np.array([0.86, 0.42, 0]),
        ]
        for a, b in zip(centers[:-1], centers[1:]):
            bonds.add(Line(a, b, color=MUTED, stroke_width=2.0, stroke_opacity=0.76))
        for i, c in enumerate(centers):
            atoms.add(
                Circle(radius=0.13 + 0.03 * (i % 2), color=PURPLE, stroke_width=1.4, fill_color=PURPLE, fill_opacity=0.45)
                .move_to(c + rng.normal(0, 0.018, 3))
            )

        trails = VGroup()
        for i, c in enumerate(centers):
            pts = []
            for t in np.linspace(0, 1, 34):
                pts.append(
                    c
                    + np.array(
                        [
                            0.22 * t - 0.04 * np.sin(5 * t + i),
                            0.13 * np.sin(2.5 * PI * t + i * 0.5),
                            0,
                        ]
                    )
                )
            trails.add(smooth_path(pts, color=SCIENCE, stroke_width=1.15, stroke_opacity=0.78))

        time_axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=1.8,
            include_numbers=False,
            color=GRID,
            stroke_width=1.1,
        ).move_to(DOWN * 0.82)
        time_label = MathTex(r"t", color=MUTED, font_size=20).next_to(time_axis, RIGHT, buff=0.06)

        visual = VGroup(trails, bonds, atoms, time_axis, time_label).move_to(frame[0].get_center() + DOWN * 0.04)
        visual.scale(0.78)
        equation = Text("state: q(t)", color=TEXT, font_size=22).next_to(frame[0], DOWN, buff=0.12)
        chips = VGroup(
            make_chip("trajectory", color=PURPLE, width=1.05, font_size=13),
            make_chip("not frames", color=WARNING, width=1.05, font_size=13),
        ).arrange(RIGHT, buff=0.12)
        chips.move_to(frame[0].get_top() + DOWN * 0.52 + RIGHT * 0.54)
        super().__init__(frame, visual, chips, equation, **kwargs)


class RobotJointPath(VGroup):
    """Robotics panel: joint angle as a continuous time function."""

    def __init__(self, **kwargs):
        frame = make_panel_frame("Robotics", "joint motion trajectory", OPERATOR)

        shoulder = Dot(LEFT * 0.5 + UP * 0.25, radius=0.06, color=OPERATOR)
        elbow = Dot(RIGHT * 0.12, radius=0.055, color=OPERATOR)
        wrist = Dot(RIGHT * 0.74 + DOWN * 0.34, radius=0.052, color=OPERATOR)
        arm = VGroup(
            Line(shoulder.get_center(), elbow.get_center(), color=TEXT, stroke_width=4.0),
            Line(elbow.get_center(), wrist.get_center(), color=TEXT, stroke_width=4.0),
            shoulder,
            elbow,
            wrist,
        )
        joint_arc = Arc(radius=0.32, start_angle=-0.45, angle=1.05, color=SCIENCE, stroke_width=2.2).move_arc_center_to(elbow.get_center())
        path = ParametricFunction(
            lambda t: np.array([1.2 * t - 0.6, 0.28 * np.sin(2.5 * PI * t), 0]),
            t_range=[0, 1, 0.02],
            color=SCIENCE,
            stroke_width=2.0,
        ).shift(DOWN * 0.82)
        path_label = MathTex(r"\theta(t)", color=TEXT, font_size=22).next_to(path, RIGHT, buff=0.08)

        visual = VGroup(arm, joint_arc, path, path_label).move_to(frame[0].get_center() + DOWN * 0.04)
        visual.scale(0.82)
        equation = Text("joint motion: theta(t)", color=TEXT, font_size=21).next_to(frame[0], DOWN, buff=0.12)
        chips = VGroup(
            make_chip("time domain", color=OPERATOR, width=1.18, font_size=13),
            make_chip("control", color=SCIENCE, width=0.9, font_size=13),
        ).arrange(RIGHT, buff=0.12)
        chips.move_to(frame[0].get_top() + DOWN * 0.52 + RIGHT * 0.48)
        super().__init__(frame, visual, chips, equation, **kwargs)


class PanelGrid(VGroup):
    """Four-domain montage requested by the script."""

    def __init__(self, **kwargs):
        panels = VGroup(
            FlowField(),
            DeformationMesh(),
            TrajectoryCurve(),
            RobotJointPath(),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.68, 0.82))
        panels.scale(0.88).move_to(LEFT * 0.02 + DOWN * 0.02)
        super().__init__(*panels, **kwargs)


class BoundaryHighlight(VGroup):
    """Reusable boundary/domain marker overlay."""

    def __init__(self, label="boundary", width=3.35, height=2.55, color=WARNING, **kwargs):
        rect = DashedVMobject(
            RoundedRectangle(width=width, height=height, corner_radius=0.12, color=color, stroke_width=1.6),
            num_dashes=38,
        )
        tag = make_chip(label, color=color, width=max(1.0, 0.15 * len(label) + 0.45), font_size=14)
        tag.next_to(rect, UP, buff=0.06)
        super().__init__(rect, tag, **kwargs)


class Scene0203FluidsMaterialsMoleculesRobots(TimedScene):
    SCRIPT_ID = "2.3"
    SCRIPT_TITLE = "Fluids, materials, molecules, robots"
    SCRIPT_START = 645.0
    SCRIPT_END = 775.0
    SCENE_DURATION = 130.0

    def make_flow_field(self):
        return FlowField()

    def make_deformation_mesh(self):
        return DeformationMesh()

    def make_molecule_trajectory(self):
        return TrajectoryCurve()

    def make_robot_joint_path(self):
        return RobotJointPath()

    def make_panel_grid(self):
        return PanelGrid()

    def make_domain_markers(self):
        chips = VGroup(
            make_chip("domain", color=INPUT, width=1.05, font_size=18),
            make_chip("geometry", color=PURPLE, width=1.15, font_size=18),
            make_chip("boundary", color=OPERATOR, width=1.15, font_size=18),
            make_chip("physics law", color=PHYSICS, width=1.35, font_size=18),
        ).arrange(RIGHT, buff=0.18)
        title = Text("Not images. Functions on domains.", font_size=32, color=TEXT)
        subtitle = Text(
            "same technical structure: domain + geometry + boundary + physics laws",
            font_size=19,
            color=MUTED,
        )
        return VGroup(title, subtitle, chips).arrange(DOWN, buff=0.22)

    def make_refinement_icon(self):
        coarse = VGroup(
            *[Line([-0.45 + i * 0.3, -0.45, 0], [-0.45 + i * 0.3, 0.45, 0], color=GRID, stroke_width=1.0) for i in range(4)],
            *[Line([-0.45, -0.45 + i * 0.3, 0], [0.45, -0.45 + i * 0.3, 0], color=GRID, stroke_width=1.0) for i in range(4)],
        )
        fine = VGroup(
            *[Line([-0.45 + i * 0.15, -0.45, 0], [-0.45 + i * 0.15, 0.45, 0], color=INPUT, stroke_width=0.75) for i in range(7)],
            *[Line([-0.45, -0.45 + i * 0.15, 0], [0.45, -0.45 + i * 0.15, 0], color=INPUT, stroke_width=0.75) for i in range(7)],
        ).shift(RIGHT * 1.1)
        arrow = Arrow(coarse.get_right() + RIGHT * 0.08, fine.get_left() + LEFT * 0.08, color=OPERATOR, stroke_width=2.0, buff=0.0)
        return VGroup(coarse, arrow, fine).scale(0.58)

    def make_query_icon(self):
        domain = Circle(radius=0.46, color=PURPLE, stroke_width=1.2, fill_color=CARD_BG, fill_opacity=0.35)
        point = Dot(RIGHT * 0.12 + UP * 0.08, radius=0.055, color=OPERATOR)
        crosshair = VGroup(
            Line(point.get_center() + LEFT * 0.18, point.get_center() + RIGHT * 0.18, color=OPERATOR, stroke_width=1.2),
            Line(point.get_center() + DOWN * 0.18, point.get_center() + UP * 0.18, color=OPERATOR, stroke_width=1.2),
        )
        return VGroup(domain, crosshair, point)

    def make_derivative_icon(self):
        axes = VGroup(
            Line(LEFT * 0.55 + DOWN * 0.35, RIGHT * 0.55 + DOWN * 0.35, color=GRID, stroke_width=1.0),
            Line(LEFT * 0.55 + DOWN * 0.35, LEFT * 0.55 + UP * 0.42, color=GRID, stroke_width=1.0),
        )
        curve = ParametricFunction(
            lambda t: np.array([1.0 * t - 0.5, 0.23 * np.sin(PI * (t + 0.12)), 0]),
            t_range=[0, 1, 0.02],
            color=INPUT,
            stroke_width=2.0,
        )
        tangent = Line(LEFT * 0.12, RIGHT * 0.42 + UP * 0.22, color=WARNING, stroke_width=2.1)
        return VGroup(axes, curve, tangent)

    def make_integral_icon(self):
        base = Line(LEFT * 0.55 + DOWN * 0.35, RIGHT * 0.55 + DOWN * 0.35, color=GRID, stroke_width=1.0)
        area = Polygon(
            [-0.5, -0.35, 0],
            [-0.32, 0.0, 0],
            [-0.05, 0.18, 0],
            [0.27, 0.06, 0],
            [0.5, -0.35, 0],
            color=OUTPUT,
            fill_color=OUTPUT,
            fill_opacity=0.22,
            stroke_width=1.2,
        )
        symbol = MathTex(r"\int", color=OUTPUT, font_size=34).next_to(area, RIGHT, buff=0.02)
        return VGroup(base, area, symbol)

    def make_final_icon_card(self, label, icon, color, width=2.28, height=1.38):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=color,
            stroke_width=1.1,
            fill_color=CARD_BG,
            fill_opacity=0.80,
        )
        icon = icon.scale(0.84)
        icon.move_to(box.get_center() + UP * 0.18)
        text = Text(label, font_size=16, color=TEXT)
        text.move_to(box.get_bottom() + UP * 0.23)
        return VGroup(box, icon, text)

    def make_error_stack(self):
        wrong_prediction = RoundedRectangle(
            width=4.75,
            height=2.3,
            corner_radius=0.12,
            stroke_color=WARNING,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.88,
        )
        nice_picture = Text("Prediction looks plausible", font_size=25, color=TEXT)
        failures = VGroup(
            make_chip("wrong derivative", color=WARNING, width=1.72, font_size=15),
            make_chip("breaks conservation", color=WARNING, width=1.95, font_size=15),
            make_chip("bad boundary", color=WARNING, width=1.48, font_size=15),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        field = self.make_toy_field(width=2.0, height=1.35)
        field.move_to(wrong_prediction.get_left() + RIGHT * 1.25)
        failures.move_to(wrong_prediction.get_right() + LEFT * 1.26)
        nice_picture.next_to(wrong_prediction, UP, buff=0.15)
        cross = Cross(wrong_prediction, stroke_color=WARNING, stroke_width=2.2).scale(0.98)
        return VGroup(wrong_prediction, field, failures, nice_picture, cross)

    def make_toy_field(self, width=2.0, height=1.35):
        lines = VGroup()
        for y in np.linspace(-height / 2, height / 2, 7):
            pts = []
            for x in np.linspace(-width / 2, width / 2, 30):
                pts.append([x, y + 0.12 * np.sin(3.8 * x + 2.0 * y), 0])
            lines.add(smooth_path(pts, color=SCIENCE, stroke_width=1.05, stroke_opacity=0.72))
        boundary = Rectangle(width=width, height=height, color=WARNING, stroke_width=1.2)
        query = Dot([0.32, 0.16, 0], radius=0.045, color=OPERATOR)
        return VGroup(lines, boundary, query)

    def make_function_contract(self):
        left = RoundedRectangle(
            width=3.45,
            height=2.35,
            corner_radius=0.15,
            color=INPUT,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.88,
        )
        right = RoundedRectangle(
            width=3.45,
            height=2.35,
            corner_radius=0.15,
            color=OUTPUT,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.88,
        )
        left_title = Text("Function-valued data", font_size=26, color=TEXT).move_to(left.get_top() + DOWN * 0.38)
        right_title = Text("Model contract", font_size=26, color=TEXT).move_to(right.get_top() + DOWN * 0.38)
        left_items = VGroup(
            MathTex(r"v(x,t),\; p(x,t),\; d(x,t),\; q(t)", color=TEXT, font_size=24),
            Text("defined on a domain", font_size=18, color=MUTED),
            Text("mesh is only the measurement layer", font_size=16, color=MUTED),
        ).arrange(DOWN, buff=0.16).move_to(left.get_center() + DOWN * 0.1)
        right_items = VGroup(
            Text("respect domain", font_size=18, color=TEXT),
            Text("respect discretization", font_size=18, color=TEXT),
            Text("support derivatives & integrals", font_size=18, color=TEXT),
            Text("handle boundary behavior", font_size=18, color=TEXT),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(right.get_center() + DOWN * 0.1)
        left_group = VGroup(left, left_title, left_items).shift(LEFT * 2.25)
        right_group = VGroup(right, right_title, right_items).shift(RIGHT * 2.25)
        arrow = Arrow(
            left_group.get_right() + RIGHT * 0.18,
            right_group.get_left() + LEFT * 0.18,
            color=OPERATOR,
            stroke_width=3.0,
            buff=0.0,
        )
        operator = MathTex(r"\mathcal{G}", color=OPERATOR, font_size=42).next_to(arrow, UP, buff=0.04)
        synthesis_title = Text("A model for function data must respect:", font_size=28, color=TEXT)
        synthesis_title.next_to(VGroup(left_group, right_group), UP, buff=0.28)
        icon_row = VGroup(
            self.make_final_icon_card("mesh refinement", self.make_refinement_icon(), INPUT),
            self.make_final_icon_card("query point", self.make_query_icon(), OPERATOR),
            self.make_final_icon_card("derivative", self.make_derivative_icon(), WARNING),
            self.make_final_icon_card("integral", self.make_integral_icon(), OUTPUT),
        ).arrange(RIGHT, buff=0.18)
        icon_row.next_to(VGroup(left_group, right_group), DOWN, buff=0.22)
        board = VGroup(synthesis_title, left_group, right_group, arrow, operator, icon_row)
        board.move_to(ORIGIN)
        return board

    def construct(self):
        title = Text("Fluids, materials, molecules, robots", font_size=28, color=TEXT)
        title.to_edge(UP, buff=0.22)
        section_tag = make_chip("Real-world data are functions", color=NVIDIA_GREEN, width=2.55, font_size=15)
        section_tag.next_to(title, DOWN, buff=0.08)

        grid = self.make_panel_grid()
        cfd_panel, material_panel, molecule_panel, robot_panel = grid

        cfd_math = MathTex(r"v(x,t),\;p(x,t)", color=INPUT, font_size=40).move_to(RIGHT * 4.5 + UP * 1.55)
        material_math = MathTex(r"d(x,t)", color=OUTPUT, font_size=42).move_to(RIGHT * 4.5 + UP * 0.55)
        molecule_math = MathTex(r"q(t)", color=PURPLE, font_size=44).move_to(RIGHT * 4.5 + DOWN * 0.55)
        robot_math = MathTex(r"\theta(t)", color=OPERATOR, font_size=42).move_to(RIGHT * 4.5 + DOWN * 1.55)
        math_column = VGroup(cfd_math, material_math, molecule_math, robot_math)
        math_column_box = SurroundingRectangle(math_column, buff=0.22, color=GRID, stroke_width=1.0)

        domain_markers = self.make_domain_markers().scale(0.86).to_edge(DOWN, buff=0.25)
        panel_boundary_overlays = VGroup(
            BoundaryHighlight("domain / boundary", color=INPUT).scale(0.88).move_to(cfd_panel[0][0]),
            BoundaryHighlight("deforming domain", color=OUTPUT).scale(0.88).move_to(material_panel[0][0]),
            BoundaryHighlight("time domain", color=PURPLE).scale(0.88).move_to(molecule_panel[0][0]),
            BoundaryHighlight("trajectory domain", color=OPERATOR).scale(0.88).move_to(robot_panel[0][0]),
        )

        error_stack = self.make_error_stack().scale(0.92).move_to(LEFT * 4.15 + DOWN * 0.08)
        field_for_ops = self.make_toy_field(width=3.05, height=2.05).move_to(RIGHT * 3.1 + UP * 0.18)
        continuous_ops = VGroup(
            make_chip("differentiate", color=INPUT, width=1.45, font_size=17),
            make_chip("integrate", color=OUTPUT, width=1.12, font_size=17),
            make_chip("conserve", color=PHYSICS, width=1.2, font_size=17),
            make_chip("query", color=OPERATOR, width=0.86, font_size=17),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        continuous_ops.next_to(field_for_ops, RIGHT, buff=0.32)
        final_contract = self.make_function_contract().scale(1.05).move_to(UP * 0.08)
        final_question = Text(
            "data is function  =>  technical contract, not a visual vibe",
            font_size=26,
            color=TEXT,
        ).next_to(final_contract, DOWN, buff=0.38)

        self.add(title, section_tag)

        # Global 10:45.0-10:55.5 => local 0.0-10.5
        self.play_timed(
            "cfd_velocity_pressure_turbulence_field",
            0.0,
            10.5,
            FadeIn(cfd_panel, shift=UP * 0.18),
            Write(cfd_math),
        )

        # Global 10:55.5-11:07.0 => local 10.5-22.0
        self.play_timed(
            "material_deformation_is_field",
            10.5,
            22.0,
            FadeIn(material_panel, shift=UP * 0.18),
            Write(material_math),
        )

        # Global 11:07.0-11:20.0 => local 22.0-35.0
        self.play_timed(
            "molecular_dynamics_continuous_trajectory",
            22.0,
            35.0,
            FadeIn(molecule_panel, shift=DOWN * 0.18),
            Write(molecule_math),
        )

        # Global 11:20.0-11:32.0 => local 35.0-47.0
        self.play_timed(
            "robotics_joint_motion_continuous_time_function",
            35.0,
            47.0,
            FadeIn(robot_panel, shift=DOWN * 0.18),
            Write(robot_math),
            FadeIn(math_column_box),
        )

        # Global 11:32.0-11:33.0 => local 47.0-48.0
        self.wait_timed("pause_before_common_structure", 47.0, 48.0)

        # Global 11:33.0-11:46.0 => local 48.0-61.0
        self.play_timed(
            "common_domain_geometry_laws_not_just_images",
            48.0,
            61.0,
            LaggedStart(*[FadeIn(marker, scale=1.02) for marker in panel_boundary_overlays], lag_ratio=0.08),
            FadeIn(domain_markers, shift=UP * 0.18),
            grid.animate.scale(0.94).shift(LEFT * 0.18 + UP * 0.04),
            math_column.animate.set_opacity(0.92),
        )

        # Global 11:46.0-12:10.0 => local 61.0-85.0
        self.play_timed(
            "plausible_picture_can_fail_physics",
            61.0,
            66.0,
            FadeOut(panel_boundary_overlays),
            FadeOut(domain_markers),
            FadeOut(math_column_box),
            math_column.animate.shift(RIGHT * 0.25).set_opacity(0.35),
            grid.animate.scale(0.62).to_edge(RIGHT, buff=0.28),
            FadeIn(error_stack, shift=LEFT * 0.2),
        )
        self.play_timed(
            "derivative_conservation_boundary_failures",
            66.0,
            77.0,
            error_stack[4].animate.set_stroke(opacity=0.72),
            grid.animate.set_opacity(0.42),
            rate_func=there_and_back,
        )
        self.play_timed(
            "continuous_operations_need_domain",
            77.0,
            85.0,
            FadeOut(grid),
            FadeOut(math_column),
            FadeIn(field_for_ops, shift=RIGHT * 0.14),
            LaggedStart(*[FadeIn(chip, shift=RIGHT * 0.08) for chip in continuous_ops], lag_ratio=0.14),
        )

        # Global 12:10.0-12:55.0 => local 85.0-130.0
        self.play_timed(
            "clear_to_function_data_contract",
            85.0,
            92.0,
            FadeOut(error_stack),
            FadeOut(field_for_ops),
            FadeOut(continuous_ops),
            FadeOut(title),
            FadeOut(section_tag),
        )
        self.play_timed(
            "function_contract_appears",
            92.0,
            108.0,
            FadeIn(final_contract[0], shift=DOWN * 0.12),
            FadeIn(final_contract[1], shift=LEFT * 0.2),
            FadeIn(final_contract[3]),
            FadeIn(final_contract[4]),
            FadeIn(final_contract[2], shift=RIGHT * 0.2),
        )
        self.play_timed(
            "respect_domain_discretization_continuous_ops",
            108.0,
            124.0,
            final_contract.animate.scale(1.02),
            FadeIn(final_contract[5], shift=UP * 0.12),
            FadeIn(final_question, shift=UP * 0.12),
        )
        self.play_timed(
            "final_hold_function_requirements",
            124.0,
            130.0,
            final_question.animate.set_color(NVIDIA_GREEN),
            final_contract[2].animate.set_stroke(opacity=0.95),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
