"""
Scene 10.2 - Basis projection: integrate by changing representation
Script: ../docs/full_voice_manim_script.md
Global time: 1:10:10.0-1:12:20.0
Local duration: 130.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_coefficient_bars, make_kernel_formula, make_wave_panel
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_basis_functions():
    funcs = VGroup()
    for index, color in enumerate((INPUT, OPERATOR, PURPLE, OUTPUT)):
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 1, 1],
            x_length=1.45,
            y_length=0.62,
            tips=False,
            axis_config={"color": GRID, "stroke_width": 0.7, "include_ticks": False},
        )
        curve = axes.plot(lambda x, k=index + 1: 0.65 * np.sin(k * x), x_range=[0, 4], color=color, stroke_width=2.0)
        funcs.add(VGroup(axes, curve))
    funcs.arrange(DOWN, buff=0.12)
    label = SafeText("basis functions", max_width=2.2, max_height=0.28, font_size=18, color=TEXT)
    label.next_to(funcs, DOWN, buff=0.12)
    group = VGroup(funcs, label)
    group.functions = funcs
    return group


def make_basis_pipeline():
    physical = make_wave_panel("physical field", color=INPUT, width=2.7, height=1.42).move_to(LEFT * 5.25 + UP * 0.05)
    basis = make_basis_functions().move_to(LEFT * 1.80 + UP * 0.10)
    coefficients = make_coefficient_bars([0.85, -0.50, 0.35, 0.22, -0.16, 0.10], color=PURPLE).move_to(RIGHT * 1.35 + UP * 0.10)
    coef_label = SafeText("coefficient space", max_width=2.6, max_height=0.28, font_size=18, color=PURPLE)
    coef_label.next_to(coefficients, DOWN, buff=0.12)
    reconstruction = make_wave_panel("reconstruction", color=OUTPUT, width=2.7, height=1.42).move_to(RIGHT * 5.25 + UP * 0.05)
    arrows = VGroup(
        Arrow(physical.get_right(), basis.get_left(), buff=0.20, color=GRID, stroke_width=2.3),
        Arrow(basis.get_right(), coefficients.get_left(), buff=0.20, color=GRID, stroke_width=2.3),
        Arrow(coefficients.get_right(), reconstruction.get_left(), buff=0.20, color=GRID, stroke_width=2.3),
    )
    residual = CurvedArrow(physical.get_bottom(), reconstruction.get_bottom(), angle=-TAU / 5, color=OUTPUT, stroke_width=2.4)
    residual_label = Chip("residual skip", max_width=1.55, height=0.42, stroke_color=OUTPUT, font_size=15)
    residual_label.move_to(DOWN * 2.05)
    group = VGroup(physical, basis, coefficients, coef_label, reconstruction, arrows, residual, residual_label)
    group.physical = physical
    group.basis = basis
    group.coefficients = coefficients
    group.coef_label = coef_label
    group.reconstruction = reconstruction
    group.arrows = arrows
    group.residual = residual
    group.residual_label = residual_label
    return group


def make_basis_menu():
    chips = VGroup(
        Chip("Fourier", max_width=1.20, height=0.42, stroke_color=OPERATOR, font_size=15),
        Chip("wavelet", max_width=1.20, height=0.42, stroke_color=SCIENCE, font_size=15),
        Chip("PCA", max_width=0.82, height=0.42, stroke_color=PURPLE, font_size=15),
        Chip("Laplacian eigenbasis", max_width=2.20, height=0.42, stroke_color=INPUT, font_size=15),
        Chip("learned basis", max_width=1.60, height=0.42, stroke_color=OUTPUT, font_size=15),
    ).arrange(RIGHT, buff=0.20)
    chips.move_to(DOWN * 3.22)
    return chips


class Scene1002BasisProjection(TimedScene):
    SCRIPT_ID = "10.2"
    SCRIPT_TITLE = "Basis projection: integrate by changing representation"
    SCRIPT_START = 70 * 60 + 10
    SCRIPT_END = 72 * 60 + 20
    SCENE_DURATION = 130.0

    KEYFRAMES = (
        "KF01 0.0s physical-space kernel alternative",
        "KF02 12.0s project into basis",
        "KF03 24.5s manipulate coefficients",
        "KF04 37.0s reconstruct function",
        "KF05 53.5s mode truncation warning",
        "KF06 68.0s residual skip",
        "KF07 86.0s basis menu",
        "KF08 130.0s basis encodes assumptions",
    )

    def construct(self):
        background = make_background_network(seed=1002, n=68, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.2  Basis projection", max_width=3.10, height=0.42, stroke_color=PURPLE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("integrate by changing representation", max_width=6.4, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        pipeline = make_basis_pipeline()
        formula = make_kernel_formula(r"a(x)\rightarrow \{c_k\}\rightarrow \tilde{c}_k\rightarrow u(x)", color=PURPLE, max_width=5.65)
        formula.move_to(UP * 2.58)
        warning = SafeText("truncation can erase sharp or rare information", max_width=6.3, max_height=0.36, font_size=22, color=WARNING)
        warning.move_to(DOWN * 2.70)
        menu = make_basis_menu()
        assumption = SafeText("the basis encodes geometry, domain, and regularity", max_width=6.2, max_height=0.36, font_size=22, color=SCIENCE)
        assumption.move_to(DOWN * 2.68)
        assert_in_frame(VGroup(section_label, title, pipeline, menu), margin=0.30, label="scene_10_02_layout")
        self.add(background)

        # Global 1:10:10.0 -> local 0.0; Global 1:10:22.0 -> local 12.0
        self.play_timed(
            "physical_space_direct_kernel_alternative",
            0.0,
            12.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(title, shift=DOWN * 0.05),
            FadeIn(pipeline.physical, shift=RIGHT * 0.05),
        )

        # Global 1:10:22.0 -> local 12.0; Global 1:10:34.5 -> local 24.5
        self.play_timed(
            "project_to_basis_functions",
            12.0,
            24.5,
            Create(pipeline.arrows[0]),
            LaggedStart(*[FadeIn(func, shift=UP * 0.04) for func in pipeline.basis.functions], lag_ratio=0.15),
            FadeIn(pipeline.basis[-1], shift=UP * 0.03),
        )

        # Global 1:10:34.5 -> local 24.5; Global 1:10:47.0 -> local 37.0
        self.play_timed(
            "manipulate_coefficients",
            24.5,
            37.0,
            Create(pipeline.arrows[1]),
            FadeIn(pipeline.coefficients, shift=UP * 0.04),
            FadeIn(pipeline.coef_label, shift=UP * 0.03),
        )

        # Global 1:10:47.0 -> local 37.0; Global 1:10:48.0 -> local 38.0
        self.wait_timed("pause_after_basis_recipe", 37.0, 38.0)

        # Global 1:10:48.0 -> local 38.0; Global 1:11:03.5 -> local 53.5
        self.play_timed(
            "reconstruct_and_show_formula",
            38.0,
            53.5,
            Create(pipeline.arrows[2]),
            FadeIn(pipeline.reconstruction, shift=LEFT * 0.05),
            FadeIn(formula, shift=DOWN * 0.04),
        )

        # Global 1:11:03.5 -> local 53.5; Global 1:11:18.0 -> local 68.0
        self.play_timed(
            "mode_truncation_warning",
            53.5,
            68.0,
            FadeIn(warning, shift=UP * 0.04),
            pipeline.coefficients[1][4:].animate.set_fill(opacity=0.18).set_stroke(opacity=0.35),
            Circumscribe(pipeline.coefficients, color=WARNING, buff=0.08),
        )

        # Global 1:11:18.0 -> local 68.0; Global 1:11:36.0 -> local 86.0
        self.play_timed(
            "residual_skip_keeps_physical_path",
            68.0,
            86.0,
            FadeOut(warning),
            Create(pipeline.residual),
            FadeIn(pipeline.residual_label, shift=UP * 0.04),
            Circumscribe(pipeline.residual_label, color=OUTPUT, buff=0.08),
        )

        # Global 1:11:36.0 -> local 86.0; Global 1:12:20.0 -> local 130.0
        self.play_timed(
            "basis_examples_and_assumptions",
            86.0,
            112.0,
            LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in menu], lag_ratio=0.10),
            FadeIn(assumption, shift=UP * 0.04),
        )
        self.play_timed(
            "final_basis_read",
            112.0,
            129.8,
            Circumscribe(VGroup(pipeline.basis, menu), color=SCIENCE, buff=0.10),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
