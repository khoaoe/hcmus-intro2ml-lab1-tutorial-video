"""
Scene 10.7 - Local and differential kernels
Script: ../docs/full_voice_manim_script.md
Global time: 1:22:30.0-1:24:10.0
Local duration: 100.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_kernel_formula, make_stencil_grid, make_wave_panel
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PHYSICS, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_differential_stage():
    cnn = make_stencil_grid("CNN stencil", color=INPUT, center_color=INPUT, scale_label="fixed coeffs").move_to(LEFT * 4.85 + UP * 0.70)
    derivative = make_stencil_grid("derivative stencil", color=PHYSICS, center_color=OUTPUT, scale_label=r"1 / h").move_to(ORIGIN + UP * 0.70)
    refined = make_stencil_grid("refined grid", color=SCIENCE, center_color=OUTPUT, cell=0.26, scale_label=r"1 / (h/2)").move_to(RIGHT * 4.85 + UP * 0.70)
    arrows = VGroup(
        Arrow(cnn.get_right(), derivative.get_left(), buff=0.22, color=GRID, stroke_width=2.3),
        Arrow(derivative.get_right(), refined.get_left(), buff=0.22, color=GRID, stroke_width=2.3),
    )
    stage = VGroup(cnn, derivative, refined, arrows)
    stage.cnn = cnn
    stage.derivative = derivative
    stage.refined = refined
    stage.arrows = arrows
    return stage


class Scene1007LocalDifferentialKernels(TimedScene):
    SCRIPT_ID = "10.7"
    SCRIPT_TITLE = "Local and differential kernels"
    SCRIPT_START = 82 * 60 + 30
    SCRIPT_END = 84 * 60 + 10
    SCENE_DURATION = 100.0

    KEYFRAMES = (
        "KF01 0.0s integral operators meet derivatives",
        "KF02 13.5s residual or forcing map",
        "KF03 26.0s CNN stencil detects differences",
        "KF04 39.5s pause",
        "KF05 56.0s coefficients scale with grid size",
        "KF06 71.0s h halves stencil scales",
        "KF07 100.0s local physics any resolution",
    )

    def construct(self):
        background = make_background_network(seed=1007, n=66, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.7  Local and differential kernels", max_width=4.35, height=0.42, stroke_color=PHYSICS, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("local physics needs the right scaling under refinement", max_width=7.2, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        field = make_wave_panel("u -> forcing / residual", color=INPUT, width=4.25, height=1.55).move_to(DOWN * 2.05 + LEFT * 3.30)
        residual = make_kernel_formula(r"\partial_x u,\; \Delta u,\; \mathcal{R}(u)", color=PHYSICS, max_width=3.85).move_to(DOWN * 2.05 + RIGHT * 3.15)
        stage = make_differential_stage()
        compare = SafeText("fixed image kernel can collapse; differential kernel has a resolution-aware limit", max_width=8.2, max_height=0.36, font_size=21, color=WARNING)
        compare.move_to(DOWN * 3.28)
        final = Chip("predict at any resolution with local physics", max_width=4.25, height=0.50, stroke_color=SCIENCE, font_size=18).move_to(DOWN * 2.95)
        assert_in_frame(VGroup(section_label, title, stage, field, residual, compare), margin=0.30, label="scene_10_07_layout")
        self.add(background)

        # Global 1:22:30.0 -> local 0.0; Global 1:22:43.5 -> local 13.5
        self.play_timed("integral_operators_meet_derivatives", 0.0, 13.5, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(field, shift=RIGHT * 0.05))

        # Global 1:22:43.5 -> local 13.5; Global 1:22:56.0 -> local 26.0
        self.play_timed("map_to_forcing_or_residual", 13.5, 26.0, FadeIn(residual, shift=LEFT * 0.05), Circumscribe(field, color=INPUT, buff=0.08))

        # Global 1:22:56.0 -> local 26.0; Global 1:23:09.5 -> local 39.5
        self.play_timed("cnn_stencil_local_differences", 26.0, 39.5, FadeIn(stage.cnn, shift=UP * 0.04), Circumscribe(stage.cnn, color=INPUT, buff=0.08))

        # Global 1:23:09.5 -> local 39.5; Global 1:23:10.5 -> local 40.5
        self.wait_timed("pause_after_cnn_stencil", 39.5, 40.5)

        # Global 1:23:10.5 -> local 40.5; Global 1:23:26.0 -> local 56.0
        self.play_timed("scale_coefficients_with_grid_size", 40.5, 56.0, Create(stage.arrows[0]), FadeIn(stage.derivative, shift=UP * 0.04), FadeIn(compare, shift=UP * 0.04))

        # Global 1:23:26.0 -> local 56.0; Global 1:23:41.0 -> local 71.0
        self.play_timed("grid_half_stencil_scale_changes", 56.0, 71.0, Create(stage.arrows[1]), FadeIn(stage.refined, shift=UP * 0.04), Circumscribe(stage.refined, color=SCIENCE, buff=0.08))

        # Global 1:23:41.0 -> local 71.0; Global 1:24:10.0 -> local 100.0
        self.play_timed("local_physics_any_resolution", 71.0, 92.0, FadeOut(compare), FadeIn(final, shift=UP * 0.04), Circumscribe(VGroup(stage.derivative, stage.refined), color=PHYSICS, buff=0.10))
        self.play_timed("final_differential_read", 92.0, 99.8, Circumscribe(final, color=SCIENCE, buff=0.08), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
