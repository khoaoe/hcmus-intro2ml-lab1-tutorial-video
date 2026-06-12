from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

class Scene0602_Theory_UQ(TimedScene):
    SCRIPT_ID = "6.2"
    SCRIPT_TITLE = "Lý thuyết nền tảng & Lượng hóa bất định"
    SCRIPT_START = 1525.0
    SCRIPT_END = 1600.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Open Problems: Lý thuyết & Lượng hóa bất định", font_size=28,
                     color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b1_title", 0, 2, FadeIn(title))

        divider = Line(UP*3.1, DOWN*2.8, color=GRAY_B, stroke_width=1.5)
        self.play_timed("b1_divider", 2, 3, Create(divider))

        dl_header = Text("Deep Learning", font_size=22, color=GREEN_SCREEN, weight=BOLD).shift(LEFT*3.5 + UP*3.1)
        
        dl_nodes_data = [
            ("Approx.\nTheory", LEFT*4.5 + UP*1.5),
            ("VC\nDimen-\nsion", LEFT*2.5 + UP*1.5),
            ("Rade-\nmacher\nComple-\nxity", LEFT*4.5 + DOWN*0.0),
            ("PAC-Bayes\nBounds", LEFT*2.5 + DOWN*0.0),
            ("NTK\nTheory", LEFT*3.5 + UP*0.7),
            ("General-\nization\nBounds", LEFT*3.5 + DOWN*1.0),
        ]
        
        dl_nodes = VGroup()
        for name, pos in dl_nodes_data:
            bg_circle = Circle(radius=0.45, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0)
            fg_circle = Circle(radius=0.45, color=GREEN_SCREEN, fill_color=GREEN_SCREEN, 
                               fill_opacity=0.2, stroke_width=2)
            
            lines = name.split("\n")
            text_mobj = VGroup(*[Text(line, font_size=12, color=GREEN_SCREEN, weight=BOLD) for line in lines])
            text_mobj.arrange(DOWN, buff=0.03)
            
            node = VGroup(
                bg_circle,
                fg_circle,
                text_mobj
            )
            node[2].move_to(fg_circle)
            node.move_to(pos)
            dl_nodes.add(node)
        
        dl_edges = VGroup()
        connections = [(0,1), (0,2), (1,3), (2,3), (0,4), (1,4), (2,5), (3,5), (4,5)]
        for i, j in connections:
            edge = Line(dl_nodes[i].get_center(), dl_nodes[j].get_center(),
                       color=GREEN_SCREEN, stroke_width=1, stroke_opacity=0.4)
            dl_edges.add(edge)

        dl_nodes.set_z_index(1)
        dl_edges.set_z_index(0)

        VGroup(dl_nodes, dl_edges).scale(1.4, about_point=LEFT*3.5 + UP*0.5).shift(UP*0.3)

        self.play_timed("b1_dl_header", 3, 4, FadeIn(dl_header))
        self.play_timed("b1_dl_nodes", 4, 9,
                        LaggedStart(*[FadeIn(n, scale=0.5) for n in dl_nodes], lag_ratio=0.15),
                        LaggedStart(*[Create(e) for e in dl_edges], lag_ratio=0.1))

        no_header = Text("Neural Operators", font_size=22, color=WARNING, weight=BOLD).shift(RIGHT*3.5 + UP*3.1)
        
        no_fog = VGroup()
        np.random.seed(42)
        for _ in range(15):
            fog_circle = Circle(
                radius=np.random.uniform(0.4, 0.9),
                color=WARNING, fill_opacity=np.random.uniform(0.05, 0.12),
                stroke_width=0
            ).shift(RIGHT*(3.5 + np.random.uniform(-1.5, 1.5)) + 
                   DOWN*np.random.uniform(-1.5, 1.5))
            no_fog.add(fog_circle)
        
        ua_lines = ["Universal", "Approx."]
        ua_text = VGroup(*[Text(l, font_size=12, color=WARNING, weight=BOLD) for l in ua_lines]).arrange(DOWN, buff=0.05)
        
        ua_node = VGroup(
            Circle(radius=0.5, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0),
            Circle(radius=0.5, color=WARNING, fill_color=WARNING, 
                   fill_opacity=0.15, stroke_width=2, stroke_opacity=0.6),
            ua_text
        )
        ua_node[2].move_to(ua_node[1])
        ua_node.shift(RIGHT*3.5 + DOWN*0.3)
        
        ua_node.scale(1.2)
        VGroup(no_fog, ua_node).shift(UP*0.3)

        self.play_timed("b1_no_header", 9, 10, FadeIn(no_header))
        
        self.play_timed("b1_no_fog", 10, 14,
                        LaggedStart(
                            FadeIn(no_fog, run_time=2),
                            FadeIn(ua_node, run_time=1.5),
                            lag_ratio=0.3
                        ))
        
        self.play_timed("b1_no_pulse", 14, 16,
                        no_fog.animate.set_opacity(0.15))

        beacon_data = [
            (VGroup(Text("Convergence", font_size=13, weight=BOLD),
                    MathTex(r"\text{as } N \to \infty?", font_size=16)).arrange(DOWN, buff=0.03),
             LEFT*3.5 + DOWN*3.1, YELLOW),
            (VGroup(Text("Architecture-", font_size=13, weight=BOLD),
                    Text("specific", font_size=13, weight=BOLD),
                    Text("limits?", font_size=13, weight=BOLD)).arrange(DOWN, buff=0.03),
             ORIGIN + DOWN*3.1, ORANGE),
            (VGroup(Text("Param-Gen", font_size=13, weight=BOLD),
                    Text("in function", font_size=13, weight=BOLD),
                    Text("space?", font_size=13, weight=BOLD)).arrange(DOWN, buff=0.03),
             RIGHT*3.5 + DOWN*3.1, RED),
        ]
        
        beacons = VGroup()
        beacon_texts = VGroup()
        for label_mobj, pos, color in beacon_data:
            label_mobj.set_color(color)
            beacon = VGroup(
                Circle(radius=0.66, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0),
                Circle(radius=0.66, color=color, fill_color=color, 
                       fill_opacity=0.25, stroke_width=2.5),
                label_mobj
            )
            beacon[2].move_to(beacon[1])
            beacon.move_to(pos)
            beacons.add(beacon)
            beacon_texts.add(beacon[2])
            
        beacons.set_z_index(2)
        
        self.play_timed("b1_beacon1", 16, 22,
                        FadeIn(beacons[0]),
                        Flash(beacons[0], color=YELLOW, flash_radius=0.8, line_length=0.2))
        self.play_timed("b1_beacon2", 22, 28,
                        FadeIn(beacons[1]),
                        Flash(beacons[1], color=ORANGE, flash_radius=0.8, line_length=0.2))
        self.play_timed("b1_beacon3", 28, 34,
                        FadeIn(beacons[2]),
                        Flash(beacons[2], color=RED, flash_radius=0.8, line_length=0.2))
        
        self.play_timed("b1_beacons_pulse", 34, 38,
                        *[b[0].animate.scale(1.1).set_fill(opacity=0.4) for b in beacons],
                        rate_func=there_and_back)
        
        self.wait_timed("b1_hold", 38, 40)

        self.play_timed("clear_b1", 40, 42,
                        *[FadeOut(m) for m in [title, divider, dl_header, dl_nodes, dl_edges,
                                               no_header, no_fog, ua_node,
                                               beacons]])

        uq_title = Text("Lượng hóa bất định trên không gian hàm", font_size=26,
                        color=PHYSICS, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 42, 44, FadeIn(uq_title))

        axes = Axes(
            x_range=[0, 6, 1], y_range=[-1.5, 2.5, 0.5],
            x_length=10, y_length=4,
            axis_config={"color": GRAY_B, "include_ticks": True, "include_numbers": False}
        ).shift(UP*0.5)
        
        x_label = Text("Vị trí x", font_size=24, color=GRAY_B).next_to(axes.x_axis, DOWN, buff=0.2).shift(LEFT*2.5)
        y_label = Text("Giá trị hàm", font_size=24, color=GRAY_B).next_to(axes.y_axis, LEFT, buff=0.2)

        self.play_timed("b2_axes", 44, 46, Create(axes), FadeIn(x_label), FadeIn(y_label))

        gt_func = lambda x: np.sin(1.2*x) + 0.3*np.cos(2.5*x)
        gt_curve = axes.plot(gt_func, x_range=[0, 6], color=WHITE, stroke_width=3)
        gt_label = Text("Ground Truth", font_size=21, color=WHITE).next_to(axes.c2p(5.5, gt_func(5.5)), RIGHT, buff=1.0).shift(UP*0.2)

        pred_func = lambda x: np.sin(1.2*x) + 0.3*np.cos(2.5*x) + 0.08*np.sin(5*x)
        pred_curve = axes.plot(pred_func, x_range=[0, 6], color=GREEN_SCREEN, stroke_width=3)
        pred_label = VGroup(
            Text("Prediction", font_size=21, color=GREEN_SCREEN),
            MathTex(r"u_\theta", font_size=24, color=GREEN_SCREEN)
        ).arrange(RIGHT, buff=0.05).next_to(axes.c2p(5.5, pred_func(5.5)), RIGHT, buff=1.0).shift(DOWN*0.2)

        self.play_timed("b2_curves", 46, 50,
                        Create(gt_curve), FadeIn(gt_label),
                        Create(pred_curve), FadeIn(pred_label))

        upper_func = lambda x: pred_func(x) + 0.25 + 0.1*np.sin(2*x)
        lower_func = lambda x: pred_func(x) - 0.25 - 0.1*np.sin(2*x)
        
        upper_curve = axes.plot(upper_func, x_range=[0, 6], color=YELLOW, stroke_width=1.5, stroke_opacity=0.6)
        lower_curve = axes.plot(lower_func, x_range=[0, 6], color=YELLOW, stroke_width=1.5, stroke_opacity=0.6)
        
        band_area = VMobject(fill_color=YELLOW, fill_opacity=0.2, stroke_width=0)
        
        x_vals = np.linspace(0, 6, 60)
        upper_pts = [axes.c2p(x, upper_func(x)) for x in x_vals]
        lower_pts = [axes.c2p(x, lower_func(x)) for x in reversed(x_vals)]
        band_area.set_points_smoothly(upper_pts + lower_pts + [upper_pts[0]])

        band_label = VGroup(
            Text("Confidence Band", font_size=21, color=YELLOW, weight=BOLD),
            Text("(per-point error bar)", font_size=21, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(axes.c2p(1.0, upper_func(1.0)), UP, buff=0.5)

        self.play_timed("b2_band", 50, 54,
                        FadeIn(band_area),
                        Create(upper_curve), Create(lower_curve),
                        FadeIn(band_label))

        mc_label = Text("Monte Carlo: 50 solver runs", font_size=21, color=RED).to_edge(DOWN, buff=0.5)
        
        mc_curves = VGroup()
        np.random.seed(123)
        for i in range(12):
            noise = np.random.uniform(-0.05, 0.05)
            phase = np.random.uniform(-0.3, 0.3)
            mc_func = lambda x, n=noise, p=phase: pred_func(x) + n + 0.15*np.sin(2*x + p)
            curve = axes.plot(mc_func, x_range=[0, 6], color=RED, 
                             stroke_width=1.2, stroke_opacity=0.5)
            mc_curves.add(curve)

        self.play_timed("b2_monte_carlo", 54, 59,
                        LaggedStart(*[Create(c, run_time=0.5) for c in mc_curves], lag_ratio=0.1),
                        FadeIn(mc_label))

        cross = Cross(mc_label, color=RED, stroke_width=3).scale(1.2)
        
        better_label = VGroup(
            Text("✓ Conformal Prediction / GANO", font_size=21, color=GREEN_SCREEN, weight=BOLD),
            Text("Coverage guarantee, no re-solve", font_size=21, color=GREEN_SCREEN, weight=BOLD)
        ).arrange(DOWN, center=True, buff=0.15).next_to(mc_label, UP, buff=0.4)

        self.play_timed("b2_better", 59, 65,
                        Create(cross),
                        FadeIn(better_label),
                        mc_curves.animate.set_opacity(0.15))

        self.play_timed("b2_band_pulse", 65, 70,
                        band_area.animate.set_fill(opacity=0.4),
                        Flash(band_label, color=YELLOW, flash_radius=0.8),
                        rate_func=there_and_back)

        self.wait_timed("b2_hold", 70, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=1.0) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
