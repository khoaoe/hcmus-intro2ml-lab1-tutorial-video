"""
Scene 5.2 — Carbon Storage & Khí động học công nghiệp
Source: original_outline.tex, Section 5, Scene 5.2
Global time: 19:10 – 20:55
Duration: 105s
"""
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0502_CarbonAero(TimedScene):
    SCRIPT_ID = "5.2"
    SCRIPT_TITLE = "Carbon Storage & Khí động học"
    SCRIPT_START = 1150.0
    SCRIPT_END = 1255.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [19:10–19:55] Carbon Storage & 700,000x ──
        title = Text("Carbon Capture & Storage", font_size=28,
                     color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.4)

        # 2D Cross-section - fade in từng lớp
        layers = VGroup()
        layer_colors = [GRAY_B, GRAY_C, GRAY_D, BLUE_E]
        layer_heights = [1.2, 1.0, 1.1, 1.5]
        layer_labels = ["Lớp đá bề mặt", "Đá trầm tích", "Đá mẹ", "Vỉa chứa CO₂"]
        y_pos = 0
        for i, (color, h, label) in enumerate(zip(layer_colors, layer_heights, layer_labels)):
            layer = Rectangle(width=10, height=h, fill_color=color, fill_opacity=0.6, 
                              stroke_color=WHITE, stroke_width=1, stroke_opacity=0.3)
            layer.shift(DOWN * y_pos)
            layer_label = Text(label, font_size=12, color=WHITE).move_to(layer)
            layers.add(VGroup(layer, layer_label))
            y_pos += h
        layers.shift(DOWN * 0.5)

        # Injection well - vẽ từ trên xuống
        well = Line(UP*2.5, DOWN*3.8, color=WHITE, stroke_width=3)
        well.shift(LEFT * 2)
        well_label = Text("Giếng bơm CO₂", font_size=14, color=WHITE).next_to(well, UP, buff=0.2)

        # CO2 particles flowing down the well
        co2_particles = VGroup()
        for i in range(8):
            particle = Dot(radius=0.08, color="#00FFFF", fill_opacity=0.8)
            particle.move_to(well.get_top() + DOWN * (i * 0.5))
            co2_particles.add(particle)

        # CO2 Plume - bắt đầu nhỏ, mở rộng
        plume_start = Ellipse(width=0.3, height=0.2, color="#00FFFF", 
                              fill_color="#00FFFF", fill_opacity=0.4, stroke_width=2)
        plume_start.move_to(well.get_bottom() + UP*0.2)
        
        plume_end = Ellipse(width=4.5, height=2.0, color="#00FFFF", 
                            fill_color="#00FFFF", fill_opacity=0.25, stroke_width=2)
        plume_end.move_to(well.get_bottom() + UP*0.2)

        self.play_timed("b1_title", 0, 2, FadeIn(title))
        
        # Layers fade in tuần tự
        for i, layer in enumerate(layers):
            start = 2 + i * 0.5
            end = start + 0.5
            self.play_timed(f"b1_layer_{i}", start, end, FadeIn(layer))

        # Well vẽ từ trên xuống
        self.play_timed("b1_well", 4, 6, Create(well), FadeIn(well_label))
        
        # CO2 particles chảy xuống giếng
        self.play_timed("b1_co2_flow", 6, 10,
                        *[particle.animate.move_to(well.get_bottom() + UP*0.2) 
                          for particle in co2_particles])

        # Plume mở rộng thực sự
        self.play_timed("b1_plume_expand", 10, 18,
                        Transform(plume_start, plume_end),
                        FadeOut(co2_particles))

        # Speed metric với impact
        speed_box = VGroup(
            RoundedRectangle(width=3.5, height=1.0, corner_radius=0.1,
                             stroke_color=NVIDIA_GREEN, fill_color=NVIDIA_GREEN, fill_opacity=0.15),
            Text("Nhanh hơn 700,000 lần", font_size=22, color=NVIDIA_GREEN, weight=BOLD)
        )
        speed_box[1].move_to(speed_box[0])
        speed_box.shift(RIGHT * 3.5 + UP * 1.8)

        self.play_timed("b1_speed", 18, 22, 
                        FadeIn(speed_box, scale=0.8),
                        Flash(speed_box, color=NVIDIA_GREEN, flash_radius=1.5))
        
        # Thêm text giải thích
        speed_note = Text("So với solver truyền thống", font_size=16, color=MUTED).next_to(speed_box, DOWN, buff=0.2)
        self.play_timed("b1_speed_note", 22, 25, FadeIn(speed_note))
        
        # Hold ngắn hơn, thêm pulse effect cho plume
        self.play_timed("b1_pulse", 25, 30,
                        plume_end.animate.set_fill(opacity=0.35).scale(1.05),
                        rate_func=there_and_back)
        
        self.wait_timed("b1_hold", 30, 45)

        # ── Beat 2: [19:55–20:25] Uncertainty Scenarios → Heatmap → Aero Transition ──
        self.play_timed("clear_b1", 45, 46,
                        *[FadeOut(m) for m in [title, layers, well, well_label, plume_end, 
                                               speed_box, speed_note]])

        ens_title = Text("Đánh giá rủi ro: Hàng nghìn kịch bản", font_size=24,
                         color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.5)

        # Multiple plume boundaries - xuất hiện tuần tự
        np.random.seed(42)
        scenario_outlines = VGroup()
        for i in range(8):
            dx = np.random.uniform(-0.8, 0.8)
            dy = np.random.uniform(-0.3, 0.3)
            w = np.random.uniform(2.0, 4.0)
            h = np.random.uniform(0.6, 1.2)
            outline = Ellipse(width=w, height=h, color="#00FFFF", stroke_width=1.5, stroke_opacity=0.4)
            outline.move_to(DOWN * 2.5 + RIGHT * dx + UP * dy)
            scenario_outlines.add(outline)

        self.play_timed("b2_title", 46, 48, FadeIn(ens_title))
        
        # Scenarios xuất hiện từng cái
        for i, outline in enumerate(scenario_outlines):
            start = 48 + i * 0.5
            end = start + 0.5
            self.play_timed(f"b2_scenario_{i}", start, end, Create(outline))

        # Merge into probability heatmap
        heatmap = VGroup()
        for i, (w, h, op) in enumerate(zip([4.5, 3.5, 2.5, 1.5], [1.4, 1.0, 0.7, 0.4], [0.1, 0.2, 0.35, 0.5])):
            contour = Ellipse(width=w, height=h, color=RED, fill_color=RED, 
                              fill_opacity=op, stroke_width=1.5, stroke_opacity=op+0.2)
            contour.move_to(DOWN * 2.5)
            heatmap.add(contour)
        
        risk_label = Text("Bản đồ rủi ro lan tỏa", font_size=18, color=RED).next_to(heatmap, DOWN, buff=0.3)

        self.play_timed("b2_heatmap", 53, 58, 
                        Transform(scenario_outlines, heatmap),
                        FadeIn(risk_label))

        # Match cut: Heatmap contour morphs into Airfoil shape
        airfoil_curve = ParametricFunction(
            lambda t: np.array([
                2.5 * (t + 0.1),
                0.8 * np.sqrt(t) * (1 - t) * 5,
                0
            ]), t_range=[0, 1, 0.01], color=WHITE, stroke_width=2.5
        ).shift(RIGHT * 2 + UP * 0.5)

        self.play_timed("b2_morph_aero", 58, 65,
                        Transform(heatmap[0], airfoil_curve),
                        FadeOut(heatmap[1:]), FadeOut(risk_label), FadeOut(ens_title))
        self.wait_timed("b2_hold", 65, 75)

        # ── Beat 3: [20:25–20:55] Hybrid Pipeline & Real-time Design ──
        pipeline_title = Text("Killer App Công nghiệp: Hybrid Pipeline", font_size=24,
                              color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)

        # Pipeline blocks
        blocks_data = [
            ("Mesh 3D\nBất quy tắc", INPUT),
            ("GNO", PURPLE),
            ("Lưới đều\n(Rasterize)", GRID),
            ("FNO (FFT)", OUTPUT),
            ("Decode\nNgược", NVIDIA_GREEN)
        ]
        pipeline = VGroup()
        for name, color in blocks_data:
            box = RoundedRectangle(width=1.6, height=1.2, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.7)
            txt = Text(name, font_size=13, color=color, weight=BOLD).move_to(box)
            pipeline.add(VGroup(box, txt))
        pipeline.arrange(RIGHT, buff=0.4).shift(UP * 1.2)

        # Arrows between blocks
        arrows = VGroup()
        for i in range(len(pipeline)-1):
            arr = Arrow(pipeline[i].get_right(), pipeline[i+1].get_left(), 
                        color=WHITE, stroke_width=2, buff=0.05)
            arrows.add(arr)

        self.play_timed("b3_title_pipeline", 75, 78, FadeIn(pipeline_title), FadeIn(pipeline), FadeIn(arrows))

        # Data packets flowing through pipeline
        packets = VGroup(*[Dot(radius=0.08, color=YELLOW) for _ in range(5)])
        def flow_packet(packet, idx):
            path = VMobject()
            path.set_points_as_corners([pipeline[i].get_center() for i in range(len(pipeline))])
            return MoveAlongPath(packet, path, rate_func=smooth)

        self.play_timed("b3_flow", 78, 83, 
                        *[flow_packet(p, i) for i, p in enumerate(packets)])

        # Real-time Airfoil iteration
        design_title = Text("Tối ưu thiết kế Real-time", font_size=20, color=TEXT).shift(DOWN * 0.5)
        
        # Base airfoil
        base_airfoil = ParametricFunction(
            lambda t: np.array([2*(t-0.5), 0.3*np.sin(PI*t)*np.exp(-2*(t-0.5)**2), 0]),
            t_range=[0, 1, 0.01], color=WHITE, stroke_width=2
        ).shift(DOWN * 1.8)
        
        # Pressure field overlay
        pressure_field = VMobject(fill_color=RED, fill_opacity=0.3, stroke_width=0)
        pressure_field.set_points_smoothly([
            base_airfoil.get_left() + UP*0.5, base_airfoil.get_top() + UP*0.3,
            base_airfoil.get_right() + UP*0.2, base_airfoil.get_right() + DOWN*0.2,
            base_airfoil.get_bottom() + DOWN*0.3, base_airfoil.get_left() + DOWN*0.4
        ])

        self.play_timed("b3_design_setup", 83, 86, FadeIn(design_title), Create(base_airfoil), FadeIn(pressure_field))

        # Morph airfoil + instant pressure update
        morphed_airfoil = ParametricFunction(
            lambda t: np.array([2*(t-0.5), 0.45*np.sin(PI*t)*np.exp(-1.5*(t-0.5)**2), 0]),
            t_range=[0, 1, 0.01], color=WHITE, stroke_width=2
        ).shift(DOWN * 1.8)
        
        morphed_pressure = VMobject(fill_color=ORANGE, fill_opacity=0.4, stroke_width=0)
        morphed_pressure.set_points_smoothly([
            morphed_airfoil.get_left() + UP*0.6, morphed_airfoil.get_top() + UP*0.4,
            morphed_airfoil.get_right() + UP*0.3, morphed_airfoil.get_right() + DOWN*0.3,
            morphed_airfoil.get_bottom() + DOWN*0.4, morphed_airfoil.get_left() + DOWN*0.5
        ])

        iter_counter = Text("Iteration: 1 → 50", font_size=18, color=NVIDIA_GREEN).next_to(design_title, DOWN, buff=0.3)
        speed_note = Text("Nhanh hơn 140,000 lần | Inference < 0.1s", font_size=16, color=NVIDIA_GREEN).to_edge(DOWN, buff=0.3)

        self.play_timed("b3_morph", 86, 92,
                        Transform(base_airfoil, morphed_airfoil),
                        Transform(pressure_field, morphed_pressure),
                        FadeIn(iter_counter))
        
        self.play_timed("b3_speed_note", 92, 95, FadeIn(speed_note), Flash(speed_note, color=NVIDIA_GREEN))
        self.wait_timed("b3_hold", 95, 103)

        self.play_timed("cut", 103, 105, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
