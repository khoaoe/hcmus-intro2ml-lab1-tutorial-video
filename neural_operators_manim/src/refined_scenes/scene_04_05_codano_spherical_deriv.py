
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0405_CoDANOSphericalDerivative(TimedScene):
    SCRIPT_ID = "4.5"
    SCRIPT_TITLE = "CoDANO, Spherical FNO & Khối Đạo hàm"
    SCRIPT_START = 945.0
    SCRIPT_END = 1020.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        coda_title = Text("CoDANO: Attention giữa biến vật lý", font_size=24,
                          color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)

        variables = ["p", "v_x", "v_y", "T", r"\rho"]
        n_vars = len(variables)
        
        cell_size = 0.9
        spacing = 1.0

        col_labels = VGroup()
        for j, var in enumerate(variables):
            label = MathTex(var, font_size=32, color=TEXT).move_to(
                RIGHT * (j * spacing) + UP * spacing)
            col_labels.add(label)
            
        row_labels = VGroup()
        cells = VGroup()
        np.random.seed(42)
        for i in range(n_vars):
            row_label = MathTex(variables[i], font_size=32, color=TEXT).move_to(
                LEFT * spacing + DOWN * (i * spacing))
            row_labels.add(row_label)
            for j in range(n_vars):
                val = np.random.uniform(0.1, 1.0) if i != j else 1.0
                cell = Square(side_length=cell_size, fill_color=OPERATOR,
                              fill_opacity=val * 0.7, stroke_width=1.0, stroke_color=GRID)
                cell.move_to(RIGHT * (j * spacing) + DOWN * (i * spacing))
                cells.add(cell)
                
        matrix_group = VGroup(col_labels, row_labels, cells).move_to(ORIGIN).shift(UP * 0.5)

        alpha_label = MathTex(r"\alpha_{c,c'}", font_size=36, color=OPERATOR)
        alpha_desc = Text("Tự học: p ảnh hưởng bao nhiêu lên v",
                          font_size=24, color=MUTED).next_to(alpha_label, DOWN, buff=0.2)
        alpha_group = VGroup(alpha_label, alpha_desc).next_to(matrix_group, DOWN, buff=0.6)

        self.play_timed("coda_title", 0, 2, FadeIn(coda_title))
        self.play_timed("matrix", 2, 6, FadeIn(matrix_group))
        self.play_timed("alpha", 6, 8, FadeIn(alpha_group))
        self.wait_timed("hold_coda", 8, 18)

        self.play_timed("clear_coda", 18, 18.5,
                        *[FadeOut(m) for m in [coda_title, matrix_group, alpha_group]])

        sphere_title = Text("Spherical FNO", font_size=24,
                            color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.4)

        def sphere_surface(u, v):
            x = 2.0 * np.cos(v) * np.cos(u)
            y = 2.0 * np.sin(v)
            z = 2.0 * np.cos(v) * np.sin(u)
            return np.array([x, y, z])

        def temperature_function(u, v):
            return 0.5 * np.cos(v) + 0.3 * np.sin(2*v) * np.cos(2*u) + 0.2 * np.cos(3*v)

        sphere_surface_obj = Surface(
            sphere_surface,
            u_range=[0, 2*PI],
            v_range=[-PI/2, PI/2],
            resolution=(32, 16),
        )

        for face in sphere_surface_obj.submobjects:
            center = face.get_center()
            x, y, z = center
            if z > 0:
                v_center = np.arcsin(np.clip(y / 2.0, -1.0, 1.0))
                u_center = np.arctan2(z, x)
                temp = temperature_function(u_center, v_center)
                color = interpolate_color(BLUE, RED, (temp + 1) / 2)
                face.set_fill(color, opacity=0.8)
                face.set_stroke(WHITE, width=0.5, opacity=0.3)
            else:
                face.set_fill(BLACK, opacity=0)
                face.set_stroke(WHITE, width=0, opacity=0)
        
        sphere_group = VGroup(sphere_surface_obj).shift(LEFT * 3)

        modes_title = Text("Spherical Harmonics Modes", font_size=18, 
                           color=SCIENCE).shift(RIGHT * 3.5 + UP * 2.2)
        
        coeff_bars = VGroup()
        coeff_labels = VGroup()
        modes = ["Y_0^0", "Y_1^0", "Y_1^1", "Y_2^0", "Y_2^1", "Y_2^2"]
        coefficients = [0.5, 0.3, 0.2, 0.15, 0.1, 0.05]
        
        for i, (mode, coeff) in enumerate(zip(modes, coefficients)):
            bar_height = coeff * 3
            bar = Rectangle(width=0.4, height=bar_height, 
                           fill_color=SCIENCE, fill_opacity=0.7, 
                           stroke_color=SCIENCE, stroke_width=1)
            bar.move_to(RIGHT * (1.5 + i * 0.8) + UP * (bar_height/2))
            coeff_bars.add(bar)
            
            label = MathTex(mode, font_size=18, color=TEXT)
            label.next_to(bar, DOWN, buff=0.1)
            coeff_labels.add(label)

        coeff_group = VGroup(coeff_bars, coeff_labels, modes_title)

        sphere_note = VGroup(
            Text("Fourier → kinh độ (longitude)", font_size=16, color=INPUT),
            Text("Legendre → vĩ độ (latitude)", font_size=16, color=PURPLE),
            Text("= Spherical Harmonics", font_size=16, color=SCIENCE, weight=BOLD),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT * 3.5 + DOWN * 1.2)

        pole_note = Text("Triệt tiêu singularity tại cực", font_size=16,
                         color=NVIDIA_GREEN).next_to(sphere_note, DOWN, buff=0.2)

        self.play_timed("sphere_title", 18.5, 20, FadeIn(sphere_title))
        self.play_timed("sphere_create", 20, 23, Create(sphere_group))
        
        self.play_timed("coeff_bars", 23, 26, 
                        *[GrowFromEdge(bar, DOWN) for bar in coeff_bars],
                        FadeIn(coeff_labels), FadeIn(modes_title))
        
        self.play_timed("sphere_notes", 26, 28, FadeIn(sphere_note), FadeIn(pole_note))
        self.wait_timed("hold_sphere", 28, 35)

        self.play_timed("clear_sphere", 35, 35.5,
                        *[FadeOut(m) for m in [sphere_title, sphere_group, coeff_group, sphere_note, pole_note]])

        deriv_title = Text("Nghịch lý & Giải pháp: Khối Đạo hàm", font_size=24,
                           color=WARNING, weight=BOLD).to_edge(UP, buff=0.4)

        paradox = VGroup(
            Text("Tích phân: giỏi tổng hợp toàn cục", font_size=20, color=OUTPUT),
            Text("nhưng mù với đạo hàm tức thời", font_size=20, color=WARNING),
        ).arrange(DOWN, buff=0.2).next_to(deriv_title, DOWN, buff=0.3)

        self.play_timed("deriv_title", 35.5, 37, FadeIn(deriv_title))
        self.play_timed("paradox", 37, 40, FadeIn(paradox))

        large_stencil_units = VGroup()
        for val in ["-1", "0", "1"]:
            box = Square(side_length=0.8, fill_color=CARD_BG, fill_opacity=0.9, 
                         stroke_color=INPUT, stroke_width=2)
            label = Text(val, font_size=24, color=INPUT, weight=BOLD).move_to(box)
            large_stencil_units.add(VGroup(box, label))
        large_stencil_units.arrange(RIGHT, buff=0.1).shift(UP * 0.5)
        
        large_stencil_label = Text("CNN stencil = [-1, 0, 1] / Δx", font_size=20, color=INPUT).next_to(large_stencil_units, DOWN, buff=0.3)
        
        self.play_timed("stencil_intro", 40, 43, FadeIn(large_stencil_units), FadeIn(large_stencil_label))

        axes = Axes(
            x_range=[0, 6, 1], y_range=[-1.2, 2.2, 1],
            x_length=7, y_length=2.5,
            axis_config={"color": GRID, "stroke_width": 1},
        ).shift(DOWN * 1.5)
        curve = axes.plot(lambda x: np.sin(x * 1.2) + 0.6, color=OUTPUT, stroke_width=2.5)
        curve_label = Text("u(x)", font_size=16, color=OUTPUT).next_to(axes.c2p(6, 1.5), UP, buff=0.1)

        self.play_timed("axes_curve", 43, 46, Create(axes), Create(curve), FadeIn(curve_label))

        stencil_units = VGroup()
        for val in ["-1", "0", "1"]:
            box = Square(side_length=0.4, fill_color=CARD_BG, fill_opacity=0.9, 
                         stroke_color=INPUT, stroke_width=2)
            label = Text(val, font_size=14, color=INPUT, weight=BOLD).move_to(box)
            stencil_units.add(VGroup(box, label))
            
        x_center_start = 1.0
        dx_start = 0.5
        y_box_start = -0.9
        
        box_positions_start = [
            axes.c2p(x_center_start - dx_start, y_box_start),
            axes.c2p(x_center_start, y_box_start),
            axes.c2p(x_center_start + dx_start, y_box_start)
        ]
        
        for i in range(3):
            stencil_units[i].move_to(box_positions_start[i])
            
        stencil_label = Text("CNN stencil = [-1, 0, 1] / Δx", font_size=14, color=INPUT)
        stencil_label.next_to(stencil_units[1], DOWN, buff=0.3)

        self.play_timed("stencil_to_graph", 46, 48,
                        ReplacementTransform(large_stencil_units, stencil_units),
                        ReplacementTransform(large_stencil_label, stencil_label))

        sample_dots = VGroup(*[Dot(color=YELLOW, radius=0.08) for _ in range(3)])
        curve_pts_start = [
            axes.input_to_graph_point(x_center_start - dx_start, curve),
            axes.input_to_graph_point(x_center_start, curve),
            axes.input_to_graph_point(x_center_start + dx_start, curve)
        ]
        for i in range(3):
            sample_dots[i].move_to(curve_pts_start[i])
            
        dash_lines = VGroup()
        for i in range(3):
            dash = DashedLine(box_positions_start[i], curve_pts_start[i], color=WHITE, stroke_opacity=0.4)
            dash_lines.add(dash)
            
        tangent_line = Line(
            curve_pts_start[0] - (curve_pts_start[2] - curve_pts_start[0])*0.5,
            curve_pts_start[2] + (curve_pts_start[2] - curve_pts_start[0])*0.5,
            color=RED, stroke_width=2.5, stroke_opacity=0.9
        )
        
        self.play_timed("show_connections", 48, 50, FadeIn(sample_dots), FadeIn(dash_lines), FadeIn(tangent_line))

        def update_cnn_visuals(mob, alpha):
            x_center = 1.0 + alpha * 4.0  # Trượt từ x=1 đến x=5
            dx = 0.5  # Khoảng cách lấy mẫu trên trục x
            
            y_box = -0.9  
            box_positions = [
                axes.c2p(x_center - dx, y_box),
                axes.c2p(x_center, y_box),
                axes.c2p(x_center + dx, y_box)
            ]
            
            for i in range(3):
                stencil_units[i].move_to(box_positions[i])
                
            curve_pts = [
                axes.input_to_graph_point(x_center - dx, curve),
                axes.input_to_graph_point(x_center, curve),
                axes.input_to_graph_point(x_center + dx, curve)
            ]
            for i in range(3):
                sample_dots[i].move_to(curve_pts[i])
                dash_lines[i].put_start_and_end_on(box_positions[i], curve_pts[i])
                
            stencil_label.next_to(stencil_units[1], DOWN, buff=0.3)
            
            p_left, p_right = curve_pts[0], curve_pts[2]
            slope_vec = p_right - p_left
            tangent_line.put_start_and_end_on(p_left - slope_vec*0.5, p_right + slope_vec*0.5)

        cnn_group = VGroup(stencil_units, sample_dots, dash_lines, stencil_label, tangent_line)
        
        self.play_timed("stencil_slide", 50, 62,
                        UpdateFromAlphaFunc(cnn_group, update_cnn_visuals))

        resolution_note = Text(
            "Tăng resolution → giảm Δx → stencil tự scale → vật lý nhất quán",
            font_size=16, color=MUTED
        ).to_edge(DOWN, buff=0.3)

        self.play_timed("res_note", 62, 65, FadeIn(resolution_note))
        self.wait_timed("hold_end", 65, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
