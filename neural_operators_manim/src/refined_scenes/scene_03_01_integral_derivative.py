"""
Scene 3.1 — Nền tảng Toán học: Tích phân & Đạo hàm
Source: original_outline.tex, Section 3, Scene 3.1
Global time: 7:30 – 8:15
Duration: 45s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0301_IntegralAndDerivative(TimedScene):
    SCRIPT_ID = "3.1"
    SCRIPT_TITLE = "Tích phân & Đạo hàm"
    SCRIPT_START = 450.0
    SCRIPT_END = 495.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [7:30–7:55] Riemann sum: N rectangles → N grows → smooth ──
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=6, y_length=3,
            axis_config={"color": GRID, "stroke_width": 1.5},
        ).shift(LEFT * 1 + UP * 0.5)

        func = axes.plot(lambda x: 0.5 * x * np.sin(x) + 1.5, x_range=[0.1, 3.8],
                         color=NVIDIA_GREEN, stroke_width=3)
        func_label = MathTex(r"a(x)", font_size=28, color=NVIDIA_GREEN).next_to(func, UP, buff=0.2)

        self.play_timed("axes_func", 0, 3, FadeIn(axes), FadeIn(func), FadeIn(func_label))

        # Riemann rectangles — start with N=4
        n_values = [4, 8, 20]
        prev_rects = None

        for idx, n in enumerate(n_values):
            dx = 3.8 / n
            rects = VGroup()
            for i in range(n):
                x_val = 0.1 + i * dx
                y_val = 0.5 * x_val * np.sin(x_val) + 1.5
                rect = Rectangle(
                    width=axes.x_length * dx / 4,
                    height=axes.y_length * y_val / 3,
                    fill_color=INPUT, fill_opacity=0.3,
                    stroke_color=INPUT, stroke_width=0.8,
                )
                rect.move_to(axes.c2p(x_val + dx / 2, y_val / 2))
                rects.add(rect)

            t_start = 3 + idx * 4
            if prev_rects is None:
                self.play_timed(f"rects_n{n}", t_start, t_start + 2, FadeIn(rects))
            else:
                self.play_timed(f"rects_n{n}", t_start, t_start + 2,
                                FadeOut(prev_rects), FadeIn(rects))
            self.wait_timed(f"hold_n{n}", t_start + 2, t_start + 4)
            prev_rects = rects

        # Area fill
        area = axes.get_area(func, x_range=[0.1, 3.8], color=INPUT, opacity=0.4)
        self.play_timed("area_fill", 15, 17, FadeOut(prev_rects), FadeIn(area))

        riemann_eq = MathTex(
            r"\sum_{i} a(x_i) \Delta x \;\to\; \int a(x)\,dx",
            font_size=30, color=TEXT
        ).to_edge(DOWN, buff=0.5)
        self.play_timed("riemann_eq", 17, 19, FadeIn(riemann_eq))
        self.wait_timed("hold_riemann", 19, 25)

        # ── Beat 2: [7:55–8:15] Finite difference: secant → tangent ──
        self.play_timed("clear_beat1", 25, 25.5,
                        *[FadeOut(m) for m in [axes, func, func_label, area, riemann_eq]])

        axes2 = Axes(
            x_range=[0, 5, 1], y_range=[0, 3, 1],
            x_length=7, y_length=3.5,
            axis_config={"color": GRID, "stroke_width": 1.5},
        ).shift(UP * 0.3)

        curve = axes2.plot(lambda x: 0.3 * x ** 2 - 0.5 * x + 1.5, x_range=[0.5, 4.5],
                           color=OUTPUT, stroke_width=3)

        # Two points for secant
        x1, x2 = 1.5, 3.5
        y1 = 0.3 * x1 ** 2 - 0.5 * x1 + 1.5
        y2 = 0.3 * x2 ** 2 - 0.5 * x2 + 1.5
        dot1 = Dot(axes2.c2p(x1, y1), color=WARNING, radius=0.08)
        dot2 = Dot(axes2.c2p(x2, y2), color=WARNING, radius=0.08)

        secant = Line(axes2.c2p(x1 - 0.5, y1 - (y2 - y1) / (x2 - x1) * 0.5),
                      axes2.c2p(x2 + 0.5, y2 + (y2 - y1) / (x2 - x1) * 0.5),
                      color=WARNING, stroke_width=2)

        self.play_timed("axes2", 25.5, 27, FadeIn(axes2), FadeIn(curve))
        self.play_timed("secant_pts", 27, 29, FadeIn(dot1), FadeIn(dot2), FadeIn(secant))

        # Move to tangent (x2 approaches x1)
        x_mid = 2.5
        y_mid = 0.3 * x_mid ** 2 - 0.5 * x_mid + 1.5
        dy = 0.6 * x_mid - 0.5  # derivative
        tangent_dot = Dot(axes2.c2p(x_mid, y_mid), color=NVIDIA_GREEN, radius=0.08)
        tangent = Line(
            axes2.c2p(x_mid - 1.5, y_mid - dy * 1.5),
            axes2.c2p(x_mid + 1.5, y_mid + dy * 1.5),
            color=NVIDIA_GREEN, stroke_width=2
        )

        self.play_timed("to_tangent", 29, 33,
                        FadeOut(dot1), FadeOut(dot2), FadeOut(secant),
                        FadeIn(tangent_dot), FadeIn(tangent))

        deriv_eq = MathTex(
            r"\frac{u(x+h) - u(x)}{h} \;\to\; \frac{du}{dx}",
            font_size=30, color=TEXT
        ).to_edge(DOWN, buff=0.5)
        self.play_timed("deriv_eq", 33, 35, FadeIn(deriv_eq))
        self.wait_timed("hold_end", 35, 44)

        self.play_timed("cut", 44, 45, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
