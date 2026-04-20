import sys
import os
import random
import numpy as np
from manim import *

# Cấu hình sys.path để import từ thư mục gốc
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.colors import *


class Scene1_1_Hook(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: [0:00–0:12] (Target duration: 12.0s)
        # ---------------------------------------------------------
        # "Trong hàng chục năm qua, Deep Learning đã tạo ra những đột phá..."
        grid = VGroup(*[
            Square(side_length=0.2, stroke_width=0.5, stroke_color=DISCRETE_GRID)
            for _ in range(256) # 16x16 grid
        ]).arrange_in_grid(16, 16, buff=0)
        
        self.play(FadeIn(grid), run_time=2.0)
        
        # Pixel fill animation (simulate an image)
        animations = []
        for sq in grid:
            if random.random() > 0.5:
                animations.append(sq.animate.set_fill(DISCRETE_BLUE, opacity=random.uniform(0.3, 0.9)))
            else:
                animations.append(sq.animate.set_fill(WHITE, opacity=random.uniform(0.1, 0.4)))
        
        self.play(LaggedStart(*animations, lag_ratio=0.01), run_time=6.0)
        self.wait(4.0) # 2.0 + 6.0 + 4.0 = 12.0s

        # ---------------------------------------------------------
        # Beat 2: [0:12–0:28] (Target duration: 16.0s)
        # ---------------------------------------------------------
        # "Chúng ta đã quá quen thuộc với việc CNN nhận diện hình ảnh..."
        
        # Morph grid to Flattened Vector x
        vector_x = Matrix([["x_1"], ["x_2"], ["\\vdots"], ["x_n"]]).scale(0.8)
        vector_x.shift(RIGHT * 3)
        
        # Transform grid to a compact box, then to vector
        grid_box = SurroundingRectangle(grid, color=DISCRETE_BLUE, fill_opacity=0.8)
        self.play(Transform(grid, grid_box), run_time=2.0)
        self.play(Transform(grid, vector_x), run_time=2.0)

        # Create Weight Matrix W and output y
        matrix_w = Matrix([
            ["w_{11}", "\\dots", "w_{1n}"],
            ["\\vdots", "\\ddots", "\\vdots"],
            ["w_{m1}", "\\dots", "w_{mn}"]
        ]).scale(0.8)
        matrix_w.set_color(MATRIX_WEIGHT)
        matrix_w.next_to(grid, LEFT, buff=0.5)
        
        eq_sign = MathTex("=").next_to(grid, RIGHT, buff=0.5)
        vector_y = Matrix([["y_1"], ["\\vdots"], ["y_m"]]).scale(0.8).next_to(eq_sign, RIGHT, buff=0.5)

        self.play(
            Write(matrix_w), 
            Write(eq_sign), 
            Write(vector_y), 
            run_time=4.0
        )
        self.wait(8.0) # 2.0 + 2.0 + 4.0 + 8.0 = 16.0s

        # ---------------------------------------------------------
        # Beat 3: [0:28–0:45] (Target duration: 17.0s)
        # ---------------------------------------------------------
        # "Nhưng nếu lùi lại một bước để quan sát, tất cả các mô hình này..."
        
        self.play(
            FadeOut(matrix_w), 
            FadeOut(eq_sign), 
            FadeOut(vector_y),
            run_time=2.0
        )
        
        # Vector becomes a discrete point in R^n
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY}
        )
        
        dot = Dot(axes.c2p(1.5, 2), color=DISCRETE_BLUE)
        self.play(
            Create(axes),
            Transform(grid, dot),
            run_time=3.0
        )
        
        # Multiple discrete points representing finite-dimensional data
        dots = VGroup(*[Dot(axes.c2p(random.uniform(-2.5, 2.5), random.uniform(-2.5, 2.5)), color=DISCRETE_BLUE) for _ in range(15)])
        self.play(FadeIn(dots, shift=UP), run_time=2.0)
        
        # Title Overlay
        rn_text = Tex(r"\textbf{Finite-dimensional Euclidean Space } $\mathbb{R}^n$").scale(1.2)
        rn_text.to_edge(UP)
        rn_text[0][:18].set_color(TEXT_HIGHLIGHT) # Highlight "Finite-dimensional"
        
        self.play(Write(rn_text), run_time=3.0)
        self.wait(7.0) # 2.0 + 3.0 + 2.0 + 3.0 + 7.0 = 17.0s


class Scene1_2_PlotTwist(ThreeDScene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: [0:45–1:00] (Target duration: 15.0s)
        # ---------------------------------------------------------
        # "Tuy nhiên, nếu chúng ta bước ra khỏi Khoa học Máy tính..."
        
        # Start with shattered R^n concept
        rn_text_old = Tex(r"\textbf{Finite-dimensional Euclidean Space } $\mathbb{R}^n$").scale(1.2).to_edge(UP)
        self.add(rn_text_old)
        
        # Shatter effect (FadeOut rapidly)
        self.play(FadeOut(rn_text_old, shift=DOWN, scale=0.5), run_time=1.5)
        
        # Setup 3D Camera and Sphere
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Represent Earth/Continuous domain
        sphere = Surface(
            lambda u, v: np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ]), v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[CONTINUOUS_PURPLE, BLUE_E], resolution=(32, 32)
        )
        
        self.play(Create(sphere), run_time=3.5)
        
        # Ambient rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10.0) # 1.5 + 3.5 + 10.0 = 15.0s

        # ---------------------------------------------------------
        # Beat 2: [1:00–1:25] (Target duration: 25.0s)
        # ---------------------------------------------------------
        # "Da liễu nghiên cứu mô da trên bề mặt liên tục. Địa vật lý phân tích hàm 3D..."
        
        # Stop 3D ambient rotation temporarily to show domains 
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2.0) # Move to 2D view
        
        self.play(FadeOut(sphere), run_time=1.0)
        
        # Create 4 math representations (Abstracts of Domains)
        # 1. Dermatology: 2D smooth gradient surface
        surf_2d = ParametricFunction(lambda t: np.array([t, np.sin(t), 0]), t_range=[-2, 2], color=RED)
        label_1 = Text("Da liễu: Hàm bề mặt").scale(0.5).next_to(surf_2d, UP)
        group_1 = VGroup(surf_2d, label_1).move_to(UL * 2)
        
        # 2. Geophysics: 3D Wave (Top View)
        wave_circles = VGroup(*[Circle(radius=r, color=BLUE, stroke_opacity=1-r/2) for r in np.arange(0.2, 2.0, 0.4)])
        label_2 = Text("Địa vật lý: Sóng 3D").scale(0.5).next_to(wave_circles, UP)
        group_2 = VGroup(wave_circles, label_2).move_to(UR * 2)
        
        # 3. CFD: Vector field
        func = lambda pos: np.array([-pos[1], pos[0], 0]) / 3
        vector_field = ArrowVectorField(func, x_range=[-1.5, 1.5], y_range=[-1.5, 1.5]).scale(0.5)
        label_3 = Text("CFD: Trường Vector").scale(0.5).next_to(vector_field, UP)
        group_3 = VGroup(vector_field, label_3).move_to(DL * 2)
        
        # 4. Climate: Global functions
        globe_icon = Circle(radius=1.0, color=GREEN_C, fill_opacity=0.3)
        eq_lines = VGroup(*[Line(LEFT, RIGHT).scale(0.8).shift(UP*y) for y in np.arange(-0.6, 0.7, 0.3)])
        globe_group = VGroup(globe_icon, eq_lines)
        label_4 = Text("Khí hậu: Hàm trên cầu").scale(0.5).next_to(globe_group, UP)
        group_4 = VGroup(globe_group, label_4).move_to(DR * 2)
        
        self.play(FadeIn(group_1, shift=UP), run_time=2.0)
        self.play(FadeIn(group_2, shift=DOWN), run_time=2.0)
        self.play(FadeIn(group_3, shift=RIGHT), run_time=2.0)
        self.play(FadeIn(group_4, shift=LEFT), run_time=2.0)
        
        # Emphasis on "Dữ liệu của họ là hàm số"
        center_text = Tex(r"\textbf{Data} = \textit{Functions} $\mathcal{U}$", color=TEXT_HIGHLIGHT).scale(1.5)
        self.play(Write(center_text), run_time=3.0)
        
        self.wait(11.0) # 2.0 + 1.0 + (4*2.0) + 3.0 + 11.0 = 25.0s

        # ---------------------------------------------------------
        # Beat 3: [1:25–1:45] (Target duration: 20.0s)
        # ---------------------------------------------------------
        # "Và đây là điểm then chốt: khi ta cố ép một mô hình..."
        
        self.play(
            FadeOut(group_1), FadeOut(group_2), FadeOut(group_3), FadeOut(group_4),
            center_text.animate.to_edge(UP),
            run_time=3.0
        )
        
        # Extreme zoom into a continuous smooth gradient
        # Represented by a large smooth interpolated color rectangle
        smooth_field = Rectangle(width=16, height=9)
        smooth_field.set_fill(color=[BLUE, PURPLE, RED], opacity=1.0) # Simulated continuous gradient
        smooth_field.set_stroke(width=0)
        
        self.play(FadeIn(smooth_field), run_time=3.0)
        
        # Camera zoom simulation via scaling
        self.play(smooth_field.animate.scale(5), run_time=5.0, rate_func=there_and_back_with_pause)
        
        # Text overlay: no grid lines
        overlay_text = Text("Bản chất liên tục (Không có Pixel)", font_size=48, color=WHITE)
        self.play(Write(overlay_text), run_time=3.0)
        
        self.wait(6.0) # 3.0 + 3.0 + 5.0 + 3.0 + 6.0 = 20.0s


class Scene1_3_GridMismatch(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: [1:45–2:00] (Target duration: 15.0s)
        # ---------------------------------------------------------
        # VO: "Sự khác biệt này tạo ra một khoảng cách công nghệ khổng lồ..."
        
        # Tạo lưới thô (64x64 đại diện)
        coarse_grid = NumberPlane(
            x_range=[-2, 2, 0.5], y_range=[-2, 2, 0.5],
            background_line_style={"stroke_color": COARSE_GRID, "stroke_width": 2, "stroke_opacity": 0.6}
        ).scale(0.8).shift(LEFT * 3)
        coarse_label = Text("Lưới 64x64", font_size=24, color=COARSE_GRID).next_to(coarse_grid, UP)

        # Tạo lưới mịn (128x128 đại diện)
        fine_grid = NumberPlane(
            x_range=[-2, 2, 0.25], y_range=[-2, 2, 0.25],
            background_line_style={"stroke_color": FINE_GRID, "stroke_width": 1, "stroke_opacity": 0.8}
        ).scale(0.8).shift(RIGHT * 3)
        fine_label = Text("Lưới 128x128", font_size=24, color=FINE_GRID).next_to(fine_grid, UP)

        self.play(
            Create(coarse_grid), Write(coarse_label),
            run_time=3.0
        )
        self.play(
            Create(fine_grid), Write(fine_label),
            run_time=3.0
        )
        self.wait(9.0) # 3.0 + 3.0 + 9.0 = 15.0s

        # ---------------------------------------------------------
        # Beat 2: [2:00–2:15] (Target duration: 15.0s)
        # ---------------------------------------------------------
        # VO: "Vấn đề là: nếu bạn huấn luyện mô hình trên lưới 64x64..."
        
        # Mô phỏng quá trình infer trên lưới sai
        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE).move_to(ORIGIN)
        train_text = Text("Train: 64x64", font_size=20).next_to(arrow, UP)
        
        self.play(GrowArrow(arrow), FadeIn(train_text), run_time=2.0)
        
        # ValueTracker cho độ nhiễu (Glitch)
        noise_tracker = ValueTracker(0.0)
        
        # Hàm số hiển thị kết quả (bị nhiễu khi đưa lưới mịn vào)
        def get_noisy_function():
            noise = noise_tracker.get_value()
            graph = fine_grid.plot(lambda x: np.sin(2 * x) + np.random.uniform(-noise, noise), color=ERROR_RED)
            return graph

        output_func = always_redraw(get_noisy_function)
        
        self.play(Create(output_func), run_time=2.0)
        
        # Tăng dần độ nhiễu
        mismatch_text = Text("GRID MISMATCH", font_size=36, color=ERROR_RED, weight=BOLD).move_to(fine_grid)
        box = SurroundingRectangle(mismatch_text, color=ERROR_RED, fill_color=BLACK, fill_opacity=0.8)
        warning_group = VGroup(box, mismatch_text)

        self.play(noise_tracker.animate.set_value(2.0), run_time=2.0)
        self.play(FadeIn(warning_group, scale=1.5), Flash(warning_group, color=ERROR_RED), run_time=1.5)
        self.wait(7.5) # 2.0 + 2.0 + 2.0 + 1.5 + 7.5 = 15.0s

        # ---------------------------------------------------------
        # Beat 3: [2:15–2:30] (Target duration: 15.0s)
        # ---------------------------------------------------------
        # VO: "Hơn nữa, trong khoa học, các đạo hàm và tích phân..."
        
        self.play(
            FadeOut(coarse_grid, coarse_label, fine_grid, fine_label, arrow, train_text, output_func, warning_group),
            run_time=2.0
        )
        
        # Ràng buộc vật lý
        phys_eq = MathTex(r"\nabla u", r"\quad \text{và} \quad", r"\int u \, dx").scale(1.5)
        phys_eq[0].set_color(BLUE)
        phys_eq[2].set_color(GREEN)
        
        self.play(Write(phys_eq), run_time=3.0)
        
        barrier_text = Text("Discretization Dependence = Barrier to Science", font_size=32, color=TEXT_HIGHLIGHT).next_to(phys_eq, DOWN, buff=1.0)
        
        self.play(FadeIn(barrier_text, shift=UP), run_time=2.0)
        self.play(Indicate(barrier_text, scale_factor=1.1, color=ERROR_RED), run_time=2.0)
        
        self.wait(6.0) # 2.0 + 3.0 + 2.0 + 2.0 + 6.0 = 15.0s


class Scene1_4_TraditionalSolvers(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: [2:30–2:50] (Target duration: 20.0s)
        # ---------------------------------------------------------
        # VO: "Trước khi có Neural Operators, các nhà khoa học giải quyết..."
        
        pde_text = MathTex(r"-\nabla \cdot (a \nabla u) = f").scale(1.5).shift(UP * 2)
        pde_text.set_color_by_tex("a", YELLOW)
        pde_text.set_color_by_tex("u", PURPLE)
        
        self.play(Write(pde_text), run_time=4.0)
        
        # Flowchart
        box_pde = Text("PDE", font_size=24).shift(LEFT * 4)
        box_fdm = Text("Finite Diff / FEM", font_size=24)
        box_grid = Text("Fixed Grid", font_size=24).shift(RIGHT * 4)
        
        bg_pde = SurroundingRectangle(box_pde, color=BLUE, buff=0.2)
        bg_fdm = SurroundingRectangle(box_fdm, color=GREEN, buff=0.2)
        bg_grid = SurroundingRectangle(box_grid, color=RED, buff=0.2)
        
        arrow1 = Arrow(box_pde.get_right() + RIGHT*0.2, box_fdm.get_left() + LEFT*0.2)
        arrow2 = Arrow(box_fdm.get_right() + RIGHT*0.2, box_grid.get_left() + LEFT*0.2)
        
        flowchart = VGroup(box_pde, bg_pde, arrow1, box_fdm, bg_fdm, arrow2, box_grid, bg_grid).shift(DOWN * 1)
        
        self.play(FadeIn(VGroup(box_pde, bg_pde)), run_time=1.0)
        self.play(GrowArrow(arrow1), FadeIn(VGroup(box_fdm, bg_fdm)), run_time=1.5)
        self.play(GrowArrow(arrow2), FadeIn(VGroup(box_grid, bg_grid)), run_time=1.5)
        
        self.wait(12.0) # 4.0 + 1.0 + 1.5 + 1.5 + 12.0 = 20.0s

        # ---------------------------------------------------------
        # Beat 2: [2:50–3:10] (Target duration: 20.0s)
        # ---------------------------------------------------------
        # VO: "Cách tiếp cận này rất mạnh mẽ nhưng tồn tại những nút thắt..."
        
        self.play(FadeOut(flowchart, pde_text), run_time=2.0)
        
        # Animation tinh chỉnh lưới và chi phí tính toán
        grid_square = Square(side_length=4, color=WHITE)
        self.play(Create(grid_square), run_time=1.0)
        
        cost_tracker = ValueTracker(10) # Bắt đầu với chi phí nhỏ
        cost_text = always_redraw(lambda: Text(f"Cost: ${int(cost_tracker.get_value())}", color=RED).next_to(grid_square, UP))
        self.add(cost_text)
        
        # Lưới nội suy (tăng dần mật độ)
        resolutions = [4, 8, 16, 32]
        times = [2.0, 2.0, 3.0, 3.0]
        costs = [100, 1000, 50000, 1000000]
        
        current_grid = grid_square
        for res, t, cost in zip(resolutions, times, costs):
            new_grid = NumberPlane(
                x_range=[-2, 2, 4/res], y_range=[-2, 2, 4/res],
                x_length=4, y_length=4,
                background_line_style={"stroke_color": BLUE, "stroke_width": 1, "stroke_opacity": 0.5}
            )
            # Animation Transform lưới và tăng cost song song
            self.play(
                Transform(current_grid, new_grid),
                cost_tracker.animate.set_value(cost),
                run_time=t,
                rate_func=linear
            )
        
        # Hiệu ứng bùng nổ (Explosion) ở cuối
        explosion = Star(outer_radius=3, inner_radius=1, color=YELLOW, fill_color=RED, fill_opacity=0.8).move_to(grid_square)
        self.play(FadeIn(explosion, scale=0.1), run_time=0.5)
        self.play(explosion.animate.scale(2).set_opacity(0), run_time=0.5)
        
        self.wait(6.0) # 2.0 + 1.0 + (2+2+3+3) + 1.0 + 6.0 = 20.0s

        # ---------------------------------------------------------
        # Beat 3: [3:10–3:30] (Target duration: 20.0s)
        # ---------------------------------------------------------
        # VO: "Và còn những nút thắt khó gỡ: sai số tích lũy..."
        
        self.play(FadeOut(current_grid, cost_text), run_time=1.0)
        
        # 4 Icons / Hạn chế
        t1 = Text("1. Sai số tích lũy", font_size=28).shift(UP * 1.5 + LEFT * 3)
        t2 = Text("2. Chi phí bùng nổ", font_size=28).shift(UP * 1.5 + RIGHT * 3)
        t3 = Text("3. Rào cản chuyên môn", font_size=28).shift(DOWN * 1.5 + LEFT * 3)
        t4 = Text("4. Không khả vi", font_size=28).shift(DOWN * 1.5 + RIGHT * 3)
        
        self.play(FadeIn(t1, shift=UP), run_time=1.5)
        self.play(FadeIn(t2, shift=UP), run_time=1.5)
        self.play(FadeIn(t3, shift=UP), run_time=1.5)
        self.play(FadeIn(t4, shift=UP), run_time=1.5)
        
        center_text = Text("Cần bổ sung ML vào Toolbox", color=TEXT_HIGHLIGHT, font_size=36).move_to(ORIGIN)
        self.play(Write(center_text), run_time=3.0)
        
        self.wait(10.0) # 1.0 + 4*1.5 + 3.0 + 10.0 = 20.0s


class Scene1_5_Teaser(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: [3:30–3:45] (Target duration: 15.0s)
        # ---------------------------------------------------------
        # VO: "Câu hỏi đặt ra là: Liệu Machine Learning có thể học được trực tiếp ánh xạ..."
        
        # Màn hình chia đôi
        divider = Line(UP * 4, DOWN * 4, color=GRAY, stroke_width=2)
        
        # Bên trái: Hữu hạn chiều (Discrete)
        left_title = MathTex(r"\mathbb{R}^n \to \mathbb{R}^m").scale(1.2).shift(UP * 2.5 + LEFT * 3.5)
        left_title.set_color(DISCRETE_BLUE)
        
        vec_in = Matrix([["x_1"], ["\\vdots"], ["x_n"]]).scale(0.6).shift(LEFT * 5)
        vec_out = Matrix([["y_1"], ["\\vdots"], ["y_m"]]).scale(0.6).shift(LEFT * 2)
        arrow_discrete = Arrow(vec_in.get_right(), vec_out.get_left(), buff=0.2, color=DISCRETE_BLUE)
        f_theta = MathTex(r"f_\theta").next_to(arrow_discrete, UP, buff=0.1).scale(0.8)
        
        left_group = VGroup(left_title, vec_in, arrow_discrete, f_theta, vec_out)

        # Bên phải: Vô hạn chiều (Continuous)
        right_title = MathTex(r"\mathcal{A} \to \mathcal{U}").scale(1.2).shift(UP * 2.5 + RIGHT * 3.5)
        right_title.set_color(CONTINUOUS_PURPLE)
        
        axes_in = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=2, y_length=1.5).shift(RIGHT * 2)
        func_in = axes_in.plot(lambda x: np.sin(x), color=TEAL)
        label_a = MathTex("a(x)").next_to(func_in, DOWN, buff=0.1).scale(0.7)
        
        axes_out = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=2, y_length=1.5).shift(RIGHT * 5)
        func_out = axes_out.plot(lambda x: 0.5 * np.cos(2*x) + 0.5, color=CONTINUOUS_PURPLE)
        label_u = MathTex("u(x)").next_to(func_out, DOWN, buff=0.1).scale(0.7)
        
        arrow_cont = Arrow(axes_in.get_right(), axes_out.get_left(), buff=0.2, color=CONTINUOUS_PURPLE)
        g_theta = MathTex(r"\mathcal{G}_\theta").next_to(arrow_cont, UP, buff=0.1).scale(0.8)
        
        right_group = VGroup(right_title, axes_in, func_in, label_a, arrow_cont, g_theta, axes_out, func_out, label_u)

        # Animation Beat 1
        self.play(Create(divider), run_time=1.0)
        self.play(FadeIn(left_group, shift=RIGHT), run_time=2.0)
        self.play(FadeIn(right_group, shift=LEFT), run_time=2.0)
        
        # Dấu chấm hỏi xuất hiện
        question_mark = Text("?", font_size=120, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(Write(question_mark), run_time=2.0)
        
        self.wait(8.0) # 1.0 + 2.0 + 2.0 + 2.0 + 8.0 = 15.0s

        # ---------------------------------------------------------
        # Beat 2: [3:45–3:55] (Target duration: 10.0s)
        # ---------------------------------------------------------
        # VO: "Và câu trả lời chính là Neural Operators — thế hệ AI mới học trên không gian vô hạn chiều."
        
        self.play(
            FadeOut(divider, left_group, right_group),
            question_mark.animate.scale(1.5).set_color(NO_GOLD),
            run_time=2.0
        )
        
        # Hiệu ứng nổ (Flash) và Reveal
        self.play(Flash(question_mark, line_length=1.5, num_lines=12, color=NO_GOLD, flash_radius=1.5), run_time=0.5)
        self.remove(question_mark)
        
        logo_text = Tex(r"\textbf{Neural Operators}", font_size=72)
        logo_text.set_color_by_gradient(CONTINUOUS_PURPLE, NO_GOLD)
        
        sub_text = Tex(r"\textit{Learning in Infinite-Dimensional Spaces}", font_size=36)
        sub_text.next_to(logo_text, DOWN, buff=0.5)
        sub_text.set_color(LIGHT_GREY)
        
        self.play(GrowFromCenter(logo_text), run_time=1.5)
        self.play(FadeIn(sub_text, shift=UP), run_time=1.5)
        
        self.wait(4.5) # 2.0 + 0.5 + 1.5 + 1.5 + 4.5 = 10.0s

        # ---------------------------------------------------------
        # Beat 3: [3:55–4:00] (Target duration: 5.0s)
        # ---------------------------------------------------------
        # VO: (nhạc chuyển cảnh, pause ngắn)
        
        self.play(FadeOut(logo_text, sub_text), run_time=1.5)
        
        # Tiêu đề Section 2 (Đã sửa lỗi Unicode LaTeX bằng cách dùng Text)
        section_2_title = Text("Section 2: Thế giới hàm số", font_size=64, weight=BOLD)
        
        self.play(Write(section_2_title), run_time=2.0)
        self.wait(1.5) # 1.5 + 2.0 + 1.5 = 5.0s