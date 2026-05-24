"""
Scene 2.2 - Seismology: functions inside Earth
Script: docs/full_voice_manim_script.md
Global time: 09:05.0-10:45.0
Local duration: 100.0s
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


def plane_surface(x_range, y_range, z, color, opacity=0.18, stroke_opacity=0.4):
    """Horizontal 3D sheet used as a conceptual geological layer."""
    surface = Surface(
        lambda u, v: np.array([u, v, z]),
        u_range=x_range,
        v_range=y_range,
        resolution=(2, 2),
        checkerboard_colors=[color, color],
        fill_opacity=opacity,
        stroke_color=GRID,
        stroke_width=0.55,
        stroke_opacity=stroke_opacity,
    )
    return surface


def make_wave_sphere(center, radius, color=OPERATOR, opacity=0.08):
    """Transparent expanding wavefront. This is conceptual, not a physical solver."""
    wave = Sphere(
        center=center,
        radius=radius,
        resolution=(8, 16),
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=0.55,
        stroke_opacity=0.22,
    )
    return wave


class EarthVelocityVolume(VGroup):
    """Layered subsurface volume representing a velocity field c(x)."""

    def __init__(self, width=4.45, depth=2.55, height=2.35, highlighted=False, **kwargs):
        frame = Prism(dimensions=[width, depth, height])
        frame.set_fill(CARD_BG, opacity=0.06 if not highlighted else 0.10)
        frame.set_stroke(SCIENCE if highlighted else GRID, width=1.15, opacity=0.72)

        z_values = np.linspace(-height / 2 + 0.35, height / 2 - 0.35, 5)
        layer_colors = [PURPLE, INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR]
        layers = VGroup()
        for idx, z in enumerate(z_values):
            sheet = plane_surface(
                [-width / 2, width / 2],
                [-depth / 2, depth / 2],
                z,
                color=layer_colors[idx % len(layer_colors)],
                opacity=0.10 + 0.03 * idx,
                stroke_opacity=0.34,
            )
            layers.add(sheet)

        velocity_markers = VGroup()
        rng = np.random.default_rng(22)
        for idx in range(18):
            x = rng.uniform(-width / 2 + 0.3, width / 2 - 0.3)
            y = rng.uniform(-depth / 2 + 0.25, depth / 2 - 0.25)
            z = rng.uniform(-height / 2 + 0.25, height / 2 - 0.25)
            color = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, PURPLE][idx % 5]
            dot = Dot3D(point=np.array([x, y, z]), radius=0.035, color=color)
            dot.set_opacity(0.62 if not highlighted else 0.86)
            velocity_markers.add(dot)

        super().__init__(frame, layers, velocity_markers, **kwargs)
        self.frame = frame
        self.layers = layers
        self.velocity_markers = velocity_markers


class SurfaceSensorArray(VGroup):
    """Sensors placed on the surface of the Earth block."""

    def __init__(self, z=1.33, **kwargs):
        sensors = VGroup()
        positions = [
            (-1.85, -0.96, z),
            (-1.12, -1.02, z),
            (-0.38, -0.98, z),
            (0.36, -1.02, z),
            (1.10, -0.96, z),
            (1.82, -1.02, z),
        ]
        for idx, pos in enumerate(positions):
            color = OUTPUT if idx % 2 == 0 else TEXT
            sensor = Dot3D(point=np.array(pos), radius=0.055, color=color)
            stem = Line3D(
                start=np.array([pos[0], pos[1], z - 0.16]),
                end=np.array(pos),
                color=color,
                thickness=0.014,
            )
            sensors.add(stem, sensor)
        super().__init__(sensors, **kwargs)


class WaveformPanel(VGroup):
    """Small fixed-in-frame panel showing surface observations as functions of time."""

    def __init__(self, title="surface observations", **kwargs):
        panel = RoundedRectangle(
            width=4.6,
            height=2.2,
            corner_radius=0.12,
            stroke_color=OUTPUT,
            stroke_width=1.35,
            fill_color=CARD_BG,
            fill_opacity=0.78,
        )
        title_mob = Text(title, font_size=22, color=OUTPUT, weight=BOLD)
        title_mob.next_to(panel, UP, buff=0.14)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.2, 1.2, 1],
            x_length=3.75,
            y_length=1.35,
            tips=False,
            axis_config={"stroke_color": GRID, "stroke_width": 1.05},
        )
        curves = VGroup()
        for idx, color in enumerate([INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR]):
            phase = idx * 0.52
            curve = axes.plot(
                lambda x, phase=phase: 0.55 * np.sin(2.2 * x + phase) * np.exp(-0.20 * x),
                color=color,
                stroke_width=2.4,
            )
            curves.add(curve)
        axes_group = VGroup(axes, curves).move_to(panel.get_center() + DOWN * 0.08)
        formula = MathTex(r"g(s,t)", color=OUTPUT, font_size=34)
        formula.next_to(panel, DOWN, buff=0.12)
        super().__init__(panel, title_mob, axes_group, formula, **kwargs)


class Scene0202SeismologyFunctionsInsideEarth(TimedThreeDScene):
    SCRIPT_ID = "2.2"
    SCRIPT_TITLE = "Seismology: functions inside Earth"
    SCRIPT_START = 545.0
    SCRIPT_END = 645.0
    SCENE_DURATION = 100.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def fixed(self, *mobjects):
        self.add_fixed_in_frame_mobjects(*mobjects)
        self.remove(*mobjects)
        return mobjects[0] if len(mobjects) == 1 else mobjects

    def make_velocity_volume(self, highlighted=False):
        return EarthVelocityVolume(highlighted=highlighted)

    def make_wavefronts(self):
        source = np.array([-1.02, -0.15, -0.62])
        return VGroup(
            make_wave_sphere(source, 0.36, color=OPERATOR, opacity=0.14),
            make_wave_sphere(source, 0.78, color=OPERATOR, opacity=0.08),
            make_wave_sphere(source, 1.22, color=INPUT, opacity=0.055),
            make_wave_sphere(source, 1.72, color=SCIENCE, opacity=0.04),
        )

    def make_fault_and_source(self):
        fault = Line3D(
            start=np.array([-1.55, -0.32, -1.05]),
            end=np.array([-0.42, 0.32, 0.92]),
            color=WARNING,
            thickness=0.035,
        )
        source = Dot3D(point=np.array([-1.02, -0.15, -0.62]), radius=0.09, color=WARNING)
        return VGroup(fault, source)

    def make_sensor_array(self):
        return SurfaceSensorArray()

    def make_waveform_panel(self):
        return WaveformPanel()

    def make_derivative_card(self):
        card = RoundedRectangle(
            width=5.55,
            height=1.35,
            corner_radius=0.12,
            stroke_color=PHYSICS,
            stroke_width=1.25,
            fill_color=CARD_BG,
            fill_opacity=0.80,
        )
        equation = MathTex(
            r"u = u(x,y,z,t)",
            r"\qquad",
            r"\nabla_x u,\; \partial_t u",
            color=TEXT,
            font_size=34,
        )
        equation[0].set_color(INPUT)
        equation[2].set_color(PHYSICS)
        equation.move_to(card)
        caption = Text("physics lives in spatial + temporal derivatives", font_size=20, color=MUTED)
        caption.next_to(card, DOWN, buff=0.14)
        return VGroup(card, equation, caption)

    def make_inverse_problem_diagram(self):
        left = make_chip("surface observation", color=OUTPUT, width=2.6, font_size=17, height=0.42)
        right = make_chip("hidden volume", color=PURPLE, width=2.15, font_size=17, height=0.42)
        arrow = Arrow(LEFT * 1.05, RIGHT * 1.05, buff=0.08, color=OPERATOR, stroke_width=4)
        label = MathTex(r"g(s,t) \Rightarrow c(x)", color=OPERATOR, font_size=34)
        group = VGroup(left, arrow, right, label)
        left.move_to(LEFT * 1.95)
        arrow.move_to(ORIGIN)
        right.move_to(RIGHT * 1.95)
        label.next_to(arrow, DOWN, buff=0.15)
        return group

    def make_surrogate_panel(self):
        box = RoundedRectangle(
            width=5.9,
            height=2.05,
            corner_radius=0.14,
            stroke_color=OPERATOR,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.82,
        )
        title = Text("fast differentiable surrogate", font_size=25, color=OPERATOR, weight=BOLD)
        title.next_to(box, UP, buff=0.12)
        formula = MathTex(
            r"\widehat{\mathcal{G}}_{\theta}: c(x) \mapsto u(x,t)",
            color=TEXT,
            font_size=36,
        )
        formula[0][0:3].set_color(OPERATOR)
        bullets = VGroup(
            make_chip("fast forward map", color=INPUT, font_size=15, height=0.34),
            make_chip("differentiable", color=SCIENCE, font_size=15, height=0.34),
            make_chip("inverse loop", color=PURPLE, font_size=15, height=0.34),
        ).arrange(RIGHT, buff=0.18)
        inner = VGroup(formula, bullets).arrange(DOWN, buff=0.22).move_to(box)
        return VGroup(box, title, inner)

    def construct(self):
        np.random.seed(22)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES, zoom=1.02)
        self.begin_ambient_camera_rotation(rate=0.018)

        background = make_background_network(seed=22, n=34, dot_opacity=0.15, line_opacity=0.11)
        background.set_z_index(-10)
        title = Text("Seismology", font_size=42, color=TEXT, weight=BOLD)
        title.set_color_by_gradient(TEXT, SCIENCE)
        title.to_corner(UL, buff=0.32)
        scene_tag = make_chip("functions inside Earth", color=SCIENCE, width=2.55, font_size=17, height=0.4)
        scene_tag.next_to(title, DOWN, aligned_edge=LEFT, buff=0.13)
        self.add_fixed_in_frame_mobjects(background, title, scene_tag)
        self.remove(background, title, scene_tag)

        velocity_volume = self.make_velocity_volume(highlighted=False).shift(LEFT * 0.7)
        velocity_label = MathTex(r"c(x): \Omega \subset \mathbb{R}^{3} \to \mathbb{R}", color=INPUT, font_size=39)
        velocity_caption = Text("subsurface velocity field", font_size=23, color=INPUT, weight=BOLD)
        velocity_label.to_edge(DOWN, buff=0.72).shift(LEFT * 2.65)
        velocity_caption.next_to(velocity_label, UP, buff=0.12)
        self.fixed(velocity_label, velocity_caption)

        # Global 09:05.0-09:15.0 => local 0.0-10.0
        self.play_timed(
            "input_velocity_field_under_surface",
            0.0,
            10.0,
            FadeIn(background),
            Write(title),
            FadeIn(scene_tag, shift=DOWN * 0.06),
            FadeIn(velocity_volume, scale=0.96),
            FadeIn(velocity_caption, shift=UP * 0.08),
            FadeIn(velocity_label, shift=UP * 0.08),
        )

        fault_and_source = self.make_fault_and_source().shift(LEFT * 0.7)
        wavefronts = self.make_wavefronts().shift(LEFT * 0.7)
        sensors = self.make_sensor_array().shift(LEFT * 0.7)
        quake_label = make_chip("earthquake source", color=WARNING, width=2.0, font_size=17, height=0.42)
        propagation_label = make_chip("wave propagation in 3D + time", color=OPERATOR, width=3.15, font_size=17, height=0.42)
        quake_label.to_edge(RIGHT, buff=0.58).shift(UP * 1.05)
        propagation_label.next_to(quake_label, DOWN, aligned_edge=LEFT, buff=0.16)
        self.fixed(quake_label, propagation_label)

        # Global 09:15.0-09:27.5 => local 10.0-22.5
        self.play_timed(
            "earthquake_wave_propagates_through_volume",
            10.0,
            22.5,
            FadeIn(fault_and_source),
            LaggedStart(*[FadeIn(wave, scale=0.65) for wave in wavefronts], lag_ratio=0.22),
            FadeIn(sensors, shift=UP * 0.08),
            FadeIn(quake_label, shift=LEFT * 0.08),
            FadeIn(propagation_label, shift=LEFT * 0.08),
            velocity_volume.animate.set_opacity(0.78),
        )

        derivative_card = self.make_derivative_card()
        derivative_card.to_edge(DOWN, buff=0.44).shift(RIGHT * 2.4)
        self.fixed(derivative_card)

        # Global 09:27.5-09:39.5 => local 22.5-34.5
        self.play_timed(
            "space_time_function_and_derivatives",
            22.5,
            34.5,
            FadeOut(velocity_label, shift=DOWN * 0.08),
            FadeOut(velocity_caption, shift=DOWN * 0.08),
            FadeIn(derivative_card, shift=UP * 0.08),
            wavefronts.animate.scale(1.04).set_opacity(0.78),
            sensors.animate.set_opacity(0.95),
            rate_func=there_and_back,
        )

        # Global 09:39.5-09:40.7 => local 34.5-35.7
        self.wait_timed("pause_before_inverse_problem", 34.5, 35.7)

        waveform_panel = self.make_waveform_panel()
        waveform_panel.to_edge(RIGHT, buff=0.45).shift(UP * 0.08)
        inverse_arrow = Arrow(LEFT * 1.1, RIGHT * 1.1, color=OPERATOR, stroke_width=5, buff=0.1)
        inverse_arrow.rotate(PI)
        inverse_arrow.to_edge(DOWN, buff=1.1).shift(RIGHT * 1.0)
        inverse_label = Text("inverse problem", font_size=28, color=OPERATOR, weight=BOLD)
        inverse_label.next_to(inverse_arrow, UP, buff=0.12)
        self.fixed(waveform_panel, inverse_arrow, inverse_label)

        # Global 09:40.7-09:55.0 => local 35.7-50.0
        self.play_timed(
            "surface_measurements_to_subsurface_structure",
            35.7,
            50.0,
            FadeOut(quake_label, shift=RIGHT * 0.08),
            FadeOut(propagation_label, shift=RIGHT * 0.08),
            FadeOut(derivative_card, shift=DOWN * 0.08),
            FadeIn(waveform_panel, shift=LEFT * 0.12),
            FadeIn(inverse_arrow, shift=LEFT * 0.08),
            FadeIn(inverse_label, shift=DOWN * 0.08),
            sensors.animate.set_opacity(1.0),
            velocity_volume.animate.set_opacity(0.48),
        )

        hidden_volume = self.make_velocity_volume(highlighted=True).shift(LEFT * 0.7)
        inverse_diagram = self.make_inverse_problem_diagram()
        inverse_diagram.to_edge(DOWN, buff=0.45).shift(RIGHT * 1.35)
        self.fixed(inverse_diagram)

        # Global 09:55.0-10:06.5 => local 50.0-61.5
        self.play_timed(
            "infer_hidden_function_in_volume",
            50.0,
            61.5,
            FadeOut(velocity_volume, scale=0.98),
            FadeIn(hidden_volume, scale=0.98),
            FadeIn(inverse_diagram, shift=UP * 0.08),
            inverse_arrow.animate.set_color(PURPLE),
            inverse_label.animate.set_color(PURPLE),
            waveform_panel.animate.set_opacity(0.86),
        )

        surrogate_panel = self.make_surrogate_panel()
        surrogate_panel.to_edge(RIGHT, buff=0.38).shift(UP * 0.06)
        fast_badge = make_chip("orders faster than repeated PDE solves", color=OPERATOR, width=3.85, font_size=16, height=0.38)
        fast_badge.to_edge(DOWN, buff=0.54).shift(LEFT * 2.7)
        self.fixed(surrogate_panel, fast_badge)

        # Global 10:06.5-10:21.5 => local 61.5-76.5
        self.play_timed(
            "neural_operator_as_fast_differentiable_surrogate",
            61.5,
            76.5,
            FadeOut(waveform_panel, shift=RIGHT * 0.1),
            FadeOut(inverse_arrow, shift=DOWN * 0.06),
            FadeOut(inverse_label, shift=DOWN * 0.06),
            FadeIn(surrogate_panel, shift=LEFT * 0.12),
            FadeIn(fast_badge, shift=UP * 0.08),
            hidden_volume.animate.set_opacity(0.84),
            wavefronts.animate.set_opacity(0.42),
        )

        loop_arrow_1 = CurvedArrow(LEFT * 2.7 + UP * 1.25, RIGHT * 2.1 + UP * 1.25, color=SCIENCE, stroke_width=4)
        loop_arrow_2 = CurvedArrow(RIGHT * 2.0 + DOWN * 1.35, LEFT * 2.7 + DOWN * 1.35, color=PURPLE, stroke_width=4)
        loop_label = Text("optimize hidden Earth model through gradients", font_size=27, color=TEXT, weight=BOLD)
        loop_label.to_edge(UP, buff=0.52).shift(RIGHT * 1.8)
        self.fixed(loop_arrow_1, loop_arrow_2, loop_label)

        # Global 10:21.5-10:36.0 => local 76.5-91.0
        self.play_timed(
            "differentiable_inverse_loop",
            76.5,
            91.0,
            FadeIn(loop_arrow_1, shift=DOWN * 0.08),
            FadeIn(loop_arrow_2, shift=UP * 0.08),
            FadeIn(loop_label, shift=DOWN * 0.08),
            hidden_volume.animate.scale(1.04),
            surrogate_panel.animate.set_opacity(0.92),
            rate_func=there_and_back,
        )

        final_label = Text("function-to-function surrogate for inverse science", font_size=31, color=OUTPUT, weight=BOLD)
        final_label.to_edge(DOWN, buff=0.48).shift(RIGHT * 1.2)
        final_formula = MathTex(r"g(s,t) \rightarrow c(x) \rightarrow u(x,t)", color=TEXT, font_size=36)
        final_formula.next_to(final_label, UP, buff=0.18)
        final_formula[0][0:5].set_color(OUTPUT)
        final_formula[0][6:10].set_color(PURPLE)
        final_formula[0][11:].set_color(INPUT)
        self.fixed(final_label, final_formula)

        # Global 10:36.0-10:45.0 => local 91.0-100.0
        self.play_timed(
            "final_seismology_takeaway",
            91.0,
            98.0,
            FadeOut(fast_badge, shift=DOWN * 0.06),
            FadeOut(inverse_diagram, shift=DOWN * 0.06),
            FadeIn(final_formula, shift=UP * 0.08),
            FadeIn(final_label, shift=UP * 0.08),
            hidden_volume.animate.set_opacity(1.0),
        )
        self.wait_timed("final_hold_for_scene_2_3", 98.0, 100.0)
        self.pad_to(self.SCENE_DURATION)
