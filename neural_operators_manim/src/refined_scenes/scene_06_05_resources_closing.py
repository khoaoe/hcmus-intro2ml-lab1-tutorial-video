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
CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

class Scene0605_Resources_Closing(TimedScene):
    SCRIPT_ID = "6.5"
    SCRIPT_TITLE = "Resources & Closing"
    SCRIPT_START = 1735.0
    SCRIPT_END = 1765.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # BEAT 1: [28:55–29:10] Resources (15s)
        # ═══════════════════════════════════════════════════════════════
        title = Text("Resources để bắt đầu", font_size=28,
                     color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b1_title", 0, 1.5, FadeIn(title))

        # ── LIBRARIES ──
        lib_header = Text("Thư viện mã nguồn mở", font_size=20, color=GREEN_SCREEN, weight=BOLD).shift(LEFT*3.5 + UP*1.8)
        
        # NeuralOperator library
        no_logo = RoundedRectangle(width=2.8, height=0.7, corner_radius=0.1,
                                   stroke_color=GREEN_SCREEN, fill_color=BLACK, fill_opacity=0.8, stroke_width=2)
        no_txt = Text("neuraloperator", font_size=16, color=GREEN_SCREEN, weight=BOLD).move_to(no_logo)
        no_group = VGroup(no_logo, no_txt).shift(LEFT*3.5 + UP*1.0)
        
        no_link = Text("neuraloperator.github.io", font_size=12, color=GRAY_B).next_to(no_group, DOWN, buff=0.15)
        no_github = Text("github.com/neuraloperator/neuraloperator", font_size=10, color=GRAY_B).next_to(no_link, DOWN, buff=0.1)
        
        # NVIDIA Modulus
        nvidia_logo = RoundedRectangle(width=2.8, height=0.7, corner_radius=0.1,
                                       stroke_color=NVIDIA_GREEN, fill_color=BLACK, fill_opacity=0.8, stroke_width=2)
        nvidia_txt = Text("NVIDIA Modulus", font_size=16, color=NVIDIA_GREEN, weight=BOLD).move_to(nvidia_logo)
        nvidia_group = VGroup(nvidia_logo, nvidia_txt).shift(LEFT*3.5 + DOWN*0.5)
        
        nvidia_link = Text("developer.nvidia.com/modulus", font_size=12, color=GRAY_B).next_to(nvidia_group, DOWN, buff=0.15)

        self.play_timed("b1_libs", 1.5, 5,
                        FadeIn(lib_header),
                        FadeIn(no_group), Write(no_link), Write(no_github),
                        FadeIn(nvidia_group), Write(nvidia_link))

        # ── PAPERS ──
        paper_header = Text("Papers quan trọng", font_size=20, color=PHYSICS, weight=BOLD).shift(RIGHT*3.5 + UP*1.8)
        
        # Kovachki 2021
        paper1_box = RoundedRectangle(width=5.5, height=1.2, corner_radius=0.1,
                                      stroke_color=PHYSICS, fill_color=BLACK, fill_opacity=0.6, stroke_width=2)
        paper1_title = Text("Neural Operator: Learning Maps\nBetween Function Spaces", 
                           font_size=13, color=WHITE).move_to(paper1_box).shift(UP*0.2)
        paper1_authors = Text("Kovachki, Li, et al. — JMLR 2021", 
                             font_size=11, color=GRAY_B).next_to(paper1_title, DOWN, buff=0.15)
        paper1 = VGroup(paper1_box, paper1_title, paper1_authors).shift(RIGHT*3.5 + UP*0.8)
        
        # Li 2021 (FNO)
        paper2_box = RoundedRectangle(width=5.5, height=1.2, corner_radius=0.1,
                                      stroke_color=PHYSICS, fill_color=BLACK, fill_opacity=0.6, stroke_width=2)
        paper2_title = Text("Fourier Neural Operator for\nParametric Partial Differential Equations", 
                           font_size=13, color=WHITE).move_to(paper2_box).shift(UP*0.2)
        paper2_authors = Text("Li, Kovachki, et al. — ICLR 2021", 
                             font_size=11, color=GRAY_B).next_to(paper2_title, DOWN, buff=0.15)
        paper2 = VGroup(paper2_box, paper2_title, paper2_authors).shift(RIGHT*3.5 + DOWN*0.8)

        self.play_timed("b1_papers", 5, 9,
                        FadeIn(paper_header),
                        FadeIn(paper1),
                        FadeIn(paper2))

        # ── QR CODE (simplified representation) ──
        qr_box = Square(side_length=1.2, color=WHITE, fill_color=WHITE, fill_opacity=0.9, stroke_width=2)
        qr_box.shift(RIGHT*5.5 + DOWN*2.5)
        
        # Simplified QR pattern (just visual representation)
        qr_pattern = VGroup(*[
            Square(side_length=0.15, color=BLACK, fill_opacity=1, stroke_width=0)
            .move_to(qr_box.get_center() + RIGHT*x*0.2 + UP*y*0.2)
            for x in range(-2, 3) for y in range(-2, 3)
            if (abs(x) == 2 or abs(y) == 2) or (x == 0 and y == 0)
        ])
        
        qr_label = Text("Scan để truy cập", font_size=10, color=GRAY_B).next_to(qr_box, DOWN, buff=0.1)

        self.play_timed("b1_qr", 9, 11,
                        FadeIn(qr_box),
                        LaggedStart(*[FadeIn(s, scale=0.5) for s in qr_pattern], lag_ratio=0.05),
                        Write(qr_label))

        self.wait_timed("b1_hold", 11, 15)

        # ═══════════════════════════════════════════════════════════════
        # BEAT 2: [29:10–29:25] Closing Message (15s)
        # ═══════════════════════════════════════════════════════════════
        self.play_timed("clear_b1", 15, 16.5,
                        *[FadeOut(m) for m in [title, lib_header, no_group, no_link, no_github,
                                               nvidia_group, nvidia_link, paper_header,
                                               paper1, paper2, qr_box, qr_pattern, qr_label]])

        # Closing message - Typography focus
        closing_line1 = Text("Neural Operators không phải thứ gì bí ẩn.", 
                            font_size=24, color=WHITE).shift(UP*1.2)
        
        closing_line2 = Text("Chúng là sự tổng quát hóa tự nhiên của", 
                            font_size=20, color=GRAY_B).shift(UP*0.5)
        
        closing_keywords = VGroup(
            Text("tổng Riemann", font_size=22, color=GREEN_SCREEN, weight=BOLD),
            Text("tích phân", font_size=22, color=GREEN_SCREEN, weight=BOLD),
            Text("MLP", font_size=22, color=GREEN_SCREEN, weight=BOLD)
        ).arrange(RIGHT, buff=0.8).shift(DOWN*0.2)
        
        closing_line3 = Text("lên không gian vô hạn chiều.", 
                            font_size=20, color=GRAY_B).shift(DOWN*0.9)

        self.play_timed("b2_closing", 16.5, 21,
                        Write(closing_line1),
                        FadeIn(closing_line2),
                        LaggedStart(*[FadeIn(k, shift=UP*0.2) for k in closing_keywords], lag_ratio=0.2),
                        FadeIn(closing_line3))

        # Call to action
        cta_box = RoundedRectangle(width=4.0, height=0.8, corner_radius=0.15,
                                   stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.15, stroke_width=2.5)
        cta_txt = Text("Subscribe để không bỏ lỡ video tiếp theo", 
                      font_size=16, color=YELLOW, weight=BOLD).move_to(cta_box)
        cta_group = VGroup(cta_box, cta_txt).shift(DOWN*2.2)

        self.play_timed("b2_cta", 21, 23.5,
                        FadeIn(cta_group),
                        cta_group.animate.scale(1.05),
                        rate_func=there_and_back)

        # Thank you
        thank_you = Text("Cảm ơn bạn đã xem đến cuối. Hẹn gặp lại!", 
                        font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        
        self.play_timed("b2_thanks", 23.5, 25, FadeIn(thank_you))

        self.wait_timed("b2_hold", 25, 28)

        # Fade to black
        self.play_timed("fade_out", 28, 30,
                        *[FadeOut(m, run_time=1.5) for m in self.mobjects])
        
        self.pad_to(self.SCENE_DURATION)
