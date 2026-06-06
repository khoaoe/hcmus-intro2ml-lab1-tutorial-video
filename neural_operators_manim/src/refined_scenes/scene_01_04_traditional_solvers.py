"""
Scene 1.4 — Traditional Solvers & 4 hạn chế
Source: original_outline.tex, Section 1, Scene 1.4
Global time: 2:30 – 3:30
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0104_TraditionalSolvers(TimedScene):
    SCRIPT_ID = "1.4"
    SCRIPT_TITLE = "Traditional Solvers & 4 hạn chế"
    SCRIPT_START = 150.0
    SCRIPT_END = 210.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [2:30–2:50] PDE → Finite Diff → Fixed Grid flowchart ──
        pde_eq = MathTex(
            r"-\nabla \cdot (a \nabla u) = f",
            font_size=38, color=TEXT
        ).shift(UP * 2)

        # Flowchart nodes
        pde_node = RoundedRectangle(width=3.2, height=0.8, corner_radius=0.1,
                                    stroke_color=PURPLE, fill_color=CARD_BG, fill_opacity=0.6)
        pde_text = Text("PDE", font_size=22, color=PURPLE).move_to(pde_node)
        pde_g = VGroup(pde_node, pde_text).shift(LEFT * 4)

        fd_node = RoundedRectangle(width=3.2, height=0.8, corner_radius=0.1,
                                   stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.6)
        fd_text = Text("Finite Difference", font_size=18, color=INPUT).move_to(fd_node)
        fd_g = VGroup(fd_node, fd_text)

        grid_node = RoundedRectangle(width=3.2, height=0.8, corner_radius=0.1,
                                     stroke_color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.6)
        grid_text = Text("Fixed Grid", font_size=22, color=OPERATOR).move_to(grid_node)
        grid_g = VGroup(grid_node, grid_text).shift(RIGHT * 4)

        arrows = VGroup(
            Arrow(pde_node.get_right(), fd_node.get_left(), color=MUTED, buff=0.15),
            Arrow(fd_node.get_right(), grid_node.get_left(), color=MUTED, buff=0.15),
        )

        self.play_timed("pde_eq", 0, 3, FadeIn(pde_eq))
        self.play_timed("flowchart", 3, 8,
                        FadeIn(pde_g), FadeIn(arrows[0]),
                        FadeIn(fd_g), FadeIn(arrows[1]),
                        FadeIn(grid_g))
        self.wait_timed("hold_flow", 8, 20)

        # ── Beat 2: [2:50–3:10] Grid refinement + timer explosion ──
        self.play_timed("clear_beat1", 20, 20.5,
                        *[FadeOut(m) for m in [pde_eq, pde_g, fd_g, grid_g, arrows]])

        resolutions = ["16²", "32²", "64²", "128²"]
        cost_labels = ["0.1s", "1s", "30s", "💥"]
        grid_groups = VGroup()

        for i, (res, cost) in enumerate(zip(resolutions, cost_labels)):
            n = [4, 6, 10, 14][i]
            mini_grid = VGroup(*[
                Square(side_length=3.0 / n, stroke_width=0.5, stroke_color=GRID,
                       fill_color=INPUT, fill_opacity=0.1 + 0.15 * i)
                for _ in range(n * n)
            ]).arrange_in_grid(rows=n, cols=n, buff=0.02)
            res_label = Text(res, font_size=18, color=TEXT).next_to(mini_grid, UP, buff=0.15)
            cost_label = Text(cost, font_size=16,
                              color=WARNING if i == 3 else MUTED).next_to(mini_grid, DOWN, buff=0.15)
            grid_groups.add(VGroup(mini_grid, res_label, cost_label))

        grid_groups.arrange(RIGHT, buff=0.6)

        for i, gg in enumerate(grid_groups):
            t = 20.5 + i * 2.5
            self.play_timed(f"grid_{i}", t, t + 1.5, FadeIn(gg))

        self.wait_timed("hold_grids", 30.5, 40)

        # ── Beat 3: [3:10–3:30] 4 limitation icons ──
        self.play_timed("clear_beat2", 40, 40.5, *[FadeOut(m) for m in grid_groups])

        limitations = [
            ("Sai số tham số hóa", WARNING),
            ("Chi phí bùng nổ", WARNING),
            ("Rào cản chuyên môn", WARNING),
            ("Không khả vi", WARNING),
        ]
        limit_icons = VGroup()
        for text, color in limitations:
            icon = VGroup(
                Circle(radius=0.35, stroke_color=color, fill_color=color, fill_opacity=0.15),
                Text("⚠", font_size=24, color=color),
            )
            icon[1].move_to(icon[0])
            label = Text(text, font_size=18, color=TEXT).next_to(icon, DOWN, buff=0.2)
            limit_icons.add(VGroup(icon, label))
        limit_icons.arrange(RIGHT, buff=1.2)

        for i, li in enumerate(limit_icons):
            t = 40.5 + i * 2.0
            self.play_timed(f"limit_{i}", t, t + 1.0, FadeIn(li))

        note = Text(
            "Mục tiêu: bổ sung ML, không thay thế solver",
            font_size=20, color=MUTED
        ).to_edge(DOWN, buff=0.5)
        self.play_timed("note", 49, 50, FadeIn(note))
        self.wait_timed("hold_end", 50, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
