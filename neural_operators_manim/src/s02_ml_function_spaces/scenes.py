import sys
import os
from manim import *

# Cấu hình sys.path để import từ thư mục gốc của project
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.colors import *

class Scene2_1_ScientificData(ThreeDScene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: Khí hậu học (30.0s) | [4:00–4:30]
        # ---------------------------------------------------------
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Trái Đất (Không gian liên tục vô hạn chiều)
        globe = Sphere(radius=2.5, resolution=(40, 40)).set_color(SPHERE_DARK_BLUE).set_opacity(0.8)
        
        # BẢN VÁ: Tạo lưới bằng cách nhân bản Sphere và chỉ giữ lại stroke
        globe_mesh = Sphere(radius=2.5, resolution=(40, 40)).set_fill(opacity=0).set_stroke(color=MATH_BLUE, width=0.5, opacity=0.5)

        # 5.0s Create
        self.play(Create(globe_mesh), FadeIn(globe), run_time=5.0)

        # Fixed in frame texts
        mapping_text = Text("Ánh xạ Hàm số", font_size=36, color=TEXT_MAIN, weight=BOLD)
        mapping_math = MathTex(r"\mathcal{U}_{\text{today}} \to \mathcal{U}_{\text{tomorrow}}", font_size=48, color=FUNC_TEAL)
        mapping_group = VGroup(mapping_text, mapping_math).arrange(DOWN, buff=0.3).to_corner(UL)
        
        self.add_fixed_in_frame_mobjects(mapping_group)
        
        # 3.0s Write
        self.play(Write(mapping_group), run_time=3.0)
        
        # 22.0s Wait to complete 30.0s beat (5.0 + 3.0 + 22.0 = 30.0)
        self.wait(22.0)

        # ---------------------------------------------------------
        # Beat 2: Địa chấn & Khí động học (20.0s) | [4:30–4:50]
        # ---------------------------------------------------------
        seismic_block = Cube(side_length=3.5, fill_color=MATRIX_WEIGHT, fill_opacity=0.6, stroke_color=MATH_YELLOW)
        
        # 3.0s Transform to block
        self.play(Transform(globe, seismic_block), FadeOut(globe_mesh), run_time=3.0)
        self.wait(5.0) # Hold for seismic explanation

        # Aerodynamic surface
        aero_surface = Surface(
            lambda u, v: np.array([u, v, 0.5 * np.sin(u) * np.cos(v)]),
            u_range=[-2, 2], v_range=[-2, 2],
            fill_color=MATH_GREEN, fill_opacity=0.8, resolution=(20, 20)
        )
        
        # Tạo lưới cho mặt cong bằng cách khởi tạo lại Surface với fill_opacity=0
        aero_mesh = Surface(
            lambda u, v: np.array([u, v, 0.5 * np.sin(u) * np.cos(v)]),
            u_range=[-2, 2], v_range=[-2, 2],
            resolution=(20, 20)
        ).set_fill(opacity=0).set_stroke(color=TEXT_MAIN, width=0.5)

        # 3.0s Transform to surface
        self.play(Transform(globe, aero_surface), FadeIn(aero_mesh), run_time=3.0)
        
        # 9.0s Wait to complete 20.0s beat (3.0 + 5.0 + 3.0 + 9.0 = 20.0)
        self.wait(9.0)

        # ---------------------------------------------------------
        # Beat 3: Động lực học phân tử (10.0s) | [4:50–5:00]
        # ---------------------------------------------------------
        self.stop_ambient_camera_rotation()
        
        # 2.0s Clear 3D objects
        self.play(FadeOut(globe), FadeOut(aero_mesh), FadeOut(mapping_group), run_time=2.0)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES) # Reset to 2D view

        # Continuous trajectory
        trajectory = ParametricFunction(
            lambda t: np.array([t, 1.5 * np.sin(2*t) * np.exp(-0.1*t), 0]),
            t_range=[-4, 4], color=FUNC_TEAL, stroke_width=4
        )
        
        checklist = VGroup(
            Text("1. Input = Hàm số", font_size=28, color=TEXT_SUB),
            Text("2. Output = Hàm số", font_size=28, color=TEXT_SUB),
            Text("3. Ràng buộc vật lý liên tục", font_size=28, color=TEXT_HIGHLIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(DR)
        
        self.add_fixed_in_frame_mobjects(checklist)

        # 3.0s Draw trajectory and list
        self.play(Create(trajectory), FadeIn(checklist, shift=UP), run_time=3.0)
        
        # 5.0s Wait to complete 10.0s beat (2.0 + 3.0 + 5.0 = 10.0)
        self.wait(5.0)


class Scene2_2_NotAnImage(MovingCameraScene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: Ảo giác của Pixel (25.0s) | [5:00–5:25]
        # ---------------------------------------------------------
        # Speaker: "Có một lưu ý quan trọng: Khi hình dung một hàm số như trường nhiệt độ, 
        # ta thường vẽ nó dưới dạng ảnh màu: chỗ đỏ là nóng, chỗ xanh là lạnh. Nhưng đó không phải là ảnh. 
        # Đó là hàm số được hiển thị, được lấy mẫu tại một số điểm nhất định để ta có thể nhìn thấy."
        
        # Constructing a procedural "heatmap" using a grid to explicitly show pixels later
        grid_size = 20
        square_size = 0.3
        heatmap_group = VGroup()
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate a continuous value simulating a heatmap (radial sine wave)
                x = (i - grid_size/2) * square_size
                y = (j - grid_size/2) * square_size
                dist = np.sqrt(x**2 + y**2)
                val = np.sin(dist)
                
                # Interpolate color (Blue/Cold to Red/Hot)
                color = interpolate_color(MATH_BLUE, MATH_RED, (val + 1) / 2)
                
                # stroke_width=0 makes it look continuous at a distance
                sq = Square(side_length=square_size, fill_color=color, fill_opacity=1, stroke_width=0)
                sq.move_to(np.array([x, y, 0]))
                heatmap_group.add(sq)

        # 3.0s Fade in "continuous" heatmap
        self.play(FadeIn(heatmap_group), run_time=3.0)
        self.wait(5.0)
        
        # Define camera zoom target
        zoom_target = heatmap_group[150] # Pick a square near the center
        
        # 5.0s Strong Zoom to reveal pixels
        self.play(
            self.camera.frame.animate.scale(0.15).move_to(zoom_target.get_center()),
            run_time=5.0,
            rate_func=there_and_back_with_pause # Zoom in, pause, but wait, we want to stay zoomed.
        )
        # Fix: We want to stay zoomed in, so use default smooth rate_func
        # Overriding the play call above to stay zoomed:
        self.remove(*self.mobjects) # clear previous play state internally just in case
        self.add(heatmap_group)
        self.play(
            self.camera.frame.animate.scale(0.15).move_to(zoom_target.get_center()),
            run_time=5.0
        )

        # 2.0s Add distinct grid strokes to show discreteness
        for sq in heatmap_group:
            sq.set_stroke(color=BG_DARK, width=0.5)
        self.play(heatmap_group.animate.set_stroke(width=0.5), run_time=2.0)
        
        # Typography interactions (scaled appropriately for the zoomed camera)
        text_image = Text("ẢNH", font_size=12, color=ERROR_RED, weight=BOLD).move_to(zoom_target.get_center() + UP*0.2)
        strike_line = Line(text_image.get_left(), text_image.get_right(), color=ERROR_RED, stroke_width=1.5)
        text_function = Text("HÀM SỐ LẤY MẪU", font_size=8, color=FUNC_TEAL, weight=BOLD).move_to(text_image.get_center() + DOWN*0.15)
        
        # 4.0s Text interactions
        self.play(Write(text_image), run_time=1.0)
        self.play(Create(strike_line), run_time=1.0)
        self.play(FadeIn(text_function, shift=DOWN*0.05), run_time=2.0)
        
        # 6.0s Wait to complete 25.0s beat (3.0 + 5.0 + 5.0 + 2.0 + 4.0 + 6.0 = 25.0)
        self.wait(6.0)

        # ---------------------------------------------------------
        # Beat 2: Bị ràng buộc bởi lưới (15.0s) | [5:25–5:40]
        # ---------------------------------------------------------
        # Speaker: "Sự khác biệt này cực kỳ quan trọng. Nếu ta xử lý nó như ảnh, đưa vào CNN 
        # và train trên lưới 64x64, là ta đang ném đi bản chất liên tục của dữ liệu. 
        # Và ta bị ràng buộc trong lưới đó."

        # 3.0s Pull back slightly to show the rigid constraint
        self.play(
            self.camera.frame.animate.scale(3.0),
            FadeOut(text_image, strike_line, text_function),
            run_time=3.0
        )
        
        # Create a strict boundary barrier
        barrier_rect = Rectangle(
            width=self.camera.frame.width * 0.8, 
            height=self.camera.frame.height * 0.8, 
            color=ERROR_RED, stroke_width=4
        ).move_to(self.camera.frame.get_center())
        
        warning_text = Text(
            "BỊ RÀNG BUỘC LƯỚI", 
            font_size=16, color=ERROR_RED, weight=BOLD
        ).next_to(barrier_rect, UP, buff=0.1)

        # 3.0s Red barrier crash
        self.play(Create(barrier_rect), Write(warning_text), run_time=3.0)
        
        # Pulsing effect to highlight the constraint
        # 3.0s Pulse
        self.play(
            barrier_rect.animate.set_stroke(width=8, opacity=0.5),
            rate_func=there_and_back, run_time=1.5
        )
        self.play(
            barrier_rect.animate.set_stroke(width=8, opacity=0.5),
            rate_func=there_and_back, run_time=1.5
        )
        
        # 6.0s Wait to complete 15.0s beat (3.0 + 3.0 + 3.0 + 6.0 = 15.0s)
        self.wait(6.0)


class Scene2_3_ShiftToOperators(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: Sự dịch chuyển hệ quy chiếu (30.0s) | [5:40–6:10]
        # ---------------------------------------------------------
        # Speaker: "Để hiểu Neural Operator, ta so sánh với Deep Learning cổ điển. 
        # DL truyền thống học hàm số f_theta: R^n -> R^m – ánh xạ giữa các vector hữu hạn chiều. 
        # Operator Learning muốn học toán tử G_theta : A -> U – ánh xạ giữa các không gian hàm vô hạn chiều."

        # Setup Split Screen
        divider = Line(UP * 4, DOWN * 4, color=AXES_COLOR, stroke_width=2)
        
        # Left Side: Traditional DL (Discrete)
        dl_title = Text("Deep Learning", font_size=32, color=TEXT_MAIN).to_edge(UP).shift(LEFT * 3.5)
        dl_math = MathTex(r"f_\theta: \mathbb{R}^n \to \mathbb{R}^m", font_size=40, color=DISCRETE_BLUE).next_to(dl_title, DOWN)
        
        dots_in = VGroup(*[Dot(color=DISCRETE_BLUE) for _ in range(5)]).arrange(DOWN, buff=0.3)
        dots_out = VGroup(*[Dot(color=DISCRETE_BLUE) for _ in range(3)]).arrange(DOWN, buff=0.3)
        dots_in.shift(LEFT * 5 + DOWN * 0.5)
        dots_out.shift(LEFT * 2 + DOWN * 0.5)
        
        arrows = VGroup()
        for din in dots_in:
            for dout in dots_out:
                arrows.add(Line(din.get_center(), dout.get_center(), stroke_width=0.5, color=DISCRETE_GRID, stroke_opacity=0.5))

        # Right Side: Operator Learning (Continuous)
        op_title = Text("Neural Operators", font_size=32, color=TEXT_MAIN).to_edge(UP).shift(RIGHT * 3.5)
        op_math = MathTex(r"G_\theta : \mathcal{A} \to \mathcal{U}", font_size=40, color=CONTINUOUS_PURPLE).next_to(op_title, DOWN)
        
        ax_in = Axes(x_range=[0, 3], y_range=[-1, 2], x_length=2.5, y_length=2).shift(RIGHT * 2 + DOWN * 0.5)
        ax_out = Axes(x_range=[0, 3], y_range=[-1, 2], x_length=2.5, y_length=2).shift(RIGHT * 5 + DOWN * 0.5)
        
        func_in = ax_in.plot(lambda x: np.sin(2 * x) * np.exp(-0.2 * x), color=FUNC_TEAL)
        func_out = ax_out.plot(lambda x: np.cos(x) + 0.5, color=CONTINUOUS_PURPLE)
        op_arrow = CurvedArrow(ax_in.get_right(), ax_out.get_left(), color=NO_GOLD, angle=-TAU/4).shift(UP*0.5)

        # 5.0s Layout setup
        self.play(Create(divider), Write(dl_title), Write(op_title), run_time=2.0)
        self.play(Write(dl_math), Write(op_math), run_time=3.0)
        
        # 10.0s Draw internals
        self.play(Create(dots_in), Create(dots_out), Create(arrows), run_time=4.0)
        self.play(Create(ax_in), Create(ax_out), run_time=2.0)
        self.play(Create(func_in), Create(func_out), Create(op_arrow), run_time=4.0)

        # 15.0s Wait
        self.wait(15.0)

        # ---------------------------------------------------------
        # Beat 2: Ví dụ Darcy Flow (30.0s) | [6:10–6:40]
        # ---------------------------------------------------------
        # Speaker: "Lấy ví dụ Darcy Flow: -\nabla \cdot (a(x)\nabla u(x)) = f(x). 
        # Trong đó a(x) là hệ số khuếch tán, u(x) là nghiệm. 
        # Thay vì giải số phức tạp cho mỗi a mới, ta muốn học toán tử G sao cho G(a) ≈ u."

        # 2.0s Clear screen
        self.play(
            FadeOut(divider), FadeOut(dl_title), FadeOut(dl_math), FadeOut(dots_in), 
            FadeOut(dots_out), FadeOut(arrows), FadeOut(op_title), FadeOut(op_math),
            FadeOut(ax_in), FadeOut(ax_out), FadeOut(func_in), FadeOut(func_out), FadeOut(op_arrow),
            run_time=2.0
        )

        darcy_title = Text("Phương trình Darcy Flow", font_size=36, color=TEXT_SUB).to_edge(UP)
        # Tách chuỗi để dễ đổi màu
        eq = MathTex(
            r"-\nabla \cdot (",   # 0
            r"a(x)",              # 1
            r"\nabla ",           # 2
            r"u(x)",              # 3
            r") = f(x)",          # 4
            font_size=60
        )
        
        # 4.0s Write equation
        self.play(Write(darcy_title), Write(eq), run_time=4.0)
        
        # 4.0s Highlight variables
        self.play(eq[1].animate.set_color(MATH_BLUE), run_time=2.0) # a(x)
        self.play(eq[3].animate.set_color(CONTINUOUS_PURPLE), run_time=2.0) # u(x)

        # 4.0s Draw Operator Connection
        g_arrow = CurvedArrow(eq[1].get_bottom() + DOWN*0.2, eq[3].get_bottom() + DOWN*0.2, color=NO_GOLD, angle=TAU/3)
        g_label = MathTex(r"G_\theta", color=NO_GOLD, font_size=36).next_to(g_arrow, DOWN, buff=0.1)
        
        self.play(Create(g_arrow), Write(g_label), run_time=4.0)

        # 16.0s Wait
        self.wait(16.0)


class Scene2_4_ChallengesAndDefinition(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Beat 1: Hai thách thức toán học (20.0s) | [6:40–7:00]
        # ---------------------------------------------------------
        # Speaker: "Việc học trong không gian hàm đòi hỏi giải quyết hai thách thức. 
        # Discretization Invariance: dữ liệu đo trên lưới khác nhau, model phải hoạt động trên mọi loại lưới không cần retrain. 
        # Continuous Query: đầu ra phải là hàm thực thụ, truy vấn được tại bất kỳ điểm nào để lấy đạo hàm kiểm tra vật lý, hoặc tính tích phân đo năng lượng."

        title = Text("Hai thách thức cốt lõi", font_size=40, color=TEXT_MAIN).to_edge(UP)
        self.add(title)

        # Left side: Discretization Invariance
        inv_text = Text("1. Discretization Invariance", font_size=28, color=MATH_YELLOW).shift(LEFT*3 + UP*1.5)
        
        grid_coarse = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=3, y_length=3, background_line_style={"stroke_color": DISCRETE_GRID})
        grid_coarse.shift(LEFT*3 + DOWN*1)
        
        grid_fine = NumberPlane(x_range=[-2, 2, 0.25], y_range=[-2, 2, 0.25], x_length=3, y_length=3, background_line_style={"stroke_color": FUNC_TEAL})
        grid_fine.shift(LEFT*3 + DOWN*1)

        # 4.0s Setup Grid morphing
        self.play(Write(inv_text), Create(grid_coarse), run_time=2.0)
        self.play(Transform(grid_coarse, grid_fine), run_time=2.0)

        # Right side: Continuous Query
        query_text = Text("2. Continuous Query", font_size=28, color=MATH_YELLOW).shift(RIGHT*3 + UP*1.5)
        
        ax = Axes(x_range=[0, 4], y_range=[0, 3], x_length=4, y_length=3).shift(RIGHT*3 + DOWN*1)
        curve = ax.plot(lambda x: 1.5 + np.sin(x*1.5), color=CONTINUOUS_PURPLE)
        
        query_dot = Dot(color=TEXT_HIGHLIGHT)
        query_label = MathTex(r"u(x_i)", font_size=24, color=TEXT_HIGHLIGHT)
        query_group = VGroup(query_dot, query_label)
        
        # 5.0s Query path animation
        self.play(Write(query_text), Create(ax), Create(curve), run_time=2.0)
        
        # Use ValueTracker to slide dot smoothly
        t_val = ValueTracker(0)
        query_dot.add_updater(lambda m: m.move_to(ax.c2p(t_val.get_value(), 1.5 + np.sin(t_val.get_value()*1.5))))
        query_label.add_updater(lambda m: m.next_to(query_dot, UP+RIGHT, buff=0.1))
        
        self.add(query_dot, query_label)
        self.play(t_val.animate.set_value(4), run_time=3.0, rate_func=smooth)
        query_dot.clear_updaters()
        query_label.clear_updaters()

        # 11.0s Wait
        self.wait(11.0)

        # ---------------------------------------------------------
        # Beat 2: Bộ 4 tiêu chí tối thượng (30.0s) | [7:00–7:30]
        # ---------------------------------------------------------
        # Speaker: "Tóm lại, Neural Operator là framework thỏa mãn bốn tiêu chí: 
        # Nhận đầu vào là hàm số tại bất kỳ độ phân giải nào. Xuất đầu ra truy vấn được tại mọi điểm. 
        # Tính hội tụ: khi lưới càng mịn, mô hình hội tụ về giới hạn liên tục duy nhất. 
        # Và tốc độ: phải nhanh hơn hàng nghìn lần so với solver truyền thống. Phần tiếp theo: cấu trúc bên trong."

        # 2.0s Clear screen
        self.play(
            FadeOut(title), FadeOut(inv_text), FadeOut(grid_coarse), 
            FadeOut(query_text), FadeOut(ax), FadeOut(curve), FadeOut(query_group),
            run_time=2.0
        )

        final_title = Text("4 Tiêu Chí Của Neural Operator", font_size=40, color=NO_GOLD, weight=BOLD).to_edge(UP)
        self.play(Write(final_title), run_time=1.0)

        # Checklist creation
        checklist = VGroup(
            Text("1. Input tại mọi độ phân giải (Resolution Invariant)", font_size=28, color=TEXT_MAIN),
            Text("2. Output truy vấn tại mọi điểm (Continuous)", font_size=28, color=TEXT_MAIN),
            Text("3. Hội tụ về giới hạn liên tục duy nhất", font_size=28, color=TEXT_MAIN),
            Text("4. Nhanh hơn solver truyền thống hàng nghìn lần", font_size=28, color=TEXT_HIGHLIGHT)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(DOWN*0.5)

        # Pre-create checkmarks to the left of each item
        checkmarks = VGroup()
        for item in checklist:
            tick = MathTex(r"\checkmark", color=MATH_GREEN).next_to(item, LEFT, buff=0.3)
            checkmarks.add(tick)

        # 16.0s Draw checklist sequentially (4 items * (2s reveal + 2s wait))
        for item, tick in zip(checklist, checkmarks):
            self.play(FadeIn(item, shift=UP*0.3), Write(tick), run_time=2.0)
            self.wait(2.0)

        # 11.0s Final Wait to pad out the remaining time exactly
        self.wait(11.0)