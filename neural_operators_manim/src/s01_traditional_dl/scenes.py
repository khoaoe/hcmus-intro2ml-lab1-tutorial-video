import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from manim import *

class Scene1_1_Hook(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # BEAT 1: [0:00 - 0:28] -> TARGET: 28.0 seconds
        # Speaker: "Trong Deep Learning truyền thống, các mô hình như MLP hay CNN..."
        # ---------------------------------------------------------
        
        # 1. Vẽ cấu trúc MLP (3.0s)
        nodes = VGroup(*[Circle(radius=0.2, color=WHITE) for _ in range(5)]).arrange(DOWN, buff=0.5)
        nodes.shift(LEFT * 3)
        self.play(Create(nodes), run_time=3.0)
        
        # 2. Đệm thời gian (5.0s)
        self.wait(5.0)
        
        # 3. Vẽ lưới dữ liệu cố định (3.0s)
        grid = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            background_line_style={"stroke_color": "#1C758A", "stroke_width": 2} # CYAN-ish
        ).scale(0.8).shift(RIGHT * 3)
        self.play(Create(grid), run_time=3.0)
        
        # 4. Đệm thời gian chờ hết Beat (17.0s)
        # TỔNG BEAT 1 = 3 + 5 + 3 + 17 = 28.0s
        self.wait(17.0)

        # ---------------------------------------------------------
        # BEAT 2: [0:28 - 0:45] -> TARGET: 17.0 seconds
        # Speaker: "Hoặc chuỗi dữ liệu là các vector có độ dài định trước..."
        # ---------------------------------------------------------
        
        # 1. Lưới thay đổi kích thước đột ngột (2.0s)
        self.play(grid.animate.scale(1.5), run_time=2.0)
        
        # 2. MLP chuyển đỏ thể hiện sự sụp đổ (2.0s)
        self.play(nodes.animate.set_color("#FC6255"), run_time=2.0) # RED
        
        # 3. Đệm thời gian chờ hết Beat 2 (13.0s)
        # TỔNG BEAT 2 = 2 + 2 + 13 = 17.0s
        self.wait(13.0)
        
        # Cleanup cuối Scene (không tính vào thời lượng đọc, hoặc có thể nối tiếp)
        self.play(FadeOut(nodes), FadeOut(grid), run_time=1.0)


class Scene1_2_PlotTwist(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # BEAT 1: [0:45 - 1:00] -> TARGET: 15.0 seconds
        # Speaker: "Nhưng hãy nhìn ra thế giới khoa học tự nhiên..."
        # ---------------------------------------------------------
        
        # 1. Tạo trục tọa độ vật lý (3.0s)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": WHITE}
        )
        self.play(Create(axes), run_time=3.0)
        
        # 2. Đệm thời gian (12.0s)
        # TỔNG BEAT 1 = 3 + 12 = 15.0s
        self.wait(12.0)

        # ---------------------------------------------------------
        # BEAT 2: [1:00 - 1:25] -> TARGET: 25.0 seconds
        # Speaker: "Vận tốc gió, sự lan truyền nhiệt của một ngọn lửa..."
        # ---------------------------------------------------------
        
        # 1. Vẽ hàm số liên tục trơn tru (4.0s)
        func = axes.plot(lambda x: np.sin(x) * np.exp(-0.1 * x), color="#FFFF00") # YELLOW
        self.play(Create(func), run_time=4.0)
        
        # 2. Đệm thời gian (21.0s)
        # TỔNG BEAT 2 = 4 + 21 = 25.0s
        self.wait(21.0)

        # ---------------------------------------------------------
        # BEAT 3: [1:25 - 1:45] -> TARGET: 20.0 seconds
        # Speaker: "Chúng là các hàm số tồn tại trong không gian vật lý..."
        # ---------------------------------------------------------
        
        # 1. Hiện công thức bản chất dữ liệu (2.0s)
        equation = MathTex(r"Data \equiv u(x, t)", font_size=60, color="#83C167") # GREEN_C
        equation.to_edge(UP)
        self.play(Write(equation), run_time=2.0)
        
        # 2. Hiệu ứng nhấn mạnh (2.0s)
        self.play(Indicate(equation, scale_factor=1.2), run_time=2.0)
        
        # 3. Đệm thời gian (16.0s)
        # TỔNG BEAT 3 = 2 + 2 + 16 = 20.0s
        self.wait(16.0)

class Scene1_3_GridMismatch(Scene):
    def construct(self):
        # Thiết lập màu sắc nội bộ để tránh lỗi import
        CONTINUOUS_YELLOW = "#FFFF00"
        GRID_GRAY = "#888888"
        GRID_WHITE = "#FFFFFF"
        ERROR_RED = "#FC6255"

        # ---------------------------------------------------------
        # BEAT 1: [1:45 - 2:00] -> TARGET: 15.0 seconds
        # Speaker: "Sự sai lệch lưới là một vấn đề lớn. Hãy tưởng tượng bạn đang rời rạc hóa..."
        # ---------------------------------------------------------
        
        # 1. Vẽ trục và hàm số (3.0s)
        axes = Axes(x_range=[0, 6, 1], y_range=[-1, 2, 1], x_length=6, y_length=3).shift(UP*1.5)
        curve = axes.plot(lambda x: np.sin(x) * np.exp(-0.2*x) + 0.5, color=CONTINUOUS_YELLOW)
        self.play(Create(axes), Create(curve), run_time=3.0)
        
        # 2. Lấy mẫu lưới thô (5 điểm) (3.0s)
        x_vals_coarse = [0.5, 1.5, 2.5, 4.0, 5.5]
        dots_coarse = VGroup(*[Dot(axes.c2p(x, curve.underlying_function(x)), color=GRID_GRAY) for x in x_vals_coarse])
        self.play(FadeIn(dots_coarse, scale=0.5), run_time=3.0)
        
        # 3. Đệm thời gian (9.0s)
        # TỔNG BEAT 1 = 3 + 3 + 9 = 15.0s
        self.wait(9.0)

        # ---------------------------------------------------------
        # BEAT 2: [2:00 - 2:15] -> TARGET: 15.0 seconds
        # Speaker: "Nếu bạn huấn luyện một mạng nơ-ron, chẳng hạn để dự báo thời tiết..."
        # ---------------------------------------------------------
        
        # 1. Vẽ mạng MLP tương ứng lưới thô (4.0s)
        mlp_nodes = VGroup(*[Circle(radius=0.15, color=WHITE, fill_opacity=1) for _ in range(5)]).arrange(RIGHT, buff=0.8).shift(DOWN*2)
        lines = VGroup(*[Line(mlp_nodes[i].get_top(), dots_coarse[i].get_bottom(), color=WHITE, stroke_opacity=0.5) for i in range(5)])
        self.play(Create(mlp_nodes), Create(lines), run_time=4.0)
        
        # 2. Đệm thời gian (11.0s)
        # TỔNG BEAT 2 = 4 + 11 = 15.0s
        self.wait(11.0)

        # ---------------------------------------------------------
        # BEAT 3: [2:15 - 2:30] -> TARGET: 15.0 seconds
        # Speaker: "...bạn không thể ép nó chạy trên lưới độ phân giải cao..."
        # ---------------------------------------------------------
        
        # 1. Chuyển sang lưới mịn (nhiều điểm hơn) (3.0s)
        x_vals_fine = np.linspace(0.2, 5.8, 20)
        dots_fine = VGroup(*[Dot(axes.c2p(x, curve.underlying_function(x)), color=GRID_WHITE, radius=0.06) for x in x_vals_fine])
        self.play(Transform(dots_coarse, dots_fine), run_time=3.0)
        
        # 2. MLP lỗi và đứt gãy (2.0s)
        self.play(
            mlp_nodes.animate.set_color(ERROR_RED),
            lines.animate.set_color(ERROR_RED).set_opacity(0.2),
            run_time=2.0
        )
        
        # 3. Đệm thời gian (10.0s)
        # TỔNG BEAT 3 = 3 + 2 + 10 = 15.0s
        self.wait(10.0)


class Scene1_4_1_5_SolutionsAndTeaser(Scene):
    def construct(self):
        # Màu nội bộ
        INPUT_CYAN = "#00FFFF"
        OUTPUT_PURPLE = "#9B59B6"
        
        # ---------------------------------------------------------
        # SCENE 1.4 - BEAT 1: [2:30 - 2:50] -> TARGET: 20.0 seconds
        # Speaker: "Để giải quyết, khoa học dùng các bộ giải PDE truyền thống..."
        # ---------------------------------------------------------
        
        # 1. Hiện phương trình PDE (4.0s)
        pde_eq = MathTex(r"\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u}", font_size=40)
        box = SurroundingRectangle(pde_eq, color=BLUE, buff=0.5)
        pde_group = VGroup(box, pde_eq).shift(UP)
        self.play(Write(pde_eq), Create(box), run_time=4.0)
        
        # 2. Đệm thời gian (16.0s)
        # TỔNG BEAT 1 = 4 + 16 = 20.0s
        self.wait(16.0)

        # ---------------------------------------------------------
        # SCENE 1.4 - BEAT 2: [2:50 - 3:10] -> TARGET: 20.0 seconds
        # Speaker: "...nhưng chúng cực kỳ chậm chạp. Bạn phải chia lưới không gian..."
        # ---------------------------------------------------------
        
        # 1. Hiện lưới chia nhỏ tốn kém và bánh răng chậm chạp (4.0s)
        grid = NumberPlane(x_range=[-3,3,0.2], y_range=[-1,1,0.2], background_line_style={"stroke_opacity": 0.3}).shift(DOWN*2)
        gear = RegularPolygon(n=8, color=GRAY).scale(0.5).shift(DOWN*2)
        self.play(FadeIn(grid), Rotate(gear, angle=PI/2, run_time=4.0, rate_func=linear))
        
        # 2. Đệm thời gian (16.0s)
        # TỔNG BEAT 2 = 4 + 16 = 20.0s
        self.wait(16.0)

        # ---------------------------------------------------------
        # SCENE 1.4 - BEAT 3: [3:10 - 3:30] -> TARGET: 20.0 seconds
        # Speaker: "Hơn nữa, mỗi khi thay đổi một điều kiện ban đầu dù là nhỏ nhất..."
        # ---------------------------------------------------------
        
        # 1. Thêm điều kiện ban đầu và hiệu ứng Reset (4.0s)
        ic_text = MathTex(r"u(x, 0) = u_0(x)", color=YELLOW).next_to(box, UP)
        self.play(Write(ic_text), run_time=2.0)
        self.play(Wiggle(ic_text), Flash(ic_text), run_time=2.0)
        
        # 2. Xóa và reset lại (2.0s)
        self.play(FadeOut(grid), FadeOut(gear), run_time=2.0)
        
        # 3. Đệm thời gian (14.0s)
        # TỔNG BEAT 3 = 2 + 2 + 2 + 14 = 20.0s
        self.wait(14.0)

        # Clear cho Scene tiếp theo
        self.play(FadeOut(pde_group), FadeOut(ic_text), run_time=1.0)
        self.wait(0.5) # Bù trừ nội bộ, không tính vào tổng do chuyển cảnh

        # ---------------------------------------------------------
        # SCENE 1.5 - BEAT 1: [3:30 - 3:45] -> TARGET: 15.0 seconds
        # Speaker: "Vậy câu hỏi then chốt là: Liệu một mạng nơ-ron có thể học..."
        # ---------------------------------------------------------
        
        # 1. Vẽ a(x) và u(x) với mũi tên ánh xạ (4.0s)
        ax_in = Axes(x_range=[0, 2, 1], y_range=[0, 2, 1], x_length=2, y_length=2).shift(LEFT*3.5)
        curve_in = ax_in.plot(lambda x: 0.5*x**2 + 0.2, color=INPUT_CYAN)
        label_in = MathTex("a(x)", color=INPUT_CYAN).next_to(ax_in, DOWN)
        
        ax_out = Axes(x_range=[0, 2, 1], y_range=[0, 2, 1], x_length=2, y_length=2).shift(RIGHT*3.5)
        curve_out = ax_out.plot(lambda x: 1.5 - 0.3*x**2, color=OUTPUT_PURPLE)
        label_out = MathTex("u(x)", color=OUTPUT_PURPLE).next_to(ax_out, DOWN)
        
        arrow_op = Arrow(start=LEFT, end=RIGHT, color=WHITE).scale(2)
        op_label = Tex("Operator Learning").next_to(arrow_op, UP)

        self.play(
            Create(ax_in), Create(curve_in), Write(label_in),
            Create(ax_out), Create(curve_out), Write(label_out),
            run_time=3.0
        )
        self.play(GrowArrow(arrow_op), Write(op_label), run_time=1.0)
        
        # 2. Đệm thời gian (11.0s)
        # TỔNG BEAT 1 = 3 + 1 + 11 = 15.0s
        self.wait(11.0)

        # ---------------------------------------------------------
        # SCENE 1.5 - BEAT 2: [3:45 - 3:55] -> TARGET: 10.0 seconds
        # Speaker: "...bất chấp mọi độ phân giải lưới?"
        # ---------------------------------------------------------
        
        # 1. Lưới nhấp nháy chuyển độ phân giải (4.0s)
        dots_in_coarse = VGroup(*[Dot(ax_in.c2p(x, curve_in.underlying_function(x)), radius=0.08) for x in np.linspace(0, 2, 4)])
        dots_in_fine = VGroup(*[Dot(ax_in.c2p(x, curve_in.underlying_function(x)), radius=0.04) for x in np.linspace(0, 2, 12)])
        
        self.play(FadeIn(dots_in_coarse), run_time=1.0)
        self.play(Transform(dots_in_coarse, dots_in_fine), Indicate(arrow_op, color=YELLOW), run_time=3.0)
        
        # 2. Đệm thời gian (6.0s)
        # TỔNG BEAT 2 = 1 + 3 + 6 = 10.0s
        self.wait(6.0)

        # ---------------------------------------------------------
        # SCENE 1.5 - BEAT 3: [3:55 - 4:00] -> TARGET: 5.0 seconds
        # Speaker: "Chào mừng bạn đến với Neural Operators."
        # ---------------------------------------------------------
        
        # 1. Biến đổi thành Title (2.0s)
        title = Text("NEURAL OPERATORS", font_size=60, weight=BOLD, color=YELLOW)
        self.play(
            ReplacementTransform(VGroup(ax_in, curve_in, label_in, ax_out, curve_out, label_out, arrow_op, op_label, dots_in_coarse), title),
            run_time=2.0
        )
        
        # 2. Đệm thời gian kết thúc Section (3.0s)
        # TỔNG BEAT 3 = 2 + 3 = 5.0s
        self.wait(3.0)