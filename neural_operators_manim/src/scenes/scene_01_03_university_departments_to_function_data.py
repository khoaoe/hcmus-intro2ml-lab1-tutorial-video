"""
Scene 1.3 - From university departments to function data
Script: docs/full_voice_manim_script.md
Global time: 05:20.0-07:20.0
Local duration: 120.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import (
    make_car_cfd_icon,
    make_deformation_mesh_icon,
    make_mesh_overlay as make_function_mesh_overlay,
    make_molecule_trajectory_icon,
    make_query_point_with_interpolation,
    make_seismic_wave_icon,
    make_weather_sphere_icon,
    smooth_path,
)
from src.common.layout import make_background_network, make_card, make_chip
from src.common.theme import (
    apply_global_config,
    BG,
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


DEPARTMENT_POSITIONS = {
    "Mechanical Engineering": np.array([-4.75, 1.15, 0.0]),
    "Geophysics": np.array([-2.35, -1.15, 0.0]),
    "Chemistry / Medicine": np.array([0.25, 1.12, 0.0]),
    "Climate Science": np.array([3.6, 1.28, 0.0]),
    "Materials Science": np.array([4.42, -1.12, 0.0]),
}


class CampusMap(VGroup):
    def __init__(self, **kwargs):
        paths = VGroup(
            Line([-5.8, 0.02, 0], [5.85, 0.02, 0], color=GRID, stroke_width=4.0, stroke_opacity=0.74),
            Line([-1.0, -2.05, 0], [1.25, 2.05, 0], color=GRID, stroke_width=3.4, stroke_opacity=0.68),
            smooth_path(
                [[-5.6, -1.8, 0], [-3.2, -0.3, 0], [-0.2, -0.7, 0], [2.7, 0.45, 0], [5.6, -1.65, 0]],
                color=GRID,
                stroke_width=2.4,
                stroke_opacity=0.58,
            ),
        )
        lawn = RoundedRectangle(
            width=12.4,
            height=4.55,
            corner_radius=0.08,
            stroke_color=GRID,
            stroke_width=1.2,
            fill_color="#0D1B2A",
            fill_opacity=0.54,
        )
        buildings = VGroup()
        nodes = {}
        colors = [INPUT, OPERATOR, PURPLE, SCIENCE, NVIDIA_GREEN]
        for i, (label, pos) in enumerate(DEPARTMENT_POSITIONS.items()):
            building = RoundedRectangle(
                width=1.24,
                height=0.72,
                corner_radius=0.06,
                stroke_color=colors[i],
                stroke_width=1.3,
                fill_color=CARD_BG,
                fill_opacity=0.76,
            ).move_to(pos)
            roof = Line(
                building.get_corner(UL) + RIGHT * 0.1,
                building.get_corner(UR) + LEFT * 0.1,
                color=colors[i],
                stroke_width=2.0,
                stroke_opacity=0.75,
            )
            node = Dot(pos, radius=0.06, color=colors[i])
            glow = Circle(radius=0.2, color=colors[i], stroke_width=1.2, stroke_opacity=0.34).move_to(pos)
            buildings.add(VGroup(building, roof, glow, node))
            nodes[label] = node
        quad = Circle(radius=0.32, color=PHYSICS, stroke_width=1.2, stroke_opacity=0.5).move_to([0, 0.02, 0])
        super().__init__(lawn, paths, quad, buildings, **kwargs)
        self.nodes = nodes
        self.buildings = buildings


class DepartmentLabels(VGroup):
    def __init__(self, positions=None, **kwargs):
        positions = positions or DEPARTMENT_POSITIONS
        label_offsets = {
            "Mechanical Engineering": UP * 0.62,
            "Geophysics": DOWN * 0.58,
            "Chemistry / Medicine": UP * 0.62,
            "Climate Science": UP * 0.62,
            "Materials Science": DOWN * 0.58,
        }
        colors = {
            "Mechanical Engineering": INPUT,
            "Geophysics": OPERATOR,
            "Chemistry / Medicine": PURPLE,
            "Climate Science": SCIENCE,
            "Materials Science": NVIDIA_GREEN,
        }
        labels = []
        for label, pos in positions.items():
            chip = make_chip(label, color=colors[label], font_size=13, height=0.34)
            chip.move_to(pos + label_offsets[label])
            labels.append(chip)
        super().__init__(*labels, **kwargs)


class FieldVisuals(VGroup):
    def __init__(self, **kwargs):
        self.car = make_car_cfd_icon().scale(0.72).move_to([-4.85, -2.55, 0])
        self.seismic = make_seismic_wave_icon().scale(0.78).move_to([-1.7, -2.55, 0])
        self.molecule = make_molecule_trajectory_icon().scale(0.82).move_to([1.35, -2.55, 0])
        self.weather = make_weather_sphere_icon().scale(0.76).move_to([4.45, -2.55, 0])
        self.materials = make_deformation_mesh_icon().scale(0.68).move_to([5.45, -0.65, 0])
        super().__init__(self.car, self.seismic, self.molecule, self.weather, self.materials, **kwargs)


class MeshOverlay(VGroup):
    def __init__(self, width=3.1, height=1.95, nx=9, ny=6, **kwargs):
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            stroke_color=SCIENCE,
            stroke_width=1.4,
            fill_color="#061E26",
            fill_opacity=0.14,
        )
        mesh = make_function_mesh_overlay(width=width, height=height, nx=nx, ny=ny, color=TEXT)
        super().__init__(frame, mesh, **kwargs)


class ZoomedGrid(VGroup):
    def __init__(self, **kwargs):
        frame = RoundedRectangle(
            width=5.1,
            height=3.05,
            corner_radius=0.08,
            stroke_color=SCIENCE,
            stroke_width=1.6,
            fill_color="#082635",
            fill_opacity=0.78,
        )
        field_bands = VGroup()
        for j, y in enumerate(np.linspace(-1.08, 1.08, 7)):
            field_bands.add(
                Line(
                    [-2.25, y, 0],
                    [2.25, y + 0.08 * np.sin(3 * y), 0],
                    color=[INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, WARNING, PURPLE, OUTPUT][j],
                    stroke_width=10,
                    stroke_opacity=0.22,
                )
            )
        query = make_query_point_with_interpolation(width=4.55, height=2.45)
        derivative = MathTex(r"\nabla", color=INPUT, font_size=44).move_to([1.86, 0.82, 0])
        integral = MathTex(r"\int", color=OPERATOR, font_size=48).move_to([-1.92, -0.82, 0])
        labels = VGroup(
            make_chip("change mesh", color=SCIENCE, font_size=15).move_to([-2.1, 1.78, 0]),
            make_chip("query anywhere", color=OPERATOR, font_size=15).move_to([0.38, 1.78, 0]),
            make_chip("differentiate", color=INPUT, font_size=15).move_to([2.55, 0.82, 0]),
            make_chip("integrate", color=OPERATOR, font_size=15).move_to([-2.55, -1.55, 0]),
        )
        super().__init__(frame, field_bands, query, derivative, integral, labels, **kwargs)


class Scene0103UniversityDepartmentsToFunctionData(TimedScene):
    SCRIPT_ID = "1.3"
    SCRIPT_TITLE = "From university departments to function data"
    SCRIPT_START = 320.0
    SCRIPT_END = 440.0
    SCENE_DURATION = 120.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_campus_map(self):
        return CampusMap()

    def make_department_labels(self):
        return DepartmentLabels()

    def make_field_visuals(self):
        return FieldVisuals()

    def make_mesh_overlay(self, width=3.1, height=1.95, nx=9, ny=6):
        return MeshOverlay(width=width, height=height, nx=nx, ny=ny)

    def make_zoomed_grid(self):
        return ZoomedGrid()

    def make_question_card(self, text, color, position):
        frame = RoundedRectangle(
            width=4.0,
            height=0.68,
            corner_radius=0.07,
            stroke_color=color,
            stroke_width=1.25,
            fill_color=CARD_BG,
            fill_opacity=0.86,
        )
        label = Text(text, font_size=22, color=TEXT)
        if label.width > frame.width - 0.32:
            label.scale_to_fit_width(frame.width - 0.32)
        label.move_to(frame)
        card = VGroup(frame, label).move_to(position)
        return card

    def make_previous_scene_cards(self):
        cat_card = make_card("cat/dog classification", "finite image label", width=2.55, height=0.78, color=INPUT)
        token_card = make_card("next-token prediction", "finite token sequence", width=2.55, height=0.78, color=PURPLE)
        cards = VGroup(cat_card, token_card).arrange(DOWN, buff=0.16)
        cards.set_opacity(0.42)
        cards.to_edge(LEFT, buff=0.42).shift(DOWN * 0.3)
        return cards

    def make_rendered_weather_frame(self):
        frame = RoundedRectangle(
            width=4.35,
            height=2.72,
            corner_radius=0.08,
            stroke_color=SCIENCE,
            stroke_width=1.6,
            fill_color="#071F2B",
            fill_opacity=0.84,
        )
        field = make_weather_sphere_icon(radius=0.86).move_to(frame.get_center() + UP * 0.05)
        field[5].set_opacity(0)
        pixels = make_function_mesh_overlay(width=3.45, height=2.05, nx=12, ny=7, color=MUTED)
        pixels.set_opacity(0.18)
        label = Text("looks like an image", font_size=25, color=TEXT).next_to(frame, DOWN, buff=0.18)
        return VGroup(frame, field, pixels, label)

    def make_two_worlds(self):
        # Canonical subtitle: same visual pixels, different mathematical object.
        left_title = Text("Euclidean vectors", font_size=31, color=MUTED, weight=BOLD)
        right_title = Text("Function Spaces", font_size=43, color=TEXT, weight=BOLD)
        right_title.set_color_by_gradient(TEXT, SCIENCE)
        subtitle = VGroup(
            Text("same visual pixels", font_size=21, color=MUTED),
            Text("different mathematical object", font_size=21, color=MUTED),
        ).arrange(DOWN, buff=0.04)
        vector = MathTex(r"x \in \mathbb{R}^n", color=MUTED, font_size=38)
        tensor = VGroup(*[Square(side_length=0.16, color=GRID, fill_color=INPUT, fill_opacity=0.35) for _ in range(36)])
        tensor.arrange_in_grid(rows=6, cols=6, buff=0.015)
        left_stack = VGroup(left_title, tensor, vector).arrange(DOWN, buff=0.28).move_to(LEFT * 4.0 + UP * 0.05)
        function_math = MathTex(r"u: \Omega \times [0,T] \to \mathbb{R}^k", color=SCIENCE, font_size=30)
        right_stack = VGroup(right_title, subtitle, function_math).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.35 + UP * 1.0)
        divider = Line(UP * 3.25, DOWN * 3.25, color=GRID, stroke_width=1.2, stroke_opacity=0.72)
        return VGroup(left_stack, divider, right_stack)

    def construct(self):
        background = make_background_network(seed=13, n=74)
        campus = self.make_campus_map().scale(0.96).move_to(DOWN * 0.1)
        dept_labels = self.make_department_labels()
        title = Text("A walk across campus", font_size=48, color=TEXT, weight=BOLD).to_edge(UP, buff=0.32)
        title.set_color_by_gradient(TEXT, SCIENCE)

        # Global 05:20.0-05:31.0 => local 0.0-11.0
        self.play_timed(
            "campus_departments_light_up",
            0.0,
            11.0,
            FadeIn(background),
            FadeIn(campus, shift=DOWN * 0.12),
            Write(title),
            LaggedStart(*[FadeIn(label, scale=0.92) for label in dept_labels], lag_ratio=0.18),
        )

        previous_cards = self.make_previous_scene_cards()
        science_label = Text(
            "Most scientific questions are not born as pixels or tokens.",
            font_size=30,
            color=TEXT,
        ).to_edge(DOWN, buff=0.42)
        compact_campus = VGroup(campus, dept_labels).copy().scale(0.88).shift(RIGHT * 0.55 + UP * 0.18)

        # Global 05:31.0-05:45.0 => local 11.0-25.0
        self.play_timed(
            "cv_nlp_cards_slide_aside",
            11.0,
            25.0,
            Transform(VGroup(campus, dept_labels), compact_campus),
            FadeIn(previous_cards, shift=LEFT * 0.22),
            FadeIn(science_label, shift=UP * 0.15),
            title.animate.scale(0.6).to_corner(UL, buff=0.24).set_opacity(0.72),
        )

        questions = VGroup(
            self.make_question_card("pressure around a car?", INPUT, [-4.85, -2.56, 0]),
            self.make_question_card("earthquake wave propagation?", OPERATOR, [0.0, -2.56, 0]),
            self.make_question_card("protein shape over time?", PURPLE, [4.85, -2.56, 0]),
        )
        question_lines = VGroup(
            Line(DEPARTMENT_POSITIONS["Mechanical Engineering"], questions[0].get_top(), color=INPUT, stroke_width=1.5, stroke_opacity=0.72),
            Line(DEPARTMENT_POSITIONS["Geophysics"], questions[1].get_top(), color=OPERATOR, stroke_width=1.5, stroke_opacity=0.72),
            Line(DEPARTMENT_POSITIONS["Chemistry / Medicine"], questions[2].get_top(), color=PURPLE, stroke_width=1.5, stroke_opacity=0.72),
        )

        # Global 05:45.0-05:56.5 => local 25.0-36.5
        self.play_timed(
            "department_questions_emit",
            25.0,
            36.5,
            FadeOut(previous_cards, shift=LEFT * 0.16),
            science_label.animate.set_opacity(0.55).shift(DOWN * 0.15),
            LaggedStart(*[Create(line) for line in question_lines], lag_ratio=0.18),
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in questions], lag_ratio=0.16),
        )

        fields = self.make_field_visuals()
        fields.scale(0.96)
        field_lines = VGroup(
            Line(DEPARTMENT_POSITIONS["Mechanical Engineering"], fields.car.get_top(), color=INPUT, stroke_width=1.4, stroke_opacity=0.65),
            Line(DEPARTMENT_POSITIONS["Geophysics"], fields.seismic.get_top(), color=OPERATOR, stroke_width=1.4, stroke_opacity=0.65),
            Line(DEPARTMENT_POSITIONS["Chemistry / Medicine"], fields.molecule.get_top(), color=PURPLE, stroke_width=1.4, stroke_opacity=0.65),
            Line(DEPARTMENT_POSITIONS["Climate Science"], fields.weather.get_top(), color=SCIENCE, stroke_width=1.4, stroke_opacity=0.65),
        )
        central_phrase = VGroup(
            Text("field = value over space / time", font_size=34, color=TEXT, weight=BOLD),
            VGroup(
                MathTex(r"u(x,t)", color=INPUT, font_size=29),
                MathTex(r"p(x,t)", color=OPERATOR, font_size=29),
                MathTex(r"q(t)", color=PURPLE, font_size=29),
            ).arrange(RIGHT, buff=0.42),
        ).arrange(DOWN, buff=0.16).move_to(UP * 2.62)
        not_image_labels = VGroup(
            make_chip("not image → function", color=SCIENCE, font_size=14).next_to(fields.car, DOWN, buff=0.02),
            make_chip("not image → function", color=OPERATOR, font_size=14).next_to(fields.weather, DOWN, buff=0.02),
        )

        # Global 05:56.5-06:07.0 => local 36.5-47.0
        self.play_timed(
            "questions_become_fields",
            36.5,
            47.0,
            FadeOut(questions, shift=DOWN * 0.12),
            FadeOut(question_lines),
            LaggedStart(*[Create(line) for line in field_lines], lag_ratio=0.1),
            LaggedStart(*[FadeIn(field, shift=UP * 0.16) for field in fields], lag_ratio=0.12),
            FadeIn(central_phrase, shift=DOWN * 0.12),
            LaggedStart(*[FadeIn(label, scale=0.94) for label in not_image_labels], lag_ratio=0.18),
        )

        # Global 06:07.0-06:08.2 => local 47.0-48.2
        self.wait_timed("field_identity_pause", 47.0, 48.2)

        rendered = self.make_rendered_weather_frame().move_to(RIGHT * 1.1 + DOWN * 0.18)
        old_world = VGroup(campus, dept_labels, field_lines, fields, central_phrase, science_label, not_image_labels)
        old_world_target = old_world.copy().scale(0.48).to_edge(LEFT, buff=0.24).set_opacity(0.34)
        function_label = Text("but behaves like a function", font_size=31, color=SCIENCE, weight=BOLD)
        function_label.next_to(rendered[0], DOWN, buff=0.2)
        soft_strike = Line(
            rendered[3].get_left() + RIGHT * 2.05,
            rendered[3].get_right() + LEFT * 0.28,
            color=MUTED,
            stroke_width=2.0,
            stroke_opacity=0.8,
        )

        # Global 06:08.2-06:20.5 => local 48.2-60.5
        self.play_timed(
            "rendered_image_trap",
            48.2,
            54.8,
            Transform(old_world, old_world_target),
            FadeIn(rendered, shift=RIGHT * 0.18),
        )
        self.play_timed(
            "image_label_fades_before_reframe",
            54.8,
            57.0,
            Create(soft_strike),
            FadeOut(rendered[3], shift=DOWN * 0.08),
            FadeOut(old_world),
        )
        self.play_timed(
            "function_label_enters_after_image_label",
            57.0,
            60.5,
            FadeIn(function_label, shift=UP * 0.1),
        )

        zoom_grid = self.make_zoomed_grid().move_to(ORIGIN + DOWN * 0.12)
        zoom_title = Text("field operations live beyond pixels", font_size=31, color=TEXT, weight=BOLD)
        zoom_title.to_edge(UP, buff=0.34)
        zoom_field_ghost = VGroup(rendered[0], rendered[1], rendered[2]).copy()
        zoom_field_ghost.scale(1.18).move_to(ORIGIN + DOWN * 0.12).set_opacity(0.18)

        # Global 06:20.5-06:35.0 => local 60.5-75.0
        self.play_timed(
            "clear_image_trap_before_zoom",
            60.5,
            63.0,
            FadeOut(title),
            FadeOut(function_label),
            FadeOut(soft_strike),
            FadeOut(rendered),
        )
        self.play_timed(
            "zoom_into_field_mesh",
            63.0,
            66.8,
            FadeIn(zoom_field_ghost, scale=1.04),
            FadeIn(zoom_title, shift=DOWN * 0.1),
        )
        self.play_timed(
            "reveal_mesh_query_derivative_integral",
            66.8,
            75.0,
            FadeIn(zoom_grid[0]),
            LaggedStart(
                FadeIn(zoom_grid[1]),
                FadeIn(zoom_grid[2]),
                FadeIn(zoom_grid[3], scale=0.8),
                FadeIn(zoom_grid[4], scale=0.8),
                LaggedStart(*[FadeIn(label, shift=UP * 0.06) for label in zoom_grid[5]], lag_ratio=0.08),
                lag_ratio=0.15,
            ),
        )

        two_worlds = self.make_two_worlds()
        final_fields = FieldVisuals().scale(0.46)
        final_fields.arrange_in_grid(rows=2, cols=3, buff=(0.48, 0.24)).move_to(RIGHT * 3.35 + DOWN * 1.25)
        flow_cue = VGroup(
            CurvedArrow(
                start_point=LEFT * 0.48 + DOWN * 1.3,
                end_point=RIGHT * 1.25 + DOWN * 1.3,
                angle=-0.35,
                color=SCIENCE,
                stroke_width=1.8,
            ),
            Text("department fields", font_size=19, color=MUTED).move_to(RIGHT * 0.48 + DOWN * 1.76),
        )
        final_group = VGroup(two_worlds, final_fields, flow_cue)
        final_glow = SurroundingRectangle(
            two_worlds[2][0],
            buff=0.16,
            color=SCIENCE,
            stroke_width=1.6,
            stroke_opacity=0.28,
            corner_radius=0.08,
        )

        # Global 06:35.0-07:20.0 => local 75.0-120.0
        self.play_timed(
            "clear_zoomed_grid_before_two_worlds",
            75.0,
            78.0,
            FadeOut(zoom_grid),
            FadeOut(zoom_title),
            FadeOut(zoom_field_ghost),
        )
        self.play_timed(
            "pull_back_two_worlds",
            78.0,
            86.0,
            FadeIn(two_worlds[0], shift=LEFT * 0.22),
            FadeIn(two_worlds[1]),
            FadeIn(two_worlds[2], shift=RIGHT * 0.22),
        )
        self.play_timed(
            "department_fields_flow_to_function_spaces",
            86.0,
            98.0,
            LaggedStart(*[FadeIn(field, shift=RIGHT * 0.12) for field in final_fields], lag_ratio=0.12),
            FadeIn(flow_cue, shift=RIGHT * 0.12),
            FadeIn(final_glow),
        )
        self.play_timed(
            "function_spaces_final_glow",
            98.0,
            116.0,
            final_glow.animate.set_stroke(opacity=0.48),
            two_worlds[2][0].animate.scale(1.035),
            final_fields.animate.set_opacity(0.9),
            rate_func=there_and_back,
        )
        self.wait_timed("final_hold", 116.0, 119.9)
        # Manim CE 0.20 writes two inclusive terminal frames at 20 fps here.
        # Target 119.9s renders as 120.0s under ffprobe while metadata stays canonical.
        self.pad_to(self.SCENE_DURATION - 0.1)
