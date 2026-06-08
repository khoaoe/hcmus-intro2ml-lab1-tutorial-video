"""
Scene 5.2 — Carbon Storage & Khí động học công nghiệp (Refactored)
Source: original_outline.tex, Section 5, Scene 5.2
Global time: 19:10 – 20:55
Duration: 105s
"""
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import * 

apply_global_config()

CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

# Hàm tạo biên dạng cánh NACA 4-digit (Chuẩn Khí động học)
def get_naca_airfoil_points(thickness=0.12, chord=3.0, n_points=60, center=ORIGIN):
    x = np.linspace(0, 1, n_points)
    y = 5 * thickness * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)
    top = np.array([[(1 - xi)*chord - chord/2 + center[0], yi + center[1], 0] for xi, yi in zip(x, y)])
    bottom = np.array([[(1 - xi)*chord - chord/2 + center[0], -yi + center[1], 0] for xi, yi in zip(x, y)])
    return np.vstack((top, bottom[::-1]))

class Scene0502_CarbonAero(TimedScene): # Kế thừa TimedScene của bạn
    SCRIPT_ID = "5.2"
    SCRIPT_TITLE = "Carbon Storage & Khí động học"
    SCRIPT_START = 1150.0
    SCRIPT_END = 1255.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # BEAT 1: [19:10–19:55] Carbon Capture & Subsurface Flow (45s)
        # ═══════════════════════════════════════════════════════════════
        title = Text("Carbon Capture & Storage (CCS)", font_size=32, color=BLUE_C, weight=BOLD).to_edge(UP, buff=0.4)
        
        # 1. Vỉa đá xốp (Porous Media) - Thể hiện bằng Point Cloud
        np.random.seed(42)
        rock_matrix = VGroup(*[
            Dot(point=[np.random.uniform(-5, 5), np.random.uniform(-2.5, 1.5), 0], 
                radius=np.random.uniform(0.03, 0.06), color=GRAY_B, fill_opacity=0.4) 
            for _ in range(300)
        ])
        
        # 2. Giếng bơm
        well = Line(UP*2.5, DOWN*1.5, color=WHITE, stroke_width=4).shift(LEFT * 3)
        well_label = Text("Giếng bơm", font_size=16, color=WHITE).next_to(well, UP, buff=0.1)
        
        # 3. CO2 Plume (Dòng chảy len lỏi) - Nhiều ellipse chồng lên nhau tạo gradient
        plume_group = VGroup()
        for i in range(5):
            scale = 1.0 - i * 0.15
            opacity = 0.5 - i * 0.08
            ellipse = Ellipse(
                width=2.0 * scale,
                height=1.2 * scale,
                fill_color=CYAN,
                fill_opacity=opacity,
                stroke_width=0
            )
            ellipse.shift(RIGHT * i * 0.4)
            plume_group.add(ellipse)

        plume_group.move_to(well.get_bottom() + DOWN*0.3)
        
        plume_spread = plume_group.copy().scale(2.5).shift(RIGHT*1.5)
        plume_base = plume_group.copy().scale(0.01).move_to(well.get_bottom())

        self.play_timed("b1_setup", 0, 5, FadeIn(title), FadeIn(rock_matrix), Create(well), FadeIn(well_label))
        
        # CO2 bắt đầu bơm và lan tỏa
        self.add(plume_base)
        self.play_timed("b1_plume_spread", 5, 15, 
                        ReplacementTransform(plume_base, plume_spread))
        
        # Time counter chạy cực nhanh (Thể hiện tốc độ NO)
        time_counter = Integer(0, unit=" Years", font_size=24, color=YELLOW).to_corner(DR, buff=0.5)
        time_counter.add_updater(lambda m, dt: m.set_value(m.get_value() + dt * 20))
        self.play_timed("b1_time_lapse", 15, 20, FadeIn(time_counter))
        
        # Speed Metric
        speed_box = VGroup(
            RoundedRectangle(width=4.5, height=1.6, corner_radius=0.1, stroke_color=NVIDIA_GREEN, fill_color=BLACK, fill_opacity=0.8),
            Text("Nhanh hơn 700,000x\nso với Solver", font_size=22, color=NVIDIA_GREEN, weight=BOLD)
        )
        speed_box[1].move_to(speed_box[0])
        speed_box.shift(RIGHT * 2.5 + UP * 1.5)
        
        self.play_timed("b1_speed", 20, 25, FadeIn(speed_box, scale=0.8), Flash(speed_box, color=NVIDIA_GREEN))
        self.wait_timed("b1_hold", 25, 45)
        time_counter.clear_updaters()

        # ═══════════════════════════════════════════════════════════════
        # BEAT 2: [19:55–20:25] Uncertainty & The "Mesh" Epiphany (30s)
        # ═══════════════════════════════════════════════════════════════
        self.play_timed("clear_b1", 45, 47, *[FadeOut(m) for m in [title, rock_matrix, well, well_label, plume_spread, time_counter, speed_box]])
        
        ens_title = Text("Đánh giá rủi ro: 10,000 Kịch bản Địa chất", font_size=28, color=BLUE_C, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 47, 49, FadeIn(ens_title))
        
        # ── FIX 1: RISK HEATMAP THỰC THỤ (thay vì 15 ellipse chồng lên nhau) ──
        # Dùng grid cells với màu gradient: xanh (thấp) → vàng → đỏ (cao)
        # Thể hiện xác suất CO2 lan đến từng vùng
        heatmap_grid = VGroup()
        grid_size = 0.25
        n_cols, n_rows = 24, 10
        center_x, center_y = 0, -1.5

        for i in range(n_cols):
            for j in range(n_rows):
                x = center_x + (i - n_cols/2) * grid_size
                y = center_y + (j - n_rows/2) * grid_size
                
                # Tính "xác suất" dựa trên khoảng cách từ tâm giếng (bên trái)
                dist_from_well = np.sqrt((x + 3)**2 + (y - center_y)**2)
                max_dist = 5.0
                probability = max(0, 1 - dist_from_well / max_dist)
                
                # Gradient màu: xanh → vàng → đỏ
                if probability > 0.6:
                    color = interpolate_color(RED, YELLOW, (probability - 0.6) / 0.4)
                elif probability > 0.3:
                    color = interpolate_color(YELLOW, BLUE_C, (probability - 0.3) / 0.3)
                else:
                    color = interpolate_color(BLUE_E, BLUE_C, probability / 0.3)
                
                cell = Square(side_length=grid_size * 0.9, fill_color=color, 
                              fill_opacity=probability * 0.7, stroke_width=0)
                cell.move_to([x, y, 0])
                heatmap_grid.add(cell)

        risk_label = Text("Bản đồ xác suất lan tỏa CO₂", font_size=18, color=YELLOW).next_to(heatmap_grid, DOWN, buff=0.3)
        sim_counter = Text("10,000 simulations / 2s", font_size=16, color=GREEN_SCREEN).to_edge(DOWN, buff=0.3)

        self.play_timed("b2_heatmap", 49, 55, 
                        LaggedStart(*[FadeIn(cell, scale=0.3) for cell in heatmap_grid], lag_ratio=0.01),
                        FadeIn(risk_label), FadeIn(sim_counter))

        # ── FIX 2: HEATMAP "TAN RÃ" THÀNH PARTICLES CÓ TỔ CHỨC ──
        # Thay vì random dots, lấy các cell có probability cao và biến thành particles
        # Các particles này sẽ có vị trí gần giống heatmap ban đầu
        high_prob_particles = VGroup()
        for cell in heatmap_grid:
            prob = cell.fill_opacity / 0.7
            if prob > 0.4:  # Chỉ lấy cells có xác suất > 40%
                # Mỗi cell tạo 1-2 particles
                n_particles = 2 if prob > 0.7 else 1
                for _ in range(n_particles):
                    p = Dot(cell.get_center(), radius=0.04, color=YELLOW, fill_opacity=0.8)
                    high_prob_particles.add(p)

        # Animation: Heatmap fade out, particles nổi lên từ vị trí cũ
        self.play_timed("b2_disintegrate", 55, 58,
                        heatmap_grid.animate.set_opacity(0.2),
                        FadeIn(high_prob_particles, scale=0.5),
                        FadeOut(risk_label), FadeOut(sim_counter), FadeOut(ens_title))

        # ── FIX 3: PARTICLES TỤ LẠI THÀNH STRUCTURED POINT CLOUD ──
        # Thay vì random, particles tụ lại thành hình ellipse (chuẩn bị morph sang airfoil)
        # Tạo target positions theo hình ellipse
        n_target_points = len(high_prob_particles)
        ellipse_a, ellipse_b = 2.5, 1.0  # bán trục
        target_points = []
        for i in range(n_target_points):
            angle = 2 * PI * i / n_target_points
            # Thêm noise nhẹ để trông tự nhiên
            r = 1.0 + np.random.uniform(-0.1, 0.1)
            x = ellipse_a * r * np.cos(angle)
            y = ellipse_b * r * np.sin(angle) * 0.5  # dẹt xuống
            target_points.append([x, y - 1.5, 0])

        # Animation: particles bay đến vị trí mới (tạo hình ellipse)
        target_dots = VGroup()
        for i, p in enumerate(high_prob_particles):
            target_dot = Dot(target_points[i], radius=0.04, color=GREEN_SCREEN, fill_opacity=0.8)
            target_dots.add(target_dot)

        self.play_timed("b2_form_cloud", 58, 62,
                        Transform(high_prob_particles, target_dots),
                        FadeOut(heatmap_grid))

        # ── FIX 4: MORPH POINT CLOUD → NACA AIRFOIL ──
        epiphany_text = Text("Với GNO, tất cả chỉ là Point Clouds", font_size=24, color=WHITE).to_edge(UP, buff=0.4)
        self.play_timed("b2_epiphany", 62, 64, FadeIn(epiphany_text))

        # Tạo NACA airfoil points
        aero_pts = get_naca_airfoil_points(thickness=0.15, chord=4.0, center=[0, -1.5, 0])

        # Pad hoặc crop high_prob_particles để bằng số lượng với aero_pts
        while len(high_prob_particles) < len(aero_pts):
            high_prob_particles.add(Dot(high_prob_particles[-1].get_center(), radius=0.04, color=GREEN_SCREEN))
        aero_cloud = VGroup(*[Dot(p, radius=0.04, color=GREEN_SCREEN) for p in aero_pts[:len(high_prob_particles)]])

        # Morph: ellipse point cloud → airfoil point cloud
        self.play_timed("b2_morph_airfoil", 64, 68,
                        Transform(high_prob_particles, aero_cloud))

        # Nối các điểm lại thành airfoil hoàn chỉnh
        aero_shape = VMobject(color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=0.3)
        aero_shape.set_points_smoothly(aero_pts[:len(high_prob_particles)])

        self.play_timed("b2_form_shape", 68, 72,
                        Create(aero_shape),
                        high_prob_particles.animate.set_opacity(0.3),
                        FadeOut(epiphany_text))

        # Hold để viewer nhìn rõ airfoil
        self.wait_timed("b2_hold", 72, 75)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3: [20:25–20:55] Hybrid Pipeline → Real-time CFD (30s)
        # ═══════════════════════════════════════════════════════════════

        # FIX 1: CLEAR TẤT CẢ từ Beat 2 (bao gồm aero_shape!)
        self.play_timed("clear_b2", 75, 77, 
                        *[FadeOut(m) for m in [high_prob_particles, epiphany_text, aero_shape]])

        # ── PIPELINE: 3 blocks với data flow ──
        pipeline_title = Text("Kiến trúc Hybrid: GNO + FNO", font_size=28, 
                              color=GREEN_SCREEN, weight=BOLD).to_edge(UP, buff=0.4)

        # Block 1: Irregular Mesh (điểm loạn xạ)
        np.random.seed(42)
        irregular_pts = VGroup(*[
            Dot([np.random.uniform(-1.5, 1.5), np.random.uniform(-0.8, 0.8), 0], 
                radius=0.04, color=CYAN) 
            for _ in range(40)
        ])
        irregular_box = SurroundingRectangle(irregular_pts, color=CYAN, buff=0.3, stroke_width=2)
        irregular_label = Text("GNO\n(Irregular Mesh)", font_size=14, color=CYAN).next_to(irregular_box, DOWN, buff=0.2)

        # Block 2: Regular Grid (lưới đều)
        regular_grid = VGroup()
        for x in np.linspace(-1.2, 1.2, 8):
            for y in np.linspace(-0.6, 0.6, 5):
                regular_grid.add(Dot([x, y, 0], radius=0.04, color=YELLOW))
        regular_box = SurroundingRectangle(regular_grid, color=YELLOW, buff=0.3, stroke_width=2)
        regular_label = Text("FNO\n(Regular Grid / FFT)", font_size=14, color=YELLOW).next_to(regular_box, DOWN, buff=0.2)

        # Block 3: Decode → OUTPUT là airfoil + pressure field
        decoded_pts = irregular_pts.copy().set_color(GREEN_SCREEN)
        decoded_box = SurroundingRectangle(decoded_pts, color=GREEN_SCREEN, buff=0.3, stroke_width=2)
        decoded_label = Text("Decode\n(Surface Output)", font_size=14, color=GREEN_SCREEN).next_to(decoded_box, DOWN, buff=0.2)

        pipeline_blocks = VGroup(
            VGroup(irregular_pts, irregular_box, irregular_label),
            VGroup(regular_grid, regular_box, regular_label),
            VGroup(decoded_pts, decoded_box, decoded_label)
        ).arrange(RIGHT, buff=1.5)

        arr1_start = irregular_box.get_right()
        arr1_end = regular_box.get_left()
        arr1_end[1] = arr1_start[1]  # force straight
        
        arr2_start = regular_box.get_right()
        arr2_end = decoded_box.get_left()
        arr2_end[1] = arr2_start[1]  # force straight

        arrows = VGroup(
            Arrow(arr1_start, arr1_end, color=WHITE, buff=0.2),
            Arrow(arr2_start, arr2_end, color=WHITE, buff=0.2)
        )
        arrow_label1 = Text("Rasterize", font_size=12, color=WHITE).next_to(arrows[0], UP, buff=0.1)
        arrow_label2 = Text("Inverse FFT", font_size=12, color=WHITE).next_to(arrows[1], UP, buff=0.1)

        pipeline = VGroup(pipeline_blocks, arrows, arrow_label1, arrow_label2)
        pipeline.move_to(ORIGIN).scale(1.2).shift(DOWN * 0.2)

        self.play_timed("b3_pipeline", 77, 82,
                        FadeIn(pipeline_title),
                        LaggedStart(*[FadeIn(p) for p in pipeline_blocks], lag_ratio=0.3),
                        Create(arrows),
                        FadeIn(arrow_label1), FadeIn(arrow_label2))

        # ── DATA FLOW: particles chạy qua pipeline ──
        data_packets = VGroup(*[Dot(radius=0.06, color=WHITE) for _ in range(3)])
        for i, packet in enumerate(data_packets):
            packet.move_to(irregular_box.get_left())

        self.play_timed("b3_data_flow", 82, 85,
                        *[MoveAlongPath(packet, 
                                       Line(irregular_box.get_center(), decoded_box.get_center()),
                                       rate_func=smooth) 
                          for packet in data_packets])

        # ── TRANSITION: Pipeline output → CFD visualization ──
        self.play_timed("b3_pipeline_to_cfd", 85, 88,
                        FadeOut(pipeline_title),
                        FadeOut(pipeline),
                        FadeOut(data_packets))

        # ── CFD: Airfoil + Streamlines + Pressure ──
        # NACA airfoil thật
        naca_pts = get_naca_airfoil_points(thickness=0.12, chord=3.0, center=ORIGIN)
        airfoil = VMobject(color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=0.8)
        airfoil.set_points_smoothly(naca_pts)

        # FIX 2: Pressure field là "halo" bao quanh airfoil (không phải hình riêng biệt)
        # Tạo pressure field bằng cách scale airfoil lên và đổi màu
        pressure_field = airfoil.copy().set_fill(color=RED, opacity=0.4).set_stroke(width=0)
        pressure_field.scale(1.3)  # Lớn hơn airfoil 30%

        # FIX 3: Streamlines uốn cong QUA airfoil (không phải đi trên/dưới)
        streamlines = VGroup()
        for y_off in np.linspace(-1.5, 1.5, 9):
            if abs(y_off) < 0.15:
                continue
            # Control points uốn cong mạnh hơn khi gần airfoil
            bend_factor = 1.0 + 0.5 * np.exp(-abs(y_off) * 2)  # Uốn cong nhiều hơn khi gần y=0
            ctrl2 = RIGHT * 1.5 + UP * (y_off * bend_factor)
            path = CubicBezier(
                LEFT * 4 + UP * y_off,
                LEFT * 1.5 + UP * y_off,
                ctrl2,
                RIGHT * 4 + UP * y_off
            )
            streamlines.add(path)
        streamlines.set_color(BLUE_D).set_stroke(width=2, opacity=0.6)

        flow_arrow = Arrow(LEFT * 3.5, LEFT * 2, color=WHITE, buff=0).shift(UP * 0.8)

        cfd_group = VGroup(airfoil, pressure_field, streamlines, flow_arrow)

        self.play_timed("b3_cfd_setup", 88, 92, FadeIn(cfd_group))

        # ─ REAL-TIME MORPHING: Thiết kế thay đổi → CFD cập nhật ngay ──
        new_naca_pts = get_naca_airfoil_points(thickness=0.20, chord=3.0, center=ORIGIN)
        new_airfoil = VMobject(color=WHITE, stroke_width=3, fill_color=BLACK, fill_opacity=0.8)
        new_airfoil.set_points_smoothly(new_naca_pts)

        # Pressure field mới cũng là halo
        new_pressure_field = new_airfoil.copy().set_fill(color=ORANGE, opacity=0.5).set_stroke(width=0)
        new_pressure_field.scale(1.4)  # Lớn hơn vì cánh dày hơn

        # Streamlines mới uốn cong mạnh hơn
        new_streamlines = VGroup()
        for y_off in np.linspace(-1.5, 1.5, 9):
            if abs(y_off) < 0.25:
                continue
            bend_factor = 1.0 + 0.8 * np.exp(-abs(y_off) * 1.5)  # Uốn cong mạnh hơn
            ctrl2 = RIGHT * 1.5 + UP * (y_off * bend_factor)
            path = CubicBezier(
                LEFT * 4 + UP * y_off,
                LEFT * 1.5 + UP * y_off,
                ctrl2,
                RIGHT * 4 + UP * y_off
            )
            new_streamlines.add(path)
        new_streamlines.set_color(BLUE_D).set_stroke(width=2, opacity=0.6)

        iter_counter = Text("Design Iteration: 1 → 50", font_size=20, color=GREEN_SCREEN).to_edge(DOWN, buff=0.5)
        speed_badge = Text("Inference: 0.05s | Tốc độ x140,000", font_size=18, color=GREEN_SCREEN, weight=BOLD).next_to(iter_counter, UP, buff=0.2)

        self.play_timed("b3_morph", 92, 98,
                        Transform(airfoil, new_airfoil),
                        Transform(pressure_field, new_pressure_field),
                        Transform(streamlines, new_streamlines),
                        FadeIn(iter_counter),
                        FadeIn(speed_badge),
                        Flash(speed_badge, color=GREEN_SCREEN, flash_radius=1.5))

        self.wait_timed("b3_hold", 98, 103)

        self.play_timed("cut", 103, 105, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
