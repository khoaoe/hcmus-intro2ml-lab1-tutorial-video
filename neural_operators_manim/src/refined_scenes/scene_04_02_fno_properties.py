"""
Scene 4.2 — Tính chất FNO & Giới hạn
Source: original_outline.tex, Section 4, Scene 4.2
Global time: 12:30 – 13:15
Duration: 45s
"""

from manim import *

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0402_FNOProperties(TimedScene):
    SCRIPT_ID = "4.2"
    SCRIPT_TITLE = "Tính chất FNO & Giới hạn"
    SCRIPT_START = 750.0
    SCRIPT_END = 795.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("FNO: 3 tính chất đột phá", font_size=28,
                     color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.4)

        # 3 property cards
        cards_data = [
            ("Tốc độ", r"O(N \log N)", "Lưới triệu điểm\ntrong vài giây", INPUT),
            ("Tầm nhìn toàn cục", "Global", "Một phép nhân tần số\nkết nối mọi điểm", OPERATOR),
            ("Zero-shot Resolution", "64→256", "Train 64×64,\nquery 256×256", OUTPUT),
        ]

        cards = VGroup()
        for name, badge, desc, color in cards_data:
            box = RoundedRectangle(width=4.0, height=3.0, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.6)
            card_title = Text(name, font_size=20, color=color, weight=BOLD).move_to(
                box.get_top() + DOWN * 0.4)
            badge_text = Text(badge, font_size=28, color=TEXT, weight=BOLD).move_to(box)
            card_desc = Text(desc, font_size=14, color=MUTED).move_to(
                box.get_bottom() + UP * 0.6)
            cards.add(VGroup(box, card_title, badge_text, card_desc))

        cards.arrange(RIGHT, buff=0.5)

        # Function space overlay
        func_space = MathTex(r"\mathcal{A} \to \mathcal{U}",
                             font_size=24, color=NVIDIA_GREEN).to_edge(DOWN, buff=1.2)

        self.play_timed("title", 0, 2, FadeIn(title))

        for i, card in enumerate(cards):
            t = 2 + i * 5
            self.play_timed(f"card_{i}", t, t + 2, FadeIn(card))
            self.wait_timed(f"hold_card_{i}", t + 2, t + 5)

        self.play_timed("func_space", 17, 18, FadeIn(func_space))
        self.wait_timed("hold_cards", 18, 30)

        # Warning: limitations
        warning_box = RoundedRectangle(width=10, height=1.2, corner_radius=0.1,
                                       stroke_color=WARNING, fill_color=CARD_BG, fill_opacity=0.6)
        warning_text = Text(
            "⚠ Giới hạn: phù hợp nhất với lưới đều & biên tuần hoàn",
            font_size=20, color=WARNING
        ).move_to(warning_box)
        warning_group = VGroup(warning_box, warning_text).to_edge(DOWN, buff=0.3)

        self.play_timed("warning", 30, 33, FadeIn(warning_group))
        self.wait_timed("hold_end", 33, 44)

        self.play_timed("cut", 44, 45, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
