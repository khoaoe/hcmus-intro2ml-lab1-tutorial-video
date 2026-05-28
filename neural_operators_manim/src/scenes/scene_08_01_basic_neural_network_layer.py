"""
Scene 8.1 - A basic neural network layer
Script: ../docs/full_voice_manim_script.md
Global time: 46:20.0-47:50.0
Local duration: 90.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
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
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame, assert_no_group_overlap


apply_global_config()


DOMAIN_START = 0.0
DOMAIN_END = 6.0
SAMPLE_XS = (0.65, 1.55, 3.45, 5.35)
SAMPLE_NAMES = ("x_1", "x_2", "x_j", "x_n")
ENTRY_NAMES = ("a_1", "a_2", "a_j", "a_n")


def sample_function(x):
    return 1.12 + 0.40 * np.sin(1.05 * x - 0.35) + 0.16 * np.cos(2.20 * x + 0.55)


def make_layer_chain():
    vector_label = SafeText("input vector", max_width=2.2, max_height=0.38, font_size=20, color=MUTED)
    matrix_label = SafeText("weight matrix", max_width=2.5, max_height=0.38, font_size=20, color=MUTED)
    activation_label = SafeText("activation", max_width=2.0, max_height=0.38, font_size=20, color=MUTED)

    vector_chip = Chip("a", max_width=0.90, height=0.50, stroke_color=INPUT, font_size=24)
    matrix_chip = Chip("K", max_width=0.90, height=0.50, stroke_color=OPERATOR, font_size=24)
    sigma_chip = Chip("sigma", max_width=1.18, height=0.50, stroke_color=OUTPUT, font_size=21)

    chips = VGroup(vector_chip, matrix_chip, sigma_chip).arrange(RIGHT, buff=1.10)
    arrow_1 = Arrow(vector_chip.get_right(), matrix_chip.get_left(), buff=0.18, color=GRID, stroke_width=2.2)
    arrow_2 = Arrow(matrix_chip.get_right(), sigma_chip.get_left(), buff=0.18, color=GRID, stroke_width=2.2)

    chain = VGroup(chips, arrow_1, arrow_2)
    labels = VGroup(vector_label, matrix_label, activation_label)
    for label, chip in zip(labels, (vector_chip, matrix_chip, sigma_chip)):
        label.next_to(chip, DOWN, buff=0.13)

    chain_group = VGroup(chain, labels).move_to(UP * 2.95)
    chain_group.vector_chip = vector_chip
    chain_group.matrix_chip = matrix_chip
    chain_group.sigma_chip = sigma_chip
    chain_group.arrows = VGroup(arrow_1, arrow_2)
    chain_group.labels = labels
    return chain_group


def make_column_vector():
    exact_header = MathTex(
        r"{{a}}",
        r"=",
        r"\big[{{a_1}},{{a_2}},\ldots,{{a_n}}\big]^T",
        font_size=38,
        color=TEXT,
    )
    exact_header.set_color_by_tex("a", INPUT)

    entries = VGroup(
        MathTex(r"{{a_1}}", font_size=36, color=INPUT),
        MathTex(r"{{a_2}}", font_size=36, color=INPUT),
        MathTex(r"\vdots", font_size=34, color=MUTED),
        MathTex(r"{{a_j}}", font_size=36, color=INPUT),
        MathTex(r"{{a_n}}", font_size=36, color=INPUT),
    ).arrange(DOWN, buff=0.23)

    height = entries.height + 0.34
    left = VGroup(
        Line(ORIGIN, UP * height, color=MUTED, stroke_width=2.1),
        Line(ORIGIN, RIGHT * 0.18, color=MUTED, stroke_width=2.1),
        Line(UP * height, UP * height + RIGHT * 0.18, color=MUTED, stroke_width=2.1),
    )
    right = left.copy().rotate(PI).flip(UP)
    left.next_to(entries, LEFT, buff=0.14)
    right.next_to(entries, RIGHT, buff=0.14)

    prefix = MathTex(r"{{a}}=", font_size=42, color=TEXT)
    prefix.set_color_by_tex("a", INPUT)
    prefix.next_to(left, LEFT, buff=0.18)

    vector = VGroup(prefix, left, entries, right)
    vector.move_to(LEFT * 4.65 + UP * 0.45)
    exact_header.next_to(vector, DOWN, buff=0.35)

    block = VGroup(vector, exact_header)
    block.entries = entries
    block.visible_entries = VGroup(entries[0], entries[1], entries[3], entries[4])
    block.header = exact_header
    return block


def make_weight_matrix_and_formula():
    matrix = MathTex(
        r"{{K}}=",
        r"\begin{bmatrix}"
        r"K_{11}&K_{12}&\cdots&K_{1n}\\"
        r"\vdots&\vdots&\ddots&\vdots\\"
        r"K_{i1}&K_{i2}&\cdots&K_{in}"
        r"\end{bmatrix}",
        font_size=30,
        color=TEXT,
    )
    matrix.set_color_by_tex("K", OPERATOR)
    matrix.move_to(ORIGIN + UP * 0.55)

    formula = MathTex(
        r"{{\nu_i}}",
        r"=",
        r"{{\sigma}}",
        r"\left(",
        r"\sum_{j=1}^{n}",
        r"{{K_{ij}}}",
        r"{{a_j}}",
        r"\right)",
        font_size=42,
        color=TEXT,
    )
    formula.set_color_by_tex(r"\nu_i", OUTPUT)
    formula.set_color_by_tex(r"\sigma", OUTPUT)
    formula.set_color_by_tex("K_{ij}", OPERATOR)
    formula.set_color_by_tex("a_j", INPUT)
    formula.next_to(matrix, DOWN, buff=0.52)

    block = VGroup(matrix, formula)
    block.matrix = matrix
    block.formula = formula
    return block


def make_function_stage():
    axes = Axes(
        x_range=[DOMAIN_START, DOMAIN_END, 1],
        y_range=[0, 2.05, 0.5],
        x_length=6.65,
        y_length=3.55,
        tips=False,
        axis_config={"color": MUTED, "stroke_width": 1.1, "include_ticks": False},
    )
    axes.move_to(RIGHT * 3.88 + DOWN * 0.04)
    curve = axes.plot(sample_function, x_range=[DOMAIN_START, DOMAIN_END], color=SCIENCE, stroke_width=3.3)
    baseline = Line(axes.c2p(DOMAIN_START, 0), axes.c2p(DOMAIN_END, 0), color=GRID, stroke_width=1.0)
    curve_label = MathTex(r"{{a}}(x)", font_size=34, color=SCIENCE)
    curve_label.next_to(curve, UP, buff=0.18).shift(RIGHT * 0.30)

    dots = VGroup()
    x_labels = VGroup()
    stems = VGroup()
    value_labels = VGroup()
    for x, x_name, entry_name in zip(SAMPLE_XS, SAMPLE_NAMES, ENTRY_NAMES):
        y = sample_function(x)
        dot = Dot(axes.c2p(x, y), radius=0.060, color=OUTPUT)
        stem = DashedLine(axes.c2p(x, 0), axes.c2p(x, y), color=GRID, stroke_width=1.0, dash_length=0.08)
        x_label = MathTex(x_name, font_size=25, color=MUTED)
        x_label.next_to(axes.c2p(x, 0), DOWN, buff=0.12)
        value_label = MathTex(rf"a({x_name})", font_size=25, color=OUTPUT)
        value_label.next_to(dot, UP, buff=0.10)
        if x_name in {"x_2", "x_j"}:
            value_label.shift(DOWN * 0.05)
        dots.add(dot)
        stems.add(stem)
        x_labels.add(x_label)
        value_labels.add(value_label)

    ellipsis = MathTex(r"\cdots", font_size=28, color=MUTED)
    ellipsis.move_to((x_labels[1].get_center() + x_labels[3].get_center()) / 2 + DOWN * 0.02)

    stage = VGroup(axes, baseline, curve, curve_label, stems, dots, x_labels, ellipsis, value_labels)
    stage.axes = axes
    stage.baseline = baseline
    stage.curve = curve
    stage.curve_label = curve_label
    stage.dots = dots
    stage.stems = stems
    stage.x_labels = x_labels
    stage.value_labels = value_labels
    stage.ellipsis = ellipsis
    return stage


def make_connectors(vector_entries, function_stage):
    connectors = VGroup()
    for entry, dot in zip(vector_entries, function_stage.dots):
        line = DashedLine(
            entry.get_right() + RIGHT * 0.08,
            dot.get_center(),
            color=OUTPUT,
            stroke_width=1.5,
            stroke_opacity=0.55,
            dash_length=0.10,
        )
        connectors.add(line)
    return connectors


class Scene0801BasicNeuralNetworkLayer(TimedScene):
    SCRIPT_ID = "8.1"
    SCRIPT_TITLE = "A basic neural network layer"
    SCRIPT_START = 46 * 60 + 20
    SCRIPT_END = 47 * 60 + 50
    SCENE_DURATION = 90.0

    KEYFRAMES = (
        "KF01 0.0s basic layer chain",
        "KF02 11.5s vector column entries",
        "KF03 23.0s matrix and activation formula",
        "KF04 37.0s vector kept, interpretation begins",
        "KF05 50.0s function curve and samples",
        "KF06 65.0s vector entries connected to samples",
        "KF07 90.0s final relation a_j = a(x_j)",
    )

    def construct(self):
        background = make_background_network(seed=801, n=72, dot_opacity=0.075, line_opacity=0.045)
        section_label = Chip("8.1  Basic NN layer", max_width=2.45, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)

        layer_chain = make_layer_chain()
        vector_block = make_column_vector()
        weight_block = make_weight_matrix_and_formula()
        function_stage = make_function_stage()
        connectors = make_connectors(vector_block.visible_entries, function_stage)

        interpretation_chip = Chip("vector entries come from a function", max_width=4.10, height=0.46, stroke_color=SCIENCE, font_size=18)
        interpretation_chip.move_to(DOWN * 3.45 + LEFT * 0.25)

        bridge_formula = MathTex(
            r"{{a_j}}",
            r"\longleftrightarrow",
            r"{{x_j}}",
            font_size=42,
            color=TEXT,
        )
        bridge_formula.set_color_by_tex("a_j", INPUT)
        bridge_formula.set_color_by_tex("x_j", OUTPUT)
        bridge_formula.move_to(DOWN * 3.12 + RIGHT * 3.75)

        final_relation = MathTex(
            r"{{a_j}}",
            r"=",
            r"{{a}}",
            r"({{x_j}})",
            font_size=54,
            color=TEXT,
        )
        final_relation.set_color_by_tex("a_j", INPUT)
        final_relation.set_color_by_tex("a", SCIENCE)
        final_relation.set_color_by_tex("x_j", OUTPUT)
        final_relation.move_to(DOWN * 3.12 + RIGHT * 3.75)

        assert_in_frame(VGroup(layer_chain, vector_block, weight_block), margin=0.32, label="finite_layer_layout")
        assert_in_frame(VGroup(vector_block, function_stage, connectors), margin=0.32, label="function_layout")
        assert_in_frame(final_relation, margin=0.32, label="final_relation")
        assert_no_group_overlap([vector_block, weight_block], min_gap=0.12, labels=["vector_block", "weight_block"])

        self.add(background)

        # VO exact: Hãy bắt đầu với một layer neural network cực cơ bản.
        # Global 46:20.0-46:31.5 => local 0.0-11.5
        self.play_timed(
            "show_basic_layer_chain",
            0.0,
            5.6,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(layer_chain.vector_chip, shift=RIGHT * 0.04),
            FadeIn(layer_chain.matrix_chip, shift=RIGHT * 0.04),
            FadeIn(layer_chain.sigma_chip, shift=RIGHT * 0.04),
        )
        self.play_timed(
            "connect_basic_layer_chain",
            5.6,
            11.5,
            Create(layer_chain.arrows),
            FadeIn(layer_chain.labels, shift=UP * 0.03),
        )

        # VO exact: Input là một vector gồm các giá trị `a_1`, `a_2`, đến `a_n`.
        # Global 46:31.5-46:43.0 => local 11.5-23.0
        self.play_timed(
            "draw_column_vector_frame",
            11.5,
            15.2,
            FadeIn(VGroup(vector_block[0][0], vector_block[0][1], vector_block[0][3]), shift=RIGHT * 0.04),
        )
        self.play_timed(
            "reveal_vector_entries",
            15.2,
            21.0,
            LaggedStart(*[FadeIn(entry, shift=UP * 0.03) for entry in vector_block[0][2]], lag_ratio=0.18),
        )
        self.play_timed(
            "show_exact_vector_header",
            21.0,
            23.0,
            FadeIn(vector_block.header, shift=DOWN * 0.03),
        )

        # VO exact: Layer nhân vector này với một matrix weight, cộng lại, rồi đưa qua nonlinearity.
        # Global 46:43.0-46:56.0 => local 23.0-36.0
        self.play_timed(
            "introduce_weight_matrix",
            23.0,
            28.5,
            FadeIn(weight_block.matrix, shift=UP * 0.05),
            layer_chain.matrix_chip.animate.set_stroke(color=OPERATOR, width=2.4),
        )
        self.play_timed(
            "write_activation_formula",
            28.5,
            33.2,
            Write(weight_block.formula),
        )
        self.play_timed(
            "highlight_sum_weight_and_input",
            33.2,
            36.0,
            Circumscribe(weight_block.formula[4:7], color=OPERATOR, buff=0.06),
        )

        # Pause exact: 1.0s.
        # Global 46:56.0-46:57.0 => local 36.0-37.0
        self.wait_timed("one_second_pause_after_layer_formula", 36.0, 37.0)

        # VO exact: Nhưng bây giờ hãy tưởng tượng vector đó không chỉ là vector ngẫu nhiên.
        # Global 46:57.0-47:10.0 => local 37.0-50.0
        finite_world = VGroup(layer_chain, weight_block)
        self.play_timed(
            "make_room_for_function_view",
            37.0,
            43.5,
            finite_world.animate.scale(0.55).move_to(LEFT * 1.35 + UP * 3.02).set_opacity(0.42),
            vector_block.animate.move_to(LEFT * 5.35 + DOWN * 0.25),
        )
        self.play_timed(
            "mark_vector_as_interpretable",
            43.5,
            50.0,
            FadeIn(interpretation_chip, shift=UP * 0.05),
            Circumscribe(vector_block.visible_entries, color=SCIENCE, buff=0.08),
        )

        # VO exact: Nó là các point evaluation của một function `a`, tại các điểm `x_1`, `x_2`, đến `x_n`.
        # Global 47:10.0-47:25.0 => local 50.0-65.0
        self.play_timed(
            "draw_underlying_function_curve",
            50.0,
            56.0,
            FadeIn(VGroup(function_stage.axes, function_stage.baseline), shift=UP * 0.04),
            Create(function_stage.curve),
            FadeIn(function_stage.curve_label, shift=UP * 0.05),
        )
        self.play_timed(
            "show_sample_locations",
            56.0,
            60.5,
            LaggedStart(*[FadeIn(mob, shift=UP * 0.03) for mob in VGroup(function_stage.stems, function_stage.dots, function_stage.x_labels)], lag_ratio=0.10),
            FadeIn(function_stage.ellipsis, shift=DOWN * 0.02),
        )
        self.play_timed(
            "connect_entries_to_sample_points",
            60.5,
            65.0,
            LaggedStart(*[Create(line) for line in connectors], lag_ratio=0.14),
        )

        # VO exact: Tức là `a_j` thật ra là `a` tại điểm `x_j`.
        # Global 47:25.0-47:50.0 => local 65.0-90.0
        self.play_timed(
            "unfold_entries_as_function_values",
            65.0,
            72.0,
            LaggedStart(
                *[
                    ReplacementTransform(entry.copy(), value)
                    for entry, value in zip(vector_block.visible_entries, function_stage.value_labels)
                ],
                lag_ratio=0.13,
            ),
        )
        self.play_timed(
            "show_symbol_to_location_bridge",
            72.0,
            76.0,
            FadeIn(bridge_formula, shift=UP * 0.05),
        )
        self.play_timed(
            "transform_to_final_point_evaluation_relation",
            76.0,
            81.5,
            TransformMatchingTex(bridge_formula, final_relation),
        )
        self.play_timed(
            "hold_final_relation_and_sample_point",
            81.5,
            89.7,
            Circumscribe(final_relation, color=OUTPUT, buff=0.08),
            function_stage.dots[2].animate.scale(1.45).set_color(NVIDIA_GREEN),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION - 0.1)
