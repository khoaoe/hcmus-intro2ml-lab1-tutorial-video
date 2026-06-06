"""
Scene 4.1 — Fourier Neural Operator (FNO): Cơ sở tần số & Định lý Tích chập
Source: original_outline.tex, Section 4, Scene 4.1
Global time: 11:15 – 12:30
Duration: 75s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0401_FNO(TimedScene):
    SCRIPT_ID = "4.1"
    SCRIPT_TITLE = "FNO — Cơ sở tần số & Định lý Tích chập"
    SCRIPT_START = 675.0
    SCRIPT_END = 750.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [11:15–11:50] FFT formula + frequency decomposition ──
        fft_title = Text("Fourier Neural Operator", font_size=30,
                         color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.4)

        fft_eq = MathTex(
            r"\hat{a}(\omega) = \int_{\Omega} a(x)\, e^{-2\pi i \langle x, \omega \rangle}\, dx",
            font_size=34, color=TEXT
        ).shift(UP * 1.5)

        # Spectral interpretation
        spec_label = MathTex(r"\hat{a}(\omega)", font_size=30, color=OPERATOR)
        spec_desc = Text("= phổ năng lượng, hệ số phức", font_size=20, color=MUTED)
        spec_group = VGroup(spec_label, spec_desc).arrange(RIGHT, buff=0.3).shift(DOWN * 0.2)

        # Waveform decomposition visual
        axes = Axes(
            x_range=[0, 6, 1], y_range=[-1.5, 1.5, 1],
            x_length=5, y_length=2,
            axis_config={"color": GRID, "stroke_width": 1},
        ).shift(DOWN * 2.5 + LEFT * 3)

        original = axes.plot(
            lambda x: np.sin(x) + 0.5 * np.sin(3 * x) + 0.3 * np.sin(5 * x),
            color=INPUT, stroke_width=2
        )

        # Frequency bars
        freq_bars = VGroup()
        freqs = [1.0, 0.5, 0.3, 0.15, 0.05]
        for i, amp in enumerate(freqs):
            bar = Rectangle(
                width=0.5, height=amp * 3,
                fill_color=OPERATOR, fill_opacity=0.7, stroke_width=0
            )
            bar.move_to(np.array([3 + i * 0.7, -2.5 + amp * 1.5, 0]))
            freq_bars.add(bar)
        freq_label = Text("Phổ tần số", font_size=16, color=MUTED).next_to(freq_bars, DOWN, buff=0.2)

        self.play_timed("fft_title", 0, 2, FadeIn(fft_title))
        self.play_timed("fft_eq", 2, 5, FadeIn(fft_eq))
        self.play_timed("spec", 5, 7, FadeIn(spec_group))
        self.play_timed("waveform", 7, 10, FadeIn(axes), FadeIn(original))
        self.play_timed("freq_bars", 10, 13, FadeIn(freq_bars), FadeIn(freq_label))
        self.wait_timed("hold_fft", 13, 35)

        # ── Beat 2: [11:50–12:30] 3-step pipeline: FFT → Multiply → IFFT ──
        self.play_timed("clear_beat1", 35, 35.5,
                        *[FadeOut(m) for m in [fft_eq, spec_group, axes, original,
                                               freq_bars, freq_label]])

        # Pipeline diagram
        step_data = [
            ("FFT", r"\mathcal{F}", INPUT),
            ("Spectral\nMultiply", r"R(\omega) \cdot \hat{v}", OPERATOR),
            ("IFFT", r"\mathcal{F}^{-1}", OUTPUT),
        ]
        pipeline_blocks = VGroup()
        for name, eq, color in step_data:
            box = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.6)
            title = Text(name, font_size=18, color=color, weight=BOLD).move_to(
                box.get_top() + DOWN * 0.4)
            formula = MathTex(eq, font_size=26, color=TEXT).move_to(box.get_center() + DOWN * 0.2)
            pipeline_blocks.add(VGroup(box, title, formula))

        pipeline_blocks.arrange(RIGHT, buff=0.6).shift(UP * 0.5)

        # Arrows
        pipe_arrows = VGroup()
        for i in range(len(pipeline_blocks) - 1):
            a = Arrow(pipeline_blocks[i].get_right(), pipeline_blocks[i + 1].get_left(),
                      color=GRID, buff=0.1, stroke_width=2)
            pipe_arrows.add(a)

        # Convolution theorem
        conv_theorem = MathTex(
            r"\text{Tích chập } O(N^2) \;\leftrightarrow\; \text{Nhân } O(N \log N)",
            font_size=24, color=NVIDIA_GREEN
        ).shift(DOWN * 1.8)

        # Global vs Local branches
        branch_global = Text("Nhánh toàn cục: tương tác xa", font_size=18, color=INPUT).shift(DOWN * 2.8 + LEFT * 3)
        branch_local = MathTex(r"W \cdot a(x)", font_size=24, color=OPERATOR)
        branch_local_desc = Text("Nhánh cục bộ: biến thiên nhanh", font_size=18, color=OPERATOR)
        local_group = VGroup(branch_local, branch_local_desc).arrange(DOWN, buff=0.15).shift(DOWN * 2.8 + RIGHT * 3)

        complexity = MathTex(r"O(N \log N)", font_size=28, color=NVIDIA_GREEN).to_edge(DOWN, buff=0.3)

        self.play_timed("pipeline", 35.5, 40, FadeIn(pipeline_blocks), FadeIn(pipe_arrows))
        self.play_timed("conv_thm", 40, 43, FadeIn(conv_theorem))
        self.play_timed("branches", 43, 48, FadeIn(branch_global), FadeIn(local_group))
        self.play_timed("complexity", 48, 50, FadeIn(complexity))
        self.wait_timed("hold_end", 50, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
