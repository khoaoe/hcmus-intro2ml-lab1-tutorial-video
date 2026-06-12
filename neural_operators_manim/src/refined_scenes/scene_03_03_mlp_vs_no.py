
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
        
        title = Text("Sự dịch chuyển sang Không gian Hàm", font_size=32, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("title", 0, 2, FadeIn(title))
        
        vector_dots = VGroup(*[
            Dot(LEFT*2.5 + UP*(i*0.48 - 0.16), color=INPUT, radius=0.1) 
            for i in range(5)
        ])
        axes_f = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=3.0, y_length=1.8, 
                      axis_config={"color": GREY_B, "include_ticks": False}).shift(RIGHT*2.5 + UP*0.8)
        func_curve = axes_f.plot(lambda x: np.sin(x*2)*0.8, color=INPUT, stroke_width=3.6)
        
        matrix_grid = VGroup()
        for i in range(4):
            for j in range(4):
                sq = Square(side_length=0.3, stroke_width=1.2, stroke_color=PURPLE, 
                            fill_color=PURPLE, fill_opacity=np.random.rand()*0.8)
                sq.move_to(LEFT*2.5 + RIGHT*(j*0.3 - 0.45) + DOWN*(i*0.3 - 0.45) + DOWN*1.0)
                matrix_grid.add(sq)
                
        kernel_box = Rectangle(width=1.8, height=1.8, stroke_width=0).shift(RIGHT*2.5 + DOWN*1.0)
        kernel_heatmap = VGroup()
        for i in range(18):
            color_val = interpolate_color(BLUE_D, RED_D, i/17)
            line = Line(
                kernel_box.get_corner(DOWN + LEFT) + RIGHT*(i*0.1 + 0.05),
                kernel_box.get_corner(UP + LEFT) + RIGHT*(i*0.1 + 0.05),
                stroke_width=12, stroke_color=color_val, stroke_opacity=0.8
            )
            kernel_heatmap.add(line)
            
        sum_sym = MathTex(r"\sum_{i=1}^{n}", font_size=58, color=WHITE).shift(LEFT*2.5 + DOWN*3.0)
        int_sym = MathTex(r"\int_{\Omega}", font_size=58, color=WHITE).shift(RIGHT*2.5 + DOWN*3.0)
        
        lbl_mlp = Text("Hữu hạn chiều (MLP)", font_size=22, color=MUTED).shift(LEFT*2.5 + UP*2.6)
        lbl_no = Text("Vô hạn chiều (NO)", font_size=22, color=NVIDIA_GREEN).shift(RIGHT*2.5 + UP*2.6)
        
        self.play_timed("show_discrete", 2, 5, 
                        FadeIn(lbl_mlp), FadeIn(lbl_no),
                        FadeIn(vector_dots), FadeIn(matrix_grid), Write(sum_sym))
        
        self.play_timed("morph_to_cont", 5, 12,
                        TransformFromCopy(vector_dots, func_curve),
                        TransformFromCopy(matrix_grid, kernel_heatmap),
                        TransformFromCopy(sum_sym, int_sym))
                        
        self.wait_timed("hold_dict", 12, 25)
        
        no_box = SurroundingRectangle(
            VGroup(func_curve, kernel_heatmap, int_sym), 
            color=NVIDIA_GREEN, buff=0.3, corner_radius=0.2
        )
        self.play_timed("highlight_no", 25, 30, Create(no_box))

        
        self.play_timed("clear_beat1", 30, 31, *[FadeOut(m) for m in self.mobjects])
        
        axes_p = Axes(
            x_range=[0, 6.2, 1], y_range=[-1.5, 2.5, 1],
            x_length=10, y_length=4,
            axis_config={"color": GREY_B, "include_ticks": False}
        ).shift(DOWN * 0.5)
        
        def sharp_func(x):
            return np.sin(x * 4) * np.exp(-0.2 * (x - 3)**2) + 1.5 * np.exp(-10 * (x - 4.5)**2)
            
        sharp_curve = axes_p.plot(sharp_func, x_range=[0, 6.0], color=WARNING, stroke_width=3)
        sharp_label = Text("Input: Chi tiết sắc nét (Shock waves)", font_size=18, color=WARNING).next_to(axes_p, UP, buff=0.2).to_edge(LEFT, buff=0.5)
        
        self.play_timed("sharp_in", 31, 34, Create(axes_p), Create(sharp_curve), FadeIn(sharp_label))
        
        def smooth_func(x):
            return np.sin(x * 1.5) * np.exp(-0.2 * (x - 3)**2) + 0.5 * np.exp(-2 * (x - 4.5)**2)
            
        smooth_curve = axes_p.plot(smooth_func, x_range=[0, 6.0], color=INPUT, stroke_width=3, stroke_opacity=0.8)
        
        kernel_lens = Circle(radius=0.6, color=OPERATOR, fill_opacity=0.2, stroke_width=2).shift(LEFT*3 + DOWN*0.5)
        lens_glow = Circle(radius=0.8, color=OPERATOR, fill_opacity=0.1, stroke_width=0).move_to(kernel_lens)
        lens_group = VGroup(kernel_lens, lens_glow)
        
        lens_path = Line(LEFT*3 + DOWN*0.5, RIGHT*3 + DOWN*0.5)
        
        self.play_timed("lens_appear", 34, 35, FadeIn(lens_group))
        
        self.play_timed("lens_sweep_and_smooth", 35, 40,
            MoveAlongPath(lens_group, lens_path, rate_func=linear),
            Transform(sharp_curve, smooth_curve, rate_func=squish_rate_func(smooth, 0.6, 0.9))
        )
        
        blur_note = Text("Tích phân = Bộ lọc thông thấp\n-> Mất chi tiết!", font_size=18, color=OPERATOR).next_to(axes_p, UP, buff=0.2).to_edge(RIGHT, buff=0.5)
        self.play_timed("blur_note", 40, 43, FadeIn(blur_note))
        
        residual_line = ArcBetweenPoints(
            axes_p.c2p(0.0, 0.0),
            axes_p.c2p(6.0, 0.0),
            angle=PI/2.5,
            stroke_color=NVIDIA_GREEN,
            stroke_width=5
        )
        
        res_label = Text("Residual Connection (Bypass)", font_size=20, color=NVIDIA_GREEN, weight=BOLD).next_to(residual_line, DOWN, buff=0.2)
        
        self.play_timed("residual_bypass", 43, 45,
            Create(residual_line), 
            FadeIn(res_label),
            ShowPassingFlash(residual_line.copy(), time_width=0.5)
        )
        self.wait_timed("residual_hold", 45, 48)
        
        def final_func(x):
            return smooth_func(x) + (sharp_func(x) - smooth_func(x))
            
        final_curve = axes_p.plot(final_func, x_range=[0, 6.0], color=NVIDIA_GREEN, stroke_width=4)
        final_label = Text("Output: Giữ nguyên vật lý!", font_size=20, color=NVIDIA_GREEN)
        final_label.set_y(res_label.get_y())
        final_label.to_edge(RIGHT, buff=0.5)
        
        self.play_timed("restoration", 48, 53,
            FadeOut(blur_note), FadeOut(lens_group),
            Transform(sharp_curve, final_curve), 
            FadeIn(final_label),
            Flash(axes_p.c2p(4.5, final_func(4.5)), color=NVIDIA_GREEN, line_length=0.4, flash_radius=0.6)
        )
                        
        self.wait_timed("hold_end", 53, 59)
        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
