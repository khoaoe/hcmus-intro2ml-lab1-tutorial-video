"""
Scene 3.4 — Deep Neural Operator & Bẫy Rời rạc hóa (The Smoothness Trap)
Source: Reformulated original_outline.tex, Section 3, Scene 3.4
Global time: 10:15 – 11:15
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0304_DeepNOErrorAnalysis(TimedScene):
    SCRIPT_ID = "3.4"
    SCRIPT_TITLE = "Deep Neural Operator & Bẫy Rời rạc hóa"
    SCRIPT_START = 615.0
    SCRIPT_END = 675.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: [10:15–10:45] The Lift-Operate-Project Ribbon
        # ═══════════════════════════════════════════════════════════════
        
        # Dùng một Axes ẩn để generate các đường cong có cùng số lượng điểm, 
        # giúp Transform mượt mà không bị xoắn (twisting)
        dummy_axes = Axes(x_range=[0, 6], y_range=[-3, 3], x_length=6, y_length=4)
        
        # 1. Input Function (Single thick line)
        in_func = dummy_axes.plot(lambda x: np.sin(x)*0.8, color=INPUT, stroke_width=5)
        in_label = Text("Hàm vật lý", font_size=20, color=INPUT).next_to(in_func, LEFT, buff=0.3)
        
        # 2. Latent Stack (5 lines, fanned out - High dimensional feature space)
        latent_stack = VGroup()
        for i in range(5):
            line = dummy_axes.plot(lambda x, i=i: np.sin(x + i*0.5)*0.4 + i*0.4 - 0.8, color=NVIDIA_GREEN, stroke_width=2.5)
            latent_stack.add(line)
            
        # 3. Operated Stack (5 lines, different shape - after integral mixing)
        operated_stack = VGroup()
        for i in range(5):
            line = dummy_axes.plot(lambda x, i=i: np.cos(x*1.2 + i*0.4)*0.4 + i*0.4 - 0.8, color=NVIDIA_GREEN, stroke_width=2.5)
            operated_stack.add(line)
            
        # 4. Output Function (Single thick line)
        out_func = dummy_axes.plot(lambda x: np.cos(x*1.5)*0.8 + 1.5, color=OUTPUT, stroke_width=5)
        out_label = Text("Hàm dự báo", font_size=20, color=OUTPUT).next_to(out_func, RIGHT, buff=0.3)
        
        # Kernel Lens (Vertical glowing slit)
        lens = Rectangle(width=0.3, height=4, color=OPERATOR, fill_opacity=0.4, stroke_width=2).set_glow_factor(0.8)
        
        # Labels for stages
        enc_lbl = Text("Encoder\n(Pointwise)", font_size=18, color=INPUT).shift(LEFT * 4.5 + UP * 2.5)
        op_lbl = Text("Integral\nOperator Layers", font_size=18, color=OPERATOR).shift(UP * 2.5)
        dec_lbl = Text("Decoder\n(Pointwise)", font_size=18, color=OUTPUT).shift(RIGHT * 4.5 + UP * 2.5)

        # Animate Beat 1
        self.play_timed("in_func", 0, 3, Create(in_func), FadeIn(in_label))
        
        # LIFT
        self.play_timed("lift", 3, 8, 
                        Transform(in_func, latent_stack), 
                        FadeIn(enc_lbl))
        
        # OPERATE (Lens sweeps across)
        lens.move_to(LEFT * 3)
        self.play_timed("operate_start", 8, 10, FadeIn(lens), FadeIn(op_lbl))
        self.play_timed("operate_sweep", 10, 15, 
                        lens.animate.move_to(RIGHT * 3),
                        Transform(in_func, operated_stack)) # in_func is now latent_stack
        self.play_timed("operate_end", 15, 16, FadeOut(lens))
        
        # PROJECT
        self.play_timed("project", 16, 20, 
                        Transform(in_func, out_func), # in_func is now operated_stack
                        FadeIn(dec_lbl), FadeIn(out_label))
                        
        # Equation & Invariance Check
        layer_eq = MathTex(
            r"v^{(\ell+1)} = \sigma\left(\int \kappa^\ell(y,x;\theta) \cdot v^\ell(x)\,dx + b^\ell(y)\right)",
            font_size=28, color=TEXT
        ).to_edge(DOWN, buff=0.8)
        
        checks = VGroup(
            Text("✓ Input: mọi discretization", font_size=18, color=NVIDIA_GREEN),
            Text("✓ Output: query mọi điểm", font_size=18, color=NVIDIA_GREEN),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(layer_eq, UP, buff=0.4).align_to(layer_eq, LEFT)

        self.play_timed("eq_checks", 20, 25, Write(layer_eq), FadeIn(checks))
        self.wait_timed("hold_pipeline", 25, 30)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [10:45–11:15] The Smoothness Trap (Discretization Error)
        # ═══════════════════════════════════════════════════════════════
        
        self.play_timed("clear_beat1", 30, 30.5, *[FadeOut(m) for m in self.mobjects])
        
        error_title = Text("Bẫy Rời rạc hóa (Discretization Error)", font_size=28,
                           color=TEXT, weight=BOLD).to_edge(UP, buff=0.4)
                           
        # Top Axes: Smooth Function (High Sobolev smoothness s)
        axes_smooth = Axes(x_range=[0, 4], y_range=[0, 2.5], x_length=5, y_length=1.5, 
                           axis_config={"include_ticks": False, "stroke_color": GREY_B}).shift(UP*1.5 + LEFT*2)
        smooth_func = axes_smooth.plot(lambda x: np.sin(x)*0.6 + 1.2, color=NVIDIA_GREEN, stroke_width=3)
        lbl_smooth = Text("Hàm trơn (s lớn)", font_size=18, color=NVIDIA_GREEN).next_to(axes_smooth, LEFT, buff=0.2)
        
        # Bottom Axes: Shock Function (Low s, discontinuity)
        axes_shock = Axes(x_range=[0, 4], y_range=[0, 2.5], x_length=5, y_length=1.5, 
                          axis_config={"include_ticks": False, "stroke_color": GREY_B}).shift(DOWN*1.5 + LEFT*2)
        # Dùng Sigmoid dốc để giả lập Shock wave, tránh lỗi NaN của Manim khi tính Riemann
        shock_func = axes_shock.plot(lambda x: 1.2 / (1 + np.exp(-15*(x-2))) + 0.4, color=WARNING, stroke_width=3)
        lbl_shock = Text("Hàm Shock (s nhỏ)", font_size=18, color=WARNING).next_to(axes_shock, LEFT, buff=0.2)
        
        self.play_timed("setup_beat2", 30.5, 33, 
                        FadeIn(error_title), 
                        Create(axes_smooth), Create(smooth_func), FadeIn(lbl_smooth),
                        Create(axes_shock), Create(shock_func), FadeIn(lbl_shock))
                        
        # Riemann Rectangles: Coarse (N=4)
        rects_smooth_coarse = axes_smooth.get_riemann_rectangles(smooth_func, dx=1.0, color=INPUT, fill_opacity=0.4, stroke_width=1.5)
        rects_shock_coarse = axes_shock.get_riemann_rectangles(shock_func, dx=1.0, color=WARNING, fill_opacity=0.4, stroke_width=1.5)
        
        self.play_timed("coarse_rects", 33, 37, 
                        FadeIn(rects_smooth_coarse), FadeIn(rects_shock_coarse))
                        
        # Riemann Rectangles: Fine (N=16)
        rects_smooth_fine = axes_smooth.get_riemann_rectangles(smooth_func, dx=0.25, color=INPUT, fill_opacity=0.5, stroke_width=0.5)
        rects_shock_fine = axes_shock.get_riemann_rectangles(shock_func, dx=0.25, color=WARNING, fill_opacity=0.5, stroke_width=0.5)
        
        self.play_timed("fine_rects", 37, 42, 
                        Transform(rects_smooth_coarse, rects_smooth_fine),
                        Transform(rects_shock_coarse, rects_shock_fine))
                        
        # Highlight the Error Triangle at the Shock
        # Vẽ một hình tam giác đỏ nhỏ ở điểm gãy để nhấn mạnh sai số không biến mất
        error_triangle = Polygon(
            axes_shock.c2p(1.8, 0.6), axes_shock.c2p(2.2, 0.6), axes_shock.c2p(2.2, 1.5),
            color=RED, fill_opacity=0.6, stroke_width=2
        )
        error_text = Text("Sai số dai dẳng!", font_size=16, color=RED, weight=BOLD).next_to(error_triangle, RIGHT, buff=0.2)
        
        self.play_timed("highlight_error", 42, 46, 
                        FadeIn(error_triangle), FadeIn(error_text),
                        Flash(error_triangle.get_center(), color=RED, line_length=0.2))
                        
        # Formula & Sobolev Note
        error_formula = MathTex(
            r"\varepsilon_{disc} \propto N^{-s}",
            font_size=36, color=PURPLE
        ).shift(RIGHT * 4.5 + UP * 0.5)
        
        sobolev_note = VGroup(
            Text("s = độ trơn Sobolev", font_size=18, color=MUTED),
            Text("Hàm trơn $\to$ Hội tụ nhanh", font_size=16, color=NVIDIA_GREEN),
            Text("Shock / Gián đoạn $\to$ Hội tụ chậm", font_size=16, color=WARNING),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(error_formula, DOWN, buff=0.4)

        self.play_timed("formula", 46, 52, Write(error_formula), FadeIn(sobolev_note))
        self.wait_timed("hold_end", 52, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
