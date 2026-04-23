import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from manim import *
from utils.colors import *


class Scene2_1_NatureOfScienceData(ThreeDScene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [4:00 - 4:30] (30.0s): Khí hậu & Thời tiết
        # ============================================================
        # VO: "Trước khi đi sâu vào định nghĩa Neural Operator, hãy quan sát bản chất..."
        
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        
        # Globe setup
        globe = Sphere(radius=1.5, resolution=(20, 20)).set_color(C_PRIMARY).set_opacity(0.4)
        
        # Layers (Nhiệt độ, gió, áp suất)
        temp_layer = Sphere(radius=1.6, resolution=(15, 15)).set_color(C_WARNING).set_opacity(0.2)
        wind_layer = Sphere(radius=1.7, resolution=(15, 15)).set_color(C_SECONDARY).set_opacity(0.2)
        pressure_layer = Sphere(radius=1.8, resolution=(15, 15)).set_color(C_ACCENT).set_opacity(0.1)
        
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # Timeline: 30s total
        self.play(Create(globe), run_time=2.0)
        self.play(FadeIn(temp_layer), run_time=1.5)
        self.play(FadeIn(wind_layer), run_time=1.5)
        self.play(FadeIn(pressure_layer), run_time=1.5)
        self.wait(5.5) # Hold to sync
        
        # "Trạng thái hôm nay -> Ngày mai" - Switch to 2D overlay for text
        arrow = Arrow(LEFT * 2, RIGHT * 2, buff=0.1, color=WHITE).shift(DOWN * 2.5)
        t_today = Text("Hôm nay (Hàm số)", font_size=24, color=C_PRIMARY).next_to(arrow, LEFT)
        t_tomorrow = Text("Ngày mai (Hàm số)", font_size=24, color=C_CONTINUOUS).next_to(arrow, RIGHT)
        mapping_text = Text("Mapping: Hàm → Hàm", font_size=28, color=C_ACCENT).next_to(arrow, UP)
        
        overlay_group = VGroup(arrow, t_today, t_tomorrow, mapping_text)
        self.add_fixed_in_frame_mobjects(overlay_group)
        
        self.play(Create(arrow), FadeIn(t_today), FadeIn(t_tomorrow), run_time=2.0)
        self.play(Write(mapping_text), run_time=2.0)
        
        # Wait out the rest of Beat 1 (30 - 16 = 14s)
        self.wait(14.0)
        
        # ============================================================
        # BEAT 2 [4:30 - 4:50] (20.0s): Địa chấn & Khí động học
        # ============================================================
        # VO: "Địa chấn học: trường vận tốc ba chiều a(x) mô tả sóng..."
        
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(globe), FadeOut(temp_layer), FadeOut(wind_layer), FadeOut(pressure_layer),
            FadeOut(overlay_group),
            run_time=2.0
        )
        
        # 3D Seismic block
        seismic_block = Prism(dimensions=[3, 3, 2]).set_color(C_SECONDARY).set_opacity(0.5)
        seismic_wave = Surface(
            lambda u, v: np.array([u, v, 0.5 * np.sin(np.sqrt(u**2 + v**2) * 3)]),
            u_range=[-1.5, 1.5], v_range=[-1.5, 1.5],
            resolution=(15, 15)
        ).set_color(C_CONTINUOUS).set_opacity(0.8)
        
        self.play(Create(seismic_block), run_time=2.0)
        self.play(Create(seismic_wave), run_time=3.0)
        self.wait(2.0)
        
        # Transform to Aerodynamics Geometry
        aero_surface = Surface(
            lambda u, v: np.array([u, v, 0.3 * np.cos(u) * np.sin(v)]),
            u_range=[-2, 2], v_range=[-2, 2]
        ).set_color(C_PRIMARY).set_opacity(0.7)
        
        self.play(
            Transform(seismic_block, aero_surface),
            FadeOut(seismic_wave),
            run_time=3.0
        )
        # Wait out the rest of Beat 2 (20 - 12 = 8s)
        self.wait(8.0)
        
        # ============================================================
        # BEAT 3 [4:50 - 5:00] (10.0s): Động lực học phân tử & Điểm chung
        # ============================================================
        # VO: "Động lực học phân tử: nguyên tử chuyển động liên tục..."
        
        self.play(FadeOut(seismic_block), run_time=1.5)
        
        # Continuous particle trajectory
        trajectory = ParametricFunction(
            lambda t: np.array([
                1.5 * np.sin(3 * t) * np.cos(t),
                1.5 * np.sin(3 * t) * np.sin(t),
                1.5 * np.cos(3 * t)
            ]),
            t_range=[0, PI],
            color=C_CONTINUOUS
        )
        
        # Checklist Text Overlay
        check_1 = Text("1. Input = Hàm số", font_size=24, color=WHITE)
        check_2 = Text("2. Output = Hàm số", font_size=24, color=WHITE)
        check_3 = Text("3. Ràng buộc vật lý liên tục", font_size=24, color=C_ACCENT)
        checklist = VGroup(check_1, check_2, check_3).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        self.add_fixed_in_frame_mobjects(checklist)
        
        self.play(Create(trajectory), run_time=2.0)
        self.play(
            FadeIn(check_1, shift=RIGHT),
            FadeIn(check_2, shift=RIGHT),
            FadeIn(check_3, shift=RIGHT),
            lag_ratio=0.3,
            run_time=2.5
        )
        
        # Wait out the rest of Beat 3 (10 - 6.0 = 4.0s)
        self.wait(4.0)
        
        # Final cleanup transition
        self.play(FadeOut(trajectory), FadeOut(checklist), run_time=1.0)


class Scene2_2_ImageIsNotFunction(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1: Bẫy ma trận rời rạc
        # ============================================================
        title = Text("Ảnh Số ≠ Hàm Số", font_size=40, color=C_WARNING).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Lưới pixel 8x8 (Đại diện cho ảnh số rời rạc)
        # Sử dụng seed để màu random được cố định giữa các lần render
        np.random.seed(42) 
        grid_8 = VGroup(*[
            Square(side_length=0.4).set_fill(C_MATRIX, opacity=0.2 + 0.8 * np.random.rand()).set_stroke(WHITE, 1) 
            for _ in range(64)
        ])
        grid_8.arrange_in_grid(8, 8, buff=0)
        grid_8.move_to(LEFT * 3)

        self.play(FadeIn(grid_8, shift=UP), run_time=1.5)
        
        brace_8 = Brace(grid_8, DOWN)
        label_8 = brace_8.get_text("Ma trận 8x8 (Rời rạc)").set_color(C_DISCRETE)
        self.play(Create(brace_8), Write(label_8), run_time=1.5)
        self.wait(1.5)

        # ============================================================
        # BEAT 2: Giới hạn của độ phân giải
        # ============================================================
        # Transform thành lưới 16x16
        grid_16 = VGroup(*[
            Square(side_length=0.2).set_fill(C_MATRIX, opacity=0.2 + 0.8 * np.random.rand()).set_stroke(WHITE, 0.5) 
            for _ in range(256)
        ])
        grid_16.arrange_in_grid(16, 16, buff=0)
        grid_16.move_to(grid_8)

        label_16 = Text("Ma trận 16x16\n(Sai lệch Input!)", font_size=24, color=C_WARNING).next_to(grid_16, DOWN, buff=0.5)

        self.play(
            Transform(grid_8, grid_16),
            Transform(label_8, label_16),
            FadeOut(brace_8),
            run_time=2.0
        )

        # Khối Standard CNN bị gãy
        cnn_box = Rectangle(width=3.5, height=2, color=C_SECONDARY).set_fill(C_SECONDARY, 0.2)
        cnn_text = Text("Standard CNN\n(Cố định Input)", font_size=24, color=WHITE).move_to(cnn_box)
        cnn_group = VGroup(cnn_box, cnn_text).next_to(grid_16, RIGHT, buff=2)

        arrow = Arrow(grid_16.get_right(), cnn_box.get_left(), color=WHITE, buff=0.2)
        cross = Cross(arrow, stroke_color=C_WARNING, stroke_width=8, scale_factor=0.6)

        self.play(Create(cnn_group), Create(arrow), run_time=1.5)
        self.play(Create(cross), run_time=1.0)
        self.wait(2.0)

        # ============================================================
        # BEAT 3: Sự tự do của hàm số liên tục
        # ============================================================
        # Dọn dẹp màn hình
        self.play(
            FadeOut(grid_8), FadeOut(label_8), 
            FadeOut(cnn_group), FadeOut(arrow), FadeOut(cross), 
            FadeOut(title),
            run_time=1.5
        )

        continuous_title = Text("Hàm Số (Liên Tục)", font_size=40, color=C_CONTINUOUS).to_edge(UP)
        
        # Vẽ đồ thị hàm số
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-1.5, 1.5, 1], 
            x_length=8, 
            y_length=4,
            axis_config={"color": GREY}
        )
        
        # Một hàm sóng mượt mà
        func = axes.plot(lambda x: np.sin(2 * x) * np.exp(-0.1 * x**2), color=C_CONTINUOUS, stroke_width=4)
        func_label = MathTex(r"f(x) \in \mathcal{A}", color=C_CONTINUOUS).next_to(func, UP, buff=0.5)

        self.play(Write(continuous_title), Create(axes), run_time=1.5)
        self.play(Create(func), Write(func_label), run_time=2.0)

        # Sampling ở độ phân giải thấp (Low Res)
        x_vals_low = np.linspace(-3, 3, 9)
        dots_low = VGroup(*[
            Dot(axes.c2p(x, np.sin(2 * x) * np.exp(-0.1 * x**2)), color=C_ACCENT, radius=0.08) 
            for x in x_vals_low
        ])
        
        # Cột lấy mẫu (Stems)
        stems_low = VGroup(*[
            DashedLine(axes.c2p(x, 0), axes.c2p(x, np.sin(2 * x) * np.exp(-0.1 * x**2)), color=C_ACCENT, stroke_opacity=0.5)
            for x in x_vals_low
        ])

        self.play(Create(stems_low), Create(dots_low), run_time=1.5)
        self.wait(1.0)

        # Sampling ở độ phân giải cao (High Res)
        x_vals_high = np.linspace(-3, 3, 45)
        dots_high = VGroup(*[
            Dot(axes.c2p(x, np.sin(2 * x) * np.exp(-0.1 * x**2)), color=C_PRIMARY, radius=0.04) 
            for x in x_vals_high
        ])
        
        self.play(
            Transform(dots_low, dots_high),
            FadeOut(stems_low),
            run_time=2.0
        )
        
        # Kết luận
        conclusion = Text("Bất biến với độ phân giải (Resolution-Invariant)", font_size=28, color=C_SECONDARY).next_to(axes, DOWN, buff=0.5)
        
        # Highlight đường cong gốc không thay đổi dù điểm lấy mẫu dày đặc
        self.play(Write(conclusion), func.animate.set_stroke(width=8, color=C_SECONDARY), run_time=1.5)
        self.wait(3.0)
        

import numpy as np
from manim import *

# ==========================================
# COLOR PALETTE (ICML Guidelines)
# ==========================================
C_PRIMARY = "#58C4DD"     # TEAL/BLUE (Lạnh)
C_SECONDARY = "#83C167"   # GREEN
C_ACCENT = "#FFFF00"      # YELLOW
C_WARNING = "#FF6666"     # RED (Nóng)
C_BACKGROUND = "#1C1C1C"  # DARK GREY

C_DISCRETE = "#FC6255"    # RED_C
C_CONTINUOUS = "#9A72AC"  # PURPLE_C

class Scene2_2_ImageIsNotFunction(Scene): # Kế thừa Scene cơ bản, không dùng MovingCameraScene nữa
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [5:00 - 5:25] (25.0s): Heatmap & Bản chất lấy mẫu
        # ============================================================
        
        grid_size = 30
        square_size = 0.15
        heatmap = VGroup()
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i - grid_size/2) * 0.2
                y = (j - grid_size/2) * 0.2
                val = (np.sin(x) + np.cos(y) + 2) / 4.0 
                val = max(0, min(1, val))
                
                # Bọc ManimColor() để tránh lỗi nội suy
                color = interpolate_color(ManimColor(C_PRIMARY), ManimColor(C_WARNING), val)
                sq = Square(side_length=square_size).set_fill(color, opacity=1).set_stroke(width=0)
                sq.move_to(RIGHT * x * 0.75 + UP * y * 0.75)
                heatmap.add(sq)
                
        heatmap.center()
        
        # Text "ẢNH" xuất hiện bình thường (sẽ tự đứng yên vì Camera không di chuyển)
        title_text = Text("ẢNH", font_size=48, color=WHITE).to_corner(UL)
        
        self.play(FadeIn(heatmap), Write(title_text), run_time=2.0)
        self.wait(3.0)
        
        # 2. ZOOM VÀO: Bằng cách phóng to và di chuyển chính heatmap thay vì camera
        target_square = heatmap[grid_size * 5 + 5] 
        target_point = target_square.get_center()
        zoom_factor = 6.0
        
        self.play(
            heatmap.animate.scale(zoom_factor, about_point=target_point).shift(ORIGIN - target_point),
            run_time=3.0
        )

        # 3. Lộ rõ các ô màu/pixel rời rạc (Hiện viền trắng)
        # Phóng to heatmap lên 6 lần nên viền cũng cần điều chỉnh độ dày tương ứng
        self.play(
            heatmap.animate.set_stroke(color=WHITE, width=2.0),
            run_time=1.5
        )
        self.wait(2.0)
        
        # 4. Gạch chéo chữ "ẢNH", hiện chữ "HÀM SỐ LẤY MẪU"
        cross_line = Line(title_text.get_left(), title_text.get_right(), color=C_WARNING, stroke_width=4)
        
        self.play(Create(cross_line), run_time=0.5)
        self.wait(1.0)
        
        sampled_text = Text("HÀM SỐ LẤY MẪU", font_size=40, color=C_ACCENT).next_to(title_text, RIGHT, buff=0.5)
        
        self.play(Write(sampled_text), run_time=1.5)
        
        self.wait(10.4)

        # ============================================================
        # BEAT 2 [5:25 - 5:40] (15.0s): Cảnh báo giới hạn lưới
        # ============================================================
        
        # 1. ZOOM OUT: Thu nhỏ heatmap về lại ban đầu
        self.play(
            heatmap.animate.scale(1/zoom_factor, about_point=ORIGIN).move_to(ORIGIN),
            run_time=2.0
        )
        
        # 2. Heatmap bị ép vào lưới (Đóng khung rào chắn)
        barrier_box = SurroundingRectangle(heatmap, color=C_WARNING, stroke_width=6, buff=0)
        grid_label = Text("Lưới 64x64", font_size=24, color=C_WARNING).next_to(barrier_box, UP)
        
        self.play(
            Create(barrier_box), FadeIn(grid_label),
            heatmap.animate.set_opacity(0.4), 
            run_time=1.5
        )
        
        # 3. CNN và Dấu chặn
        cnn_box = Rectangle(width=2.5, height=1.5, color=C_SECONDARY).set_fill(C_SECONDARY, 0.2)
        cnn_text = Text("Standard\nCNN", font_size=24, color=WHITE).move_to(cnn_box)
        cnn_group = VGroup(cnn_box, cnn_text).next_to(barrier_box, RIGHT, buff=1.5)
        
        arrow = Arrow(barrier_box.get_right(), cnn_box.get_left(), color=WHITE, buff=0.1)
        red_block = Cross(arrow, stroke_color=C_WARNING, stroke_width=8, scale_factor=0.6)
        
        self.play(Create(cnn_group), Create(arrow), run_time=1.5)
        self.play(Create(red_block), run_time=0.5)
        
        # 4. Text Overlay: Ném đi bản chất liên tục -> Bị ràng buộc lưới
        warning_group = VGroup(
            Text("Ném đi bản chất liên tục", font_size=28, color=WHITE),
            Text("↓", font_size=32, color=WHITE),
            Text("BỊ RÀNG BUỘC LƯỚI", font_size=32, color=C_WARNING)
        ).arrange(DOWN, buff=0.2).to_corner(DL)
        
        self.play(FadeIn(warning_group, shift=UP), run_time=1.5)
        
        # tạo hiệu ứng rung lắc 
        self.play(Wiggle(warning_group), run_time=1.0)
        
        self.wait(7.0)


class Scene2_3_DLvsOperator(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [5:40 - 6:10] (30.0s): Màn hình chia đôi
        # ============================================================
        
        # Đường chia đôi màn hình
        split_line = DashedLine(UP * 4, DOWN * 4, color=GREY, dash_length=0.1)
        self.play(Create(split_line), run_time=1.0)
        
        # --- NỬA TRÁI: DEEP LEARNING TRUYỀN THỐNG ---
        left_title = Text("Deep Learning Cổ Điển", font_size=28, color=C_DISCRETE).move_to(LEFT * 3.5 + UP * 3)
        left_formula = MathTex(r"f_\theta : \mathbb{R}^n \rightarrow \mathbb{R}^m", font_size=36).next_to(left_title, DOWN, buff=0.5)
        
        # Trực quan hóa vector rời rạc
        vec_in = Matrix([["x_1"], ["x_2"], [r"\vdots"], ["x_n"]], element_alignment_corner=UP).scale(0.7)
        vec_in.get_brackets().set_color(WHITE)
        vec_out = Matrix([["y_1"], ["y_2"], [r"\vdots"], ["y_m"]], element_alignment_corner=UP).scale(0.7)
        vec_out.get_brackets().set_color(WHITE)
        
        vec_group = VGroup(vec_in, Arrow(LEFT, RIGHT, color=WHITE, buff=0.2), vec_out).arrange(RIGHT, buff=0.5)
        vec_group.next_to(left_formula, DOWN, buff=1.0)
        
        self.play(Write(left_title), run_time=1.0)
        self.play(Write(left_formula), run_time=1.5)
        self.play(FadeIn(vec_group, shift=UP), run_time=2.0)
        
        # --- NỬA PHẢI: OPERATOR LEARNING ---
        right_title = Text("Operator Learning", font_size=28, color=C_CONTINUOUS).move_to(RIGHT * 3.5 + UP * 3)
        right_formula = MathTex(r"\mathcal{G}_\theta : \mathcal{A} \rightarrow \mathcal{U}", font_size=36).next_to(right_title, DOWN, buff=0.5)
        
        # Trực quan hóa hàm số liên tục
        ax_in = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=2, y_length=1.5).set_opacity(0.5)
        curve_in = ax_in.plot(lambda x: np.sin(2*x)*np.exp(-0.2*x), color=C_PRIMARY)
        graph_in = VGroup(ax_in, curve_in)
        
        ax_out = Axes(x_range=[0, 3], y_range=[-1, 1], x_length=2, y_length=1.5).set_opacity(0.5)
        curve_out = ax_out.plot(lambda x: 0.5*np.cos(3*x) + 0.2*x, color=C_CONTINUOUS)
        graph_out = VGroup(ax_out, curve_out)
        
        func_group = VGroup(graph_in, Arrow(LEFT, RIGHT, color=WHITE, buff=0.2), graph_out).arrange(RIGHT, buff=0.3)
        func_group.next_to(right_formula, DOWN, buff=1.0)
        
        self.play(Write(right_title), run_time=1.0)
        self.play(Write(right_formula), run_time=1.5)
        self.play(Create(func_group), run_time=2.0)
        
        # Đợi đồng bộ hóa (30s - 10s = 20s)
        self.wait(20.0)
        
        # ============================================================
        # BEAT 2 [6:10 - 6:40] (30.0s): Darcy Flow Equation
        # ============================================================
        
        # Xóa màn hình chia đôi
        self.play(
            FadeOut(split_line), 
            FadeOut(left_title), FadeOut(left_formula), FadeOut(vec_group),
            FadeOut(right_title), FadeOut(right_formula), FadeOut(func_group),
            run_time=1.5
        )
        
        # Xuất hiện phương trình Darcy Flow
        # -nabla \cdot (a(x) \nabla u(x)) = f(x)
        darcy_eq = MathTex(
            r"-\nabla \cdot (", 
            r"a(x)", 
            r"\nabla ", 
            r"u(x)", 
            r") = f(x)", 
            font_size=56
        )
        
        self.play(Write(darcy_eq), run_time=2.5)
        self.wait(1.0)
        
        # Highlight a(x) và u(x)
        self.play(darcy_eq[1].animate.set_color(C_PRIMARY), run_time=1.0)   # a(x) -> Teal
        self.play(darcy_eq[3].animate.set_color(C_CONTINUOUS), run_time=1.0) # u(x) -> Purple
        self.wait(1.0)
        
        # Tách hai hàm ra để thể hiện ánh xạ
        func_a = MathTex(r"a(x) \in \mathcal{A}", font_size=40, color=C_PRIMARY).move_to(LEFT * 3 + DOWN * 1.5)
        func_u = MathTex(r"u(x) \in \mathcal{U}", font_size=40, color=C_CONTINUOUS).move_to(RIGHT * 3 + DOWN * 1.5)
        
        # Mũi tên ánh xạ G
        op_arrow = CurvedArrow(func_a.get_top() + UP*0.2, func_u.get_top() + UP*0.2, angle=-PI/3, color=WHITE)
        op_label = MathTex(r"\mathcal{G}_\theta", font_size=36, color=C_ACCENT).next_to(op_arrow, UP, buff=0.1)
        
        self.play(
            darcy_eq.animate.shift(UP * 2),
            FadeIn(func_a, shift=UP),
            FadeIn(func_u, shift=UP),
            run_time=2.0
        )
        self.play(Create(op_arrow), Write(op_label), run_time=1.5)
        
        # Box nhấn mạnh kết luận G(a) \approx u
        conclusion = MathTex(r"\mathcal{G}_\theta(a) \approx u", font_size=48, color=C_ACCENT)
        box = SurroundingRectangle(conclusion, color=C_SECONDARY, buff=0.3)
        conc_group = VGroup(conclusion, box).move_to(DOWN * 2.5)
        
        self.play(Write(conclusion), Create(box), run_time=2.0)
        
        # Đợi cho hết thời gian (30 - 13.5 = 16.5s)
        self.wait(16.5)
        
        # Dọn dẹp cảnh chuẩn bị cho Section mới
        self.play(
            FadeOut(darcy_eq), FadeOut(func_a), FadeOut(func_u), 
            FadeOut(op_arrow), FadeOut(op_label), FadeOut(conc_group),
            run_time=1.5
        )



class Scene2_4_ChallengesAndDefinition(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [6:40 - 7:00] (20.0s): Hai thách thức
        # ============================================================
        
        # 1. Thách thức 1: Discretization Invariance
        # Tạo lưới vuông cơ bản
        grid_square = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": C_MATRIX, "stroke_width": 2, "stroke_opacity": 0.5}
        )
        
        # Tạo lưới bất quy tắc (bằng cách warp lưới vuông)
        grid_irregular = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": C_WARNING, "stroke_width": 2, "stroke_opacity": 0.5}
        ).apply_function(lambda p: p + np.array([0.3 * np.sin(p[1]), 0.3 * np.cos(p[0]), 0]))
        
        # Tạo lưới mịn
        grid_smooth = NumberPlane(
            x_range=[-6, 6, 0.25], y_range=[-4, 4, 0.25],
            background_line_style={"stroke_color": C_PRIMARY, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        
        self.play(Create(grid_square), run_time=1.5)
        self.play(Transform(grid_square, grid_irregular), run_time=1.5)
        self.play(Transform(grid_square, grid_smooth), run_time=1.5)
        
        question_mark = Text("?", font_size=96, color=C_ACCENT).move_to(ORIGIN)
        text_inv = Text("Discretization Invariance", font_size=40, color=C_ACCENT)
        box_inv = SurroundingRectangle(text_inv, color=C_ACCENT, buff=0.3).set_fill(C_BACKGROUND, 0.8)
        group_inv = VGroup(box_inv, text_inv)
        
        self.play(FadeIn(question_mark, scale=0.5), run_time=0.5)
        self.play(Flash(question_mark, color=C_ACCENT, line_length=0.5), run_time=0.5)
        self.play(Transform(question_mark, group_inv), run_time=1.0)
        self.wait(1.5)
        
        # 2. Thách thức 2: Continuous Query
        self.play(FadeOut(grid_square), FadeOut(question_mark), run_time=1.0)
        
        curve = ParametricFunction(
            lambda t: np.array([t, 1.5 * np.sin(t) * np.exp(-0.1 * t**2), 0]),
            t_range=[-5, 5], color=C_CONTINUOUS, stroke_width=6
        )
        query_dot = Dot(color=C_VECTOR, radius=0.15)
        query_dot.move_to(curve.get_start())
        
        text_query = Text("Continuous Query", font_size=36, color=C_VECTOR).next_to(query_dot, UP)
        text_query.add_updater(lambda m: m.next_to(query_dot, UP, buff=0.2))
        
        self.play(Create(curve), run_time=1.5)
        self.play(FadeIn(query_dot), FadeIn(text_query), run_time=0.5)
        
        # Chấm di chuyển dọc theo đường cong
        self.play(MoveAlongPath(query_dot, curve), run_time=4.0, rate_func=linear)
        text_query.clear_updaters()
        
        # Buffer cho hết 20s Beat 1 (20 - 15.0 = 5.0s)
        self.wait(5.0)
        
        # ============================================================
        # BEAT 2 [7:00 - 7:30] (30.0s): Định nghĩa Checklist
        # ============================================================
        self.play(FadeOut(curve), FadeOut(query_dot), FadeOut(text_query), run_time=1.0)
        
        title = Text("NEURAL OPERATOR", font_size=48, color=C_PRIMARY, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)
        
        # Checklist items
        items = [
            "1. Nhận đầu vào ở mọi độ phân giải",
            "2. Truy vấn đầu ra tại bất kỳ điểm nào",
            "3. Hội tụ về giới hạn liên tục duy nhất",
            "4. Tốc độ: Nhanh hơn solver 1000x"
        ]
        
        checklist_group = VGroup()
        
        # Hàm tạo icon checkmark
        def get_checkmark():
            return VGroup(
                Line(LEFT*0.2 + UP*0.1, DOWN*0.15, color=C_SECONDARY, stroke_width=4),
                Line(DOWN*0.15, RIGHT*0.25 + UP*0.25, color=C_SECONDARY, stroke_width=4)
            )

        for i, text in enumerate(items):
            check = get_checkmark()
            item_text = Text(text, font_size=32, color=WHITE).next_to(check, RIGHT, buff=0.3)
            row = VGroup(check, item_text)
            checklist_group.add(row)
            
        checklist_group.arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(title, DOWN, buff=1.0)
        
        # Animation hiện từng mục checklist
        for row in checklist_group:
            self.play(Create(row[0]), FadeIn(row[1], shift=RIGHT), run_time=0.8)
            self.wait(0.2)
        
        # Buffer hold cho đến hết section (30s - 2s(title) - 4s(items) = 24s)
        self.wait(24.0)