"""
Scene 1.2 — Plot twist: Thế giới khoa học — dữ liệu là hàm số
Source: original_outline.tex, Section 1, Scene 1.2
Global time: 0:45 – 1:45
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0102_PlotTwistFunctionData(TimedScene):
    SCRIPT_ID = "1.2"
    SCRIPT_TITLE = "Plot twist — Dữ liệu khoa học là hàm số"
    SCRIPT_START = 45.0
    SCRIPT_END = 105.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [0:45–1:00] R^n shatter → globe with 3 field layers ──
        rn_frame = RoundedRectangle(
            width=6, height=4, corner_radius=0.2,
            stroke_color=INPUT, stroke_width=2, fill_opacity=0
        )
        rn_label = MathTex(r"\mathbb{R}^n", font_size=40, color=INPUT).move_to(rn_frame)
        rn_group = VGroup(rn_frame, rn_label)

        self.add(rn_group)
        self.play_timed("shatter_rn", 0, 2, FadeOut(rn_group, shift=UP * 0.5))

        # Globe (circle stand-in)
        globe = Circle(radius=1.8, color=SCIENCE, fill_opacity=0.15, stroke_width=2)
        globe_label = Text("🌍", font_size=60).move_to(globe)
        # Field layers
        heat_layer = Arc(radius=2.0, angle=PI, color=WARNING, stroke_width=3).shift(UP * 0.2)
        wind_layer = Arc(radius=2.2, angle=PI * 0.8, start_angle=PI * 0.3, color=INPUT, stroke_width=3)
        pressure_layer = Arc(radius=2.4, angle=PI * 0.6, start_angle=PI * 0.7, color=OPERATOR, stroke_width=3)

        self.play_timed("globe", 2, 4, FadeIn(globe), FadeIn(globe_label))
        self.play_timed("heat", 4, 5, FadeIn(heat_layer))
        self.play_timed("wind", 5, 6, FadeIn(wind_layer))
        self.play_timed("pressure", 6, 7, FadeIn(pressure_layer))

        layer_labels = VGroup(
            Text("Nhiệt độ", font_size=16, color=WARNING),
            Text("Gió", font_size=16, color=INPUT),
            Text("Áp suất", font_size=16, color=OPERATOR),
        ).arrange(RIGHT, buff=0.8).next_to(globe, DOWN, buff=0.5)
        self.play_timed("layer_labels", 7, 8, FadeIn(layer_labels))
        self.wait_timed("hold_globe", 8, 15)

        # ── Beat 2: [1:00–1:25] 4 domain icons ──
        self.play_timed("clear_globe", 15, 15.5,
                        *[FadeOut(m) for m in [globe, globe_label, heat_layer, wind_layer,
                                               pressure_layer, layer_labels]])

        domains = VGroup()
        domain_data = [
            ("Da liễu", "Gradient da\nliên tục", WARNING),
            ("Địa vật lý", "Sóng 3D\nđịa chấn", PURPLE),
            ("CFD", "Dòng khí\n4D vector", INPUT),
            ("Khí hậu", "100+ hàm\ntrên cầu", OUTPUT),
        ]
        for name, desc, color in domain_data:
            icon = Circle(radius=0.4, color=color, fill_opacity=0.3, stroke_width=2)
            title = Text(name, font_size=22, color=color, weight=BOLD).next_to(icon, DOWN, buff=0.15)
            subtitle = Text(desc, font_size=14, color=MUTED).next_to(title, DOWN, buff=0.1)
            domains.add(VGroup(icon, title, subtitle))
        domains.arrange(RIGHT, buff=1.0)

        for i, dom in enumerate(domains):
            t_start = 15.5 + i * 4.0
            t_end = t_start + 2.0
            self.play_timed(f"domain_{i}", t_start, t_end, FadeIn(dom, shift=UP * 0.3))
            self.wait_timed(f"hold_domain_{i}", t_end, t_start + 4.0)

        # ── Beat 3: [1:25–1:45] Zoom close → continuous gradient, no pixel ──
        self.play_timed("clear_domains", 31.5, 32, *[FadeOut(m) for m in domains])

        # Continuous gradient field
        gradient_rect = Rectangle(width=10, height=5, fill_opacity=0.8, stroke_width=0)
        gradient_rect.set_color_by_gradient(WARNING, INPUT, OUTPUT)

        no_grid_label = Text("Không pixel — Liên tục hoàn toàn", font_size=24, color=TEXT)
        overlay = Text("Data = Functions", font_size=40, color=NVIDIA_GREEN, weight=BOLD)
        VGroup(no_grid_label, overlay).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play_timed("gradient", 32, 34, FadeIn(gradient_rect))
        self.play_timed("no_grid", 34, 36, FadeIn(no_grid_label))
        self.play_timed("overlay_text", 36, 38, FadeIn(overlay))
        self.wait_timed("hold_end", 38, 59)

        # Hard cut
        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
