"""
Scene 11.4 - Carbon storage and climate mitigation
Script: ../docs/full_voice_manim_script.md
Global time: 1:31:20.0-1:33:35.0
Local duration: 135.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_reservoir_cross_section, make_scenario_grid
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "CO2 plume",
    "many scenarios",
    "fast neural-operator surrogate",
    "uncertainty quantification",
    "plume-boundary",
    "analysis at scale",
)


class Scene1104CarbonStorage(TimedScene):
    SCRIPT_ID = "11.4"
    SCRIPT_TITLE = "Carbon storage and climate mitigation"
    SCRIPT_START = 91 * 60 + 20
    SCRIPT_END = 93 * 60 + 35
    SCENE_DURATION = 135.0

    KEYFRAMES = (
        "KF01 0.0s carbon storage setup",
        "KF02 13.0s plume prediction",
        "KF03 27.0s expensive realizations",
        "KF04 40.0s pause",
        "KF05 55.5s fast surrogate",
        "KF06 71.0s UQ optimization",
        "KF07 87.0s plume boundary risk",
        "KF08 135.0s scale analysis payoff",
    )

    def construct(self):
        background = make_background_network(seed=1104, n=70, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.4  Carbon storage", max_width=2.95, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("operator learning makes many subsurface scenarios practical", max_width=8.0, max_height=0.42, font_size=29, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        reservoir = make_reservoir_cross_section().move_to(LEFT * 3.75 + UP * 0.10)
        scenarios = make_scenario_grid(rows=2, cols=4).move_to(RIGHT * 4.20 + UP * 0.10)
        solver = Chip("expensive simulator", max_width=2.35, height=0.46, stroke_color=WARNING, font_size=16).move_to(RIGHT * 1.00 + UP * 1.10)
        surrogate = Chip("fast neural-operator surrogate", max_width=3.40, height=0.48, stroke_color=OUTPUT, font_size=17).move_to(RIGHT * 1.00 + DOWN * 0.10)
        uq = SafeText("uncertainty quantification + reservoir optimization", max_width=6.7, max_height=0.34, font_size=21, color=PURPLE).move_to(DOWN * 2.62)
        risk = SafeText("small plume-boundary errors can change engineering decisions", max_width=7.4, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.34)
        payoff = SafeText("payoff: analysis at scale, not just faster prediction", max_width=6.9, max_height=0.36, font_size=22, color=TEXT).move_to(DOWN * 3.34)
        assert_in_frame(VGroup(section_label, title, reservoir, scenarios, risk), margin=0.30, label="scene_11_04_layout")
        self.add(background)

        # Global 1:31:20.0 -> local 0.0; Global 1:31:33.0 -> local 13.0
        self.play_timed("carbon_capture_storage_setup", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(reservoir.section, shift=RIGHT * 0.05), FadeIn(reservoir.well, shift=DOWN * 0.04))

        # Global 1:31:33.0 -> local 13.0; Global 1:31:47.0 -> local 27.0
        self.play_timed("co2_plume_under_geologic_uncertainty", 13.0, 27.0, GrowFromCenter(reservoir.plume), FadeIn(reservoir[-1], shift=UP * 0.03), Circumscribe(reservoir.plume, color=OPERATOR, buff=0.08))

        # Global 1:31:47.0 -> local 27.0; Global 1:32:00.0 -> local 40.0
        self.play_timed("expensive_realizations", 27.0, 40.0, FadeIn(solver, shift=UP * 0.04), FadeIn(scenarios, shift=LEFT * 0.05))

        # Global 1:32:00.0 -> local 40.0; Global 1:32:01.0 -> local 41.0
        self.wait_timed("pause_before_surrogate", 40.0, 41.0)

        # Global 1:32:01.0 -> local 41.0; Global 1:32:15.5 -> local 55.5
        self.play_timed("surrogate_runs_many_scenarios", 41.0, 55.5, FadeIn(surrogate, shift=UP * 0.04), Circumscribe(surrogate, color=OUTPUT, buff=0.08))

        # Global 1:32:15.5 -> local 55.5; Global 1:32:31.0 -> local 71.0
        self.play_timed("uq_and_optimization_support", 55.5, 71.0, FadeIn(uq, shift=UP * 0.04), Circumscribe(scenarios, color=PURPLE, buff=0.08))

        # Global 1:32:31.0 -> local 71.0; Global 1:32:47.0 -> local 87.0
        self.play_timed("plume_boundary_risk", 71.0, 87.0, FadeIn(risk, shift=UP * 0.04), Circumscribe(reservoir.plume, color=WARNING, buff=0.16))

        # Global 1:32:47.0 -> local 87.0; Global 1:33:35.0 -> local 135.0
        self.play_timed("operator_learning_payoff_at_scale", 87.0, 116.0, FadeOut(risk), FadeIn(payoff, shift=UP * 0.04), Circumscribe(VGroup(reservoir, scenarios), color=SCIENCE, buff=0.12))
        self.play_timed("final_carbon_storage_read", 116.0, 134.8, Circumscribe(surrogate, color=OUTPUT, buff=0.08), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
