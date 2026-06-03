"""
Scene 11.3 - Geophysics and inverse solvers
Script: ../docs/full_voice_manim_script.md
Global time: 1:29:00.0-1:31:20.0
Local duration: 140.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_scenario_grid, make_subsurface_panel, make_surface_sensors
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, GRID, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "Earth structure",
    "surface sensors",
    "forward neural operator",
    "inverse loop",
    "Bayesian inversion",
    "ill-posed",
    "MCMC",
)


def make_forward_wave_operator():
    earth = make_subsurface_panel("Earth structure + source", width=4.25, height=2.45).move_to(LEFT * 4.70 + UP * 0.35)
    sensors = make_surface_sensors(count=7)
    sensors.move_to(earth.get_top() + UP * 0.35)
    waves = VGroup()
    for radius in (0.35, 0.62, 0.90):
        waves.add(Circle(radius=radius, color=OPERATOR, stroke_width=1.4, stroke_opacity=0.55).move_to(earth.get_center() + LEFT * 0.45 + DOWN * 0.15))
    operator = Chip("forward neural operator", max_width=3.05, height=0.50, stroke_color=OPERATOR, font_size=17).move_to(ORIGIN + UP * 0.35)
    observation = make_subsurface_panel("surface observations", width=3.25, height=1.62).move_to(RIGHT * 4.65 + UP * 0.35)
    arrows = VGroup(
        Arrow(earth.get_right(), operator.get_left(), buff=0.22, color=GRID, stroke_width=2.4),
        Arrow(operator.get_right(), observation.get_left(), buff=0.22, color=GRID, stroke_width=2.4),
    )
    group = VGroup(earth, sensors, waves, operator, observation, arrows)
    group.earth = earth
    group.sensors = sensors
    group.waves = waves
    group.operator = operator
    group.observation = observation
    group.arrows = arrows
    return group


class Scene1103GeophysicsInverseSolvers(TimedScene):
    SCRIPT_ID = "11.3"
    SCRIPT_TITLE = "Geophysics and inverse solvers"
    SCRIPT_START = 89 * 60
    SCRIPT_END = 91 * 60 + 20
    SCENE_DURATION = 140.0

    KEYFRAMES = (
        "KF01 0.0s forward wave map",
        "KF02 13.5s inverse problem",
        "KF03 26.0s infer subsurface",
        "KF04 41.0s pause",
        "KF05 57.0s differentiable surrogate",
        "KF06 73.5s ill-posed inversion",
        "KF07 90.0s posterior distribution",
        "KF08 140.0s sampling in function space",
    )

    def construct(self):
        background = make_background_network(seed=1103, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.3  Geophysics inverse solvers", max_width=4.15, height=0.42, stroke_color=PURPLE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("fast differentiable operators turn forward maps into inverse workflows", max_width=8.7, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        forward = make_forward_wave_operator()
        inverse_arrow = CurvedArrow(forward.observation.get_bottom(), forward.earth.get_bottom(), angle=-TAU / 4, color=OUTPUT, stroke_width=2.8)
        inverse_label = Chip("inverse loop", max_width=1.50, height=0.42, stroke_color=OUTPUT, font_size=15).move_to(DOWN * 2.05)
        surrogate = SafeText("optimization / Bayesian inversion uses the surrogate repeatedly", max_width=7.5, max_height=0.34, font_size=21, color=SCIENCE).move_to(DOWN * 3.30)
        illposed = SafeText("many underground structures can explain similar sensors", max_width=7.0, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 3.30)
        posterior = make_scenario_grid(rows=2, cols=5).move_to(DOWN * 2.35 + RIGHT * 3.85)
        sampler = Chip("Langevin / diffusion / MCMC in function space", max_width=5.05, height=0.48, stroke_color=PURPLE, font_size=16).move_to(DOWN * 3.35)
        assert_in_frame(VGroup(section_label, title, forward, surrogate, sampler), margin=0.30, label="scene_11_03_layout")
        self.add(background)

        # Global 1:29:00.0 -> local 0.0; Global 1:29:13.5 -> local 13.5
        self.play_timed("forward_wave_operator", 0.0, 13.5, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(forward.earth, shift=RIGHT * 0.05), FadeIn(forward.sensors, shift=DOWN * 0.04), LaggedStart(*[Create(wave) for wave in forward.waves], lag_ratio=0.18))

        # Global 1:29:13.5 -> local 13.5; Global 1:29:26.0 -> local 26.0
        self.play_timed("forward_to_inverse_problem", 13.5, 26.0, FadeIn(forward.operator, shift=UP * 0.04), Create(forward.arrows[0]), Create(forward.arrows[1]), FadeIn(forward.observation, shift=LEFT * 0.05))

        # Global 1:29:26.0 -> local 26.0; Global 1:29:41.0 -> local 41.0
        self.play_timed("surface_to_subsurface_inverse_loop", 26.0, 41.0, Create(inverse_arrow), FadeIn(inverse_label, shift=UP * 0.04), Circumscribe(forward.sensors, color=OUTPUT, buff=0.08))

        # Global 1:29:41.0 -> local 41.0; Global 1:29:42.0 -> local 42.0
        self.wait_timed("pause_before_surrogate", 41.0, 42.0)

        # Global 1:29:42.0 -> local 42.0; Global 1:29:57.0 -> local 57.0
        self.play_timed("fast_differentiable_surrogate", 42.0, 57.0, FadeIn(surrogate, shift=UP * 0.04), Circumscribe(forward.operator, color=SCIENCE, buff=0.08))

        # Global 1:29:57.0 -> local 57.0; Global 1:30:13.5 -> local 73.5
        self.play_timed("ill_posed_inverse_problem", 57.0, 73.5, FadeOut(surrogate), FadeIn(illposed, shift=UP * 0.04), Circumscribe(forward.earth, color=WARNING, buff=0.10))

        # Global 1:30:13.5 -> local 73.5; Global 1:30:30.0 -> local 90.0
        self.play_timed("posterior_distribution_not_single_estimate", 73.5, 90.0, FadeOut(illposed), FadeIn(posterior, shift=UP * 0.04), Circumscribe(posterior, color=PURPLE, buff=0.08))

        # Global 1:30:30.0 -> local 90.0; Global 1:31:20.0 -> local 140.0
        self.play_timed("sampling_algorithms_in_function_space", 90.0, 121.0, FadeIn(sampler, shift=UP * 0.04), Circumscribe(VGroup(posterior, sampler), color=PURPLE, buff=0.10))
        self.play_timed("final_geophysics_read", 121.0, 139.8, Circumscribe(VGroup(forward, inverse_arrow), color=SCIENCE, buff=0.12), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
