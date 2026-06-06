"""
Scene 2.3 — Từ Deep Learning truyền thống đến Operator Learning
Source: original_outline.tex, Section 2, Scene 2.3
Global time: 5:40 – 6:40
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0203_FromDLToOperatorLearning(TimedScene):
    SCRIPT_ID = "2.3"
    SCRIPT_TITLE = "Từ Deep Learning truyền thống đến Operator Learning"
    SCRIPT_START = 340.0
    SCRIPT_END = 400.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: [5:40–6:10] Solver Loop vs Operator Forward
        # ═══════════════════════════════════════════════════════════════
        
        # 1. Divider line (center)
        divider = Line(UP * 4, DOWN * 4, color=MUTED, stroke_width=1.5, stroke_opacity=0.5)
        
        # 2. Titles
        left_title = Text("Solver truyền thống", font_size=28, color=WARNING, weight=BOLD)
        left_title.move_to(LEFT * 4 + UP * 3.5)
        
        right_title = Text("Operator Learning", font_size=28, color=NVIDIA_GREEN, weight=BOLD)
        right_title.move_to(RIGHT * 4 + UP * 3.5)
        
        # 3. Inputs (a1, a2, a3) - Far left
        inputs = VGroup()
        for i, label in enumerate(["a_1", "a_2", "a_3"]):
            inp = RoundedRectangle(
                width=1.0, height=0.7, corner_radius=0.1,
                stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.8, stroke_width=2
            )
            inp_text = MathTex(label, font_size=22, color=INPUT).move_to(inp)
            inp_group = VGroup(inp, inp_text)
            inputs.add(inp_group)
        inputs.arrange(DOWN, buff=0.6).move_to(LEFT * 6.5)
        
        # Clone inputs for right side
        inputs_right = inputs.copy().move_to(RIGHT * 1.5)
        
        # 4. Outputs (u1, u2, u3) - Left side (near divider but not crossing)
        outputs = VGroup()
        for i, label in enumerate(["u_1", "u_2", "u_3"]):
            out = RoundedRectangle(
                width=1.0, height=0.7, corner_radius=0.1,
                stroke_color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.8, stroke_width=2
            )
            out_text = MathTex(label, font_size=22, color=OPERATOR).move_to(out)
            out_group = VGroup(out, out_text)
            outputs.add(out_group)
        outputs.arrange(DOWN, buff=0.6).move_to(LEFT * 1.5)
        
        outputs_right = outputs.copy().move_to(RIGHT * 6.5)
        
        # 5. LEFT SIDE: Solver boxes with circular arrow icons
        solver_boxes = VGroup()
        loop_icons = VGroup()
        
        for i in range(3):
            # Solver box
            box = RoundedRectangle(
                width=1.8, height=0.9, corner_radius=0.15,
                stroke_color=WARNING, fill_color=CARD_BG, fill_opacity=0.9, stroke_width=2
            )
            box_text = Text("Solver", font_size=18, color=WARNING).move_to(box)
            box_group = VGroup(box, box_text)
            solver_boxes.add(box_group)
            
            # Circular arrow icon (↻) - represents iteration
            loop_arrow = Arc(
                radius=0.2, start_angle=PI/4, angle=3*PI/2,
                color=WARNING, stroke_width=2.5
            )
            # Add arrowhead
            arrow_tip = Triangle(
                color=WARNING, fill_opacity=1, stroke_width=0
            ).scale(0.08)
            arrow_tip.move_to(loop_arrow.get_end())
            arrow_tip.rotate(np.arctan2(
                loop_arrow.get_end()[1] - loop_arrow.point_from_proportion(0.9)[1],
                loop_arrow.get_end()[0] - loop_arrow.point_from_proportion(0.9)[0]
            ) + PI/2)
            
            loop_icon = VGroup(loop_arrow, arrow_tip)
            loop_icons.add(loop_icon)
        
        solver_boxes.arrange(DOWN, buff=0.6).move_to(LEFT * 4)
        for i in range(3):
            loop_icons[i].move_to(solver_boxes[i].get_right())
        
        # 6. RIGHT SIDE: Operator box (large)
        operator_box = RoundedRectangle(
            width=2.8, height=3.5, corner_radius=0.2,
            stroke_color=NVIDIA_GREEN, fill_color=CARD_BG, fill_opacity=0.9, stroke_width=3
        ).move_to(RIGHT * 4.0)
        
        op_text = VGroup(
            Text("Learned", font_size=24, color=NVIDIA_GREEN),
            Text("Operator G", font_size=28, color=NVIDIA_GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.1).move_to(operator_box)
        
        # 7. Arrows - Left side (Input → Solver → Output)
        left_arrows_in = VGroup()
        left_arrows_out = VGroup()
        for i in range(3):
            # Input → Solver
            arr_in = Arrow(
                inputs[i].get_right(), solver_boxes[i].get_left(),
                color=MUTED, buff=0.15, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            # Solver → Output
            arr_out = Arrow(
                solver_boxes[i].get_right(), outputs[i].get_left(),
                color=MUTED, buff=0.15, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            left_arrows_in.add(arr_in)
            left_arrows_out.add(arr_out)
        
        # 8. Arrows - Right side (Input → Operator → Output)
        right_arrows_in = VGroup()
        right_arrows_out = VGroup()
        for i in range(3):
            arr_in = Arrow(
                inputs_right[i].get_right(), operator_box.get_left() + UP * (1 - i * 1),
                color=NVIDIA_GREEN, buff=0.15, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
            )
            arr_out = Arrow(
                operator_box.get_right() + UP * (1 - i * 1), outputs_right[i].get_left(),
                color=NVIDIA_GREEN, buff=0.15, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
            )
            right_arrows_in.add(arr_in)
            right_arrows_out.add(arr_out)
        
        # ══════════════════════════════════════════════════════════════
        # Animation Sequence
        # ═══════════════════════════════════════════════════════════════
        
        # 0. Divider
        self.play_timed("divider", 0, 1, Create(divider))
        
        # 1. Titles
        self.play_timed("titles", 1, 3, FadeIn(left_title), FadeIn(right_title))
        
        # 2. Inputs (both sides)
        self.play_timed("inputs", 3, 5, 
                        LaggedStart(*[FadeIn(inp) for inp in inputs], lag_ratio=0.2),
                        LaggedStart(*[FadeIn(inp) for inp in inputs_right], lag_ratio=0.2))
        
        # 3. Left side: Solver boxes appear sequentially (emphasize sequential nature)
        for i in range(3):
            t_start = 5 + i * 1.2
            t_end = t_start + 1.2
            self.play_timed(f"solver_box_{i}", t_start, t_end,
                            FadeIn(solver_boxes[i]),
                            GrowArrow(left_arrows_in[i]))
        
        # 4. Left side: Loop icons appear (show iteration)
        for i in range(3):
            t_start = 8.6 + i * 0.5
            t_end = t_start + 0.5
            self.play_timed(f"loop_icon_{i}", t_start, t_end,
                            Create(loop_icons[i]))
        
        # 5. Left side: Output arrows and outputs
        for i in range(3):
            t_start = 10.1 + i * 0.5
            t_end = t_start + 0.5
            self.play_timed(f"left_output_{i}", t_start, t_end,
                            GrowArrow(left_arrows_out[i]),
                            FadeIn(outputs[i]))
        
        # 6. Right side: Operator box appears at once (parallel)
        self.play_timed("operator_box", 11.6, 13.1,
                        FadeIn(operator_box), Write(op_text))
        
        # 7. Right side: All arrows shoot at once
        self.play_timed("right_arrows", 13.1, 15.1,
                        LaggedStart(*[GrowArrow(arr) for arr in right_arrows_in], lag_ratio=0.1),
                        LaggedStart(*[GrowArrow(arr) for arr in right_arrows_out], lag_ratio=0.1),
                        LaggedStart(*[FadeIn(out) for out in outputs_right], lag_ratio=0.1))
        
        # 8. Overlay text: The Core Difference
        diff_text = VGroup(
            Text("Solver: Giải từng cái một (Sequential)", font_size=22, color=WARNING),
            Text("Operator: Học một lần, dùng cho tất cả (Amortized)", font_size=22, color=NVIDIA_GREEN)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        
        self.play_timed("diff_text", 15.1, 18.1, FadeIn(diff_text, shift=UP*0.2))
        
        self.wait_timed("hold_beat1", 18.1, 30)
        
        # Clear beat 1
        self.play_timed("clear_beat1", 30, 31, *[FadeOut(m) for m in self.mobjects])
        
        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [6:10–6:40] Darcy Flow: Gallery of Solutions
        # ═══════════════════════════════════════════════════════════════
        
        # Title
        darcy_title = Text("Darcy Flow: Dòng chảy qua môi trường xốp", 
                          font_size=28, color=WHITE, weight=BOLD).to_edge(UP, buff=0.3)
                          
        # Darcy equation (faded in background)
        darcy_eq = MathTex(
            r"-\nabla \cdot (a(x) \nabla u(x)) = f(x)",
            font_size=32, color=MUTED
        ).next_to(darcy_title, DOWN, buff=0.3)
        
        # Gallery of (a, u) pairs (3 columns x 2 rows)
        gallery = VGroup()
        n_pairs = 6
        for i in range(n_pairs):
            # Input a(x)
            a_box = Square(side_length=1.0, stroke_color=INPUT, stroke_width=2, fill_opacity=0)
            a_box.move_to(LEFT * 5.0 + UP * (0.8 - (i // 3) * 1.8) + RIGHT * (i % 3) * 4.2)
            
            # Simulate permeability pattern with random squares
            a_pattern = VGroup()
            np.random.seed(i * 10)
            for _ in range(8):
                sq = Square(
                    side_length=0.2,
                    fill_color=interpolate_color(ManimColor(BLUE_D), ManimColor(BLUE_A), np.random.rand()),
                    fill_opacity=0.8,
                    stroke_width=0
                )
                sq.move_to(a_box.get_center() + np.array([
                    np.random.uniform(-0.35, 0.35),
                    np.random.uniform(-0.35, 0.35),
                    0
                ]))
                a_pattern.add(sq)
            
            a_label = MathTex(f"a_{i+1}(x)", font_size=18, color=INPUT).next_to(a_box, DOWN, buff=0.1)
            
            # Output u(x)
            u_box = Square(side_length=1.0, stroke_color=OPERATOR, stroke_width=2, fill_opacity=0)
            u_box.move_to(a_box.get_center() + RIGHT * 1.5)
            
            # Simulate pressure gradient
            u_gradient = Rectangle(
                width=1.0, height=1.0,
                fill_color=interpolate_color(ManimColor(PURPLE_A), ManimColor(PURPLE_D), 0.5),
                fill_opacity=0.7,
                stroke_width=0
            ).move_to(u_box)
            
            u_label = MathTex(f"u_{i+1}(x)", font_size=18, color=OPERATOR).next_to(u_box, DOWN, buff=0.1)
            
            # Arrow between a and u
            pair_arrow = Arrow(
                a_box.get_right(), u_box.get_left(),
                color=MUTED, buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2
            )
            
            pair_group = VGroup(a_box, a_pattern, a_label, u_box, u_gradient, u_label, pair_arrow)
            gallery.add(pair_group)
        
        gallery.scale(1.2).shift(UP * 0.6)
        
        # Horizontal Pipeline: [a(x)] --> [Learned Operator G] --> [u(x)]
        pipeline = VGroup()
        
        pipe_a = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.1, stroke_color=INPUT, fill_color=CARD_BG, fill_opacity=0.8)
        pipe_a_text = MathTex("a(x)", font_size=24, color=INPUT).move_to(pipe_a)
        pipe_a_group = VGroup(pipe_a, pipe_a_text)
        
        pipe_g = RoundedRectangle(width=3.2, height=1.0, corner_radius=0.15, stroke_color=NVIDIA_GREEN, fill_color=CARD_BG, fill_opacity=0.9)
        pipe_g_text = Text("Learned Operator G", font_size=20, color=NVIDIA_GREEN, weight=BOLD).move_to(pipe_g)
        pipe_g_group = VGroup(pipe_g, pipe_g_text)
        
        pipe_u = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.1, stroke_color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.8)
        pipe_u_text = MathTex("u(x)", font_size=24, color=OPERATOR).move_to(pipe_u)
        pipe_u_group = VGroup(pipe_u, pipe_u_text)
        
        pipeline.add(pipe_a_group, pipe_g_group, pipe_u_group)
        pipeline.arrange(RIGHT, buff=1.0).move_to(DOWN * 2.6)
        
        arr_in = Arrow(pipe_a_group.get_right(), pipe_g_group.get_left(), color=NVIDIA_GREEN, buff=0.1, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        arr_out = Arrow(pipe_g_group.get_right(), pipe_u_group.get_left(), color=NVIDIA_GREEN, buff=0.1, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        
        pipeline_group = VGroup(pipeline, arr_in, arr_out)
        
        # Final message
        final_msg = Text(
            "Không giải PDE mỗi lần. Học ánh xạ G.",
            font_size=24, color=YELLOW, weight=BOLD
        ).next_to(pipeline_group, DOWN, buff=0.3)
        
        # Animate beat 2
        self.play_timed("darcy_title", 31, 33, FadeIn(darcy_title))
        
        # Equation appears (faded)
        self.play_timed("darcy_eq", 33, 35, FadeIn(darcy_eq))
        
        # Gallery appears pair by pair
        for i, pair in enumerate(gallery):
            t_start = 35 + i * 0.8
            t_end = t_start + 0.8
            self.play_timed(f"pair_{i}", t_start, t_end, FadeIn(pair))
            
        # Horizontal Pipeline appears
        self.play_timed("pipeline_appear", 41, 44, 
                        FadeIn(pipe_a_group),
                        GrowArrow(arr_in),
                        FadeIn(pipe_g_group),
                        GrowArrow(arr_out),
                        FadeIn(pipe_u_group))
                        
        # Equation fades out, final message appears
        self.play_timed("final_msg", 44, 47,
                        FadeOut(darcy_eq),
                        FadeIn(final_msg))
                        
        self.wait_timed("hold_end", 47, 59)
        
        # Cut to black
        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
