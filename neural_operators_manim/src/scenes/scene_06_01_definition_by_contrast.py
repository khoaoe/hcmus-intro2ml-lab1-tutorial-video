"""
Scene 6.1 - Definition by contrast
Script: ../docs/full_voice_manim_script.md
Global time: 35:00.0-36:45.0
Local duration: 105.0s
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
from src.common.panels import Chip, make_formula_badge
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    OPERATOR,
    OUTPUT,
    PURPLE,
    SCIENCE,
    TEXT,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame, assert_no_group_overlap


apply_global_config()


VO_LINES = (
    (0.0, 13.0, "Neural network truyền thống học một function giữa finite-dimensional spaces: vector vào, vector ra."),
    (13.0, 28.0, "Neural operator học một operator giữa function spaces: input là function, output cũng là function."),
    (28.0, 29.0, "Pause: 1.0s."),
    (29.0, 43.0, "Nếu neural network hỏi: “given vector x, y là gì?”, neural operator hỏi: “given function a, function u là gì?”"),
    (43.0, 57.0, "Ở đây a có thể là coefficient field, geometry field, initial condition, hoặc trạng thái hệ thống."),
    (57.0, 72.0, "u có thể là solution field, future state, wave propagation, pressure distribution, hoặc displacement field."),
    (72.0, 105.0, "Cốt lõi không phải tên biến. Cốt lõi là map từ một object vô hạn chiều sang một object vô hạn chiều khác."),
)


def make_vector_column(label, values, accent=INPUT):
    cells = VGroup()
    for value in values:
        box = RoundedRectangle(
            width=0.58,
            height=0.42,
            corner_radius=0.04,
            stroke_color=accent,
            stroke_width=1.0,
            fill_color="#0D1B2A",
            fill_opacity=0.78,
        )
        text = SafeMathTex(value, max_width=0.42, max_height=0.28, font_size=24, color=TEXT)
        text.move_to(box)
        cells.add(VGroup(box, text))
    cells.arrange(DOWN, buff=0.08)
    dots = VGroup(
        Dot(radius=0.028, color=MUTED),
        Dot(radius=0.028, color=MUTED),
        Dot(radius=0.028, color=MUTED),
    ).arrange(DOWN, buff=0.06)
    label_mob = SafeText(label, max_width=1.35, max_height=0.28, font_size=18, color=accent, weight="BOLD")
    column = VGroup(label_mob, cells[:2], dots, cells[2:]).arrange(DOWN, buff=0.12)
    column.label_mob = label_mob
    column.cells = cells
    return column


def make_finite_node_graph():
    layer_specs = [3, 4, 3]
    layers = VGroup()
    for layer_index, count in enumerate(layer_specs):
        layer = VGroup(
            *[
                Circle(radius=0.095, stroke_color=OPERATOR, stroke_width=1.3, fill_color=CARD_BG, fill_opacity=0.92)
                for _ in range(count)
            ]
        ).arrange(DOWN, buff=0.22)
        layer.shift(RIGHT * (layer_index - 1) * 0.62)
        layers.add(layer)
    edges = VGroup()
    for left_layer, right_layer in zip(layers[:-1], layers[1:]):
        for start in left_layer:
            for end in right_layer:
                edges.add(
                    Line(
                        start.get_center(),
                        end.get_center(),
                        color=GRID,
                        stroke_width=0.75,
                        stroke_opacity=0.60,
                    )
                )
    block = RoundedRectangle(
        width=2.05,
        height=2.15,
        corner_radius=0.08,
        stroke_color=OPERATOR,
        stroke_width=1.2,
        fill_color="#15192A",
        fill_opacity=0.76,
    )
    label = SafeText("finite layers", max_width=1.65, max_height=0.26, font_size=17, color=OPERATOR)
    label.next_to(block, DOWN, buff=0.10)
    return VGroup(block, edges, layers, label)


def make_neural_network_diagram():
    title = SafeText("Neural Network", max_width=3.0, max_height=0.40, font_size=27, color=INPUT, weight="BOLD")
    formula = make_formula_badge(r"f:\mathbb{R}^n\to\mathbb{R}^m", max_width=3.15, height=0.58, stroke_color=INPUT, font_size=27)
    title_group = VGroup(title, formula).arrange(DOWN, buff=0.14)

    x_col = make_vector_column("vector x", [r"x_1", r"x_2", r"x_n"], accent=INPUT)
    y_col = make_vector_column("vector y", [r"y_1", r"y_2", r"y_m"], accent=OUTPUT)
    graph = make_finite_node_graph()
    row = VGroup(x_col, graph, y_col).arrange(RIGHT, buff=0.42)
    arrows = VGroup(
        Arrow(x_col.get_right() + RIGHT * 0.06, graph.get_left() + LEFT * 0.06, buff=0.02, color=INPUT, stroke_width=2.0),
        Arrow(graph.get_right() + RIGHT * 0.06, y_col.get_left() + LEFT * 0.06, buff=0.02, color=OUTPUT, stroke_width=2.0),
    )
    caption = Chip("finite vector map", max_width=2.25, height=0.42, stroke_color=INPUT, font_size=17)
    diagram = VGroup(title_group, VGroup(row, arrows), caption).arrange(DOWN, buff=0.30)
    diagram.move_to(LEFT * 4.0 + DOWN * 0.04)
    diagram.x_col = x_col
    diagram.y_col = y_col
    diagram.graph = graph
    diagram.formula = formula
    return diagram


def _curve_points(seed, width, height, phase=0.0, count=7):
    rng = np.random.default_rng(seed)
    xs = np.linspace(-0.32 * width, 0.32 * width, count)
    amp = rng.uniform(0.07, 0.13) * height
    freq = rng.uniform(1.3, 2.2)
    offset = rng.uniform(-0.12, 0.12) * height
    rx = width / 2 - 0.16
    ry = height / 2 - 0.16
    points = []
    for x in xs:
        y = offset + amp * np.sin(freq * x + phase) + 0.06 * height * np.cos(1.8 * x - phase)
        y_limit = 0.66 * ry * np.sqrt(max(0.0, 1.0 - (x / rx) ** 2))
        y = float(np.clip(y, -y_limit, y_limit))
        points.append([x, y, 0])
    return points


def make_function_space_blob(label, center, accent=SCIENCE, seed=11, phase=0.0):
    width = 1.82
    height = 2.58
    blob = Ellipse(
        width=width,
        height=height,
        stroke_color=accent,
        stroke_width=1.6,
        fill_color="#102336",
        fill_opacity=0.42,
    )
    halo = Ellipse(
        width=width + 0.18,
        height=height + 0.18,
        stroke_color=accent,
        stroke_width=0.8,
        stroke_opacity=0.28,
    )
    curves = VGroup()
    colors = [accent, INPUT, PURPLE]
    for index in range(3):
        curve = smooth_path(
            _curve_points(seed + index * 13, width, height, phase=phase + index * 0.55),
            color=colors[index],
            stroke_width=2.2,
            stroke_opacity=0.86,
        )
        curve.shift(DOWN * (0.12 * (index - 1)))
        curves.add(curve)
    label_mob = SafeMathTex(label, max_width=0.50, max_height=0.36, font_size=29, color=TEXT)
    label_mob.move_to(blob.get_top() + DOWN * 0.34)
    group = VGroup(halo, blob, curves, label_mob).move_to(center)
    group.blob = blob
    group.curves = curves
    group.label_mob = label_mob
    return group


def make_neural_operator_diagram():
    title = SafeText("Neural Operator", max_width=3.25, max_height=0.40, font_size=27, color=OPERATOR, weight="BOLD")
    formula = make_formula_badge(r"\mathcal{G}:\mathcal{A}\to\mathcal{U}", max_width=3.10, height=0.58, stroke_color=OPERATOR, font_size=27)
    title_group = VGroup(title, formula).arrange(DOWN, buff=0.14)

    space_a = make_function_space_blob(r"\mathcal{A}", LEFT * 1.55, accent=SCIENCE, seed=601, phase=0.0)
    space_u = make_function_space_blob(r"\mathcal{U}", RIGHT * 1.55, accent=OUTPUT, seed=701, phase=0.8)
    arrow = Arrow(space_a.get_right() + RIGHT * 0.10, space_u.get_left() + LEFT * 0.10, buff=0.05, color=OPERATOR, stroke_width=2.4)
    arrow_label = SafeMathTex(r"\mathcal{G}", max_width=0.42, max_height=0.34, font_size=27, color=OPERATOR)
    arrow_label.next_to(arrow, UP, buff=0.08)
    body = VGroup(space_a, VGroup(arrow, arrow_label), space_u)
    caption = Chip("function-space map", max_width=2.55, height=0.42, stroke_color=OPERATOR, font_size=17)
    diagram = VGroup(title_group, body, caption).arrange(DOWN, buff=0.24)
    diagram.move_to(RIGHT * 4.0 + DOWN * 0.02)
    diagram.space_a = space_a
    diagram.space_u = space_u
    diagram.arrow = arrow
    diagram.arrow_label = arrow_label
    diagram.formula = formula
    diagram.curves = VGroup(space_a.curves, space_u.curves)
    return diagram


def make_question_cards():
    left = Chip("given vector x → y?", max_width=3.10, height=0.52, stroke_color=INPUT, font_size=19)
    right = Chip("given function a → function u?", max_width=3.85, height=0.52, stroke_color=OPERATOR, font_size=18)
    left.move_to(LEFT * 4.0 + DOWN * 3.55)
    right.move_to(RIGHT * 4.0 + DOWN * 3.55)
    cards = VGroup(left, right)
    assert_no_group_overlap([left, right], min_gap=0.10)
    return cards


def make_input_chips(no_diagram):
    x = no_diagram.space_a.get_left()[0] - 1.03
    chips = VGroup(
        Chip("coefficient field", max_width=1.96, height=0.40, stroke_color=SCIENCE, font_size=14),
        Chip("geometry field", max_width=1.72, height=0.40, stroke_color=SCIENCE, font_size=14),
        Chip("initial condition", max_width=1.94, height=0.40, stroke_color=SCIENCE, font_size=14),
        Chip("system state", max_width=1.62, height=0.40, stroke_color=SCIENCE, font_size=14),
    )
    for chip, y in zip(chips, [0.86, 0.34, -0.18, -0.70]):
        chip.move_to([x, y, 0])
    assert_no_group_overlap(list(chips), min_gap=0.03)
    assert_no_group_overlap([*list(chips), no_diagram.space_a.blob, no_diagram.formula], min_gap=0.02)
    return chips


def make_output_chips(no_diagram):
    x = no_diagram.space_u.get_center()[0]
    chips = VGroup(
        Chip("solution field", max_width=1.62, height=0.38, stroke_color=OUTPUT, font_size=14),
        Chip("future state", max_width=1.48, height=0.38, stroke_color=OUTPUT, font_size=14),
        Chip("wave", max_width=0.92, height=0.38, stroke_color=OUTPUT, font_size=14),
        Chip("pressure", max_width=1.16, height=0.38, stroke_color=OUTPUT, font_size=14),
        Chip("displacement", max_width=1.58, height=0.38, stroke_color=OUTPUT, font_size=14),
    )
    chips[0].move_to([x - 1.75, -1.86, 0])
    chips[1].move_to([x - 0.10, -1.86, 0])
    chips[2].move_to([x + 1.25, -1.86, 0])
    chips[3].move_to([x - 0.76, -2.34, 0])
    chips[4].move_to([x + 0.84, -2.34, 0])
    assert_no_group_overlap(list(chips), min_gap=0.03)
    assert_no_group_overlap([*list(chips), no_diagram.space_u.blob, no_diagram.formula], min_gap=0.02)
    return chips


def make_final_focus():
    formula = make_formula_badge(r"\mathcal{G}:\mathcal{A}\to\mathcal{U}", max_width=3.10, height=0.58, stroke_color=OPERATOR, font_size=28)
    statement_text = "infinite-dimensional object → infinite-dimensional object"
    source = Chip("infinite-dimensional object", max_width=2.48, height=0.46, stroke_color=SCIENCE, font_size=14)
    target = Chip("infinite-dimensional object", max_width=2.48, height=0.46, stroke_color=OUTPUT, font_size=14)
    source.move_to(LEFT * 1.58)
    target.move_to(RIGHT * 1.58)
    map_arrow = Arrow(
        source.get_right() + RIGHT * 0.06,
        target.get_left() + LEFT * 0.06,
        buff=0,
        color=OPERATOR,
        stroke_width=2.1,
        max_tip_length_to_length_ratio=0.18,
    )
    mapping = VGroup(source, map_arrow, target)
    statement_box = RoundedRectangle(
        width=5.95,
        height=0.96,
        corner_radius=0.08,
        stroke_color=OPERATOR,
        stroke_width=1.2,
        fill_color=CARD_BG,
        fill_opacity=0.86,
    )
    mapping.move_to(statement_box)
    sentence = VGroup(statement_box, mapping)
    sentence.source_box = source
    sentence.target_box = target
    sentence.map_arrow = map_arrow
    final = VGroup(formula, sentence).arrange(DOWN, buff=0.12)
    final.move_to(RIGHT * 4.0 + DOWN * 3.12)
    return final


class Scene0601DefinitionByContrast(TimedScene):
    SCRIPT_ID = "6.1"
    SCRIPT_TITLE = "Definition by contrast"
    SCRIPT_START = 35 * 60
    SCRIPT_END = 36 * 60 + 45
    SCENE_DURATION = 105.0

    KEYFRAMES = (
        "KF01 0.0s left neural network vector map only",
        "KF02 13.0s right neural operator function-space map appears",
        "KF03 29.0s compact contrast questions",
        "KF04 43.0s input function-space examples around A",
        "KF05 57.0s output function-space examples around U",
        "KF06 72.0s neural operator focus with infinite-dimensional formula",
    )

    def construct(self):
        background = make_background_network(seed=6101, n=62, dot_opacity=0.10, line_opacity=0.07)
        divider = Line(UP * 3.86, DOWN * 3.86, color=GRID, stroke_width=1.2, stroke_opacity=0.72)
        self.add(background)

        nn_diagram = make_neural_network_diagram()
        no_diagram = make_neural_operator_diagram()
        question_cards = make_question_cards()
        input_chips = make_input_chips(no_diagram)
        output_chips = make_output_chips(no_diagram)
        final_focus = make_final_focus()

        assert_in_frame(VGroup(divider, nn_diagram), margin=0.24, label="left_nn_diagram")
        assert_in_frame(no_diagram, margin=0.24, label="right_no_diagram")
        assert_in_frame(question_cards, margin=0.24, label="question_cards")
        assert_in_frame(VGroup(no_diagram, input_chips), margin=0.18, label="input_chips_layout")
        assert_in_frame(VGroup(no_diagram, output_chips), margin=0.18, label="output_chips_layout")
        assert_in_frame(VGroup(no_diagram.copy().scale(1.08).shift(UP * 0.12), final_focus), margin=0.18, label="final_focus_layout")

        # VO exact: Neural network truyền thống học một function giữa finite-dimensional spaces: vector vào, vector ra.
        # Global 35:00.0-35:13.0 => 35:00.0 -> local 0.0, 35:13.0 -> local 13.0
        self.play_timed(
            "build_left_neural_network_vector_map",
            0.0,
            11.8,
            FadeIn(divider, shift=DOWN * 0.04),
            FadeIn(nn_diagram[0], shift=DOWN * 0.08),
            LaggedStart(
                FadeIn(nn_diagram.x_col, shift=RIGHT * 0.08),
                FadeIn(nn_diagram.graph, shift=UP * 0.06),
                FadeIn(nn_diagram.y_col, shift=LEFT * 0.08),
                lag_ratio=0.24,
            ),
        )
        self.play_timed(
            "emphasize_vector_in_vector_out",
            11.8,
            13.0,
            FadeIn(nn_diagram[2], shift=UP * 0.05),
            Circumscribe(VGroup(nn_diagram.x_col, nn_diagram.y_col), color=INPUT, buff=0.10),
        )

        # VO exact: Neural operator học một operator giữa function spaces: input là function, output cũng là function.
        # Global 35:13.0-35:28.0 => 35:13.0 -> local 13.0, 35:28.0 -> local 28.0
        self.play_timed(
            "bring_neural_operator_online",
            13.0,
            26.8,
            FadeIn(no_diagram[0], shift=DOWN * 0.08),
            LaggedStart(
                FadeIn(no_diagram.space_a, shift=RIGHT * 0.06),
                GrowArrow(no_diagram.arrow),
                FadeIn(no_diagram.arrow_label, shift=UP * 0.04),
                FadeIn(no_diagram.space_u, shift=LEFT * 0.06),
                lag_ratio=0.22,
            ),
        )
        self.play_timed(
            "emphasize_function_in_function_out",
            26.8,
            28.0,
            FadeIn(no_diagram[2], shift=UP * 0.05),
            Indicate(no_diagram.space_a.blob, color=SCIENCE, scale_factor=1.01),
            Indicate(no_diagram.space_u.blob, color=OUTPUT, scale_factor=1.01),
        )

        # Pause exact: 1.0s.
        # Global 35:28.0-35:29.0 => 35:28.0 -> local 28.0, 35:29.0 -> local 29.0
        self.play_timed(
            "pause_subtle_curve_breath",
            28.0,
            28.7,
            no_diagram.curves.animate.shift(UP * 0.035),
            rate_func=there_and_back,
        )
        self.wait_timed("pause_hold_definition_contrast", 28.7, 29.0)

        # VO exact: Nếu neural network hỏi: “given vector x, y là gì?”, neural operator hỏi: “given function a, function u là gì?”
        # Global 35:29.0-35:43.0 => 35:29.0 -> local 29.0, 35:43.0 -> local 43.0
        self.play_timed(
            "add_question_cards",
            29.0,
            34.2,
            FadeIn(question_cards, shift=UP * 0.08),
        )
        self.play_timed(
            "contrast_questions_left_and_right",
            34.2,
            43.0,
            Circumscribe(question_cards[0], color=INPUT, buff=0.06),
            Circumscribe(question_cards[1], color=OPERATOR, buff=0.06),
            no_diagram.curves.animate.shift(DOWN * 0.035),
            rate_func=there_and_back,
        )

        # VO exact: Ở đây a có thể là coefficient field, geometry field, initial condition, hoặc trạng thái hệ thống.
        # Global 35:43.0-35:57.0 => 35:43.0 -> local 43.0, 35:57.0 -> local 57.0
        self.play_timed(
            "highlight_input_space_examples",
            43.0,
            48.2,
            Circumscribe(no_diagram.space_a.blob, color=SCIENCE, buff=0.08),
        )
        self.play_timed(
            "show_input_example_chips",
            48.2,
            57.0,
            LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in input_chips], lag_ratio=0.16),
        )

        # VO exact: u có thể là solution field, future state, wave propagation, pressure distribution, hoặc displacement field.
        # Global 35:57.0-36:12.0 => 35:57.0 -> local 57.0, 36:12.0 -> local 72.0
        self.play_timed(
            "highlight_output_space_examples",
            57.0,
            62.2,
            FadeOut(no_diagram[2], shift=DOWN * 0.03),
            Circumscribe(no_diagram.space_u.blob, color=OUTPUT, buff=0.08),
        )
        no_diagram[2].set_opacity(0)
        self.play_timed(
            "show_output_example_chips",
            62.2,
            72.0,
            LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in output_chips], lag_ratio=0.13),
        )

        # VO exact: Cốt lõi không phải tên biến. Cốt lõi là map từ một object vô hạn chiều sang một object vô hạn chiều khác.
        # Global 36:12.0-36:45.0 => 36:12.0 -> local 72.0, 36:45.0 -> local 105.0
        self.play_timed(
            "focus_neural_operator_and_dim_neural_network",
            72.0,
            76.4,
            nn_diagram.animate.set_opacity(0.40),
            FadeOut(question_cards, shift=DOWN * 0.04),
            FadeOut(input_chips, shift=DOWN * 0.05),
            FadeOut(output_chips, shift=DOWN * 0.05),
            no_diagram.animate.scale(1.08).shift(UP * 0.12),
        )
        self.play_timed(
            "show_final_infinite_dimensional_formula",
            76.4,
            84.0,
            FadeIn(final_focus, shift=UP * 0.08),
            Circumscribe(final_focus[1], color=OPERATOR, buff=0.08),
        )
        self.play_timed(
            "hold_final_function_space_map",
            84.0,
            104.8,
            no_diagram.curves.animate.shift(UP * 0.04),
            Indicate(no_diagram.arrow_label, color=OPERATOR, scale_factor=1.08),
            rate_func=there_and_back,
        )

        # Manim partial-clip concatenation adds four frames at 20fps for this scene.
        # Rendered duration still lands on Global 36:45.0 -> local 105.0.
        self.t = self.SCENE_DURATION
        self.pad_to(self.SCENE_DURATION)
