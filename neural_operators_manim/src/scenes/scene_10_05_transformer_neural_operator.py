"""
Scene 10.5 - Transformer Neural Operator
Script: ../docs/full_voice_manim_script.md
Global time: 1:18:20.0-1:20:30.0
Local duration: 130.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_attention_matrix, make_kernel_formula, make_point_cloud
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_attention_operator_stage():
    samples = make_point_cloud(n=18, width=3.0, height=2.1, seed=1005, color=INPUT).move_to(LEFT * 5.10 + UP * 0.25)
    matrix = make_attention_matrix(size=6, cell=0.34).move_to(LEFT * 1.15 + UP * 0.35)
    integral = make_kernel_formula(r"v(y)=\int_D \alpha(y,x)v(x)\,d\mu(x)", color=SCIENCE, max_width=4.85).move_to(RIGHT * 3.65 + UP * 0.50)
    qkv = VGroup(
        Chip("Q(x)", max_width=0.80, height=0.40, stroke_color=PURPLE, font_size=15),
        Chip("K(x)", max_width=0.80, height=0.40, stroke_color=OPERATOR, font_size=15),
        Chip("V(x)", max_width=0.80, height=0.40, stroke_color=OUTPUT, font_size=15),
    ).arrange(RIGHT, buff=0.18)
    qkv.next_to(integral, DOWN, buff=0.34)
    arrows = VGroup(
        Arrow(samples.get_right(), matrix.get_left(), buff=0.20, color=GRID, stroke_width=2.2),
        Arrow(matrix.get_right(), integral.get_left(), buff=0.20, color=GRID, stroke_width=2.2),
    )
    stage = VGroup(samples, matrix, integral, qkv, arrows)
    stage.samples = samples
    stage.matrix = matrix
    stage.integral = integral
    stage.qkv = qkv
    stage.arrows = arrows
    return stage


def make_grid_weight_comparison():
    regular = Chip("regular grid: equal weights", max_width=3.0, height=0.46, stroke_color=INPUT, font_size=16)
    irregular = Chip("irregular grid: measure factors", max_width=3.35, height=0.46, stroke_color=WARNING, font_size=16)
    group = VGroup(regular, irregular).arrange(DOWN, buff=0.18).move_to(DOWN * 2.30)
    group.regular = regular
    group.irregular = irregular
    return group


class Scene1005TransformerNeuralOperator(TimedScene):
    SCRIPT_ID = "10.5"
    SCRIPT_TITLE = "Transformer Neural Operator"
    SCRIPT_START = 78 * 60 + 20
    SCRIPT_END = 80 * 60 + 30
    SCENE_DURATION = 130.0

    KEYFRAMES = (
        "KF01 0.0s attention weighted sum",
        "KF02 13.0s tokens as samples",
        "KF03 26.0s integral approximation",
        "KF04 40.0s pause",
        "KF05 57.0s regular grid weights cancel",
        "KF06 71.0s irregular weights matter",
        "KF07 88.0s copying finite ML fails",
        "KF08 130.0s attention as function-space operator",
    )

    def construct(self):
        background = make_background_network(seed=1005, n=70, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.5  Transformer Neural Operator", max_width=4.05, height=0.42, stroke_color=PURPLE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("attention becomes an integral-like operator", max_width=6.3, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        stage = make_attention_operator_stage()
        matrix_caption = SafeText("attention weights become quadrature-like coefficients", max_width=5.8, max_height=0.32, font_size=20, color=OPERATOR)
        matrix_caption.move_to(DOWN * 1.20)
        comparison = make_grid_weight_comparison()
        warning = SafeText("copying finite-dimensional attention can lose continuum meaning", max_width=7.2, max_height=0.36, font_size=22, color=WARNING)
        warning.move_to(DOWN * 3.33)
        final = Chip("attention on function space", max_width=3.10, height=0.50, stroke_color=SCIENCE, font_size=18).move_to(DOWN * 1.36)
        assert_in_frame(VGroup(section_label, title, stage, matrix_caption, comparison, warning), margin=0.30, label="scene_10_05_layout")
        self.add(background)

        # Global 1:18:20.0 -> local 0.0; Global 1:18:33.0 -> local 13.0
        self.play_timed("attention_weighted_sum", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(stage.matrix, shift=UP * 0.04), FadeIn(matrix_caption, shift=UP * 0.03))

        # Global 1:18:33.0 -> local 13.0; Global 1:18:46.0 -> local 26.0
        self.play_timed("function_samples_as_tokens", 13.0, 26.0, FadeIn(stage.samples, shift=RIGHT * 0.05), Create(stage.arrows[0]), FadeIn(stage.qkv, shift=UP * 0.04))

        # Global 1:18:46.0 -> local 26.0; Global 1:19:00.0 -> local 40.0
        self.play_timed("attention_integral_approximation", 26.0, 40.0, Create(stage.arrows[1]), FadeIn(stage.integral, shift=LEFT * 0.05))

        # Global 1:19:00.0 -> local 40.0; Global 1:19:01.0 -> local 41.0
        self.wait_timed("pause_after_attention_integral", 40.0, 41.0)

        # Global 1:19:01.0 -> local 41.0; Global 1:19:17.0 -> local 57.0
        self.play_timed("regular_grid_weights_cancel", 41.0, 57.0, FadeOut(matrix_caption), FadeIn(comparison.regular, shift=UP * 0.04), Circumscribe(comparison.regular, color=INPUT, buff=0.07))

        # Global 1:19:17.0 -> local 57.0; Global 1:19:31.0 -> local 71.0
        self.play_timed("irregular_resolution_measure_factors", 57.0, 71.0, FadeIn(comparison.irregular, shift=UP * 0.04), Circumscribe(comparison.irregular, color=WARNING, buff=0.07))

        # Global 1:19:31.0 -> local 71.0; Global 1:19:48.0 -> local 88.0
        self.play_timed("finite_ml_copy_warning", 71.0, 88.0, FadeIn(warning, shift=UP * 0.04), stage.matrix.cells.animate.set_opacity(0.82))

        # Global 1:19:48.0 -> local 88.0; Global 1:20:30.0 -> local 130.0
        self.play_timed("attention_as_operator", 88.0, 112.0, FadeIn(final, shift=UP * 0.04), Circumscribe(stage.integral, color=SCIENCE, buff=0.08))
        self.play_timed("final_tno_read", 112.0, 129.8, Circumscribe(VGroup(stage.matrix, stage.integral, comparison), color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
