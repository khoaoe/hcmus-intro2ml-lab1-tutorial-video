
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0401_FNO(TimedScene):
    SCRIPT_ID = "4.1"
    SCRIPT_TITLE = "FNO — Cơ sở tần số & Định lý Tích chập"
    SCRIPT_START = 675.0
    SCRIPT_END = 750.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        
        title = Text("Fourier Neural Operator (FNO)", font_size=28, 
                     color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.4)
        
        axes = Axes(
            x_range=[0, 2*PI, PI/10],
            y_range=[-2, 2, 1],
            x_length=10, 
            y_length=5,
            axis_config={"color": GREY_B, "include_ticks": True},
            tips=False
        ).shift(DOWN * 0.5)
        
        def original_func(x):
            return np.sin(x) + 0.5*np.sin(3*x) + 0.3*np.sin(5*x)
        
        original_curve = axes.plot(original_func, color=WHITE, stroke_width=3)
        
        wave1 = axes.plot(lambda x: np.sin(x), color=BLUE, stroke_width=2)
        wave2 = axes.plot(lambda x: 0.5*np.sin(3*x), color=GREEN, stroke_width=2)
        wave3 = axes.plot(lambda x: 0.3*np.sin(5*x), color=RED, stroke_width=2)
        
        wave_labels = VGroup(
            MathTex(r"\sin(x)", font_size=36, color=BLUE),
            MathTex(r"+ 0.5\sin(3x)", font_size=36, color=GREEN),
            MathTex(r"+ 0.3\sin(5x)", font_size=36, color=RED),
        ).arrange(RIGHT, buff=0.4).next_to(axes, UP, buff=0.4)
        
        freq_axes = Axes(
            x_range=[0, 6, 1], 
            y_range=[0, 1.2, 0.3],
            x_length=4, 
            y_length=2,
            axis_config={"color": GREY_B, "include_ticks": True}
        ).shift(RIGHT * 3.5 + DOWN * 1)
        
        bar_heights = [1.0, 0, 0.5, 0, 0.3, 0]  # modes 1,2,3,4,5,6
        bar_colors = [BLUE, GREY, GREEN, GREY, RED, GREY]
        
        freq_bars = VGroup()
        for i, (h, c) in enumerate(zip(bar_heights, bar_colors)):
            if h > 0:
                x_val = i + 1
                bottom_pt = freq_axes.c2p(x_val, 0)
                top_pt = freq_axes.c2p(x_val, h)
                
                bar_rect = Rectangle(
                    width=0.4, 
                    height=top_pt[1] - bottom_pt[1],
                    fill_color=c, 
                    fill_opacity=0.7, 
                    stroke_width=0
                )
                bar_rect.move_to((top_pt + bottom_pt) / 2)
                freq_bars.add(bar_rect)
        
        freq_label = Text("Phổ tần số (|â(ω)|)", font_size=16, color=GREY).next_to(freq_axes, UP, buff=0.2)
        
        fft_formula = MathTex(
            r"\hat{a}(\omega) = \int_{\Omega} a(x)\, e^{-2\pi i \langle x, \omega \rangle}\, dx",
            font_size=28, color=WHITE
        ).to_edge(DOWN, buff=0.5)
        
        
        self.play_timed("beat1_init", 0, 2, FadeIn(title), Create(axes), Create(original_curve))
        
        self.play_timed("decomp1", 2, 4, Transform(original_curve, wave1), FadeIn(wave_labels[0]))
        self.play_timed("decomp2", 4, 6, Transform(original_curve, wave2), FadeIn(wave_labels[1]))
        self.play_timed("decomp3", 6, 8, Transform(original_curve, wave3), FadeIn(wave_labels[2]))
        
        self.play_timed("recombine", 8, 9.5,
            FadeOut(wave_labels),
            Transform(original_curve, axes.plot(original_func, color=WHITE, stroke_width=3))
        )
        
        graph_group = VGroup(axes, original_curve)
        self.play_timed("shrink_graph", 9.5, 10.5,
            graph_group.animate.scale(0.6).move_to(LEFT * 3.5 + DOWN * 0.5)
        )
        
        self.play_timed("freq_bars", 10.5, 12.5,
            Create(freq_axes),
            FadeIn(freq_label),
            *[GrowFromEdge(bar, DOWN) for bar in freq_bars]
        )
        
        kmax_note = Text("k_max = 5: chỉ giữ low-frequency modes", font_size=16, 
                         color=YELLOW).next_to(freq_axes, DOWN, buff=0.3)
        self.play_timed("kmax_note", 12.5, 13.5, FadeIn(kmax_note))
        
        self.play_timed("fft_formula", 13.5, 15, Write(fft_formula))
        self.wait_timed("hold_beat1", 15, 34)
        
        self.play_timed("clear_beat1", 34, 35, *[FadeOut(m) for m in self.mobjects])
        
        
        pipeline_title = Text("FNO Layer Pipeline", font_size=24, color=NVIDIA_GREEN, 
                              weight=BOLD).to_edge(UP, buff=0.4)
        
        step_data = [
            ("FFT", r"\mathcal{F}", BLUE),
            ("Spectral\nMultiply", r"R(\omega) \cdot \hat{v}(\omega)", NVIDIA_GREEN),
            ("IFFT", r"\mathcal{F}^{-1}", RED),
        ]
        pipeline_blocks = VGroup()
        for name, eq, color in step_data:
            box = RoundedRectangle(width=2.2, height=1.7, corner_radius=0.1,
                                   stroke_color=color, fill_color=CARD_BG, fill_opacity=0.6)
            text = VGroup(
                Text(name, font_size=20, color=color, weight=BOLD),
                MathTex(eq, font_size=22, color=WHITE),
                Text("Matrix phức (d x d)", font_size=14, color=GREY),
            ).arrange(DOWN, buff=0.1).move_to(box)
            pipeline_blocks.add(VGroup(box, text))
        
        pipeline_blocks.arrange_in_grid(
            rows=1,
            buff=0.6,
            col_alignments=["c"] * len(pipeline_blocks)
        ).shift(UP * 1.5)
        
        grid_bg = Rectangle(
            width=pipeline_blocks.width * 1.2,
            height=pipeline_blocks.height * 1.2,
            fill_color=BLACK,
            fill_opacity=0.3,
            stroke_color=GREY_B,
            stroke_width=0.5
        ).move_to(pipeline_blocks)
        
        arrow1 = Arrow(pipeline_blocks[0].get_right(), pipeline_blocks[1].get_left(), 
                       color=WHITE, buff=0.1, stroke_width=2)
        arrow2 = Arrow(pipeline_blocks[1].get_right(), pipeline_blocks[2].get_left(), 
                       color=WHITE, buff=0.1, stroke_width=2)
        
        conv_title = Text("Định lý Tích chập", font_size=20, color=YELLOW, 
                          weight=BOLD).shift(DOWN * 0.5)
        
        spatial_label = Text("Tích chập trong Spatial Domain", font_size=16, color=BLUE
                             ).shift(DOWN * 1.2 + LEFT * 3)
        spatial_complexity = MathTex(r"O(N^2)", font_size=24, color=RED
                                     ).next_to(spatial_label, DOWN, buff=0.2)
        
        kernel = Square(side_length=0.3, color=RED, fill_opacity=0.5).shift(DOWN * 2.5 + LEFT * 5)
        signal_line = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=2).shift(DOWN * 2.5 + LEFT * 3)
        
        freq_label = Text("Nhân trong Frequency Domain", font_size=16, color=NVIDIA_GREEN
                          ).shift(DOWN * 1.2 + RIGHT * 3)
        freq_complexity = MathTex(r"O(N \log N)", font_size=24, color=NVIDIA_GREEN
                                  ).next_to(freq_label, DOWN, buff=0.2)
        
        freq_bars_small = VGroup(*[
            Rectangle(width=0.15, height=0.3 + i*0.1, 
                      fill_color=NVIDIA_GREEN, fill_opacity=0.7, stroke_width=0)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.05).shift(RIGHT * 3 + DOWN * 2.5)
        
        branch_title = Text("Hai nhánh của FNO Layer", font_size=18, color=WHITE, 
                            weight=BOLD).shift(DOWN * 0.5)
        
        global_branch = VGroup(
            Text("Nhánh Toàn cục (Spectral)", font_size=16, color=BLUE),
            Text("Học tương tác xa qua Fourier modes", font_size=14, color=GREY),
        ).arrange(DOWN, buff=0.1).shift(DOWN * 1.5 + LEFT * 3)
        
        local_branch = VGroup(
            MathTex(r"W \cdot a(x)", font_size=20, color=NVIDIA_GREEN),
            Text("Nhánh Cục bộ (Pointwise)", font_size=16, color=NVIDIA_GREEN),
            Text("Bù đắp thông tin cục bộ", font_size=14, color=GREY),
        ).arrange(DOWN, buff=0.1).shift(DOWN * 1.5 + RIGHT * 3)
        
        final_complexity = VGroup(
            Text("Độ phức tạp: ", font_size=20, color=NVIDIA_GREEN),
            MathTex(r"O(N \log N)", font_size=24, color=NVIDIA_GREEN)
        ).arrange(RIGHT, buff=0.15).shift(DOWN * 3.0)

        self.play_timed("pipe_title", 35, 36, FadeIn(pipeline_title))
        
        self.play_timed("pipe_blocks", 36, 38, FadeIn(grid_bg), FadeIn(pipeline_blocks))
        self.play_timed("pipe_arr1", 38, 38.5, GrowArrow(arrow1))
        self.play_timed("pipe_arr2", 38.5, 39, GrowArrow(arrow2))
        
        r_omega_highlight = SurroundingRectangle(pipeline_blocks[1][1][1], color=YELLOW, buff=0.1)
        self.play_timed("r_omega_hl_in", 39, 40, Create(r_omega_highlight))
        self.wait_timed("r_omega_hold", 40, 41)
        self.play_timed("r_omega_hl_out", 41, 42, FadeOut(r_omega_highlight))
        
        self.play_timed("conv_title", 42, 43, FadeIn(conv_title))
        self.play_timed("conv_spatial", 43, 44, FadeIn(spatial_label), FadeIn(spatial_complexity), FadeIn(signal_line), FadeIn(kernel))
        self.play_timed("conv_freq", 44, 45, FadeIn(freq_label), FadeIn(freq_complexity), FadeIn(freq_bars_small))
        
        kernel_trace = TracedPath(kernel.get_center, stroke_color=YELLOW, stroke_width=2.5, stroke_opacity=0.8)
        def fading_trail_update(mob, alpha):
            mob.set_stroke(opacity=1 - alpha * 0.5)
            return mob
            
        self.play_timed("conv_anim", 45, 47,
            kernel.animate.move_to(signal_line.get_right()),
            Create(kernel_trace),
            UpdateFromAlphaFunc(kernel_trace, fading_trail_update),
            rate_func=linear
        )
        self.play_timed("freq_anim", 47, 48,
            *[bar.animate.set_height(bar.height * 1.5) for bar in freq_bars_small]
        )
        
        self.play_timed("clear_conv", 48, 49,
            FadeOut(conv_title), FadeOut(spatial_label), FadeOut(spatial_complexity), FadeOut(signal_line), FadeOut(kernel), FadeOut(kernel_trace), FadeOut(freq_label), FadeOut(freq_complexity), FadeOut(freq_bars_small)
        )
        self.play_timed("branch_title", 49, 50, FadeIn(branch_title))
        self.play_timed("branches_in", 50, 51.5, FadeIn(global_branch), FadeIn(local_branch))
        
        self.play_timed("final_comp", 51.5, 52.5, FadeIn(final_complexity))
        
        self.wait_timed("hold_end", 52.5, 74)
        self.play_timed("cut2", 74, 75, *[FadeOut(m) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
