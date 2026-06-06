"""
Scene 2.2 — Lưu ý then chốt: Ảnh không phải là Hàm số
Source: original_outline.tex, Section 2, Scene 2.2
Global time: 5:00 – 5:40
Duration: 40s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0202_ImageIsNotFunction(TimedScene):
    SCRIPT_ID = "2.2"
    SCRIPT_TITLE = "Ảnh không phải là Hàm số"
    SCRIPT_START = 300.0
    SCRIPT_END = 340.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [5:00–5:25] Heatmap → zoom → pixel revealed ──
        # Create a heatmap-like grid
        n = 16
        heatmap = VGroup()
        for i in range(n):
            for j in range(n):
                val = (np.sin(i * 0.5) * np.cos(j * 0.4) + 1) / 2
                color = interpolate_color(
                    ManimColor(INPUT), ManimColor(WARNING), val
                )
                sq = Square(
                    side_length=0.35, stroke_width=0,
                    fill_color=color, fill_opacity=0.9,
                )
                sq.move_to(np.array([(j - n / 2 + 0.5) * 0.36, (i - n / 2 + 0.5) * 0.36, 0]))
                heatmap.add(sq)

        heatmap_label = Text("Trường nhiệt độ", font_size=24, color=TEXT).to_edge(UP, buff=0.5)

        self.play_timed("heatmap", 0, 3, FadeIn(heatmap), FadeIn(heatmap_label))
        self.wait_timed("hold_heatmap", 3, 8)

        # Reveal grid lines → pixels
        grid_lines = VGroup()
        for i in range(n + 1):
            x = (i - n / 2) * 0.36
            grid_lines.add(Line(
                np.array([x, -n / 2 * 0.36, 0]),
                np.array([x, n / 2 * 0.36, 0]),
                stroke_width=0.5, color=WHITE
            ))
            y = (i - n / 2) * 0.36
            grid_lines.add(Line(
                np.array([-n / 2 * 0.36, y, 0]),
                np.array([n / 2 * 0.36, y, 0]),
                stroke_width=0.5, color=WHITE
            ))

        self.play_timed("grid_lines", 8, 10, FadeIn(grid_lines))

        # Strike through "ẢNH"
        anh_text = Text("ẢNH", font_size=44, color=WARNING, weight=BOLD).shift(RIGHT * 5)
        strike = Line(anh_text.get_left(), anh_text.get_right(),
                      color=WARNING, stroke_width=4).move_to(anh_text)

        self.play_timed("anh_label", 10, 12, FadeIn(anh_text))
        self.play_timed("strike", 12, 13, FadeIn(strike))

        # Replace with "HÀM SỐ LẤY MẪU"
        sample_text = Text("HÀM SỐ LẤY MẪU", font_size=32, color=NVIDIA_GREEN,
                           weight=BOLD).move_to(anh_text.get_center() + DOWN * 1.0)
        self.play_timed("sample", 13, 15, FadeIn(sample_text))
        self.wait_timed("hold_revelation", 15, 25)

        # ── Beat 2: [5:25–5:40] CNN warning ──
        self.play_timed("clear_beat1", 25, 25.5,
                        *[FadeOut(m) for m in [heatmap, heatmap_label, grid_lines,
                                               anh_text, strike, sample_text]])

        cnn_label = Text("CNN + lưới 64×64", font_size=28, color=MUTED).shift(UP * 1)

        barrier = Rectangle(width=8, height=0.15, fill_color=WARNING,
                            fill_opacity=0.8, stroke_width=0).shift(DOWN * 0.3)
        barrier_label = MathTex(r"\times", font_size=60, color=WARNING).next_to(barrier, UP, buff=0.1)

        warning_lines = VGroup(
            Text("Ném đi bản chất liên tục", font_size=24, color=WARNING),
            Text("→ Bị ràng buộc lưới", font_size=24, color=WARNING),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 1.5)

        self.play_timed("cnn", 25.5, 27, FadeIn(cnn_label))
        self.play_timed("barrier", 27, 29, FadeIn(barrier), FadeIn(barrier_label))
        self.play_timed("warning", 29, 31, FadeIn(warning_lines))
        self.wait_timed("hold_end", 31, 39)

        self.play_timed("cut", 39, 40, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
