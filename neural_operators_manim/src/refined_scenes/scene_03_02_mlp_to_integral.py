"""
Scene 3.2 — Bước nhảy từ MLP sang Toán tử Tích phân
Source: original_outline.tex, Section 3, Scene 3.2
Global time: 8:15 – 9:15
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0302_MLPToIntegralOperator(TimedScene):
    SCRIPT_ID = "3.2"
    SCRIPT_TITLE = "MLP → Toán tử Tích phân"
    SCRIPT_START = 495.0
    SCRIPT_END = 555.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [8:15–8:45] MLP equation → morph to integral operator ──
        mlp_title = Text("MLP Layer", font_size=28, color=MUTED, weight=BOLD).to_edge(UP, buff=0.5)

        mlp_eq = MathTex(
            r"y_j", r"=", r"\sigma", r"\left(", r"\sum_i",
            r"W_{ji}", r"x_i", r"+", r"b_j", r"\right)",
            font_size=36
        ).shift(UP * 1.5)
        mlp_eq[0].set_color(OUTPUT)    # y_j
        mlp_eq[5].set_color(OPERATOR)  # W_ji
        mlp_eq[6].set_color(INPUT)     # x_i
        mlp_eq[8].set_color(MUTED)     # b_j

        self.play_timed("mlp_title", 0, 2, FadeIn(mlp_title))
        self.play_timed("mlp_eq", 2, 5, FadeIn(mlp_eq))
        self.wait_timed("hold_mlp", 5, 10)

        # Morph annotations
        morph_arrows = VGroup()
        morph_data = [
            (mlp_eq[0], r"j \to y", LEFT * 4 + DOWN * 0.5),
            (mlp_eq[5], r"W \to \kappa(y,x;\theta)", DOWN * 1.5),
            (mlp_eq[4], r"\sum \to \int", RIGHT * 4 + DOWN * 0.5),
        ]
        morph_labels = VGroup()
        for target, label_text, offset in morph_data:
            label = MathTex(label_text, font_size=24, color=NVIDIA_GREEN).move_to(
                mlp_eq.get_center() + offset
            )
            morph_labels.add(label)

        for i, ml in enumerate(morph_labels):
            t = 10 + i * 3
            self.play_timed(f"morph_{i}", t, t + 2, FadeIn(ml))

        self.wait_timed("hold_morph", 19, 22)

        # Hard cut to integral form
        self.play_timed("clear_mlp", 22, 22.5,
                        FadeOut(mlp_title), FadeOut(mlp_eq), FadeOut(morph_labels))

        no_title = Text("Neural Operator Layer", font_size=28,
                        color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.5)

        integral_eq = MathTex(
            r"v(y)", r"=", r"\sigma", r"\left(",
            r"\int", r"\kappa(y,x;\theta)", r"a(x)", r"\,dx",
            r"+", r"b(y)", r"\right)",
            font_size=36
        ).shift(UP * 1.0)
        integral_eq[0].set_color(OUTPUT)    # v(y)
        integral_eq[5].set_color(OPERATOR)  # kappa
        integral_eq[6].set_color(INPUT)     # a(x)
        integral_eq[9].set_color(MUTED)     # b(y)

        self.play_timed("no_title", 22.5, 24, FadeIn(no_title))
        self.play_timed("integral_eq", 24, 28, FadeIn(integral_eq))

        # ── Beat 2: [8:45–9:15] Definition overlay + physics connections ──
        overlay = Text(
            "Định nghĩa Lớp Neural Operator",
            font_size=26, color=NVIDIA_GREEN, weight=BOLD
        ).shift(DOWN * 1.0)

        connections = VGroup(
            Text("• Đáp ứng xung", font_size=18, color=MUTED),
            Text("• Hàm Green", font_size=18, color=MUTED),
            Text("• Tích chập", font_size=18, color=MUTED),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(DOWN * 2.5 + LEFT * 2)

        diff_note = Text(
            "Khác biệt: trước kernel cho trước, giờ học từ data",
            font_size=20, color=OPERATOR
        ).to_edge(DOWN, buff=0.5)

        self.play_timed("overlay", 28, 30, FadeIn(overlay))
        self.play_timed("connections", 30, 35, FadeIn(connections))
        self.play_timed("diff_note", 35, 37, FadeIn(diff_note))
        self.wait_timed("hold_end", 37, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
