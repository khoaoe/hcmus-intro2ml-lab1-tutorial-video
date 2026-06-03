"""
Scene 11.7 - Physics verification
Script: ../docs/full_voice_manim_script.md
Global time: 1:38:10.0-1:41:40.0
Local duration: 210.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_kernel_formula, make_wave_panel
from src.common.domain_visuals import make_conservation_gauge, make_leaderboard_card, make_tipping_curve
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_residual_checker():
    prediction = make_wave_panel("predicted function", color=INPUT, width=3.1, height=1.42)
    checker = make_kernel_formula(r"\mathcal{R}(\hat{u})", color=OPERATOR, max_width=2.35)
    residual = Chip("PDE residual", max_width=1.75, height=0.42, stroke_color=WARNING, font_size=15)
    group = VGroup(prediction, checker, residual).arrange(RIGHT, buff=0.48)
    group.prediction = prediction
    group.checker = checker
    group.residual = residual
    return group


class Scene1107PhysicsVerification(TimedScene):
    SCRIPT_ID = "11.7"
    SCRIPT_TITLE = "Physics verification"
    SCRIPT_START = 98 * 60 + 10
    SCRIPT_END = 101 * 60 + 40
    SCENE_DURATION = 210.0

    KEYFRAMES = (
        "KF01 0.0s expert verification question",
        "KF02 14.0s residual conservation checks",
        "KF03 28.0s tipping point",
        "KF04 42.0s pause",
        "KF05 58.0s time function equation check",
        "KF06 75.0s output as function enables verification",
        "KF07 92.0s pretty but unsafe field",
        "KF08 115.0s uncertainty calibration validation",
        "KF09 210.0s L2 leaderboard cracks",
    )

    def construct(self):
        background = make_background_network(seed=1107, n=74, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.7  Physics verification", max_width=3.45, height=0.42, stroke_color=WARNING, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("domain experts verify functions with physics, not only screenshots", max_width=8.4, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        checker = make_residual_checker().move_to(UP * 1.50)
        gauge = make_conservation_gauge("conservation").move_to(LEFT * 4.65 + DOWN * 0.65)
        tipping = make_tipping_curve().move_to(RIGHT * 4.15 + DOWN * 0.48)
        function_note = SafeText("output-as-function makes equation checks meaningful", max_width=6.7, max_height=0.34, font_size=21, color=SCIENCE).move_to(DOWN * 2.28)
        unsafe = SafeText("a pretty field that violates conservation can be dangerous", max_width=7.0, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.25)
        validation = VGroup(
            Chip("uncertainty", max_width=1.55, height=0.40, stroke_color=PURPLE, font_size=14),
            Chip("calibration", max_width=1.45, height=0.40, stroke_color=OUTPUT, font_size=14),
            Chip("physics-informed loss", max_width=2.45, height=0.40, stroke_color=OPERATOR, font_size=14),
            Chip("domain validation", max_width=2.05, height=0.40, stroke_color=SCIENCE, font_size=14),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 2.95)
        leaderboard = make_leaderboard_card().move_to(RIGHT * 4.55 + DOWN * 0.72)
        final = SafeText("winning a small L2 benchmark can still lose the real problem", max_width=7.0, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.38)
        assert_in_frame(VGroup(section_label, title, checker, gauge, tipping, final), margin=0.30, label="scene_11_07_layout")
        self.add(background)

        # Global 1:38:10.0 -> local 0.0; Global 1:38:24.0 -> local 14.0
        self.play_timed("expert_verification_question", 0.0, 14.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(checker.prediction, shift=RIGHT * 0.05))

        # Global 1:38:24.0 -> local 14.0; Global 1:38:38.0 -> local 28.0
        self.play_timed("residual_conservation_checks", 14.0, 28.0, FadeIn(checker.checker, shift=UP * 0.04), FadeIn(checker.residual, shift=UP * 0.04), FadeIn(gauge, shift=UP * 0.04))

        # Global 1:38:38.0 -> local 28.0; Global 1:38:52.0 -> local 42.0
        self.play_timed("climate_tipping_point_curve", 28.0, 42.0, FadeIn(tipping, shift=UP * 0.04), Circumscribe(tipping, color=WARNING, buff=0.08))

        # Global 1:38:52.0 -> local 42.0; Global 1:38:53.0 -> local 43.0
        self.wait_timed("pause_before_function_verification", 42.0, 43.0)

        # Global 1:38:53.0 -> local 43.0; Global 1:39:08.0 -> local 58.0
        self.play_timed("time_function_equation_check", 43.0, 58.0, FadeIn(function_note, shift=UP * 0.04), Circumscribe(checker, color=SCIENCE, buff=0.10))

        # Global 1:39:08.0 -> local 58.0; Global 1:39:25.0 -> local 75.0
        self.play_timed("output_as_function_not_aesthetic", 58.0, 75.0, checker.prediction.curve.animate.set_stroke(width=4.4), Circumscribe(function_note, color=SCIENCE, buff=0.08))

        # Global 1:39:25.0 -> local 75.0; Global 1:39:42.0 -> local 92.0
        self.play_timed("pretty_field_wrong_conservation_danger", 75.0, 92.0, FadeIn(unsafe, shift=UP * 0.04), gauge[1].animate.rotate(-0.55, about_point=ORIGIN))

        # Global 1:39:42.0 -> local 92.0; Global 1:40:05.0 -> local 115.0
        self.play_timed("uncertainty_calibration_physics_validation", 92.0, 115.0, FadeOut(unsafe), LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in validation], lag_ratio=0.08), Circumscribe(validation, color=PURPLE, buff=0.08))

        # Global 1:40:05.0 -> local 115.0; Global 1:41:40.0 -> local 210.0
        self.play_timed("l2_leaderboard_cracks", 115.0, 160.0, FadeOut(tipping), FadeIn(leaderboard, shift=LEFT * 0.05), FadeIn(final, shift=UP * 0.04), Circumscribe(leaderboard, color=WARNING, buff=0.08))
        self.play_timed("bridge_to_open_problems", 160.0, 209.8, Circumscribe(VGroup(checker, validation, leaderboard), color=SCIENCE, buff=0.12), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
