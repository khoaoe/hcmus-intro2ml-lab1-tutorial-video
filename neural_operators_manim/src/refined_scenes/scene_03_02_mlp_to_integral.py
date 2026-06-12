
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0302_MLPToIntegralOperator(TimedScene):
    SCRIPT_ID = "3.2"
    SCRIPT_TITLE = "MLP → Toán tử Tích phân"
    SCRIPT_START = 495.0
    SCRIPT_END = 555.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        
        mlp_eq = MathTex(
            r"y_j", r"=", r"\sigma", r"\left(", r"\sum_i",
            r"W_{ji}", r"x_i", r"+", r"b_j", r"\right)",
            font_size=38
        ).to_edge(UP, buff=0.6)
        mlp_eq[0].set_color(OUTPUT)    # y_j
        mlp_eq[5].set_color(OPERATOR)  # W_ji
        mlp_eq[6].set_color(INPUT)     # x_i
        
        self.play_timed("mlp_eq", 0, 3, Write(mlp_eq))
        
        x_nodes = VGroup(*[Dot(LEFT*4 + UP*(i*0.6 - 0.9), color=INPUT, radius=0.08) for i in range(4)])
        y_nodes = VGroup(*[Dot(RIGHT*4 + UP*(i*0.6 - 0.9), color=OUTPUT, radius=0.08) for i in range(4)])
        
        w_lines = VGroup()
        for x in x_nodes:
            for y in y_nodes:
                line = Line(x.get_right(), y.get_left(), stroke_width=1.5, stroke_color=OPERATOR, stroke_opacity=0.4)
                w_lines.add(line)
        discrete_graph = VGroup(x_nodes, y_nodes, w_lines).shift(UP * 0.5)
        
        self.play_timed("discrete_graph", 3, 6, FadeIn(discrete_graph))
        self.wait_timed("hold_discrete", 6, 10)
        
        axes_in = Axes(
            x_range=[0, 3.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=3.5, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1, "include_ticks": False, "tip_width": 0.15, "tip_height": 0.15}
        ).shift(LEFT * 4 + UP * 0.5)
        
        func_a = axes_in.plot(lambda x: np.sin(x) * 0.8, x_range=[0, 3], color=INPUT, stroke_width=3)
        label_a = MathTex("a(x)", font_size=24, color=INPUT).next_to(axes_in, UP, buff=0.1)
        
        kernel_box = Rectangle(width=2.5, height=2.5, stroke_width=0).shift(UP * 0.5)
        kernel_heatmap = VGroup()
        for i in range(25):
            color_val = interpolate_color(BLUE_D, RED_D, i/24)
            line = Line(
                kernel_box.get_corner(DOWN + LEFT) + RIGHT*(i*0.1), 
                kernel_box.get_corner(UP + LEFT) + RIGHT*(i*0.1),
                stroke_width=12, stroke_color=color_val, stroke_opacity=0.8
            )
            kernel_heatmap.add(line)
            
        label_k = MathTex(r"\kappa(y,x;\theta)", font_size=24, color=OPERATOR).next_to(kernel_box, UP, buff=0.1)
        
        axes_out = Axes(
            x_range=[0, 3.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=3.5, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1, "include_ticks": False, "tip_width": 0.15, "tip_height": 0.15}
        ).shift(RIGHT * 4 + UP * 0.5)
        
        func_v = axes_out.plot(lambda x: np.cos(x) * 0.6, x_range=[0, 3], color=OUTPUT, stroke_width=3)
        label_v = MathTex("v(y)", font_size=24, color=OUTPUT).next_to(axes_out, UP, buff=0.1)
        
        integral_eq = MathTex(
            r"v(y)", r"=", r"\sigma", r"\left(", r"\int",
            r"\kappa(y,x;\theta)", r"a(x)", r"\,dx",
            r"+", r"b(y)", r"\right)",
            font_size=38
        ).to_edge(UP, buff=0.6)
        integral_eq[0].set_color(OUTPUT)
        integral_eq[5].set_color(OPERATOR)
        integral_eq[6].set_color(INPUT)
        
        self.play_timed("melting", 10, 16,
            Transform(x_nodes, axes_in), FadeIn(func_a), FadeIn(label_a),
            Transform(y_nodes, axes_out), FadeIn(func_v), FadeIn(label_v),
            Transform(w_lines, kernel_box), FadeIn(kernel_heatmap), FadeIn(label_k),
            Transform(mlp_eq, integral_eq)
        )
        
        self.wait_timed("hold_continuous", 16, 25)

        
        scanner = Rectangle(width=0.2, height=2.5, color=YELLOW, fill_opacity=0.3, stroke_width=2)
        scanner.move_to(axes_in.get_left())
        
        connect_arrow = Arrow(
            kernel_box.get_right(), axes_out.get_left() + LEFT*0.2,
            color=YELLOW, stroke_width=3, buff=0.1
        )
        
        self.play_timed("scanner_appear", 25, 27, FadeIn(scanner), GrowArrow(connect_arrow))
        
        self.play_timed("scan_and_draw", 27, 33,
            scanner.animate.move_to(axes_in.get_right()),
            Create(func_v), # Vẽ lại hàm v(y) để tạo cảm giác nó đang được "sinh ra"
            rate_func=linear
        )
        
        ripple_center = kernel_box.get_center()
        ripples = VGroup(*[
            Circle(radius=r, color=WHITE, stroke_width=1.5, stroke_opacity=0.8 - r*0.15)
            for r in np.linspace(0.2, 1.2, 5)
        ]).move_to(ripple_center)
        
        physics_text = Text("Hàm Green / Đáp ứng xung", font_size=20, color=WHITE)
        physics_text.next_to(kernel_box, DOWN, buff=0.2)
        
        self.play_timed("physics_flash", 33, 36,
            FadeIn(ripples, scale=0.5),
            FadeIn(physics_text)
        )
        self.play_timed("ripple_expand", 36, 38,
            ripples.animate.scale(1.5).set_stroke(opacity=0),
            FadeOut(ripples)
        )
        
        self.play_timed("clear_clutter", 38, 40,
            FadeOut(scanner), FadeOut(connect_arrow), FadeOut(physics_text)
        )
        
        punchline = VGroup(
            Text("Trong Vật lý: Kernel được", font_size=24, color=MUTED),
            Text("THIẾT KẾ BẰNG TAY", font_size=28, color=WARNING, weight=BOLD),
            Text("Trong Neural Operator: Kernel được", font_size=24, color=MUTED),
            Text("HỌC TỪ DỮ LIỆU", font_size=28, color=NVIDIA_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        
        self.play_timed("punchline", 40, 45,
            LaggedStart(*[FadeIn(line, shift=UP*0.2) for line in punchline], lag_ratio=0.2)
        )
        
        self.wait_timed("hold_end", 45, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
