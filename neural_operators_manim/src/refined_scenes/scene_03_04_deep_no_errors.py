
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0304_DeepNOErrorAnalysis(TimedScene):
    SCRIPT_ID = "3.4"
    SCRIPT_TITLE = "Deep Neural Operator & Bẫy Rời rạc hóa"
    SCRIPT_START = 615.0
    SCRIPT_END = 675.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        
        dummy_axes = Axes(x_range=[0, 6], y_range=[-3, 3], x_length=8, y_length=4)
        
        in_func = dummy_axes.plot(lambda x: np.sin(x) * 0.8, color=INPUT, stroke_width=4)
        in_label = Text("Hàm vật lý", font_size=20, color=INPUT).next_to(in_func, LEFT, buff=0.5)
        
        latent_ribbon = VGroup()
        n_layers = 20
        for i in range(n_layers):
            c = interpolate_color(ManimColor(INPUT), ManimColor(PURPLE), i/(n_layers-1))
            line = dummy_axes.plot(
                lambda x, i=i: np.sin(x + i*0.05) * 0.6 + (i/(n_layers-1))*1.5 - 0.75,
                color=c, stroke_width=2, stroke_opacity=0.6
            )
            latent_ribbon.add(line)
            
        operated_ribbon = VGroup()
        for i in range(n_layers):
            c = interpolate_color(ManimColor(INPUT), ManimColor(PURPLE), i/(n_layers-1))
            line = dummy_axes.plot(
                lambda x, i=i: np.cos(x*1.2 + i*0.08) * 0.6 + (i/(n_layers-1))*1.5 - 0.75,
                color=c, stroke_width=2, stroke_opacity=0.6
            )
            operated_ribbon.add(line)
            
        out_func = dummy_axes.plot(lambda x: np.cos(x*1.5) * 0.8, color=OUTPUT, stroke_width=4)
        out_label = Text("Hàm dự báo", font_size=20, color=OUTPUT).next_to(out_func, RIGHT, buff=0.5)
        
        kernel_lens = Rectangle(width=0.2, height=4, color=OPERATOR, fill_opacity=0.6, stroke_width=2)
        lens_glow = Rectangle(width=0.6, height=4.5, color=OPERATOR, fill_opacity=0.2, stroke_width=0)
        lens_group = VGroup(kernel_lens, lens_glow).shift(LEFT*4)
        
        enc_lbl = Text("Encoder\n(Pointwise)", font_size=18, color=INPUT)
        enc_lbl.set_x(in_label.get_x())
        enc_lbl.set_y(2.8)
        
        op_lbl = Text("Integral\nOperator Layers", font_size=18, color=OPERATOR).shift(UP*2.8)
        
        dec_lbl = Text("Decoder\n(Pointwise)", font_size=18, color=OUTPUT)
        dec_lbl.set_x(out_label.get_x())
        dec_lbl.set_y(2.8)
        
        self.play_timed("in_func", 0, 2, Create(in_func), FadeIn(in_label))
        
        self.play_timed("lift", 2, 6,
            ReplacementTransform(in_func, latent_ribbon),
            FadeIn(enc_lbl)
        )
        
        particles = VGroup()
        for i in [0, 4, 9, 14, 19]:
            dot = Dot(color=WHITE, radius=0.06)
            dot.move_to(latent_ribbon[i].points[0])
            particles.add(dot)
            
        self.play_timed("add_particles", 6, 7, FadeIn(particles))
        self.play_timed("lens_in", 7, 8, FadeIn(lens_group), FadeIn(op_lbl))
        
        self.play_timed("operate_sweep", 8, 14,
            lens_group.animate.shift(RIGHT*8),
            Transform(latent_ribbon, operated_ribbon),
            *[MoveAlongPath(particles[j], operated_ribbon[i]) for j, i in enumerate([0, 4, 9, 14, 19])],
            rate_func=linear
        )
        
        self.play_timed("lens_out", 14, 15, FadeOut(lens_group), FadeOut(particles))
        
        self.play_timed("project", 15, 19,
            ReplacementTransform(latent_ribbon, out_func),
            FadeIn(dec_lbl), FadeIn(out_label)
        )
        
        overlay_text = Text("Dữ liệu luôn là Hàm số", font_size=24, color=WHITE, weight=BOLD).to_edge(DOWN, buff=1)
        self.play_timed("overlay", 19, 22, Write(overlay_text))
        
        self.wait_timed("hold_b1", 22, 29)
        self.play_timed("clear_b1", 29, 30, *[FadeOut(m) for m in self.mobjects])
        
        
        error_title = Text("Bẫy Rời rạc hóa", font_size=28, color=WHITE, weight=BOLD).to_edge(UP, buff=0.3)
        
        axes_smooth = Axes(x_range=[0, 4.3, 1], y_range=[0, 2.5], x_length=5, y_length=1.5,
                           axis_config={"stroke_color": GREY_B, "include_ticks": False}).shift(UP*1.5 + LEFT*2)
        smooth_func = axes_smooth.plot(lambda x: np.sin(x)*0.6 + 1.2, x_range=[0, 4], color=NVIDIA_GREEN, stroke_width=3)
        lbl_smooth = Text("Hàm trơn (s lớn)", font_size=18, color=NVIDIA_GREEN).next_to(axes_smooth, LEFT, buff=0.3)
        
        axes_shock = Axes(x_range=[0, 4.3, 1], y_range=[0, 2.5], x_length=5, y_length=1.5,
                          axis_config={"stroke_color": GREY_B, "include_ticks": False}).shift(DOWN*1.5 + LEFT*2)
        shock_func = axes_shock.plot(
            lambda x: 1.2 / (1 + np.exp(-20*(x-2))) + 0.4,
            x_range=[0, 4], color=WARNING, stroke_width=3
        )
        lbl_shock = Text("Hàm Shock (s nhỏ)", font_size=18, color=WARNING).next_to(axes_shock, LEFT, buff=0.3)
        
        self.play_timed("setup_b2", 30, 32,
            FadeIn(error_title),
            Create(axes_smooth), Create(smooth_func), FadeIn(lbl_smooth),
            Create(axes_shock), Create(shock_func), FadeIn(lbl_shock)
        )
        
        def get_sampling(axes, func, n_samples, color):
            dots = VGroup()
            lines = VGroup()
            for i in range(n_samples):
                x = i * 4 / (n_samples - 1)
                y = func(x)
                dot = Dot(axes.c2p(x, y), color=color, radius=0.06)
                line = DashedLine(axes.c2p(x, 0), axes.c2p(x, y), color=color, stroke_opacity=0.5)
                dots.add(dot)
                lines.add(line)
            return VGroup(dots, lines)
            
        sm_samp = get_sampling(axes_smooth, lambda x: np.sin(x)*0.6 + 1.2, 4, NVIDIA_GREEN)
        sh_samp = get_sampling(axes_shock, lambda x: 1.2 / (1 + np.exp(-20*(x-2))) + 0.4, 4, WARNING)
        
        self.play_timed("sample_N4", 32, 34, FadeIn(sm_samp), FadeIn(sh_samp))
        
        smooth_glow = SurroundingRectangle(
            sm_samp, color=NVIDIA_GREEN, fill_opacity=0.3, stroke_width=0
        )
        shock_glow = Rectangle(
            width=1.0, height=2.0, color=WARNING, fill_opacity=0.3, stroke_width=0
        ).move_to(axes_shock.c2p(2, 1.0))
        
        self.play_timed("glows_in", 34, 35, FadeIn(smooth_glow), FadeIn(shock_glow))
        
        N_vals = [8, 16, 32]
        times = [(35, 36.5), (36.5, 38), (38, 39.5)]
        
        curr_sm_samp = sm_samp
        curr_sh_samp = sh_samp
        
        for idx, n in enumerate(N_vals):
            new_sm = get_sampling(axes_smooth, lambda x: np.sin(x)*0.6 + 1.2, n, NVIDIA_GREEN)
            new_sh = get_sampling(axes_shock, lambda x: 1.2 / (1 + np.exp(-20*(x-2))) + 0.4, n, WARNING)
            
            t_start, t_end = times[idx]
            self.play_timed(f"N_{n}", t_start, t_end,
                Transform(curr_sm_samp, new_sm),
                Transform(curr_sh_samp, new_sh),
                smooth_glow.animate.scale(0.3), # smooth error shrinks rapidly
                shock_glow.animate.scale(0.8)  # shock error shrinks slowly
            )
            curr_sm_samp = new_sm
            curr_sh_samp = new_sh
            
        self.play_timed("hide_smooth_glow", 39.5, 40, FadeOut(smooth_glow))
        
        conv_axes = Axes(
            x_range=[0, 3.5, 1], y_range=[-5.5, 0.5, 1],
            x_length=3.6, y_length=3.0,
            axis_config={"stroke_color": GREY_B, "include_ticks": True},
            y_axis_config={"include_tip": False}
        ).shift(RIGHT*4 + UP*0.5)
        
        for i in range(1, 4):
            lbl = MathTex(f"10^{i}", font_size=16).next_to(conv_axes.c2p(i, 0), UP, buff=0.15)
            conv_axes.add(lbl)
        for i in range(2, 6, 2):
            lbl = MathTex(f"10^{{-{i}}}", font_size=16).next_to(conv_axes.c2p(0, -i), LEFT, buff=0.2)
            conv_axes.add(lbl)
            
        conv_lbl_x = Text("N (lưới)", font_size=16, color=WHITE).next_to(conv_axes.x_axis, RIGHT, buff=0.1)
        conv_lbl_y = MathTex(r"\varepsilon_{disc}", font_size=20, color=WHITE).next_to(conv_axes.y_axis, UP, buff=0.1)
        
        x_vals = np.linspace(0, 2.5, 15)
        
        smooth_conv = conv_axes.plot_line_graph(
            x_values=x_vals, y_values=-2*x_vals,
            line_color=NVIDIA_GREEN,
            add_vertex_dots=True,
            vertex_dot_radius=0.04,
            vertex_dot_style={"color": NVIDIA_GREEN}
        )
        shock_conv = conv_axes.plot_line_graph(
            x_values=x_vals, y_values=-0.5*x_vals,
            line_color=WARNING,
            add_vertex_dots=True,
            vertex_dot_radius=0.04,
            vertex_dot_style={"color": WARNING}
        )
        
        smooth_label = Text("Trơn: s ≈ 2", font_size=14, color=NVIDIA_GREEN).next_to(
            conv_axes.c2p(2.5, -5.0), RIGHT, buff=0.2
        )
        shock_label = Text("Shock: s ≈ 0.5", font_size=14, color=WARNING).next_to(
            conv_axes.c2p(2.5, -1.25), RIGHT, buff=0.2
        )
        
        self.play_timed("conv_plot_in", 40, 43,
            Create(conv_axes), FadeIn(conv_lbl_x), FadeIn(conv_lbl_y),
            Create(smooth_conv), Create(shock_conv),
            FadeIn(smooth_label), FadeIn(shock_label)
        )
        
        error_formula = MathTex(
            r"\varepsilon_{disc} \propto N^{-s}",
            font_size=36, color=PURPLE
        ).next_to(conv_axes, DOWN, buff=0.5)
        
        self.play_timed("formula_in", 43, 46, Write(error_formula))
        
        self.wait_timed("hold_end2", 46, 59)
        self.play_timed("cut2", 59, 60, *[FadeOut(m) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
