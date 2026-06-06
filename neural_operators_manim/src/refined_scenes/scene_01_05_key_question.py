"""
Scene 1.5 — Câu hỏi then chốt & Teaser Neural Operators
Source: original_outline.tex, Section 1, Scene 1.5
Global time: 3:30 – 4:00
Duration: 30s
"""

from manim import *

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0105_KeyQuestionTeaser(TimedScene):
    SCRIPT_ID = "1.5"
    SCRIPT_TITLE = "Câu hỏi then chốt & Teaser Neural Operators"
    SCRIPT_START = 210.0
    SCRIPT_END = 240.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [3:30–3:45] Split screen: R^n→R^m vs A→U ──
        left_title = Text("DL truyền thống", font_size=22, color=MUTED).shift(LEFT * 4 + UP * 3)
        left_eq = MathTex(
            r"f_\theta: \mathbb{R}^n \to \mathbb{R}^m",
            font_size=38, color=INPUT
        ).shift(LEFT * 4)
        left_desc = Text("Vector → Vector", font_size=18, color=MUTED).next_to(left_eq, DOWN, buff=0.3)

        right_title = Text("Operator Learning", font_size=22, color=NVIDIA_GREEN).shift(RIGHT * 4 + UP * 3)
        right_eq = MathTex(
            r"G_\theta: \mathcal{A} \to \mathcal{U}",
            font_size=38, color=NVIDIA_GREEN
        ).shift(RIGHT * 4)
        right_desc = Text("Hàm → Hàm", font_size=18, color=OUTPUT).next_to(right_eq, DOWN, buff=0.3)

        divider = Line(UP * 3.5, DOWN * 3.5, color=GRID, stroke_width=1)

        left_group = VGroup(left_title, left_eq, left_desc)
        right_group = VGroup(right_title, right_eq, right_desc)

        self.play_timed("split_screen", 0, 3,
                        FadeIn(divider), FadeIn(left_group), FadeIn(right_group))
        self.wait_timed("hold_split", 3, 15)

        # ── Beat 2: [3:45–3:55] Question mark → Neural Operator logo ──
        self.play_timed("clear_split", 15, 15.5,
                        FadeOut(left_group), FadeOut(right_group), FadeOut(divider))

        question = Text("?", font_size=120, color=OPERATOR)
        self.play_timed("question", 15.5, 17, FadeIn(question, scale=2))

        self.play_timed("clear_q", 17, 17.3, FadeOut(question))

        logo_text = Text("Neural Operators", font_size=52, color=NVIDIA_GREEN, weight=BOLD)
        logo_sub = Text("AI học trên không gian vô hạn chiều", font_size=24, color=MUTED)
        logo = VGroup(logo_text, logo_sub).arrange(DOWN, buff=0.4)

        self.play_timed("logo", 17.3, 19, FadeIn(logo))
        self.wait_timed("hold_logo", 19, 25)

        # ── Beat 3: [3:55–4:00] Fade to black + section title ──
        self.play_timed("clear_logo", 25, 25.5, FadeOut(logo))

        section_title = Text(
            "Section 2: Thế giới hàm số",
            font_size=34, color=TEXT, weight=BOLD
        )
        self.play_timed("section_2", 25.5, 27, FadeIn(section_title))
        self.wait_timed("hold_section", 27, 29)
        self.play_timed("cut", 29, 30, FadeOut(section_title, run_time=0.3))
        self.pad_to(self.SCENE_DURATION)
