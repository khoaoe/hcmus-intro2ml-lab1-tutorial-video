"""
Scene 13.2 - Last line
Script: ../docs/full_voice_manim_script.md
Global time: 1:57:30.0-1:58:20.0
Local duration: 50.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.closing_visuals import (
    make_beginning_line,
    make_final_operator_arrow,
    make_grand_summary_flow,
    make_learning_in_infinite_dimensions_title,
)
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, OPERATOR, SCIENCE, TEXT
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "Learning in infinite dimensions",
    r"\mathcal{G}: \mathcal{A} \to \mathcal{U}",
    "field này mới chỉ bắt đầu",
)


class Scene1302LastLine(TimedScene):
    SCRIPT_ID = "13.2"
    SCRIPT_TITLE = "Last line"
    SCRIPT_START = 117 * 60 + 30
    SCRIPT_END = 118 * 60 + 20
    SCENE_DURATION = 50.0

    KEYFRAMES = (
        "KF01 0.0s prior flow compresses",
        "KF02 12.0s pause before core sentence",
        "KF03 13.0s final operator arrow",
        "KF04 30.0s learning in infinite dimensions",
        "KF05 42.0s field just begins",
        "KF06 50.0s fade out",
    )

    def construct(self):
        background = make_background_network(seed=1302, n=64, dot_opacity=0.06, line_opacity=0.035)
        section_label = Chip("13.2  Last line", max_width=2.70, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        prompt = SafeText("if you keep one sentence, keep this one", max_width=7.8, max_height=0.40, font_size=27, color=TEXT, weight="BOLD").move_to(UP * 3.28)
        prior_flow = make_grand_summary_flow().scale(0.72).move_to(UP * 1.45)
        prior_flow.set_opacity(0.52)
        operator_arrow = make_final_operator_arrow().move_to(UP * 0.72)
        final_title = make_learning_in_infinite_dimensions_title().move_to(DOWN * 1.30)
        beginning = make_beginning_line().move_to(DOWN * 2.82)
        assert_in_frame(VGroup(section_label, prompt, prior_flow, operator_arrow, final_title, beginning), margin=0.30, label="scene_13_02_layout")
        self.add(background)

        # Global 1:57:30.0 -> local 0.0; Global 1:57:42.0 -> local 12.0
        self.play_timed(
            "keep_one_sentence",
            0.0,
            12.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(prompt, shift=DOWN * 0.05),
            FadeIn(prior_flow, shift=UP * 0.04),
        )

        # Global 1:57:42.0 -> local 12.0; Global 1:57:43.0 -> local 13.0
        self.wait_timed("pause_before_final_sentence", 12.0, 13.0)

        # Global 1:57:43.0 -> local 13.0; Global 1:58:00.0 -> local 30.0
        self.play_timed(
            "function_data_requires_function_space_model",
            13.0,
            30.0,
            ReplacementTransform(prior_flow, operator_arrow),
            FadeOut(prompt),
            Circumscribe(operator_arrow.formula_label, color=OPERATOR, buff=0.10),
        )

        # Global 1:58:00.0 -> local 30.0; Global 1:58:12.0 -> local 42.0
        self.play_timed(
            "learning_in_infinite_dimensions",
            30.0,
            42.0,
            FadeIn(final_title, shift=UP * 0.06),
            Circumscribe(final_title, color=SCIENCE, buff=0.10),
        )

        # Global 1:58:12.0 -> local 42.0; Global 1:58:20.0 -> local 50.0
        self.play_timed(
            "field_just_begins",
            42.0,
            47.5,
            FadeIn(beginning, shift=UP * 0.05),
            Circumscribe(beginning, color=SCIENCE, buff=0.10),
        )
        self.play_timed(
            "fade_out",
            47.5,
            49.8,
            FadeOut(VGroup(section_label, operator_arrow, final_title, beginning)),
        )
        self.pad_to(self.SCENE_DURATION)
