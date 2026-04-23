import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from manim import *
from utils.colors import *

class Scene3_1_MathFoundations(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [7:30 - 7:55] (25.0s): Tích phân & Tổng Riemann
        # ============================================================
        
        # Setup Axes & Curve
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 4, 1], 
            x_length=8, y_length=4,
            axis_config={"color": GREY}
        ).shift(DOWN * 0.5)
        
        # Hàm số a(x)
        def func(x):
            return -0.3 * (x - 3)**2 + 3.2
            
        curve = axes.plot(func, color=C_PRIMARY, x_range=[0.5, 5.5])
        curve_label = MathTex("a(x)", color=C_PRIMARY).next_to(curve, UP, buff=0.2)
        
        # Phương trình Riemann -> Tích phân
        eq_riemann = MathTex(
            r"\lim_{N \to \infty} \sum_{i=1}^N", r"a(x_i) \Delta x", r"=", r"\int a(x) dx",
            font_size=42
        ).to_edge(UP, buff=0.8)
        eq_riemann[1].set_color(C_DISCRETE)    # Tổng rời rạc màu Đỏ
        eq_riemann[3].set_color(C_CONTINUOUS)  # Tích phân màu Tím
        
        self.play(Create(axes), Create(curve), FadeIn(curve_label), run_time=2.0)
        self.play(Write(eq_riemann[0:2]), run_time=2.0)
        
        # ValueTracker cho số lượng hình chữ nhật N
        N_tracker = ValueTracker(4)
        
        # Tạo Riemann Rectangles update tự động theo N_tracker
        rects = always_redraw(lambda: axes.get_riemann_rectangles(
            curve,
            x_range=[1, 5],
            dx=4.0 / int(N_tracker.get_value()),
            input_sample_type="center",
            color=[C_SECONDARY, C_PRIMARY], # Gradient mượt
            fill_opacity=0.6,
            stroke_width=1.5 if N_tracker.get_value() < 20 else 0.5
        ))
        
        self.play(FadeIn(rects), run_time=1.0)
        
        # Animate N tiến tới "vô cùng" (60 là đủ để mịn trên màn hình)
        self.play(
            N_tracker.animate.set_value(60),
            run_time=5.0,
            rate_func=smooth
        )
        self.wait(1.0)
        
        # Chuyển đổi từ các cột rời rạc thành một vùng liên tục mượt mà
        smooth_area = axes.get_area(curve, x_range=[1, 5], color=C_CONTINUOUS, opacity=0.6)
        
        self.play(
            Transform(rects, smooth_area),
            Write(eq_riemann[2:]),
            run_time=2.0
        )
        
        # Đợi đồng bộ hóa Beat 1 (25.0 - 13.0 = 12.0s)
        self.wait(12.0)
        
        # ============================================================
        # BEAT 2 [7:55 - 8:15] (20.0s): Đạo hàm & Sai phân hữu hạn
        # ============================================================
        
        # Dọn dẹp tích phân, giữ lại hệ trục và đường cong
        self.play(
            FadeOut(rects), FadeOut(smooth_area), FadeOut(eq_riemann),
            run_time=1.5
        )
        
        # Phương trình Đạo hàm Rời rạc
        eq_fd = MathTex(
            r"a'(x)", r"\approx", r"\frac{a(x+\Delta x) - a(x)}{\Delta x}",
            font_size=42
        ).to_edge(UP, buff=0.8)
        eq_fd[0].set_color(C_CONTINUOUS)
        eq_fd[2].set_color(C_ACCENT)
        
        # Setup điểm và tracker cho dx
        x0 = 1.5
        dx_tracker = ValueTracker(2.5) # Bắt đầu với khoảng cách xa
        
        # Điểm cố định
        dot_fixed = Dot(axes.c2p(x0, func(x0)), color=C_PRIMARY, radius=0.1)
        
        # Điểm di chuyển (ràng buộc vào dx_tracker)
        dot_moving = always_redraw(lambda: Dot(
            axes.c2p(x0 + dx_tracker.get_value(), func(x0 + dx_tracker.get_value())),
            color=C_WARNING, radius=0.1
        ))
        
        # Đường cát tuyến (Secant line) update liên tục tạo thành tiếp tuyến
        def get_secant_line():
            dx = dx_tracker.get_value()
            x1, y1 = x0, func(x0)
            x2, y2 = x0 + dx, func(x0 + dx)
            
            # Tránh chia cho 0
            if abs(dx) < 0.0001: dx = 0.0001
            slope = (y2 - y1) / dx
            
            # Vẽ đường thẳng dài hơn khoảng cách 2 điểm để nhìn rõ
            line_start_x = x0 - 1.5
            line_end_x = x0 + 3.5
            line_start_y = y1 + slope * (line_start_x - x0)
            line_end_y = y1 + slope * (line_end_x - x0)
            
            return Line(
                axes.c2p(line_start_x, line_start_y),
                axes.c2p(line_end_x, line_end_y),
                color=C_VECTOR, stroke_width=4
            )
            
        secant_line = always_redraw(get_secant_line)
        
        # Animations
        self.play(Write(eq_fd[2]), run_time=1.5) # Hiện vế phải sai phân
        self.play(FadeIn(dot_fixed), FadeIn(dot_moving), run_time=1.0)
        self.play(Create(secant_line), run_time=1.0)
        
        # Điểm thứ 2 trượt dần về điểm thứ nhất -> dx tiến về 0
        self.play(
            dx_tracker.animate.set_value(0.001),
            Write(eq_fd[0:2]), # Hiện vế trái (đạo hàm chính xác)
            run_time=4.0,
            rate_func=there_and_back_with_pause # Trượt về rồi dừng
        )
        # Sửa lại thành trượt về 0 hẳn
        self.play(dx_tracker.animate.set_value(0.0001), run_time=1.0)
        
        # Đợi đồng bộ hóa Beat 2 (20.0 - 10.0 = 10.0s)
        self.wait(10.0)
        
        # Clean up for next scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )


class Scene3_2_MLPToIntegralOperator(Scene):
    def construct(self):
        self.camera.background_color = C_BACKGROUND
        
        # ============================================================
        # BEAT 1 [8:15 - 8:45] (30.0s): MLP -> Integral
        # ============================================================
        
        # 1. Khởi tạo phương trình MLP
        # y_j = \sigma( \sum_{i} W_{ji} x_i + b_j )
        eq_mlp = MathTex(
            r"y_j", r"=", r"\sigma \Big(", r"\sum_i", r"W_{ji}", r"x_i", r"+", r"b_j", r"\Big)",
            font_size=48
        ).to_edge(UP, buff=1.0)
        eq_mlp[0].set_color(C_VECTOR)       # y_j
        eq_mlp[3].set_color(C_DISCRETE)     # sum
        eq_mlp[4].set_color(C_MATRIX)       # W_{ji}
        eq_mlp[5].set_color(C_VECTOR)       # x_i
        eq_mlp[7].set_color(C_SECONDARY)    # b_j
        
        self.play(Write(eq_mlp), run_time=2.0)
        
        # Khởi tạo đồ thị MLP rời rạc (Nodes & Weights)
        nodes_x = VGroup(*[Dot(radius=0.1, color=C_VECTOR).move_to(LEFT * 3 + UP * (1.5 - i)) for i in range(4)])
        nodes_y = VGroup(*[Dot(radius=0.1, color=C_VECTOR).move_to(RIGHT * 3 + UP * (1.5 - i)) for i in range(4)])
        
        edges = VGroup()
        for nx in nodes_x:
            for ny in nodes_y:
                edges.add(Line(nx.get_center(), ny.get_center(), color=C_MATRIX, stroke_opacity=0.3, stroke_width=1))
                
        mlp_graph = VGroup(edges, nodes_x, nodes_y).shift(DOWN * 0.5)
        
        self.play(FadeIn(nodes_x), FadeIn(nodes_y), run_time=1.0)
        self.play(Create(edges), run_time=2.0)
        self.wait(5.0) # VO: "Hãy nhìn MLP: tầng rời rạc..."
        
        # 2. Khởi tạo phương trình Toán tử tích phân
        # v(y) = \sigma( \int \kappa(y,x;\theta) a(x) dx + b(y) )
        eq_integral = MathTex(
            r"v(y)", r"=", r"\sigma \Big(", r"\int", r"\kappa(y,x;\theta)", r"a(x)dx", r"+", r"b(y)", r"\Big)",
            font_size=48
        ).to_edge(UP, buff=1.0)
        eq_integral[0].set_color(C_CONTINUOUS)     # v(y)
        eq_integral[3].set_color(C_PRIMARY)        # int
        eq_integral[4].set_color(C_ACCENT)         # kappa
        eq_integral[5].set_color(C_CONTINUOUS)     # a(x)dx
        eq_integral[7].set_color(C_SECONDARY)      # b(y)
        
        # 3. Khởi tạo trường liên tục đại diện cho Kernel
        domain_x = Line(LEFT * 3 + UP * 1.5, LEFT * 3 + DOWN * 1.5, color=C_CONTINUOUS, stroke_width=8)
        domain_y = Line(RIGHT * 3 + UP * 1.5, RIGHT * 3 + DOWN * 1.5, color=C_CONTINUOUS, stroke_width=8)
        
        # Kernel Area (Sử dụng khối gradient mô phỏng tích phân)
        kernel_area = Polygon(
            domain_x.get_start(), domain_x.get_end(), domain_y.get_end(), domain_y.get_start(),
            color=C_ACCENT, fill_opacity=0.3, stroke_width=0
        )
        kernel_label = MathTex(r"\kappa(y,x;\theta)", color=C_ACCENT).move_to(kernel_area)
        
        continuous_graph = VGroup(kernel_area, domain_x, domain_y, kernel_label).shift(DOWN * 0.5)
        
        # 4. Thực hiện bước nhảy vọt (Transform)
        self.play(
            Transform(eq_mlp[0], eq_integral[0]), # y_j -> v(y)
            Transform(eq_mlp[1:3], eq_integral[1:3]),
            Transform(eq_mlp[3], eq_integral[3]), # sum -> int
            Transform(eq_mlp[4], eq_integral[4]), # W_ji -> kappa
            Transform(eq_mlp[5], eq_integral[5]), # x_i -> a(x)dx
            Transform(eq_mlp[6], eq_integral[6]),
            Transform(eq_mlp[7], eq_integral[7]), # b_j -> b(y)
            Transform(eq_mlp[8], eq_integral[8]),
            
            # Đồ thị biến đổi
            Transform(nodes_x, domain_x),
            Transform(nodes_y, domain_y),
            Transform(edges, kernel_area),
            FadeIn(kernel_label),
            
            run_time=3.0,
            rate_func=smooth
        )
        
        # Gom nhóm phương trình mới thành 1 khối để dễ thao tác sau này
        final_eq = VGroup(
            eq_mlp[0], eq_mlp[1:3], eq_mlp[3], eq_mlp[4], eq_mlp[5], eq_mlp[6], eq_mlp[7], eq_mlp[8]
        )
        
        self.wait(17.0) # Đợi cho hết Beat 1 (30 - 13)
        
        # ============================================================
        # BEAT 2 [8:45 - 9:15] (30.0s): Lớp Neural Operator & Vật lý
        # ============================================================
        
        # Xóa hình ảnh bên dưới, mang phương trình ra giữa
        self.play(
            FadeOut(continuous_graph),
            FadeOut(nodes_x), FadeOut(nodes_y), FadeOut(edges),
            final_eq.animate.move_to(ORIGIN).scale(1.2),
            run_time=2.0
        )
        
        # Text Overlay Định nghĩa
        def_text = Text("ĐỊNH NGHĨA: LỚP NEURAL OPERATOR", font_size=36, color=WHITE)
        def_box = SurroundingRectangle(def_text, color=C_PRIMARY, buff=0.3, stroke_width=2).set_fill(C_PRIMARY, opacity=0.2)
        def_group = VGroup(def_box, def_text).next_to(final_eq, UP, buff=1.0)
        
        self.play(FadeIn(def_group, shift=DOWN), run_time=1.5)
        self.wait(4.0)
        
        # Flash các định lý vật lý tương đương
        physics_terms = ["Đáp ứng xung", "Hàm Green (Green's Function)", "Tích chập (Convolution)"]
        term_mobjects = []
        for i, term in enumerate(physics_terms):
            t = Text(term, font_size=28, color=C_SECONDARY).next_to(final_eq, DOWN, buff=1.0 + i*0.8)
            term_mobjects.append(t)
            
        for term in term_mobjects:
            self.play(FadeIn(term, shift=UP), run_time=0.8)
            
        self.wait(2.0)
        
        # Highlight sự khác biệt (Học Kernel từ data)
        highlight_box = SurroundingRectangle(eq_mlp[4], color=C_ACCENT, buff=0.1) # eq_mlp[4] lúc này là kappa
        note_text = Text("Học từ dữ liệu thay vì cho trước!", font_size=24, color=C_ACCENT).next_to(highlight_box, DOWN, buff=0.2)
        
        self.play(Create(highlight_box), Write(note_text), run_time=1.5)
        
        self.wait(16.6) # Đợi kết thúc Beat 2
        
        # Dọn dẹp cảnh để chuẩn bị cho FNO
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
