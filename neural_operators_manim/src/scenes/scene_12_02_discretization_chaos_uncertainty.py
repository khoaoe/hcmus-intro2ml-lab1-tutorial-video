"""
Scene 12.2 - Discretization, chaos, uncertainty
Script: ../docs/full_voice_manim_script.md
Global time: 1:44:05.0-1:47:20.0
Local duration: 195.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.open_problem_visuals import make_chaotic_trajectories, make_mesh_error_plot, make_probability_cone, make_uncertainty_stack
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "mesh change",
    "error behavior",
    "nearby initial states diverge",
    "distribution, not one line",
    "calibrated uncertainty",
    "probabilistic NO",
    "conformal prediction",
    "sampling in function space",
)


class Scene1202DiscretizationChaosUncertainty(TimedScene):
    SCRIPT_ID = "12.2"
    SCRIPT_TITLE = "Discretization, chaos, uncertainty"
    SCRIPT_START = 104 * 60 + 5
    SCRIPT_END = 107 * 60 + 20
    SCENE_DURATION = 195.0

    KEYFRAMES = (
        "KF01 0.0s discretization error",
        "KF02 14.0s train deploy resolution",
        "KF03 28.0s mesh refinement convergence",
        "KF04 43.0s pause",
        "KF05 59.0s chaos sensitivity",
        "KF06 74.5s distribution over point estimate",
        "KF07 90.0s uncertainty awareness",
        "KF08 106.0s engineering risk",
        "KF09 128.0s calibrated uncertainty stack",
        "KF10 195.0s research intersection",
    )

    def construct(self):
        background = make_background_network(seed=1202, n=74, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("12.2  Discretization, chaos, uncertainty", max_width=4.95, height=0.42, stroke_color=PURPLE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("open problems compound when mesh, dynamics, and risk all change", max_width=8.7, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        mesh = make_mesh_error_plot().move_to(UP * 1.30)
        deploy = SafeText("train resolution != deploy resolution", max_width=4.8, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 1.10)
        convergence = SafeText("refinement should approach a stable limit, not prettier artifacts", max_width=7.5, max_height=0.34, font_size=21, color=SCIENCE).move_to(DOWN * 2.05)
        chaos = make_chaotic_trajectories().move_to(LEFT * 3.75 + UP * 0.30)
        cone = make_probability_cone().move_to(RIGHT * 4.05 + UP * 0.30)
        risk = SafeText("risk decisions need uncertainty, not just a confident curve", max_width=7.1, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 2.72)
        stack = make_uncertainty_stack().move_to(DOWN * 3.30)
        bridge = SafeText("probabilistic modeling + dynamical systems + numerical analysis", max_width=7.5, max_height=0.34, font_size=21, color=TEXT).move_to(DOWN * 2.68)
        assert_in_frame(VGroup(section_label, title, mesh, deploy, stack), margin=0.30, label="scene_12_02_layout")
        self.add(background)

        # Global 1:44:05.0 -> local 0.0; Global 1:44:19.0 -> local 14.0
        self.play_timed("discretization_error_problem", 0.0, 14.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(mesh, shift=UP * 0.04))

        # Global 1:44:19.0 -> local 14.0; Global 1:44:33.0 -> local 28.0
        self.play_timed("train_deploy_resolution_gap", 14.0, 28.0, FadeIn(deploy, shift=UP * 0.04), Circumscribe(mesh.meshes, color=WARNING, buff=0.08))

        # Global 1:44:33.0 -> local 28.0; Global 1:44:48.0 -> local 43.0
        self.play_timed("mesh_refinement_convergence_question", 28.0, 43.0, FadeIn(convergence, shift=UP * 0.04), Circumscribe(mesh.plot, color=SCIENCE, buff=0.08))

        # Global 1:44:48.0 -> local 43.0; Global 1:44:49.0 -> local 44.0
        self.wait_timed("pause_before_chaos", 43.0, 44.0)

        # Global 1:44:49.0 -> local 44.0; Global 1:45:04.0 -> local 59.0
        self.play_timed("chaos_sensitive_initial_condition", 44.0, 59.0, FadeOut(deploy), FadeOut(convergence), mesh.animate.shift(UP * 0.25).set_opacity(0.35), FadeIn(chaos, shift=UP * 0.04))

        # Global 1:45:04.0 -> local 59.0; Global 1:45:19.5 -> local 74.5
        self.play_timed("distribution_better_than_point_estimate", 59.0, 74.5, FadeIn(cone, shift=UP * 0.04), Circumscribe(cone, color=PURPLE, buff=0.08))

        # Global 1:45:19.5 -> local 74.5; Global 1:45:35.0 -> local 90.0
        self.play_timed("model_must_know_uncertainty", 74.5, 90.0, FadeIn(risk, shift=UP * 0.04), Circumscribe(chaos, color=WARNING, buff=0.08))

        # Global 1:45:35.0 -> local 90.0; Global 1:45:51.0 -> local 106.0
        self.play_timed("forecast_inverse_engineering_risk", 90.0, 106.0, Circumscribe(risk, color=WARNING, buff=0.08), cone[0].animate.set_fill(opacity=0.22))

        # Global 1:45:51.0 -> local 106.0; Global 1:46:13.0 -> local 128.0
        self.play_timed("uncertainty_method_stack", 106.0, 128.0, LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in stack], lag_ratio=0.08))

        # Global 1:46:13.0 -> local 128.0; Global 1:47:20.0 -> local 195.0
        self.play_timed("research_intersection", 128.0, 165.0, FadeOut(risk), FadeIn(bridge, shift=UP * 0.04), Circumscribe(VGroup(mesh, chaos, cone), color=SCIENCE, buff=0.12))
        self.play_timed("final_uncertainty_read", 165.0, 194.8, Circumscribe(stack, color=PURPLE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
