"""
Scene 6.5 — Resources & Closing remarks
Source: original_outline.tex, Section 6, Scene 6.5
Global time: 28:55 – 29:25
Duration: 30s
"""
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

# Fallback colors
BLACK = "#0b1020"
OPERATOR = "#76B900" # NVIDIA Green
PHYSICS = "#00FFFF"  # Cyan
NVIDIA_GREEN = "#76B900"
GRAY_B = "#AAAAAA"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"

class Scene0605_Resources_Closing(TimedScene):
    SCRIPT_ID = "6.5"
    SCRIPT_TITLE = "Resources & Closing"
    SCRIPT_START = 1735.0
    SCRIPT_END = 1765.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # BEAT 1: [28:55–29:10] The Starter Kit (15s)
        # ═══════════════════════════════════════════════════════════════
        
        # Title
        title = Text("Starter Kit: Bắt đầu từ đâu?", font_size=32,
                     color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("b1_title", 0, 1.5, Write(title))

        # --- LEFT: THEORY (Papers) ---
        theory_header = Text("1. Nền tảng Lý thuyết", font_size=20, color=PHYSICS, weight=BOLD).shift(LEFT*3.8 + UP*2.0)
        
        # Paper 1
        p1_box = RoundedRectangle(width=4.8, height=1.1, corner_radius=0.15,
                                  stroke_color=PHYSICS, fill_color="#111827", fill_opacity=0.8, stroke_width=1.5)
        p1_line1 = Text("Neural Operator: Learning Maps", font_size=16, color=WHITE, weight=BOLD)
        p1_line2 = Text("Between Function Spaces", font_size=16, color=WHITE, weight=BOLD)
        p1_title = VGroup(p1_line1, p1_line2).arrange(DOWN, buff=0.1).move_to(p1_box.get_top() + DOWN*0.35)
        p1_auth = Text("Kovachki, Li, et al. (JMLR 2021)", 
                       font_size=13, color=GRAY_B).next_to(p1_title, DOWN, buff=0.2)
        paper1 = VGroup(p1_box, p1_title, p1_auth).shift(LEFT*3.8 + UP*0.9)

        # Paper 2
        p2_box = RoundedRectangle(width=4.8, height=1.1, corner_radius=0.15,
                                  stroke_color=PHYSICS, fill_color="#111827", fill_opacity=0.8, stroke_width=1.5)
        p2_line1 = Text("Fourier Neural Operator for", font_size=16, color=WHITE, weight=BOLD)
        p2_line2 = Text("Parametric PDEs", font_size=16, color=WHITE, weight=BOLD)
        p2_title = VGroup(p2_line1, p2_line2).arrange(DOWN, buff=0.1).move_to(p2_box.get_top() + DOWN*0.35)
        p2_auth = Text("Li, Kovachki, et al. (ICLR 2021)", 
                       font_size=13, color=GRAY_B).next_to(p2_title, DOWN, buff=0.2)
        paper2 = VGroup(p2_box, p2_title, p2_auth).shift(LEFT*3.8 + DOWN*0.9)

        self.play_timed("b1_theory", 1.5, 5.5,
                        FadeIn(theory_header),
                        FadeIn(paper1, shift=RIGHT*0.2),
                        FadeIn(paper2, shift=RIGHT*0.2))

        # --- RIGHT: CODE (Libraries & Terminal) ---
        code_header = Text("2. Công cụ Thực chiến", font_size=20, color=OPERATOR, weight=BOLD).shift(RIGHT*3.8 + UP*2.0)
        
        # Terminal Window (macOS style)
        term_bg = RoundedRectangle(width=6.8, height=3.2, corner_radius=0.15,
                                   stroke_color=GRAY_B, fill_color="#0d1117", fill_opacity=0.95, stroke_width=1.5)
        term_bg.shift(RIGHT*3.8 + UP*0.1)
        
        # Terminal Dots
        dots = VGroup(Dot(color="#FF5F56", radius=0.06), Dot(color="#FFBD2E", radius=0.06), Dot(color="#27C93F", radius=0.06)).arrange(RIGHT, buff=0.12)
        dots.move_to(term_bg.get_top() + DOWN*0.15 + LEFT*(term_bg.width/2 - 0.3))
        
        # Terminal Text (Dùng font Monospace để giả lập code)
        t_line1 = Text("$ pip install neuraloperator", font="Monospace", font_size=18, color="#A5D6FF")
        t_line2 = Text(">>> from neuralop.models import FNO", font="Monospace", font_size=18, color="#A5D6FF")
        t_line3 = Text(">>> model = FNO(n_modes=(64,64), ...)", font="Monospace", font_size=18, color="#A5D6FF")
        
        term_code = VGroup(t_line1, t_line2, t_line3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        term_code.move_to(term_bg).shift(DOWN*0.05)
        
        terminal = VGroup(term_bg, dots, term_code)

        self.play_timed("b1_code", 5.5, 9.5,
                        FadeIn(code_header),
                        FadeIn(terminal, scale=0.9))

        # --- BOTTOM: HUB (No QR, just clean URL/Description callout) ---
        hub_box = RoundedRectangle(width=11.5, height=1.0, corner_radius=0.2,
                                   stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.1, stroke_width=2)
        hub_box.shift(DOWN*2.5)
        
        hub_text = Text("Toàn bộ Code, Slides và Papers đã được để sẵn ở phần MÔ TẢ (Description)", 
                        font_size=20, color=YELLOW, weight=BOLD).move_to(hub_box)
        
        hub_group = VGroup(hub_box, hub_text)

        self.play_timed("b1_hub", 9.5, 12.5,
                        FadeIn(hub_group, shift=UP*0.2))
        
        self.wait_timed("b1_hold", 12.5, 15)

        # ═══════════════════════════════════════════════════════════════
        # BEAT 2: [29:10–29:25] The Final Synthesis (15s)
        # ═══════════════════════════════════════════════════════════════
        self.play_timed("clear_b1", 15, 16.5,
                        *[FadeOut(m) for m in [title, theory_header, paper1, paper2, 
                                               code_header, terminal, hub_group]])

        # Mathematical Isomorphisms (Chốt hạ bằng Toán học)
        iso1 = MathTex(r"\sum", r"\xrightarrow{\Delta x \to 0}", r"\int", font_size=36)
        iso2 = MathTex(r"\mathbb{R}^n", r"\xrightarrow{N \to \infty}", r"\mathcal{A}", font_size=36)
        iso3 = MathTex(r"W", r"\xrightarrow{\text{continuum}}", r"\kappa(y,x)", font_size=36)
        
        isos = VGroup(iso1, iso2, iso3).arrange(RIGHT, buff=1.5).shift(UP*2.0)
        
        self.play_timed("b2_isos", 16.5, 18.5,
                        LaggedStart(*[Write(i) for i in isos], lag_ratio=0.3))
        
        # Hold math on screen
        self.wait_timed("b2_hold_math", 18.5, 19.5)

        # Closing Text
        closing_line1 = Text("Neural Operators không phải thứ gì bí ẩn.", 
                            font_size=28, color=WHITE, weight=BOLD).shift(UP*0.5)
        
        closing_line2 = Text("Chúng là sự tổng quát hóa tự nhiên của", 
                            font_size=20, color=GRAY_B).shift(DOWN*0.2)
        
        closing_keywords = VGroup(
            Text("tổng Riemann", font_size=22, color=OPERATOR, weight=BOLD),
            Text("tích phân", font_size=22, color=OPERATOR, weight=BOLD),
            Text("và MLP", font_size=22, color=OPERATOR, weight=BOLD)
        ).arrange(RIGHT, buff=0.6).shift(DOWN*0.8)
        
        closing_line3 = Text("lên không gian vô hạn chiều.", 
                            font_size=20, color=GRAY_B).shift(DOWN*1.4)

        # Show the main quote completely first
        self.play_timed("b2_text_1", 19.5, 21.0,
                        Write(closing_line1))

        # Then show the rest of the explanation
        self.play_timed("b2_text_2", 21.0, 24.5,
                        FadeIn(closing_line2),
                        LaggedStart(*[FadeIn(k, shift=UP*0.1) for k in closing_keywords], lag_ratio=0.2),
                        FadeIn(closing_line3))

        # Final CTA & Thank You
        thank_you = Text("Cảm ơn bạn đã xem đến cuối. Hẹn gặp lại!", 
                        font_size=20, color=WHITE).shift(DOWN*2.5)
        
        self.play_timed("b2_thanks", 24.5, 26.5, FadeIn(thank_you, shift=UP*0.2))

        self.wait_timed("b2_hold", 26.5, 28.5)

        # Fade to black
        self.play_timed("fade_out", 28.5, 30,
                        *[FadeOut(m, run_time=1.5) for m in self.mobjects])
        
        self.pad_to(self.SCENE_DURATION)
