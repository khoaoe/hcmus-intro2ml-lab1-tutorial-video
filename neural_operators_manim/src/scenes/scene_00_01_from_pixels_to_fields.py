"""
Scene 0.1 - From pixels to fields
Script: ../docs/full_voice_manim_script.md
Global time: 00:00.0-00:42.0
Local duration: 42.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import (
    make_mesh_overlay,
    smooth_path,
)
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
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
    PURPLE,
    SCIENCE,
    TEXT,
    WARNING,
)
from src.common.timing import TimedScene


apply_global_config()


class PixelGrid(VGroup):
    """Finite-dimensional pixel block with deterministic color structure."""

    def __init__(self, rows=7, cols=9, side=0.22, **kwargs):
        super().__init__(**kwargs)
        palette = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, WARNING, PURPLE, OUTPUT]
        squares = VGroup()
        for row in range(rows):
            for col in range(cols):
                phase = 0.55 * row + 0.82 * col
                opacity = 0.28 + 0.55 * (0.5 + 0.5 * np.sin(phase))
                square = Square(side_length=side)
                square.set_stroke(BG, width=0.75, opacity=0.9)
                square.set_fill(palette[(row + 2 * col) % len(palette)], opacity=opacity)
                square.move_to([col * side, -row * side, 0])
                squares.add(square)
        squares.center()

        frame = RoundedRectangle(
            width=squares.width + 0.24,
            height=squares.height + 0.24,
            corner_radius=0.08,
            stroke_color=INPUT,
            stroke_width=1.4,
            fill_color="#0B1830",
            fill_opacity=0.38,
        ).move_to(squares)
        self.squares = squares
        self.add(frame, squares)


class SphereField(VGroup):
    """2D sphere-style continuous field glyph for the cold open."""

    def __init__(self, radius=1.08, **kwargs):
        super().__init__(**kwargs)
        sphere = Circle(radius=radius, stroke_color=SCIENCE, stroke_width=1.7)
        sphere.set_fill("#092F3F", opacity=0.62)

        latitudes = VGroup()
        for y in np.linspace(-0.62, 0.62, 5):
            width = 2 * radius * np.sqrt(max(1 - (y / radius) ** 2, 0))
            lat = Ellipse(
                width=width,
                height=0.16,
                stroke_color=GRID,
                stroke_width=0.9,
                stroke_opacity=0.72,
            ).shift(UP * y)
            latitudes.add(lat)

        longitudes = VGroup()
        for scale in (0.28, 0.52, 0.76):
            longitudes.add(
                Ellipse(
                    width=2 * radius * scale,
                    height=2 * radius,
                    stroke_color=GRID,
                    stroke_width=0.85,
                    stroke_opacity=0.62,
                )
            )

        bands = VGroup()
        for i, y in enumerate(np.linspace(-0.46, 0.46, 5)):
            x_extent = radius * np.sqrt(max(1 - (y / radius) ** 2, 0)) * 0.86
            color = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, PURPLE][i]
            bands.add(
                smooth_path(
                    [
                        [-x_extent, y - 0.05 * np.sin(i), 0],
                        [-0.35 * x_extent, y + 0.10 * np.cos(i), 0],
                        [0.28 * x_extent, y - 0.08 * np.sin(i + 1), 0],
                        [x_extent, y + 0.04 * np.cos(i + 2), 0],
                    ],
                    color=color,
                    stroke_width=4.0,
                    stroke_opacity=0.52,
                )
            )

        wind = VGroup()
        for x, y, dx, dy in [(-0.54, 0.34, 0.42, 0.08), (-0.28, -0.12, 0.48, 0.12), (0.1, 0.18, 0.36, -0.10)]:
            wind.add(
                Arrow(
                    [x, y, 0],
                    [x + dx, y + dy, 0],
                    buff=0,
                    color=TEXT,
                    stroke_width=1.4,
                    max_tip_length_to_length_ratio=0.2,
                ).set_opacity(0.78)
            )

        self.add(sphere, bands, latitudes, longitudes, wind)


class ContinuousSurface(VGroup):
    """Small continuous field surface, shown as contour mesh plus smooth graph."""

    def __init__(self, width=2.35, height=1.25, **kwargs):
        super().__init__(**kwargs)
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=OUTPUT,
            stroke_width=1.35,
            fill_color="#08251F",
            fill_opacity=0.38,
        )
        mesh = make_mesh_overlay(width=width * 0.9, height=height * 0.7, nx=7, ny=4, color=TEXT)
        mesh.set_opacity(0.38)
        mesh.move_to(frame)

        contours = VGroup()
        for j, offset in enumerate(np.linspace(-0.34, 0.34, 4)):
            contours.add(
                smooth_path(
                    [
                        [-width * 0.38, offset - 0.08, 0],
                        [-width * 0.18, offset + 0.11 * np.sin(j + 1), 0],
                        [width * 0.05, offset + 0.06 * np.cos(j), 0],
                        [width * 0.33, offset + 0.10 * np.sin(j + 0.4), 0],
                    ],
                    color=[SCIENCE, NVIDIA_GREEN, OPERATOR, PURPLE][j],
                    stroke_width=2.0,
                    stroke_opacity=0.82,
                )
            )

        dots = VGroup(
            Dot([-0.72, -0.16, 0], radius=0.035, color=OPERATOR),
            Dot([0.12, 0.22, 0], radius=0.035, color=OUTPUT),
            Dot([0.66, -0.02, 0], radius=0.035, color=SCIENCE),
        )
        self.add(frame, mesh, contours, dots)


class Scene0001FromPixelsToFields(TimedScene):
    SCRIPT_ID = "0.1"
    SCRIPT_TITLE = "From pixels to fields"
    SCRIPT_START = 0.0
    SCRIPT_END = 42.0
    SCENE_DURATION = 42.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_pixel_grid(self):
        return PixelGrid()

    def make_sphere_field(self):
        return SphereField()

    def make_continuous_surface(self):
        return ContinuousSurface()

    def make_transition_arrow(self):
        arrow = Arrow(
            LEFT * 0.92,
            RIGHT * 0.92,
            buff=0,
            color=OPERATOR,
            stroke_width=5.2,
            max_tip_length_to_length_ratio=0.14,
        )
        glow = Arrow(
            LEFT * 0.92,
            RIGHT * 0.92,
            buff=0,
            color=OPERATOR,
            stroke_width=13.0,
            stroke_opacity=0.13,
            max_tip_length_to_length_ratio=0.14,
        )
        return VGroup(glow, arrow)

    def make_vector_formula(self):
        return MathTex(r"f: \mathbb{R}^n \to \mathbb{R}^m", color=TEXT, font_size=38)

    def make_operator_formula(self):
        return MathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}", color=TEXT, font_size=40)

    def make_vector_world(self):
        grid = self.make_pixel_grid()
        tokens = VGroup()
        for i, width in enumerate([0.88, 0.64, 0.78, 0.52]):
            token = RoundedRectangle(
                width=width,
                height=0.14,
                corner_radius=0.04,
                stroke_width=0,
                fill_color=[PURPLE, INPUT, OUTPUT, OPERATOR][i],
                fill_opacity=0.72,
            )
            tokens.add(token)
        tokens.arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        tokens.next_to(grid, RIGHT, buff=0.36)

        label = SafeText(
            "Finite-dimensional data",
            max_width=3.7,
            max_height=0.38,
            font_size=24,
            color=INPUT,
            weight=BOLD,
        )
        label.next_to(VGroup(grid, tokens), UP, buff=0.28)
        return VGroup(label, grid, tokens)

    def make_function_world(self):
        sphere = self.make_sphere_field()
        surface = self.make_continuous_surface().scale(0.78)
        surface.next_to(sphere, DOWN, buff=0.3)
        label = SafeText(
            "Function-valued data",
            max_width=3.7,
            max_height=0.38,
            font_size=24,
            color=OUTPUT,
            weight=BOLD,
        )
        label.next_to(sphere, UP, buff=0.28)
        return VGroup(label, sphere, surface)

    def make_example_glyphs(self):
        def boxed_field(width, height, stroke_color, fill_color):
            return RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.07,
                stroke_color=stroke_color,
                stroke_width=1.4,
                fill_color=fill_color,
                fill_opacity=0.48,
            )

        def temperature_glyph():
            box = boxed_field(1.18, 0.82, SCIENCE, "#092F3F")
            bands = VGroup()
            for j, y in enumerate(np.linspace(-0.25, 0.25, 4)):
                bands.add(
                    Line(
                        [-0.42, y, 0],
                        [0.42, y + 0.05 * np.sin(j + 1), 0],
                        color=[INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR][j],
                        stroke_width=2.0,
                        stroke_opacity=0.78,
                    )
                )
            arrows = VGroup(
                Arrow([-0.38, 0.21, 0], [0.16, 0.31, 0], buff=0, color=TEXT, stroke_width=1.1, max_tip_length_to_length_ratio=0.18),
                Arrow([-0.28, -0.2, 0], [0.28, -0.09, 0], buff=0, color=TEXT, stroke_width=1.1, max_tip_length_to_length_ratio=0.18),
            )
            return VGroup(box, bands, arrows)

        def velocity_glyph():
            box = boxed_field(1.18, 0.82, OPERATOR, "#211B32")
            layers = VGroup()
            for j, y in enumerate(np.linspace(-0.24, 0.24, 4)):
                layers.add(
                    smooth_path(
                        [
                            [-0.48, y, 0],
                            [-0.2, y + 0.04 * np.cos(j), 0],
                            [0.14, y - 0.05 * np.sin(j + 1), 0],
                            [0.48, y + 0.03 * np.cos(j + 2), 0],
                        ],
                        color=GRID,
                        stroke_width=1.0,
                        stroke_opacity=0.7,
                    )
                )
            waves = VGroup()
            source = Dot([-0.18, -0.08, 0], radius=0.035, color=WARNING)
            for radius in (0.14, 0.27, 0.40):
                arc = Arc(
                    radius=radius,
                    start_angle=0.18,
                    angle=1.72,
                    color=OPERATOR,
                    stroke_width=1.45,
                    stroke_opacity=0.78,
                )
                arc.shift(source.get_center())
                waves.add(arc)
            return VGroup(box, layers, source, waves)

        def airflow_glyph():
            box = boxed_field(1.28, 0.82, INPUT, "#09243A")
            streamlines = VGroup()
            for j, y in enumerate(np.linspace(-0.24, 0.24, 4)):
                streamlines.add(
                    smooth_path(
                        [
                            [-0.52, y, 0],
                            [-0.18, y + 0.04, 0],
                            [0.18, y + 0.06 * np.cos(j), 0],
                            [0.52, y - 0.03, 0],
                        ],
                        color=[SCIENCE, INPUT, NVIDIA_GREEN, OPERATOR][j],
                        stroke_width=1.45,
                        stroke_opacity=0.78,
                    )
                )
            car = VGroup(
                Polygon(
                    [-0.35, -0.08, 0],
                    [-0.22, 0.08, 0],
                    [0.22, 0.1, 0],
                    [0.36, -0.06, 0],
                    [0.30, -0.14, 0],
                    [-0.35, -0.14, 0],
                    color=TEXT,
                    fill_color=CARD_BG,
                    fill_opacity=0.9,
                    stroke_width=1.1,
                ),
                Dot([-0.18, -0.14, 0], radius=0.045, color=MUTED),
                Dot([0.22, -0.14, 0], radius=0.045, color=MUTED),
            )
            return VGroup(box, streamlines, car)

        glyphs = VGroup(temperature_glyph(), velocity_glyph(), airflow_glyph()).arrange(RIGHT, buff=0.42)

        chips = VGroup(
            Chip("temperature field", max_width=2.08, height=0.44, stroke_color=SCIENCE, font_size=15),
            Chip("velocity field", max_width=1.72, height=0.44, stroke_color=NVIDIA_GREEN, font_size=15),
            Chip("airflow", max_width=1.20, height=0.44, stroke_color=INPUT, font_size=15),
        ).arrange(RIGHT, buff=0.22)
        chips.next_to(glyphs, DOWN, buff=0.14)
        return VGroup(glyphs, chips)

    def construct(self):
        background = make_background_network(seed=101, n=50, dot_opacity=0.13, line_opacity=0.11)
        self.add(background)

        vector_world = self.make_vector_world().scale(0.92).move_to(LEFT * 3.85 + UP * 0.12)
        function_world = self.make_function_world().scale(0.92).move_to(RIGHT * 3.85 + UP * 0.05)
        transition = self.make_transition_arrow().move_to(ORIGIN + UP * 0.05)

        vector_world.set_opacity(0.0)
        function_world.set_opacity(0.0)
        transition.set_opacity(0.0)

        # Global 00:00.0-00:05.5 => local 0.0-5.5
        self.play_timed(
            "opening_question_ghost_worlds",
            0.0,
            5.5,
            FadeIn(vector_world, shift=0.16 * RIGHT),
            FadeIn(function_world, shift=0.16 * LEFT),
            FadeIn(transition),
            background.animate.set_opacity(0.55),
        )
        vector_world.set_opacity(0.34)
        function_world.set_opacity(0.34)
        transition.set_opacity(0.28)

        # Global 00:05.5-00:06.3 => local 5.5-6.3
        self.wait_timed("real_pause_after_question", 5.5, 6.3)

        not_image = SafeText(
            "not just images",
            max_width=2.2,
            max_height=0.38,
            font_size=23,
            color=WARNING,
            weight=BOLD,
        )
        not_token = SafeText(
            "not just token sequences",
            max_width=3.0,
            max_height=0.38,
            font_size=23,
            color=WARNING,
            weight=BOLD,
        )
        contrast = VGroup(not_image, not_token).arrange(DOWN, buff=0.14)
        contrast.next_to(vector_world, DOWN, buff=0.42)

        # Global 00:06.3-00:13.5 => local 6.3-13.5
        self.play_timed(
            "not_only_images_or_tokens",
            6.3,
            13.5,
            vector_world.animate.set_opacity(1.0),
            function_world.animate.set_opacity(0.42),
            transition.animate.set_opacity(0.36),
            FadeIn(contrast, shift=0.18 * UP),
        )

        # Global 00:13.5-00:14.2 => local 13.5-14.2
        self.wait_timed("pause_before_function_examples", 13.5, 14.2)

        examples = self.make_example_glyphs().move_to(DOWN * 2.62)
        function_word = SafeText(
            "It is a function.",
            max_width=3.2,
            max_height=0.52,
            font_size=32,
            color=OUTPUT,
            weight=BOLD,
        )
        function_word.next_to(function_world, DOWN, buff=0.36)

        # Global 00:14.2-00:23.0 => local 14.2-23.0
        self.play_timed(
            "reveal_function_valued_examples",
            14.2,
            18.0,
            function_world.animate.set_opacity(1.0),
            transition.animate.set_opacity(0.75),
            FadeIn(function_word, shift=0.2 * UP),
            contrast.animate.set_opacity(0.38),
        )
        self.play_timed(
            "temperature_velocity_airflow_glyphs",
            18.0,
            23.0,
            FadeOut(function_word, shift=0.12 * DOWN),
            FadeOut(contrast, shift=0.12 * DOWN),
            LaggedStart(*[FadeIn(item, shift=0.15 * UP) for item in examples], lag_ratio=0.16),
        )

        # Global 00:23.0-00:24.0 => local 23.0-24.0
        self.wait_timed("pause_before_title", 23.0, 24.0)

        title_top = SafeText(
            "Machine Learning on Function Spaces",
            max_width=11.0,
            max_height=0.72,
            font_size=46,
            color=TEXT,
            weight=BOLD,
        )
        title_bottom = SafeText(
            "Neural Operators",
            max_width=7.0,
            max_height=0.72,
            font_size=48,
            color=NVIDIA_GREEN,
            weight=BOLD,
        )
        title = VGroup(title_top, title_bottom).arrange(DOWN, buff=0.16).move_to(UP * 0.96)
        title_backplate = RoundedRectangle(
            width=12.1,
            height=1.85,
            corner_radius=0.12,
            stroke_color=NVIDIA_GREEN,
            stroke_width=1.1,
            stroke_opacity=0.28,
            fill_color=CARD_BG,
            fill_opacity=0.68,
        ).move_to(title)
        title_lockup = VGroup(title_backplate, title)

        # Global 00:24.0-00:33.5 => local 24.0-33.5
        self.play_timed(
            "clear_stage_for_title",
            24.0,
            25.8,
            FadeOut(examples, shift=0.16 * DOWN),
            FadeOut(vector_world[0], shift=0.08 * DOWN),
            FadeOut(function_world[0], shift=0.08 * DOWN),
            VGroup(vector_world[1], vector_world[2]).animate.scale(0.82).move_to(LEFT * 4.6 + DOWN * 1.55).set_opacity(0.32),
            VGroup(function_world[1], function_world[2]).animate.scale(0.82).move_to(RIGHT * 4.6 + DOWN * 1.52).set_opacity(0.32),
            transition.animate.move_to(DOWN * 1.48).set_opacity(0.28),
        )
        self.play_timed(
            "form_tutorial_title",
            25.8,
            29.0,
            FadeIn(title_lockup, shift=0.22 * UP),
        )
        self.play_timed(
            "title_hold",
            29.0,
            33.5,
            title_backplate.animate.set_stroke(opacity=0.42),
            background.animate.set_opacity(0.36),
        )

        vector_formula = self.make_vector_formula().move_to(LEFT * 2.45 + DOWN * 0.6)
        operator_formula = self.make_operator_formula().move_to(RIGHT * 2.45 + DOWN * 0.6)
        vector_label = Chip(
            "vector to vector",
            max_width=1.72,
            height=0.36,
            stroke_color=INPUT,
            text_color=TEXT,
            font_size=16,
        )
        function_label = Chip(
            "function to function",
            max_width=2.08,
            height=0.36,
            stroke_color=OUTPUT,
            text_color=TEXT,
            font_size=16,
        )
        vector_label.next_to(vector_formula, DOWN, buff=0.16)
        function_label.next_to(operator_formula, DOWN, buff=0.16)
        formula_arrow = self.make_transition_arrow().scale(0.7)
        formula_arrow.move_to(DOWN * 0.6)
        formula_lockup = VGroup(vector_formula, operator_formula, vector_label, function_label, formula_arrow)

        # Global 00:33.5-00:42.0 => local 33.5-42.0
        self.play_timed(
            "vector_formula_appears",
            33.5,
            36.3,
            FadeIn(vector_formula, shift=0.12 * UP),
            FadeIn(vector_label, shift=0.08 * UP),
            title_lockup.animate.shift(UP * 0.36).scale(0.86),
        )
        self.play_timed(
            "morph_to_operator_formula",
            36.3,
            39.0,
            FadeIn(formula_arrow),
            TransformFromCopy(vector_formula, operator_formula),
            FadeIn(function_label, shift=0.08 * UP),
        )
        self.play_timed(
            "final_lockup_hold",
            39.0,
            42.0,
            formula_arrow.animate.set_opacity(0.86),
            formula_lockup.animate.set_opacity(1.0),
            title_backplate.animate.set_stroke(opacity=0.56),
        )

        self.pad_to(self.SCENE_DURATION)
