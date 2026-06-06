"""
Scene 2.1 — Bản chất dữ liệu khoa học
Source: original_outline.tex, Section 2, Scene 2.1
Global time: 4:00 – 5:00
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

# Palette riêng cho scene này theo ý tưởng của tác giả
CYAN = "#00E5FF"
AMBER = "#F5A623"
DARK_BLUE = "#1A237E"

class Scene0201_NatureOfScientificData(TimedScene):
    SCRIPT_ID = "2.1"
    SCRIPT_TITLE = "Bản chất dữ liệu khoa học -- Không gian, Hình học và Trường"
    SCRIPT_START = 240.0
    SCRIPT_END = 300.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # BEAT 1: FLUID VOLUME & DIVERGENCE (Khối chất lưu & Bảo toàn)
        # ═══════════════════════════════════════════════════════════════
        
        # 1. Hàm chiếu Isometric (Biến tọa độ 3D (x,y,z) thành 2D để vẽ)
        def iso(x, y, z):
            return np.array([
                (x - y) * np.cos(PI/6) * 0.8,
                (x + y) * np.sin(PI/6) * 0.8 - z * 0.8,
                0
            ])

        # 2. Vẽ khung hộp chất lưu (Fluid Volume)
        back_box_lines = VGroup()
        front_box_lines = VGroup()
        
        # Mặt trên (z=0) - nhìn thấy toàn bộ
        front_box_lines.add(Line(iso(-2,-2,0), iso(2,-2,0), color=GREY_B, stroke_width=1.5))
        front_box_lines.add(Line(iso(2,-2,0), iso(2,2,0), color=GREY_B, stroke_width=1.5))
        front_box_lines.add(Line(iso(2,2,0), iso(-2,2,0), color=GREY_B, stroke_width=1.5))
        front_box_lines.add(Line(iso(-2,2,0), iso(-2,-2,0), color=GREY_B, stroke_width=1.5))
        
        # Mặt dưới (z=2) - có 2 cạnh khuất
        front_box_lines.add(Line(iso(-2,-2,2), iso(2,-2,2), color=GREY_B, stroke_width=1.5))
        back_box_lines.add(DashedLine(iso(2,-2,2), iso(2,2,2), color=GREY_C, stroke_width=1.5, dashed_ratio=0.5))
        back_box_lines.add(DashedLine(iso(2,2,2), iso(-2,2,2), color=GREY_C, stroke_width=1.5, dashed_ratio=0.5))
        front_box_lines.add(Line(iso(-2,2,2), iso(-2,-2,2), color=GREY_B, stroke_width=1.5))
        
        # Cạnh dọc - có 1 cạnh khuất ở góc (2,2)
        front_box_lines.add(Line(iso(-2,-2,0), iso(-2,-2,2), color=GREY_B, stroke_width=1.5))
        front_box_lines.add(Line(iso(2,-2,0), iso(2,-2,2), color=GREY_B, stroke_width=1.5))
        front_box_lines.add(Line(iso(-2,2,0), iso(-2,2,2), color=GREY_B, stroke_width=1.5))
        back_box_lines.add(DashedLine(iso(2,2,0), iso(2,2,2), color=GREY_C, stroke_width=1.5, dashed_ratio=0.5))
        
        # Sắp xếp z_index để tạo chiều sâu 3D chuẩn xác
        back_box_lines.set_z_index(0)
        front_box_lines.set_z_index(2)
        box_lines = VGroup(back_box_lines, front_box_lines)

        # 3. Vẽ các đường dòng (Streamlines) xuyên qua khối
        flow_lines = VGroup()
        for z in [0.5, 1.0, 1.5]:
            # Dùng CubicBezier để tạo đường cong uốn lượn mượt mà
            p0 = iso(-2.5, -1, z)
            p1 = iso(-1, 1.5, z)
            p2 = iso(1, -1.5, z)
            p3 = iso(2.5, 1, z)
            line = CubicBezier(p0, p1, p2, p3, color=CYAN, stroke_width=2.5)
            flow_lines.add(line)
            
            # Thêm mũi tên nhỏ ở giữa đường dòng để chỉ hướng
            mid_point = line.point_from_proportion(0.5)
            p_next = line.point_from_proportion(0.51)
            p_prev = line.point_from_proportion(0.49)
            tangent = p_next - p_prev
            arrow = Triangle(color=CYAN, fill_opacity=1, stroke_width=0).scale(0.05)
            arrow.rotate(np.arctan2(tangent[1], tangent[0]))
            arrow.move_to(mid_point)
            flow_lines.add(arrow)
        flow_lines.set_z_index(1)

        # 4. Highlight một Voxel nhỏ (Control Volume) để nói về Divergence
        voxel = VGroup()
        v_size = 0.8
        v_center = iso(0, 0, 1.0)
        # Vẽ 6 mặt của voxel bằng các Polygon mờ
        faces = [
            [iso(-v_size,-v_size,1-v_size), iso(v_size,-v_size,1-v_size), iso(v_size,v_size,1-v_size), iso(-v_size,v_size,1-v_size)], # bottom
            [iso(-v_size,-v_size,1+v_size), iso(v_size,-v_size,1+v_size), iso(v_size,v_size,1+v_size), iso(-v_size,v_size,1+v_size)], # top
        ]
        for f in faces:
            poly = Polygon(*f, color=YELLOW, fill_opacity=0.2, stroke_width=1.5)
            voxel.add(poly)
        voxel.set_z_index(1.5)

        # Text & Equation
        title_1 = Text("Fluid Volume (Khối chất lưu)", font_size=32, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        div_eq = MathTex(r"\nabla \cdot \mathbf{u} = 0", font_size=48, color=YELLOW).to_edge(DOWN, buff=0.8)
        div_text = Text("Bảo toàn khối lượng: Đạo hàm không gian = 0", font_size=20, color=MUTED).next_to(div_eq, DOWN, buff=0.2)

        # Animate Beat 1
        self.play_timed("box_appear", 0, 3, Create(box_lines))
        self.play_timed("title_appear", 3, 5, FadeIn(title_1))
        self.play_timed("flow_appear", 5, 9, Create(flow_lines))
        self.wait_timed("wait_flow", 9, 11)
        
        self.play_timed("voxel_appear", 11, 14, FadeIn(voxel), Flash(v_center, color=YELLOW, line_length=0.2))
        self.play_timed("div_eq_appear", 14, 16, Write(div_eq), FadeIn(div_text))
        self.wait_timed("wait_beat1", 16, 18)

        # Clear Beat 1
        self.play_timed("clear_beat1", 18, 20, *[FadeOut(m) for m in self.mobjects])

        # ═══════════════════════════════════════════════════════════════
        # BEAT 2: SEISMOLOGY & CROSS-DOMAIN MAPPING (Địa chấn & Bài toán ngược)
        # ═══════════════════════════════════════════════════════════════
        
        # 1. Vẽ lát cắt lòng đất (3D Layers giả lập)
        earth_layers = VGroup()
        layer_colors = ["#1A237E", "#283593", "#3949AB", "#5C6BC0"] # Dark blues
        for i, color in enumerate(layer_colors):
            rect = Rectangle(width=6, height=1, fill_color=color, fill_opacity=0.8, stroke_color=WHITE, stroke_width=0.5)
            rect.move_to(LEFT * 3.5 + DOWN * (i - 1.5))
            earth_layers.add(rect)
            
        earth_title = Text("Hidden 3D Volume", font_size=20, color=WHITE).next_to(earth_layers, UP, buff=0.3)

        # 2. Nguồn phát sóng và sóng lan truyền
        source = Dot(earth_layers[0].get_top() + LEFT * 2, color=RED, radius=0.08)
        wavefronts = VGroup()
        for i in range(1, 4):
            arc = Arc(radius=i*0.8, start_angle=-PI, angle=PI, color=WHITE, stroke_width=1.5, stroke_opacity=0.6)
            arc.move_arc_center_to(source.get_center())
            wavefronts.add(arc)

        # 3. Sensor trên mặt đất & Tín hiệu 1D
        surface_line = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY_B, stroke_width=2).move_to(earth_layers[0].get_top())
        sensors = VGroup(*[Dot(surface_line.point_from_proportion(p), color=AMBER, radius=0.06) for p in [0.2, 0.5, 0.8]])
        
        # Đồ thị 1D (Seismogram)
        axes = Axes(
            x_range=[0, 10, 2], y_range=[-1, 1, 0.5],
            x_length=4, y_length=1.5,
            axis_config={"color": GREY_B, "stroke_width": 1, "include_ticks": False}
        ).shift(RIGHT * 3.5 + UP * 1)
        
        # Hàm sóng tắt dần (damped sine)
        seismo_curve = axes.plot(lambda x: np.sin(3*x) * np.exp(-0.2*x) * 0.8, color=AMBER, stroke_width=2.5)
        seismo_title = Text("1D Surface Signals", font_size=20, color=AMBER).next_to(axes, UP, buff=0.2)

        # 4. Mũi tên Toán tử (Cross-Domain Operator)
        # Bỏ .flip(UP) vì nó làm sai lệch hoàn toàn tọa độ start/end. Dùng angle để bẻ cong mũi tên.
        op_arrow = CurvedArrow(
            axes.get_left() + LEFT * 0.2, 
            earth_layers.get_right() + RIGHT * 0.5, 
            color=NVIDIA_GREEN, stroke_width=4, angle=PI/3
        )
        op_text = Text("Inverse Operator", font_size=22, color=NVIDIA_GREEN, weight=BOLD).next_to(op_arrow, DOWN, buff=0.2)
        map_text = MathTex(r"\text{1D Time} \to \text{3D Space}", font_size=36, color=WHITE).to_edge(DOWN, buff=0.5)

        # Animate Beat 2
        self.play_timed("earth_appear", 20, 22, FadeIn(earth_layers), FadeIn(earth_title), Create(surface_line), FadeIn(sensors))
        self.play_timed("source_appear", 22, 23, FadeIn(source))
        self.play_timed("wave_appear", 23, 26, Create(wavefronts))
        
        self.play_timed("seismo_appear", 26, 28, FadeIn(axes), FadeIn(seismo_title))
        self.play_timed("seismo_curve", 28, 32, Create(seismo_curve))
        
        self.play_timed("op_arrow", 32, 34, Create(op_arrow), FadeIn(op_text))
        self.play_timed("map_text", 34, 36, Write(map_text))
        self.wait_timed("wait_beat2", 36, 38)

        # Clear Beat 2
        self.play_timed("clear_beat2", 38, 40, *[FadeOut(m) for m in self.mobjects])

        # ═══════════════════════════════════════════════════════════════
        # BEAT 3: AIRFOIL, BOUNDARY LAYER & CONTINUOUS TIME
        # ═══════════════════════════════════════════════════════════════
        
        # 1. Vẽ Profile cánh máy bay (Airfoil)
        airfoil_points = [
            [-3, 0, 0], [-1.5, 0.8, 0], [1.5, 0.4, 0], [3, 0, 0],
            [1.5, -0.3, 0], [-1.5, -0.6, 0], [-3, 0, 0]
        ]
        airfoil = VMobject().set_points_smoothly([np.array(p) for p in airfoil_points])
        airfoil.set_fill(color="#E0E0E0", opacity=0.9)
        airfoil.set_stroke(color=WHITE, width=1.5)
        airfoil.move_to(ORIGIN)

        # 2. Vẽ các đường dòng (Streamlines) - Chú ý vùng Boundary Layer
        flow_group = VGroup()
        # Các đường xa (thưa)
        for y_off in [1.5, 2.0, 2.5, -1.5, -2.0, -2.5]:
            line = CubicBezier(
                LEFT*4 + UP*y_off, LEFT*1 + UP*(y_off*0.8), 
                RIGHT*1 + UP*(y_off*0.8), RIGHT*4 + UP*y_off,
                color=CYAN, stroke_width=1.5, stroke_opacity=0.5
            )
            flow_group.add(line)
            
        # Các đường sát thân (Boundary Layer - Dày đặc & Gradient lớn)
        for y_off in [0.45, 0.55, 0.65, -0.35, -0.45, -0.55]:
            line = CubicBezier(
                LEFT*4 + UP*y_off, LEFT*1 + UP*(y_off*1.2), 
                RIGHT*1 + UP*(y_off*1.1), RIGHT*4 + UP*(y_off*1.5), # Bẻ cong mạnh ở đuôi (Wake)
                color=AMBER, stroke_width=2.5, stroke_opacity=0.9
            )
            flow_group.add(line)

        cfd_group = VGroup(airfoil, flow_group)

        # 3. Text & Highlight Boundary Layer
        cfd_title = Text("Khí động học (CFD)", font_size=28, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        
        # Animate Beat 3 (Phase 1: CFD)
        self.play_timed("cfd_appear", 40, 42, FadeIn(cfd_title), DrawBorderThenFill(airfoil))
        self.play_timed("flow_cfd", 42, 45, Create(flow_group))
        
        # Zoom vào vùng Boundary Layer & Wake (Đuôi cánh)
        self.play_timed("cfd_zoom", 45, 47, cfd_group.animate.scale(2.5).shift(LEFT * 1.5 + DOWN * 0.5))
        
        # 3. Tạo Brace cho "Boundary Layer"
        # Vùng boundary layer sau khi zoom nằm trong khoảng y = 0.9 đến y = 1.7
        brace = Brace(Line(UP*0.9, UP*1.7), RIGHT, color=WARNING).shift(RIGHT * 2.5)
        # Manim Brace(RIGHT) mặc định chỉ sang trái '{', ta lật ngang thành '}' để mũi nhọn chỉ về text
        brace.flip(RIGHT)
        
        brace_text = Text("Boundary Layer\n(Sharp Gradients)", font_size=20, color=WARNING, line_spacing=0.8)
        # Đặt text bên phải brace, và đẩy lên cao để nằm gọn giữa đường xanh và vàng
        brace_text.next_to(brace, RIGHT, buff=0.2).shift(UP * 0.9)
        
        self.play_timed("bl_highlight", 47, 49, GrowFromCenter(brace), FadeIn(brace_text))
        self.wait_timed("wait_cfd", 49, 50)

        # 4. Transition sang Quantum / Schrödinger (Continuous Time)
        # Xóa CFD, hiện Probability Cloud
        self.play_timed("quantum_transition", 50, 52, FadeOut(cfd_group), FadeOut(brace), FadeOut(brace_text), FadeOut(cfd_title))

        # Vẽ đám mây xác suất (Probability Cloud) bằng các vòng tròn đồng tâm mờ dần
        cloud_group = VGroup()
        for i in range(1, 8):
            r = i * 0.4
            # Tạo hiệu ứng gradient bằng cách chồng nhiều hình tròn
            c = Circle(radius=r, color=NVIDIA_GREEN, fill_opacity=0.15 / i, stroke_width=0)
            cloud_group.add(c)
            
        # Thêm các đường contour (quỹ đạo xác suất)
        contours = VGroup()
        for i in range(1, 4):
            # Ellipse xoay nghiêng
            e = Ellipse(width=i*1.2, height=i*0.6, color=NVIDIA_GREEN, stroke_width=1.5, stroke_opacity=0.6)
            e.rotate(i * 30 * DEGREES)
            contours.add(e)
            
        quantum_group = VGroup(cloud_group, contours)
        
        q_title = Text("Động lực học lượng tử", font_size=28, color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.5)
        q_eq = MathTex(r"i\hbar \frac{\partial}{\partial t}\Psi = \hat{H}\Psi", font_size=36, color=WHITE).to_edge(DOWN, buff=0.8)
        q_text = Text("Tiến hóa liên tục theo thời gian (Continuum)", font_size=20, color=MUTED).next_to(q_eq, DOWN, buff=0.2)

        self.play_timed("quantum_appear", 52, 54, FadeIn(q_title), FadeIn(quantum_group, scale=0.8))
        
        # Animation đám mây "thở" (pulsing) để thể hiện sự tiến hóa liên tục
        self.play_timed("quantum_pulse", 54, 56, quantum_group.animate.scale(1.1).rotate(15 * DEGREES), rate_func=there_and_back)
        
        self.play_timed("q_eq", 56, 58, Write(q_eq), FadeIn(q_text))
        self.wait_timed("wait_end", 58, 59)

        # Fade out kết thúc Scene
        self.play_timed("cut", 59, 60, *[FadeOut(m) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
