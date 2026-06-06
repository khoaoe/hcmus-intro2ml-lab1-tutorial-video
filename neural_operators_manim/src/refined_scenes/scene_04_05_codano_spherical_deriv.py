"""
Scene 4.5 — CoDANO, Spherical FNO & Khối Đạo hàm
Source: original_outline.tex, Section 4, Scene 4.5
Global time: 15:45 – 17:00
Duration: 75s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0405_CoDANOSphericalDerivative(TimedScene):
    SCRIPT_ID = "4.5"
    SCRIPT_TITLE = "CoDANO, Spherical FNO & Khối Đạo hàm"
    SCRIPT_START = 945.0
    SCRIPT_END = 1020.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [15:45–16:20] CoDANO attention + Spherical FNO ──
        # CoDANO attention matrix
        coda_title = Text("CoDANO: Attention giữa biến vật lý", font_size=24,
                          color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)

        # Attention matrix visualization
        variables = ["p", "v_x", "v_y", "T", "ρ"]
        n_vars = len(variables)
        matrix_group = VGroup()

        # Header row
        for j, var in enumerate(variables):
            label = MathTex(var, font_size=18, color=TEXT).move_to(
                LEFT * 3.5 + RIGHT * (j * 0.8 + 1.2) + UP * 2.2)
            matrix_group.add(label)

        # Matrix cells
        np.random.seed(42)
        for i in range(n_vars):
            row_label = MathTex(variables[i], font_size=18, color=TEXT).move_to(
                LEFT * 3.5 + UP * (1.5 - i * 0.7))
            matrix_group.add(row_label)
            for j in range(n_vars):
                val = np.random.uniform(0.1, 1.0) if i != j else 1.0
                opacity = val * 0.8
                cell = Square(side_length=0.6, fill_color=OPERATOR,
                              fill_opacity=opacity, stroke_width=0.5, stroke_color=GRID)
                cell.move_to(LEFT * 3.5 + RIGHT * (j * 0.8 + 1.2) + UP * (1.5 - i * 0.7))
                matrix_group.add(cell)

        alpha_label = MathTex(r"\alpha_{c,c'}", font_size=24, color=OPERATOR).shift(LEFT * 3.5 + DOWN * 2.5)
        alpha_desc = Text("Tự học: p ảnh hưởng bao nhiêu lên v",
                          font_size=16, color=MUTED).next_to(alpha_label, DOWN, buff=0.2)

        self.play_timed("coda_title", 0, 2, FadeIn(coda_title))
        self.play_timed("matrix", 2, 6, FadeIn(matrix_group))
        self.play_timed("alpha", 6, 8, FadeIn(alpha_label), FadeIn(alpha_desc))
        self.wait_timed("hold_coda", 8, 18)

        # Spherical FNO
        self.play_timed("clear_coda", 18, 18.5,
                        *[FadeOut(m) for m in [coda_title, matrix_group, alpha_label, alpha_desc]])

        sphere_title = Text("Spherical FNO", font_size=24,
                            color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.4)

        # Sphere with harmonic grid
        sphere = Circle(radius=2.0, color=SCIENCE, stroke_width=2, fill_opacity=0.05)

        # Latitude lines
        lat_lines = VGroup()
        for lat in range(-60, 90, 30):
            y = 2.0 * np.sin(np.radians(lat))
            half_w = 2.0 * np.cos(np.radians(lat))
            if half_w > 0.1:
                line = Line(LEFT * half_w + UP * y, RIGHT * half_w + UP * y,
                            color=GRID, stroke_width=0.5, stroke_opacity=0.5)
                lat_lines.add(line)

        # Longitude lines
        lon_lines = VGroup()
        for lon in range(0, 180, 30):
            ellipse = Ellipse(width=4.0 * np.cos(np.radians(lon)), height=4.0,
                              color=GRID, stroke_width=0.5, stroke_opacity=0.3)
            lon_lines.add(ellipse)

        sphere_group = VGroup(sphere, lat_lines, lon_lines)

        sphere_note = VGroup(
            Text("Fourier → kinh độ", font_size=18, color=INPUT),
            Text("Legendre → vĩ độ", font_size=18, color=PURPLE),
            Text("= Spherical Harmonics", font_size=18, color=SCIENCE, weight=BOLD),
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 5)

        pole_note = Text("Triệt tiêu sai số tại hai cực", font_size=18,
                         color=NVIDIA_GREEN).to_edge(DOWN, buff=0.5)

        self.play_timed("sphere_title", 18.5, 20, FadeIn(sphere_title))
        self.play_timed("sphere", 20, 24, FadeIn(sphere_group))
        self.play_timed("sphere_note", 24, 27, FadeIn(sphere_note))
        self.play_timed("pole_note", 27, 29, FadeIn(pole_note))
        self.wait_timed("hold_sphere", 29, 35)

        # ── Beat 2: [16:20–17:00] CNN stencil derivative block ──
        self.play_timed("clear_sphere", 35, 35.5,
                        *[FadeOut(m) for m in [sphere_title, sphere_group, sphere_note, pole_note]])

        deriv_title = Text("Nghịch lý & Giải pháp: Khối Đạo hàm", font_size=24,
                           color=WARNING, weight=BOLD).to_edge(UP, buff=0.4)

        # Paradox
        paradox = VGroup(
            Text("Tích phân: giỏi tổng hợp", font_size=20, color=OUTPUT),
            Text("nhưng kém nắm bắt đạo hàm", font_size=20, color=WARNING),
        ).arrange(DOWN, buff=0.2).shift(UP * 1.5)

        # CNN stencil
        stencil_values = ["-1", "0", "1"]
        stencil = VGroup()
        for i, val in enumerate(stencil_values):
            box = Square(side_length=0.8, stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.6)
            text = Text(val, font_size=22, color=INPUT).move_to(box)
            stencil.add(VGroup(box, text))
        stencil.arrange(RIGHT, buff=0.05).shift(DOWN * 0.5)
        stencil_label = Text("CNN stencil = sai phân hữu hạn", font_size=18,
                             color=INPUT).next_to(stencil, DOWN, buff=0.3)

        # Function with sliding stencil
        axes = Axes(
            x_range=[0, 6, 1], y_range=[-1, 2, 1],
            x_length=8, y_length=2,
            axis_config={"color": GRID, "stroke_width": 1},
        ).shift(DOWN * 2.8)

        curve = axes.plot(lambda x: np.sin(x * 1.5) + 0.5, color=OUTPUT, stroke_width=2)

        resolution_note = Text(
            "Tăng resolution → điều chỉnh hệ số stencil → vật lý nhất quán",
            font_size=16, color=MUTED
        ).to_edge(DOWN, buff=0.3)

        self.play_timed("deriv_title", 35.5, 37, FadeIn(deriv_title))
        self.play_timed("paradox", 37, 40, FadeIn(paradox))
        self.play_timed("stencil", 40, 44, FadeIn(stencil), FadeIn(stencil_label))
        self.play_timed("curve", 44, 47, FadeIn(axes), FadeIn(curve))
        self.play_timed("res_note", 47, 50, FadeIn(resolution_note))
        self.wait_timed("hold_end", 50, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
