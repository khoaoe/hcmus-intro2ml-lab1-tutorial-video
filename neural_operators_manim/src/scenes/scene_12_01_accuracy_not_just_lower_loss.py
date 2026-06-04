"""
Scene 12.1 - Accuracy is not just lower loss
Script: ../docs/full_voice_manim_script.md
Global time: 1:41:40.0-1:44:05.0
Local duration: 145.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.open_problem_visuals import make_loss_bar, make_metric_gauges, make_problem_formulation_card, make_rare_event_miss
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "MSE low",
    "rare event missed",
    "anomaly correlation",
    "energy spectrum",
    "drag coefficient",
    "mass conservation",
    "PDE residual",
    "calibration error",
    "problem formulation",
)


class Scene1201AccuracyNotJustLowerLoss(TimedScene):
    SCRIPT_ID = "12.1"
    SCRIPT_TITLE = "Accuracy is not just lower loss"
    SCRIPT_START = 101 * 60 + 40
    SCRIPT_END = 104 * 60 + 5
    SCENE_DURATION = 145.0

    KEYFRAMES = (
        "KF01 0.0s absolute accuracy question",
        "KF02 13.0s small scientific errors accumulate",
        "KF03 26.5s low L2 misses rare event",
        "KF04 39.0s pause",
        "KF05 55.5s domain metric gauges",
        "KF06 72.0s metric research question",
        "KF07 93.0s MSE can miss spectra boundaries invariants",
        "KF08 145.0s loss becomes problem formulation",
    )

    def construct(self):
        background = make_background_network(seed=1201, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("12.1  Accuracy is not just lower loss", max_width=4.75, height=0.42, stroke_color=WARNING, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("accuracy must become domain-meaningful, not just benchmark-relative", max_width=8.7, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        loss = make_loss_bar().move_to(LEFT * 4.25 + UP * 0.90)
        rare = make_rare_event_miss().move_to(RIGHT * 4.15 + UP * 0.90)
        gauges = make_metric_gauges(("anomaly corr.", "energy spectrum", "drag coeff.", "mass conserved", "PDE residual", "calibration err.")).move_to(DOWN * 1.25)
        question = SafeText("which metric reflects the value of prediction?", max_width=6.2, max_height=0.34, font_size=22, color=SCIENCE).move_to(DOWN * 2.95)
        failure = SafeText("pretty MSE can still miss spectrum, boundary, or invariant", max_width=7.1, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.34)
        formulation = make_problem_formulation_card().move_to(DOWN * 1.20)
        assert_in_frame(VGroup(section_label, title, loss, rare, gauges, failure), margin=0.30, label="scene_12_01_layout")
        self.add(background)

        # Global 1:41:40.0 -> local 0.0; Global 1:41:53.0 -> local 13.0
        self.play_timed("absolute_accuracy_question", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(loss, shift=UP * 0.04))

        # Global 1:41:53.0 -> local 13.0; Global 1:42:06.5 -> local 26.5
        self.play_timed("small_pattern_errors_accumulate", 13.0, 26.5, FadeIn(rare, shift=UP * 0.04), Circumscribe(rare.spike, color=WARNING, buff=0.08))

        # Global 1:42:06.5 -> local 26.5; Global 1:42:19.0 -> local 39.0
        self.play_timed("low_l2_misses_rare_event", 26.5, 39.0, Circumscribe(VGroup(loss, rare), color=WARNING, buff=0.10), loss.bar.animate.set_fill(opacity=0.92))

        # Global 1:42:19.0 -> local 39.0; Global 1:42:20.0 -> local 40.0
        self.wait_timed("pause_before_domain_metrics", 39.0, 40.0)

        # Global 1:42:20.0 -> local 40.0; Global 1:42:35.5 -> local 55.5
        self.play_timed("domain_specific_metric_gauges", 40.0, 55.5, LaggedStart(*[FadeIn(gauge, shift=UP * 0.04) for gauge in gauges], lag_ratio=0.08))

        # Global 1:42:35.5 -> local 55.5; Global 1:42:52.0 -> local 72.0
        self.play_timed("metric_research_question", 55.5, 72.0, FadeIn(question, shift=UP * 0.04), Circumscribe(gauges, color=SCIENCE, buff=0.08))

        # Global 1:42:52.0 -> local 72.0; Global 1:43:13.0 -> local 93.0
        self.play_timed("mse_misses_physical_failures", 72.0, 93.0, FadeOut(question), FadeIn(failure, shift=UP * 0.04), Circumscribe(rare, color=WARNING, buff=0.08))

        # Global 1:43:13.0 -> local 93.0; Global 1:44:05.0 -> local 145.0
        self.play_timed("loss_becomes_problem_formulation", 93.0, 122.0, FadeOut(gauges), FadeOut(failure), ReplacementTransform(loss.copy(), formulation), FadeOut(rare))
        self.play_timed("final_accuracy_read", 122.0, 144.8, Circumscribe(formulation, color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
