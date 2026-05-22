from manim import *
import numpy as np
import sys
from pathlib import Path

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
)


apply_global_config()


# ---------------------------------------------------------------------
# Scene 01 — Hook: finite-dimensional ML vs function-space ML
# Project: ICML 2024 Neural Operators tutorial, Manim remake
# Manim: Community Edition
# ---------------------------------------------------------------------


class TimedScene(Scene):
    def setup(self):
        self.t = 0.0

    def play_timed(self, *animations, run_time=1.0, **kwargs):
        self.play(*animations, run_time=run_time, **kwargs)
        self.t += run_time

    def wait_timed(self, duration=1.0):
        self.wait(duration)
        self.t += duration

    def pad_to(self, target_time, render_tail=0.0):
        remaining = target_time - self.t
        if remaining > 0:
            self.wait(remaining)
            self.t = target_time
        if render_tail > 0:
            self.wait(render_tail)


class Scene01HookFunctionSpaces(TimedScene):
    """
    Opening hook.

    Narrative purpose:
    - Establish the contrast:
      conventional deep learning learns maps between finite-dimensional vectors,
      while scientific computing often needs maps between functions.
    - Do not define Neural Operators formally yet.
    - Set up the central question for the next scene.
    """

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    # -----------------------------------------------------------------
    # Reusable mini visual components
    # -----------------------------------------------------------------

    def make_pixel_patch(self, rows=7, cols=7, cell=0.13):
        """A small image-like finite-dimensional grid."""
        pixels = VGroup()
        center_r = (rows - 1) / 2
        center_c = (cols - 1) / 2

        for r in range(rows):
            for c in range(cols):
                dist = np.sqrt((r - center_r) ** 2 + (c - center_c) ** 2)
                t = np.clip(1 - dist / max(rows, cols), 0, 1)
                color = interpolate_color(ManimColor("#1E3A8A"), ManimColor("#FDE68A"), t)
                sq = Square(side_length=cell)
                sq.set_stroke(GRID, width=0.35, opacity=0.4)
                sq.set_fill(color, opacity=0.9)
                sq.move_to(np.array([
                    (c - center_c) * cell,
                    (center_r - r) * cell,
                    0,
                ]))
                pixels.add(sq)

        frame = SurroundingRectangle(pixels, buff=0.05, color=MUTED, stroke_width=0.8)
        return VGroup(pixels, frame).scale(1.15)

    def make_token_stack(self):
        """Small text/token blocks representing language data."""
        bars = VGroup()
        widths = [0.95, 0.70, 1.10, 0.55, 0.88]
        colors = [PURPLE, INPUT, OUTPUT, OPERATOR, "#60A5FA"]

        for i, (w, color) in enumerate(zip(widths, colors)):
            bar = RoundedRectangle(
                width=w,
                height=0.16,
                corner_radius=0.05,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.85,
            )
            bars.add(bar)

        bars.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        bracket = Brace(bars, LEFT, color=MUTED, buff=0.08)
        return VGroup(bars, bracket).scale(1.35)

    def make_vector(self):
        """Column vector as finite-dimensional object."""
        entries = VGroup(
            MathTex("x_1", color=TEXT, font_size=28),
            MathTex("x_2", color=TEXT, font_size=28),
            MathTex("\\vdots", color=MUTED, font_size=28),
            MathTex("x_n", color=TEXT, font_size=28),
        ).arrange(DOWN, buff=0.08)

        left = Line(UP * 0.9, DOWN * 0.9, color=MUTED, stroke_width=2)
        right = left.copy()
        left.next_to(entries, LEFT, buff=0.12)
        right.next_to(entries, RIGHT, buff=0.12)
        return VGroup(left, entries, right)

    def make_function_curve(self):
        """A continuous-looking function a(x)."""
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3.0,
            y_length=1.35,
            tips=False,
            axis_config={
                "stroke_color": GRID,
                "stroke_width": 1.3,
            },
        )

        def f(x):
            return 0.75 * np.sin(1.7 * x) + 0.25 * np.cos(4.2 * x)

        curve = axes.plot(f, color=INPUT, stroke_width=4)
        samples = VGroup(*[
            Dot(axes.c2p(x, f(x)), radius=0.035, color=OPERATOR)
            for x in np.linspace(0.25, 3.75, 9)
        ])

        label = MathTex("a(x)", color=INPUT, font_size=32)
        label.next_to(axes, UP, buff=0.04)

        return VGroup(axes, curve, samples, label)

    def make_heat_field(self, rows=9, cols=13, cell=0.11):
        """A tiny field/heatmap: visualized as pixels, meant to represent a function."""
        field = VGroup()
        cx, cy = 0.58 * cols, 0.45 * rows

        for r in range(rows):
            for c in range(cols):
                x = c / max(cols - 1, 1)
                y = r / max(rows - 1, 1)
                peak = np.exp(-((c - cx) ** 2 + (r - cy) ** 2) / 18.0)
                wave = 0.22 * (np.sin(7 * x) * np.cos(5 * y) + 1)
                val = np.clip(0.70 * peak + 0.30 * wave, 0, 1)

                color = interpolate_color(ManimColor("#1E1B4B"), ManimColor(OUTPUT), val)
                sq = Square(side_length=cell)
                sq.set_stroke(GRID, width=0.25, opacity=0.25)
                sq.set_fill(color, opacity=0.9)
                sq.move_to(np.array([
                    (c - (cols - 1) / 2) * cell,
                    ((rows - 1) / 2 - r) * cell,
                    0,
                ]))
                field.add(sq)

        frame = SurroundingRectangle(field, buff=0.04, color=MUTED, stroke_width=0.8)
        label = MathTex("u(x,t)", color=OUTPUT, font_size=30)
        label.next_to(frame, UP, buff=0.05)

        return VGroup(field, frame, label).scale(1.25)

    def make_operator_box(self, tex, color=OPERATOR):
        """Yellow operator box."""
        box = RoundedRectangle(
            width=1.45,
            height=0.82,
            corner_radius=0.16,
            stroke_color=color,
            stroke_width=2,
            fill_color="#1F2937",
            fill_opacity=0.72,
        )
        label = MathTex(tex, color=color, font_size=38)
        label.move_to(box)
        return VGroup(box, label)

    # -----------------------------------------------------------------
    # Main scene
    # -----------------------------------------------------------------

    def construct(self):
        bg_network = make_background_network(
            seed=11,
            n=42,
            x_range=(-7.7, 7.7),
            y_range=(-4.1, 4.1),
            max_distance=2.2,
            dot_opacity=0.32,
            line_opacity=0.25,
        )
        self.add(bg_network)

        # -------------------------------------------------------------
        # VO [00:00 - 00:06]
        # "Trước giờ, deep learning chủ yếu rất giỏi với ảnh, text,
        # speech — những thứ sau cùng đều được đưa về vector hữu hạn chiều."
        # -------------------------------------------------------------
        title = Text(
            "Machine Learning\non Function Spaces",
            font_size=56,
            line_spacing=0.9,
            weight=BOLD,
            color=TEXT,
        )
        title.set_color_by_gradient(INPUT, OUTPUT)

        subtitle = Text(
            "# Neural Operators",
            font_size=34,
            color=OPERATOR,
            weight=MEDIUM,
        )

        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.32)
        title_group.move_to(ORIGIN)

        self.play_timed(FadeIn(title_group, shift=0.25 * UP), run_time=1.4)
        self.play_timed(
            bg_network.animate.set_opacity(0.55),
            title_group.animate.scale(0.92),
            run_time=1.4,
        )
        self.wait_timed(2.0)

        self.play_timed(
            title_group.animate.to_edge(UP, buff=0.18).scale(0.45),
            run_time=1.2,
        )
        self.pad_to(6.0)

        # -------------------------------------------------------------
        # VO [00:06 - 00:15]
        # "Ta đưa một vector vào neural network, và học một ánh xạ
        # từ R n sang R m. Đây là thế giới quen thuộc của computer vision
        # và language models."
        # -------------------------------------------------------------
        left_title = Text(
            "Traditional deep learning",
            font_size=29,
            color=TEXT,
            weight=BOLD,
        )
        left_subtitle = Text(
            "finite-dimensional objects",
            font_size=20,
            color=MUTED,
        )
        left_header = VGroup(left_title, left_subtitle).arrange(DOWN, buff=0.08)
        left_header.move_to(LEFT * 4.25 + UP * 3.12)

        image_card = labeled_card(
            self.make_pixel_patch(),
            "image / pixels",
            width=2.15,
            height=1.55,
            accent=INPUT,
        )
        text_card = labeled_card(
            self.make_token_stack(),
            "text / tokens",
            width=2.15,
            height=1.55,
            accent=PURPLE,
        )
        vector_card = labeled_card(
            self.make_vector(),
            "vector",
            width=2.15,
            height=1.55,
            accent=OPERATOR,
        )

        finite_inputs = VGroup(image_card, text_card, vector_card).arrange(
            RIGHT,
            buff=0.25,
        )
        finite_inputs.scale(0.72)
        finite_inputs.move_to(LEFT * 4.6 + UP * 0.85)

        f_box = self.make_operator_box("f_\\theta", OPERATOR)
        f_box.move_to(LEFT * 4.6 + DOWN * 0.78)

        finite_formula = MathTex(
            "f_\\theta:\\mathbb{R}^{n}\\to\\mathbb{R}^{m}",
            color=TEXT,
            font_size=32,
        )
        finite_formula.next_to(f_box, DOWN, buff=0.42)

        left_arrow_in = Arrow(
            finite_inputs.get_bottom(),
            f_box.get_top(),
            buff=0.16,
            color=MUTED,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12,
        )

        left_output = VGroup(
            MathTex("y", color=OUTPUT, font_size=30),
            Text("label / vector", font_size=18, color=MUTED),
        ).arrange(DOWN, buff=0.06)
        left_output.next_to(f_box, RIGHT, buff=0.55)

        left_arrow_out = Arrow(
            f_box.get_right(),
            left_output.get_left(),
            buff=0.12,
            color=OUTPUT,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12,
        )

        left_group = VGroup(
            left_header,
            finite_inputs,
            left_arrow_in,
            f_box,
            finite_formula,
            left_output,
            left_arrow_out,
        )

        self.play_timed(FadeIn(left_header, shift=0.25 * RIGHT), run_time=0.8)
        self.play_timed(
            LaggedStart(
                FadeIn(image_card, shift=0.2 * UP),
                FadeIn(text_card, shift=0.2 * UP),
                FadeIn(vector_card, shift=0.2 * UP),
                lag_ratio=0.18,
            ),
            run_time=1.5,
        )
        self.play_timed(
            GrowArrow(left_arrow_in),
            FadeIn(f_box, scale=0.92),
            run_time=1.2,
        )
        self.play_timed(
            GrowArrow(left_arrow_out),
            FadeIn(left_output, shift=0.25 * RIGHT),
            Write(finite_formula),
            run_time=1.6,
        )
        self.wait_timed(1.1)
        self.pad_to(15.0)

        # -------------------------------------------------------------
        # VO [00:15 - 00:26]
        # "Nhưng trong khoa học tự nhiên và kỹ thuật, dữ liệu thường
        # không thật sự là một vector cố định. Nhiệt độ trên Trái Đất,
        # vận tốc dòng chảy, sóng địa chấn — tất cả là các hàm trên
        # không gian và thời gian."
        # -------------------------------------------------------------
        right_title = Text(
            "Scientific computing",
            font_size=29,
            color=TEXT,
            weight=BOLD,
        )
        right_subtitle = Text(
            "function-valued data",
            font_size=20,
            color=MUTED,
        )
        right_header = VGroup(right_title, right_subtitle).arrange(DOWN, buff=0.08)
        right_header.move_to(RIGHT * 4.25 + UP * 3.12)

        curve_card = labeled_card(
            self.make_function_curve(),
            "signal / field",
            width=3.45,
            height=1.95,
            accent=INPUT,
        )
        heat_card = labeled_card(
            self.make_heat_field(),
            "state over space-time",
            width=3.45,
            height=1.95,
            accent=OUTPUT,
        )

        function_inputs = VGroup(curve_card, heat_card).arrange(DOWN, buff=0.42)
        function_inputs.scale(0.72)
        function_inputs.move_to(RIGHT * 4.25 + UP * 0.85)

        g_box = self.make_operator_box("\\mathcal{G}_\\theta", OPERATOR)
        g_box.next_to(function_inputs, DOWN, buff=0.34)

        function_formula = MathTex(
            "\\mathcal{G}_\\theta:\\mathcal{A}\\to\\mathcal{U}",
            color=TEXT,
            font_size=32,
        )
        function_formula.next_to(g_box, DOWN, buff=0.42)

        right_arrow_in = Arrow(
            function_inputs.get_bottom(),
            g_box.get_top(),
            buff=0.14,
            color=MUTED,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12,
        )

        right_output = VGroup(
            MathTex("u(x,t)", color=OUTPUT, font_size=30),
            Text("new function", font_size=18, color=MUTED),
        ).arrange(DOWN, buff=0.06)
        right_output.next_to(g_box, RIGHT, buff=0.48)

        right_arrow_out = Arrow(
            g_box.get_right(),
            right_output.get_left(),
            buff=0.12,
            color=OUTPUT,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12,
        )

        right_group = VGroup(
            right_header,
            function_inputs,
            right_arrow_in,
            g_box,
            function_formula,
            right_output,
            right_arrow_out,
        )

        # Give left side less opacity, then reveal right side.
        self.play_timed(left_group.animate.set_opacity(0.42), run_time=0.7)
        self.play_timed(FadeIn(right_header, shift=0.25 * LEFT), run_time=0.8)
        self.play_timed(
            LaggedStart(
                FadeIn(curve_card, shift=0.2 * UP),
                FadeIn(heat_card, shift=0.2 * UP),
                lag_ratio=0.22,
            ),
            run_time=1.5,
        )
        self.play_timed(
            GrowArrow(right_arrow_in),
            FadeIn(g_box, scale=0.92),
            run_time=1.1,
        )
        self.play_timed(
            GrowArrow(right_arrow_out),
            FadeIn(right_output, shift=0.25 * RIGHT),
            Write(function_formula),
            run_time=1.6,
        )

        not_image = Text(
            "not just pictures — functions",
            font_size=22,
            color=WARNING,
            weight=MEDIUM,
        )
        not_image.to_corner(UR, buff=0.55)
        self.play_timed(FadeIn(not_image, shift=0.18 * DOWN), run_time=0.9)
        self.wait_timed(1.0)
        self.pad_to(26.0)

        # -------------------------------------------------------------
        # VO [00:26 - 00:36]
        # "Vì vậy câu hỏi không còn là: học một function trên vector.
        # Câu hỏi mới là: làm sao học một operator, tức là một ánh xạ
        # biến một hàm đầu vào thành một hàm đầu ra?"
        # -------------------------------------------------------------
        question = Text(
            "The question changes.",
            font_size=38,
            color=TEXT,
            weight=BOLD,
        )
        question.to_edge(DOWN, buff=0.34)

        old_question = MathTex(
            "\\text{learn } f_\\theta(x)",
            color=MUTED,
            font_size=32,
        )
        new_question = MathTex(
            "\\text{learn } \\mathcal{G}_\\theta(a)(x)",
            color=OPERATOR,
            font_size=34,
        )
        comparison = VGroup(old_question, new_question).arrange(RIGHT, buff=0.62)
        comparison.next_to(question, UP, buff=0.18)

        cross = Cross(old_question, stroke_color=WARNING, stroke_width=5)
        arrow_shift = Arrow(
            old_question.get_right(),
            new_question.get_left(),
            buff=0.12,
            color=OPERATOR,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.14,
        )

        self.play_timed(FadeIn(question, shift=0.2 * UP), run_time=0.7)
        self.play_timed(Write(old_question), run_time=0.8)
        self.play_timed(Create(cross), run_time=0.45)
        self.play_timed(
            GrowArrow(arrow_shift),
            Write(new_question),
            run_time=1.3,
        )
        self.play_timed(
            Indicate(g_box, color=OPERATOR, scale_factor=1.08),
            Indicate(function_formula, color=OPERATOR, scale_factor=1.06),
            run_time=1.5,
        )
        self.wait_timed(0.7)
        self.pad_to(36.0)

        # -------------------------------------------------------------
        # VO [00:36 - 00:45]
        # "Đó là lý do ta cần Machine Learning on Function Spaces —
        # và nhân vật chính của video này: Neural Operators."
        # -------------------------------------------------------------
        final_title = Text(
            "Machine Learning on Function Spaces",
            font_size=46,
            color=TEXT,
            weight=BOLD,
        )
        final_title.set_color_by_gradient(INPUT, OUTPUT)

        final_subtitle = Text(
            "Neural Operators",
            font_size=56,
            color=OPERATOR,
            weight=BOLD,
        )

        final_group = VGroup(final_title, final_subtitle).arrange(DOWN, buff=0.28)
        final_group.move_to(ORIGIN)

        all_current = VGroup(
            title_group,
            left_group,
            right_group,
            not_image,
            question,
            comparison,
            cross,
            arrow_shift,
        )

        self.play_timed(
            FadeOut(all_current, shift=0.25 * DOWN),
            bg_network.animate.set_opacity(0.28),
            run_time=1.4,
        )
        self.play_timed(FadeIn(final_group, shift=0.25 * UP), run_time=1.2)

        underline = Line(
            final_subtitle.get_left() + DOWN * 0.18,
            final_subtitle.get_right() + DOWN * 0.18,
            color=OPERATOR,
            stroke_width=4,
        )
        self.play_timed(Create(underline), run_time=0.7)
        self.wait_timed(2.2)
        self.pad_to(45.0, render_tail=0.175)
