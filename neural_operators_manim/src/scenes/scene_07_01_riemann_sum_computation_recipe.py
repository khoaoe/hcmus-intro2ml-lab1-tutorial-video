"""
Scene 7.1 - Riemann sum as a computation recipe
Script: ../docs/full_voice_manim_script.md
Global time: 42:30.0-44:20.0
Local duration: 110.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip, make_formula_badge
from src.common.safe_text import SafeMathTex
from src.common.theme import (
    apply_global_config,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    SCIENCE,
    TEXT,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame, assert_no_group_overlap


apply_global_config()


DOMAIN_START = 0.0
DOMAIN_END = 6.0
COARSE_EDGES = np.linspace(DOMAIN_START, DOMAIN_END, 7)
FINE_EDGES = np.linspace(DOMAIN_START, DOMAIN_END, 15)
ALT_EDGES = np.linspace(DOMAIN_START, DOMAIN_END, 10)
NONUNIFORM_EDGES = np.array([0.0, 0.38, 1.02, 1.78, 2.24, 3.05, 4.10, 4.55, 5.34, 6.0])
RIGHT_FORMULA_CENTER = RIGHT * 4.65
INITIAL_FORMULA_OFFSET = UP * 0.15
FINAL_WEIGHTED_FORMULA_OFFSET = UP * 0.92
TEASER_OFFSET = DOWN * 1.15


def sample_function(x):
    return 1.13 + 0.42 * np.sin(1.05 * x - 0.25) + 0.18 * np.cos(2.25 * x + 0.45)


def make_riemann_stage():
    axes = Axes(
        x_range=[DOMAIN_START, DOMAIN_END, 1],
        y_range=[0, 2.05, 0.5],
        x_length=8.0,
        y_length=4.25,
        tips=False,
        axis_config={
            "color": MUTED,
            "stroke_width": 1.15,
            "include_ticks": False,
        },
    )
    axes.move_to(LEFT * 2.55 + UP * 0.28)

    graph = axes.plot(sample_function, x_range=[DOMAIN_START, DOMAIN_END], color=INPUT, stroke_width=3.2)
    exact_area = axes.get_area(
        graph,
        x_range=[DOMAIN_START, DOMAIN_END],
        color=INPUT,
        opacity=0.18,
    )
    baseline = Line(axes.c2p(DOMAIN_START, 0), axes.c2p(DOMAIN_END, 0), color=GRID, stroke_width=1.1)
    stage = VGroup(axes, baseline, exact_area, graph)
    stage.axes = axes
    stage.graph = graph
    stage.exact_area = exact_area
    stage.baseline = baseline
    return stage


def _rectangle_for_interval(axes, left, right, color=OUTPUT, opacity=0.32):
    midpoint = 0.5 * (left + right)
    height = sample_function(midpoint)
    rectangle = Polygon(
        axes.c2p(left, 0),
        axes.c2p(right, 0),
        axes.c2p(right, height),
        axes.c2p(left, height),
        stroke_color=color,
        stroke_width=1.05,
        fill_color=color,
        fill_opacity=opacity,
    )
    rectangle.sample_x = midpoint
    rectangle.cell_width = right - left
    return rectangle


def make_uniform_rectangles(axes, edges=COARSE_EDGES, color=OUTPUT, opacity=0.32):
    return VGroup(*[_rectangle_for_interval(axes, float(edges[i]), float(edges[i + 1]), color, opacity) for i in range(len(edges) - 1)])


def make_nonuniform_rectangles(axes, edges=NONUNIFORM_EDGES):
    rectangles = VGroup()
    for i in range(len(edges) - 1):
        rectangles.add(_rectangle_for_interval(axes, float(edges[i]), float(edges[i + 1]), OPERATOR, 0.34))
    return rectangles


def make_sample_dots(axes, sample_positions, color=SCIENCE, radius=0.052):
    return VGroup(*[Dot(axes.c2p(float(x), sample_function(float(x))), radius=radius, color=color) for x in sample_positions])


def make_recipe_callouts(axes):
    example_left = float(COARSE_EDGES[2])
    example_right = float(COARSE_EDGES[3])
    sample_x = 0.5 * (example_left + example_right)
    sample_y = sample_function(sample_x)
    height_line = Line(axes.c2p(sample_x, 0), axes.c2p(sample_x, sample_y), color=NVIDIA_GREEN, stroke_width=3.0)
    height_label = Chip("height = f(x_i)", max_width=2.18, height=0.43, stroke_color=NVIDIA_GREEN, font_size=17)
    height_label.next_to(height_line, RIGHT, buff=0.16)
    width_line = Line(axes.c2p(example_left, 0), axes.c2p(example_right, 0), color=OPERATOR, stroke_width=3.0)
    # Visual label: width = \Delta x
    width_label = Chip("width = \\Delta x", max_width=1.82, height=0.43, stroke_color=OPERATOR, font_size=17)
    width_label.next_to(width_line, DOWN, buff=0.14)
    return VGroup(height_line, height_label, width_line, width_label)


def make_formula_sequence():
    integral = make_formula_badge(r"\int_D f(x)\,dx", max_width=3.15, height=0.66, stroke_color=INPUT, font_size=30)
    uniform_sum = make_formula_badge(r"\sum_i f(x_i)\,\Delta x_i", max_width=3.70, height=0.66, stroke_color=OUTPUT, font_size=30)
    weighted_sum = make_formula_badge(r"\sum_i f(x_i)\,w_i \approx \int_D f(x)\,dx", max_width=5.70, height=0.72, stroke_color=NVIDIA_GREEN, font_size=30)
    group = VGroup(integral, uniform_sum, weighted_sum).arrange(DOWN, buff=0.22)
    group.move_to(RIGHT_FORMULA_CENTER + INITIAL_FORMULA_OFFSET)
    group.integral = integral
    group.uniform_sum = uniform_sum
    group.weighted_sum = weighted_sum
    return group


def make_discretization_tags():
    tags = VGroup(
        Chip("same integral", max_width=2.05, height=0.46, stroke_color=INPUT, font_size=18),
        Chip("different discretizations", max_width=3.16, height=0.46, stroke_color=OUTPUT, font_size=18),
    ).arrange(DOWN, buff=0.20)
    tags.move_to(RIGHT_FORMULA_CENTER + UP * 2.62)
    return tags


def make_nonuniform_weight_labels(axes, edges=NONUNIFORM_EDGES):
    labels = VGroup()
    for index in (1, 4, 6):
        left = float(edges[index])
        right = float(edges[index + 1])
        center = 0.5 * (left + right)
        weight = SafeMathTex(r"w_i", max_width=0.52, max_height=0.30, font_size=23, color=OPERATOR)
        weight.move_to(axes.c2p(center, sample_function(center) + 0.18))
        labels.add(weight)
    local_weight = Chip("local weight", max_width=2.16, height=0.48, stroke_color=OPERATOR, font_size=18)
    local_weight.move_to(axes.c2p(4.92, 1.88))
    return VGroup(labels, local_weight)


def make_neural_operator_teaser():
    badge = make_formula_badge(
        r"\sum_j \kappa(y,x_j)\,a(x_j)\,w_j",
        max_width=5.65,
        height=0.76,
        stroke_color=OPERATOR,
        font_size=30,
    )
    badge.set_opacity(0.60)
    title = Chip("Neural operator layer", max_width=2.65, height=0.48, stroke_color=OPERATOR, font_size=18)
    title.next_to(badge, UP, buff=0.18)
    teaser = VGroup(title, badge).move_to(RIGHT_FORMULA_CENTER + TEASER_OFFSET)
    teaser.badge = badge
    return teaser


class Scene0701RiemannSumComputationRecipe(TimedScene):
    SCRIPT_ID = "7.1"
    SCRIPT_TITLE = "Riemann sum as a computation recipe"
    SCRIPT_START = 42 * 60 + 30
    SCRIPT_END = 44 * 60 + 20
    SCENE_DURATION = 110.0

    KEYFRAMES = (
        "KF01 0.0s sampled dots first on one function curve",
        "KF02 11.0s coarse rectangles with height and width recipe",
        "KF03 24.0s finer rectangles over true integral area",
        "KF04 38.5s same continuum integral from multiple grids",
        "KF05 52.0s nonuniform rectangles with local weights",
        "KF06 67.0s weighted sum bridge with neural-operator teaser",
    )

    def construct(self):
        background = make_background_network(seed=701, n=70, dot_opacity=0.08, line_opacity=0.045)
        stage = make_riemann_stage()
        axes = stage.axes
        graph = stage.graph
        exact_area = stage.exact_area

        sample_positions = np.linspace(DOMAIN_START + 0.50, DOMAIN_END - 0.50, 7)
        sample_dots = make_sample_dots(axes, sample_positions)
        sample_chip = Chip("known only at sample points", max_width=3.45, height=0.48, stroke_color=SCIENCE, font_size=18)
        sample_chip.next_to(axes, UP, buff=0.25)

        coarse_rectangles = make_uniform_rectangles(axes, COARSE_EDGES)
        fine_rectangles = make_uniform_rectangles(axes, FINE_EDGES, color=OUTPUT, opacity=0.24)
        alternate_rectangles = make_uniform_rectangles(axes, ALT_EDGES, color=SCIENCE, opacity=0.22)
        alternate_rectangles.shift(DOWN * 0.10)
        nonuniform_rectangles = make_nonuniform_rectangles(axes)
        nonuniform_dots = make_sample_dots(axes, [0.5 * (NONUNIFORM_EDGES[i] + NONUNIFORM_EDGES[i + 1]) for i in range(len(NONUNIFORM_EDGES) - 1)], color=OPERATOR)

        recipe_callouts = make_recipe_callouts(axes)
        formula_sequence = make_formula_sequence()
        integral_formula = formula_sequence.integral
        uniform_formula = formula_sequence.uniform_sum
        weighted_formula = formula_sequence.weighted_sum
        discretization_tags = make_discretization_tags()
        weight_labels = make_nonuniform_weight_labels(axes)
        teaser = make_neural_operator_teaser()
        true_integral_label = Chip("true integral", max_width=1.70, height=0.44, stroke_color=INPUT, font_size=17)
        true_integral_label.move_to(axes.c2p(5.20, 1.68))
        nonuniform_chip = Chip("nonuniform samples", max_width=2.28, height=0.46, stroke_color=OPERATOR, font_size=18)
        nonuniform_chip.move_to(axes.c2p(1.08, 1.88))

        assert_in_frame(VGroup(stage, sample_chip), margin=0.28, label="sample_stage")
        assert_in_frame(VGroup(stage, formula_sequence), margin=0.25, label="stage_with_formula")
        assert_in_frame(discretization_tags, margin=0.25, label="discretization_tags")
        assert_in_frame(VGroup(weighted_formula, teaser), margin=0.25, label="final_formula_teaser")
        assert_no_group_overlap([integral_formula, uniform_formula, weighted_formula], min_gap=0.06)

        self.add(background)

        # VO exact: Giả sử ta có một function một chiều, và chỉ biết giá trị của nó tại các điểm sample.
        # Global 42:30.0-42:41.0 => 42:30.0 -> local 0.0, 42:41.0 -> local 11.0
        self.play_timed(
            "show_sample_points_before_curve",
            0.0,
            5.0,
            FadeIn(VGroup(stage.axes, stage.baseline), shift=UP * 0.04),
            LaggedStart(*[FadeIn(dot, scale=1.35) for dot in sample_dots], lag_ratio=0.09),
            FadeIn(sample_chip, shift=DOWN * 0.05),
        )
        self.play_timed(
            "reveal_curve_through_samples",
            5.0,
            11.0,
            Create(graph),
        )

        # VO exact: Muốn xấp xỉ diện tích dưới đường cong, ta cộng các cột nhỏ: chiều cao là giá trị function, chiều rộng là bước lưới.
        # Global 42:41.0-42:54.0 => 42:41.0 -> local 11.0, 42:54.0 -> local 24.0
        self.play_timed(
            "build_coarse_riemann_rectangles",
            11.0,
            18.0,
            LaggedStart(*[FadeIn(rect, shift=UP * 0.05) for rect in coarse_rectangles], lag_ratio=0.08),
            FadeIn(integral_formula, shift=LEFT * 0.08),
        )
        self.play_timed(
            "label_height_and_width_recipe",
            18.0,
            24.0,
            FadeIn(recipe_callouts, shift=UP * 0.04),
            FadeIn(uniform_formula, shift=LEFT * 0.08),
        )

        # VO exact: Lưới càng mịn, tổng này càng tiến gần tích phân thật.
        # Global 42:54.0-43:07.5 => 42:54.0 -> local 24.0, 43:07.5 -> local 37.5
        self.play_timed(
            "show_true_area_behind_rectangles",
            24.0,
            28.5,
            FadeIn(exact_area),
            FadeIn(true_integral_label, shift=LEFT * 0.05),
            recipe_callouts.animate.set_opacity(0.34),
        )
        self.play_timed(
            "refine_rectangles_shrink_gap",
            28.5,
            37.5,
            ReplacementTransform(coarse_rectangles, fine_rectangles),
            uniform_formula.animate.set_opacity(0.92),
            sample_dots.animate.set_opacity(0.45),
        )

        # Pause exact: 1.0s.
        # Global 43:07.5-43:08.5 => 43:07.5 -> local 37.5, 43:08.5 -> local 38.5
        self.wait_timed("hold_refined_riemann_sum", 37.5, 38.5)

        # VO exact: Điều quan trọng ở đây là: cùng một integral continuum có thể được tính gần đúng từ nhiều discretization khác nhau.
        # Global 43:08.5-43:22.0 => 43:08.5 -> local 38.5, 43:22.0 -> local 52.0
        self.play_timed(
            "show_same_integral_different_uniform_grids",
            38.5,
            45.5,
            FadeIn(discretization_tags, shift=DOWN * 0.05),
            fine_rectangles.animate.set_opacity(0.16),
            FadeIn(alternate_rectangles, shift=DOWN * 0.04),
        )
        self.play_timed(
            "alternate_discretization_pulse",
            45.5,
            52.0,
            alternate_rectangles.animate.set_opacity(0.38).shift(UP * 0.10),
            Circumscribe(integral_formula, color=INPUT, buff=0.06),
        )

        # VO exact: Nếu sample không đều, mỗi điểm không nên đóng góp như nhau. Ta cần weight tương ứng với local cell size hoặc quadrature rule.
        # Global 43:22.0-43:37.0 => 43:22.0 -> local 52.0, 43:37.0 -> local 67.0
        self.play_timed(
            "switch_to_nonuniform_samples",
            52.0,
            58.5,
            FadeOut(VGroup(fine_rectangles, alternate_rectangles, sample_dots, sample_chip, true_integral_label, recipe_callouts), shift=DOWN * 0.04),
            FadeIn(nonuniform_rectangles, shift=UP * 0.04),
            FadeIn(nonuniform_dots, scale=1.15),
            FadeIn(nonuniform_chip, shift=RIGHT * 0.04),
        )
        self.play_timed(
            "add_local_quadrature_weights",
            58.5,
            67.0,
            FadeIn(weight_labels, shift=UP * 0.04),
            ReplacementTransform(uniform_formula, weighted_formula),
        )

        # VO exact: Chính ý tưởng “sum có trọng số như xấp xỉ integral” sẽ xuất hiện lại trong neural operator layer.
        # Global 43:37.0-44:20.0 => 43:37.0 -> local 67.0, 44:20.0 -> local 110.0
        self.play_timed(
            "make_weighted_sum_the_bridge",
            67.0,
            78.0,
            FadeOut(VGroup(integral_formula, discretization_tags, nonuniform_chip), shift=UP * 0.04),
            weighted_formula.animate.move_to(RIGHT_FORMULA_CENTER + FINAL_WEIGHTED_FORMULA_OFFSET).set_opacity(1.0),
            nonuniform_rectangles.animate.set_opacity(0.44),
        )
        self.play_timed(
            "ghost_preview_neural_operator_weighted_sum",
            78.0,
            92.0,
            FadeIn(teaser, shift=UP * 0.08),
            Circumscribe(weighted_formula, color=NVIDIA_GREEN, buff=0.07),
        )
        self.play_timed(
            "hold_teaser_without_deriving",
            92.0,
            109.7,
            teaser.animate.set_opacity(0.72),
            weighted_formula.animate.set_opacity(1.0),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
