"""
Scene 10.4 - Numerical-analysis family: quadrature, Galerkin, multigrid, U-NO
Script: ../docs/full_voice_manim_script.md
Global time: 1:15:40.0-1:18:20.0
Local duration: 160.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_coefficient_bars, make_kernel_formula, make_wave_panel
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard, PanelGrid
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_quadrature_panel():
    dots = VGroup(*[Dot(LEFT * 1.2 + RIGHT * 0.48 * i + UP * (0.18 * (-1) ** i), radius=0.055, color=INPUT) for i in range(6)])
    weights = VGroup(*[Circle(radius=0.13 + 0.035 * (i % 3), color=OPERATOR, stroke_width=1.1).move_to(dot) for i, dot in enumerate(dots)])
    formula = make_kernel_formula(r"\sum_j w_j f(x_j)", color=OPERATOR, max_width=2.65)
    formula.next_to(dots, DOWN, buff=0.20)
    return PanelCard("quadrature", VGroup(dots, weights, formula), width=3.25, height=2.28, accent_color=OPERATOR)


def make_galerkin_panel():
    basis = make_coefficient_bars([0.8, -0.45, 0.30, 0.18], color=PURPLE, width=2.3, height=1.0)
    subspace = Chip("finite subspace", max_width=1.80, height=0.38, stroke_color=PURPLE, font_size=14)
    subspace.next_to(basis, DOWN, buff=0.16)
    return PanelCard("Galerkin", VGroup(basis, subspace), width=3.25, height=2.28, accent_color=PURPLE)


def make_vcycle_panel():
    levels = VGroup(
        Line(LEFT * 1.1 + UP * 0.65, LEFT * 0.35 + DOWN * 0.10, color=SCIENCE, stroke_width=2.3),
        Line(LEFT * 0.35 + DOWN * 0.10, ORIGIN + DOWN * 0.58, color=SCIENCE, stroke_width=2.3),
        Line(ORIGIN + DOWN * 0.58, RIGHT * 0.35 + DOWN * 0.10, color=SCIENCE, stroke_width=2.3),
        Line(RIGHT * 0.35 + DOWN * 0.10, RIGHT * 1.1 + UP * 0.65, color=SCIENCE, stroke_width=2.3),
    )
    for point in (LEFT * 1.1 + UP * 0.65, LEFT * 0.35 + DOWN * 0.10, ORIGIN + DOWN * 0.58, RIGHT * 0.35 + DOWN * 0.10, RIGHT * 1.1 + UP * 0.65):
        levels.add(Dot(point, radius=0.055, color=OUTPUT))
    label = SafeText("near + far scales", max_width=2.2, max_height=0.24, font_size=16, color=SCIENCE)
    label.next_to(levels, DOWN, buff=0.16)
    return PanelCard("multigrid", VGroup(levels, label), width=3.25, height=2.28, accent_color=SCIENCE)


def make_uno_panel():
    blocks = VGroup()
    sizes = [1.05, 0.78, 0.52, 0.78, 1.05]
    for i, size in enumerate(sizes):
        block = RoundedRectangle(
            width=0.56,
            height=size,
            corner_radius=0.06,
            stroke_color=OUTPUT,
            stroke_width=1.1,
            fill_color=OUTPUT,
            fill_opacity=0.18,
        )
        block.shift(RIGHT * (i - 2) * 0.62)
        blocks.add(block)
    arrows = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.06, color=GRID, stroke_width=1.3) for i in range(4)])
    label = SafeText("contract -> expand", max_width=2.6, max_height=0.24, font_size=15, color=OUTPUT)
    label.next_to(blocks, DOWN, buff=0.16)
    return PanelCard("U-NO", VGroup(blocks, arrows, label), width=3.25, height=2.28, accent_color=OUTPUT)


def make_numerical_family_grid():
    panels = [make_quadrature_panel(), make_galerkin_panel(), make_vcycle_panel(), make_uno_panel()]
    grid = PanelGrid(panels, rows=2, cols=2, width=7.1, height=5.0, buff=0.30).move_to(LEFT * 3.75 + DOWN * 0.15)
    return grid


class Scene1004NumericalAnalysisFamily(TimedScene):
    SCRIPT_ID = "10.4"
    SCRIPT_TITLE = "Numerical-analysis family: quadrature, Galerkin, multigrid, U-NO"
    SCRIPT_START = 75 * 60 + 40
    SCRIPT_END = 78 * 60 + 20
    SCENE_DURATION = 160.0

    KEYFRAMES = (
        "KF01 0.0s integration has history",
        "KF02 13.0s quadrature weights",
        "KF03 26.0s Galerkin subspaces",
        "KF04 38.0s pause and full family",
        "KF05 52.0s multigrid",
        "KF06 69.0s U-NO",
        "KF07 85.0s hidden domain contraction",
        "KF08 99.0s rewrite DL architecture",
    )

    def construct(self):
        background = make_background_network(seed=1004, n=74, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.4  Numerical-analysis family", max_width=4.15, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("old numerical ideas become neural-operator design tools", max_width=8.0, max_height=0.42, font_size=28, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        family_grid = make_numerical_family_grid()
        focus = make_wave_panel("operator-learning rewrite", color=OUTPUT, width=4.4, height=2.10).move_to(RIGHT * 3.85 + UP * 0.40)
        formula = make_kernel_formula(r"\text{architecture bias} \neq \text{copy finite ML}", color=OPERATOR, max_width=5.15)
        formula.move_to(RIGHT * 3.85 + DOWN * 1.40)
        note = SafeText("quadrature, basis, scale, and geometry must remain visible", max_width=6.0, max_height=0.34, font_size=21, color=SCIENCE)
        note.move_to(DOWN * 3.38)
        assert_in_frame(VGroup(section_label, title, family_grid, focus, formula, note), margin=0.30, label="scene_10_04_layout")
        self.add(background)

        # Global 1:15:40.0 -> local 0.0; Global 1:15:53.0 -> local 13.0
        self.play_timed("integration_history", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(family_grid[0], shift=UP * 0.04))

        # Global 1:15:53.0 -> local 13.0; Global 1:16:06.0 -> local 26.0
        self.play_timed("quadrature_weights", 13.0, 26.0, Circumscribe(family_grid[0], color=OPERATOR, buff=0.06), FadeIn(focus, shift=LEFT * 0.05))

        # Global 1:16:06.0 -> local 26.0; Global 1:16:18.0 -> local 38.0
        self.play_timed("galerkin_projection", 26.0, 38.0, FadeIn(family_grid[1], shift=UP * 0.04), Circumscribe(family_grid[1], color=PURPLE, buff=0.06))

        # Global 1:16:18.0 -> local 38.0; Global 1:16:32.0 -> local 52.0
        self.play_timed("show_family_after_pause", 38.0, 52.0, FadeIn(family_grid[2], shift=UP * 0.04), FadeIn(family_grid[3], shift=UP * 0.04))

        # Global 1:16:32.0 -> local 52.0; Global 1:16:49.0 -> local 69.0
        self.play_timed("multigrid_near_far", 52.0, 69.0, Circumscribe(family_grid[2], color=SCIENCE, buff=0.06), focus.curve.animate.set_stroke(width=4.1))

        # Global 1:16:49.0 -> local 69.0; Global 1:17:05.0 -> local 85.0
        self.play_timed("uno_multipole_style", 69.0, 85.0, Circumscribe(family_grid[3], color=OUTPUT, buff=0.06), FadeIn(formula, shift=UP * 0.04))

        # Global 1:17:05.0 -> local 85.0; Global 1:17:19.0 -> local 99.0
        self.play_timed("hidden_domain_contraction_expansion", 85.0, 99.0, family_grid[3].animate.set_opacity(0.96), Circumscribe(focus, color=OUTPUT, buff=0.08))

        # Global 1:17:19.0 -> local 99.0; Global 1:18:20.0 -> local 160.0
        self.play_timed("rewrite_deep_learning_architecture", 99.0, 134.0, FadeIn(note, shift=UP * 0.04), Circumscribe(formula, color=OPERATOR, buff=0.08))
        self.play_timed("final_numerical_family_read", 134.0, 159.8, Circumscribe(family_grid, color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
