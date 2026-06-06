"""
Scene 1.1 — Hook: Giới hạn của DL hữu hạn chiều
Source: original_outline.tex, Section 1, Scene 1.1
Global time: 0:00 – 0:45
Duration: 45s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0101_HookFiniteDimensionalLimit(TimedScene):
    SCRIPT_ID = "1.1"
    SCRIPT_TITLE = "Hook — Giới hạn của DL hữu hạn chiều"
    SCRIPT_START = 0.0
    SCRIPT_END = 45.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [0:00–0:12] Grid 64x64 fade-in → pixel fill → image ──
        grid_size = 16  # visual stand-in for 64x64
        squares = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                sq = Square(side_length=0.28, stroke_width=0.5, stroke_color=GRID)
                sq.move_to(np.array([j * 0.3 - 2.1, -i * 0.3 + 2.1, 0]))
                squares.add(sq)

        grid_label = Text("64 × 64", font_size=20, color=MUTED).next_to(squares, DOWN, buff=0.3)
        self.play_timed("grid_fadein", 0, 2, FadeIn(squares, lag_ratio=0.002), FadeIn(grid_label))

        # Color fill to simulate image
        colors = [INPUT, OUTPUT, OPERATOR, PURPLE, NVIDIA_GREEN, WARNING]
        for idx, sq in enumerate(squares):
            sq.set_fill(colors[idx % len(colors)], opacity=0.6)
        self.play_timed("pixel_fill", 2, 5, squares.animate.set_opacity(1), run_time=3)

        img_label = Text("Ảnh", font_size=28, color=TEXT, weight=BOLD).next_to(squares, UP, buff=0.3)
        self.play_timed("img_label", 5, 6, FadeIn(img_label))
        self.wait_timed("hold_img", 6, 12)

        # ── Beat 2: [0:12–0:28] Image morph → tensor → matrix multiply ──
        self.remove(img_label, grid_label)
        self.play_timed("clear_grid", 12, 12.5, FadeOut(squares))

        tensor_tex = MathTex(
            r"\mathbf{x} \in \mathbb{R}^{n}",
            font_size=42, color=INPUT
        )
        weight_tex = MathTex(
            r"\mathbf{W} \cdot \mathbf{x} + \mathbf{b}",
            font_size=42, color=OPERATOR
        )
        VGroup(tensor_tex, weight_tex).arrange(DOWN, buff=0.6)

        self.play_timed("tensor_show", 12.5, 14, FadeIn(tensor_tex))
        self.play_timed("weight_show", 14, 16, FadeIn(weight_tex))

        arch_labels = VGroup(
            Text("CNN", font_size=24, color=MUTED),
            Text("Transformer", font_size=24, color=MUTED),
            Text("ResNet / GPT", font_size=24, color=MUTED),
        ).arrange(RIGHT, buff=1.0).next_to(weight_tex, DOWN, buff=0.8)

        self.play_timed("arch_labels", 16, 18, FadeIn(arch_labels))
        self.wait_timed("hold_arch", 18, 28)

        # ── Beat 3: [0:28–0:45] Zoom out → R^n frame → "Finite-dimensional" ──
        self.play_timed("clear_beat2", 28, 28.8,
                        FadeOut(tensor_tex), FadeOut(weight_tex), FadeOut(arch_labels))

        rn_frame = RoundedRectangle(
            width=10, height=6, corner_radius=0.2,
            stroke_color=INPUT, stroke_width=2, fill_opacity=0
        )
        rn_label = MathTex(r"\mathbb{R}^n", font_size=52, color=INPUT).move_to(rn_frame.get_corner(UR) + DL * 0.6)

        dots = VGroup(*[
            Dot(point=np.array([np.random.uniform(-4, 4), np.random.uniform(-2.2, 2.2), 0]),
                radius=0.05, color=MUTED)
            for _ in range(60)
        ])
        np.random.seed(42)

        overlay_text = Text(
            "Finite-dimensional Euclidean Space",
            font_size=30, color=NVIDIA_GREEN, weight=BOLD
        ).to_edge(DOWN, buff=0.6)

        self.play_timed("rn_frame", 28.8, 31, FadeIn(rn_frame), FadeIn(rn_label))
        self.play_timed("dots", 31, 33, FadeIn(dots, lag_ratio=0.02))
        self.play_timed("overlay", 33, 35, FadeIn(overlay_text))
        self.wait_timed("hold_end", 35, 44)

        # Hard cut to black
        self.play_timed("cut_to_black", 44, 45,
                        *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
