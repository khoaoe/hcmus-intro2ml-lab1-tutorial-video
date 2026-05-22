"""
Scene 0.2 - Roadmap
Script: docs/full_voice_manim_script.md
Global time: 00:42.0-02:20.0
Local duration: 98.0s
"""

from manim import *
import numpy as np
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
from src.common.layout import make_background_network


apply_global_config()


class Scene0002Roadmap(TimedScene):
    SCRIPT_ID = "0.2"
    SCRIPT_TITLE = "Roadmap"
    SCRIPT_START = 42.0
    SCRIPT_END = 140.0
    SCENE_DURATION = 98.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_pixel_vector_icon(self):
        pixels = VGroup()
        colors = [INPUT, OUTPUT, OPERATOR, PURPLE]
        for r in range(4):
            for c in range(4):
                sq = Square(0.18)
                sq.set_stroke(GRID, width=0.5, opacity=0.6)
                sq.set_fill(colors[(r + 2 * c) % len(colors)], opacity=0.82)
                sq.move_to(np.array([(c - 1.5) * 0.2, (1.5 - r) * 0.2, 0]))
                pixels.add(sq)

        tokens = VGroup()
        for i, width in enumerate([0.48, 0.34, 0.42, 0.28]):
            token = RoundedRectangle(
                width=width,
                height=0.13,
                corner_radius=0.04,
                stroke_width=0,
                fill_color=[PURPLE, INPUT, OUTPUT, OPERATOR][i],
                fill_opacity=0.9,
            )
            tokens.add(token)
        tokens.arrange(DOWN, buff=0.055, aligned_edge=LEFT)
        tokens.next_to(pixels, RIGHT, buff=0.28)

        vector = MathTex(r"\mathbb{R}^{n}", color=TEXT, font_size=26)
        vector.next_to(VGroup(pixels, tokens), DOWN, buff=0.18)
        return VGroup(pixels, tokens, vector)

    def make_solver_icon(self):
        board = RoundedRectangle(
            width=1.7,
            height=0.82,
            corner_radius=0.08,
            stroke_color=INPUT,
            stroke_width=1.4,
            fill_color=CARD_BG,
            fill_opacity=0.58,
        )
        equation = MathTex(r"\nabla\!\cdot(a\nabla u)=f", color=TEXT, font_size=22)
        equation.move_to(board)

        solver = RoundedRectangle(
            width=1.0,
            height=0.38,
            corner_radius=0.08,
            stroke_color=NVIDIA_GREEN,
            stroke_width=1.6,
            fill_color="#16221A",
            fill_opacity=0.75,
        )
        solver_text = Text("solver", font_size=17, color=NVIDIA_GREEN, weight=MEDIUM)
        solver_label = VGroup(solver, solver_text).move_to(solver)
        solver_label.next_to(board, DOWN, buff=0.2)
        arrow = Arrow(board.get_bottom(), solver_label.get_top(), buff=0.08, color=MUTED, stroke_width=1.5)
        return VGroup(board, equation, arrow, solver_label)

    def make_operator_icon(self):
        left = MathTex(r"a(x)", color=INPUT, font_size=30)
        right = MathTex(r"u(x)", color=OUTPUT, font_size=30)
        arrow = Arrow(LEFT * 0.45, RIGHT * 0.45, color=OPERATOR, stroke_width=2.6)
        op = MathTex(r"\mathcal{G}", color=OPERATOR, font_size=26)
        group = VGroup(left, arrow, right).arrange(RIGHT, buff=0.18)
        op.move_to(arrow.get_center() + UP * 0.28)
        return VGroup(group, op)

    def make_kernel_icon(self):
        integral = MathTex(r"\int K(x,y)v(y)\,dy", color=TEXT, font_size=25)
        rectangles = VGroup()
        for i, height in enumerate([0.18, 0.34, 0.55, 0.38, 0.24]):
            rect = Rectangle(width=0.15, height=height, stroke_width=0, fill_color=INPUT, fill_opacity=0.75)
            rect.align_to(ORIGIN, DOWN)
            rect.shift(RIGHT * (i - 2) * 0.18)
            rectangles.add(rect)
        rectangles.next_to(integral, DOWN, buff=0.12)

        left_nodes = VGroup(*[Dot(radius=0.035, color=PURPLE) for _ in range(3)]).arrange(DOWN, buff=0.12)
        right_nodes = VGroup(*[Dot(radius=0.035, color=NVIDIA_GREEN) for _ in range(2)]).arrange(DOWN, buff=0.18)
        right_nodes.next_to(left_nodes, RIGHT, buff=0.35)
        edges = VGroup(
            *[
                Line(a.get_center(), b.get_center(), color=GRID, stroke_width=0.7, stroke_opacity=0.75)
                for a in left_nodes
                for b in right_nodes
            ]
        )
        layer = VGroup(edges, left_nodes, right_nodes)
        layer.next_to(rectangles, RIGHT, buff=0.32)
        return VGroup(integral, rectangles, layer)

    def make_architecture_icon(self):
        cards = VGroup()
        for i, name in enumerate(["GNO", "FNO", "U-NO", "TNO", "CoDA"]):
            card = RoundedRectangle(
                width=0.82,
                height=0.36,
                corner_radius=0.06,
                stroke_color=[INPUT, OPERATOR, OUTPUT, PURPLE, NVIDIA_GREEN][i],
                stroke_width=1.2,
                fill_color=CARD_BG,
                fill_opacity=0.78,
            )
            label = Text(name, font_size=15, color=TEXT, weight=MEDIUM)
            label.move_to(card)
            cards.add(VGroup(card, label))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.12, 0.12))
        cards[-1].shift(RIGHT * 0.34)
        return cards

    def make_domains_icon(self):
        sphere = Circle(radius=0.22, color=INPUT, stroke_width=1.6)
        equator = Arc(radius=0.22, start_angle=0, angle=PI, color=GRID, stroke_width=1.1)
        equator.stretch(0.35, 1).move_to(sphere)
        weather = VGroup(sphere, equator)

        wave = ParametricFunction(
            lambda t: np.array([t, 0.16 * np.sin(12 * t), 0]),
            t_range=[-0.35, 0.35],
            color=OPERATOR,
            stroke_width=2.0,
        )
        wave.next_to(weather, RIGHT, buff=0.28)

        atoms = VGroup(
            Dot(LEFT * 0.14, radius=0.05, color=PURPLE),
            Dot(RIGHT * 0.15 + UP * 0.08, radius=0.045, color=OUTPUT),
            Dot(RIGHT * 0.05 + DOWN * 0.16, radius=0.04, color=NVIDIA_GREEN),
        )
        bonds = VGroup(
            Line(atoms[0].get_center(), atoms[1].get_center(), color=GRID, stroke_width=1),
            Line(atoms[0].get_center(), atoms[2].get_center(), color=GRID, stroke_width=1),
        )
        molecule = VGroup(bonds, atoms)
        molecule.next_to(weather, DOWN, buff=0.22)

        car = VGroup(
            Polygon(
                LEFT * 0.34 + DOWN * 0.07,
                LEFT * 0.16 + UP * 0.12,
                RIGHT * 0.22 + UP * 0.12,
                RIGHT * 0.36 + DOWN * 0.07,
                color=NVIDIA_GREEN,
                fill_color=NVIDIA_GREEN,
                fill_opacity=0.22,
                stroke_width=1.4,
            ),
            Dot(LEFT * 0.2 + DOWN * 0.11, radius=0.035, color=TEXT),
            Dot(RIGHT * 0.22 + DOWN * 0.11, radius=0.035, color=TEXT),
        )
        car.next_to(wave, DOWN, buff=0.25)

        question = Text("?", font_size=32, color=WARNING, weight=BOLD)
        question.next_to(VGroup(wave, car), RIGHT, buff=0.2)
        return VGroup(weather, wave, molecule, car, question)

    def make_node(self, x, index, title, label, icon, accent):
        center = np.array([x, 0.25, 0])
        halo = VGroup(
            Circle(radius=0.34, stroke_color=accent, stroke_width=2.2, stroke_opacity=0.35),
            Circle(radius=0.52, stroke_color=accent, stroke_width=1.4, stroke_opacity=0.16),
        ).move_to(center)
        dot = Dot(center, radius=0.105, color=accent)
        number = Text(str(index), font_size=16, color=BG, weight=BOLD).move_to(dot)

        icon_scale = 0.58 if title == "Architectures" else 0.78
        icon_buff = 0.88 if title == "Architectures" else 0.58
        label_font_size = 14 if title == "Architectures" else 16

        icon.scale(icon_scale).next_to(dot, UP, buff=icon_buff)
        title_text = Text(title, font_size=22, color=TEXT, weight=BOLD)
        label_text = Text(label, font_size=label_font_size, color=MUTED)
        text = VGroup(title_text, label_text).arrange(DOWN, buff=0.06)
        text.next_to(dot, DOWN, buff=0.44)

        content = VGroup(icon, text)
        node = VGroup(halo, dot, number, content)
        node.halo = halo
        return node

    def activate_node_anims(self, nodes, active_index):
        anims = []
        for i, node in enumerate(nodes):
            if i == active_index:
                anims.append(node.animate.set_opacity(1.0))
                anims.append(node.halo.animate.set_stroke(opacity=0.95))
            else:
                anims.append(node.animate.set_opacity(0.28))
                anims.append(node.halo.animate.set_stroke(opacity=0.18))
        return anims

    def construct(self):
        self.camera.frame.move_to(LEFT * 6.0)

        background = make_background_network(seed=11)
        self.add(background)

        title = Text("Roadmap", font_size=58, color=TEXT, weight=BOLD)
        title.set_color_by_gradient(TEXT, NVIDIA_GREEN)
        subtitle = Text("animation-first tutorial", font_size=24, color=MUTED)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.18)
        title_group.move_to(LEFT * 6.0 + UP * 3.08)

        line = Line(LEFT * 11.4, RIGHT * 11.4, color=GRID, stroke_width=3.2)
        line.shift(UP * 0.25)
        progress_line = Line(LEFT * 11.4, LEFT * 11.4, color=NVIDIA_GREEN, stroke_width=4.2)
        progress_line.shift(UP * 0.25)

        nodes = VGroup(
            self.make_node(-10.0, 1, "Traditional DL", "finite-dimensional ML", self.make_pixel_vector_icon(), INPUT),
            self.make_node(-6.0, 2, "Scientific Computing", "PDEs + solvers", self.make_solver_icon(), NVIDIA_GREEN),
            self.make_node(-2.0, 3, "Solution Operator", "learn G?", self.make_operator_icon(), OPERATOR),
            self.make_node(2.0, 4, "Neural Operators", "integral + derivative + NN", self.make_kernel_icon(), PURPLE),
            self.make_node(6.0, 5, "Architectures", "GNO, FNO, U-NO, TNO, CoDA", self.make_architecture_icon(), OUTPUT),
            self.make_node(10.0, 6, "Domains + Open Problems", "real domains, open problems", self.make_domains_icon(), WARNING),
        )
        nodes.set_opacity(0.0)
        roadmap = VGroup(line, progress_line, nodes)

        # Global 00:42.0-00:49.0 => local 0.0-7.0
        self.play_timed(
            "intro_roadmap",
            0.0,
            7.0,
            FadeIn(title_group, shift=0.25 * UP),
            Create(line),
            FadeIn(nodes, lag_ratio=0.08),
            background.animate.set_opacity(0.58),
        )
        nodes.set_opacity(0.28)

        # Global 00:49.0-00:50.0 => local 7.0-8.0
        self.wait_timed("pause_after_intro", 7.0, 8.0)

        # Global 00:50.0-01:01.5 => local 8.0-19.5
        self.play_timed(
            "traditional_deep_learning",
            8.0,
            19.5,
            *self.activate_node_anims(nodes, 0),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, LEFT * 10.0 + UP * 0.25),
            self.camera.frame.animate.move_to(LEFT * 8.1),
        )

        # Global 01:01.5-01:10.5 => local 19.5-28.5
        self.play_timed(
            "scientific_computing",
            19.5,
            28.5,
            *self.activate_node_anims(nodes, 1),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, LEFT * 6.0 + UP * 0.25),
            self.camera.frame.animate.move_to(LEFT * 5.5),
        )

        # Global 01:10.5-01:18.5 => local 28.5-36.5
        self.play_timed(
            "solution_operator",
            28.5,
            36.5,
            *self.activate_node_anims(nodes, 2),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, LEFT * 2.0 + UP * 0.25),
            self.camera.frame.animate.move_to(LEFT * 2.0),
        )

        # Global 01:18.5-01:19.3 => local 36.5-37.3
        self.wait_timed("pause_before_building", 36.5, 37.3)

        # Global 01:19.3-01:31.0 => local 37.3-49.0
        self.play_timed(
            "build_neural_operators",
            37.3,
            49.0,
            *self.activate_node_anims(nodes, 3),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, RIGHT * 2.0 + UP * 0.25),
            self.camera.frame.animate.move_to(RIGHT * 1.7),
        )

        # Global 01:31.0-01:43.0 => local 49.0-61.0
        self.play_timed(
            "architectures",
            49.0,
            61.0,
            *self.activate_node_anims(nodes, 4),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, RIGHT * 6.0 + UP * 0.25),
            self.camera.frame.animate.move_to(RIGHT * 5.6),
        )

        # Global 01:43.0-01:54.5 => local 61.0-72.5
        self.play_timed(
            "domains_open_problems",
            61.0,
            72.5,
            *self.activate_node_anims(nodes, 5),
            progress_line.animate.put_start_and_end_on(LEFT * 11.4 + UP * 0.25, RIGHT * 10.0 + UP * 0.25),
            self.camera.frame.animate.move_to(RIGHT * 8.25),
        )

        final_question = Text(
            "When data are functions,\nwhat must ML change?",
            font_size=42,
            color=TEXT,
            weight=BOLD,
            line_spacing=0.85,
        )
        final_question.move_to(UP * 2.45)
        final_question.set_color_by_gradient(TEXT, NVIDIA_GREEN)

        terms = VGroup(
            Text("input", font_size=24, color=INPUT),
            Dot(radius=0.04, color=MUTED),
            Text("architecture", font_size=24, color=OPERATOR),
            Dot(radius=0.04, color=MUTED),
            Text("loss", font_size=24, color=OUTPUT),
            Dot(radius=0.04, color=MUTED),
            Text("problem definition", font_size=24, color=PURPLE),
        ).arrange(RIGHT, buff=0.28)
        terms.next_to(final_question, DOWN, buff=0.38)

        focus_frame = SurroundingRectangle(final_question, buff=0.24, color=NVIDIA_GREEN, stroke_width=1.3)
        focus_frame.set_stroke(opacity=0.22)

        # Global 01:54.5-02:20.0 => local 72.5-98.0
        self.play_timed(
            "zoom_out_full_roadmap",
            72.5,
            80.0,
            *[node.animate.set_opacity(0.9) for node in nodes],
            roadmap.animate.shift(DOWN * 1.15),
            title_group.animate.set_opacity(0.0),
            self.camera.frame.animate.move_to(ORIGIN).set(width=26.0),
        )
        self.play_timed(
            "central_question",
            80.0,
            86.0,
            FadeIn(final_question, shift=0.22 * UP),
            Create(focus_frame),
        )
        self.play_timed(
            "change_dimensions",
            86.0,
            90.0,
            LaggedStart(*[FadeIn(item, shift=0.1 * UP) for item in terms], lag_ratio=0.15),
        )
        self.play_timed(
            "ambient_final_hold",
            90.0,
            98.0,
            background.animate.set_opacity(0.38),
            focus_frame.animate.set_stroke(opacity=0.38),
            *[node.halo.animate.scale(1.04).set_stroke(opacity=0.55) for node in nodes],
        )

        self.pad_to(self.SCENE_DURATION)
