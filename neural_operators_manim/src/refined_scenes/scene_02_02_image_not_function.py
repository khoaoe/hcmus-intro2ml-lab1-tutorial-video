"""
Scene 2.2 — Lưu ý then chốt: Ảnh không phải là Hàm số
Source: original_outline.tex, Section 2, Scene 2.2
Global time: 5:00 – 6:00
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0202_ImageIsNotFunction(TimedScene):
    SCRIPT_ID = "2.2"
    SCRIPT_TITLE = "Ảnh không phải là Hàm số & Sự sụp đổ số"
    SCRIPT_START = 300.0
    SCRIPT_END = 360.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # =====================================================================
        # PHẦN 1 (0s - 30s) [Trước đây là 2.2a]
        # =====================================================================
        # Beat 1: Bản đồ thời tiết 2D
        map_group = VGroup()
        n = 16
        for i in range(n):
            for j in range(n):
                val = (np.sin(i * 0.4) * np.cos(j * 0.4) + 1) / 2
                color = interpolate_color(ManimColor(INPUT), ManimColor(WARNING), val)
                sq = Square(side_length=0.25, stroke_width=0, fill_color=color, fill_opacity=0.9)
                sq.move_to(np.array([(j - n / 2 + 0.5) * 0.25, (i - n / 2 + 0.5) * 0.25, 0]))
                map_group.add(sq)
                
        title = Text("Bản đồ dự báo thời tiết (64x64 Pixel)", font_size=32, color=WHITE).to_edge(UP, buff=0.5)
        
        self.play_timed("map_appear", 0, 3, FadeIn(map_group), FadeIn(title))
        
        slice_line = Line(LEFT*2.2, RIGHT*2.2, color=WHITE, stroke_width=4)
        slice_label = Text("Lát cắt 1D", font_size=20, color=WHITE).next_to(slice_line, UP, buff=0.1)
        
        self.play_timed("slice_appear", 3, 6, Create(slice_line), FadeIn(slice_label))
        
        # Beat 2: Trích xuất lát cắt 1D
        axes_1d = Axes(
            x_range=[-3, 3, 1], y_range=[0, 2, 0.5],
            x_length=8, y_length=4,
            axis_config={"color": GREY_B, "include_ticks": False}
        ).shift(DOWN*0.5)
        
        x_vals_1d = np.arange(-3, 3.1, 0.5)
        def smooth_func_1d(x):
            return (np.sin(x * 1.5) + 1) / 2 + 0.5
            
        y_vals_1d = [smooth_func_1d(x) for x in x_vals_1d]
        
        staircase_1d = VGroup()
        for i in range(len(x_vals_1d)-1):
            x1, x2 = x_vals_1d[i], x_vals_1d[i+1]
            y1 = y_vals_1d[i]
            y2 = y_vals_1d[i+1] if i < len(x_vals_1d)-2 else y_vals_1d[i]
            staircase_1d.add(Line(axes_1d.c2p(x1, y1), axes_1d.c2p(x2, y1), color=WARNING, stroke_width=4))
            if i < len(x_vals_1d)-1:
                staircase_1d.add(Line(axes_1d.c2p(x2, y1), axes_1d.c2p(x2, y2), color=WARNING, stroke_width=4))
                
        smooth_graph_1d = axes_1d.plot(smooth_func_1d, color=NVIDIA_GREEN, stroke_width=4)
        
        # Manim sẽ crash nếu transform giữa Line và Axes do khác cấu trúc sub-mobjects
        self.play_timed("to_1d", 6, 9,
            FadeOut(map_group), 
            FadeOut(slice_label),
            FadeOut(slice_line), FadeIn(axes_1d),
            FadeOut(title)
        )
        
        title_1d = Text("Lát cắt 1D (Đồ thị nhiệt độ)", font_size=32, color=WHITE).to_edge(UP, buff=0.5)
        self.play_timed("show_title_1d", 9, 10, FadeIn(title_1d))
        
        staircase_label = Text("Ảnh rời rạc (Pixels)", font_size=24, color=WARNING).next_to(staircase_1d, UP, buff=0.5).shift(RIGHT * 2.5)
        self.play_timed("show_staircase", 10, 13, Create(staircase_1d), FadeIn(staircase_label))
        
        smooth_label = Text("Hàm liên tục", font_size=24, color=NVIDIA_GREEN).next_to(smooth_graph_1d, DOWN, buff=0.5)
        self.play_timed("show_smooth", 13, 16, Create(smooth_graph_1d), FadeIn(smooth_label))
        
        # Beat 3: Zoom mạnh vào 1 đoạn
        zoom_group = VGroup(axes_1d, staircase_1d, smooth_graph_1d)
        
        self.play_timed("zoom_in", 16, 20,
            zoom_group.animate.scale(3).shift(LEFT * 1.5 + DOWN * 1.5),
            FadeOut(staircase_label), FadeOut(smooth_label), FadeOut(title_1d)
        )
        
        q_text = Text("Zoom 100 lần:\nKhông hề\nmượt mà!", font_size=28, color=WARNING, line_spacing=1.0).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
        self.play_timed("show_q", 20, 22, FadeIn(q_text))
        
        self.wait_timed("wait_a", 22, 28)
        
        # Xoá toàn bộ để sang phần 2
        self.play_timed("end_a", 28, 30, *[FadeOut(m) for m in self.mobjects])

        # =====================================================================
        # PHẦN 2 (30s - 60s) [Option 1: PDE Residual Blow-up - Heatmap]
        # =====================================================================
        DARK_BLUE = "#1A237E"
        ERROR_RED = "#FF3333"
        AMBER = "#F5A623"
        CYAN = "#00E5FF"
        
        # Beat 1: THE PIXELATED FIELD & THE PHYSICS QUESTION
        # 1. Tạo trường pixel hóa (10x10 grid) - Đại diện cho "Ảnh" / CNN Input
        n = 10
        pixel_field = VGroup()
        for i in range(n):
            for j in range(n):
                # Giả lập một trường nhiệt độ mượt nhưng bị lượng tử hóa thành pixel
                val = (np.sin(i/2.5) * np.cos(j/2.5) + 1) / 2
                color = interpolate_color(ManimColor(DARK_BLUE), ManimColor(AMBER), val)
                sq = Square(
                    side_length=0.45, 
                    fill_color=color, 
                    fill_opacity=1.0, 
                    stroke_width=0 # Không viền để trông như một khối màu liền
                )
                sq.move_to(np.array([
                    (j - n/2 + 0.5) * 0.45, 
                    (i - n/2 + 0.5) * 0.45, 
                    0
                ]))
                pixel_field.add(sq)
                
        pixel_field.shift(LEFT * 3.5)
        
        label_pixel = Text("Pixelated Field\n(CNN Input)", font_size=24, color=WHITE).next_to(pixel_field, UP, buff=0.3)
        
        # 2. Phương trình Vật lý (Heat Equation / Diffusion)
        pde_eq = VGroup(
            MathTex(r"\frac{\partial u}{\partial t} = \alpha \nabla^2 u", font_size=36, color=WHITE),
            Text("(Khuếch tán / Năng lượng)", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 3.5 + UP * 2)
        
        pde_text = Text("Kiểm tra Vật lý: Tính Laplacian", font_size=20, color=MUTED).next_to(pde_eq, DOWN, buff=0.3)
        pde_math = MathTex(r"(\nabla^2 u)", font_size=24, color=MUTED).next_to(pde_text, DOWN, buff=0.1)
        
        self.play_timed("show_pixel_field", 30, 32, FadeIn(pixel_field), FadeIn(label_pixel))
        self.play_timed("show_pde", 32, 34, Write(pde_eq), FadeIn(pde_text), FadeIn(pde_math))
        self.wait_timed("wait_pde", 34, 36)

        # Beat 2: THE RESIDUAL REVEAL (Phần dư bùng nổ tại ranh giới)
        # Làm tối các ô vuông (Residual ≈ 0 inside pixels)
        self.play_timed("darken_pixels", 36, 37.5, pixel_field.animate.set_fill(opacity=0.3))
        
        inside_text = VGroup(
            Text("Residual", font_size=18, color=CYAN),
            MathTex(r"\approx 0", font_size=18, color=CYAN),
            Text("(bên trong pixel)", font_size=18, color=CYAN)
        ).arrange(DOWN, buff=0.1).next_to(pixel_field, DOWN, buff=0.3).shift(LEFT * 1.2)
        
        self.play_timed("show_inside_text", 37.5, 38.5, FadeIn(inside_text))
        
        # Bật sáng các đường viền (Residual → ∞ at boundaries)
        boundary_lines = VGroup()
        for i in range(n + 1):
            # Horizontal lines
            h_line = Line(
                pixel_field.get_left() + UP * (2.25 - i * 0.45),
                pixel_field.get_right() + UP * (2.25 - i * 0.45),
                color=ERROR_RED, stroke_width=3
            )
            boundary_lines.add(h_line)
            # Vertical lines
            v_line = Line(
                pixel_field.get_top() + LEFT * (2.25 - i * 0.45),
                pixel_field.get_bottom() + LEFT * (2.25 - i * 0.45),
                color=ERROR_RED, stroke_width=3
            )
            boundary_lines.add(v_line)
            
        # Animation: Các đường viền xuất hiện và "nóng lên" (glow/pulse)
        self.play_timed("show_boundaries", 38.5, 40.5, Create(boundary_lines, lag_ratio=0.05))
        
        boundary_text = VGroup(
            Text("Residual", font_size=18, color=ERROR_RED, weight=BOLD),
            MathTex(r"\to \infty", font_size=18, color=ERROR_RED),
            Text("(tại ranh giới pixel)", font_size=18, color=ERROR_RED, weight=BOLD)
        ).arrange(DOWN, buff=0.1).next_to(inside_text, RIGHT, buff=0.5)
        
        self.play_timed("show_boundary_text", 40.5, 41.5, FadeIn(boundary_text, shift=UP*0.2))

        # Beat 3: THE BLOW-UP (Định lượng sự sụp đổ)
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 5, 1],
            x_length=5, y_length=2.5,
            axis_config={"color": GREY_B, "stroke_width": 1, "include_ticks": False}
        ).shift(RIGHT * 3.5 + DOWN * 1.5)
        
        # Hàm residual: 0 ở giữa, spikes ở các số nguyên (ranh giới pixel)
        def residual_func(x):
            spikes = sum([4 * np.exp(-20 * (x - i)**2) for i in range(1, 10)])
            return spikes
            
        residual_curve = axes.plot(residual_func, color=ERROR_RED, stroke_width=3)
        residual_label = MathTex(r"\|\nabla^2 u\|", font_size=28, color=ERROR_RED).next_to(axes, UP, buff=0.2)
        
        self.play_timed("show_residual_graph", 41.5, 44, 
                        FadeIn(axes), 
                        Create(residual_curve),
                        FadeIn(residual_label))
        
        # Highlight một cái gai nhọn
        spike_highlight = axes.get_vertical_line(axes.c2p(5, 4), color=WHITE, stroke_width=2)
        inf_label = MathTex(r"\infty", font_size=32, color=WHITE).next_to(spike_highlight.get_top(), UP, buff=0.1)
        
        self.play_timed("show_spike", 44, 46, Create(spike_highlight), FadeIn(inf_label))
        self.wait_timed("wait_spike", 46, 48)

        # Beat 4: CONCLUSION (Kết luận sắc bén)
        self.play_timed("clear_for_conclusion", 48, 50, *[FadeOut(m) for m in self.mobjects])
        
        final_msg = VGroup(
            Text("CNN tạo ra các", font_size=32, color=MUTED),
            Text("PIXEL", font_size=40, color=AMBER, weight=BOLD),
            Text("nhưng Vật lý cần các", font_size=32, color=MUTED),
            Text("ĐẠO HÀM", font_size=40, color=NVIDIA_GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.3)
        
        sub_msg = Text("Ép hàm số thành ảnh = Vi phạm định luật bảo toàn.", 
                       font_size=22, color=WHITE).next_to(final_msg, DOWN, buff=0.8)
                       
        self.play_timed("show_conclusion", 50, 54, 
            LaggedStart(*[FadeIn(m, shift=UP*0.2) for m in final_msg], lag_ratio=0.2),
            FadeIn(sub_msg)
        )
        self.wait_timed("hold_conclusion", 54, 58)
        
        self.play_timed("cut", 58, 60, *[FadeOut(m) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
