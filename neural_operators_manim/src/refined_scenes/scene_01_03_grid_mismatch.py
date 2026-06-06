"""
Scene 1.3 — Grid Mismatch & Ràng buộc vật lý
Source: original_outline.tex, Section 1, Scene 1.3
Global time: 1:45 – 2:30
Duration: 45s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0103_GridMismatch(TimedScene):
    SCRIPT_ID = "1.3"
    SCRIPT_TITLE = "Grid Mismatch & Ràng buộc vật lý"
    SCRIPT_START = 105.0
    SCRIPT_END = 150.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def _make_grid(self, n, color, label_text, x_offset):
        """Create an n×n grid centered at x_offset."""
        cell_size = 4.0 / n
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(
                    side_length=cell_size * 0.95,
                    stroke_width=0.5 if n > 10 else 1.0,
                    stroke_color=color,
                    fill_color=color,
                    fill_opacity=0.15,
                )
                sq.move_to(np.array([
                    x_offset + (j - n / 2 + 0.5) * cell_size,
                    (i - n / 2 + 0.5) * cell_size,
                    0
                ]))
                grid.add(sq)
        label = Text(label_text, font_size=20, color=color).next_to(grid, DOWN, buff=0.25)
        return VGroup(grid, label)

    def construct(self):
        # ── Beat 1: [1:45–2:00] Two grids side-by-side ──
        coarse = self._make_grid(8, INPUT, "64 × 64 (thô)", -3.5)
        fine = self._make_grid(16, PURPLE, "128 × 128 (mịn)", 3.5)

        # Sample same function on both
        func_label = Text("Cùng 1 hàm nhiệt độ", font_size=22, color=MUTED).to_edge(UP, buff=0.5)

        self.play_timed("grids_in", 0, 3,
                        FadeIn(coarse), FadeIn(fine), FadeIn(func_label))
        self.wait_timed("hold_grids", 3, 15)

        # ── Beat 2: [2:00–2:15] Train on coarse → test on fine → GLITCH ──
        self.play_timed("clear_grids", 15, 15.5,
                        FadeOut(coarse), FadeOut(fine), FadeOut(func_label))

        train_box = RoundedRectangle(width=4, height=2.5, corner_radius=0.15,
                                     stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.6)
        train_label = Text("Train: 64×64", font_size=22, color=INPUT).move_to(train_box.get_top() + DOWN * 0.4)
        model_icon = Text("Model ✓", font_size=20, color=OUTPUT).move_to(train_box)
        train_group = VGroup(train_box, train_label, model_icon).shift(LEFT * 3.5)

        test_box = RoundedRectangle(width=4, height=2.5, corner_radius=0.15,
                                    stroke_color=WARNING, fill_color=CARD_BG, fill_opacity=0.6)
        test_label = Text("Test: 128×128", font_size=22, color=WARNING).move_to(test_box.get_top() + DOWN * 0.4)
        glitch_text = Text("GRID MISMATCH", font_size=28, color=WARNING, weight=BOLD).move_to(test_box)
        cross = Text("✗", font_size=60, color=WARNING).move_to(test_box)
        test_group = VGroup(test_box, test_label).shift(RIGHT * 3.5)

        arrow = Arrow(train_box.get_right(), test_box.get_left(), color=MUTED, buff=0.3)

        self.play_timed("train", 15.5, 17, FadeIn(train_group))
        self.play_timed("arrow", 17, 18, FadeIn(arrow))
        self.play_timed("test", 18, 19, FadeIn(test_group))
        self.play_timed("glitch", 19, 20, FadeIn(cross), FadeIn(glitch_text))
        self.wait_timed("hold_mismatch", 20, 30)

        # ── Beat 3: [2:15–2:30] Physics constraints overlay ──
        self.play_timed("clear_beat2", 30, 30.5,
                        *[FadeOut(m) for m in [train_group, arrow, test_group, cross, glitch_text]])

        physics_eqs = VGroup(
            MathTex(r"\nabla u", font_size=40, color=PHYSICS),
            MathTex(r"\int u \, dx", font_size=40, color=PHYSICS),
        ).arrange(RIGHT, buff=2.0)

        barrier_text = Text(
            "Discretization Dependence = Barrier to Science",
            font_size=26, color=WARNING, weight=BOLD
        ).to_edge(DOWN, buff=0.8)

        self.play_timed("physics", 30.5, 33, FadeIn(physics_eqs))
        self.play_timed("barrier", 33, 35, FadeIn(barrier_text))
        self.wait_timed("hold_end", 35, 44)

        self.play_timed("cut", 44, 45, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
