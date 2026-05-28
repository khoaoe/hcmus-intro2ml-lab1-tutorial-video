"""
Scene 6.2 - Three desired properties
Script: ../docs/full_voice_manim_script.md
Global time: 36:45.0-38:40.0
Local duration: 115.0s
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
    (0.0, 10.5, "Một neural operator tốt cần ít nhất ba property."),
    (10.5, 21.5, "Thứ nhất: input có thể được cung cấp ở nhiều discretization."),
    (21.5, 33.0, "Thứ hai: output có thể query ở các điểm ta muốn, không bị khóa vào một grid duy nhất."),
    (33.0, 48.0, "Thứ ba: khi mesh refinement tiến dần về continuum, model converges về một operator limit nhất quán."),
    (48.0, 49.0, "Pause: 1.0s."),
    (49.0, 63.5, "Đây là lý do các operation bên trong model thường được xây như xấp xỉ của operation continuum."),
    (63.5, 77.5, "Matrix multiplication trên index cố định không đủ tự nhiên. Integral operator thì tự nhiên hơn."),
    (77.5, 115.0, "Vậy để xây neural operator từ neural network, ta cần một trick đẹp: nhìn lại một layer neural network như một Riemann sum."),
)


def _function_points(width=2.35, height=1.12, count=9, phase=0.0):
    xs = np.linspace(-width / 2, width / 2, count)
    return [[x, 0.34 * np.sin(1.55 * x + phase) + 0.16 * np.cos(2.7 * x - 0.4), 0] for x in xs]


def _make_curve(width=2.35, phase=0.0, color=SCIENCE, stroke_width=2.4):
    return smooth_path(_function_points(width=width, phase=phase, count=13), color=color, stroke_width=stroke_width)


def _checkmark(color=NVIDIA_GREEN):
    mark = SafeMathTex(r"\checkmark", max_width=0.42, max_height=0.34, font_size=26, color=color)
    circle = Circle(radius=0.23, stroke_color=color, stroke_width=1.3, fill_color="#102514", fill_opacity=0.65)
    mark.move_to(circle)
    return VGroup(circle, mark)


def _sample_dots(xs, curve_width=2.35, color=INPUT, radius=0.038):
    dots = VGroup()
    for x in xs:
        y = 0.34 * np.sin(1.55 * x) + 0.16 * np.cos(2.7 * x - 0.4)
        dots.add(Dot([x, y, 0], radius=radius, color=color))
    return dots


def _mini_grid(width=2.35, height=1.20, nx=6, color=GRID, opacity=0.34):
    lines = VGroup()
    for i in range(nx + 1):
        x = -width / 2 + width * i / nx
        lines.add(Line([x, -height / 2, 0], [x, height / 2, 0], color=color, stroke_width=0.55, stroke_opacity=opacity))
    lines.add(Line([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0], color=color, stroke_width=0.55, stroke_opacity=opacity))
    lines.add(Line([-width / 2, height / 2, 0], [width / 2, height / 2, 0], color=color, stroke_width=0.55, stroke_opacity=opacity))
    return lines


def make_input_discretization_visual():
    rows = VGroup()
    specs = (
        ("coarse grid", np.linspace(-1.05, 1.05, 5), INPUT),
        ("fine grid", np.linspace(-1.05, 1.05, 10), SCIENCE),
        ("irregular", np.array([-1.10, -0.70, -0.38, 0.02, 0.43, 0.86, 1.11]), PURPLE),
    )
    for label, xs, color in specs:
        curve = _make_curve(color=SCIENCE, stroke_width=1.7)
        dots = _sample_dots(xs, color=color)
        tag = Chip(label, max_width=1.30, height=0.34, stroke_color=color, font_size=11, min_font_size=9, padding=0.05)
        row = VGroup(tag, VGroup(curve, dots)).arrange(RIGHT, buff=0.12)
        rows.add(row)
    rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    check = _checkmark().scale(0.86)
    check.next_to(rows, RIGHT, buff=0.15)
    visual = VGroup(rows, check)
    visual.checkmark = check
    return visual


def make_output_query_visual():
    grid = _mini_grid(nx=7, opacity=0.28)
    curve = _make_curve(color=OUTPUT, stroke_width=2.3)
    xs = [-0.78, -0.12, 0.68]
    dots = VGroup()
    labels = VGroup()
    label_tex = ("u(y_1)", "u(y_2)", "u(y_3)")
    for i, x in enumerate(xs):
        y = 0.34 * np.sin(1.55 * x) + 0.16 * np.cos(2.7 * x - 0.4)
        dot = Dot([x, y, 0], radius=0.048, color=OPERATOR)
        label = SafeMathTex(label_tex[i], max_width=0.58, max_height=0.24, font_size=20, color=TEXT)
        label.next_to(dot, UP if i != 2 else DOWN, buff=0.06)
        dots.add(dot)
        labels.add(label)
    check = _checkmark().scale(0.86)
    check.next_to(grid, RIGHT, buff=0.18)
    visual = VGroup(grid, curve, dots, labels, check)
    visual.query_dots = dots
    return visual


def _prediction_curve(noise=0.0, color=SCIENCE):
    xs = np.linspace(-0.95, 0.95, 9)
    points = []
    for i, x in enumerate(xs):
        base = 0.30 * np.sin(1.35 * x) + 0.08 * np.cos(3.0 * x)
        wobble = noise * np.sin(4.7 * x + i * 0.61)
        points.append([x, base + wobble, 0])
    return smooth_path(points, color=color, stroke_width=1.75)


def make_refinement_limit_visual():
    panels = VGroup()
    meshes = VGroup()
    prediction_curves = VGroup()
    specs = (
        ("coarse", 4, 0.16, WARNING),
        ("medium", 7, 0.08, INPUT),
        ("fine", 12, 0.02, NVIDIA_GREEN),
    )
    for label, nx, noise, color in specs:
        mesh = _mini_grid(width=1.15, height=0.72, nx=nx, color=color, opacity=0.25)
        curve = _prediction_curve(noise=noise, color=color).scale(0.46).move_to(mesh)
        glow = _prediction_curve(noise=0.0, color=OPERATOR).scale(0.46).move_to(mesh).set_stroke(opacity=0.24, width=5.5)
        tag = Chip(label, max_width=0.90, height=0.32, stroke_color=color, font_size=10, min_font_size=8, padding=0.05)
        tile = VGroup(mesh, glow, curve)
        body = VGroup(tile, tag).arrange(DOWN, buff=0.06)
        panels.add(body)
        meshes.add(mesh)
        prediction_curves.add(curve)
    arrows = VGroup(
        Arrow(panels[0].get_right() + RIGHT * 0.03, panels[1].get_left() + LEFT * 0.03, buff=0.02, color=OPERATOR, stroke_width=1.6),
        Arrow(panels[1].get_right() + RIGHT * 0.03, panels[2].get_left() + LEFT * 0.03, buff=0.02, color=OPERATOR, stroke_width=1.6),
    )
    panels.arrange(RIGHT, buff=0.28)
    arrows[0].put_start_and_end_on(panels[0].get_right() + RIGHT * 0.03, panels[1].get_left() + LEFT * 0.03)
    arrows[1].put_start_and_end_on(panels[1].get_right() + RIGHT * 0.03, panels[2].get_left() + LEFT * 0.03)
    check = _checkmark().scale(0.78)
    check.next_to(panels[2], RIGHT, buff=0.08)
    visual = VGroup(panels, arrows, check)
    visual.limit_curve = prediction_curves[2]
    visual.meshes = meshes
    visual.prediction_curves = prediction_curves
    return visual


def make_property_cards(empty=False):
    titles = (
        ("Input: many discretizations", SCIENCE, make_input_discretization_visual),
        ("Output: query anywhere", OUTPUT, make_output_query_visual),
        ("Refinement: stable limit", NVIDIA_GREEN, make_refinement_limit_visual),
    )
    cards = VGroup()
    for title, accent, factory in titles:
        body = VGroup() if empty else factory().scale(0.84)
        card = PanelCard(title, body=body, width=4.25, height=3.15, accent_color=accent, title_font_size=21)
        cards.add(card)
    cards.arrange(RIGHT, buff=0.34).move_to(DOWN * 0.32)
    cards.input_card = cards[0]
    cards.output_card = cards[1]
    cards.refinement_card = cards[2]
    return cards


def make_architecture_constraints():
    center = Chip("Architecture constraints", max_width=3.35, height=0.62, stroke_color=OPERATOR, font_size=20)
    top = Chip("coordinate-aware", max_width=2.50, height=0.42, stroke_color=SCIENCE, font_size=16)
    mid = Chip("quadrature-aware", max_width=2.45, height=0.42, stroke_color=INPUT, font_size=16)
    right = Chip("output as function u(y)", max_width=2.95, height=0.42, stroke_color=OUTPUT, font_size=16)
    bottom = Chip("continuum operation", max_width=2.70, height=0.42, stroke_color=NVIDIA_GREEN, font_size=16)
    left_group = VGroup(top, mid).arrange(DOWN, buff=0.20)
    left_group.next_to(center, LEFT, buff=0.78)
    right.next_to(center, RIGHT, buff=0.78)
    bottom.next_to(center, DOWN, buff=0.52)
    arrows = VGroup(
        Arrow(left_group.get_right(), center.get_left(), buff=0.08, color=SCIENCE, stroke_width=2.0),
        Arrow(right.get_left(), center.get_right(), buff=0.08, color=OUTPUT, stroke_width=2.0),
        Arrow(bottom.get_top(), center.get_bottom(), buff=0.08, color=NVIDIA_GREEN, stroke_width=2.0),
    )
    source_hints = VGroup(
        Chip("many discretizations", max_width=2.70, height=0.40, stroke_color=SCIENCE, font_size=15),
        Chip("query anywhere", max_width=2.25, height=0.40, stroke_color=OUTPUT, font_size=15),
        Chip("stable limit", max_width=1.85, height=0.40, stroke_color=NVIDIA_GREEN, font_size=15),
    ).arrange(RIGHT, buff=0.44)
    source_hints.next_to(VGroup(left_group, center, right), UP, buff=0.48)
    hints_arrows = VGroup(
        Arrow(source_hints[0].get_bottom(), left_group.get_top(), buff=0.06, color=SCIENCE, stroke_width=1.5),
        Arrow(source_hints[1].get_bottom(), right.get_top(), buff=0.06, color=OUTPUT, stroke_width=1.5),
        Arrow(source_hints[2].get_bottom(), bottom.get_top(), buff=0.06, color=NVIDIA_GREEN, stroke_width=1.5),
    )
    constraints = VGroup(source_hints, hints_arrows, left_group, right, bottom, arrows, center).move_to(ORIGIN)
    constraints.center_node = center
    return constraints


def _small_matrix(rows=4, cols=4, cell=0.28, color=INPUT):
    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            rect = Square(side_length=cell, stroke_color=GRID, stroke_width=0.65, fill_color=CARD_BG, fill_opacity=0.70)
            rect.move_to([(j - (cols - 1) / 2) * cell, ((rows - 1) / 2 - i) * cell, 0])
            if i == 1 or j == 2:
                rect.set_fill(color, opacity=0.38)
                rect.set_stroke(color, opacity=0.75)
            cells.add(rect)
    return cells


def make_matrix_vs_continuum_view():
    matrix = _small_matrix(rows=5, cols=5, color=WARNING)
    matrix_label = SafeText("K_ij on fixed grid", max_width=2.55, max_height=0.32, font_size=19, color=TEXT, weight="BOLD")
    lock = SafeText("lock", max_width=0.48, max_height=0.24, font_size=14, color=WARNING, weight="BOLD")
    fixed = Chip("fixed index", max_width=1.72, height=0.40, stroke_color=WARNING, font_size=15)
    lock_group = VGroup(lock, fixed).arrange(RIGHT, buff=0.10)
    left_panel = PanelCard("grid-bound layer", body=VGroup(matrix, matrix_label, lock_group).arrange(DOWN, buff=0.18), width=4.60, height=3.55, accent_color=WARNING, title_font_size=23)

    blob = Ellipse(width=2.35, height=1.38, stroke_color=NVIDIA_GREEN, stroke_width=1.8, fill_color="#102514", fill_opacity=0.42)
    curves = VGroup(
        _make_curve(width=1.18, phase=0.2, color=SCIENCE, stroke_width=2.0).scale(0.70),
        _make_curve(width=1.18, phase=0.8, color=PURPLE, stroke_width=2.0).scale(0.70).shift(DOWN * 0.12),
    )
    curves.move_to(blob).shift(DOWN * 0.02)
    function_blob = VGroup(blob, curves)
    continuum = Chip("continuum operation", max_width=2.55, height=0.44, stroke_color=NVIDIA_GREEN, font_size=16)
    integral = Chip("integral operator", max_width=2.20, height=0.44, stroke_color=OPERATOR, font_size=16)
    right_panel = PanelCard("function-space layer", body=VGroup(function_blob, continuum, integral).arrange(DOWN, buff=0.18), width=4.60, height=3.55, accent_color=NVIDIA_GREEN, title_font_size=23)

    row = VGroup(left_panel, right_panel).arrange(RIGHT, buff=1.20)
    arrow = Arrow(left_panel.get_right() + RIGHT * 0.14, right_panel.get_left() + LEFT * 0.14, buff=0.04, color=OPERATOR, stroke_width=2.6)
    label = Chip("more natural for functions", max_width=3.10, height=0.44, stroke_color=OPERATOR, font_size=16)
    label.next_to(arrow, UP, buff=0.12)
    view = VGroup(row, arrow, label).move_to(ORIGIN)
    view.matrix_panel = left_panel
    view.continuum_panel = right_panel
    view.continuum_blob = blob
    view.continuum_curves = curves
    return view


def _vector_column(symbol, color=INPUT):
    cells = VGroup()
    for sub in ("1", "2", "j", "n"):
        box = RoundedRectangle(width=0.58, height=0.42, corner_radius=0.04, stroke_color=color, stroke_width=1.0, fill_color="#0D1B2A", fill_opacity=0.78)
        label = SafeMathTex(fr"{symbol}_{sub}", max_width=0.42, max_height=0.26, font_size=22, color=TEXT)
        label.move_to(box)
        cells.add(VGroup(box, label))
    dots = VGroup(Dot(radius=0.025, color=MUTED), Dot(radius=0.025, color=MUTED)).arrange(DOWN, buff=0.055)
    return VGroup(cells[:2], dots, cells[2:]).arrange(DOWN, buff=0.09)


def make_neural_layer_zoom():
    title = SafeText("Neural network layer", max_width=4.2, max_height=0.46, font_size=30, color=INPUT, weight="BOLD")
    input_col = _vector_column("a", color=INPUT)
    output_col = _vector_column("v", color=OUTPUT)
    matrix = _small_matrix(rows=5, cols=5, cell=0.32, color=OPERATOR)
    matrix_box = RoundedRectangle(width=2.25, height=2.25, corner_radius=0.07, stroke_color=OPERATOR, stroke_width=1.4, fill_color=CARD_BG, fill_opacity=0.45)
    matrix_label = SafeMathTex(r"K_{ij}", max_width=0.78, max_height=0.42, font_size=32, color=OPERATOR)
    matrix_block = VGroup(matrix_box, matrix, matrix_label)
    matrix_label.move_to(matrix_box)
    row = VGroup(input_col, matrix_block, output_col).arrange(RIGHT, buff=0.82)
    left_arrow = Arrow(input_col.get_right() + RIGHT * 0.08, matrix_block.get_left() + LEFT * 0.08, buff=0.02, color=INPUT, stroke_width=2.2)
    right_arrow = Arrow(matrix_block.get_right() + RIGHT * 0.08, output_col.get_left() + LEFT * 0.08, buff=0.02, color=OUTPUT, stroke_width=2.2)
    teaser = Chip("Next: view this layer as a Riemann sum", max_width=5.25, height=0.54, stroke_color=OPERATOR, font_size=19)
    formula = make_formula_badge(r"a_j \quad\to\quad K_{ij}\quad\to\quad v_i", max_width=5.10, height=0.58, stroke_color=GRID, font_size=25)
    layer = VGroup(title, VGroup(row, left_arrow, right_arrow), formula, teaser).arrange(DOWN, buff=0.30).move_to(ORIGIN)
    layer.input_column = input_col
    layer.matrix_block = matrix_block
    layer.output_column = output_col
    layer.left_arrow = left_arrow
    layer.right_arrow = right_arrow
    return layer


class Scene0602ThreeDesiredProperties(TimedScene):
    SCRIPT_ID = "6.2"
    SCRIPT_TITLE = "Three desired properties"
    SCRIPT_START = 36 * 60 + 45
    SCRIPT_END = 38 * 60 + 40
    SCENE_DURATION = 115.0

    KEYFRAMES = (
        "KF01 0.0s title and empty property cards",
        "KF02 10.5s input discretization property",
        "KF03 21.5s output query property",
        "KF04 33.0s refinement stable limit property",
        "KF05 49.0s cards become architecture constraints",
        "KF06 63.5s fixed-index matrix contrasted with continuum operation",
        "KF07 77.5s neural network layer teaser for Riemann sum",
    )

    def construct(self):
        background = make_background_network(seed=6202, n=68, dot_opacity=0.10, line_opacity=0.07)
        self.add(background)

        title = SafeText("Three properties of a good Neural Operator", max_width=9.9, max_height=0.58, font_size=34, color=TEXT, weight="BOLD")
        title.to_edge(UP, buff=0.42)
        empty_cards = make_property_cards(empty=True)
        filled_cards = make_property_cards(empty=False)
        property_bodies = VGroup(filled_cards[0].body, filled_cards[1].body, filled_cards[2].body)
        constraints = make_architecture_constraints()
        matrix_vs_continuum = make_matrix_vs_continuum_view()
        layer_zoom = make_neural_layer_zoom()

        assert_in_frame(VGroup(title, empty_cards), margin=0.24, label="initial_property_cards")
        assert_in_frame(filled_cards, margin=0.24, label="filled_property_cards")
        assert_in_frame(constraints, margin=0.24, label="architecture_constraints")
        assert_in_frame(matrix_vs_continuum, margin=0.24, label="matrix_vs_continuum")
        assert_in_frame(layer_zoom, margin=0.24, label="neural_layer_zoom")
        assert_no_group_overlap(list(filled_cards), min_gap=0.06)

        # VO exact: Một neural operator tốt cần ít nhất ba property.
        # Global 36:45.0-36:55.5 => 36:45.0 -> local 0.0, 36:55.5 -> local 10.5
        self.play_timed(
            "introduce_three_property_frames",
            0.0,
            10.5,
            FadeIn(title, shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in empty_cards], lag_ratio=0.18),
        )

        # VO exact: Thứ nhất: input có thể được cung cấp ở nhiều discretization.
        # Global 36:55.5-37:06.5 => 36:55.5 -> local 10.5, 37:06.5 -> local 21.5
        self.play_timed(
            "fill_input_many_discretizations",
            10.5,
            21.5,
            FadeIn(filled_cards[0].body, shift=UP * 0.04),
            Circumscribe(filled_cards[0].body.checkmark, color=NVIDIA_GREEN, buff=0.05),
        )

        # VO exact: Thứ hai: output có thể query ở các điểm ta muốn, không bị khóa vào một grid duy nhất.
        # Global 37:06.5-37:18.0 => 37:06.5 -> local 21.5, 37:18.0 -> local 33.0
        self.play_timed(
            "fill_output_query_anywhere",
            21.5,
            33.0,
            FadeIn(filled_cards[1].body, shift=UP * 0.04),
            LaggedStart(*[Indicate(dot, color=OPERATOR, scale_factor=1.25) for dot in filled_cards[1].body.query_dots], lag_ratio=0.20),
        )

        # VO exact: Thứ ba: khi mesh refinement tiến dần về continuum, model converges về một operator limit nhất quán.
        # Global 37:18.0-37:33.0 => 37:18.0 -> local 33.0, 37:33.0 -> local 48.0
        self.play_timed(
            "fill_refinement_stable_limit",
            33.0,
            48.0,
            FadeIn(filled_cards[2].body, shift=UP * 0.04),
            Circumscribe(filled_cards[2].body.limit_curve, color=NVIDIA_GREEN, buff=0.08),
        )

        # Pause exact: 1.0s.
        # Global 37:33.0-37:34.0 => 37:33.0 -> local 48.0, 37:34.0 -> local 49.0
        self.wait_timed("hold_three_properties", 48.0, 49.0)

        # VO exact: Đây là lý do các operation bên trong model thường được xây như xấp xỉ của operation continuum.
        # Global 37:34.0-37:48.5 => 37:34.0 -> local 49.0, 37:48.5 -> local 63.5
        self.play_timed(
            "compress_cards_into_architecture_constraints",
            49.0,
            53.0,
            FadeOut(title, shift=UP * 0.05),
            FadeOut(empty_cards, scale=0.96),
            FadeOut(property_bodies, scale=0.96),
            FadeIn(constraints, shift=DOWN * 0.06),
        )
        self.wait_timed("hold_architecture_constraints", 53.0, 63.5)

        # VO exact: Matrix multiplication trên index cố định không đủ tự nhiên. Integral operator thì tự nhiên hơn.
        # Global 37:48.5-38:02.5 => 37:48.5 -> local 63.5, 38:02.5 -> local 77.5
        self.play_timed(
            "contrast_fixed_index_matrix_with_continuum_operation",
            63.5,
            67.0,
            FadeOut(constraints, shift=UP * 0.05),
            FadeIn(matrix_vs_continuum, shift=UP * 0.06),
        )
        self.wait_timed("hold_matrix_vs_continuum_contrast", 67.0, 77.5)

        # VO exact: Vậy để xây neural operator từ neural network, ta cần một trick đẹp: nhìn lại một layer neural network như một Riemann sum.
        # Global 38:02.5-38:40.0 => 38:02.5 -> local 77.5, 38:40.0 -> local 115.0
        self.play_timed(
            "move_into_neural_network_layer",
            77.5,
            86.0,
            FadeOut(matrix_vs_continuum, shift=LEFT * 0.08),
            FadeIn(layer_zoom, shift=RIGHT * 0.08),
        )
        self.play_timed(
            "hold_layer_as_riemann_sum_teaser",
            86.0,
            114.8,
            layer_zoom.matrix_block.animate.set_opacity(0.78),
            Indicate(layer_zoom[3], color=OPERATOR, scale_factor=1.02),
            rate_func=there_and_back,
        )

        self.pad_to(self.SCENE_DURATION)
