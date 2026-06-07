"""
Scene 3.3 — Visual Dictionary & The Smoothing Paradox
Source: original_outline.tex, Section 3, Scene 3.3
Global time: 9:15 – 10:15
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0303_MLPvsNOComponents(TimedScene):
    SCRIPT_ID = "3.3"
    SCRIPT_TITLE = "Từ điển Hình học & Nghịch lý Làm mịn"
    SCRIPT_START = 555.0
    SCRIPT_END = 615.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: [9:15–9:45] The Visual Dictionary (Morphing)
        # ═══════════════════════════════════════════════════════════════
        
        title = Text("Sự dịch chuyển sang Không gian Hàm", font_size=32, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("title", 0, 2, FadeIn(title))
        
        # 1. Vector -> Function
        # Vector: Cột các chấm rời rạc
        vector_dots = VGroup(*[Dot(LEFT*5 + UP*(i*0.4 - 0.8), color=INPUT, radius=0.08) for i in range(5)])
        # Function: Đường cong mượt
        axes_f = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=2.5, y_length=1.5, axis_config={"color": GREY_B, "include_ticks": False}).shift(LEFT*2.5)
        func_curve = axes_f.plot(lambda x: np.sin(x*2)*0.8, color=INPUT, stroke_width=3)
        
        # 2. Matrix -> Kernel Heatmap
        # Matrix: Lưới ô vuông nhỏ
        matrix_grid = VGroup()
        for i in range(4):
            for j in range(4):
                sq = Square(side_length=0.25, stroke_width=1, stroke_color=OPERATOR, fill_color=OPERATOR, fill_opacity=np.random.rand()*0.8)
                sq.move_to(LEFT*5 + RIGHT*(j*0.25 - 0.375) + DOWN*(i*0.25 - 0.375) + DOWN*1.5)
                matrix_grid.add(sq)
        # Kernel: Heatmap 2D (dùng các đường line gradient giả lập cho nhẹ render)
        kernel_box = Rectangle(width=1.5, height=1.5, stroke_width=0).shift(LEFT*2.5 + DOWN*1.5)
        kernel_heatmap = VGroup()
        for i in range(15):
            color_val = interpolate_color(BLUE_D, RED_D, i/14)
            line = Line(kernel_box.get_left() + RIGHT*(i*0.1), kernel_box.get_left() + RIGHT*(i*0.1) + UP*1.5, stroke_width=12, stroke_color=color_val, stroke_opacity=0.8)
            kernel_heatmap.add(line)
            
        # 3. Sum -> Integral
        sum_sym = MathTex(r"\sum_{i=1}^{n}", font_size=48, color=TEXT).shift(LEFT*5 + DOWN*3.2)
        int_sym = MathTex(r"\int_{\Omega}", font_size=48, color=TEXT).shift(LEFT*2.5 + DOWN*3.2)
        
        # Labels
        lbl_mlp = Text("Hữu hạn chiều (MLP)", font_size=18, color=MUTED).shift(LEFT*5 + UP*1.5)
        lbl_no = Text("Vô hạn chiều (NO)", font_size=18, color=NVIDIA_GREEN).shift(LEFT*2.5 + UP*1.5)
        
        self.play_timed("show_discrete", 2, 5, 
                        FadeIn(lbl_mlp), FadeIn(lbl_no),
                        FadeIn(vector_dots), FadeIn(matrix_grid), Write(sum_sym))
        
        # The Morphing
        self.play_timed("morph_to_cont", 5, 12,
                        Transform(vector_dots, func_curve),
                        Transform(matrix_grid, kernel_heatmap),
                        Transform(sum_sym, int_sym))
                        
        self.wait_timed("hold_dict", 12, 25)
        
        # Arrows showing the mapping
        map_arrows = VGroup(
            Arrow(vector_dots.get_right(), func_curve.get_left(), color=YELLOW, buff=0.2, stroke_width=2),
            Arrow(matrix_grid.get_right(), kernel_heatmap.get_left(), color=YELLOW, buff=0.2, stroke_width=2),
            Arrow(sum_sym.get_right(), int_sym.get_left(), color=YELLOW, buff=0.2, stroke_width=2),
        )
        # Wait, they are already side-by-side, let's just use a big bracket or glowing line
        # Actually, the Transform already shows it. Let's add a glowing box around the NO side.
        no_box = SurroundingRectangle(VGroup(func_curve, kernel_heatmap, int_sym), color=NVIDIA_GREEN, buff=0.3, corner_radius=0.2)
        self.play_timed("highlight_no", 25, 30, Create(no_box))

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [9:45–10:15] The Smoothing Paradox & Residual
        # ═══════════════════════════════════════════════════════════════
        
        self.play_timed("clear_beat1", 30, 31, *[FadeOut(m) for m in self.mobjects])
        
        # Setup axes for the paradox
        axes_p = Axes(
            x_range=[0, 6, 1], y_range=[-1.5, 2.5, 1],
            x_length=10, y_length=4,
            axis_config={"color": GREY_B, "include_ticks": False}
        ).shift(DOWN * 0.5)
        
        # 1. The Sharp Input (Shock wave / High frequency)
        def sharp_func(x):
            # Tạo một hàm có gai nhọn và bước nhảy
            return np.sin(x * 4) * np.exp(-0.2 * (x - 3)**2) + 1.5 * np.exp(-10 * (x - 4.5)**2)
            
        sharp_curve = axes_p.plot(sharp_func, color=INPUT, stroke_width=3)
        sharp_label = Text("Input: Chi tiết sắc nét (Shock waves)", font_size=20, color=INPUT).next_to(axes_p, UP, buff=0.2).align_to(axes_p, LEFT)
        
        self.play_timed("sharp_in", 31, 34, Create(axes_p), Create(sharp_curve), FadeIn(sharp_label))
        
        # 2. The Integral Operator (Low-pass filter -> Smoothing)
        # Hàm bị làm mịn (mất gai nhọn)
        def smooth_func(x):
            return np.sin(x * 1.5) * np.exp(-0.2 * (x - 3)**2) + 0.5 * np.exp(-2 * (x - 4.5)**2)
            
        smooth_curve = axes_p.plot(smooth_func, color=WARNING, stroke_width=3, stroke_opacity=0.8)
        
        op_box = RoundedRectangle(width=1.5, height=1, corner_radius=0.1, color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.8).shift(UP * 2.5)
        op_text = Text("Lõi Tích phân", font_size=16, color=OPERATOR).move_to(op_box)
        op_group = VGroup(op_box, op_text)
        
        # Mũi tên đi qua Operator
        arr_to_op = Arrow(sharp_curve.get_top() + UP*0.2, op_box.get_left(), color=MUTED, stroke_width=2)
        arr_from_op = Arrow(op_box.get_right(), smooth_curve.get_top() + UP*0.2, color=WARNING, stroke_width=2)
        
        self.play_timed("integral_smooth", 34, 40,
                        FadeIn(op_group), GrowArrow(arr_to_op), GrowArrow(arr_from_op),
                        Create(smooth_curve))
                        
        blur_note = Text("Tích phân = Bộ lọc thông thấp $\to$ Mất chi tiết!", font_size=20, color=WARNING).shift(RIGHT * 3 + UP * 2.5)
        self.play_timed("blur_note", 40, 43, FadeIn(blur_note))
        
        # 3. The Residual Lifeline (Bypass)
        # Mũi tên Residual nối thẳng từ Input sang Output
        residual_path = CubicBezier(
            sharp_curve.get_left() + LEFT*0.2, 
            sharp_curve.get_left() + LEFT*1.5 + DOWN*1, 
            smooth_curve.get_right() + RIGHT*1.5 + DOWN*1, 
            smooth_curve.get_right() + RIGHT*0.2
        )
        residual_arrow = Arrow(
            sharp_curve.get_left(), smooth_curve.get_right(), 
            color=NVIDIA_GREEN, stroke_width=4, buff=0.1
        )
        # Dùng đường cong cho đẹp
        residual_line = VMobject(stroke_color=NVIDIA_GREEN, stroke_width=4)
        residual_line.set_points_smoothly([
            sharp_curve.get_left() + LEFT*0.2,
            sharp_curve.get_left() + LEFT*1.0 + DOWN*1.5,
            smooth_curve.get_right() + RIGHT*1.0 + DOWN*1.5,
            smooth_curve.get_right() + RIGHT*0.2
        ])
        
        res_label = Text("Residual Connection (Bypass)", font_size=20, color=NVIDIA_GREEN, weight=BOLD).next_to(residual_line, DOWN, buff=0.2)
        
        self.play_timed("residual_bypass", 43, 48,
                        Create(residual_line), FadeIn(res_label))
        
        # 4. The Restoration (Output = Smooth + Sharp)
        # Hàm cuối cùng phục hồi lại độ sắc nét
        final_curve = axes_p.plot(lambda x: smooth_func(x) + (sharp_func(x) - smooth_func(x))*0.9, color=NVIDIA_GREEN, stroke_width=4)
        final_label = Text("Output: Giữ nguyên vật lý!", font_size=20, color=NVIDIA_GREEN).next_to(axes_p, DOWN, buff=0.3).align_to(axes_p, RIGHT)
        
        self.play_timed("restoration", 48, 53,
                        FadeOut(smooth_curve), FadeOut(blur_note),
                        Create(final_curve), FadeIn(final_label),
                        Flash(final_curve.get_center(), color=NVIDIA_GREEN, line_length=0.3))
                        
        self.wait_timed("hold_end", 53, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
