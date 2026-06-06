"""
Scene 4.6 — Tổng kết kiến trúc & Chuyển cảnh
Source: original_outline.tex, Section 4, Scene 4.6
Global time: 17:00 – 17:25
Duration: 25s
"""

from manim import *

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0406_ArchitectureSummary(TimedScene):
    SCRIPT_ID = "4.6"
    SCRIPT_TITLE = "Tổng kết kiến trúc & Chuyển cảnh"
    SCRIPT_START = 1020.0
    SCRIPT_END = 1045.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Tổng kết: Chọn kiến trúc nào?", font_size=28,
                     color=TEXT, weight=BOLD).to_edge(UP, buff=0.4)

        # Decision grid — 4 architectures
        grid_data = [
            ("FNO", "Lưới đều\nTốc độ", INPUT),
            ("GNO", "Mesh phức tạp", PURPLE),
            ("U-NO", "Nghiệm đa tỷ lệ", OUTPUT),
            ("CoDANO", "Nhiều biến\ntương tác", OPERATOR),
        ]

        grid_cards = VGroup()
        for name, use_case, color in grid_data:
            box = RoundedRectangle(width=3.0, height=1.8, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.6)
            arch_name = Text(name, font_size=24, color=color, weight=BOLD).move_to(
                box.get_top() + DOWN * 0.4)
            desc = Text(use_case, font_size=14, color=MUTED).move_to(
                box.get_center() + DOWN * 0.2)
            check = Text("✓", font_size=22, color=NVIDIA_GREEN).move_to(
                box.get_corner(UR) + DL * 0.25)
            grid_cards.add(VGroup(box, arch_name, desc, check))

        grid_cards.arrange_in_grid(rows=2, cols=2, buff=0.4).shift(UP * 0.3)

        # Hybrid SOTA badge
        hybrid_badge = VGroup(
            RoundedRectangle(width=4, height=0.6, corner_radius=0.1,
                             stroke_color=NVIDIA_GREEN, fill_color=NVIDIA_GREEN, fill_opacity=0.15),
            Text("Hybrid = SOTA", font_size=22, color=NVIDIA_GREEN, weight=BOLD),
        )
        hybrid_badge[1].move_to(hybrid_badge[0])
        hybrid_badge.shift(DOWN * 2.5)

        # 4 core components
        components = VGroup(
            Text("Tích phân", font_size=14, color=OPERATOR),
            Text("Residual", font_size=14, color=NVIDIA_GREEN),
            Text("Bias hàm", font_size=14, color=MUTED),
            Text("CNN đạo hàm", font_size=14, color=INPUT),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.3)

        self.play_timed("title", 0, 2, FadeIn(title))
        self.play_timed("grid", 2, 7, FadeIn(grid_cards))
        self.play_timed("hybrid", 7, 9, FadeIn(hybrid_badge))
        self.play_timed("components", 9, 12, FadeIn(components))
        self.wait_timed("hold_summary", 12, 20)

        # Section transition
        self.play_timed("clear", 20, 20.5,
                        *[FadeOut(m) for m in [title, grid_cards, hybrid_badge, components]])

        next_section = Text(
            "Section 5: Ứng dụng thực tế",
            font_size=34, color=TEXT, weight=BOLD
        )
        self.play_timed("next", 20.5, 22, FadeIn(next_section))
        self.wait_timed("hold_next", 22, 24)
        self.play_timed("cut", 24, 25, FadeOut(next_section, run_time=0.3))
        self.pad_to(self.SCENE_DURATION)
