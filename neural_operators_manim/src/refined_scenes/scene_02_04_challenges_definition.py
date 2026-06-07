"""
Scene 2.4 — Thách thức & Định nghĩa Neural Operator
Source: Director's Cut
Global time: 6:40 – 7:30
Duration: 50s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0204_ChallengesAndDefinition(TimedScene):
    SCRIPT_ID = "2.4"
    SCRIPT_TITLE = "Thách thức & Định nghĩa Neural Operator"
    SCRIPT_START = 400.0
    SCRIPT_END = 450.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1A: [6:40-6:52] Discretization Invariance (Local 0 - 12s)
        # ═══════════════════════════════════════════════════════════════
        
        di_label = Text("Discretization Invariance", font_size=36, color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=1.0)
        
        # 1. CAD Mesh (Triangles)
        cad_mesh = VGroup()
        for i in range(6):
            for j in range(6):
                triangle = Polygon(
                    np.array([-0.4, -0.4, 0]),
                    np.array([0.4, -0.4, 0]),
                    np.array([0, 0.4, 0]),
                    stroke_color=INPUT, stroke_width=1, fill_color=INPUT, fill_opacity=0.3
                ).shift(RIGHT * (i - 2.5) * 0.8 + UP * (j - 2.5) * 0.8)
                if (i+j) % 2 == 1:
                    triangle.rotate(PI, about_point=triangle.get_center())
                cad_mesh.add(triangle)
        cad_mesh.move_to(ORIGIN)
                
        # 2. Globe mesh (Satellite)
        globe_mesh = VGroup()
        circle = Circle(radius=2.5, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.1)
        globe_mesh.add(circle)
        for i in range(1, 5):
            ellipse = Ellipse(width=5, height=5 - i, stroke_color=PURPLE, stroke_width=1)
            globe_mesh.add(ellipse)
            ellipse2 = Ellipse(width=5 - i, height=5, stroke_color=PURPLE, stroke_width=1)
            globe_mesh.add(ellipse2)
        globe_mesh.move_to(ORIGIN)
            
        # 3. Sparse sensors (Dots)
        sparse_sensors = VGroup()
        np.random.seed(42)
        for _ in range(80):
            pt = np.array([np.random.uniform(-3, 3), np.random.uniform(-3, 3), 0])
            if np.linalg.norm(pt) <= 2.5:
                sparse_sensors.add(Dot(pt, color=OPERATOR, radius=0.08))
        sparse_sensors.move_to(ORIGIN)
        
        self.play_timed("di_title", 0, 1.5, Write(di_label))
        self.play_timed("cad_mesh", 1.5, 3.5, Create(cad_mesh))
        
        self.play_timed("morph_to_globe", 5, 7, Transform(cad_mesh, globe_mesh))
        
        self.play_timed("morph_to_sparse", 8.5, 10.5, Transform(cad_mesh, sparse_sensors))
        
        self.play_timed("clear_beat1a", 11.5, 12, FadeOut(cad_mesh), FadeOut(di_label))

        # ═══════════════════════════════════════════════════════════════
        # Beat 1B: [6:52-7:05] Continuous Query (Local 12 - 25s)
        # ═══════════════════════════════════════════════════════════════
        
        cq_label = Text("Continuous Query", font_size=36, color=OPERATOR, weight=BOLD).to_edge(UP, buff=1.0)
        
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 4, 1], x_length=10, y_length=4).shift(DOWN * 0.5)
        curve = axes.plot(lambda x: 2 + np.sin(x), color=INPUT, stroke_width=4)
        
        x_tracker = ValueTracker(1)
        
        # Tangent line
        def get_tangent():
            x = x_tracker.get_value()
            dx = 0.01
            p1 = axes.c2p(x, 2 + np.sin(x))
            p2 = axes.c2p(x + dx, 2 + np.sin(x + dx))
            angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
            line = Line(LEFT, RIGHT, color=WARNING, stroke_width=4).scale(1.5).rotate(angle).move_to(p1)
            return line
            
        tangent = always_redraw(get_tangent)
        
        # Area
        def get_area():
            x = x_tracker.get_value()
            # Ensure max > min to avoid ValueError
            x_end = max(1.01, x)
            return axes.get_area(curve, x_range=[1, x_end], color=PURPLE, opacity=0.4)
            
        area = always_redraw(get_area)
        
        # Caliper Crosshair
        def get_caliper():
            x = x_tracker.get_value()
            p = axes.c2p(x, 2 + np.sin(x))
            cross = VGroup(
                Line(p + UP*0.3, p + DOWN*0.3, color=WHITE, stroke_width=3),
                Line(p + LEFT*0.3, p + RIGHT*0.3, color=WHITE, stroke_width=3)
            )
            return cross
            
        caliper = always_redraw(get_caliper)
        
        # Labels
        def get_labels():
            x = x_tracker.get_value()
            p = axes.c2p(x, 2 + np.sin(x))
            d_text = MathTex("f'(x)", font_size=24, color=WARNING).next_to(p, UP+RIGHT, buff=0.2)
            i_text = MathTex(r"\int f(x) dx", font_size=24, color=PURPLE).move_to(axes.c2p(max(1.5, x/2 + 0.5), 1.0))
            return VGroup(d_text, i_text)
            
        labels = always_redraw(get_labels)
        
        self.play_timed("cq_setup", 12.5, 14, FadeIn(cq_label), Create(axes), Create(curve))
        self.play_timed("caliper_in", 14.5, 15.5, FadeIn(caliper), FadeIn(tangent), FadeIn(area), FadeIn(labels))
        
        # Slide caliper
        self.play_timed("slide_caliper", 16, 21, x_tracker.animate.set_value(9), rate_func=smooth)
        
        self.play_timed("clear_beat1b", 24, 25, 
                        *[FadeOut(m) for m in [cq_label, axes, curve, caliper, tangent, area, labels]])

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [7:05-7:30] The Mathematical Manifesto (Local 25 - 50s)
        # ═══════════════════════════════════════════════════════════════
        
        manifesto_title = Text("Bản chất của Neural Operator", font_size=36, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        
        # 3 Pillars
        pillars = VGroup()
        texts = [
            "", # placeholder for index 0
            "2. Độc lập lưới rời rạc",
            "3. Hội tụ giới hạn liên tục"
        ]
        
        for i in range(3):
            # Make it look like a glowing pillar / stone tablet
            pillar_box = RoundedRectangle(
                width=7.5, height=1.0, corner_radius=0.1, 
                stroke_color=NVIDIA_GREEN, stroke_width=2, 
                fill_color=CARD_BG, fill_opacity=0.9
            )
            
            if i == 0:
                t = VGroup(
                    Text("1. Ánh xạ Function", font_size=24, color=WHITE, weight=BOLD),
                    MathTex(r"\rightarrow", font_size=24, color=WHITE),
                    Text("Function", font_size=24, color=WHITE, weight=BOLD)
                ).arrange(RIGHT, buff=0.1)
            else:
                t = Text(texts[i], font_size=24, color=WHITE, weight=BOLD)
                
            t.move_to(pillar_box)
            t.align_to(pillar_box, LEFT).shift(RIGHT * 0.5)
            pillars.add(VGroup(pillar_box, t))
            
        pillars.arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)
        
        # Visual for Continuum Limit (Right side)
        local_axes = Axes(x_range=[0, 4, 1], y_range=[-1.5, 1.5, 1], x_length=5, y_length=4)
        local_axes.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        grid_bg = NumberPlane(
            x_range=[0, 4, 0.5], y_range=[-1.5, 1.5, 0.5], 
            x_length=5, y_length=4, 
            background_line_style={"stroke_color": TEAL, "stroke_width": 1, "stroke_opacity": 0.4}
        ).move_to(local_axes.get_center())
        
        # Noisy curve (Grid artifacts)
        np.random.seed(42)
        x_vals = np.linspace(0, 4, 15)
        y_vals = np.sin(x_vals * 1.5) + np.random.normal(0, 0.3, len(x_vals))
        
        noisy_curve = VGroup()
        for i in range(len(x_vals)-1):
            p1 = local_axes.c2p(x_vals[i], y_vals[i])
            p2 = local_axes.c2p(x_vals[i+1], y_vals[i+1])
            # Step function look
            noisy_curve.add(Line(p1, local_axes.c2p(x_vals[i+1], y_vals[i]), color=WARNING, stroke_width=3))
            noisy_curve.add(Line(local_axes.c2p(x_vals[i+1], y_vals[i]), p2, color=WARNING, stroke_width=3))
            
        grid_hallucination_text = Text("Ảo giác của lưới", font_size=18, color=WARNING).next_to(local_axes, UP, buff=0.2)
        
        # Smooth curve
        smooth_curve = local_axes.plot(lambda x: np.sin(x * 1.5), color=NVIDIA_GREEN, stroke_width=5)
        continuum_text = Text("Hội tụ liên tục", font_size=18, color=NVIDIA_GREEN).next_to(local_axes, UP, buff=0.2)
        
        self.play_timed("manifesto_title", 25.5, 27, FadeIn(manifesto_title))
        
        # Pillars appear
        self.play_timed("pillar_1", 27, 28.5, FadeIn(pillars[0], shift=UP*0.2))
        self.play_timed("pillar_2", 29, 30.5, FadeIn(pillars[1], shift=UP*0.2))
        self.play_timed("pillar_3", 31, 32.5, FadeIn(pillars[2], shift=UP*0.2))
        
        # Visual appears
        self.play_timed("grid_visual_in", 33, 35, 
                        FadeIn(local_axes), FadeIn(grid_bg), 
                        Create(noisy_curve), FadeIn(grid_hallucination_text))
                        
        # Transform to smooth
        self.play_timed("transform_continuum", 37, 40,
                        ReplacementTransform(noisy_curve, smooth_curve),
                        ReplacementTransform(grid_hallucination_text, continuum_text),
                        grid_bg.animate.set_opacity(0.1))
                        
        self.wait_timed("hold_end", 40, 49)
        self.play_timed("cut", 49, 50, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
