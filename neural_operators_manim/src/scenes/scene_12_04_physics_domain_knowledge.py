"""
Scene 12.4 - Incorporating physics and domain knowledge
Script: ../docs/full_voice_manim_script.md
Global time: 1:50:20.0-1:53:05.0
Local duration: 165.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.open_problem_visuals import make_balance_scale, make_collaboration_network, make_physics_prior_blocks
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "flexibility",
    "physics prior",
    "symmetry",
    "conservation",
    "boundary",
    "local kernels",
    "PDE loss",
    "ML",
    "applied math",
    "domain expert",
)


class Scene1204PhysicsDomainKnowledge(TimedScene):
    SCRIPT_ID = "12.4"
    SCRIPT_TITLE = "Incorporating physics and domain knowledge"
    SCRIPT_START = 110 * 60 + 20
    SCRIPT_END = 113 * 60 + 5
    SCENE_DURATION = 165.0

    KEYFRAMES = (
        "KF01 0.0s encode physics at right level",
        "KF02 13.0s too little domain knowledge",
        "KF03 26.0s too much hand-designed bias",
        "KF04 40.0s pause",
        "KF05 56.0s balance modules",
        "KF06 73.0s domain-specific answer",
        "KF07 90.0s early field",
        "KF08 110.0s collaboration",
        "KF09 165.0s combine ML and solvers",
    )

    def construct(self):
        background = make_background_network(seed=1204, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("12.4  Physics and domain knowledge", max_width=4.45, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("the hard question is how much physics to encode", max_width=7.2, max_height=0.42, font_size=29, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        scale = make_balance_scale().move_to(UP * 1.35)
        too_little = SafeText("too little prior: too much data, possible law violations", max_width=6.8, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 0.95)
        too_much = SafeText("too much hand design: less flexibility, unknown physics missed", max_width=7.4, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 1.70)
        blocks = make_physics_prior_blocks().move_to(DOWN * 0.20)
        domain_answer = SafeText("each domain chooses a different balance", max_width=5.4, max_height=0.34, font_size=21, color=SCIENCE).move_to(DOWN * 3.16)
        collaboration = make_collaboration_network().move_to(DOWN * 0.30)
        combine = SafeText("the strength is combining data learning with solver knowledge", max_width=7.2, max_height=0.36, font_size=22, color=TEXT).move_to(DOWN * 3.30)
        assert_in_frame(VGroup(section_label, title, scale, too_much, domain_answer), margin=0.30, label="scene_12_04_layout")
        self.add(background)

        # Global 1:50:20.0 -> local 0.0; Global 1:50:33.0 -> local 13.0
        self.play_timed("right_amount_of_physics", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(scale, shift=UP * 0.04))

        # Global 1:50:33.0 -> local 13.0; Global 1:50:46.0 -> local 26.0
        self.play_timed("too_little_domain_knowledge", 13.0, 26.0, FadeIn(too_little, shift=UP * 0.04), Circumscribe(scale[3], color=WARNING, buff=0.08))

        # Global 1:50:46.0 -> local 26.0; Global 1:51:00.0 -> local 40.0
        self.play_timed("too_much_hand_designed_bias", 26.0, 40.0, FadeIn(too_much, shift=UP * 0.04), Circumscribe(scale[4], color=WARNING, buff=0.08))

        # Global 1:51:00.0 -> local 40.0; Global 1:51:01.0 -> local 41.0
        self.wait_timed("pause_before_balance", 40.0, 41.0)

        # Global 1:51:01.0 -> local 41.0; Global 1:51:16.0 -> local 56.0
        self.play_timed("physics_prior_modules", 41.0, 56.0, FadeOut(too_little), FadeOut(too_much), FadeIn(blocks, shift=UP * 0.05))

        # Global 1:51:16.0 -> local 56.0; Global 1:51:33.0 -> local 73.0
        self.play_timed("domain_specific_answer", 56.0, 73.0, FadeIn(domain_answer, shift=UP * 0.04), Circumscribe(blocks, color=SCIENCE, buff=0.10))

        # Global 1:51:33.0 -> local 73.0; Global 1:51:50.0 -> local 90.0
        early = Chip("early field, many open design choices", max_width=4.05, height=0.48, stroke_color=PURPLE, font_size=17).move_to(DOWN * 2.42)
        self.play_timed("field_is_still_early", 73.0, 90.0, FadeIn(early, shift=UP * 0.04), Circumscribe(early, color=PURPLE, buff=0.08))

        # Global 1:51:50.0 -> local 90.0; Global 1:52:10.0 -> local 110.0
        self.play_timed("collaboration_between_disciplines", 90.0, 110.0, FadeOut(blocks), FadeOut(domain_answer), FadeOut(early), FadeIn(collaboration, shift=UP * 0.05), LaggedStart(*[Create(edge) for edge in collaboration[0]], lag_ratio=0.08))

        # Global 1:52:10.0 -> local 110.0; Global 1:53:05.0 -> local 165.0
        self.play_timed("combine_ml_and_solvers", 110.0, 142.0, FadeIn(combine, shift=UP * 0.04), Circumscribe(collaboration, color=SCIENCE, buff=0.12))
        self.play_timed("final_physics_balance_read", 142.0, 164.8, Circumscribe(scale, color=OPERATOR, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
