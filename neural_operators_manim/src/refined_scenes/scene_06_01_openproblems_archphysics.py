from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

class Scene0601_OpenProblems_ArchPhysics(TimedScene):
    SCRIPT_ID = "6.1"
    SCRIPT_TITLE = "Open Problems: Kiến trúc & Vật lý"
    SCRIPT_START = 1450.0
    SCRIPT_END = 1525.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Open Problems: Kiến trúc & Tích hợp vật lý", 
                     font_size=32, color=GOLD, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b1_title", 0, 2, Write(title))
        
        divider = Line(UP*3.2, DOWN*3.2, color=WHITE, stroke_width=2)
        self.play_timed("b1_divider", 2, 3, Create(divider))
        
        known_title = Text("KNOWN", font_size=28, color=GREEN_SCREEN, weight=BOLD)
        known_title.shift(LEFT*3.5 + UP*2.5)
        
        fno_icon = VGroup(*[
            ParametricFunction(
                lambda t: np.array([t/3, np.sin(3*t + i*PI/3)/4, 0]),
                t_range=[-PI, PI], color=GREEN_SCREEN, stroke_width=2
            ).shift(LEFT*5.5 + UP*(1.5 - i*0.3))
            for i in range(3)
        ])
        fno_label = Text("FNO", font_size=20, color=GREEN_SCREEN).next_to(fno_icon, DOWN, buff=0.1)
        fno_group = VGroup(fno_icon, fno_label)
        
        gno_nodes = VGroup(*[Dot(radius=0.08, color=GREEN_SCREEN) for _ in range(5)])
        gno_nodes.arrange_in_grid(2, 3, buff=0.25).shift(LEFT*5.5 + DOWN*0.2)
        gno_edges = VGroup(*[
            Line(gno_nodes[i].get_center(), gno_nodes[j].get_center(), 
                 color=GREEN_SCREEN, stroke_width=1.5, stroke_opacity=0.6)
            for i, j in [(0,1), (0,2), (1,3), (2,4), (1,4), (2,3)]
        ])
        gno_icon = VGroup(gno_edges, gno_nodes)
        gno_label = Text("GNO", font_size=20, color=GREEN_SCREEN).next_to(gno_icon, DOWN, buff=0.1)
        gno_group = VGroup(gno_icon, gno_label)
        
        u_no_path = ParametricFunction(
            lambda t: np.array([t/2, abs(t)/3 - 0.3, 0]),
            t_range=[-1.5, 1.5], color=GREEN_SCREEN, stroke_width=3
        ).shift(LEFT*5.5 + DOWN*1.5)
        u_no_label = Text("U-NO", font_size=20, color=GREEN_SCREEN).next_to(u_no_path, DOWN, buff=0.1)
        uno_group = VGroup(u_no_path, u_no_label)
        
        kernel_icon = Rectangle(width=1.2, height=1.2, color=GREEN_SCREEN, stroke_width=2).shift(LEFT*2.0 + UP*1.0)
        kernel_grid = VGroup(*[
            Dot(radius=0.08, color=GREEN_SCREEN, fill_opacity=0.3 + 0.08*i)
            for i in range(9)
        ]).arrange_in_grid(3, 3, buff=0.2).move_to(kernel_icon)
        kernel_label = Text("Integral Kernels", font_size=18, color=GREEN_SCREEN).next_to(kernel_icon, UP, buff=0.2)
        
        res_coarse = Rectangle(width=0.8, height=0.8, color=GREEN_SCREEN, stroke_width=2).shift(LEFT*2.6 + DOWN*1.5)
        res_fine = VGroup(*[
            Square(side_length=0.2, stroke_width=1, color=GREEN_SCREEN) 
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0).move_to(res_coarse.get_center() + RIGHT*1.2)
        
        res_arrow = Arrow(res_coarse.get_right(), res_fine.get_left(), buff=0.1, color=GREEN_SCREEN)
        res_label = Text("Resolution Invariant", font_size=18, color=GREEN_SCREEN).next_to(VGroup(res_coarse, res_fine), DOWN, buff=0.2)
        
        arrow_fno_k = Arrow(fno_group.get_right(), kernel_icon.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=2)
        arrow_gno_k = Arrow(gno_group.get_right(), kernel_icon.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=2)
        arrow_uno_k = Arrow(uno_group.get_right(), kernel_icon.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=2)
        
        arrow_k_res = Arrow(kernel_icon.get_bottom(), VGroup(res_coarse, res_fine).get_top(), color=GREEN_SCREEN, buff=0.2, stroke_width=2)
        
        self.play_timed("b1_known_title", 3, 4, FadeIn(known_title))
        self.play_timed("b1_known_icons", 4, 8,
                        LaggedStart(
                            GrowFromCenter(fno_icon), Write(fno_label),
                            *[GrowFromPoint(n, gno_nodes.get_center()) for n in gno_nodes],
                            Create(gno_edges), Write(gno_label),
                            Create(u_no_path), Write(u_no_label),
                            lag_ratio=0.2
                        ))
        self.play_timed("b1_known_props", 8, 11,
                        Create(kernel_icon), Create(kernel_grid), Write(kernel_label),
                        Create(res_coarse), Create(res_fine), Create(res_arrow), Write(res_label),
                        Create(arrow_fno_k), Create(arrow_gno_k), Create(arrow_uno_k), Create(arrow_k_res))
        
        unknown_title = Text("UNKNOWN", font_size=32, color=RED, weight=BOLD).shift(RIGHT*3.5 + UP*2.5)

        island1 = RoundedRectangle(
            width=3.2, height=1.2, corner_radius=0.15,
            color=RED, stroke_width=3, stroke_opacity=0.8,
            fill_color=RED, fill_opacity=0.15
        )
        island1.shift(RIGHT*3.5 + UP*1.0)
        q1_text = Text("Max-pooling trong\nkhông gian hàm?", font_size=20, color=RED, weight=BOLD)
        q1_text.move_to(island1)

        island2 = RoundedRectangle(
            width=3.2, height=1.2, corner_radius=0.15,
            color=ORANGE, stroke_width=3, stroke_opacity=0.8,
            fill_color=ORANGE, fill_opacity=0.15
        )
        island2.shift(RIGHT*3.5 + DOWN*0.3)
        q2_text = Text("Attention biến thể\ncho operators?", font_size=20, color=ORANGE, weight=BOLD)
        q2_text.move_to(island2)

        island3 = RoundedRectangle(
            width=3.2, height=1.2, corner_radius=0.15,
            color=RED_E, stroke_width=3, stroke_opacity=0.8,
            fill_color=RED_E, fill_opacity=0.15
        )
        island3.shift(RIGHT*3.5 + DOWN*1.6)
        q3_text = Text("Scale 3D > 10M points?", font_size=20, color=RED_E, weight=BOLD)
        q3_text.move_to(island3)

        self.play_timed("b1_unknown_title", 11, 12, FadeIn(unknown_title))

        self.play_timed("b1_unknown_island1", 13, 16,
                        Create(island1), Write(q1_text))

        self.play_timed("b1_unknown_island2", 17, 20,
                        Create(island2), Write(q2_text))

        self.play_timed("b1_unknown_island3", 21, 24,
                        Create(island3), Write(q3_text))

        self.wait_timed("b1_hold", 24, 35)

        self.play_timed("clear_b1", 35, 37, *[FadeOut(m) for m in self.mobjects])

        pinO_title = Text("Tích hợp vật lý: PINO & Những câu hỏi mở", font_size=26,
                          color=PHYSICS, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 37, 39, FadeIn(pinO_title))

        nn_box = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.5, color=INPUT, stroke_width=3, fill_color=BLACK, fill_opacity=0.8).shift(LEFT*2.0 + UP*0.5)
        nn_label = MathTex("u_\\theta", font_size=48, color=INPUT).move_to(nn_box)
        
        pde_box = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.5, color=OPERATOR, stroke_width=3, fill_color=BLACK, fill_opacity=0.8).shift(RIGHT*2.0 + UP*0.5)
        pde_label = Text("PDE Residual", font_size=29, color=OPERATOR).move_to(pde_box)
        
        arrow_forward = Arrow(nn_box.get_right(), pde_box.get_left(), buff=0.1, color=WHITE)
        
        loss_data_box = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.0, color=INPUT, stroke_width=2, fill_color=BLACK, fill_opacity=0.8).shift(LEFT*2.0 + DOWN*1.5)
        loss_data_label = MathTex("\mathcal{L}_{data}", font_size=36, color=INPUT).move_to(loss_data_box)
        
        loss_phys_box = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.0, color=WARNING, stroke_width=2, fill_color=BLACK, fill_opacity=0.8).shift(RIGHT*2.0 + DOWN*1.5)
        loss_phys_label = MathTex("\mathcal{L}_{physics}", font_size=36, color=WARNING).move_to(loss_phys_box)
        
        loss_total_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.0, color=GREEN_SCREEN, stroke_width=2, fill_color=BLACK, fill_opacity=0.8).shift(DOWN*3.0)
        loss_total_label = MathTex("\mathcal{L}_{total}", font_size=36, color=GREEN_SCREEN).move_to(loss_total_box)

        arrow_data_data = Arrow(nn_box.get_bottom(), loss_data_box.get_top(), color=INPUT, buff=0.1)
        arrow_pde_phys = Arrow(pde_box.get_bottom(), loss_phys_box.get_top(), color=WARNING, buff=0.1)
        arrow_data_total = Arrow(loss_data_box.get_bottom(), loss_total_box.get_left(), color=GREEN_SCREEN, buff=0.1)
        arrow_phys_total = Arrow(loss_phys_box.get_bottom(), loss_total_box.get_right(), color=GREEN_SCREEN, buff=0.1)

        self.play_timed("b2_pipeline", 39, 45,
                        FadeIn(nn_box), FadeIn(nn_label), FadeIn(pde_box), FadeIn(pde_label), Create(arrow_forward),
                        FadeIn(loss_data_box), FadeIn(loss_data_label), FadeIn(loss_phys_box), FadeIn(loss_phys_label),
                        FadeIn(loss_total_box), FadeIn(loss_total_label),
                        Create(arrow_data_data), Create(arrow_pde_phys), Create(arrow_data_total), Create(arrow_phys_total))

        q1_pino = VGroup(
            Circle(radius=0.3, color=WARNING, fill_color=WARNING, fill_opacity=0.2),
            Text("1", font_size=20, color=WARNING)
        ).shift(LEFT*4.2 + UP*2.6)
        q1_text_pino = VGroup(
            Text("Hard-code", font_size=18, color=WARNING),
            Text("Conservation Laws?", font_size=18, color=WARNING)
        ).arrange(DOWN, buff=0.1).next_to(q1_pino, DOWN, buff=0.2)
        
        q2_pino = VGroup(
            Circle(radius=0.3, color=RED_E, fill_color=RED_E, fill_opacity=0.2),
            Text("2", font_size=20, color=RED_E)
        ).shift(UP*2.6)
        q2_text_pino = VGroup(
            Text("Stable High-order", font_size=18, color=RED_E),
            Text("Derivatives?", font_size=18, color=RED_E)
        ).arrange(DOWN, buff=0.1).next_to(q2_pino, DOWN, buff=0.2)
        
        q3_pino = VGroup(
            Circle(radius=0.3, color=ORANGE, fill_color=ORANGE, fill_opacity=0.2),
            Text("3", font_size=20, color=ORANGE)
        ).shift(RIGHT*4.2 + UP*2.6)
        q3_text_pino = VGroup(
            Text("Auto-balance", font_size=18, color=ORANGE),
            Text("Loss Terms?", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.1).next_to(q3_pino, DOWN, buff=0.2)

        self.play_timed("b2_q1", 45, 49, FadeIn(q1_pino), Write(q1_text_pino), Flash(q1_pino, color=WARNING, flash_radius=0.4))
        self.play_timed("b2_q2", 49, 53, FadeIn(q2_pino), Write(q2_text_pino), Flash(q2_pino, color=RED_E, flash_radius=0.4))
        self.play_timed("b2_q3", 53, 57, FadeIn(q3_pino), Write(q3_text_pino), Flash(q3_pino, color=ORANGE, flash_radius=0.4))

        warning_txt = Text("Thực tế: chưa có phương pháp tối ưu", font_size=18, color=RED, weight=BOLD).next_to(loss_total_box, DOWN, buff=0.15)
        self.play_timed("b2_warning", 57, 62,
                        FadeIn(warning_txt),
                        Flash(warning_txt, color=RED, flash_radius=0.8, line_length=0.2))

        self.wait_timed("b2_hold", 62, 73)

        self.play_timed("cut", 73, 75, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
