"""
Scene 3.3 — So sánh MLP vs Neural Operator & Thành phần Lớp
Source: original_outline.tex, Section 3, Scene 3.3
Global time: 9:15 – 10:15
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0303_MLPvsNOComponents(TimedScene):
    SCRIPT_ID = "3.3"
    SCRIPT_TITLE = "So sánh MLP vs Neural Operator & Thành phần Lớp"
    SCRIPT_START = 555.0
    SCRIPT_END = 615.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [9:15–9:45] Side-by-side MLP vs NO ──
        title = Text("MLP  vs  Neural Operator", font_size=30, color=TEXT,
                      weight=BOLD).to_edge(UP, buff=0.4)
        divider = Line(UP * 2.8, DOWN * 2.5, color=GRID, stroke_width=1)

        # Left: MLP column
        mlp_header = Text("MLP", font_size=24, color=INPUT, weight=BOLD).shift(LEFT * 4 + UP * 2.3)
        mlp_rows = VGroup(
            VGroup(
                Text("Input:", font_size=18, color=MUTED),
                MathTex(r"\mathbf{x} \in \mathbb{R}^n", font_size=24, color=INPUT),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Trọng số:", font_size=18, color=MUTED),
                MathTex(r"W \in \mathbb{R}^{m \times n}", font_size=24, color=OPERATOR),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Phép tính:", font_size=18, color=MUTED),
                MathTex(r"\sum_i W_{ji} x_i", font_size=24, color=TEXT),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Bias:", font_size=18, color=MUTED),
                MathTex(r"\mathbf{b} \in \mathbb{R}^m", font_size=24, color=MUTED),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT * 4 + DOWN * 0.3)

        # Right: NO column
        no_header = Text("Neural Operator", font_size=24, color=NVIDIA_GREEN,
                         weight=BOLD).shift(RIGHT * 4 + UP * 2.3)
        no_rows = VGroup(
            VGroup(
                Text("Input:", font_size=18, color=MUTED),
                MathTex(r"a(x) \in \mathcal{A}", font_size=24, color=INPUT),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Kernel:", font_size=18, color=MUTED),
                MathTex(r"\kappa(y,x;\theta)", font_size=24, color=OPERATOR),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Phép tính:", font_size=18, color=MUTED),
                MathTex(r"\int \kappa \cdot a(x)\,dx", font_size=24, color=TEXT),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Bias:", font_size=18, color=MUTED),
                MathTex(r"b(y)", font_size=24, color=MUTED),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(RIGHT * 4 + DOWN * 0.3)

        # Correspondence arrows
        corr_arrows = VGroup()
        for mlp_row, no_row in zip(mlp_rows, no_rows):
            arrow = Arrow(
                mlp_row.get_right() + RIGHT * 0.2,
                no_row.get_left() + LEFT * 0.2,
                color=GRID, stroke_width=1.5, buff=0.1,
                max_tip_length_to_length_ratio=0.15,
            )
            corr_arrows.add(arrow)

        self.play_timed("title", 0, 2, FadeIn(title), FadeIn(divider))
        self.play_timed("headers", 2, 4, FadeIn(mlp_header), FadeIn(no_header))
        self.play_timed("rows", 4, 10, FadeIn(mlp_rows), FadeIn(no_rows), FadeIn(corr_arrows))
        self.wait_timed("hold_comparison", 10, 30)

        # ── Beat 2: [9:45–10:15] Zoom into complete NO layer: 3 components ──
        self.play_timed("clear_beat1", 30, 30.5,
                        *[FadeOut(m) for m in [title, divider, mlp_header, mlp_rows,
                                               no_header, no_rows, corr_arrows]])

        layer_title = Text("Một lớp Neural Operator hoàn chỉnh", font_size=26,
                           color=TEXT, weight=BOLD).to_edge(UP, buff=0.5)

        # 3 component cards
        comp_data = [
            ("1. Lõi tích phân", r"\int \kappa \cdot a\,dx", "Tổng hợp toàn cục", OPERATOR),
            ("2. Bias hàm b(y)", r"b(y)", "Biến thiên theo không gian", MUTED),
            ("3. Residual Connection", r"v + a", "Giữ chi tiết sắc nét", NVIDIA_GREEN),
        ]
        components = VGroup()
        for name, eq, desc, color in comp_data:
            card = VGroup()
            box = RoundedRectangle(width=4.0, height=2.2, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.6)
            card_title = Text(name, font_size=18, color=color, weight=BOLD).move_to(
                box.get_top() + DOWN * 0.35
            )
            card_eq = MathTex(eq, font_size=28, color=TEXT).move_to(box)
            card_desc = Text(desc, font_size=14, color=MUTED).move_to(
                box.get_bottom() + UP * 0.35
            )
            card.add(box, card_title, card_eq, card_desc)
            components.add(card)

        components.arrange(RIGHT, buff=0.5)

        self.play_timed("layer_title", 30.5, 32, FadeIn(layer_title))

        for i, comp in enumerate(components):
            t = 32 + i * 4
            self.play_timed(f"comp_{i}", t, t + 2, FadeIn(comp))
            self.wait_timed(f"hold_comp_{i}", t + 2, t + 4)

        # Residual explanation
        residual_note = Text(
            "Tích phân làm mịn → Residual giữ nét",
            font_size=20, color=NVIDIA_GREEN
        ).to_edge(DOWN, buff=0.5)
        self.play_timed("residual_note", 44, 46, FadeIn(residual_note))
        self.wait_timed("hold_end", 46, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
