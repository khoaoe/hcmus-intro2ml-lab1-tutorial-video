"""
Scene 11.2 - Weather forecast
Script: ../docs/full_voice_manim_script.md
Global time: 1:26:10.0-1:29:00.0
Local duration: 170.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_ensemble_futures, make_sphere_field
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import apply_global_config, INPUT, MUTED, NVIDIA_GREEN, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_weather_system():
    current = make_sphere_field("state now", radius=1.18).move_to(LEFT * 4.95 + UP * 0.20)
    operator = Chip("SFNO / spherical basis", max_width=2.85, height=0.52, stroke_color=OPERATOR, font_size=17).move_to(ORIGIN + UP * 0.25)
    future = make_sphere_field("future state", radius=1.18).move_to(RIGHT * 4.95 + UP * 0.20)
    arrows = VGroup(
        Arrow(current.get_right(), operator.get_left(), buff=0.22, color=OPERATOR, stroke_width=3.0),
        Arrow(operator.get_right(), future.get_left(), buff=0.22, color=OPERATOR, stroke_width=3.0),
    )
    group = VGroup(current, operator, future, arrows)
    group.current = current
    group.operator = operator
    group.future = future
    group.arrows = arrows
    return group


class Scene1102WeatherForecast(TimedScene):
    SCRIPT_ID = "11.2"
    SCRIPT_TITLE = "Weather forecast"
    SCRIPT_START = 86 * 60 + 10
    SCRIPT_END = 89 * 60
    SCENE_DURATION = 170.0

    KEYFRAMES = (
        "KF01 0.0s weather on function spaces",
        "KF02 13.0s atmosphere ocean state",
        "KF03 27.0s sphere geometry",
        "KF04 40.0s spherical harmonics",
        "KF05 56.0s pause",
        "KF06 72.5s domain-informed basis",
        "KF07 89.0s ensemble futures",
        "KF08 104.5s chaos uncertainty metrics",
        "KF09 170.0s trustworthy forecast",
    )

    def construct(self):
        background = make_background_network(seed=1102, n=74, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.2  Weather forecast", max_width=3.15, height=0.42, stroke_color=INPUT, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("weather is a function-space forecasting domain", max_width=7.2, max_height=0.42, font_size=29, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        system = make_weather_system()
        formula = SafeMathTex(r"a_t(\theta,\phi)\mapsto a_{t+\Delta t}(\theta,\phi)", max_width=4.8, max_height=0.48, font_size=31, color=SCIENCE).move_to(DOWN * 1.95)
        geometry = Chip("basis follows Earth geometry", max_width=3.25, height=0.48, stroke_color=NVIDIA_GREEN, font_size=17).move_to(DOWN * 2.72)
        ensemble = make_ensemble_futures(count=7).move_to(DOWN * 2.10)
        open_problems = SafeText("chaos, uncertainty, extremes, calibration, domain metrics", max_width=7.2, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.38)
        trust = SafeText("beautiful forecast is not enough: event metrics and calibration matter", max_width=8.0, max_height=0.36, font_size=22, color=TEXT).move_to(DOWN * 3.38)
        assert_in_frame(VGroup(section_label, title, system, formula, open_problems), margin=0.30, label="scene_11_02_layout")
        self.add(background)

        # Global 1:26:10.0 -> local 0.0; Global 1:26:23.0 -> local 13.0
        self.play_timed("weather_function_space_domain", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(system.current, shift=RIGHT * 0.05))

        # Global 1:26:23.0 -> local 13.0; Global 1:26:37.0 -> local 27.0
        self.play_timed("atmosphere_ocean_to_future_state", 13.0, 27.0, Create(system.arrows[0]), FadeIn(system.operator, shift=UP * 0.04), Create(system.arrows[1]), FadeIn(system.future, shift=LEFT * 0.05), FadeIn(formula, shift=UP * 0.04))

        # Global 1:26:37.0 -> local 27.0; Global 1:26:50.0 -> local 40.0
        self.play_timed("sphere_domain_not_flat_fourier", 27.0, 40.0, Circumscribe(VGroup(system.current.globe, system.future.globe), color=SCIENCE, buff=0.08), FadeIn(geometry, shift=UP * 0.04))

        # Global 1:26:50.0 -> local 40.0; Global 1:27:06.0 -> local 56.0
        self.play_timed("spherical_fourier_neural_operator", 40.0, 56.0, Circumscribe(system.operator, color=OPERATOR, buff=0.08), system.current.bands.animate.set_stroke(width=4.4))

        # Global 1:27:06.0 -> local 56.0; Global 1:27:07.0 -> local 57.0
        self.wait_timed("pause_after_sfno", 56.0, 57.0)

        # Global 1:27:07.0 -> local 57.0; Global 1:27:22.5 -> local 72.5
        self.play_timed("domain_informed_architecture", 57.0, 72.5, Circumscribe(geometry, color=NVIDIA_GREEN, buff=0.08))

        # Global 1:27:22.5 -> local 72.5; Global 1:27:39.0 -> local 89.0
        self.play_timed("ensemble_forecast_distribution", 72.5, 89.0, FadeOut(formula), FadeOut(geometry), FadeIn(ensemble, shift=UP * 0.05), LaggedStart(*[Create(curve) for curve in ensemble.curves], lag_ratio=0.08))

        # Global 1:27:39.0 -> local 89.0; Global 1:27:54.5 -> local 104.5
        self.play_timed("open_problems_visible", 89.0, 104.5, FadeIn(open_problems, shift=UP * 0.04), Circumscribe(ensemble, color=WARNING, buff=0.08))

        # Global 1:27:54.5 -> local 104.5; Global 1:29:00.0 -> local 170.0
        self.play_timed("forecast_must_match_domain_metric", 104.5, 140.0, FadeOut(open_problems), FadeIn(trust, shift=UP * 0.04), Circumscribe(VGroup(system.future, ensemble), color=OUTPUT, buff=0.10))
        self.play_timed("final_weather_read", 140.0, 169.8, Circumscribe(system, color=SCIENCE, buff=0.12), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
