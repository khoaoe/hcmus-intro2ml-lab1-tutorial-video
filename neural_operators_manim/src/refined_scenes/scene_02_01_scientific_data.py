"""
Scene 2.1 — Bản chất dữ liệu khoa học: Mọi thứ đều là hàm số
Source: original_outline.tex, Section 2, Scene 2.1
Global time: 4:00 – 5:00
Duration: 60s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0201_ScientificDataAreFunctions(TimedScene):
    SCRIPT_ID = "2.1"
    SCRIPT_TITLE = "Bản chất dữ liệu khoa học"
    SCRIPT_START = 240.0
    SCRIPT_END = 300.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [4:00–4:30] Globe ERA5 + "Hàm → Hàm" ──
        globe = Circle(radius=1.5, color=SCIENCE, fill_opacity=0.1, stroke_width=2)
        globe_icon = Text("🌍", font_size=50).move_to(globe)

        # Data layers
        heat = Text("T(x)", font_size=20, color=WARNING).next_to(globe, UR, buff=0.3)
        wind = Text("v(x)", font_size=20, color=INPUT).next_to(globe, RIGHT, buff=0.5)
        pressure = Text("p(x)", font_size=20, color=OPERATOR).next_to(globe, DR, buff=0.3)

        globe_group = VGroup(globe, globe_icon, heat, wind, pressure).shift(LEFT * 3)

        # Today → Tomorrow
        today_label = Text("Hôm nay", font_size=20, color=MUTED).next_to(globe_group, DOWN, buff=0.4)
        arrow = Arrow(LEFT * 0.5, RIGHT * 2.5, color=NVIDIA_GREEN, stroke_width=3).shift(RIGHT * 0.5)
        tomorrow = Text("Ngày mai", font_size=20, color=MUTED).next_to(arrow, DOWN, buff=0.2)

        func_overlay = MathTex(
            r"\text{Hàm} \to \text{Hàm}",
            font_size=36, color=NVIDIA_GREEN
        ).shift(RIGHT * 4)

        self.play_timed("globe", 0, 3, FadeIn(globe_group), FadeIn(today_label))
        self.play_timed("arrow", 3, 5, FadeIn(arrow), FadeIn(tomorrow))
        self.play_timed("func_overlay", 5, 7, FadeIn(func_overlay))
        self.wait_timed("hold_weather", 7, 30)

        # ── Beat 2: [4:30–4:50] Seismology 3D + CFD geometry ──
        self.play_timed("clear_beat1", 30, 30.5,
                        *[FadeOut(m) for m in [globe_group, today_label, arrow, tomorrow, func_overlay]])

        # Seismology block
        seismo_rect = Rectangle(width=4, height=3, stroke_color=PURPLE, fill_color=PURPLE,
                                fill_opacity=0.15, stroke_width=2).shift(LEFT * 3.5)
        seismo_label = Text("Địa chấn: a(x) 3D", font_size=20, color=PURPLE).next_to(seismo_rect, DOWN, buff=0.2)
        wave_line = FunctionGraph(lambda x: 0.3 * np.sin(3 * x), x_range=[-1.5, 1.5],
                                  color=PURPLE, stroke_width=2).move_to(seismo_rect)

        # CFD geometry
        cfd_rect = Rectangle(width=4, height=3, stroke_color=INPUT, fill_color=INPUT,
                             fill_opacity=0.15, stroke_width=2).shift(RIGHT * 3.5)
        cfd_label = Text("Khí động: Navier-Stokes", font_size=20, color=INPUT).next_to(cfd_rect, DOWN, buff=0.2)
        airfoil = FunctionGraph(lambda x: 0.5 * np.sqrt(max(0, 1 - x ** 2)),
                                x_range=[-1.2, 1.2], color=INPUT, stroke_width=2).move_to(cfd_rect)

        self.play_timed("seismo", 30.5, 33,
                        FadeIn(seismo_rect), FadeIn(seismo_label), FadeIn(wave_line))
        self.play_timed("cfd", 33, 36,
                        FadeIn(cfd_rect), FadeIn(cfd_label), FadeIn(airfoil))
        self.wait_timed("hold_beat2", 36, 50)

        # ── Beat 3: [4:50–5:00] Molecular trajectory + summary ──
        self.play_timed("clear_beat2", 50, 50.5,
                        *[FadeOut(m) for m in [seismo_rect, seismo_label, wave_line,
                                               cfd_rect, cfd_label, airfoil]])

        summary = VGroup(
            Text("Input = Hàm", font_size=28, color=INPUT),
            Text("Output = Hàm", font_size=28, color=OUTPUT),
            Text("Ràng buộc vật lý liên tục", font_size=28, color=PHYSICS),
        ).arrange(DOWN, buff=0.5)

        self.play_timed("summary", 50.5, 53, FadeIn(summary))
        self.wait_timed("hold_end", 53, 59)

        self.play_timed("cut", 59, 60, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
