"""
Scene 11.6 - Automotive CFD and domain knowledge
Script: ../docs/full_voice_manim_script.md
Global time: 1:35:30.0-1:38:10.0
Local duration: 160.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_car_mesh, make_pressure_field
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "car geometry",
    "pressure / velocity field",
    "sharp boundary",
    "geometry + boundary sensitive",
    "inductive bias",
    "domain-informed",
    "sample",
    "not millions",
)


class Scene1106AutomotiveCFD(TimedScene):
    SCRIPT_ID = "11.6"
    SCRIPT_TITLE = "Automotive CFD and domain knowledge"
    SCRIPT_START = 95 * 60 + 30
    SCRIPT_END = 98 * 60 + 10
    SCENE_DURATION = 160.0

    KEYFRAMES = (
        "KF01 0.0s car geometry mesh input",
        "KF02 13.0s pressure velocity output",
        "KF03 25.5s geometry boundary sensitivity",
        "KF04 39.0s pause",
        "KF05 55.0s discontinuity question",
        "KF06 70.0s hard without inductive bias",
        "KF07 87.0s encode domain knowledge",
        "KF08 105.0s sample efficiency",
        "KF09 160.0s not magic",
    )

    def construct(self):
        background = make_background_network(seed=1106, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.6  Automotive CFD", max_width=3.15, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("domain knowledge turns geometry-sensitive CFD into learnable structure", max_width=8.7, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        car = make_car_mesh().move_to(LEFT * 4.35 + UP * 0.70)
        pressure = make_pressure_field().move_to(RIGHT * 4.00 + UP * 0.70)
        arrow = Arrow(car.get_right(), pressure.get_left(), buff=0.30, color=OPERATOR, stroke_width=3.0)
        sensitive = Chip("geometry + boundary sensitive", max_width=3.30, height=0.48, stroke_color=WARNING, font_size=17).move_to(DOWN * 0.80)
        discontinuity = SafeText("sharp features are hard without the right inductive bias", max_width=7.0, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 2.15)
        domain = Chip("domain-informed representation / basis", max_width=4.10, height=0.50, stroke_color=SCIENCE, font_size=17).move_to(DOWN * 2.15)
        sample = VGroup(
            Chip("hundreds of domain-aware samples", max_width=3.55, height=0.44, stroke_color=OUTPUT, font_size=15),
            Chip("not millions of generic examples", max_width=3.55, height=0.44, stroke_color=PURPLE, font_size=15),
        ).arrange(DOWN, buff=0.14).move_to(DOWN * 3.02)
        not_magic = SafeText("the gain comes from physics, geometry, and regularity assumptions", max_width=7.4, max_height=0.36, font_size=22, color=TEXT).move_to(DOWN * 3.38)
        assert_in_frame(VGroup(section_label, title, car, pressure, sample), margin=0.30, label="scene_11_06_layout")
        self.add(background)

        # Global 1:35:30.0 -> local 0.0; Global 1:35:43.0 -> local 13.0
        self.play_timed("geometry_mesh_flow_condition_input", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(car, shift=RIGHT * 0.05))

        # Global 1:35:43.0 -> local 13.0; Global 1:35:55.5 -> local 25.5
        self.play_timed("pressure_velocity_drag_output", 13.0, 25.5, Create(arrow), FadeIn(pressure, shift=LEFT * 0.05))

        # Global 1:35:55.5 -> local 25.5; Global 1:36:09.0 -> local 39.0
        self.play_timed("sensitive_to_geometry_boundary", 25.5, 39.0, FadeIn(sensitive, shift=UP * 0.04), Circumscribe(pressure[1], color=WARNING, buff=0.08))

        # Global 1:36:09.0 -> local 39.0; Global 1:36:10.0 -> local 40.0
        self.wait_timed("pause_before_discontinuity_question", 39.0, 40.0)

        # Global 1:36:10.0 -> local 40.0; Global 1:36:25.0 -> local 55.0
        self.play_timed("discontinuity_question", 40.0, 55.0, FadeIn(discontinuity, shift=UP * 0.04), Circumscribe(pressure, color=WARNING, buff=0.10))

        # Global 1:36:25.0 -> local 55.0; Global 1:36:40.0 -> local 70.0
        self.play_timed("hard_without_inductive_bias", 55.0, 70.0, pressure[0].curve.animate.set_stroke(width=4.5), Circumscribe(discontinuity, color=WARNING, buff=0.08))

        # Global 1:36:40.0 -> local 70.0; Global 1:36:57.0 -> local 87.0
        self.play_timed("encode_domain_expert_knowledge", 70.0, 87.0, FadeOut(discontinuity), FadeIn(domain, shift=UP * 0.04), Circumscribe(domain, color=SCIENCE, buff=0.08))

        # Global 1:36:57.0 -> local 87.0; Global 1:37:15.0 -> local 105.0
        self.play_timed("sample_efficiency_from_domain_knowledge", 87.0, 105.0, LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in sample], lag_ratio=0.12), Circumscribe(sample, color=OUTPUT, buff=0.08))

        # Global 1:37:15.0 -> local 105.0; Global 1:38:10.0 -> local 160.0
        self.play_timed("not_magic_architecture_matches_domain", 105.0, 137.0, FadeOut(domain), FadeIn(not_magic, shift=UP * 0.04), Circumscribe(VGroup(car, pressure), color=SCIENCE, buff=0.12))
        self.play_timed("final_cfd_read", 137.0, 159.8, Circumscribe(pressure[1], color=WARNING, buff=0.08), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
