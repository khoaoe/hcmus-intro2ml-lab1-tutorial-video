"""
Scene 2.4 — Thách thức & Định nghĩa Neural Operator
Source: original_outline.tex, Section 2, Scene 2.4
Global time: 6:40 – 7:30
Duration: 50s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0204_ChallengesAndDefinition(TimedScene):
    SCRIPT_ID = "2.4"
    SCRIPT_TITLE = "Thách thức & Định nghĩa Neural Operator"
    SCRIPT_START = 400.0
    SCRIPT_END = 450.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [6:40–7:00] 3 different grids + discretization invariance ──
        grids = VGroup()
        grid_data = [
            ("64×64 vuông", 8, INPUT),
            ("Tam giác bất quy tắc", 0, PURPLE),  # special handling
            ("128×128 mịn", 14, OUTPUT),
        ]

        # Regular grid
        g1 = VGroup(*[
            Square(side_length=0.22, stroke_width=0.5, stroke_color=INPUT,
                   fill_color=INPUT, fill_opacity=0.1)
            for _ in range(64)
        ]).arrange_in_grid(rows=8, cols=8, buff=0.02)
        l1 = Text("64×64", font_size=16, color=INPUT).next_to(g1, DOWN, buff=0.15)
        grids.add(VGroup(g1, l1))

        # Irregular mesh (triangle-ish dots)
        np.random.seed(42)
        irregular = VGroup(*[
            Dot(point=np.array([np.random.uniform(-1.2, 1.2),
                                np.random.uniform(-1.2, 1.2), 0]),
                radius=0.04, color=PURPLE)
            for _ in range(40)
        ])
        l2 = Text("Bất quy tắc", font_size=16, color=PURPLE).next_to(irregular, DOWN, buff=0.15)
        grids.add(VGroup(irregular, l2))

        # Fine grid
        g3 = VGroup(*[
            Square(side_length=0.12, stroke_width=0.3, stroke_color=OUTPUT,
                   fill_color=OUTPUT, fill_opacity=0.1)
            for _ in range(196)
        ]).arrange_in_grid(rows=14, cols=14, buff=0.01)
        l3 = Text("128×128", font_size=16, color=OUTPUT).next_to(g3, DOWN, buff=0.15)
        grids.add(VGroup(g3, l3))

        grids.arrange(RIGHT, buff=1.0).shift(UP * 0.5)

        self.play_timed("grids", 0, 4, FadeIn(grids))

        # Discretization Invariance label
        di_label = Text("Discretization Invariance", font_size=28,
                        color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("di_label", 4, 6, FadeIn(di_label))

        # Query dot moving freely
        query_dot = Dot(radius=0.1, color=OPERATOR)
        query_label = Text("Query tại bất kỳ điểm", font_size=20,
                           color=OPERATOR).to_edge(DOWN, buff=1.5)
        cq_label = Text("Continuous Query", font_size=28,
                        color=OPERATOR, weight=BOLD).next_to(di_label, DOWN, buff=0.3)

        self.play_timed("query_label", 6, 8, FadeIn(query_label), FadeIn(cq_label))

        # Animate query dot moving
        path_points = [LEFT * 5, LEFT * 2, ORIGIN, RIGHT * 2, RIGHT * 5]
        query_dot.move_to(path_points[0])
        self.add(query_dot)
        for i, pt in enumerate(path_points[1:]):
            self.play_timed(f"query_move_{i}", 8 + i * 2, 10 + i * 2,
                            query_dot.animate.move_to(pt))

        self.wait_timed("hold_challenges", 16, 20)

        # ── Beat 2: [7:00–7:30] 4-criteria checklist ──
        self.play_timed("clear_beat1", 20, 20.5,
                        *[FadeOut(m) for m in [grids, di_label, query_label,
                                               cq_label, query_dot]])

        checklist_title = Text("Neural Operator: 4 tiêu chí", font_size=30,
                               color=TEXT, weight=BOLD).shift(UP * 3)

        criteria = [
            "1. Input mọi độ phân giải",
            "2. Output truy vấn mọi điểm",
            "3. Hội tụ giới hạn liên tục",
            "4. Nhanh hơn solver hàng nghìn lần",
        ]
        checks = VGroup()
        for cr in criteria:
            check = Text("✓", font_size=28, color=NVIDIA_GREEN)
            text = Text(cr, font_size=22, color=TEXT)
            row = VGroup(check, text).arrange(RIGHT, buff=0.3)
            checks.add(row)
        checks.arrange(DOWN, buff=0.5, aligned_edge=LEFT).shift(DOWN * 0.3)

        self.play_timed("checklist_title", 20.5, 22, FadeIn(checklist_title))

        for i, ch in enumerate(checks):
            t = 22 + i * 3.0
            self.play_timed(f"check_{i}", t, t + 1.5, FadeIn(ch))

        self.wait_timed("hold_checklist", 34, 38)

        # Section transition
        section_hint = Text("Phần tiếp theo: cấu trúc bên trong",
                            font_size=22, color=MUTED).to_edge(DOWN, buff=0.5)
        self.play_timed("hint", 38, 40, FadeIn(section_hint))
        self.wait_timed("hold_end", 40, 49)

        self.play_timed("cut", 49, 50, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
