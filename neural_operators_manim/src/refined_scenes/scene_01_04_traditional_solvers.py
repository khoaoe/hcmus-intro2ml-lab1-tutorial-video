"""
Scene 1.4 — Traditional Solvers & Nỗi đau của Giải tích số
Source: original_outline.tex, Section 1, Scene 1.4
Global time: 2:30 – 3:30
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0104_TraditionalSolvers(TimedScene):
    SCRIPT_ID = "1.4"
    SCRIPT_TITLE = "Traditional Solvers & Nỗi đau của Giải tích số"
    SCRIPT_START = 150.0
    SCRIPT_END = 210.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: [2:30–2:50] The Discretization Meat Grinder
        # ═══════════════════════════════════════════════════════════════
        
        # 1. Tạo một trường liên tục (Gradient mượt mà)
        # Dùng Heatmap / Gradient để giả lập trường vật lý
        def get_gradient_image():
            img = np.zeros((200, 200, 3))
            for i in range(200):
                for j in range(200):
                    # Màu sắc biến thiên mượt mà (Xanh -> Tím -> Đỏ)
                    val = np.sin(i/30) * np.cos(j/30)
                    img[i, j] = [0.5 + 0.5*val, 0.2, 0.8 - 0.5*val] 
            return img
        
        # Using a rectangle with color gradient or just relying on manim's ImageMobject
        # Note: In manim CE, ImageMobject takes a filename or numpy array. 
        # Numpy array must be uint8 (0-255). Let's fix this for safety:
        img_array = (get_gradient_image() * 255).astype(np.uint8)
        field_img = ImageMobject(img_array).scale(2.5).shift(LEFT * 2.5)
        
        # 2. Tấm lưới sắt (Grid) đè xuống
        grid_lines = VGroup()
        n = 12
        for i in range(n + 1):
            grid_lines.add(Line(UP*1.2, DOWN*1.2, stroke_color=WHITE, stroke_width=1.5).shift(LEFT * 2.5 + RIGHT * (i * 2.4 / n - 1.2)))
            grid_lines.add(Line(LEFT*1.2, RIGHT*1.2, stroke_color=WHITE, stroke_width=1.5).shift(LEFT * 2.5 + UP * (i * 2.4 / n - 1.2)))
            
        pde_eq = MathTex(r"-\nabla \cdot (a \nabla u) = f", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)

        self.play_timed("field_appear", 0, 3, FadeIn(field_img))
        self.play_timed("grid_drop", 3, 6, 
                        Create(grid_lines, lag_ratio=0.05), 
                        Write(pde_eq))
        
        # 3. Hiệu ứng "Băm nát" (Pixelation / Discretization)
        # Tạo các ô vuông màu sắc rời rạc để thay thế ảnh mượt
        discrete_blocks = VGroup()
        for i in range(n):
            for j in range(n):
                val = np.sin((i+0.5)/30 * 20) * np.cos((j+0.5)/30 * 20)
                # Manim default colors
                color = interpolate_color(BLUE, RED, 0.5 + 0.5*val)
                sq = Square(side_length=2.4/n - 0.02, fill_color=color, fill_opacity=0.9, stroke_width=0)
                sq.move_to(LEFT * 2.5 + RIGHT * ((j + 0.5) * 2.4 / n - 1.2) + UP * (1.2 - (i + 0.5) * 2.4 / n))
                discrete_blocks.add(sq)
                
        self.play_timed("pixelate", 6, 10, 
                        FadeOut(field_img), 
                        FadeIn(discrete_blocks))
        self.wait_timed("hold_beat1", 10, 20)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [2:50–3:10] The Iterative Crawl & Compute Wall
        # ═══════════════════════════════════════════════════════════════
        
        self.play_timed("clear_left", 20, 21, 
                        FadeOut(discrete_blocks), FadeOut(grid_lines), FadeOut(pde_eq))
        
        # Dọn field sang trái, dành chỗ cho biểu đồ Cost bên phải
        mini_grid = VGroup(*[Square(side_length=0.2, stroke_color=GREY_B, stroke_width=1) for _ in range(64)]).arrange_in_grid(8, 8, buff=0.05).shift(LEFT * 3.5)
        
        # Tia sáng quét (Solver Sweep)
        scan_line = Line(UP*1, DOWN*1, color=YELLOW, stroke_width=4).set_glow_factor(1).move_to(mini_grid.get_left())
        
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 10, 2],
            x_length=4, y_length=3,
            tips=False, axis_config={"stroke_color": GREY_B}
        ).shift(RIGHT * 2.5)
        
        cost_curve = axes.plot(lambda x: 0.1 * (x**3), x_range=[0.5, 3.8], color=RED, stroke_width=3)
        cost_label = Text("Compute Cost", font_size=20, color=RED).next_to(axes, UP)
        
        self.play_timed("setup_beat2", 21, 23, 
                        FadeIn(mini_grid), FadeIn(scan_line), 
                        FadeIn(axes), Write(cost_label))
        
        # Quét lưới 1 (Nhanh)
        self.play_timed("sweep1", 23, 24.8, 
                        scan_line.animate.move_to(mini_grid.get_right()))
        self.play_timed("reset_sweep1", 24.8, 25, 
                        scan_line.animate.move_to(mini_grid.get_left()))
        
        # Lưới nhân đôi độ mịn (Transform)
        dense_grid = VGroup(*[Square(side_length=0.1, stroke_color=GREY_B, stroke_width=0.5) for _ in range(256)]).arrange_in_grid(16, 16, buff=0.02).shift(LEFT * 3.5)
        self.play_timed("refine_grid", 25, 27, Transform(mini_grid, dense_grid))
        
        # Quét lưới 2 (Chậm hơn) + Vẽ đường cong Cost
        self.play_timed("sweep2_and_cost", 27, 31.8, 
                        scan_line.animate.move_to(mini_grid.get_right()), 
                        Create(cost_curve))
        self.play_timed("reset_sweep2", 31.8, 32, 
                        scan_line.animate.move_to(mini_grid.get_left()))
        
        # Quét lưới 3 (Cực chậm) + Cost đâm thủng trần
        self.play_timed("sweep3_explosion", 32, 38, 
                        scan_line.animate.shift(RIGHT * 0.5), # Chỉ nhích được một chút
                        cost_curve.animate.shift(UP * 2).set_color(WARNING) # Đường cong vọt lên
                        )
        
        explosion_text = Text("BÙNG NỔ!", font_size=28, color=WARNING, weight=BOLD).next_to(cost_curve, RIGHT, buff=0.2).shift(UP)
        self.play_timed("boom", 38, 40, FadeIn(explosion_text, scale=1.5))

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: [3:10–3:30] The White-Box Solver & The Gradient Wall
        # ═══════════════════════════════════════════════════════════════
        
        self.play_timed("clear_beat2", 40, 41, 
                        *[FadeOut(m) for m in [mini_grid, scan_line, axes, cost_curve, cost_label, explosion_text]])
        
        # 1. Solver là WHITE BOX - hiện rõ phương trình bên trong
        solver_box = RoundedRectangle(
            width=4, height=2.5, corner_radius=0.2,
            fill_color=GREY_E, fill_opacity=0.3,  # Trong suốt, thấy được bên trong
            stroke_color=WHITE, stroke_width=2
        ).shift(UP * 0.3)
        
        # Phương trình Navier-Stokes hiện bên trong box (white-box nature)
        ns_eq = MathTex(
            r"\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u}",
            font_size=28, color=WHITE
        ).move_to(solver_box)
        
        solver_label = Text("Traditional Solver", 
                            font_size=22, color=WHITE).next_to(solver_box, DOWN, buff=0.2)
        
        self.play_timed("whitebox_appear", 41, 43,
                        Create(solver_box), Write(ns_eq), FadeIn(solver_label))
        
        # 2. Forward pass: Mũi tên XANH đi qua trơn tru
        fwd_arrow = Arrow(LEFT * 5.5, solver_box.get_left() + LEFT * 0.2, 
                          color=NVIDIA_GREEN, buff=0.1, stroke_width=4)
        fwd_label = Text("Forward: Mô phỏng\n(Input → PDE → Output)", 
                         font_size=18, color=NVIDIA_GREEN).next_to(fwd_arrow, UP)
        
        # Output đi ra
        out_arrow = Arrow(solver_box.get_right() + RIGHT * 0.2, RIGHT * 5.5,
                          color=NVIDIA_GREEN, buff=0.1, stroke_width=4)
        
        self.play_timed("forward_pass", 43, 45,
                        GrowArrow(fwd_arrow), FadeIn(fwd_label),
                        GrowArrow(out_arrow))
        
        # 3. Inverse Problem scenario: "Cho Output, tìm Input"
        inverse_text = Text("Inverse Problem: Cho Output → Tìm Input (Thiết kế tối ưu)",
                            font_size=22, color=WARNING, weight=BOLD).to_edge(UP, buff=0.3)
        
        self.play_timed("inverse_scenario", 45, 47, FadeIn(inverse_text))
        
        # 4. Gradient arrow (ĐỎ) cố đi NGƯỢC lại qua solver
        grad_arrow = Arrow(RIGHT * 5.5, solver_box.get_right() + RIGHT * 0.2,
                           color=WARNING, buff=0.1, stroke_width=4)
        grad_label = Text("Gradient / Backprop\n(Tối ưu hóa)", 
                          font_size=18, color=WARNING).next_to(grad_arrow, UP)
        
        self.play_timed("gradient_try", 47, 49,
                        GrowArrow(grad_arrow), FadeIn(grad_label))
        
        # 5. Bức tường chặn gradient - hiện rõ LÝ DO
        wall = Line(solver_box.get_right() + UP*1.2, 
                    solver_box.get_right() + DOWN*1.2, 
                    color=WARNING, stroke_width=5)
        
        reasons = Text("Non-differentiable", font_size=20, color=WARNING).next_to(wall, RIGHT, buff=0.3).shift(DOWN * 0.8)
        
        self.play_timed("gradient_wall", 49, 52,
                        Create(wall),
                        FadeIn(reasons, shift=RIGHT*0.3))
        
        # 6. Gradient vỡ tan (shatter) khi đập vào tường
        shatter_pieces = VGroup(*[
            Dot(solver_box.get_right() + RIGHT*0.5, color=WARNING, radius=0.05)
            .shift(np.random.uniform(-0.5, 0.5, 3)) 
            for _ in range(20)
        ])
        
        self.play_timed("gradient_shatter", 52, 54,
                        FadeOut(grad_arrow),
                        LaggedStart(*[
                            FadeOut(p, shift=LEFT * np.random.uniform(0.5, 1.5)) 
                            for p in shatter_pieces
                        ], lag_ratio=0.05))
        
        # 7. Kết luận: Bổ sung ML, không thay thế Solver
        note = Text(
            "Mục tiêu: Bổ sung ML vào Toolbox,\nkhông thay thế Solver truyền thống",
            font_size=20, color=YELLOW, weight=BOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play_timed("conclusion", 54, 57, Write(note))
        self.wait_timed("hold_end", 57, 59)
        
        self.play_timed("cut", 59, 60, *[FadeOut(m) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
