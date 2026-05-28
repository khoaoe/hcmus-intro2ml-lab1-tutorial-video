"""
Scene 6.3 - The suspense line
Script: ../docs/full_voice_manim_script.md
Global time: 38:40.0-42:30.0
Local duration: 230.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import smooth_path
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


VO_LINES = (
    (0.0, 12.0, "Từ đây đến vài phút tới là phần quan trọng nhất của tutorial."),
    (12.0, 23.5, "Ta sẽ không định nghĩa neural operator bằng cách ném ra một công thức rồi hy vọng mọi người tin."),
    (23.5, 35.0, "Ta sẽ bắt đầu từ neural network layer quen thuộc, rồi biến nó từng bước thành integral operator."),
    (35.0, 36.0, "Pause: 1.0s."),
    (36.0, 49.5, "Nếu phần này click, các kiến trúc phía sau — GNO, FNO, Transformer Neural Operator — sẽ trở nên hợp lý hơn rất nhiều."),
    (49.5, 64.0, "Nhưng trước khi làm điều đó, cần hai mảnh toán rất cũ: xấp xỉ tích phân và xấp xỉ đạo hàm."),
    (64.0, 77.0, "Đây là những thứ ta đã gặp từ calculus hoặc numerical methods."),
    (77.0, 93.0, "Tích phân có thể xấp xỉ bằng tổng các giá trị function nhân với độ rộng ô lưới."),
    (93.0, 108.0, "Đạo hàm có thể xấp xỉ bằng finite difference: lấy hiệu hai giá trị gần nhau, chia cho khoảng cách."),
    (108.0, 125.0, "Hai ý tưởng này nghe đơn giản, nhưng chúng là cầu nối giữa function continuum và tensor computation."),
    (125.0, 230.0, "Và bây giờ, ta đi vào chiếc cầu đó."),
)


def _sample_curve_points(width=2.55, height=1.35, count=19, phase=0.0):
    xs = np.linspace(-width / 2, width / 2, count)
    return [[x, 0.24 * height * np.sin(1.35 * x + phase) + 0.11 * height * np.cos(2.3 * x - 0.4), 0] for x in xs]


def _small_vector(symbol, color=INPUT):
    cells = VGroup()
    for sub in ("1", "2", "j", "n"):
        box = RoundedRectangle(width=0.56, height=0.38, corner_radius=0.04, stroke_color=color, stroke_width=1.0, fill_color="#0D1B2A", fill_opacity=0.78)
        label = SafeMathTex(fr"{symbol}_{sub}", max_width=0.40, max_height=0.24, font_size=21, color=TEXT)
        label.move_to(box)
        cells.add(VGroup(box, label))
    dots = VGroup(Dot(radius=0.023, color=MUTED), Dot(radius=0.023, color=MUTED)).arrange(DOWN, buff=0.05)
    return VGroup(cells[:2], dots, cells[2:]).arrange(DOWN, buff=0.08)


def _matrix_grid(rows=5, cols=5, cell=0.30):
    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            rect = Square(side_length=cell, stroke_color=GRID, stroke_width=0.65, fill_color=CARD_BG, fill_opacity=0.75)
            rect.move_to([(j - (cols - 1) / 2) * cell, ((rows - 1) / 2 - i) * cell, 0])
            if i == 2 or j == 2:
                rect.set_fill(OPERATOR, opacity=0.38).set_stroke(OPERATOR, opacity=0.76)
            cells.add(rect)
    return cells


def make_neural_layer_closeup():
    title = SafeText("The key bridge", max_width=3.6, max_height=0.46, font_size=31, color=NVIDIA_GREEN, weight="BOLD")
    subtitle = Chip("Neural network layer → integral operator", max_width=5.25, height=0.50, stroke_color=OPERATOR, font_size=18)
    input_col = _small_vector("a", INPUT)
    output_col = _small_vector("v", OUTPUT)
    matrix_box = RoundedRectangle(width=2.10, height=2.10, corner_radius=0.07, stroke_color=OPERATOR, stroke_width=1.4, fill_color=CARD_BG, fill_opacity=0.48)
    matrix = _matrix_grid(cell=0.29)
    matrix_label = SafeMathTex(r"K_{ij}", max_width=0.72, max_height=0.40, font_size=30, color=OPERATOR).move_to(matrix_box)
    matrix_block = VGroup(matrix_box, matrix, matrix_label)
    row = VGroup(input_col, matrix_block, output_col).arrange(RIGHT, buff=0.78)
    left_arrow = Arrow(input_col.get_right() + RIGHT * 0.08, matrix_block.get_left() + LEFT * 0.08, buff=0.02, color=INPUT, stroke_width=2.2)
    right_arrow = Arrow(matrix_block.get_right() + RIGHT * 0.08, output_col.get_left() + LEFT * 0.08, buff=0.02, color=OUTPUT, stroke_width=2.2)
    layer = VGroup(title, subtitle, VGroup(row, left_arrow, right_arrow)).arrange(DOWN, buff=0.28).move_to(ORIGIN)
    layer.input_column = input_col
    layer.matrix_block = matrix_block
    layer.output_column = output_col
    return layer


def make_formula_dump_warning():
    ghost_formula = make_formula_badge(r"\mathcal{G}(a)(y)=\cdots", max_width=4.65, height=0.86, stroke_color=WARNING, font_size=28)
    ghost_formula.set_opacity(0.38)
    slash = Line(ghost_formula.get_left() + DOWN * 0.40, ghost_formula.get_right() + UP * 0.40, color=WARNING, stroke_width=4.0)
    stamp = Chip("not first", max_width=1.52, height=0.44, stroke_color=WARNING, font_size=17)
    stamp.move_to(ghost_formula.get_bottom() + UP * 0.12)
    build = Chip("Build it step by step", max_width=3.45, height=0.56, stroke_color=NVIDIA_GREEN, font_size=21)
    build.next_to(ghost_formula, DOWN, buff=0.30)
    warning = VGroup(ghost_formula, slash, stamp, build).move_to(ORIGIN)
    warning.formula_panel = ghost_formula
    return warning


def make_future_architecture_chips():
    question = Chip("Why do these architectures make sense?", max_width=5.30, height=0.58, stroke_color=OPERATOR, font_size=20)
    chips = VGroup(
        Chip("GNO", max_width=1.08, height=0.44, stroke_color=SCIENCE, font_size=18),
        Chip("FNO", max_width=1.08, height=0.44, stroke_color=PURPLE, font_size=18),
        Chip("Transformer NO", max_width=2.20, height=0.44, stroke_color=OUTPUT, font_size=17),
    ).arrange(RIGHT, buff=0.26)
    chips.next_to(question, DOWN, buff=0.30)
    group = VGroup(question, chips).move_to(ORIGIN)
    group.chips = chips
    return group


def make_tool_cards():
    integral_icon = VGroup(
        smooth_path(_sample_curve_points(width=1.45, height=0.72, count=9), color=SCIENCE, stroke_width=2.0),
        VGroup(*[Rectangle(width=0.18, height=0.42 + 0.08 * i, stroke_width=0, fill_color=OPERATOR, fill_opacity=0.32).shift(RIGHT * (i - 2) * 0.20 + DOWN * 0.18) for i in range(5)]),
    )
    derivative_icon = VGroup(
        smooth_path(_sample_curve_points(width=1.45, height=0.72, count=9, phase=0.5), color=PURPLE, stroke_width=2.0),
        Arrow(LEFT * 0.42 + DOWN * 0.08, RIGHT * 0.42 + UP * 0.20, buff=0.02, color=OPERATOR, stroke_width=2.0),
    )
    cards = VGroup(
        PanelCard("Integral approximation", body=integral_icon, width=3.75, height=2.35, accent_color=SCIENCE, title_font_size=22),
        PanelCard("Derivative approximation", body=derivative_icon, width=3.75, height=2.35, accent_color=PURPLE, title_font_size=22),
    ).arrange(RIGHT, buff=0.70)
    cards.move_to(ORIGIN)
    return cards


def _chalkboard_frame():
    board = RoundedRectangle(width=13.4, height=6.9, corner_radius=0.08, stroke_color=GRID, stroke_width=1.6, fill_color="#0C1A18", fill_opacity=0.64)
    caption = Chip("Old tools, new role", max_width=2.80, height=0.46, stroke_color=NVIDIA_GREEN, font_size=18)
    caption.move_to(board.get_top() + DOWN * 0.38)
    return VGroup(board, caption)


def make_riemann_panel():
    plot_window = Rectangle(width=3.35, height=1.85, stroke_opacity=0, fill_opacity=0)
    axes = VGroup(
        Line(plot_window.get_left() + DOWN * 0.72, plot_window.get_right() + DOWN * 0.72, color=MUTED, stroke_width=1.0),
        Line(plot_window.get_left() + DOWN * 0.72, plot_window.get_left() + UP * 0.74, color=MUTED, stroke_width=1.0),
    )
    xs = np.linspace(-1.42, 1.42, 7)
    rectangles = VGroup()
    samples = VGroup()
    for i, x in enumerate(xs[:-1]):
        next_x = xs[i + 1]
        mid = 0.5 * (x + next_x)
        height = 0.78 + 0.34 * np.sin(1.4 * mid) + 0.13 * np.cos(2.0 * mid)
        rect = Rectangle(width=next_x - x, height=height, stroke_color=OPERATOR, stroke_width=0.8, fill_color=OPERATOR, fill_opacity=0.26)
        rect.move_to([0.5 * (x + next_x), plot_window.get_bottom()[1] + height / 2 + 0.03, 0])
        rectangles.add(rect)
        samples.add(Dot([mid, rect.get_top()[1], 0], radius=0.035, color=SCIENCE))
    curve = smooth_path([[x, plot_window.get_bottom()[1] + 0.80 + 0.34 * np.sin(1.4 * x) + 0.13 * np.cos(2.0 * x), 0] for x in np.linspace(-1.45, 1.45, 17)], color=SCIENCE, stroke_width=2.3)
    plot = VGroup(plot_window, axes, rectangles, curve, samples)
    equation = make_formula_badge(r"\sum a(x_j)\Delta x_j \approx \int a(x)\,dx", max_width=4.45, height=0.58, stroke_color=SCIENCE, font_size=24)
    body = VGroup(plot, equation).arrange(DOWN, buff=0.18)
    panel = PanelCard("Integral approximation", body=body, width=5.30, height=3.75, accent_color=SCIENCE, title_font_size=22)
    panel.rectangles = rectangles
    panel.plot_window = plot_window
    return panel


def make_finite_difference_panel():
    plot_window = Rectangle(width=3.35, height=1.85, stroke_opacity=0, fill_opacity=0)
    axes = VGroup(
        Line(plot_window.get_left() + DOWN * 0.70, plot_window.get_right() + DOWN * 0.70, color=MUTED, stroke_width=1.0),
        Line(plot_window.get_left() + DOWN * 0.70, plot_window.get_left() + UP * 0.74, color=MUTED, stroke_width=1.0),
    )
    curve_points = [[x, plot_window.get_bottom()[1] + 0.78 + 0.38 * np.sin(1.12 * x + 0.4), 0] for x in np.linspace(-1.45, 1.45, 17)]
    curve = smooth_path(curve_points, color=PURPLE, stroke_width=2.3)
    p1 = np.array([-0.35, plot_window.get_bottom()[1] + 0.78 + 0.38 * np.sin(1.12 * -0.35 + 0.4), 0])
    p2 = np.array([0.48, plot_window.get_bottom()[1] + 0.78 + 0.38 * np.sin(1.12 * 0.48 + 0.4), 0])
    dots = VGroup(Dot(p1, radius=0.045, color=OPERATOR), Dot(p2, radius=0.045, color=OPERATOR))
    secant = Arrow(p1, p2, buff=0.03, color=OPERATOR, stroke_width=2.3)
    label = Chip("finite difference", max_width=2.50, height=0.42, stroke_color=PURPLE, font_size=16)
    equation = make_formula_badge(r"\mathrm{slope}\approx \Delta a / \Delta x", max_width=4.20, height=0.58, stroke_color=PURPLE, font_size=24)
    plot = VGroup(plot_window, axes, curve, dots, secant)
    body = VGroup(plot, label, equation).arrange(DOWN, buff=0.14)
    panel = PanelCard("Derivative approximation", body=body, width=5.30, height=3.75, accent_color=PURPLE, title_font_size=22)
    panel.secant = secant
    return panel


def make_bridge_graphic():
    continuum_curve = smooth_path(_sample_curve_points(width=2.25, height=1.15, count=17), color=SCIENCE, stroke_width=2.6)
    continuum_label = Chip("function continuum", max_width=2.75, height=0.46, stroke_color=SCIENCE, font_size=17)
    continuum = VGroup(continuum_curve, continuum_label).arrange(DOWN, buff=0.16)

    samples = VGroup()
    for i, y in enumerate([0.32, -0.05, 0.24, -0.20, 0.10]):
        box = RoundedRectangle(width=0.46, height=0.42, corner_radius=0.04, stroke_color=OUTPUT, stroke_width=1.0, fill_color="#0D1B2A", fill_opacity=0.82)
        dot = Dot(radius=0.035, color=OUTPUT).move_to(box)
        samples.add(VGroup(box, dot).shift(RIGHT * (i - 2) * 0.50 + UP * y))
    tensor_label = Chip("sampled tensor computation", max_width=3.35, height=0.46, stroke_color=OUTPUT, font_size=17)
    tensor = VGroup(samples, tensor_label).arrange(DOWN, buff=0.16)

    row = VGroup(continuum, tensor).arrange(RIGHT, buff=2.40)
    bridge_arrow = Arrow(continuum.get_right() + RIGHT * 0.16, tensor.get_left() + LEFT * 0.16, buff=0.03, color=OPERATOR, stroke_width=4.0)
    bridge_label = Chip("calculus + numerical methods", max_width=3.95, height=0.46, stroke_color=OPERATOR, font_size=17)
    bridge_label.next_to(bridge_arrow, UP, buff=0.16)
    final = Chip("Next: Riemann sum", max_width=2.75, height=0.52, stroke_color=NVIDIA_GREEN, font_size=20)
    final.next_to(bridge_arrow, DOWN, buff=0.44)

    bridge = VGroup(row, bridge_arrow, bridge_label, final).move_to(ORIGIN)
    bridge.continuum = continuum
    bridge.tensor = tensor
    bridge.bridge_arrow = bridge_arrow
    bridge.final_text = final
    return bridge


class Scene0603TheSuspenseLine(TimedScene):
    SCRIPT_ID = "6.3"
    SCRIPT_TITLE = "The suspense line"
    SCRIPT_START = 38 * 60 + 40
    SCRIPT_END = 42 * 60 + 30
    SCENE_DURATION = 230.0

    KEYFRAMES = (
        "KF01 0.0s neural layer key bridge",
        "KF02 12.0s formula dump rejected",
        "KF03 23.5s layer points toward integral operator placeholder",
        "KF04 36.0s future architectures question",
        "KF05 49.5s two old tool cards",
        "KF06 77.0s Riemann rectangles",
        "KF07 93.0s finite difference secant",
        "KF08 125.0s long bridge beat to Riemann sum",
    )

    def construct(self):
        background = make_background_network(seed=6303, n=82, dot_opacity=0.10, line_opacity=0.06)
        layer = make_neural_layer_closeup()
        warning = make_formula_dump_warning()
        future = make_future_architecture_chips()
        tools = make_tool_cards()
        board = _chalkboard_frame()
        riemann = make_riemann_panel()
        finite_diff = make_finite_difference_panel()
        panels = VGroup(riemann, finite_diff).arrange(RIGHT, buff=0.56).move_to(DOWN * 0.12)
        bridge = make_bridge_graphic()
        layer_final_probe = make_neural_layer_closeup().move_to(LEFT * 2.5).scale(0.82)
        placeholder = Chip("integral operator", max_width=2.45, height=0.52, stroke_color=OPERATOR, font_size=19)
        placeholder.move_to(RIGHT * 3.7 + DOWN * 0.10)
        layer_arrow = Arrow(layer_final_probe.matrix_block.get_right() + RIGHT * 0.22, placeholder.get_left() + LEFT * 0.12, buff=0.03, color=OPERATOR, stroke_width=2.6)
        layer_to_operator = VGroup(placeholder, layer_arrow)

        assert_in_frame(layer, margin=0.25, label="layer")
        assert_in_frame(warning, margin=0.25, label="formula_warning")
        assert_in_frame(future, margin=0.25, label="future_architecture_chips")
        assert_in_frame(tools, margin=0.25, label="tool_cards")
        assert_in_frame(VGroup(board, panels), margin=0.24, label="chalkboard_panels")
        assert_in_frame(bridge, margin=0.30, label="bridge_graphic")
        assert_no_group_overlap([riemann, finite_diff], min_gap=0.08)

        self.add(background)

        # VO exact: Từ đây đến vài phút tới là phần quan trọng nhất của tutorial.
        # Global 38:40.0-38:52.0 => 38:40.0 -> local 0.0, 38:52.0 -> local 12.0
        self.play_timed(
            "fade_in_key_bridge_layer",
            0.0,
            12.0,
            FadeIn(layer, shift=UP * 0.08),
            self.camera.frame.animate.scale(0.96),
        )

        # VO exact: Ta sẽ không định nghĩa neural operator bằng cách ném ra một công thức rồi hy vọng mọi người tin.
        # Global 38:52.0-39:03.5 => 38:52.0 -> local 12.0, 39:03.5 -> local 23.5
        self.play_timed(
            "reject_formula_dump",
            12.0,
            18.0,
            layer.animate.set_opacity(0.22).shift(LEFT * 0.25),
            FadeIn(warning, shift=DOWN * 0.06),
        )
        self.play_timed(
            "replace_with_step_by_step",
            18.0,
            23.5,
            Circumscribe(warning[-1], color=NVIDIA_GREEN, buff=0.06),
        )

        # VO exact: Ta sẽ bắt đầu từ neural network layer quen thuộc, rồi biến nó từng bước thành integral operator.
        # Global 39:03.5-39:15.0 => 39:03.5 -> local 23.5, 39:15.0 -> local 35.0
        self.play_timed(
            "move_layer_toward_operator_placeholder",
            23.5,
            29.0,
            FadeOut(warning, shift=DOWN * 0.05),
            layer.animate.set_opacity(1.0).move_to(LEFT * 2.5).scale(0.82),
        )
        self.play_timed(
            "fade_integral_operator_placeholder",
            29.0,
            35.0,
            FadeIn(layer_to_operator, shift=LEFT * 0.06),
        )

        # Pause exact: 1.0s.
        # Global 39:15.0-39:16.0 => 39:15.0 -> local 35.0, 39:16.0 -> local 36.0
        self.wait_timed("hold_layer_to_operator", 35.0, 36.0)

        # VO exact: Nếu phần này click, các kiến trúc phía sau — GNO, FNO, Transformer Neural Operator — sẽ trở nên hợp lý hơn rất nhiều.
        # Global 39:16.0-39:29.5 => 39:16.0 -> local 36.0, 39:29.5 -> local 49.5
        self.play_timed(
            "show_future_architecture_question",
            36.0,
            43.0,
            FadeOut(VGroup(layer, layer_to_operator), shift=LEFT * 0.06),
            FadeIn(future, shift=UP * 0.08),
        )
        self.play_timed(
            "dim_future_architecture_chips",
            43.0,
            49.5,
            future.chips.animate.set_opacity(0.42),
        )

        # VO exact: Nhưng trước khi làm điều đó, cần hai mảnh toán rất cũ: xấp xỉ tích phân và xấp xỉ đạo hàm.
        # Global 39:29.5-39:44.0 => 39:29.5 -> local 49.5, 39:44.0 -> local 64.0
        self.play_timed(
            "reveal_two_old_math_tools",
            49.5,
            64.0,
            FadeOut(future, shift=UP * 0.06),
            FadeIn(tools, shift=UP * 0.08),
        )

        # VO exact: Đây là những thứ ta đã gặp từ calculus hoặc numerical methods.
        # Global 39:44.0-39:57.0 => 39:44.0 -> local 64.0, 39:57.0 -> local 77.0
        self.play_timed(
            "move_tools_to_chalkboard",
            64.0,
            77.0,
            FadeIn(board, shift=DOWN * 0.04),
            tools.animate.scale(0.58).move_to(DOWN * 0.12).set_opacity(0.62),
        )

        # VO exact: Tích phân có thể xấp xỉ bằng tổng các giá trị function nhân với độ rộng ô lưới.
        # Global 39:57.0-40:13.0 => 39:57.0 -> local 77.0, 40:13.0 -> local 93.0
        self.play_timed(
            "show_riemann_rectangles",
            77.0,
            93.0,
            FadeOut(tools, shift=DOWN * 0.03),
            FadeIn(riemann, shift=RIGHT * 0.08),
            LaggedStart(*[FadeIn(rect, shift=UP * 0.02) for rect in riemann.rectangles], lag_ratio=0.08),
        )

        # VO exact: Đạo hàm có thể xấp xỉ bằng finite difference: lấy hiệu hai giá trị gần nhau, chia cho khoảng cách.
        # Global 40:13.0-40:28.0 => 40:13.0 -> local 93.0, 40:28.0 -> local 108.0
        self.play_timed(
            "show_finite_difference_secant",
            93.0,
            108.0,
            FadeIn(finite_diff, shift=LEFT * 0.08),
            GrowArrow(finite_diff.secant),
        )

        # VO exact: Hai ý tưởng này nghe đơn giản, nhưng chúng là cầu nối giữa function continuum và tensor computation.
        # Global 40:28.0-40:45.0 => 40:28.0 -> local 108.0, 40:45.0 -> local 125.0
        self.play_timed(
            "connect_tools_into_bridge",
            108.0,
            125.0,
            VGroup(riemann, finite_diff).animate.set_opacity(0.30).scale(0.58).move_to(DOWN * 2.12),
            FadeIn(bridge, shift=UP * 0.10),
        )

        # VO exact: Và bây giờ, ta đi vào chiếc cầu đó.
        # Global 40:45.0-42:30.0 => 40:45.0 -> local 125.0, 42:30.0 -> local 230.0
        self.play_timed(
            "long_bridge_forward_motion",
            125.0,
            229.7,
            bridge.animate.scale(1.08).shift(UP * 0.08),
            bridge.bridge_arrow.animate.set_stroke(width=6.0),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
