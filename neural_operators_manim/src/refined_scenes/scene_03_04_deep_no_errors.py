"""
Scene 3.4 — Deep Neural Operator & Phân tích Sai số
Source: original_outline.tex, Section 3, Scene 3.4
Global time: 10:15 – 11:15
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0304_DeepNOErrorAnalysis(TimedScene):
    SCRIPT_ID = "3.4"
    SCRIPT_TITLE = "Deep Neural Operator & Error Analysis"
    SCRIPT_START = 615.0
    SCRIPT_END = 675.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [10:15–10:45] Stack L layers + Encoder→Layers→Decoder ──
        pipeline_title = Text("Deep Neural Operator", font_size=28,
                              color=TEXT, weight=BOLD).to_edge(UP, buff=0.4)

        # Pipeline blocks
        encoder_box = RoundedRectangle(width=2.2, height=1.2, corner_radius=0.1,
                                       stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.6)
        encoder_label = Text("Encoder\n(pointwise)", font_size=16, color=INPUT).move_to(encoder_box)
        encoder = VGroup(encoder_box, encoder_label)

        layers = VGroup()
        for i in range(3):
            box = RoundedRectangle(width=1.8, height=1.2, corner_radius=0.1,
                                   stroke_color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.6)
            label = Text(f"Layer {i + 1}", font_size=14, color=OPERATOR).move_to(box)
            layers.add(VGroup(box, label))

        ellipsis = Text("···", font_size=36, color=MUTED)

        decoder_box = RoundedRectangle(width=2.2, height=1.2, corner_radius=0.1,
                                       stroke_color=OUTPUT, fill_color=CARD_BG, fill_opacity=0.6)
        decoder_label = Text("Decoder\n(pointwise)", font_size=16, color=OUTPUT).move_to(decoder_box)
        decoder = VGroup(decoder_box, decoder_label)

        pipeline = VGroup(encoder, *layers, ellipsis, decoder).arrange(RIGHT, buff=0.35)

        # Arrows between blocks
        arrows = VGroup()
        all_blocks = [encoder, layers[0], layers[1], layers[2], ellipsis, decoder]
        for i in range(len(all_blocks) - 1):
            a = Arrow(all_blocks[i].get_right(), all_blocks[i + 1].get_left(),
                      color=GRID, buff=0.05, stroke_width=1.5,
                      max_tip_length_to_length_ratio=0.2)
            arrows.add(a)

        # Layer equation
        layer_eq = MathTex(
            r"v^{(\ell+1)} = \sigma\left(\int \kappa^\ell(y,x;\theta) \cdot v^\ell(x)\,dx + b^\ell(y)\right)",
            font_size=26, color=TEXT
        ).shift(DOWN * 1.5)

        # Invariance checks
        checks = VGroup(
            Text("✓ Input: mọi discretization", font_size=18, color=NVIDIA_GREEN),
            Text("✓ Output: query mọi điểm", font_size=18, color=NVIDIA_GREEN),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).shift(DOWN * 3)

        self.play_timed("title", 0, 2, FadeIn(pipeline_title))
        self.play_timed("pipeline", 2, 8, FadeIn(pipeline), FadeIn(arrows))
        self.play_timed("layer_eq", 8, 12, FadeIn(layer_eq))
        self.play_timed("checks", 12, 15, FadeIn(checks))
        self.wait_timed("hold_pipeline", 15, 30)

        # ── Beat 2: [10:45–11:15] 3 error bars ──
        self.play_timed("clear_beat1", 30, 30.5,
                        *[FadeOut(m) for m in [pipeline_title, pipeline, arrows, layer_eq, checks]])

        error_title = Text("Phân tích sai số", font_size=28,
                           color=TEXT, weight=BOLD).to_edge(UP, buff=0.5)

        # 3 error bars
        error_data = [
            ("Tổng quát hóa", 0.6, INPUT),
            ("Xấp xỉ", 0.45, OPERATOR),
            ("Rời rạc hóa", 0.7, PURPLE),
        ]

        bars = VGroup()
        for name, height_frac, color in error_data:
            bar_bg = Rectangle(width=2.5, height=3.0, stroke_color=GRID,
                               fill_color=CARD_BG, fill_opacity=0.3)
            bar_fill = Rectangle(width=2.3, height=3.0 * height_frac,
                                 fill_color=color, fill_opacity=0.6, stroke_width=0)
            bar_fill.align_to(bar_bg, DOWN).shift(UP * 0.1)
            label = Text(name, font_size=16, color=TEXT).next_to(bar_bg, DOWN, buff=0.2)
            bars.add(VGroup(bar_bg, bar_fill, label))

        bars.arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)

        # Error formula
        error_formula = MathTex(
            r"\varepsilon_{disc} = O(N^{-s})",
            font_size=30, color=PURPLE
        ).shift(DOWN * 3)

        sobolev_note = Text(
            "s = độ trơn Sobolev — hàm trơn → sai số giảm nhanh",
            font_size=18, color=MUTED
        ).to_edge(DOWN, buff=0.3)

        self.play_timed("error_title", 30.5, 32, FadeIn(error_title))
        self.play_timed("bars", 32, 38, FadeIn(bars))
        self.play_timed("formula", 38, 41, FadeIn(error_formula))
        self.play_timed("sobolev", 41, 43, FadeIn(sobolev_note))
        self.wait_timed("hold_end", 43, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
