"""
Scene 1.1 - The finite-dimensional comfort zone
Script: docs/full_voice_manim_script.md
Global time: 02:20.0-03:35.0
Local duration: 75.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import labeled_card, make_background_network
from src.common.theme import (
    apply_global_config,
    BG,
    CARD_BG,
    GRID,
    TEXT,
    MUTED,
    INPUT,
    OUTPUT,
    OPERATOR,
    WARNING,
    PURPLE,
    NVIDIA_GREEN,
)
from src.common.timing import TimedScene


apply_global_config()


class Scene0101FiniteDimensionalComfortZone(TimedScene):
    SCRIPT_ID = "1.1"
    SCRIPT_TITLE = "The finite-dimensional comfort zone"
    SCRIPT_START = 140.0
    SCRIPT_END = 215.0
    SCENE_DURATION = 75.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_matrix_grid(self, rows=12, cols=12, cell=0.105):
        cells = VGroup()
        center_r = (rows - 1) / 2
        center_c = (cols - 1) / 2
        for r in range(rows):
            for c in range(cols):
                x = (c - center_c) / center_c
                y = (center_r - r) / center_r
                blob = np.exp(-2.6 * ((x + 0.25) ** 2 + (y - 0.15) ** 2))
                stripe = 0.5 + 0.5 * np.sin(4.0 * x + 3.0 * y)
                value = np.clip(0.25 + 0.55 * blob + 0.20 * stripe, 0, 1)
                color = interpolate_color(ManimColor("#0F2A4A"), ManimColor(INPUT), value)
                square = Square(side_length=cell)
                square.set_stroke(GRID, width=0.35, opacity=0.5)
                square.set_fill(color, opacity=0.92)
                square.move_to([(c - center_c) * cell, (center_r - r) * cell, 0])
                cells.add(square)

        frame = SurroundingRectangle(cells, buff=0.04, color=INPUT, stroke_width=1.2)
        return VGroup(cells, frame)

    def make_token_sequence(self):
        labels = ["Deep", "learning", "loves", "tokens"]
        boxes = VGroup()
        for i, word in enumerate(labels):
            box = RoundedRectangle(
                width=0.66 + 0.08 * len(word),
                height=0.38,
                corner_radius=0.06,
                stroke_color=PURPLE,
                stroke_width=1.1,
                fill_color="#251B4A",
                fill_opacity=0.78,
            )
            text = Text(word, font_size=16, color=TEXT)
            text.move_to(box)
            boxes.add(VGroup(box, text))
        boxes.arrange(RIGHT, buff=0.08)
        index_marks = VGroup(
            *[
                Text(str(i + 1), font_size=12, color=MUTED).next_to(token, DOWN, buff=0.06)
                for i, token in enumerate(boxes)
            ]
        )
        return VGroup(boxes, index_marks)

    def make_waveform_samples(self):
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.2, 1.2, 1],
            x_length=2.5,
            y_length=1.08,
            tips=False,
            axis_config={"stroke_color": GRID, "stroke_width": 1.0},
        )

        def wave(x):
            return 0.65 * np.sin(2.8 * x) + 0.25 * np.sin(8.5 * x)

        curve = axes.plot(wave, color=OUTPUT, stroke_width=3.0)
        stems = VGroup()
        dots = VGroup()
        for x in np.linspace(0.2, 3.8, 14):
            top = axes.c2p(x, wave(x))
            base = axes.c2p(x, 0)
            stems.add(Line(base, top, color=OUTPUT, stroke_width=1.0, stroke_opacity=0.62))
            dots.add(Dot(top, radius=0.035, color=NVIDIA_GREEN))
        return VGroup(axes, curve, stems, dots)

    def make_neural_network_graph(self):
        layer_sizes = [4, 5, 3]
        layers = VGroup()
        for layer_index, size in enumerate(layer_sizes):
            nodes = VGroup(
                *[
                    Circle(
                        radius=0.105,
                        stroke_color=[INPUT, OPERATOR, OUTPUT][layer_index],
                        stroke_width=1.3,
                        fill_color=CARD_BG,
                        fill_opacity=0.85,
                    )
                    for _ in range(size)
                ]
            )
            nodes.arrange(DOWN, buff=0.18)
            layers.add(nodes)
        layers.arrange(RIGHT, buff=0.55)

        edges = VGroup()
        for left_layer, right_layer in zip(layers[:-1], layers[1:]):
            for left_node in left_layer:
                for right_node in right_layer:
                    edges.add(
                        Line(
                            left_node.get_center(),
                            right_node.get_center(),
                            color=GRID,
                            stroke_width=0.65,
                            stroke_opacity=0.64,
                        )
                    )
        nodes = VGroup(*layers)
        return VGroup(edges, nodes)

    def make_vector_stack(self):
        entries = VGroup(
            MathTex(r"x_1", color=TEXT, font_size=26),
            MathTex(r"x_2", color=TEXT, font_size=26),
            MathTex(r"\vdots", color=MUTED, font_size=26),
            MathTex(r"x_n", color=TEXT, font_size=26),
        ).arrange(DOWN, buff=0.06)
        left = Line(UP * 0.82, DOWN * 0.82, color=MUTED, stroke_width=2)
        right = left.copy()
        left.next_to(entries, LEFT, buff=0.1)
        right.next_to(entries, RIGHT, buff=0.1)
        vector = VGroup(left, entries, right)

        label = Text("vector / tensor / sequence of numbers", font_size=22, color=TEXT)
        label.next_to(vector, DOWN, buff=0.18)
        tensor_sheets = VGroup()
        for i in range(3):
            sheet = RoundedRectangle(
                width=1.05,
                height=1.28,
                corner_radius=0.04,
                stroke_color=INPUT,
                stroke_width=1.0,
                fill_color="#0F243A",
                fill_opacity=0.22,
            )
            sheet.shift(RIGHT * (0.08 * i) + UP * (0.06 * i))
            tensor_sheets.add(sheet)
        tensor_sheets.move_to(vector)
        tensor_sheets.set_z_index(-1)
        return VGroup(tensor_sheets, vector, label)

    def make_output_block(self):
        chip_specs = [
            ("label", OUTPUT),
            ("embedding", PURPLE),
            ("vector", INPUT),
        ]
        chips = VGroup()
        for name, color in chip_specs:
            box = RoundedRectangle(
                width=1.35,
                height=0.38,
                corner_radius=0.06,
                stroke_color=color,
                stroke_width=1.2,
                fill_color=CARD_BG,
                fill_opacity=0.74,
            )
            text = Text(name, font_size=18, color=TEXT)
            text.move_to(box)
            chips.add(VGroup(box, text))
        chips.arrange(DOWN, buff=0.13)
        return chips

    def make_chip(self, name, color):
        box = RoundedRectangle(
            width=1.25,
            height=0.42,
            corner_radius=0.07,
            stroke_color=color,
            stroke_width=1.15,
            fill_color=CARD_BG,
            fill_opacity=0.82,
        )
        text = Text(name, font_size=18, color=TEXT)
        text.move_to(box)
        return VGroup(box, text)

    def construct(self):
        background = make_background_network(seed=11)

        title = Text("Traditional deep learning", font_size=48, color=TEXT, weight=BOLD)
        title.set_color_by_gradient(TEXT, INPUT)
        subtitle = Text("finite-dimensional world", font_size=27, color=MUTED)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.16)
        title_group.move_to(UP * 2.82)

        # Global 02:20.0-02:28.0 => local 0.0-8.0
        self.play_timed(
            "finite_world_intro",
            0.0,
            8.0,
            FadeIn(background),
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.18),
            lag_ratio=0.2,
        )

        matrix_grid = self.make_matrix_grid()
        image_card = labeled_card(matrix_grid, "image → pixel matrix", accent=INPUT)
        token_sequence = self.make_token_sequence()
        token_card = labeled_card(token_sequence, "text → token sequence", accent=PURPLE)
        waveform_samples = self.make_waveform_samples()
        audio_card = labeled_card(waveform_samples, "audio → samples", accent=OUTPUT)
        input_cards = VGroup(image_card, token_card, audio_card).arrange(RIGHT, buff=0.44)
        input_cards.move_to(DOWN * 0.15)

        # Global 02:28.0-02:36.5 => local 8.0-16.5
        self.play_timed(
            "finite_objects_enter",
            8.0,
            16.5,
            LaggedStart(
                FadeIn(image_card, shift=UP * 0.25),
                FadeIn(token_card, shift=UP * 0.25),
                FadeIn(audio_card, shift=UP * 0.25),
                lag_ratio=0.2,
            ),
            title_group.animate.scale(0.78).to_edge(UP, buff=0.28),
        )

        # Global 02:36.5-02:37.4 => local 16.5-17.4
        self.wait_timed("pause_before_packaging", 16.5, 17.4)

        vector_stack = self.make_vector_stack()
        vector_stack.move_to(RIGHT * 1.05 + DOWN * 0.05)
        compact_cards = input_cards.copy().scale(0.64)
        compact_cards.arrange(DOWN, buff=0.18).move_to(LEFT * 4.75 + DOWN * 0.1)
        flow_arrows = VGroup(
            *[
                Arrow(
                    card.get_right(),
                    vector_stack.get_left(),
                    buff=0.16,
                    color=OPERATOR,
                    stroke_width=2.1,
                    max_tip_length_to_length_ratio=0.06,
                )
                for card in compact_cards
            ]
        )

        # Global 02:37.4-02:47.0 => local 17.4-27.0
        self.play_timed(
            "finite_packaging",
            17.4,
            27.0,
            Transform(input_cards, compact_cards),
            LaggedStart(*[GrowArrow(arrow) for arrow in flow_arrows], lag_ratio=0.18),
            FadeIn(vector_stack, shift=RIGHT * 0.18),
            FadeOut(subtitle),
            title_group.animate.to_edge(UP, buff=0.22),
        )

        neural_network = self.make_neural_network_graph()
        neural_network.move_to(RIGHT * 1.15 + DOWN * 0.08)
        vector_input = vector_stack.copy().scale(0.74).move_to(LEFT * 3.95 + DOWN * 0.06)
        input_to_network = Arrow(
            vector_input.get_right(),
            neural_network.get_left(),
            buff=0.18,
            color=OPERATOR,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.07,
        )
        output_block = self.make_output_block()
        output_block.move_to(RIGHT * 5.2 + DOWN * 0.06)
        network_to_output = Arrow(
            neural_network.get_right(),
            output_block.get_left(),
            buff=0.18,
            color=OPERATOR,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.07,
        )
        formula = MathTex(r"f:\mathbb{R}^n \to \mathbb{R}^m", color=OPERATOR, font_size=38)
        formula.next_to(neural_network, UP, buff=0.42)
        pipeline = VGroup(vector_input, input_to_network, neural_network, network_to_output, output_block)

        # Global 02:47.0-02:58.5 => local 27.0-38.5
        self.play_timed(
            "neural_network_map",
            27.0,
            38.5,
            FadeOut(flow_arrows),
            FadeOut(input_cards, shift=LEFT * 0.18),
            Transform(vector_stack, vector_input),
            FadeIn(input_to_network),
            Create(neural_network),
            GrowArrow(network_to_output),
            FadeIn(output_block, shift=RIGHT * 0.16),
            Write(formula),
        )

        chip_specs = [
            ("CNN", INPUT),
            ("ResNet", NVIDIA_GREEN),
            ("U-Net", OUTPUT),
            ("Transformer", PURPLE),
            ("ViT", OPERATOR),
        ]
        chips = VGroup(*[self.make_chip(name, color) for name, color in chip_specs])
        chips.arrange(RIGHT, buff=0.16)
        chips.next_to(pipeline, DOWN, buff=0.46)
        chip_title = Text("architectures built on this pipeline", font_size=22, color=MUTED)
        chip_title.next_to(chips, DOWN, buff=0.14)
        architecture_group = VGroup(chips, chip_title)

        # Global 02:58.5-03:12.0 => local 38.5-52.0
        self.play_timed(
            "architecture_family",
            38.5,
            52.0,
            LaggedStart(*[FadeIn(chip, shift=UP * 0.12) for chip in chips], lag_ratio=0.16),
            FadeIn(chip_title),
            neural_network.animate.set_stroke(width=1.6),
            formula.animate.set_color(TEXT),
        )

        finite_pipeline = VGroup(vector_stack, input_to_network, neural_network, network_to_output, output_block, formula, architecture_group)
        comfort_box = SurroundingRectangle(
            finite_pipeline,
            buff=0.34,
            color=OPERATOR,
            stroke_width=2.2,
            corner_radius=0.08,
        )
        glow = VGroup(
            *[
                SurroundingRectangle(
                    finite_pipeline,
                    buff=0.34 + 0.06 * i,
                    color=OPERATOR,
                    stroke_width=1.2,
                    stroke_opacity=0.22 / (i + 1),
                    corner_radius=0.08,
                )
                for i in range(4)
            ]
        )
        comfort_label = Text("finite-dimensional comfort zone", font_size=32, color=OPERATOR)
        comfort_label.next_to(comfort_box, UP, buff=0.16)
        contrast_text = Text("Not everything wants to be 224×224.", font_size=24, color=WARNING)
        contrast_text.next_to(comfort_box, DOWN, buff=0.22)
        final_group = VGroup(finite_pipeline, comfort_box, glow, comfort_label, contrast_text)

        # Global 03:12.0-03:35.0 => local 52.0-75.0
        self.play_timed(
            "comfort_zone_box",
            52.0,
            61.0,
            self.camera.frame.animate.scale(1.12).move_to(ORIGIN),
            Create(glow),
            Create(comfort_box),
            FadeIn(comfort_label, shift=DOWN * 0.12),
        )
        self.play_timed(
            "final_contrast",
            61.0,
            67.0,
            FadeIn(contrast_text, shift=UP * 0.12),
            final_group.animate.scale(0.985).move_to(ORIGIN),
        )
        self.play_timed(
            "ambient_hold",
            67.0,
            73.5,
            glow.animate.set_stroke(opacity=0.34),
            comfort_box.animate.set_stroke(width=2.8),
            rate_func=there_and_back,
        )
        self.wait_timed("final_hold", 73.5, 75.0)
        self.pad_to(self.SCENE_DURATION)
