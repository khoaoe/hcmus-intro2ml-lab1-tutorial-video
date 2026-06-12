from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

class Scene0604_Collaboration_Recap(TimedScene):
    SCRIPT_ID = "6.4"
    SCRIPT_TITLE = "Thách thức hợp tác & Recap 3 nguyên tắc"
    SCRIPT_START = 1675.0
    SCRIPT_END = 1735.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Thách thức: Xây cầu nối giữa hai thế giới", font_size=28,
                     color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b1_title", 0, 2, FadeIn(title))

        physics_box = RoundedRectangle(
            width=4.5, height=3.0, corner_radius=0.2,
            stroke_color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.1, stroke_width=2.5
        ).shift(LEFT * 3.8 + DOWN * 0.3)
        
        physics_header = Text("PHYSICS WORLD", font_size=18, color=BLUE_C, weight=BOLD)
        physics_header.next_to(physics_box, UP, buff=0.15)
        
        physics_tools = VGroup(
            MathTex(r"\nabla \cdot \mathbf{u} = 0", font_size=22, color=BLUE_C),
            MathTex(r"\partial_t u + \mathcal{N}(u) = f", font_size=20, color=BLUE_C),
            Text("Finite Element", font_size=16, color=BLUE_C),
            Text("Conservation Laws", font_size=16, color=BLUE_C),
            Text("50+ years of solvers", font_size=14, color=BLUE_C)
        ).arrange(DOWN, buff=0.25).move_to(physics_box)
        
        self.play_timed("b1_physics", 2, 7,
                        Create(physics_box), FadeIn(physics_header),
                        LaggedStart(*[FadeIn(t, shift=RIGHT*0.2) for t in physics_tools], lag_ratio=0.15))

        ml_box = RoundedRectangle(
            width=4.5, height=3.0, corner_radius=0.2,
            stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.1, stroke_width=2.5
        ).shift(RIGHT * 3.8 + DOWN * 0.3)
        
        ml_header = Text("ML WORLD", font_size=18, color=PURPLE, weight=BOLD)
        ml_header.next_to(ml_box, UP, buff=0.15)
        
        ml_tools = VGroup(
            Text("Neural Networks", font_size=16, color=PURPLE),
            MathTex(r"\mathcal{L}(\theta)", font_size=22, color=PURPLE),
            Text("Gradient Descent", font_size=16, color=PURPLE),
            Text("Loss Functions", font_size=16, color=PURPLE),
            Text("Data-driven", font_size=14, color=PURPLE)
        ).arrange(DOWN, buff=0.25).move_to(ml_box)
        
        self.play_timed("b1_ml", 7, 12,
                        Create(ml_box), FadeIn(ml_header),
                        LaggedStart(*[FadeIn(t, shift=LEFT*0.2) for t in ml_tools], lag_ratio=0.15))

        gap_zone = Rectangle(
            width=2.0, height=3.0, color=RED,
            fill_color=RED, fill_opacity=0.08, stroke_width=1, stroke_opacity=0.3
        ).shift(DOWN*0.3)
        
        gap_problems = VGroup(
            Text("Different\nLanguages", font_size=14, color=RED),
            Text("Biased Data", font_size=14, color=RED),
            Text("Different\nMetrics", font_size=14, color=RED),
            Text("Skepticism", font_size=14, color=RED)
        ).arrange(DOWN, buff=0.3).move_to(gap_zone)
        
        gap_label = Text("THE GAP", font_size=16, color=RED, weight=BOLD).next_to(gap_zone, UP, buff=0.15)
        
        self.play_timed("b1_gap", 12, 16,
                        FadeIn(gap_zone), FadeIn(gap_label),
                        LaggedStart(*[FadeIn(p, scale=0.7) for p in gap_problems], lag_ratio=0.2))

        bridge_band = RoundedRectangle(
            width=10.5, height=0.9, corner_radius=0.15,
            stroke_color=GREEN_SCREEN, fill_color=GREEN_SCREEN, fill_opacity=0.25, stroke_width=3
        ).shift(DOWN * 2.8)
        
        bridge_concepts = VGroup(
            Text("Function Spaces", font_size=14, color=GREEN_SCREEN, weight=BOLD),
            Text("Operators", font_size=14, color=GREEN_SCREEN, weight=BOLD),
            Text("Discretization", font_size=14, color=GREEN_SCREEN, weight=BOLD),
            MathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}", font_size=18, color=GREEN_SCREEN)
        ).arrange(RIGHT, buff=0.6).move_to(bridge_band)
        
        bridge_label = Text("BRIDGE: Neural Operators", font_size=16, 
                            color=GREEN_SCREEN, weight=BOLD).next_to(bridge_band, UP, buff=0.15)
        
        arrow_left = Arrow(physics_box.get_bottom(), bridge_band.get_left() + RIGHT*1.5,
                          color=GREEN_SCREEN, buff=0.15, stroke_width=2.5)
        arrow_right = Arrow(ml_box.get_bottom(), bridge_band.get_right() + LEFT*1.5,
                           color=GREEN_SCREEN, buff=0.15, stroke_width=2.5)
        
        self.play_timed("b1_bridge", 16, 24,
                        FadeOut(gap_zone), FadeOut(gap_problems), FadeOut(gap_label),
                        Create(bridge_band), FadeIn(bridge_label),
                        LaggedStart(*[FadeIn(c, shift=UP*0.2) for c in bridge_concepts], lag_ratio=0.15),
                        GrowArrow(arrow_left), GrowArrow(arrow_right),
                        Flash(bridge_band, color=GREEN_SCREEN, flash_radius=2.0, line_length=0.3))
        
        self.wait_timed("b1_hold", 24, 30)

        self.play_timed("clear_b1", 30, 32,
                        *[FadeOut(m) for m in [title, physics_box, physics_header, physics_tools,
                                               ml_box, ml_header, ml_tools,
                                               bridge_band, bridge_label, bridge_concepts,
                                               arrow_left, arrow_right]])

        recap_title = Text("Ba nguyên tắc cốt lõi của Neural Operators", font_size=28,
                          color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 32, 34, FadeIn(recap_title))

        pillar1_box = RoundedRectangle(
            width=3.5, height=4.5, corner_radius=0.15,
            stroke_color=BLUE_C, fill_color=BLACK, fill_opacity=0.8, stroke_width=2.5
        ).shift(LEFT * 4.5 + DOWN * 0.5)
        
        pillar1_icon = VGroup(
            VGroup(*[Line(LEFT*0.6 + UP*y, RIGHT*0.6 + UP*y, color=BLUE_C, stroke_width=1.5) 
                     for y in np.linspace(-0.6, 0.6, 3)]),
            VGroup(*[Line(UP*0.6 + RIGHT*x, DOWN*0.6 + RIGHT*x, color=BLUE_C, stroke_width=1.5) 
                     for x in np.linspace(-0.6, 0.6, 3)]),
            Arrow(RIGHT*0.7, RIGHT*1.1, color=BLUE_C, stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.3),
            VGroup(*[Line(LEFT*0.6 + UP*y, RIGHT*0.6 + UP*y, color=BLUE_C, stroke_width=1.0) 
                     for y in np.linspace(-0.6, 0.6, 6)]).shift(RIGHT*1.8),
            VGroup(*[Line(UP*0.6 + RIGHT*x, DOWN*0.6 + RIGHT*x, color=BLUE_C, stroke_width=1.0) 
                     for x in np.linspace(-0.6, 0.6, 6)]).shift(RIGHT*1.8),
        ).move_to(LEFT * 4.5 + UP * 0.6)
        
        pillar1_text = VGroup(
            Text("Discretization", font_size=16, color=BLUE_C, weight=BOLD),
            Text("Invariant", font_size=16, color=BLUE_C, weight=BOLD)
        ).arrange(DOWN, buff=0.1).shift(LEFT * 4.5 + DOWN * 1.6)
        
        pillar1_check = Text("✓", font_size=32, color=GREEN_SCREEN, weight=BOLD)
        pillar1_check.shift(LEFT * 4.5 + DOWN * 2.3)
        
        self.play_timed("b2_pillar1", 34, 39,
                        Create(pillar1_box),
                        LaggedStart(*[Create(p) for p in pillar1_icon], lag_ratio=0.1),
                        Write(pillar1_text),
                        Write(pillar1_check))

        pillar2_box = RoundedRectangle(
            width=3.5, height=4.5, corner_radius=0.15,
            stroke_color=PURPLE, fill_color=BLACK, fill_opacity=0.8, stroke_width=2.5
        ).shift(DOWN * 0.5)
        
        pillar2_curve = ParametricFunction(
            lambda t: np.array([t*0.8, 0.4*np.sin(3*t), 0]),
            t_range=[-1.5, 1.5], color=PURPLE, stroke_width=3
        ).shift(DOWN * 0.5 + UP * 1.0)
        
        pillar2_queries = VGroup(*[
            Dot(pillar2_curve.point_from_proportion(p), radius=0.06, 
                color=GREEN_SCREEN, fill_opacity=1)
            for p in [0.2, 0.4, 0.6, 0.8]
        ])
        
        pillar2_deriv = MathTex(r"\nabla u, \int u \, dx", font_size=20, color=PURPLE)
        pillar2_deriv.shift(DOWN * 0.5 + DOWN * 0.5)
        
        pillar2_text = VGroup(
            Text("Function", font_size=16, color=PURPLE, weight=BOLD),
            Text("Output", font_size=16, color=PURPLE, weight=BOLD)
        ).arrange(DOWN, buff=0.1).shift(DOWN * 1.6)
        
        pillar2_check = Text("✓", font_size=32, color=GREEN_SCREEN, weight=BOLD)
        pillar2_check.shift(DOWN * 2.3)
        
        self.play_timed("b2_pillar2", 39, 44,
                        Create(pillar2_box),
                        Create(pillar2_curve),
                        LaggedStart(*[FadeIn(q, scale=0.5) for q in pillar2_queries], lag_ratio=0.2),
                        Write(pillar2_deriv),
                        Write(pillar2_text),
                        Write(pillar2_check))

        pillar3_box = RoundedRectangle(
            width=3.5, height=4.5, corner_radius=0.15,
            stroke_color=GREEN_SCREEN, fill_color=BLACK, fill_opacity=0.8, stroke_width=2.5
        ).shift(RIGHT * 4.5 + DOWN * 0.5)
        
        bolt = VMobject(stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8)
        bolt.set_points_as_corners([
            UP*0.6 + LEFT*0.2, UP*0.1 + RIGHT*0.1, UP*0.1 + LEFT*0.05,
            DOWN*0.6 + RIGHT*0.2, DOWN*0.1 + LEFT*0.1, DOWN*0.1 + RIGHT*0.05,
            UP*0.6 + LEFT*0.2
        ]).shift(RIGHT * 4.5 + UP * 1.0)
        
        speed_data = VGroup(
            VGroup(Text("45,000×", font_size=16, color=YELLOW, weight=BOLD),
                   Text("Weather", font_size=12, color=GRAY_B)).arrange(DOWN, buff=0.05),
            VGroup(Text("140,000×", font_size=16, color=YELLOW, weight=BOLD),
                   Text("CFD Design", font_size=12, color=GRAY_B)).arrange(DOWN, buff=0.05),
            VGroup(Text("700,000×", font_size=16, color=YELLOW, weight=BOLD),
                   Text("Carbon Storage", font_size=12, color=GRAY_B)).arrange(DOWN, buff=0.05)
        ).arrange(DOWN, buff=0.25).shift(RIGHT * 4.5 + DOWN * 0.6)
        
        pillar3_text = Text("Speed Orders of Magnitude", font_size=14, color=GREEN_SCREEN, weight=BOLD)
        pillar3_text.shift(RIGHT * 4.5 + DOWN * 1.6)
        
        pillar3_check = Text("✓", font_size=32, color=GREEN_SCREEN, weight=BOLD)
        pillar3_check.shift(RIGHT * 4.5 + DOWN * 2.3)
        
        self.play_timed("b2_pillar3", 44, 50,
                        Create(pillar3_box),
                        DrawBorderThenFill(bolt),
                        LaggedStart(*[FadeIn(s, shift=RIGHT*0.2) for s in speed_data], lag_ratio=0.2),
                        Write(pillar3_text),
                        Write(pillar3_check))

        impact_text = Text(
            "Không chỉ là con số — mở ra những phân tích trước đây không thể làm được",
            font_size=18, color=WHITE, weight=BOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play_timed("b2_impact", 50, 55,
                        FadeIn(impact_text, shift=UP*0.3),
                        Flash(impact_text, color=GREEN_SCREEN, flash_radius=1.5))
        
        self.wait_timed("b2_hold", 55, 58)
        
        self.play_timed("cut", 58, 60, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
