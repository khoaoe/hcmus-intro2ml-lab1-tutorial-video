"""
Scene 2.4 - The core warning
Script: ../docs/full_voice_manim_script.md
Global time: 12:55.0-15:45.0
Local duration: 170.0s

Animation-first warning scene: rendered pictures are peeled back into
function-space structure, then bridged into traditional scientific computing.
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
from src.common.safe_text import SafeMathTex, SafeText, safe_paragraph
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    PHYSICS,
    PURPLE,
    SCIENCE,
    TEXT,
    WARNING,
)
from src.common.timing import TimedScene
from src.common.function_visuals import make_mesh_overlay, smooth_path


apply_global_config()


def make_colored_field(width=3.5, height=2.1, rows=9, cols=15, seed=24):
    """Small deterministic scalar field that reads as an image at first glance."""
    rng = np.random.default_rng(seed)
    palette = [INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR, WARNING, PURPLE, OUTPUT]
    cells = VGroup()
    dx = width / cols
    dy = height / rows
    for row in range(rows):
        for col in range(cols):
            wave = np.sin(row * 0.82 + col * 0.46) + 0.45 * np.cos(col * 0.7)
            jitter = rng.normal(0.0, 0.18)
            index = int(abs(wave + jitter) * 2.2 + row + col) % len(palette)
            opacity = 0.48 + 0.38 * (0.5 + 0.5 * np.sin(row * 0.5 + col * 0.35))
            cell = Rectangle(
                width=dx,
                height=dy,
                stroke_color=CARD_BG,
                stroke_width=0.35,
                fill_color=palette[index],
                fill_opacity=opacity,
            )
            cell.move_to(
                [
                    -width / 2 + dx / 2 + col * dx,
                    height / 2 - dy / 2 - row * dy,
                    0,
                ]
            )
            cells.add(cell)
    frame = RoundedRectangle(
        width=width + 0.14,
        height=height + 0.14,
        corner_radius=0.08,
        stroke_color=INPUT,
        stroke_width=1.2,
        fill_color=CARD_BG,
        fill_opacity=0.24,
    )
    return VGroup(frame, cells)


def make_scalar_field_card(label="image?", width=4.15, height=2.95, seed=24):
    field = make_colored_field(width=3.45, height=2.05, seed=seed)
    label_mob = SafeText(label, max_width=2.7, max_height=0.34, font_size=23, color=WARNING, weight="BOLD")
    body = VGroup(field, label_mob).arrange(DOWN, buff=0.18)
    return PanelCard("rendered scalar field", body=body, width=width, height=height, accent_color=INPUT, title_font_size=24)


def make_video_strip(seed=44):
    frames = VGroup()
    for idx in range(4):
        frame = RoundedRectangle(
            width=1.26,
            height=1.03,
            corner_radius=0.05,
            stroke_color=OPERATOR,
            stroke_width=1.0,
            fill_color=CARD_BG,
            fill_opacity=0.78,
        )
        layers = VGroup()
        for level in range(3):
            y = -0.28 + level * 0.25
            pts = []
            for x in np.linspace(-0.48, 0.48, 16):
                pts.append([x, y + 0.05 * np.sin(5.0 * x + idx * 0.8 + level), 0])
            layers.add(smooth_path(pts, color=GRID, stroke_width=0.9, stroke_opacity=0.82))
        source = Dot(LEFT * 0.28 + DOWN * 0.2, radius=0.035, color=WARNING)
        waves = VGroup(
            Arc(radius=0.16 + 0.08 * k + 0.025 * idx, start_angle=0.12, angle=2.35, color=OPERATOR, stroke_width=1.4)
            .shift(source.get_center())
            for k in range(3)
        )
        frame_group = VGroup(frame, layers, source, waves)
        frames.add(frame_group)
    frames.arrange(RIGHT, buff=0.10)
    tick = SafeText("t", max_width=0.25, max_height=0.25, font_size=16, color=MUTED)
    arrow = Arrow(frames.get_left() + DOWN * 0.26, frames.get_right() + DOWN * 0.26, color=MUTED, stroke_width=1.0, buff=0)
    tick.next_to(arrow, RIGHT, buff=0.05)
    return VGroup(frames, arrow, tick)


def make_hidden_structure_panel():
    mesh = make_mesh_overlay(width=3.0, height=1.75, nx=8, ny=5, color=TEXT)
    boundary = DashedVMobject(
        RoundedRectangle(width=3.15, height=1.9, corner_radius=0.08, stroke_color=WARNING, stroke_width=1.5),
        num_dashes=34,
    )
    coords = VGroup(
        Arrow(LEFT * 1.45 + DOWN * 0.92, RIGHT * 1.45 + DOWN * 0.92, color=MUTED, stroke_width=1.1, buff=0),
        Arrow(LEFT * 1.45 + DOWN * 0.92, LEFT * 1.45 + UP * 0.92, color=MUTED, stroke_width=1.1, buff=0),
        SafeText("domain D", max_width=1.2, max_height=0.28, font_size=16, color=MUTED).shift(RIGHT * 0.8 + DOWN * 1.06),
    )
    query_points = VGroup(
        Dot([-0.86, 0.34, 0], radius=0.045, color=OPERATOR),
        Dot([0.12, -0.18, 0], radius=0.045, color=OPERATOR),
        Dot([0.94, 0.43, 0], radius=0.045, color=OPERATOR),
    )
    glyphs = VGroup(
        SafeMathTex(r"\nabla", max_width=0.56, max_height=0.52, font_size=34, color=INPUT),
        SafeMathTex(r"\int_D", max_width=0.75, max_height=0.52, font_size=34, color=OUTPUT),
        SafeMathTex(r"\partial D", max_width=0.75, max_height=0.52, font_size=30, color=WARNING),
    ).arrange(RIGHT, buff=0.22)
    glyphs.next_to(boundary, DOWN, buff=0.18)
    message = SafeText(
        "domain knowledge gets lost",
        max_width=3.6,
        max_height=0.36,
        font_size=24,
        color=WARNING,
        weight="BOLD",
    )
    message.next_to(boundary, UP, buff=0.16)
    return VGroup(message, boundary, mesh, coords, query_points, glyphs)


def make_warning_card(title, question, color, width=5.35, height=2.25):
    if question == "Does the model see the pattern?":
        lines = ["Does the model see", "the pattern?"]
    elif question == "Does it learn the map between function spaces?":
        lines = ["Does it learn the map", "between function spaces?"]
    else:
        lines = [question]
    question_lines = VGroup(
        *[
            SafeText(line, max_width=4.65, max_height=0.36, font_size=24, min_font_size=18, color=TEXT)
            for line in lines
        ]
    ).arrange(DOWN, buff=0.09)
    return PanelCard(title, body=question_lines, width=width, height=height, accent_color=color, title_font_size=25)


def make_function_space_blob(label_tex, color, seed=1):
    rng = np.random.default_rng(seed)
    blob = Ellipse(
        width=3.45,
        height=2.45,
        stroke_color=color,
        stroke_width=2.0,
        fill_color=CARD_BG,
        fill_opacity=0.52,
    )
    curves = VGroup()
    for idx in range(4):
        pts = []
        phase = rng.uniform(0.0, TAU)
        for t in np.linspace(0, 1, 32):
            x = -1.05 + 2.1 * t
            y = -0.48 + idx * 0.32 + 0.12 * np.sin(2.2 * TAU * t + phase)
            pts.append([x, y, 0])
        curves.add(smooth_path(pts, color=color, stroke_width=1.55, stroke_opacity=0.75))
    label = SafeMathTex(label_tex, max_width=1.0, max_height=0.7, font_size=46, color=color)
    label.move_to(blob.get_top() + DOWN * 0.42)
    caption = SafeText("function space", max_width=2.0, max_height=0.28, font_size=16, color=MUTED)
    caption.move_to(blob.get_bottom() + UP * 0.26)
    return VGroup(blob, curves, label, caption)


def make_operator_arrow(label_tex=r"\mathrm{operator}", color=OPERATOR):
    glow = Arrow(LEFT * 1.25, RIGHT * 1.25, color=color, stroke_width=12, stroke_opacity=0.14, buff=0.0)
    arrow = Arrow(LEFT * 1.25, RIGHT * 1.25, color=color, stroke_width=4.0, buff=0.0)
    label = SafeMathTex(label_tex, max_width=2.5, max_height=0.58, font_size=34, color=color)
    label.next_to(arrow, UP, buff=0.12)
    return VGroup(glow, arrow, label)


def make_operator_map(label_tex=r"\mathrm{operator}"):
    left_space = make_function_space_blob(r"\mathcal{A}", INPUT, seed=5).shift(LEFT * 4.1)
    right_space = make_function_space_blob(r"\mathcal{U}", OUTPUT, seed=9).shift(RIGHT * 4.1)
    arrow = make_operator_arrow(label_tex).move_to(ORIGIN)
    formula = make_formula_badge(r"\mathcal{G}: \mathcal{A}\to\mathcal{U}", max_width=3.35, height=0.62, stroke_color=OPERATOR)
    formula.next_to(arrow, DOWN, buff=0.16)
    return VGroup(left_space, right_space, arrow, formula)


def make_example_rows():
    row1_left = make_colored_field(width=1.55, height=0.92, rows=5, cols=8, seed=70)
    row1_right = make_colored_field(width=1.55, height=0.92, rows=5, cols=8, seed=71)
    row2_left = make_colored_field(width=1.55, height=0.92, rows=5, cols=8, seed=72)
    row2_right = make_colored_field(width=1.55, height=0.92, rows=5, cols=8, seed=73)
    rows = VGroup()
    for left, right, left_label, right_label in (
        (row1_left, row1_right, r"a(x)", r"u(x)"),
        (row2_left, row2_right, r"\mathrm{atmosphere}_{t}", r"\mathrm{atmosphere}_{t+1}"),
    ):
        arrow = Arrow(LEFT * 0.42, RIGHT * 0.42, color=OPERATOR, stroke_width=2.2, buff=0)
        left_math = SafeMathTex(left_label, max_width=1.8, max_height=0.35, font_size=26, color=INPUT)
        right_math = SafeMathTex(right_label, max_width=2.2, max_height=0.35, font_size=26, color=OUTPUT)
        left_group = VGroup(left, left_math).arrange(DOWN, buff=0.08)
        right_group = VGroup(right, right_math).arrange(DOWN, buff=0.08)
        row = VGroup(left_group, arrow, right_group).arrange(RIGHT, buff=0.24)
        rows.add(row)
    rows.arrange(DOWN, buff=0.24)
    return rows


def make_data_pairs(count=6):
    pairs = VGroup()
    positions = [
        [-5.8, 2.4, 0],
        [-4.9, -2.45, 0],
        [-2.2, 2.75, 0],
        [2.2, -2.75, 0],
        [5.0, 2.35, 0],
        [5.85, -2.25, 0],
    ]
    for idx in range(count):
        tiny_a = make_colored_field(width=0.72, height=0.46, rows=3, cols=5, seed=90 + idx)
        tiny_u = make_colored_field(width=0.72, height=0.46, rows=3, cols=5, seed=110 + idx)
        arrow = Arrow(LEFT * 0.16, RIGHT * 0.16, color=OPERATOR, stroke_width=1.4, buff=0)
        pair = VGroup(tiny_a, arrow, tiny_u).arrange(RIGHT, buff=0.06).move_to(positions[idx])
        pairs.add(pair)
    return pairs


def make_transition_pipeline():
    specs = [
        ("physical\nphenomenon", PHYSICS, r"\phi(x,t)"),
        ("equations\n/ PDE", WARNING, r"\mathcal{L}u=f"),
        ("discretization", INPUT, r"D_h"),
        ("solver", OPERATOR, r"S_h"),
        ("solution\nfield", OUTPUT, r"u_h(x)"),
    ]
    nodes = VGroup()
    for title, color, formula in specs:
        box = RoundedRectangle(
            width=1.92,
            height=1.72,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.25,
            fill_color=CARD_BG,
            fill_opacity=0.72,
        )
        icon = SafeMathTex(formula, max_width=1.45, max_height=0.52, font_size=30, color=color)
        label = safe_paragraph(
            title,
            max_width=1.52,
            max_height=0.58,
            font_size=17,
            min_font_size=14,
            color=TEXT,
            alignment="center",
            line_spacing=-0.5,
        )
        body = VGroup(icon, label).arrange(DOWN, buff=0.12).move_to(box)
        node = VGroup(box, body)
        nodes.add(node)
    nodes.arrange(RIGHT, buff=0.45)
    arrows = VGroup()
    for left, right in zip(nodes[:-1], nodes[1:]):
        arrows.add(Arrow(left.get_right() + RIGHT * 0.08, right.get_left() + LEFT * 0.08, color=MUTED, stroke_width=2.2, buff=0))
    pipeline = VGroup(nodes, arrows)
    title = SafeText(
        "Traditional scientific computing path",
        max_width=7.4,
        max_height=0.48,
        font_size=30,
        color=TEXT,
        weight="BOLD",
    )
    title.next_to(pipeline, UP, buff=0.46)
    question = SafeText(
        "Before learning the operator, how did we compute it?",
        max_width=8.8,
        max_height=0.52,
        font_size=30,
        color=OPERATOR,
        weight="BOLD",
    )
    question.next_to(pipeline, DOWN, buff=0.48)
    return VGroup(title, pipeline, question)


class Scene0204TheCoreWarning(TimedScene):
    SCRIPT_ID = "2.4"
    SCRIPT_TITLE = "The core warning"
    SCRIPT_START = 12 * 60 + 55
    SCRIPT_END = 15 * 60 + 45
    SCENE_DURATION = 170.0

    def construct(self):
        background = make_background_network(seed=204, n=58, dot_opacity=0.13, line_opacity=0.12)
        self.add(background)

        warning_title = SafeText(
            "Visualization \u2260 data nature",
            max_width=8.8,
            max_height=0.72,
            font_size=44,
            color=WARNING,
            weight="BOLD",
        ).to_edge(UP, buff=0.38)
        opening_field = make_scalar_field_card().scale(1.12).move_to(DOWN * 0.32)
        rendered_badge = Chip(
            "looks like an image",
            max_width=2.45,
            height=0.48,
            stroke_color=WARNING,
            font_size=16,
        )
        rendered_badge.next_to(opening_field, DOWN, buff=0.24)
        opening_group = VGroup(warning_title, opening_field, rendered_badge)

        # Global 12:55.0-12:57.0 => local 0.0-2.0
        self.play_timed(
            "visualization_warning_scalar_field",
            0.0,
            2.0,
            FadeIn(opening_field, shift=UP * 0.18),
            FadeIn(rendered_badge, shift=UP * 0.10),
            FadeIn(warning_title, shift=DOWN * 0.10),
        )

        # Global 12:57.0-13:05.5 => local 2.0-10.5
        self.play_timed(
            "visualization_warning_hold",
            2.0,
            10.5,
            Indicate(opening_field, color=INPUT, scale_factor=1.015),
        )

        weather_card = make_scalar_field_card(label="rendered image", width=5.0, height=3.15, seed=32).scale(0.94)
        weather_card.shift(LEFT * 3.15 + DOWN * 0.06)
        seismic_body = VGroup(make_video_strip(), SafeText("rendered video", max_width=2.3, max_height=0.32, font_size=22, color=WARNING, weight="BOLD")).arrange(DOWN, buff=0.20)
        seismic_card = PanelCard("seismic wave strip", body=seismic_body, width=5.0, height=3.15, accent_color=OPERATOR, title_font_size=24)
        seismic_card.scale(0.94).shift(RIGHT * 3.15 + DOWN * 0.06)
        image_video_group = VGroup(weather_card, seismic_card)
        warning_title_target = warning_title.copy().scale(0.72).to_edge(UP, buff=0.28)

        # Global 13:05.5-13:17.0 => local 10.5-22.0
        self.play_timed(
            "rendered_image_and_video_examples",
            10.5,
            22.0,
            Transform(warning_title, warning_title_target),
            FadeOut(opening_field, shift=DOWN * 0.12),
            FadeOut(rendered_badge, shift=DOWN * 0.10),
            FadeIn(weather_card, shift=RIGHT * 0.16),
            FadeIn(seismic_card, shift=LEFT * 0.16),
        )

        image_video_label = SafeText("image / video", max_width=2.3, max_height=0.42, font_size=26, color=TEXT, weight="BOLD")
        image_video_label.move_to(UP * 2.62)
        image_video_cross = Cross(image_video_label, stroke_color=WARNING, stroke_width=2.4)
        hidden_structure = make_hidden_structure_panel().scale(0.96).move_to(DOWN * 1.04)
        dim_overlay = Rectangle(width=13.4, height=3.65, stroke_opacity=0, fill_color="#000000", fill_opacity=0.24).move_to(DOWN * 0.06)

        # Global 13:17.0-13:29.0 => local 22.0-34.0
        self.play_timed(
            "cross_out_images_reveal_domain_structure",
            22.0,
            34.0,
            image_video_group.animate.set_opacity(0.38),
            FadeIn(dim_overlay),
            FadeIn(image_video_label, shift=UP * 0.08),
            Create(image_video_cross),
            FadeIn(hidden_structure, shift=UP * 0.16),
        )

        # Global 13:29.0-13:30.0 => local 34.0-35.0
        self.wait_timed("script_pause_after_domain_warning", 34.0, 35.0)

        wrong_card = make_warning_card("Wrong question", "Does the model see the pattern?", WARNING)
        right_card = make_warning_card("Right question", "Does it learn the map between function spaces?", OUTPUT)
        question_cards = VGroup(wrong_card, right_card).arrange(RIGHT, buff=0.70).move_to(DOWN * 0.1)
        contrast_title = SafeText("Pattern recognition is not enough", max_width=7.4, max_height=0.52, font_size=32, color=TEXT, weight="BOLD")
        contrast_title.to_edge(UP, buff=0.50)

        # Global 13:30.0-13:42.5 => local 35.0-47.5
        self.play_timed(
            "wrong_question_right_question",
            35.0,
            47.5,
            FadeOut(VGroup(warning_title, image_video_group, image_video_label, image_video_cross, hidden_structure, dim_overlay), shift=DOWN * 0.18),
            FadeIn(contrast_title, shift=DOWN * 0.10),
            FadeIn(wrong_card, shift=RIGHT * 0.16),
            FadeIn(right_card, shift=LEFT * 0.16),
        )

        operator_map = make_operator_map().move_to(DOWN * 0.05)
        operator_title = SafeText("Operator = function in, function out", max_width=7.2, max_height=0.52, font_size=32, color=TEXT, weight="BOLD")
        operator_title.to_edge(UP, buff=0.42)

        # Global 13:42.5-13:57.0 => local 47.5-62.0
        self.play_timed(
            "introduce_operator_between_function_spaces",
            47.5,
            62.0,
            FadeOut(VGroup(contrast_title, question_cards), shift=DOWN * 0.18),
            FadeIn(operator_title, shift=DOWN * 0.08),
            FadeIn(operator_map[0], shift=RIGHT * 0.18),
            FadeIn(operator_map[1], shift=LEFT * 0.18),
            GrowArrow(operator_map[2][1]),
            FadeIn(operator_map[2][0]),
            Write(operator_map[2][2]),
            FadeIn(operator_map[3], shift=UP * 0.10),
        )

        examples = make_example_rows().scale(0.92).move_to(DOWN * 2.45)
        example_title = SafeText("Examples of function-space maps", max_width=5.5, max_height=0.40, font_size=25, color=TEXT)
        example_title.next_to(examples, UP, buff=0.18)
        map_shrunk = operator_map.copy().scale(0.72).move_to(UP * 0.80)

        # Global 13:57.0-14:12.5 => local 62.0-77.5
        self.play_timed(
            "operator_examples_coefficient_weather",
            62.0,
            77.5,
            Transform(operator_map, map_shrunk),
            FadeIn(example_title, shift=UP * 0.10),
            FadeIn(examples[0], shift=RIGHT * 0.12),
            FadeIn(examples[1], shift=LEFT * 0.12),
        )

        learned_map = make_operator_map(r"\mathcal{G}_{\theta}").scale(0.88).move_to(UP * 0.05)
        learned_message = SafeText(
            "neural operator learns an operator from data",
            max_width=7.7,
            max_height=0.46,
            font_size=29,
            color=OPERATOR,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.44)
        data_pairs = make_data_pairs()
        learned_group = VGroup(learned_map, learned_message, data_pairs)

        # Global 14:12.5-14:28.5 => local 77.5-93.5
        self.play_timed(
            "learned_operator_from_data_pairs",
            77.5,
            93.5,
            FadeOut(VGroup(operator_title, operator_map, example_title, examples), shift=DOWN * 0.14),
            FadeIn(learned_map, shift=UP * 0.12),
            FadeIn(data_pairs, lag_ratio=0.08),
            FadeIn(learned_message, shift=UP * 0.10),
        )

        vector_map = VGroup(
            make_formula_badge(r"f:\mathbb{R}^{n}\to\mathbb{R}^{m}", max_width=3.15, height=0.62, stroke_color=MUTED),
            SafeText("finite vector map", max_width=2.4, max_height=0.32, font_size=21, color=MUTED),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 4.6 + UP * 2.25)
        vector_box = SurroundingRectangle(vector_map, buff=0.18, color=MUTED, stroke_width=1.0)
        central_function_map = make_formula_badge(r"\mathcal{G}: \mathcal{A}\to\mathcal{U}", max_width=3.65, height=0.72, stroke_color=OPERATOR, font_size=32)
        central_function_map.move_to(ORIGIN)
        central_label = SafeText("function-space map", max_width=2.7, max_height=0.34, font_size=23, color=OPERATOR, weight="BOLD")
        central_label.next_to(central_function_map, DOWN, buff=0.18)
        function_focus = VGroup(central_function_map, central_label)

        # Global 14:28.5-14:45.5 => local 93.5-110.5
        self.play_timed(
            "normal_nn_contrast_function_space_map",
            93.5,
            110.5,
            learned_group.animate.set_opacity(0.20).scale(0.82).shift(DOWN * 0.15),
            FadeIn(vector_box),
            FadeIn(vector_map),
            FadeIn(function_focus, shift=UP * 0.10),
        )

        pipeline = make_transition_pipeline().scale(0.96).move_to(DOWN * 0.05)
        pipeline_title, pipeline_body, final_question = pipeline
        pipeline_nodes, pipeline_arrows = pipeline_body

        # Global 14:45.5-14:55.0 => local 110.5-120.0
        self.play_timed(
            "pipeline_physical_phenomenon",
            110.5,
            120.0,
            FadeOut(VGroup(learned_group, vector_box, vector_map, function_focus), shift=DOWN * 0.18),
            FadeIn(pipeline_title, shift=DOWN * 0.08),
            FadeIn(pipeline_nodes[0], shift=UP * 0.10),
        )

        # Global 14:55.0-15:05.0 => local 120.0-130.0
        self.play_timed(
            "pipeline_equations_pde",
            120.0,
            130.0,
            GrowArrow(pipeline_arrows[0]),
            FadeIn(pipeline_nodes[1], shift=UP * 0.10),
        )

        # Global 15:05.0-15:15.0 => local 130.0-140.0
        self.play_timed(
            "pipeline_discretization",
            130.0,
            140.0,
            GrowArrow(pipeline_arrows[1]),
            FadeIn(pipeline_nodes[2], shift=UP * 0.10),
        )

        # Global 15:15.0-15:25.0 => local 140.0-150.0
        self.play_timed(
            "pipeline_solver",
            140.0,
            150.0,
            GrowArrow(pipeline_arrows[2]),
            FadeIn(pipeline_nodes[3], shift=UP * 0.10),
        )

        # Global 15:25.0-15:35.0 => local 150.0-160.0
        self.play_timed(
            "pipeline_solution_field",
            150.0,
            160.0,
            GrowArrow(pipeline_arrows[3]),
            FadeIn(pipeline_nodes[4], shift=UP * 0.10),
        )

        # Global 15:35.0-15:45.0 => local 160.0-170.0
        self.play_timed(
            "transition_question_hold_with_motion",
            160.0,
            170.0,
            FadeIn(final_question, shift=UP * 0.10),
            Indicate(pipeline_nodes[1], color=WARNING, scale_factor=1.04),
            Indicate(pipeline_nodes[3], color=OPERATOR, scale_factor=1.04),
        )

        self.pad_to(self.SCENE_DURATION)
