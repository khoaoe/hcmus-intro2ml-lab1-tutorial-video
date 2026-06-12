from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0503_MD_PINO(TimedScene):
    SCRIPT_ID = "5.3"
    SCRIPT_TITLE = "Động lực học phân tử & PINO"
    SCRIPT_START = 1255.0
    SCRIPT_END = 1360.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Tiến hóa theo thời gian: Rời rạc vs Liên tục", font_size=28, 
                     color=BLUE_C, weight=BOLD).to_edge(UP, buff=0.4)
        
        t_axis = NumberLine(x_range=[0, 6, 1], length=8, include_ticks=True, 
                            include_numbers=True, color=GRAY_B).shift(DOWN * 1.5)
        t_label = Text("Thời gian (t)", font_size=16, color=GRAY_B).next_to(t_axis, DOWN, buff=1.2)
        
        continuous_func = lambda t: np.sin(1.5 * t) * np.exp(-0.2 * t) + 0.5 * np.cos(3 * t)
        curve = ParametricFunction(
            lambda t: np.array([t_axis.number_to_point(t)[0], continuous_func(t) * 1.2, 0]),
            t_range=[0, 6, 0.01], color=PHYSICS, stroke_width=3
        )
        
        dt = 0.8
        t_vals = np.arange(0, 6.1, dt)
        discrete_dots = VGroup(*[
            Dot(t_axis.number_to_point(t) + UP * continuous_func(t) * 1.2, 
                radius=0.06, color=RED, stroke_width=2, stroke_color=WHITE)
            for t in t_vals
        ])
        discrete_labels = VGroup(*[
            MathTex(f"t_{{{i}}}", font_size=14, color=RED).next_to(dot, UP, buff=0.15)
            for i, dot in enumerate(discrete_dots)
        ])
        
        step_arrows = VGroup()
        for i in range(len(t_vals)-1):
            p1 = discrete_dots[i].get_center()
            p2 = discrete_dots[i+1].get_center()
            arr = Arrow(p1, p2, color=RED, buff=0.15, stroke_width=2, max_tip_length_to_length_ratio=0.2)
            step_arrows.add(arr)
            
        ml_label_text = Text("ML rời rạc: ", font_size=18, color=RED)
        ml_label_math = MathTex(r"t \to t+\Delta t", font_size=26, color=RED)
        ml_label = VGroup(ml_label_text, ml_label_math).arrange(RIGHT, buff=0.1).shift(LEFT * 3.5 + UP * 2)
        no_label = Text("Neural Operator: Toán tử liên tục", font_size=18, color=PHYSICS).shift(RIGHT * 3.5 + UP * 2)
        
        self.play_timed("b1_setup", 0, 5, FadeIn(title), Create(t_axis), FadeIn(t_label))
        
        self.play_timed("b1_discrete", 5, 12,
                        LaggedStart(*[FadeIn(d) for d in discrete_dots], lag_ratio=0.15),
                        FadeIn(discrete_labels), FadeIn(ml_label))
        self.play_timed("b1_steps", 12, 18, Create(step_arrows))
        
        self.play_timed("b1_continuous", 18, 25, Create(curve), FadeIn(no_label))
        
        supervision_braces = VGroup(*[
            BraceBetweenPoints(d.get_center() + DOWN*0.2, d.get_center() + UP*0.2, color=YELLOW)
            for d in discrete_dots[1:-1]
        ])
        supervision_text = Text("Solver steps = Supervision", font_size=16, color=YELLOW).move_to(UP * 0.8)
        
        self.play_timed("b1_supervision", 25, 32, 
                        LaggedStart(*[GrowFromCenter(b) for b in supervision_braces], lag_ratio=0.1),
                        FadeIn(supervision_text))
        
        emulator_note = Text("Output = Emulator → kiểm tra bằng PDE gốc", font_size=16, color=WHITE).to_edge(DOWN, buff=0.4)
        self.play_timed("b1_emulator", 32, 38, FadeIn(emulator_note))
        self.wait_timed("b1_hold", 38, 45)
        
        self.play_timed("clear_b1", 45, 47, *[FadeOut(m) for m in self.mobjects])
        
        pinO_title = Text("Physics-Informed Neural Operator (PINO)", font_size=32, 
                          color=PHYSICS, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 47, 49, FadeIn(pinO_title))

        u_theta_box = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.15, 
                                       stroke_color=BLUE_C, fill_color=BLACK, fill_opacity=0.9, stroke_width=3)
        u_theta_txt = MathTex(r"u_\theta(x,t)", font_size=28, color=BLUE_C).move_to(u_theta_box)
        u_theta = VGroup(u_theta_box, u_theta_txt).shift(UP * 0.5)

        gt_box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.15,
                                  stroke_color=GRAY_B, fill_color=BLACK, fill_opacity=0.8, stroke_width=2)
        gt_txt = Text("Ground Truth", font_size=18, color=GRAY_B).move_to(gt_box)
        gt = VGroup(gt_box, gt_txt).shift(LEFT * 4 + UP * 0.5)

        data_loss_box = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1,
                                         stroke_color=BLUE_C, fill_color=BLACK, fill_opacity=0.9)
        data_loss_txt = MathTex(r"\mathcal{L}_{data}", font_size=22, color=BLUE_C).move_to(data_loss_box)
        data_loss = VGroup(data_loss_box, data_loss_txt).shift(LEFT * 2 + DOWN * 1.5)

        pde_box = RoundedRectangle(width=2.8, height=1.4, corner_radius=0.15,
                                   stroke_color=YELLOW, fill_color=BLACK, fill_opacity=0.9, stroke_width=3)
        pde_txt = MathTex(r"\partial_t u + \mathcal{N}(u) = 0", font_size=22, color=YELLOW).move_to(pde_box)
        pde = VGroup(pde_box, pde_txt).shift(RIGHT * 4 + UP * 0.5)

        physics_loss_box = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.1,
                                            stroke_color=RED, fill_color=BLACK, fill_opacity=0.9)
        physics_loss_txt = MathTex(r"\mathcal{L}_{physics}", font_size=22, color=RED).move_to(physics_loss_box)
        physics_loss = VGroup(physics_loss_box, physics_loss_txt).shift(RIGHT * 2 + DOWN * 1.5)

        total_loss_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.1,
                                          stroke_color=PHYSICS, fill_color=BLACK, fill_opacity=0.9)
        total_loss_txt = VGroup(
            MathTex(r"\mathcal{L}_{total} =", font_size=20, color=PHYSICS),
            MathTex(r"\mathcal{L}_{data} + \lambda \mathcal{L}_{physics}", font_size=20, color=PHYSICS)
        ).arrange(DOWN, buff=0.1).move_to(total_loss_box)
        total_loss = VGroup(total_loss_box, total_loss_txt).shift(DOWN * 3.5)

        arrow_gt_u = Arrow(gt.get_right(), u_theta.get_left(), color=GRAY_B, buff=0.2, stroke_width=2)
        arrow_u_data = Arrow(u_theta.get_bottom() + LEFT*0.3, data_loss.get_top(), color=BLUE_C, buff=0.2, stroke_width=2)
        arrow_u_pde = Arrow(u_theta.get_right(), pde.get_left(), color=YELLOW, buff=0.2, stroke_width=2)
        arrow_pde_phys = Arrow(pde.get_bottom(), physics_loss.get_top(), color=RED, buff=0.2, stroke_width=2)
        arrow_data_total = Arrow(data_loss.get_bottom(), total_loss.get_left(), color=BLUE_C, buff=0.2, stroke_width=2)
        arrow_phys_total = Arrow(physics_loss.get_bottom(), total_loss.get_right(), color=RED, buff=0.2, stroke_width=2)

        self.play_timed("b2_model", 49, 52, FadeIn(u_theta))
        
        self.play_timed("b2_data_path", 52, 55,
                        FadeIn(gt), Create(arrow_gt_u),
                        FadeIn(data_loss), Create(arrow_u_data))
        
        self.play_timed("b2_physics_path", 55, 58,
                        FadeIn(pde), Create(arrow_u_pde),
                        FadeIn(physics_loss), Create(arrow_pde_phys))
        
        self.play_timed("b2_total_loss", 58, 61,
                        FadeIn(total_loss),
                        Create(arrow_data_total), Create(arrow_phys_total))

        dim_targets = [gt, arrow_gt_u, data_loss, arrow_u_data, 
                       physics_loss, arrow_pde_phys, total_loss, 
                       arrow_data_total, arrow_phys_total]
        
        self.play_timed("b2_dim", 61, 63,
                        *[m.animate.set_opacity(0.2) for m in dim_targets],
                        u_theta.animate.set_opacity(0.5),
                        arrow_u_pde.animate.set_opacity(0.5))

        dt_u = MathTex(r"\frac{\partial u}{\partial t}", font_size=24, color=ORANGE).move_to(pde.get_top() + UP * 1.0 + LEFT * 0.5)
        grad_u = MathTex(r"\nabla u", font_size=24, color=TEAL).move_to(pde.get_top() + UP * 1.0 + RIGHT * 0.5)

        arrow_dt = Arrow(dt_u.get_bottom(), pde.get_top() + LEFT*0.3, color=ORANGE, buff=0.1, stroke_width=2)
        arrow_grad = Arrow(grad_u.get_bottom(), pde.get_top() + RIGHT*0.3, color=TEAL, buff=0.1, stroke_width=2)

        self.play_timed("b2_autograd", 63, 67,
                        FadeIn(dt_u), Create(arrow_dt),
                        FadeIn(grad_u), Create(arrow_grad),
                        Flash(pde, color=YELLOW, flash_radius=1.5, line_length=0.3))

        residual_eq = MathTex(r"\mathcal{R} = \frac{\partial u}{\partial t} + \mathcal{N}(u)", 
                              font_size=33, color=RED).move_to(u_theta.get_top() + UP * 1.0)
        self.play_timed("b2_residual", 67, 70, FadeIn(residual_eq))

        self.play_timed("b2_restore", 70, 73,
                        *[m.animate.set_opacity(1.0) for m in dim_targets],
                        u_theta.animate.set_opacity(1.0),
                        arrow_u_pde.animate.set_opacity(1.0),
                        FadeOut(dt_u), FadeOut(grad_u),
                        FadeOut(arrow_dt), FadeOut(arrow_grad),
                        FadeOut(residual_eq))

        self.play_timed("b2_merge", 73, 75,
                        Flash(total_loss, color=PHYSICS, flash_radius=1.5),
                        total_loss.animate.scale(1.1),
                        rate_func=there_and_back)

        self.play_timed("clear_b2", 75, 77, *[FadeOut(m) for m in self.mobjects])

        upscaling_title = Text("Zero-shot Upscaling: Physics Fine-tune", font_size=26, 
                               color=PHYSICS, weight=BOLD).to_edge(UP, buff=0.4)
        
        coarse_grid = NumberPlane(x_range=[-3, 3, 0.5], y_range=[-2, 2, 0.5], 
                                  background_line_style={"stroke_color": BLUE_C, "stroke_width": 1.5, "stroke_opacity": 0.6})
        coarse_grid.scale(0.6).shift(LEFT * 3.5 + UP * 1.0)
        coarse_label = Text("Train: 64×64", font_size=16, color=BLUE_C).next_to(coarse_grid, DOWN, buff=0.2)
        
        fine_grid = NumberPlane(x_range=[-3, 3, 0.125], y_range=[-2, 2, 0.125],
                                background_line_style={"stroke_color": PHYSICS, "stroke_width": 1, "stroke_opacity": 0.5})
        fine_grid.scale(0.6).shift(RIGHT * 3.5 + UP * 1.0)
        fine_label = Text("Inference: 256×256 (Zero-shot)", font_size=16, color=PHYSICS).next_to(fine_grid, DOWN, buff=0.2)
        
        arrow_upscale = Arrow(coarse_grid.get_right(), fine_grid.get_left(), color=YELLOW, buff=0.3)
        arrow_label = Text("No extra data", font_size=14, color=YELLOW).next_to(arrow_upscale, UP, buff=0.1)
        
        self.play_timed("b3_title", 77, 79, FadeIn(upscaling_title))
        self.play_timed("b3_grids", 79, 84, 
                        Create(coarse_grid), FadeIn(coarse_label),
                        Create(arrow_upscale), FadeIn(arrow_label),
                        Create(fine_grid), FadeIn(fine_label))
        
        spec_axes = Axes(x_range=[0, 5, 1], y_range=[0, 1.2, 0.2], x_length=5, y_length=2.5,
                         axis_config={"color": GRAY_B, "include_ticks": True, "include_numbers": False})
        spec_axes.shift(DOWN * 2.2)
        x_label = Text("Tần số (k)", font_size=12, color=GRAY_B).next_to(spec_axes.x_axis, DOWN, buff=0.1)
        y_label = Text("Năng lượng", font_size=12, color=GRAY_B).next_to(spec_axes.y_axis, LEFT, buff=0.1)
        
        gt_func = lambda k: np.exp(-0.8 * k)
        gt_plot_base = spec_axes.plot(gt_func, x_range=[0, 5], color=GRAY_A, stroke_width=2.5)
        gt_plot = DashedVMobject(gt_plot_base)
        gt_label = Text("Ground Truth", font_size=12, color=GRAY_A).next_to(gt_plot_base.get_end(), RIGHT, buff=0.1)
        
        pred_plot = spec_axes.plot(gt_func, x_range=[0, 5], color=PHYSICS, stroke_width=3)
        
        self.play_timed("b3_spectrum_setup", 84, 88, 
                        Create(spec_axes), FadeIn(x_label), FadeIn(y_label),
                        Create(gt_plot), FadeIn(gt_label))
        
        self.play_timed("b3_pred_match", 88, 93, Create(pred_plot))
        
        match_glow = VGroup(*[
            Dot(spec_axes.coords_to_point(k, gt_func(k)), radius=0.08, color=PHYSICS, fill_opacity=0.4)
            for k in np.linspace(0.5, 4.5, 8)
        ])
        match_text = Text("Spectrum khớp chính xác | Physics Fine-tune", font_size=16, color=PHYSICS).to_edge(DOWN, buff=0.3)
        
        self.play_timed("b3_glow", 93, 99, 
                        LaggedStart(*[FadeIn(g, scale=1.5) for g in match_glow], lag_ratio=0.1),
                        FadeIn(match_text))
        
        self.wait_timed("b3_hold", 99, 103)
        
        self.play_timed("cut", 103, 105, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
