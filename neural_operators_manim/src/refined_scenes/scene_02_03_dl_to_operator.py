"""
Scene 2.3 — Từ Deep Learning truyền thống đến Operator Learning
Source: original_outline.tex, Section 2, Scene 2.3
Global time: 5:40 – 6:40
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0203_DLToOperatorLearning(TimedScene):
    SCRIPT_ID = "2.3"
    SCRIPT_TITLE = "Từ DL truyền thống đến Operator Learning"
    SCRIPT_START = 340.0
    SCRIPT_END = 400.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [5:40–6:10] Split screen: R^n→R^m vs A→U ──
        # Left: DL truyền thống
        left_title = Text("DL truyền thống", font_size=24, color=MUTED,
                          weight=BOLD).shift(LEFT * 4 + UP * 3)

        # Discrete dots representing vectors
        left_dots = VGroup(*[
            Dot(radius=0.08, color=INPUT).move_to(np.array([
                -5 + i * 0.4, np.sin(i * 0.8) * 0.8, 0
            ]))
            for i in range(8)
        ])
        left_eq = MathTex(
            r"f_\theta: \mathbb{R}^n \to \mathbb{R}^m",
            font_size=34, color=INPUT
        ).shift(LEFT * 4 + DOWN * 1.5)

        # Right: Operator learning
        right_title = Text("Operator Learning", font_size=24, color=NVIDIA_GREEN,
                           weight=BOLD).shift(RIGHT * 4 + UP * 3)

        # Smooth curve representing function
        right_curve = FunctionGraph(
            lambda x: 0.8 * np.sin(x * 1.5) + 0.3 * np.cos(x * 3),
            x_range=[-2, 2], color=OUTPUT, stroke_width=3
        ).shift(RIGHT * 4)

        right_eq = MathTex(
            r"G_\theta: \mathcal{A} \to \mathcal{U}",
            font_size=34, color=NVIDIA_GREEN
        ).shift(RIGHT * 4 + DOWN * 1.5)

        divider = Line(UP * 3.5, DOWN * 3.5, color=GRID, stroke_width=1)

        self.play_timed("left_side", 0, 3,
                        FadeIn(left_title), FadeIn(left_dots), FadeIn(left_eq))
        self.play_timed("divider", 3, 4, FadeIn(divider))
        self.play_timed("right_side", 4, 7,
                        FadeIn(right_title), FadeIn(right_curve), FadeIn(right_eq))
        self.wait_timed("hold_split", 7, 30)

        # ── Beat 2: [6:10–6:40] Darcy Flow equation + operator G ──
        self.play_timed("clear_split", 30, 30.5,
                        *[FadeOut(m) for m in [left_title, left_dots, left_eq,
                                               divider, right_title, right_curve, right_eq]])

        darcy_eq = MathTex(
            r"-\nabla \cdot (", r"a(x)", r"\nabla", r"u(x)", r") = f(x)",
            font_size=40
        ).shift(UP * 1.5)
        darcy_eq[1].set_color(INPUT)   # a(x)
        darcy_eq[3].set_color(PURPLE)  # u(x)

        a_label = Text("a(x): hệ số khuếch tán", font_size=20, color=INPUT).shift(LEFT * 3 + DOWN * 0.5)
        u_label = Text("u(x): nghiệm", font_size=20, color=PURPLE).shift(RIGHT * 3 + DOWN * 0.5)

        self.play_timed("darcy_eq", 30.5, 34, FadeIn(darcy_eq))
        self.play_timed("labels", 34, 36, FadeIn(a_label), FadeIn(u_label))

        # Operator G arrow
        a_func = FunctionGraph(lambda x: 0.5 * np.sin(2 * x), x_range=[-1.5, 1.5],
                               color=INPUT, stroke_width=3).shift(LEFT * 4 + DOWN * 2.5)
        u_func = FunctionGraph(lambda x: 0.4 * np.cos(1.5 * x) + 0.2, x_range=[-1.5, 1.5],
                               color=PURPLE, stroke_width=3).shift(RIGHT * 4 + DOWN * 2.5)
        g_arrow = CurvedArrow(
            a_func.get_right() + RIGHT * 0.3,
            u_func.get_left() + LEFT * 0.3,
            color=NVIDIA_GREEN, angle=-0.3
        )
        g_label = MathTex(r"G", font_size=36, color=NVIDIA_GREEN).next_to(g_arrow, UP, buff=0.15)
        approx_eq = MathTex(r"G(a) \approx u", font_size=32, color=NVIDIA_GREEN).shift(DOWN * 4)

        self.play_timed("a_func", 36, 38, FadeIn(a_func))
        self.play_timed("g_arrow", 38, 40, FadeIn(g_arrow), FadeIn(g_label))
        self.play_timed("u_func", 40, 42, FadeIn(u_func))
        self.play_timed("approx", 42, 44, FadeIn(approx_eq))
        self.wait_timed("hold_end", 44, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
