"""
Scene 12.5 - The honest state of the field
Script: ../docs/full_voice_manim_script.md
Global time: 1:53:05.0-1:55:20.0
Local duration: 135.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.open_problem_visuals import make_domain_orbit, make_function_space_diagram, make_open_problems_board
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "open problems",
    "accuracy",
    "metrics",
    "scaling",
    "OOD behavior",
    "uncertainty",
    "discretization",
    "weather",
    "CFD",
    "geophysics",
)


class Scene1205HonestStateOfField(TimedScene):
    SCRIPT_ID = "12.5"
    SCRIPT_TITLE = "The honest state of the field"
    SCRIPT_START = 113 * 60 + 5
    SCRIPT_END = 115 * 60 + 20
    SCENE_DURATION = 135.0

    KEYFRAMES = (
        "KF01 0.0s not final answer",
        "KF02 13.0s unresolved list",
        "KF03 27.0s strong language for function spaces",
        "KF04 41.0s pause",
        "KF05 59.0s ask operator domain discretization",
        "KF06 76.0s continuum object question",
        "KF07 94.0s ML closer to scientific computing",
        "KF08 135.0s ML meets physics",
    )

    def construct(self):
        background = make_background_network(seed=1205, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("12.5  Honest state of the field", max_width=4.10, height=0.42, stroke_color=WARNING, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("neural operators are not the final answer, but they changed the language", max_width=9.0, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        board = make_open_problems_board().move_to(UP * 0.95)
        language = SafeText("a strong language for ML on function spaces", max_width=6.2, max_height=0.34, font_size=22, color=SCIENCE).move_to(DOWN * 1.55)
        questions = VGroup(
            Chip("underlying operator?", max_width=2.35, height=0.42, stroke_color=OPERATOR, font_size=15),
            Chip("domain?", max_width=1.05, height=0.42, stroke_color=INPUT, font_size=15),
            Chip("discretization effect?", max_width=2.55, height=0.42, stroke_color=WARNING, font_size=15),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 2.50)
        diagram = make_function_space_diagram().move_to(DOWN * 0.10)
        orbit = make_domain_orbit().move_to(DOWN * 0.20)
        final = SafeText("not just an architecture trend: a place where ML meets physics", max_width=7.6, max_height=0.36, font_size=22, color=TEXT).move_to(DOWN * 3.38)
        assert_in_frame(VGroup(section_label, title, board, questions, final), margin=0.30, label="scene_12_05_layout")
        self.add(background)

        # Global 1:53:05.0 -> local 0.0; Global 1:53:18.0 -> local 13.0
        self.play_timed("not_final_answer", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(board, shift=UP * 0.04))

        # Global 1:53:18.0 -> local 13.0; Global 1:53:32.0 -> local 27.0
        self.play_timed("unresolved_accuracy_metrics_scaling_ood", 13.0, 27.0, Circumscribe(board, color=WARNING, buff=0.08))

        # Global 1:53:32.0 -> local 27.0; Global 1:53:46.0 -> local 41.0
        self.play_timed("language_for_function_spaces", 27.0, 41.0, FadeIn(language, shift=UP * 0.04), Circumscribe(language, color=SCIENCE, buff=0.08))

        # Global 1:53:46.0 -> local 41.0; Global 1:53:47.0 -> local 42.0
        self.wait_timed("pause_before_core_questions", 41.0, 42.0)

        # Global 1:53:47.0 -> local 42.0; Global 1:54:04.0 -> local 59.0
        self.play_timed("ask_operator_domain_discretization", 42.0, 59.0, LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in questions], lag_ratio=0.12))

        # Global 1:54:04.0 -> local 59.0; Global 1:54:21.0 -> local 76.0
        self.play_timed("continuum_object_question", 59.0, 76.0, FadeOut(language), FadeIn(diagram, shift=UP * 0.05), Circumscribe(diagram, color=OPERATOR, buff=0.10))

        # Global 1:54:21.0 -> local 76.0; Global 1:54:39.0 -> local 94.0
        self.play_timed("ml_language_closer_to_scientific_computing", 76.0, 94.0, ReplacementTransform(diagram, orbit), Circumscribe(orbit, color=SCIENCE, buff=0.12))

        # Global 1:54:39.0 -> local 94.0; Global 1:55:20.0 -> local 135.0
        self.play_timed("where_ml_meets_physics", 94.0, 118.0, FadeIn(final, shift=UP * 0.04), Circumscribe(VGroup(board, orbit), color=SCIENCE, buff=0.12))
        self.play_timed("final_section_12_read", 118.0, 134.8, Circumscribe(final, color=OPERATOR, buff=0.08), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
