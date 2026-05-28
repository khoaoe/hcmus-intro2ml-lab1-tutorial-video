"""
Scene 7.2 - Finite difference as local physics probe
Script: ../docs/full_voice_manim_script.md
Global time: 44:20.0-46:20.0
Local duration: 120.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard, make_formula_badge
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    PURPLE,
    SCIENCE,
    TEXT,
    WARNING,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame, assert_no_group_overlap


apply_global_config()


DOMAIN_START = 0.0
DOMAIN_END = 6.0
X0 = 2.55
COARSE_H = 1.05
FINE_H = 0.38


def sample_function(x):
    return 1.08 + 0.38 * np.sin(1.08 * x - 0.45) + 0.17 * np.cos(2.35 * x + 0.22)


def sample_derivative(x):
    return 0.38 * 1.08 * np.cos(1.08 * x - 0.45) - 0.17 * 2.35 * np.sin(2.35 * x + 0.22)


def make_derivative_stage():
    axes = Axes(
        x_range=[DOMAIN_START, DOMAIN_END, 1],
        y_range=[0, 2.05, 0.5],
        x_length=7.35,
        y_length=4.05,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 1.15, "include_ticks": False},
    )
    axes.move_to(LEFT * 2.85 + UP * 0.25)
    curve = axes.plot(sample_function, x_range=[DOMAIN_START, DOMAIN_END], color=INPUT, stroke_width=3.2)
    baseline = Line(axes.c2p(DOMAIN_START, 0), axes.c2p(DOMAIN_END, 0), color=GRID, stroke_width=1.0)
    stage = VGroup(axes, baseline, curve)
    stage.axes = axes
    stage.curve = curve
    stage.baseline = baseline
    return stage


def make_tangent_probe(axes, x=X0):
    y = sample_function(x)
    slope = sample_derivative(x)
    span = 0.86
    tangent = Line(
        axes.c2p(x - span, y - slope * span),
        axes.c2p(x + span, y + slope * span),
        color=NVIDIA_GREEN,
        stroke_width=3.2,
    )
    point = Dot(axes.c2p(x, y), radius=0.065, color=NVIDIA_GREEN)
    label = Chip("derivative = local slope", max_width=3.12, height=0.48, stroke_color=NVIDIA_GREEN, font_size=18)
    label.next_to(tangent, UP, buff=0.22).shift(RIGHT * 0.35)
    x_label = SafeMathTex(r"x_i", max_width=0.42, max_height=0.26, font_size=22, color=TEXT)
    x_label.next_to(point, DOWN, buff=0.12)
    probe = VGroup(tangent, point, x_label, label)
    probe.tangent = tangent
    probe.point = point
    probe.label = label
    return probe


def make_secant_probe(axes, x=X0, dx=COARSE_H):
    y0 = sample_function(x)
    y1 = sample_function(x + dx)
    p0 = axes.c2p(x, y0)
    p1 = axes.c2p(x + dx, y1)
    base1 = axes.c2p(x + dx, y0)

    secant = Line(p0, p1, color=OPERATOR, stroke_width=3.0)
    dots = VGroup(Dot(p0, radius=0.055, color=OPERATOR), Dot(p1, radius=0.055, color=OPERATOR))
    vertical = Line(base1, p1, color=PURPLE, stroke_width=3.0)
    horizontal = Line(p0, base1, color=OPERATOR, stroke_width=3.0)

    vertical_label = Chip("vertical difference", max_width=2.58, height=0.44, stroke_color=PURPLE, font_size=16)
    horizontal_label = Chip("horizontal spacing", max_width=2.48, height=0.44, stroke_color=OPERATOR, font_size=16)

    formula = make_formula_badge(
        r"\frac{a(x_{i+1})-a(x_i)}{\Delta x}",
        max_width=4.28,
        height=0.78,
        stroke_color=OPERATOR,
        font_size=32,
    )
    formula.move_to(RIGHT * 4.15 + UP * 0.62)
    measure_labels = VGroup(vertical_label, horizontal_label).arrange(DOWN, buff=0.14)
    measure_labels.next_to(formula, DOWN, buff=0.14)

    probe = VGroup(secant, dots, vertical, horizontal, measure_labels, formula)
    probe.secant = secant
    probe.dots = dots
    probe.vertical = vertical
    probe.horizontal = horizontal
    probe.measure_labels = measure_labels
    probe.formula = formula
    probe.dx = dx
    return probe


def make_refinement_note():
    note = Chip(
        "finer mesh -> better derivative approximation",
        max_width=4.92,
        height=0.52,
        stroke_color=NVIDIA_GREEN,
        font_size=18,
    )
    note.move_to(RIGHT * 4.15 + DOWN * 0.44)
    return note


def make_pde_residual_bubble():
    formula = SafeMathTex(
        r"R[u] = u_t - F(u,\nabla u,\nabla^2 u)",
        max_width=4.86,
        max_height=0.58,
        font_size=29,
        color=TEXT,
    )
    title = Chip("PDE residual", max_width=1.90, height=0.42, stroke_color=SCIENCE, font_size=16)
    derivative_terms = Chip("derivative terms", max_width=2.28, height=0.42, stroke_color=NVIDIA_GREEN, font_size=16)
    body = VGroup(formula, derivative_terms).arrange(DOWN, buff=0.20)
    card = PanelCard("local physics check", body=body, width=5.55, height=2.38, accent_color=SCIENCE, title_font_size=21)
    title.move_to(card.get_top() + DOWN * 0.48 + RIGHT * 1.55)
    highlights = VGroup(
        SurroundingRectangle(formula[0][5:7], color=NVIDIA_GREEN, buff=0.03, stroke_width=1.4),
        SurroundingRectangle(formula[0][14:17], color=NVIDIA_GREEN, buff=0.03, stroke_width=1.4),
    )
    bubble = VGroup(card, title, highlights).move_to(RIGHT * 3.95 + UP * 0.78)
    bubble.formula = formula
    bubble.card = card
    return bubble


def make_raster_icon():
    cells = VGroup()
    for row in range(4):
        for col in range(5):
            color = [GRID, INPUT, SCIENCE, OPERATOR, PURPLE][(row + col) % 5]
            cell = Square(side_length=0.22, stroke_color=GRID, stroke_width=0.6, fill_color=color, fill_opacity=0.26)
            cell.move_to([0.24 * (col - 2), 0.24 * (1.5 - row), 0])
            cells.add(cell)
    label = Chip("flat raster", max_width=1.45, height=0.38, stroke_color=WARNING, font_size=15)
    bad = Chip("insufficient for physics checks", max_width=3.24, height=0.42, stroke_color=WARNING, font_size=15)
    return VGroup(cells, label, bad).arrange(DOWN, buff=0.14)


def make_output_function_panel():
    stage = make_derivative_stage().scale(0.62).move_to(LEFT * 3.75 + DOWN * 0.40)
    axes = stage.axes
    tangent = make_tangent_probe(axes, x=3.08).scale(0.82)
    query_dots = VGroup(
        Dot(axes.c2p(1.0, sample_function(1.0)), radius=0.045, color=SCIENCE),
        Dot(axes.c2p(3.08, sample_function(3.08)), radius=0.052, color=NVIDIA_GREEN),
        Dot(axes.c2p(5.0, sample_function(5.0)), radius=0.045, color=SCIENCE),
    )
    message = Chip(
        "output must support meaningful derivatives",
        max_width=4.92,
        height=0.52,
        stroke_color=NVIDIA_GREEN,
        font_size=18,
    )
    message.move_to(RIGHT * 3.55 + UP * 1.72)
    raster = make_raster_icon().move_to(RIGHT * 3.55 + DOWN * 0.82)
    panel = VGroup(stage, tangent.tangent, tangent.point, query_dots, message, raster)
    panel.stage = stage
    panel.message = message
    panel.raster = raster
    return panel


def _make_integral_icon():
    axes = Axes(
        x_range=[0, 3, 1],
        y_range=[0, 1.8, 1],
        x_length=2.15,
        y_length=1.16,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 0.8, "include_ticks": False},
    )
    curve = axes.plot(lambda x: 0.78 + 0.34 * np.sin(1.6 * x - 0.2), x_range=[0, 3], color=INPUT, stroke_width=2.1)
    area = axes.get_area(curve, x_range=[0, 3], color=OUTPUT, opacity=0.30)
    sweep = Arrow(axes.c2p(0.2, 1.45), axes.c2p(2.8, 1.45), buff=0.02, color=OUTPUT, stroke_width=2.0)
    return VGroup(axes, area, curve, sweep)


def _make_derivative_icon():
    axes = Axes(
        x_range=[0, 3, 1],
        y_range=[0, 1.8, 1],
        x_length=2.15,
        y_length=1.16,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 0.8, "include_ticks": False},
    )
    curve = axes.plot(lambda x: 0.78 + 0.34 * np.sin(1.6 * x - 0.2), x_range=[0, 3], color=INPUT, stroke_width=2.1)
    p = axes.c2p(1.45, 0.78 + 0.34 * np.sin(1.6 * 1.45 - 0.2))
    tangent = Line(p + LEFT * 0.46 + DOWN * 0.20, p + RIGHT * 0.46 + UP * 0.20, color=NVIDIA_GREEN, stroke_width=2.2)
    stencil = VGroup(Dot(p + LEFT * 0.34, radius=0.035, color=OPERATOR), Dot(p + RIGHT * 0.34, radius=0.035, color=OPERATOR))
    return VGroup(axes, curve, tangent, stencil)


def make_integral_derivative_cards():
    integral_body = VGroup(
        _make_integral_icon(),
        Chip("integral = global aggregation", max_width=3.72, height=0.42, stroke_color=OUTPUT, font_size=16),
    ).arrange(DOWN, buff=0.18)
    derivative_body = VGroup(
        _make_derivative_icon(),
        Chip("derivative = local physics probe", max_width=3.86, height=0.42, stroke_color=NVIDIA_GREEN, font_size=16),
    ).arrange(DOWN, buff=0.18)
    integral_card = PanelCard("Integral", body=integral_body, width=4.35, height=2.92, accent_color=OUTPUT, title_font_size=23)
    derivative_card = PanelCard("Derivative", body=derivative_body, width=4.35, height=2.92, accent_color=NVIDIA_GREEN, title_font_size=23)
    cards = VGroup(integral_card, derivative_card).arrange(RIGHT, buff=1.05).move_to(ORIGIN)
    cards.integral_card = integral_card
    cards.derivative_card = derivative_card
    return cards


def make_neural_operator_bridge():
    cards = make_integral_derivative_cards()
    cards.integral_card.move_to(LEFT * 4.65 + UP * 0.52)
    cards.derivative_card.move_to(RIGHT * 4.65 + UP * 0.52)
    layer_box = RoundedRectangle(
        width=3.10,
        height=1.10,
        corner_radius=0.08,
        stroke_color=OPERATOR,
        stroke_width=1.8,
        fill_color=CARD_BG,
        fill_opacity=0.80,
    )
    layer_label = SafeText("Neural Operator layer", max_width=2.72, max_height=0.38, font_size=22, color=TEXT, weight="BOLD")
    layer_label.move_to(layer_box)
    layer = VGroup(layer_box, layer_label).move_to(DOWN * 1.02)
    left_arrow = Arrow(cards.integral_card.get_bottom(), layer.get_left() + LEFT * 0.05, buff=0.08, color=OUTPUT, stroke_width=2.8)
    right_arrow = Arrow(cards.derivative_card.get_bottom(), layer.get_right() + RIGHT * 0.05, buff=0.08, color=NVIDIA_GREEN, stroke_width=2.8)
    bridge_note = Chip("function-to-function mapping + local physics", max_width=4.82, height=0.48, stroke_color=OPERATOR, font_size=17)
    bridge_note.next_to(layer, DOWN, buff=0.24)
    bridge = VGroup(cards.integral_card, cards.derivative_card, left_arrow, right_arrow, layer, bridge_note).move_to(ORIGIN)
    bridge.integral_card = cards.integral_card
    bridge.derivative_card = cards.derivative_card
    bridge.layer = layer
    return bridge


class Scene0702FiniteDifferenceLocalPhysicsProbe(TimedScene):
    SCRIPT_ID = "7.2"
    SCRIPT_TITLE = "Finite difference as local physics probe"
    SCRIPT_START = 44 * 60 + 20
    SCRIPT_END = 46 * 60 + 20
    SCENE_DURATION = 120.0

    KEYFRAMES = (
        "KF01 0.0s curve with tangent at x_i",
        "KF02 11.5s secant finite difference stencil",
        "KF03 23.0s mesh refinement secant approaches tangent",
        "KF04 37.0s PDE residual bubble highlights derivative terms",
        "KF05 50.5s output function supports derivatives, raster does not",
        "KF06 64.5s integral and derivative cards",
        "KF07 81.5s both feed Neural Operator layer",
    )

    def construct(self):
        background = make_background_network(seed=702, n=74, dot_opacity=0.08, line_opacity=0.045)
        stage = make_derivative_stage()
        tangent_probe = make_tangent_probe(stage.axes)
        secant_probe = make_secant_probe(stage.axes, X0, COARSE_H)
        fine_secant_probe = make_secant_probe(stage.axes, X0, FINE_H)
        fine_secant_visible = VGroup(
            fine_secant_probe.secant,
            fine_secant_probe.dots,
            fine_secant_probe.vertical,
            fine_secant_probe.horizontal,
        )
        refinement_note = make_refinement_note()
        residual_bubble = make_pde_residual_bubble()
        output_panel = make_output_function_panel()
        compare_cards = make_integral_derivative_cards()
        bridge = make_neural_operator_bridge()

        assert_in_frame(VGroup(stage, tangent_probe), margin=0.30, label="tangent_stage")
        assert_in_frame(VGroup(stage, secant_probe), margin=0.30, label="secant_stage")
        assert_in_frame(residual_bubble, margin=0.30, label="residual_bubble")
        assert_in_frame(output_panel, margin=0.30, label="output_panel")
        assert_in_frame(compare_cards, margin=0.30, label="comparison_cards")
        assert_in_frame(bridge, margin=0.30, label="final_bridge")
        assert_no_group_overlap([bridge.integral_card, bridge.layer, bridge.derivative_card], min_gap=0.08)

        self.add(background)

        # VO exact: Bây giờ là đạo hàm. Nếu function là một đường cong, đạo hàm tại một điểm đo độ nghiêng local.
        # Global 44:20.0-44:31.5 => 44:20.0 -> local 0.0, 44:31.5 -> local 11.5
        self.play_timed(
            "show_curve_and_local_tangent",
            0.0,
            6.0,
            FadeIn(VGroup(stage.axes, stage.baseline), shift=UP * 0.04),
            Create(stage.curve),
        )
        self.play_timed(
            "mark_derivative_as_local_slope",
            6.0,
            11.5,
            FadeIn(tangent_probe, shift=UP * 0.05),
        )

        # VO exact: Với dữ liệu rời rạc, ta lấy chênh lệch giữa hai điểm gần nhau, chia cho khoảng cách.
        # Global 44:31.5-44:43.0 => 44:31.5 -> local 11.5, 44:43.0 -> local 23.0
        self.play_timed(
            "add_finite_difference_secant",
            11.5,
            17.5,
            FadeIn(VGroup(secant_probe.secant, secant_probe.dots), shift=UP * 0.04),
            FadeIn(secant_probe.formula, shift=LEFT * 0.05),
        )
        self.play_timed(
            "connect_formula_to_vertical_and_horizontal_differences",
            17.5,
            23.0,
            FadeIn(VGroup(secant_probe.vertical, secant_probe.horizontal), shift=UP * 0.03),
            FadeIn(secant_probe.measure_labels, shift=DOWN * 0.03),
        )

        # VO exact: Lưới càng mịn, finite difference càng có cơ hội xấp xỉ đạo hàm tốt hơn.
        # Global 44:43.0-44:56.0 => 44:43.0 -> local 23.0, 44:56.0 -> local 36.0
        self.play_timed(
            "refine_secant_toward_tangent",
            23.0,
            31.0,
            ReplacementTransform(secant_probe.secant, fine_secant_probe.secant),
            ReplacementTransform(secant_probe.dots, fine_secant_probe.dots),
            ReplacementTransform(secant_probe.vertical, fine_secant_probe.vertical),
            ReplacementTransform(secant_probe.horizontal, fine_secant_probe.horizontal),
            tangent_probe.tangent.animate.set_stroke(width=4.2),
        )
        self.play_timed(
            "clear_measurement_callouts_before_refinement_note",
            31.0,
            33.0,
            FadeOut(secant_probe.measure_labels, shift=DOWN * 0.03),
        )
        self.play_timed(
            "show_refinement_message",
            33.0,
            36.0,
            FadeIn(refinement_note, shift=UP * 0.04),
        )

        # Pause exact: 1.0s.
        # Global 44:56.0-44:57.0 => 44:56.0 -> local 36.0, 44:57.0 -> local 37.0
        self.wait_timed("hold_refined_secant", 36.0, 37.0)

        # VO exact: Trong physics, derivative không phải chi tiết phụ. Nó nằm ngay trong PDE.
        # Global 44:57.0-45:10.5 => 44:57.0 -> local 37.0, 45:10.5 -> local 50.5
        self.play_timed(
            "bring_in_pde_residual_bubble",
            37.0,
            44.0,
            VGroup(stage, tangent_probe, fine_secant_visible, secant_probe.formula, refinement_note).animate.scale(0.72).move_to(LEFT * 3.65 + DOWN * 0.28).set_opacity(0.72),
            FadeIn(residual_bubble, shift=LEFT * 0.08),
        )
        self.play_timed(
            "highlight_residual_derivative_terms",
            44.0,
            50.5,
            Circumscribe(residual_bubble.card.body[-1], color=NVIDIA_GREEN, buff=0.06),
        )

        # VO exact: Vì vậy một model output function phải cho phép ta tính derivative một cách có nghĩa.
        # Global 45:10.5-45:24.5 => 45:10.5 -> local 50.5, 45:24.5 -> local 64.5
        self.play_timed(
            "replace_with_output_function_derivative_check",
            50.5,
            58.0,
            FadeOut(VGroup(stage, tangent_probe, fine_secant_visible, secant_probe.formula, refinement_note, residual_bubble), shift=LEFT * 0.06),
            FadeIn(output_panel, shift=UP * 0.08),
        )
        self.play_timed(
            "contrast_output_curve_with_flat_raster",
            58.0,
            64.5,
            Circumscribe(output_panel.message, color=NVIDIA_GREEN, buff=0.06),
            output_panel.raster.animate.set_opacity(0.62),
        )

        # VO exact: Từ đây, hãy nhớ hai phép toán: integral để tổng hợp thông tin toàn domain, derivative để đọc local structure.
        # Global 45:24.5-45:41.5 => 45:24.5 -> local 64.5, 45:41.5 -> local 81.5
        self.play_timed(
            "show_integral_and_derivative_roles",
            64.5,
            72.5,
            FadeOut(output_panel, shift=DOWN * 0.06),
            FadeIn(compare_cards, shift=UP * 0.08),
        )
        self.play_timed(
            "pulse_global_and_local_cards",
            72.5,
            81.5,
            Circumscribe(compare_cards.integral_card, color=OUTPUT, buff=0.05),
            Circumscribe(compare_cards.derivative_card, color=NVIDIA_GREEN, buff=0.05),
        )

        # VO exact: Neural operator sẽ cần cả hai: integral operator để map function sang function, và đôi khi differential component để bắt local physics.
        # Global 45:41.5-46:20.0 => 45:41.5 -> local 81.5, 46:20.0 -> local 120.0
        self.play_timed(
            "feed_both_roles_into_neural_operator_layer",
            81.5,
            94.0,
            ReplacementTransform(compare_cards, bridge),
        )
        self.play_timed(
            "hold_final_bridge",
            94.0,
            119.7,
            bridge.layer.animate.set_stroke(color=OPERATOR, width=2.6),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
