"""
Scene 11.1 - These are domains, not applications
Script: ../docs/full_voice_manim_script.md
Global time: 1:24:10.0-1:26:10.0
Local duration: 120.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_domain_pillar
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, NVIDIA_GREEN, OPERATOR, OUTPUT, PURPLE, SCIENCE, STAMP_RED, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_domain_pillars():
    pillars = VGroup(
        make_domain_pillar("weather", INPUT, ("dataset", "metric", "uncertainty")),
        make_domain_pillar("seismology", PURPLE, ("sensors", "inverse", "posterior")),
        make_domain_pillar("CFD", OPERATOR, ("geometry", "boundary", "drag")),
        make_domain_pillar("molecules", OUTPUT, ("symmetry", "trajectory", "stability")),
    ).arrange(RIGHT, buff=0.28)
    pillars.move_to(UP * 0.25)
    return pillars


def make_ecosystem_labels():
    return VGroup(
        Chip("problem setup", max_width=1.65, height=0.40, stroke_color=SCIENCE, font_size=14),
        Chip("dataset", max_width=1.08, height=0.40, stroke_color=INPUT, font_size=14),
        Chip("loss", max_width=0.82, height=0.40, stroke_color=WARNING, font_size=14),
        Chip("metric", max_width=0.98, height=0.40, stroke_color=OUTPUT, font_size=14),
        Chip("physics", max_width=1.10, height=0.40, stroke_color=OPERATOR, font_size=14),
        Chip("validation", max_width=1.45, height=0.40, stroke_color=NVIDIA_GREEN, font_size=14),
    ).arrange(RIGHT, buff=0.18).move_to(DOWN * 2.82)


class Scene1101DomainsNotApplications(TimedScene):
    SCRIPT_ID = "11.1"
    SCRIPT_TITLE = "These are domains, not applications"
    SCRIPT_START = 84 * 60 + 10
    SCRIPT_END = 86 * 60 + 10
    SCENE_DURATION = 120.0

    KEYFRAMES = (
        "KF01 0.0s application icons",
        "KF02 13.0s domain pillars",
        "KF03 25.0s ecosystem labels",
        "KF04 38.0s pause",
        "KF05 54.0s benchmark ecosystem",
        "KF06 79.5s no universal loss",
        "KF07 120.0s no plug-and-play framework",
    )

    def construct(self):
        background = make_background_network(seed=1101, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.1  Domains, not applications", max_width=3.90, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("weather, seismology, CFD, molecules are ML domains", max_width=8.1, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        pillars = make_domain_pillars()
        ecosystem = make_ecosystem_labels()
        benchmark = SafeText("scientific ML must build its own benchmark ecosystem", max_width=7.3, max_height=0.34, font_size=22, color=TEXT).move_to(DOWN * 2.15)
        no_loss = SafeText("no universal loss: conservation, rare events, uncertainty all matter", max_width=8.1, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.38)
        stamp = Chip("not auto-solve every PDE", max_width=3.20, height=0.54, stroke_color=STAMP_RED, text_color=STAMP_RED, font_size=20).move_to(DOWN * 2.18)
        assert_in_frame(VGroup(section_label, title, pillars, ecosystem, no_loss), margin=0.30, label="scene_11_01_layout")
        self.add(background)

        # Global 1:24:10.0 -> local 0.0; Global 1:24:23.0 -> local 13.0
        self.play_timed("apps_are_not_just_applications", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), LaggedStart(*[FadeIn(pillar.icon, shift=UP * 0.04) for pillar in pillars], lag_ratio=0.12))

        # Global 1:24:23.0 -> local 13.0; Global 1:24:35.0 -> local 25.0
        self.play_timed("become_domain_pillars", 13.0, 25.0, LaggedStart(*[FadeIn(pillar, shift=UP * 0.04) for pillar in pillars], lag_ratio=0.10))

        # Global 1:24:35.0 -> local 25.0; Global 1:24:48.0 -> local 38.0
        self.play_timed("domain_needs_full_problem_setup", 25.0, 38.0, LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in ecosystem], lag_ratio=0.08))

        # Global 1:24:48.0 -> local 38.0; Global 1:24:49.0 -> local 39.0
        self.wait_timed("pause_before_ecosystem", 38.0, 39.0)

        # Global 1:24:49.0 -> local 39.0; Global 1:25:04.0 -> local 54.0
        self.play_timed("scientific_ml_ecosystem", 39.0, 54.0, FadeIn(benchmark, shift=UP * 0.04), Circumscribe(ecosystem, color=SCIENCE, buff=0.08))

        # Global 1:25:04.0 -> local 54.0; Global 1:25:19.5 -> local 79.5
        self.play_timed("no_universal_l2_loss", 54.0, 79.5, FadeOut(benchmark), FadeIn(no_loss, shift=UP * 0.05), Circumscribe(VGroup(pillars[0].body, pillars[2].body), color=WARNING, buff=0.08))

        # Global 1:25:19.5 -> local 79.5; Global 1:26:10.0 -> local 120.0
        self.play_timed("framework_not_button", 79.5, 106.0, FadeOut(no_loss), FadeIn(stamp, shift=UP * 0.04), Circumscribe(stamp, color=STAMP_RED, buff=0.08))
        self.play_timed("final_domain_pillar_read", 106.0, 119.8, Circumscribe(pillars, color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
