"""
Scene 2.1 - Weather: functions on a sphere
Script: docs/full_voice_manim_script.md
Global time: 07:20.0-09:05.0
Local duration: 105.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network, make_chip
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
from src.common.timing import TimedThreeDScene


apply_global_config()


def sphere_point(radius, latitude, longitude):
    return np.array(
        [
            radius * np.cos(latitude) * np.cos(longitude),
            radius * np.cos(latitude) * np.sin(longitude),
            radius * np.sin(latitude),
        ]
    )


def sphere_curve(radius, latitude_fn, longitude_fn, t_values, color, stroke_width=1.0, stroke_opacity=1.0):
    curve = VMobject(color=color, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
    points = [sphere_point(radius, latitude_fn(t), longitude_fn(t)) for t in t_values]
    curve.set_points_smoothly(points)
    return curve


class WeatherSphere(VGroup):
    def __init__(self, radius=1.55, phase=0.0, with_field=True, with_arrows=True, **kwargs):
        surface_opacity = 0.48 if with_field else 0.08
        surface_colors = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR] if with_field else [GRID, SCIENCE]
        surface = Surface(
            lambda u, v: np.array(
                [
                    radius * np.sin(u) * np.cos(v),
                    radius * np.sin(u) * np.sin(v),
                    radius * np.cos(u),
                ]
            ),
            u_range=[0.02, PI - 0.02],
            v_range=[0, TAU],
            resolution=(4, 8),
            checkerboard_colors=surface_colors,
            fill_opacity=surface_opacity,
            stroke_color=GRID,
            stroke_width=0.45,
            stroke_opacity=0.42,
        )
        rim = Circle(radius=radius, color=SCIENCE, stroke_width=1.4, stroke_opacity=0.45)
        rim.rotate(PI / 2, axis=RIGHT)

        latitudes = VGroup()
        for lat in np.linspace(-0.82, 0.82, 4):
            curve = sphere_curve(
                radius * 1.006,
                lambda t, lat=lat: lat,
                lambda t: t,
                np.linspace(0, TAU, 28),
                color=GRID,
                stroke_width=0.75,
                stroke_opacity=0.58,
            )
            latitudes.add(curve)

        longitudes = VGroup()
        for lon in np.linspace(0, PI, 4, endpoint=False):
            curve = sphere_curve(
                radius * 1.007,
                lambda t: t,
                lambda t, lon=lon: lon,
                np.linspace(-PI / 2, PI / 2, 18),
                color=GRID,
                stroke_width=0.65,
                stroke_opacity=0.48,
            )
            longitudes.add(curve)

        bands = VGroup()
        if with_field:
            for i, lat in enumerate(np.linspace(-0.64, 0.64, 4)):
                color = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR][i]
                wiggle = 0.06 * np.sin(phase + i)
                band = sphere_curve(
                    radius * 1.018,
                    lambda t, lat=lat, wiggle=wiggle: lat + wiggle * np.sin(2 * t + phase),
                    lambda t: t,
                    np.linspace(-2.75, 0.85, 18),
                    color=color,
                    stroke_width=5.0,
                    stroke_opacity=0.58,
                )
                bands.add(band)

        arrows = VGroup()
        if with_arrows:
            wind_specs = [
                (-0.78, -1.05, 0.36),
                (-0.52, -0.35, 0.28),
                (-0.24, -1.32, 0.32),
                (0.02, -0.64, 0.26),
                (0.24, -1.08, 0.3),
                (0.46, -0.28, 0.25),
                (0.66, -1.46, 0.23),
            ]
            for lat, lon, length in wind_specs:
                start = sphere_point(radius * 1.08, lat, lon)
                end = sphere_point(radius * 1.08, lat + 0.02 * np.cos(lon), lon + length)
                arrows.add(
                    Line3D(
                        start=start,
                        end=end,
                        color=TEXT,
                        thickness=0.018,
                    ).set_opacity(0.75)
                )

        super().__init__(surface, latitudes, longitudes, rim, bands, arrows, **kwargs)
        self.surface = surface
        self.grid = VGroup(latitudes, longitudes, rim)
        self.bands = bands
        self.wind_arrows = arrows


class PixelGrid(VGroup):
    def __init__(self, rows=8, cols=13, **kwargs):
        pixels = VGroup()
        palette = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, WARNING, PURPLE, OUTPUT]
        for row in range(rows):
            for col in range(cols):
                intensity = 0.38 + 0.42 * (0.5 + 0.5 * np.sin(row * 0.9 + col * 0.55))
                pixel = Square(
                    side_length=0.22,
                    stroke_color=BG,
                    stroke_width=0.7,
                    fill_color=palette[(row + 2 * col) % len(palette)],
                    fill_opacity=intensity,
                )
                pixels.add(pixel)
        pixels.arrange_in_grid(rows=rows, cols=cols, buff=0.018)
        frame = RoundedRectangle(
            width=pixels.width + 0.18,
            height=pixels.height + 0.18,
            corner_radius=0.06,
            stroke_color=WARNING,
            stroke_width=1.4,
            fill_color="#1A1020",
            fill_opacity=0.18,
        ).move_to(pixels)
        super().__init__(frame, pixels, **kwargs)


class ForecastOperator(VGroup):
    def __init__(self, **kwargs):
        arrow = Arrow(
            LEFT * 1.2,
            RIGHT * 1.2,
            buff=0.0,
            color=OPERATOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.16,
        )
        glow = Arrow(
            LEFT * 1.2,
            RIGHT * 1.2,
            buff=0.0,
            color=OPERATOR,
            stroke_width=14,
            stroke_opacity=0.16,
            max_tip_length_to_length_ratio=0.16,
        )
        label = MathTex(r"\mathcal{G}: a_t \mapsto a_{t+1}", color=OPERATOR, font_size=34)
        label.next_to(arrow, UP, buff=0.14)
        super().__init__(glow, arrow, label, **kwargs)


class Scene0201WeatherFunctionsOnSphere(TimedThreeDScene):
    SCRIPT_ID = "2.1"
    SCRIPT_TITLE = "Weather: functions on a sphere"
    SCRIPT_START = 440.0
    SCRIPT_END = 545.0
    SCENE_DURATION = 105.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_weather_sphere(self, radius=1.55, phase=0.0, with_field=True, with_arrows=True):
        return WeatherSphere(radius=radius, phase=phase, with_field=with_field, with_arrows=with_arrows)

    def make_variable_list(self):
        variables = [
            ("temperature", INPUT),
            ("wind velocity", TEXT),
            ("humidity", SCIENCE),
            ("pressure", NVIDIA_GREEN),
            ("precipitation", OUTPUT),
            ("vorticity", PURPLE),
        ]
        title = Text("variables at each point", font_size=21, color=MUTED)
        chips = VGroup(*[make_chip(label, color=color, font_size=15, height=0.34) for label, color in variables])
        chips.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        return VGroup(title, chips).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

    def make_forecast_operator(self):
        return ForecastOperator()

    def make_pixel_grid(self):
        return PixelGrid()

    def make_physics_glyphs(self):
        glyphs = VGroup(
            MathTex(r"\nabla", color=INPUT, font_size=46),
            MathTex(r"\operatorname{div}", color=SCIENCE, font_size=36),
            MathTex(r"\int", color=OPERATOR, font_size=50),
        ).arrange(RIGHT, buff=0.46)
        labels = VGroup(
            Text("gradient", font_size=20, color=INPUT),
            Text("divergence", font_size=20, color=SCIENCE),
            Text("energy", font_size=20, color=OPERATOR),
            Text("flux", font_size=20, color=OUTPUT),
        ).arrange(RIGHT, buff=0.28)
        return VGroup(glyphs, labels).arrange(DOWN, buff=0.18)

    def fixed(self, *mobjects):
        self.add_fixed_in_frame_mobjects(*mobjects)
        self.remove(*mobjects)
        return mobjects[0] if len(mobjects) == 1 else mobjects

    def construct(self):
        np.random.seed(21)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-38 * DEGREES, zoom=1.05)
        self.begin_ambient_camera_rotation(rate=0.025)

        background = make_background_network(seed=21, n=32, dot_opacity=0.16, line_opacity=0.12)
        background.set_z_index(-10)
        title = Text("Weather / Climate", font_size=42, color=TEXT, weight=BOLD)
        title.set_color_by_gradient(TEXT, NVIDIA_GREEN)
        title.to_corner(UL, buff=0.32)
        domain_label = make_chip("Domain ≈ sphere", color=SCIENCE, font_size=19, height=0.42)
        domain_label.to_edge(DOWN, buff=0.48).shift(LEFT * 3.75)
        self.add_fixed_in_frame_mobjects(background, title, domain_label)
        self.remove(background, title, domain_label)

        wire_sphere = self.make_weather_sphere(with_field=False, with_arrows=False)

        # Global 07:20.0-07:30.5 => local 0.0-10.5
        self.play_timed(
            "weather_climate_domain_sphere",
            0.0,
            10.5,
            FadeIn(background),
            Write(title),
            FadeIn(wire_sphere, scale=0.96),
            FadeIn(domain_label, shift=UP * 0.1),
        )

        field_sphere = self.make_weather_sphere(with_field=True, with_arrows=True)
        variable_list = self.make_variable_list()
        variable_list.to_edge(RIGHT, buff=0.46).shift(UP * 0.18)
        self.fixed(variable_list)

        # Global 07:30.5-07:42.5 => local 10.5-22.5
        self.play_timed(
            "scalar_field_and_weather_variables",
            10.5,
            22.5,
            FadeOut(wire_sphere, scale=0.98),
            FadeIn(field_sphere, scale=0.98),
            LaggedStart(
                *[FadeIn(item, shift=LEFT * 0.08) for item in variable_list],
                lag_ratio=0.12,
            ),
        )

        formula = MathTex(r"a_t : S^2 \to \mathbb{R}^d", color=TEXT, font_size=48)
        formula.to_edge(DOWN, buff=0.75).shift(RIGHT * 1.05)
        vector_label = make_chip("vector-valued function", color=NVIDIA_GREEN, font_size=18, height=0.42)
        vector_label.next_to(formula, DOWN, buff=0.15)
        self.fixed(formula, vector_label)

        # Global 07:42.5-07:54.0 => local 22.5-34.0
        self.play_timed(
            "state_is_vector_valued_function",
            22.5,
            34.0,
            field_sphere.animate.scale(1.06),
            variable_list.animate.set_opacity(0.66),
            FadeIn(formula, shift=UP * 0.12),
            FadeIn(vector_label, shift=UP * 0.08),
        )

        today_sphere = self.make_weather_sphere(radius=1.05, phase=0.0, with_field=True, with_arrows=True).shift(LEFT * 2.85)
        tomorrow_sphere = self.make_weather_sphere(radius=1.05, phase=1.4, with_field=True, with_arrows=True).shift(RIGHT * 2.85)
        today_label = make_chip("today", color=INPUT, font_size=19, height=0.4).move_to(LEFT * 3.0 + DOWN * 2.82)
        tomorrow_label = make_chip("tomorrow", color=OUTPUT, font_size=19, height=0.4).move_to(RIGHT * 3.0 + DOWN * 2.82)
        operator_arrow = self.make_forecast_operator().move_to(UP * 0.08)
        self.fixed(today_label, tomorrow_label, operator_arrow)

        # Global 07:54.0-07:57.0 => local 34.0-37.0
        self.play_timed(
            "clear_single_state_before_forecast",
            34.0,
            37.0,
            FadeOut(field_sphere, scale=0.92),
            FadeOut(domain_label),
            FadeOut(formula, shift=DOWN * 0.1),
            FadeOut(vector_label, shift=DOWN * 0.08),
            FadeOut(variable_list, shift=RIGHT * 0.08),
        )
        # Global 07:57.0-08:06.5 => local 37.0-46.5
        self.play_timed(
            "forecast_function_to_function_map",
            37.0,
            46.5,
            FadeIn(today_sphere, shift=LEFT * 0.2),
            FadeIn(tomorrow_sphere, shift=RIGHT * 0.2),
            FadeIn(today_label, shift=UP * 0.08),
            FadeIn(tomorrow_label, shift=UP * 0.08),
            FadeIn(operator_arrow, scale=0.95),
        )

        # Global 08:06.5-08:07.5 => local 46.5-47.5
        self.wait_timed("forecast_operator_pause", 46.5, 47.5)

        physics_glyphs = self.make_physics_glyphs()
        physics_glyphs.to_edge(DOWN, buff=0.46)
        expert_need = Text("physics checks need field calculus", font_size=25, color=TEXT, weight=BOLD)
        expert_need.to_edge(UP, buff=0.42).shift(RIGHT * 1.95)
        tangent_arrows = self.make_weather_sphere(radius=1.12, phase=2.1, with_field=False, with_arrows=True)
        tangent_arrows.shift(LEFT * 2.85)
        self.fixed(physics_glyphs, expert_need)

        # Global 08:07.5-08:25.0 => local 47.5-65.0
        self.play_timed(
            "calculus_on_weather_fields",
            47.5,
            65.0,
            FadeIn(expert_need, shift=DOWN * 0.08),
            FadeIn(physics_glyphs, shift=UP * 0.1),
            FadeIn(tangent_arrows.wind_arrows),
            today_sphere.animate.scale(1.08),
            tomorrow_sphere.animate.set_opacity(0.78),
            operator_arrow.animate.set_opacity(0.76),
        )

        pixel_grid = self.make_pixel_grid()
        pixel_grid.move_to(RIGHT * 2.9 + DOWN * 0.08)
        warning = VGroup(
            RoundedRectangle(
                width=3.8,
                height=0.62,
                corner_radius=0.07,
                stroke_color=WARNING,
                stroke_width=2.2,
                fill_color="#351020",
                fill_opacity=0.25,
            ),
            Text("discrete image only", font_size=23, color=WARNING, weight=BOLD),
        )
        warning[1].move_to(warning[0])
        warning.next_to(pixel_grid, DOWN, buff=0.2)
        output_label = Text("Output must remain a function", font_size=34, color=OUTPUT, weight=BOLD)
        output_label.to_edge(DOWN, buff=0.52)
        final_formula = MathTex(r"\mathcal{G}: a_t \mapsto a_{t+1}", color=OPERATOR, font_size=38)
        final_formula.to_edge(UP, buff=0.46).shift(RIGHT * 2.55)
        self.fixed(pixel_grid, warning, output_label, final_formula)

        final_function_sphere = self.make_weather_sphere(radius=1.15, phase=2.6, with_field=True, with_arrows=True)
        final_function_sphere.shift(RIGHT * 2.85)

        # Global 08:25.0-09:05.0 => local 65.0-105.0
        self.play_timed(
            "flatten_function_to_pixel_warning",
            65.0,
            76.0,
            FadeOut(expert_need, shift=UP * 0.08),
            FadeOut(physics_glyphs, shift=DOWN * 0.08),
            FadeOut(tangent_arrows.wind_arrows),
            FadeOut(tomorrow_sphere, scale=0.92),
            FadeIn(pixel_grid, shift=LEFT * 0.18),
            FadeIn(warning, shift=UP * 0.08),
            today_sphere.animate.shift(LEFT * 0.15).set_opacity(0.68),
        )
        self.play_timed(
            "restore_function_semantics",
            76.0,
            89.0,
            FadeOut(pixel_grid, shift=RIGHT * 0.16),
            FadeOut(warning, shift=DOWN * 0.08),
            FadeIn(final_function_sphere, shift=RIGHT * 0.18),
            FadeIn(output_label, shift=UP * 0.08),
            FadeIn(final_formula, shift=DOWN * 0.08),
            operator_arrow.animate.set_opacity(1.0),
            today_label.animate.set_opacity(1.0),
            tomorrow_label.animate.set_opacity(1.0),
        )
        self.play_timed(
            "function_output_final_hold_motion",
            89.0,
            102.0,
            output_label.animate.set_color_by_gradient(TEXT, OUTPUT),
            final_function_sphere.animate.scale(1.04),
            today_sphere.animate.set_opacity(0.9),
            rate_func=there_and_back,
        )
        self.wait_timed("final_composition_hold_for_scene_2_2", 102.0, 104.9)
        # Manim CE writes terminal frames inclusively at 20 fps for this project.
        self.pad_to(self.SCENE_DURATION - 0.1)
