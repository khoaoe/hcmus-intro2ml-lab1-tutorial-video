import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from manim import *
import numpy as np
from utils.colors import *

class Scene1_1_Hook(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ==========================================
        # BEAT 1 [0:00 - 0:12] Target: 12.0 seconds
        # ==========================================
        # VO: "Trong hàng chục năm qua, Deep Learning đã tạo ra những đột phá không tưởng..."
        
        # Tạo grid 16x16 đại diện cho ảnh 64x64 để tối ưu render
        grid_size = 16
        squares = VGroup(*[
            Square(side_length=0.25).set_style(fill_opacity=0, stroke_width=1, stroke_color=GREY_D)
            for _ in range(grid_size**2)
        ]).arrange_in_grid(grid_size, grid_size, buff=0)
        
        # 0.5s: Hiện lưới
        self.play(FadeIn(squares), run_time=0.5)
        
        # 5.5s: Pixel fill animation (Tạo màu cho ảnh)
        fill_animations = []
        for i, square in enumerate(squares):
            # Tính khoảng cách từ tâm để tạo một gradient giả lập hình ảnh
            x, y = i % grid_size, i // grid_size
            dist = np.sqrt((x - grid_size/2)**2 + (y - grid_size/2)**2)
            color = interpolate_color(TEAL, PURPLE, dist / (grid_size/2))
            fill_animations.append(
                square.animate.set_style(fill_opacity=0.8, fill_color=color, stroke_width=0)
            )
            
        self.play(LaggedStart(*fill_animations, lag_ratio=0.01), run_time=5.5)
        
        # Padding cho đủ 12 giây (0.5 + 5.5 + 6.0 = 12.0)
        self.wait(6.0)

        # ==========================================
        # BEAT 2 [0:12 - 0:28] Target: 16.0 seconds
        # ==========================================
        # VO: "Chúng ta đã quá quen thuộc với việc CNN nhận diện hình ảnh..."
        
        # 2.0s: Image morphs into abstract 1D Vector (Flatten)
        flattened_squares = squares.copy().arrange_in_grid(1, grid_size**2, buff=0.05).scale(0.3)
        flattened_squares.move_to(RIGHT * 3)
        self.play(ReplacementTransform(squares, flattened_squares), run_time=2.0)
        
        # 2.0s: Tạo W matrix (Neural Network Weights)
        w_matrix = Rectangle(width=4, height=6, color=C_MATRIX, fill_opacity=0.3)
        w_label = MathTex("W", font_size=72, color=C_MATRIX)
        w_group = VGroup(w_matrix, w_label).move_to(LEFT * 2)
        
        x_label = MathTex(r"\vec{x}", font_size=48, color=C_VECTOR).next_to(flattened_squares, UP)
        
        self.play(
            FadeIn(w_group, shift=RIGHT),
            FadeIn(x_label, shift=DOWN),
            run_time=2.0
        )
        
        # 2.0s: Abstract Matrix Multiplication
        equation_eq = MathTex("=").next_to(flattened_squares, RIGHT)
        y_vector = Rectangle(width=0.5, height=4, color=C_SECONDARY, fill_opacity=0.8).next_to(equation_eq, RIGHT)
        y_label = MathTex(r"\vec{y}", font_size=48, color=C_SECONDARY).next_to(y_vector, UP)
        
        self.play(
            Write(equation_eq),
            FadeIn(y_vector, shift=LEFT),
            Write(y_label),
            run_time=2.0
        )
        
        dl_math_group = VGroup(w_group, flattened_squares, x_label, equation_eq, y_vector, y_label)
        
        # Padding cho đủ 16 giây (2.0 + 2.0 + 2.0 + 10.0 = 16.0)
        self.wait(10.0)

        # ==========================================
        # BEAT 3 [0:28 - 0:45] Target: 17.0 seconds
        # ==========================================
        # VO: "Nhưng nếu lùi lại một bước để quan sát, tất cả các mô hình này..."
        
        # 2.0s: Zoom out and collapse math into a single discrete dot
        discrete_dot = Dot(radius=0.15, color=C_DISCRETE)
        self.play(
            ReplacementTransform(dl_math_group, discrete_dot),
            run_time=2.0
        )
        
        # 3.0s: Hiện hệ tọa độ R^n với các điểm rời rạc
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6
        )
        axes_labels = axes.get_axis_labels(x_label="x_1", y_label="x_2", z_label="x_n")
        
        # Tạo thêm vài điểm rời rạc để nhấn mạnh tính chất Euclid
        random_dots = VGroup(*[
            Dot3D(axes.c2p(np.random.uniform(-2, 2), np.random.uniform(-2, 2), np.random.uniform(-2, 2)), color=GREY, radius=0.1)
            for _ in range(15)
        ])
        
        rn_space = VGroup(axes, axes_labels, random_dots, discrete_dot)
        
        self.play(
            Create(axes),
            FadeIn(axes_labels),
            FadeIn(random_dots),
            discrete_dot.animate.move_to(axes.c2p(1.5, 2, 1)),
            run_time=3.0
        )
        
        # 2.0s: Text Overlay "Finite-dimensional Euclidean Space R^n"
        title = Text("Finite-dimensional Euclidean Space", font_size=36, weight=BOLD)
        subtitle = MathTex(r"\mathbb{R}^n", font_size=60, color=C_DISCRETE)
        text_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5).to_corner(UL)
        
        self.play(
            Write(text_group),
            rn_space.animate.rotate(PI/6, axis=UP).rotate(-PI/12, axis=RIGHT), # 3D slight rotation for depth
            run_time=2.0
        )
        
        # Padding cho đủ 17 giây (2.0 + 3.0 + 2.0 + 10.0 = 17.0)
        self.wait(10.0)
        
        # Dọn dẹp màn hình chuẩn bị cho Scene 1.2
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene1_2_PlotTwist(ThreeDScene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # ==========================================
        # BEAT 1 [0:45 - 1:00] Target: 15.0 seconds
        # ==========================================
        # VO: "Tuy nhiên, nếu chúng ta bước ra khỏi Khoa học Máy tính..."
        
        # 1.5s: Giả lập hiệu ứng "Shatter" không gian rời rạc R^n cũ
        rn_dots = VGroup(*[
            Dot3D(np.random.uniform(-3, 3, 3), color=C_DISCRETE, radius=0.15)
            for _ in range(30)
        ])
        self.add(rn_dots)
        self.play(FadeOut(rn_dots, shift=OUT * 3, scale=3), run_time=1.5)
        
        # 1.5s: Khởi tạo mô hình quả cầu Trái Đất liên tục (Core Function Domain)
        globe = Sphere(radius=1.5, resolution=(30, 30))
        globe.set_color(BLUE_E).set_opacity(0.6)
        self.play(Create(globe), run_time=1.5)
        
        # Lần lượt fade-in 3 lớp trường đại diện (0.5s x 3 = 1.5s)
        temp_layer = Sphere(radius=1.6, resolution=(20, 20)).set_color(RED).set_opacity(0.15)
        wind_layer = Sphere(radius=1.7, resolution=(20, 20)).set_color(TEAL).set_opacity(0.15)
        pres_layer = Sphere(radius=1.8, resolution=(20, 20)).set_color(YELLOW).set_opacity(0.15)
        
        self.play(FadeIn(temp_layer), run_time=0.5)
        self.play(FadeIn(wind_layer), run_time=0.5)
        self.play(FadeIn(pres_layer), run_time=0.5)
        
        # Padding cho Beat 1 (1.5 + 1.5 + 1.5 + 10.5 = 15.0s)
        self.wait(10.5)

        # ==========================================
        # BEAT 2 [1:00 - 1:25] Target: 25.0 seconds
        # ==========================================
        # Dọn dẹp Beat 1 (0.5s)
        self.play(FadeOut(Group(globe, temp_layer, wind_layer, pres_layer)), run_time=0.5)
        
        # --- 1. Da liễu (5.0s) ---
        # VO: "Da liễu nghiên cứu mô da trên bề mặt liên tục."
        skin_surface = Surface(
            lambda u, v: np.array([u, v, 0.4 * np.sin(u) * np.cos(v)]),
            u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(20, 20)
        ).set_color_by_gradient(ORANGE, RED_E)
        
        skin_label = Text("Da liễu (Continuous Surface)", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(skin_label)
        
        self.play(Create(skin_surface), FadeIn(skin_label), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(skin_surface), FadeOut(skin_label), run_time=0.5)
        
        # --- 2. Địa vật lý (5.0s) ---
        # VO: "Địa vật lý phân tích hàm 3D mô tả sóng địa chấn."
        geo_wave1 = Sphere(radius=0.5, resolution=(20, 20)).set_color(PURPLE).set_opacity(0.6)
        geo_wave2 = Sphere(radius=1.5, resolution=(20, 20)).set_color(PURPLE).set_opacity(0.3)
        geo_wave3 = Sphere(radius=2.5, resolution=(20, 20)).set_color(PURPLE).set_opacity(0.1)
        
        geo_label = Text("Địa vật lý (3D Seismic Waves)", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(geo_label)
        
        self.play(Create(geo_wave1), FadeIn(geo_label), run_time=0.5)
        self.play(TransformFromCopy(geo_wave1, geo_wave2), TransformFromCopy(geo_wave2, geo_wave3), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(Group(geo_wave1, geo_wave2, geo_wave3)), FadeOut(geo_label), run_time=0.5)
        
        # --- 3. Cơ khí CFD (5.0s) ---
        # VO: "Cơ khí tính toán trường vector 4D."
        cfd_curves = VGroup(*[
            ParametricFunction(
                lambda t, offset=i: np.array([t, 0.8 * np.sin(t + offset), 0.8 * np.cos(t + offset)]),
                t_range=[-3, 3]
            ).set_color(TEAL).set_stroke(width=4) for i in np.linspace(0, 2*PI, 6)
        ])
        
        cfd_label = Text("Cơ học Lưu chất (Vector Fields)", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(cfd_label)
        
        self.play(Create(cfd_curves), FadeIn(cfd_label), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(cfd_curves), FadeOut(cfd_label), run_time=0.5)
        
        # --- 4. Khí hậu (9.5s) ---
        # VO: "Khí hậu mô phỏng hàng trăm hàm trên cầu... Dữ liệu của họ là hàm số."
        climate_globe = Sphere(radius=2.0, resolution=(40, 40))
        climate_globe.set_color_by_gradient(BLUE_D, GREEN, YELLOW, RED_D)
        
        climate_label = Text("Khí hậu (Functions on Sphere)", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(climate_label)
        
        self.play(FadeIn(climate_globe), FadeIn(climate_label), run_time=1.0)
        self.play(Rotate(climate_globe, angle=PI, axis=UP), run_time=2.0)
        self.wait(6.5)
        # Tổng Beat 2: 0.5 + 5.0 + 5.0 + 5.0 + 9.5 = 25.0s

        # ==========================================
        # BEAT 3 [1:25 - 1:45] Target: 20.0 seconds
        # ==========================================
        # VO: "Và đây là điểm then chốt: khi ta cố ép một mô hình Deep Learning truyền thống..."
        
        self.play(FadeOut(climate_label), run_time=1.0)
        
        # 4.0s: Infinite Zoom - Scale khối cầu lên cực đại để thấy độ mịn màng liên tục (không có pixel)
        self.play(
            climate_globe.animate.scale(15).shift(IN * 5),
            run_time=4.0,
            rate_func=linear
        )
        
        # 2.0s: Text xuất hiện khẳng định bản chất
        final_text = Text("Data = Functions", font_size=72, weight=BOLD, color=C_ACCENT)
        self.add_fixed_in_frame_mobjects(final_text)
        
        # Sử dụng Write kết hợp Glow mờ ảo để tôn lên tính chất toán học
        self.play(Write(final_text), run_time=2.0)
        
        # Padding cho Beat 3 (1.0 + 4.0 + 2.0 + 12.0 = 19.0 + 1.0 dọn dẹp = 20.0s)
        self.wait(12.0)
        
        # 1.0s: Dọn dẹp sạch sẽ chuẩn bị cho Scene 1.3
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)


class Scene1_3_GridMismatch(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ==========================================
        # BEAT 1 [1:45 - 2:00] Target: 15.0 seconds
        # ==========================================
        # VO: "Sự khác biệt này tạo ra một khoảng cách công nghệ khổng lồ..."
        
        # Hàm ẩn dụ lấy mẫu nhiệt độ: sin(x) + cos(y)
        def temp_func(x, y, grid_size):
            nx, ny = x / grid_size * 2 * PI, y / grid_size * 2 * PI
            val = np.sin(nx) + np.cos(ny)
            return interpolate_color(BLUE, RED, (val + 2) / 4)

        # Tạo lưới Coarse (8x8 đại diện cho 64x64)
        coarse_grid = VGroup(*[
            Square(side_length=0.4).set_style(fill_opacity=0.8, fill_color=temp_func(i%8, i//8, 8), stroke_width=0.5, stroke_color=WHITE)
            for i in range(8**2)
        ]).arrange_in_grid(8, 8, buff=0)
        
        coarse_label = Text("64x64 Grid (Coarse)", font_size=24, color=BLUE_B).next_to(coarse_grid, UP)
        coarse_group = VGroup(coarse_grid, coarse_label).move_to(LEFT * 3)

        # Tạo lưới Fine (16x16 đại diện cho 128x128)
        fine_grid = VGroup(*[
            Square(side_length=0.2).set_style(fill_opacity=0.8, fill_color=temp_func(i%16, i//16, 16), stroke_width=0.1, stroke_color=WHITE)
            for i in range(16**2)
        ]).arrange_in_grid(16, 16, buff=0)
        
        fine_label = Text("128x128 Grid (Fine)", font_size=24, color=PURPLE_B).next_to(fine_grid, UP)
        fine_group = VGroup(fine_grid, fine_label).move_to(RIGHT * 3)

        # 3.0s: Tạo hai lưới song song
        self.play(
            Create(coarse_grid, lag_ratio=0.01), FadeIn(coarse_label, shift=DOWN),
            Create(fine_grid, lag_ratio=0.005), FadeIn(fine_label, shift=DOWN),
            run_time=3.0
        )
        
        # Padding cho Beat 1 (3.0s + 12.0s = 15.0s)
        self.wait(12.0)

        # ==========================================
        # BEAT 2 [2:00 - 2:15] Target: 15.0 seconds
        # ==========================================
        # VO: "Vấn đề là: nếu bạn huấn luyện mô hình trên lưới 64x64 nhưng lại muốn chạy thử nghiệm..."
        
        # 1.0s: Biến màn hình để chuẩn bị đưa vào NN
        self.play(
            coarse_group.animate.scale(0.6).to_corner(DL),
            fine_group.animate.scale(0.6).to_corner(UL),
            run_time=1.0
        )
        
        # 1.5s: Hiện Model
        nn_box = Rectangle(width=3, height=4, color=C_SECONDARY, fill_opacity=0.2).move_to(RIGHT * 3)
        nn_text = Text("Fixed-Grid\nCNN Model", font_size=28).move_to(nn_box)
        nn_group = VGroup(nn_box, nn_text)
        self.play(FadeIn(nn_group, shift=LEFT), run_time=1.5)
        
        # 1.5s: Train trên lưới thô -> Thành công
        arrow_coarse = Arrow(coarse_group.get_right(), nn_box.get_left(), color=GREEN_C)
        train_text = Text("Trained OK!", font_size=24, color=GREEN_C).next_to(arrow_coarse, UP)
        self.play(GrowArrow(arrow_coarse), FadeIn(train_text), run_time=1.5)
        self.wait(1.5)
        
        # 2.0s: Đưa lưới mịn vào -> Thất bại
        self.play(FadeOut(arrow_coarse), FadeOut(train_text), run_time=0.5)
        arrow_fine = Arrow(fine_group.get_right(), nn_box.get_left(), color=RED_C)
        self.play(GrowArrow(arrow_fine), run_time=1.5)
        
        # 1.5s: Glitch Effect & Grid Mismatch Alert
        mismatch_alert = Text("GRID MISMATCH", font_size=60, color=RED, weight=BOLD)
        mismatch_alert.set_stroke(BLACK, 5, background=True)
        mismatch_box = BackgroundRectangle(mismatch_alert, color=BLACK, fill_opacity=0.8, buff=0.2)
        alert_group = VGroup(mismatch_box, mismatch_alert).move_to(ORIGIN)

        # Lắc khối NN để tạo cảm giác bị lỗi
        self.play(
            Wiggle(nn_group, scale_value=1.2, rotation_angle=0.05 * PI, n_wiggles=6),
            nn_box.animate.set_color(RED).set_fill(RED_E, opacity=0.5),
            FadeIn(alert_group, scale=1.5),
            run_time=1.5
        )
        
        # Padding cho Beat 2 (1.0 + 1.5 + 1.5 + 1.5 + 0.5 + 1.5 + 1.5 + 6.0 = 15.0s)
        self.wait(6.0)

        # ==========================================
        # BEAT 3 [2:15 - 2:30] Target: 15.0 seconds
        # ==========================================
        # VO: "Hơn nữa, trong khoa học, các đạo hàm và tích phân của đầu ra phải tuân thủ..."
        
        # 1.0s: Dọn dẹp scene trước
        self.play(
            FadeOut(coarse_group), FadeOut(fine_group), FadeOut(arrow_fine),
            FadeOut(nn_group), FadeOut(alert_group),
            run_time=1.0
        )
        
        # 3.0s: Khởi tạo các phương trình vật lý bị vi phạm
        eq_grad = MathTex(r"\nabla u(x)", font_size=72, color=BLUE_B)
        eq_int = MathTex(r"\int u(x) \, dx", font_size=72, color=TEAL_C)
        equations = VGroup(eq_grad, eq_int).arrange(RIGHT, buff=2).move_to(UP * 1)
        
        self.play(Write(eq_grad), run_time=1.5)
        self.play(Write(eq_int), run_time=1.5)
        
        # 2.0s: Barrier Text
        barrier_title = Text("Discretization Dependence", font_size=40, color=RED_B)
        barrier_subtitle = Text("= Barrier to Science", font_size=40, color=WHITE, weight=BOLD)
        barrier_group = VGroup(barrier_title, barrier_subtitle).arrange(DOWN, buff=0.3).next_to(equations, DOWN, buff=1.5)
        
        # Dấu chéo đè lên các phương trình liên tục để thể hiện việc lưới rời rạc phá vỡ vật lý
        cross1 = Cross(eq_grad, stroke_color=RED_C, stroke_width=6)
        cross2 = Cross(eq_int, stroke_color=RED_C, stroke_width=6)
        
        self.play(
            Write(barrier_group),
            Create(cross1), Create(cross2),
            run_time=2.0
        )
        
        # Cảm giác nhấp nháy (Pulse) để nhấn mạnh sự nghiêm trọng
        self.play(
            barrier_title.animate.set_opacity(0.5),
            rate_func=there_and_back, run_time=1.0
        )
        
        # Padding cho Beat 3 (1.0 + 3.0 + 2.0 + 1.0 + 8.0 = 15.0s)
        self.wait(8.0)
        
        # 0.5s: Dọn sạch chuẩn bị cho Scene 1.4 (Lưu ý: 0.5s này có thể lấn nhẹ sang transition)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


class Scene1_4_TraditionalSolvers(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ==========================================
        # BEAT 1 [2:30 - 2:50] Target: 20.0 seconds
        # ==========================================
        # VO: "Trước khi có Neural Operators, các nhà khoa học giải quyết những bài toán này..."
        
        # 3.0s: Hiện phương trình PDE
        pde_title = Text("Partial Differential Equation (PDE)", font_size=36, color=C_SECONDARY)
        pde_eq = MathTex(
            r"-\nabla \cdot (", r"a(x)", r"\nabla ", r"u(x)", r") = ", r"f(x)",
            font_size=60
        )
        pde_eq.set_color_by_tex(r"a(x)", BLUE)
        pde_eq.set_color_by_tex(r"u(x)", PURPLE_C)
        pde_eq.set_color_by_tex(r"f(x)", GREEN)
        
        pde_group = VGroup(pde_title, pde_eq).arrange(DOWN, buff=0.5).move_to(UP * 2)
        
        self.play(FadeIn(pde_title, shift=DOWN), Write(pde_eq), run_time=3.0)
        self.wait(1.0)
        
        # 4.0s: Tạo Flowchart
        box1 = Rectangle(width=3, height=1.5, color=WHITE)
        text1 = Text("Continuous\nPDE", font_size=24).move_to(box1)
        node1 = VGroup(box1, text1)
        
        box2 = Rectangle(width=3, height=1.5, color=BLUE_B)
        text2 = Text("Finite\nDifferences", font_size=24).move_to(box2)
        node2 = VGroup(box2, text2)
        
        box3 = Rectangle(width=3, height=1.5, color=RED_B)
        text3 = Text("Fixed\nDiscrete Grid", font_size=24).move_to(box3)
        node3 = VGroup(box3, text3)
        
        flowchart = VGroup(node1, node2, node3).arrange(RIGHT, buff=1.0).move_to(DOWN * 1.5)
        arrow1 = Arrow(node1.get_right(), node2.get_left(), buff=0.1)
        arrow2 = Arrow(node2.get_right(), node3.get_left(), buff=0.1)
        
        self.play(Create(node1), run_time=1.0)
        self.play(GrowArrow(arrow1), Create(node2), run_time=1.5)
        self.play(GrowArrow(arrow2), Create(node3), run_time=1.5)
        
        # Padding Beat 1 (3.0 + 1.0 + 4.0 + 12.0 = 20.0s)
        self.wait(12.0)

        # ==========================================
        # BEAT 2 [2:50 - 3:10] Target: 20.0 seconds
        # ==========================================
        # VO: "Cách tiếp cận này rất mạnh mẽ nhưng tồn tại những nút thắt khó gỡ..."
        
        # 1.0s: Dọn dẹp Beat 1
        self.play(FadeOut(pde_group), FadeOut(flowchart), FadeOut(arrow1), FadeOut(arrow2), run_time=1.0)
        
        # Thiết lập trực quan hóa lưới và đồng hồ
        # Lưới abstraction: Dùng số lượng ô vuông nhỏ dần để biểu diễn
        def get_grid(n, color=BLUE_E):
            grid = VGroup(*[
                Square(side_length=4/n).set_style(fill_opacity=0.3, fill_color=color, stroke_width=0.5)
                for _ in range(n**2)
            ]).arrange_in_grid(n, n, buff=0)
            return grid

        grid_mob = get_grid(4).move_to(LEFT * 2.5) # Represent 16^2
        
        # Đồng hồ đếm giờ
        time_tracker = ValueTracker(0.01)
        time_label = Text("Compute Time:", font_size=36).move_to(RIGHT * 2.5 + UP * 1)
        time_val = DecimalNumber(0.01, num_decimal_places=2, font_size=48, color=GREEN).next_to(time_label, DOWN)
        time_val.add_updater(lambda d: d.set_value(time_tracker.get_value()))
        unit = Text("s", font_size=36).next_to(time_val, RIGHT, aligned_edge=DOWN)
        
        res_label = Text("Resolution: 16x16", font_size=32).next_to(grid_mob, DOWN, buff=0.5)
        
        self.play(Create(grid_mob), FadeIn(time_label), FadeIn(time_val), FadeIn(unit), FadeIn(res_label), run_time=2.0)
        
        # 4.5s: Tăng dần độ phân giải và thời gian
        # Step 1: 32x32
        grid_32 = get_grid(8).move_to(LEFT * 2.5)
        self.play(
            Transform(grid_mob, grid_32),
            res_label.animate.become(Text("Resolution: 32x32", font_size=32).next_to(grid_mob, DOWN, buff=0.5)),
            time_tracker.animate.set_value(0.50),
            run_time=1.5
        )
        
        # Step 2: 64x64
        grid_64 = get_grid(16).move_to(LEFT * 2.5)
        self.play(
            Transform(grid_mob, grid_64),
            res_label.animate.become(Text("Resolution: 64x64", font_size=32).next_to(grid_mob, DOWN, buff=0.5)),
            time_tracker.animate.set_value(8.00),
            time_val.animate.set_color(YELLOW),
            run_time=1.5
        )
        
        # Step 3: 128x128 (Bùng nổ)
        grid_128 = get_grid(32, color=RED_E).move_to(LEFT * 2.5)
        self.play(
            Transform(grid_mob, grid_128),
            res_label.animate.become(Text("Resolution: 128x128", font_size=32, color=RED).next_to(grid_mob, DOWN, buff=0.5)),
            time_tracker.animate.set_value(999.99), # Exponential jump
            time_val.animate.set_color(RED),
            run_time=1.5
        )
        
        # 1.5s: Explosion Effect
        explosion_center = time_val.get_center() + RIGHT * 0.8
        explosion = Star(outer_radius=2.2, inner_radius=1.0, color=RED, fill_opacity=0.3).move_to(explosion_center)
        boom_text = Text("EXPLOSION", font_size=48, color=WHITE, weight=BOLD).move_to(explosion_center)
        self.play(
            FadeIn(explosion, scale=0.1), 
            Write(boom_text),
            time_val.animate.set_opacity(0),
            unit.animate.set_opacity(0),
            run_time=0.5
        )
        self.play(Flash(explosion, color=YELLOW, line_length=2), run_time=1.0)
        
        # Padding Beat 2 (1.0 + 2.0 + 4.5 + 1.5 + 11.0 = 20.0s)
        self.wait(11.0)

        # ==========================================
        # BEAT 3 [3:10 - 3:30] Target: 20.0 seconds
        # ==========================================
        # VO: "Và còn những nút thắt khó gỡ: sai số tích lũy do tham số hóa..."
        
        # 1.0s: Dọn màn hình
        self.play(
            FadeOut(grid_mob), FadeOut(res_label), FadeOut(time_label), 
            FadeOut(explosion), FadeOut(boom_text), FadeOut(time_val), FadeOut(unit),
            run_time=1.0
        )
        
        # Tạo 4 khối thông tin (Grid 2x2)
        def create_limitation_card(text_str, icon_mob, position):
            card = RoundedRectangle(width=5, height=2.5, corner_radius=0.2, color=GREY, fill_opacity=0.1)
            card.move_to(position)
            icon_mob.move_to(card.get_center() + UP * 0.3).scale(0.8)
            label = Text(text_str, font_size=24).move_to(card.get_center() + DOWN * 0.7)
            return VGroup(card, icon_mob, label)

        # Card centers are spread farther apart to avoid horizontal overlap.
        left_col_x, right_col_x = 3.3, 3.3
        top_row_y, bottom_row_y = 2.3, -1.2

        # 1: Sai số
        err_icon = MathTex(r"\epsilon \approx \mathcal{O}(\Delta x)", color=C_WARNING)
        card1 = create_limitation_card("1. Accumulation Error", err_icon, LEFT * left_col_x + UP * top_row_y)
        
        # 2: Chi phí (Line chart)
        cost_ax = Axes(x_range=[0, 3], y_range=[0, 5], x_length=2, y_length=1).set_color(GREY)
        cost_curve = cost_ax.plot(lambda x: 0.2 * np.exp(x), color=RED_B)
        card2 = create_limitation_card("2. Exponential Cost", VGroup(cost_ax, cost_curve), RIGHT * right_col_x + UP * top_row_y)
        
        # 3: Chuyên môn (Stack of books)
        book1 = Rectangle(width=1.5, height=0.3, color=BLUE, fill_opacity=0.8)
        book2 = Rectangle(width=1.3, height=0.4, color=TEAL, fill_opacity=0.8).next_to(book1, UP, buff=0)
        book3 = Rectangle(width=1.4, height=0.3, color=PURPLE, fill_opacity=0.8).next_to(book2, UP, buff=0)
        card3 = create_limitation_card("3. Expertise Barrier", VGroup(book1, book2, book3), LEFT * left_col_x + UP * bottom_row_y)
        
        # 4: Không khả vi
        diff_icon = MathTex(r"\frac{\partial \text{Solver}}{\partial \theta} = ?", color=ORANGE)
        card4 = create_limitation_card("4. Non-Differentiable", diff_icon, RIGHT * right_col_x + UP * bottom_row_y)
        
        # 4.0s: Hiện lần lượt 4 nút thắt
        self.play(FadeIn(card1, shift=UP), run_time=1.0)
        self.play(FadeIn(card2, shift=UP), run_time=1.0)
        self.play(FadeIn(card3, shift=UP), run_time=1.0)
        self.play(FadeIn(card4, shift=UP), run_time=1.0)
        
        # 3.0s: Final objective chốt hạ
        target_box = BackgroundRectangle(Text("x", font_size=40), color=BLACK, fill_opacity=0.8, buff=0.5) # Dummy to size
        final_text = Text("Add ML to toolbox,\nNOT to replace.", font_size=48, color=C_ACCENT)
        final_group = VGroup(BackgroundRectangle(final_text, color=BLACK, fill_opacity=0.9, buff=0.4), final_text)
        final_group.move_to(ORIGIN)
        
        self.play(FadeIn(final_group, scale=1.2), run_time=1.5)
        self.play(Flash(final_group, color=C_ACCENT, line_length=1.5), run_time=1.5)
        
        # Padding Beat 3 (1.0 + 4.0 + 3.0 + 11.0 = 19.0 + 1.0 = 20.0s)
        self.wait(11.0)
        
        # 1.0s: Dọn sạch màn hình để chốt Section 1
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from manim import *
from utils.colors import *

class Scene1_5_Teaser(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ==========================================
        # BEAT 1 [3:30 - 3:45] Target: 15.0 seconds
        # ==========================================
        # VO: "Câu hỏi đặt ra là: Liệu Machine Learning có thể học được trực tiếp ánh xạ..."
        
        # Tạo đường phân chia màn hình
        divider = Line(UP * 4, DOWN * 4, color=GREY, stroke_opacity=0.5)
        
        # Nửa trái: Traditional ML
        left_title = Text("Traditional ML", font_size=32, color=BLUE_C).move_to(LEFT * 3.5 + UP * 2)
        left_math = MathTex(
            r"f_\theta : ", r"\mathbb{R}^n", r"\to", r"\mathbb{R}^m", 
            font_size=48
        ).next_to(left_title, DOWN, buff=0.5)
        left_math.set_color_by_tex(r"\mathbb{R}", BLUE_B)
        
        # Icon Vector cho nửa trái
        left_icon = VGroup(*[Dot(color=BLUE_E, radius=0.1) for _ in range(5)]).arrange(DOWN, buff=0.2)
        left_icon.next_to(left_math, DOWN, buff=1)
        left_group = VGroup(left_title, left_math, left_icon)

        # Nửa phải: Operator Learning
        right_title = Text("Operator Learning", font_size=32, color=PURPLE_C).move_to(RIGHT * 3.5 + UP * 2)
        right_math = MathTex(
            r"\mathcal{G}_\theta : ", r"\mathcal{A}", r"\to", r"\mathcal{U}", 
            font_size=48
        ).next_to(right_title, DOWN, buff=0.5)
        right_math.set_color_by_tex(r"\mathcal{A}", PURPLE_B)
        right_math.set_color_by_tex(r"\mathcal{U}", PURPLE_B)
        
        # Icon Hàm liên tục cho nửa phải
        right_icon = ParametricFunction(
            lambda t: np.array([t, 0.5 * np.sin(3 * t), 0]), t_range=[-1.5, 1.5]
        ).set_color(PURPLE_B).set_stroke(width=4)
        right_icon.next_to(right_math, DOWN, buff=1)
        right_group = VGroup(right_title, right_math, right_icon)

        # 3.0s: Hiện hai nửa màn hình
        self.play(Create(divider), run_time=0.5)
        self.play(FadeIn(left_group, shift=RIGHT), FadeIn(right_group, shift=LEFT), run_time=2.5)
        
        # 1.0s: Dấu chấm hỏi lớn ở giữa
        question_mark = Text("?", font_size=120, color=C_ACCENT, weight=BOLD).move_to(ORIGIN)
        question_bg = BackgroundRectangle(question_mark, color=C_BACKGROUND, fill_opacity=0.8, buff=0.2)
        q_group = VGroup(question_bg, question_mark)
        
        self.play(FadeIn(q_group, scale=0.5), run_time=1.0)
        
        # Padding Beat 1 (3.0 + 1.0 + 11.0 = 15.0s)
        self.wait(11.0)

        # ==========================================
        # BEAT 2 [3:45 - 3:55] Target: 10.0 seconds
        # ==========================================
        # VO: "Và câu trả lời chính là Neural Operators — thế hệ AI mới học trên không gian..."
        
        # 1.0s: Vụ nổ làm biến mất mọi thứ cũ
        self.play(
            Flash(ORIGIN, color=C_ACCENT, line_length=4, num_lines=20, flash_radius=1),
            FadeOut(left_group), FadeOut(right_group), FadeOut(divider), FadeOut(q_group),
            run_time=1.0
        )
        
        # 2.0s: Hiện Logo Neural Operators
        # Tạo logo bằng cách kết hợp chữ N và ký hiệu Vô cực/Tích phân
        logo_n = MathTex(r"\mathcal{N}", font_size=160, color=WHITE)
        logo_o = MathTex(r"\mathcal{O}", font_size=160, color=C_PRIMARY).next_to(logo_n, RIGHT, buff=0.1)
        logo_glow = VGroup(logo_n, logo_o).copy().set_color(TEAL).set_opacity(0.4).set_stroke(width=15)
        
        logo = VGroup(logo_glow, logo_n, logo_o).move_to(UP * 0.5)
        
        title_main = Text("Neural Operators", font_size=60, weight=BOLD).next_to(logo, DOWN, buff=0.5)
        title_sub = Text("AI for Infinite-Dimensional Spaces", font_size=32, color=GREY_B).next_to(title_main, DOWN, buff=0.3)
        
        self.play(
            GrowFromCenter(logo),
            run_time=1.0
        )
        self.play(
            Write(title_main),
            FadeIn(title_sub, shift=UP),
            run_time=1.0
        )
        
        # Padding Beat 2 (1.0 + 2.0 + 7.0 = 10.0s)
        self.wait(7.0)

        # ==========================================
        # BEAT 3 [3:55 - 4:00] Target: 5.0 seconds
        # ==========================================
        # VO: (nhạc chuyển cảnh, pause ngắn)
        
        # 1.0s: Fade out mọi thứ (Fade to black)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        
        # 2.0s: Hiện tiêu đề Section 2
        section_title = Text("SECTION 2", font_size=40, color=C_PRIMARY, weight=BOLD)
        section_subtitle = Text("Thế giới Hàm số", font_size=60, color=WHITE, weight=BOLD)
        section_group = VGroup(section_title, section_subtitle).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        
        self.play(Write(section_group), run_time=2.0)
        
        # Padding Beat 3 (1.0 + 2.0 + 2.0 = 5.0s) để giữ trước khi cut
        self.wait(2.0)
        
        # Dọn dẹp màn hình chuẩn bị cho Scene mới
        self.play(FadeOut(section_group), run_time=0.5)