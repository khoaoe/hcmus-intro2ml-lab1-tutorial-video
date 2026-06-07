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

        # Decision grid — 4 architectures (giảm height, tăng buff)
        grid_data = [
            ("FNO", "Lưới đều\nTốc độ", INPUT),
            ("GNO", "Mesh phức tạp", PURPLE),
            ("U-NO", "Đa tỷ lệ", OUTPUT),  # Rút gọn text
            ("CoDANO", "Nhiều biến", OPERATOR),  # Rút gọn text
        ]

        grid_cards = VGroup()
        for name, use_case, color in grid_data:
            box = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.1,
                                   stroke_color=color, stroke_width=2,
                                   fill_color=CARD_BG, fill_opacity=0.6)
            arch_name = Text(name, font_size=22, color=color, weight=BOLD).move_to(
                box.get_top() + DOWN * 0.35)
                
            if "\n" in use_case:
                desc = VGroup(*[Text(line, font_size=16, color=MUTED) for line in use_case.split("\n")])
                desc.arrange(DOWN, buff=0.1)
            else:
                desc = Text(use_case, font_size=16, color=MUTED)
                
            desc.move_to(box.get_center() + DOWN * 0.1)
            
            check = Text("✓", font_size=20, color=NVIDIA_GREEN).move_to(
                box.get_corner(UR) + DL * 0.2)
            grid_cards.add(VGroup(box, arch_name, desc, check))

        grid_cards.arrange_in_grid(rows=2, cols=2, buff=0.5).shift(UP * 0.5)

        self.play_timed("title", 0, 1.5, FadeIn(title))
        
        # FadeIn từng card sync với VO
        for i, card in enumerate(grid_cards):
            start = 1.5 + i * 1.2
            end = start + 1.2
            self.play_timed(f"card_{i}", start, end, FadeIn(card, shift=UP*0.2))

        # Hybrid badge - nhấn mạnh với pulse
        hybrid_badge = VGroup(
            RoundedRectangle(width=3.5, height=0.5, corner_radius=0.1,
                             stroke_color=NVIDIA_GREEN, fill_color=NVIDIA_GREEN, 
                             fill_opacity=0.2, stroke_width=2),
            Text("Hybrid = SOTA", font_size=20, color=NVIDIA_GREEN, weight=BOLD),
        )
        hybrid_badge[1].move_to(hybrid_badge[0])
        hybrid_badge.shift(DOWN * 1.8)

        self.play_timed("hybrid", 6.5, 8, 
                        FadeIn(hybrid_badge, scale=0.8),
                        *[m.animate.set_opacity(0.4) for m in grid_cards])  # Mờ grid
        
        # Pulse hybrid badge
        self.play_timed("hybrid_pulse", 8, 9.5,
                        hybrid_badge.animate.scale(1.05).set_stroke(width=3),
                        rate_func=there_and_back)

        # 4 core components - xuất hiện tuần tự
        components = VGroup(
            Text(" Tích phân", font_size=15, color=OPERATOR, weight=BOLD),
            Text("+ Residual", font_size=15, color=NVIDIA_GREEN),
            Text("+ Bias hàm", font_size=15, color=MUTED),
            Text("+ CNN đạo hàm", font_size=15, color=INPUT),
        ).arrange(RIGHT, buff=0.6).shift(DOWN * 2.8)

        for i, comp in enumerate(components):
            start = 9.5 + i * 0.6
            end = start + 0.6
            self.play_timed(f"comp_{i}", start, end, FadeIn(comp, shift=RIGHT*0.2))

        self.wait_timed("hold_summary", 12, 17)  # Giảm từ 8s → 5s

        # Transition sang Section 5 - mạnh hơn
        self.play_timed("clear", 17, 17.5,
                        *[FadeOut(m, run_time=0.3) for m in [title, grid_cards, 
                                                              hybrid_badge, components]])

        next_section = VGroup(
            Text("Section 5", font_size=40, color=TEXT, weight=BOLD),
            Text("Ứng dụng thực tế", font_size=28, color=MUTED),
        ).arrange(DOWN, buff=0.2)

        self.play_timed("next", 17.5, 19.5, 
                        FadeIn(next_section, shift=UP*0.5, scale=0.9))
        self.wait_timed("hold_next", 19.5, 23)
        self.play_timed("cut", 23, 25, FadeOut(next_section, run_time=0.5))
        self.pad_to(self.SCENE_DURATION)
