"""
Scene 10.1 - Graph Neural Operator: learn the kernel directly
Script: ../docs/full_voice_manim_script.md
Global time: 1:07:40.0-1:10:10.0
Local duration: 150.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_kernel_formula, make_message_edges, make_point_cloud, make_wave_panel
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_gno_stage():
    point_cloud = make_point_cloud(n=30, width=5.1, height=3.0, seed=1001).move_to(LEFT * 3.65 + DOWN * 0.10)
    messages = make_message_edges(point_cloud, max_edges=8)
    query_label = SafeMathTex(r"y", max_width=0.5, max_height=0.30, font_size=28, color=OUTPUT)
    query_label.next_to(point_cloud.query, UR, buff=0.08)
    kernel_nn = Chip("kernel NN", max_width=1.55, height=0.50, stroke_color=OPERATOR, font_size=18)
    kernel_nn.move_to(RIGHT * 0.60 + UP * 1.35)
    pair_formula = make_kernel_formula(r"\kappa_\theta(y,x_j)", color=OPERATOR, max_width=2.65)
    pair_formula.next_to(kernel_nn, DOWN, buff=0.24)
    sum_formula = make_kernel_formula(r"v'(y)=\sum_j w_j\kappa_\theta(y,x_j)v(x_j)", color=SCIENCE, max_width=4.85)
    sum_formula.move_to(RIGHT * 3.20 + UP * 0.08)
    weights = VGroup(
        Chip("feature", max_width=1.05, height=0.42, stroke_color=INPUT, font_size=15),
        Chip("kernel value", max_width=1.55, height=0.42, stroke_color=OPERATOR, font_size=15),
        Chip("quadrature weight", max_width=2.15, height=0.42, stroke_color=SCIENCE, font_size=15),
    ).arrange(DOWN, buff=0.12)
    weights.next_to(sum_formula, DOWN, buff=0.30)
    metric_label = SafeText("graph comes from domain metric, not just data order", max_width=5.5, max_height=0.34, font_size=21, color=TEXT)
    metric_label.move_to(DOWN * 3.15)
    local = Chip("local radius", max_width=1.55, height=0.44, stroke_color=OPERATOR, font_size=16)
    global_kernel = Chip("global kernel", max_width=1.65, height=0.44, stroke_color=PURPLE, font_size=16)
    locality = VGroup(local, global_kernel).arrange(RIGHT, buff=0.36).move_to(RIGHT * 3.15 + DOWN * 2.05)
    compute = SafeText("accuracy improves with neighbors, but compute grows with edges", max_width=6.8, max_height=0.36, font_size=22, color=WARNING)
    compute.move_to(DOWN * 3.55)
    stage = VGroup(point_cloud, messages, query_label, kernel_nn, pair_formula, sum_formula, weights, metric_label, locality, compute)
    stage.point_cloud = point_cloud
    stage.messages = messages
    stage.query_label = query_label
    stage.kernel_nn = kernel_nn
    stage.pair_formula = pair_formula
    stage.sum_formula = sum_formula
    stage.weights = weights
    stage.metric_label = metric_label
    stage.locality = locality
    stage.compute = compute
    return stage


def make_refinement_strip():
    coarse = make_point_cloud(n=10, width=1.8, height=1.0, seed=13, color=MUTED)
    fine = make_point_cloud(n=25, width=1.8, height=1.0, seed=14, color=INPUT)
    continuum = make_wave_panel("same integral limit", color=OUTPUT, width=2.1, height=1.05)
    strip = VGroup(coarse, fine, continuum).arrange(RIGHT, buff=0.42)
    labels = VGroup(
        SafeText("coarse mesh", max_width=1.7, max_height=0.22, font_size=15, color=MUTED),
        SafeText("refined mesh", max_width=1.7, max_height=0.22, font_size=15, color=INPUT),
        SafeText("operator", max_width=1.6, max_height=0.22, font_size=15, color=OUTPUT),
    )
    for label, mob in zip(labels, strip):
        label.next_to(mob, DOWN, buff=0.08)
    group = VGroup(strip, labels).move_to(RIGHT * 2.15 + UP * 2.18)
    group.coarse = coarse
    group.fine = fine
    group.continuum = continuum
    return group


class Scene1001GraphNeuralOperator(TimedScene):
    SCRIPT_ID = "10.1"
    SCRIPT_TITLE = "Graph Neural Operator: learn the kernel directly"
    SCRIPT_START = 67 * 60 + 40
    SCRIPT_END = 70 * 60 + 10
    SCENE_DURATION = 150.0

    KEYFRAMES = (
        "KF01 0.0s kernel NN parameterizes kappa",
        "KF02 13.5s compute message from x to y",
        "KF03 28.0s quadrature sum",
        "KF04 41.5s GNO label",
        "KF05 56.0s graph from metric space",
        "KF06 70.0s mesh refinement limit",
        "KF07 87.0s local versus global kernels",
        "KF08 150.0s compute trade-off",
    )

    def construct(self):
        background = make_background_network(seed=1001, n=70, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.1  Graph Neural Operator", max_width=3.35, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        stage = make_gno_stage()
        refinement = make_refinement_strip()
        title = SafeText("learn the kernel directly", max_width=4.2, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.52)
        gno_badge = Chip("kernel neural operator", max_width=2.40, height=0.48, stroke_color=SCIENCE, font_size=17)
        gno_badge.next_to(title, DOWN, buff=0.18)
        assert_in_frame(VGroup(section_label, title, stage.point_cloud, stage.sum_formula, stage.weights), margin=0.30, label="scene_10_01_initial")
        self.add(background)

        # Global 1:07:40.0 -> local 0.0; Global 1:07:53.5 -> local 13.5
        self.play_timed(
            "parameterize_kernel_by_nn",
            0.0,
            13.5,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(title, shift=DOWN * 0.05),
            FadeIn(stage.point_cloud, shift=RIGHT * 0.05),
            FadeIn(stage.kernel_nn, shift=DOWN * 0.06),
            FadeIn(stage.pair_formula, shift=DOWN * 0.04),
        )

        # Global 1:07:53.5 -> local 13.5; Global 1:08:08.0 -> local 28.0
        self.play_timed(
            "messages_to_query_node",
            13.5,
            28.0,
            FadeIn(stage.query_label, shift=UP * 0.03),
            LaggedStart(*[Create(edge) for edge in stage.messages], lag_ratio=0.10),
            Circumscribe(stage.point_cloud.query, color=OUTPUT, buff=0.08),
        )

        # Global 1:08:08.0 -> local 28.0; Global 1:08:09.0 -> local 29.0
        self.wait_timed("pause_after_message_recipe", 28.0, 29.0)

        # Global 1:08:09.0 -> local 29.0; Global 1:08:21.5 -> local 41.5
        self.play_timed(
            "name_gno_kernel_neural_operator",
            29.0,
            41.5,
            FadeIn(stage.sum_formula, shift=LEFT * 0.05),
            FadeIn(stage.weights, shift=UP * 0.04),
            FadeIn(gno_badge, shift=DOWN * 0.04),
        )

        # Global 1:08:21.5 -> local 41.5; Global 1:08:36.0 -> local 56.0
        self.play_timed(
            "metric_space_graph_not_sequence",
            41.5,
            56.0,
            FadeIn(stage.metric_label, shift=UP * 0.05),
            stage.point_cloud.lines.animate.set_stroke(opacity=0.85, width=1.5),
            Circumscribe(stage.point_cloud.radius, color=OPERATOR, buff=0.04),
        )

        # Global 1:08:36.0 -> local 56.0; Global 1:08:50.0 -> local 70.0
        self.play_timed(
            "mesh_refinement_same_integral_operator",
            56.0,
            70.0,
            FadeIn(refinement, shift=DOWN * 0.05),
            stage.point_cloud.dots.animate.set_opacity(0.72),
        )

        # Global 1:08:50.0 -> local 70.0; Global 1:09:07.0 -> local 87.0
        self.play_timed(
            "local_vs_global_kernel",
            70.0,
            87.0,
            FadeIn(stage.locality, shift=UP * 0.04),
            stage.point_cloud.radius.animate.scale(1.35).set_stroke(color=PURPLE, opacity=0.62),
            Circumscribe(stage.locality, color=PURPLE, buff=0.08),
        )

        # Global 1:09:07.0 -> local 87.0; Global 1:10:10.0 -> local 150.0
        self.play_timed(
            "compute_tradeoff_hold",
            87.0,
            124.0,
            FadeIn(stage.compute, shift=UP * 0.05),
            stage.messages.animate.set_stroke(width=2.6, opacity=0.82),
        )
        self.play_timed(
            "final_readable_gno_summary",
            124.0,
            149.8,
            Circumscribe(VGroup(stage.sum_formula, stage.locality), color=SCIENCE, buff=0.10),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
