"""
Scene 4.2 — Tính chất FNO & Giới hạn
Source: original_outline.tex, Section 4, Scene 4.2
Global time: 12:30 – 13:15
Duration: 45s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *
from src.common.safe_text import SafeText, SafeMathTex

apply_global_config()

class Scene0402_FNO_Properties_Enhanced(TimedScene):
    SCRIPT_ID = "4.2"
    SCRIPT_TITLE = "Tính chất FNO & Giới hạn"
    SCRIPT_START = 750.0
    SCRIPT_END = 795.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # BEAT 1: FNO Properties & Limitations
        # ═══════════════════════════════════════════════════════════════
        
        # --- Title ---
        title = SafeText("Tính chất FNO & Giới hạn", max_width=14.0, font_size=32, 
                    color=NVIDIA_GREEN, weight="BOLD").to_edge(UP, buff=0.4)
        
        # --- Property 1: Speed O(N log N) ---
        speed_card = RoundedRectangle(width=3.2, height=1.8, corner_radius=0.1,
                                      fill_color=BLUE_B, fill_opacity=0.4, stroke_color=BLUE)
        speed_icon = SafeMathTex(r"O(N \log N)", max_width=2.8, font_size=32, color=BLUE)
        speed_label = SafeText("Tốc độ xử lý lưới triệu điểm", max_width=3.0, font_size=16, color=BLUE)
        speed_content = VGroup(speed_icon, speed_label).arrange(DOWN, buff=0.2).move_to(speed_card)
        speed_card_group = VGroup(speed_card, speed_content)
        
        # --- Property 2: Global Connectivity ---
        global_card = RoundedRectangle(width=3.2, height=1.8, corner_radius=0.1,
                                      fill_color=GREEN_B, fill_opacity=0.4, stroke_color=GREEN)
        # Thay SVGMobject bằng VGroup tạo icon đơn giản
        global_icon = VGroup(
            Circle(radius=0.3, color=GREEN),
            Dot(color=GREEN)
        )
        global_label = SafeText("Tầm nhìn toàn cục", max_width=3.0, font_size=16, color=GREEN)
        global_content = VGroup(global_icon, global_label).arrange(DOWN, buff=0.2).move_to(global_card)
        global_card_group = VGroup(global_card, global_content)
        
        # --- Property 3: Zero-shot Super-resolution ---
        zero_card = RoundedRectangle(width=3.4, height=1.8, corner_radius=0.1,
                                    fill_color=RED_B, fill_opacity=0.4, stroke_color=RED)
        zero_icon = VGroup(
            SafeText("64x64", max_width=1.0, font_size=18, color=RED),
            Arrow(LEFT*0.5, RIGHT*0.5, color=RED, stroke_width=2),
            SafeText("256x256", max_width=1.2, font_size=18, color=RED)
        ).arrange(RIGHT, buff=0.2)
        zero_label = SafeText("Zero-shot super-resolution", max_width=3.2, font_size=16, color=RED)
        zero_content = VGroup(zero_icon, zero_label).arrange(DOWN, buff=0.2).move_to(zero_card)
        zero_card_group = VGroup(zero_card, zero_content)
        
        # --- Property Layout ---
        properties = VGroup(speed_card_group, global_card_group, zero_card_group).arrange(RIGHT, buff=0.4)
        properties.shift(UP * 1.6)
        
        # --- Animation Sequence ---
        self.play_timed("title", 0, 1.5, FadeIn(title))
        self.play_timed("prop1", 1.5, 3.0, FadeIn(speed_card_group))
        self.play_timed("prop2", 3.0, 4.5, FadeIn(global_card_group))
        self.play_timed("prop3", 4.5, 6.0, FadeIn(zero_card_group))
        
        # Property 2: Global Connectivity (tia sáng bao phủ)
        domain_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=3, y_length=3,
            axis_config={"color": GREY_B, "include_ticks": False}
        ).shift(DOWN*1.5 + RIGHT*3.5)
        
        point = Dot(domain_axes.c2p(2.5, 2.5), color=YELLOW, radius=0.1)
        rays = VGroup()
        for angle in np.linspace(0, 2*np.pi, 24):
            ray = Line(
                domain_axes.c2p(2.5, 2.5),
                domain_axes.c2p(2.5 + 2.5*np.cos(angle), 2.5 + 2.5*np.sin(angle)),
                color=YELLOW, stroke_width=1, stroke_opacity=0.5
            )
            rays.add(ray)
        
        self.play_timed("domain_rays_in", 7.0, 9.0,
            FadeIn(domain_axes),
            FadeIn(point),
            FadeIn(rays)
        )
        self.wait_timed("domain_rays_hold", 9.0, 11.0)
        self.play_timed("domain_rays_out", 11.0, 12.0, FadeOut(domain_axes), FadeOut(point), FadeOut(rays))
        
        # Property 3: Zero-shot super-resolution
        # Giảm số lượng ô vuông để tối ưu render, dùng 16x16 và 32x32 biểu trưng
        grid_64 = VGroup(*[
            Square(side_length=0.15, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.3)
            for _ in range(16*16)
        ]).arrange_in_grid(rows=16, cols=16, buff=0).shift(LEFT*3.5 + DOWN*1.5)
        
        grid_256 = VGroup(*[
            Square(side_length=0.075, stroke_color=RED, fill_color=RED, fill_opacity=0.3)
            for _ in range(32*32)
        ]).arrange_in_grid(rows=32, cols=32, buff=0).shift(RIGHT*3.5 + DOWN*1.5)
        
        # Zoom vào góc để thấy "Mất chi tiết sắc nét"
        zoom_area = Rectangle(width=0.6, height=0.6, color=YELLOW, stroke_width=2).move_to(grid_256.get_corner(UL) + RIGHT*0.3 + DOWN*0.3)
        zoom_label = Text("Mất chi tiết sắc nét", font_size=16, color=YELLOW).next_to(zoom_area, DOWN, buff=0.2)
        
        self.play_timed("grids_in", 12.0, 13.5,
            FadeIn(grid_64), FadeIn(grid_256)
        )
        self.play_timed("zoom_in", 13.5, 15.0,
            Create(zoom_area),
            FadeIn(zoom_label)
        )
        self.wait_timed("grids_hold", 15.0, 17.0)
        self.play_timed("grids_out", 17.0, 18.0, FadeOut(grid_64), FadeOut(grid_256), FadeOut(zoom_area), FadeOut(zoom_label))
        
        # Property 4: Gibbs phenomenon (Shock Wave)
        shock_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.5, 0.5],
            x_length=6,
            y_length=2.5,
            axis_config={"color": GREY_B, "include_ticks": False}
        ).shift(DOWN*1.2 + LEFT*2.5)
        
        # Shock wave (step function)
        shock_wave = shock_axes.plot(
            lambda x: 0.3 if x < 5 else 1.2,
            color=RED, stroke_width=3, use_smoothing=False
        )
        shock_label = Text("Shock wave (gián đoạn)", font_size=16, color=RED).next_to(shock_axes, DOWN, buff=0.2)
        
        # FNO output (Gibbs phenomenon)
        def gibbs_wave(x):
            return 0.3 + 0.9 * (1 + 0.2 * np.sin(10*x)) * (0.5 + 0.5 * np.tanh(20*(x-5)))
        
        gibbs_approx = shock_axes.plot(
            gibbs_wave,
            color=BLUE, stroke_width=2.5
        )
        gibbs_label = Text("FNO output: Gibbs phenomenon", font_size=16, color=BLUE).next_to(shock_axes, DOWN, buff=0.5)
        
        # Gibbs ringing artifacts
        ringing_area = Rectangle(width=1.2, height=0.8, color=YELLOW, stroke_width=2).move_to(shock_axes.c2p(5, 0.75))
        ringing_label = Text("Gợn sóng Gibbs", font_size=16, color=YELLOW).next_to(ringing_area, RIGHT, buff=0.2)
        
        self.play_timed("shock_in", 18.0, 19.5,
            Create(shock_axes),
            Create(shock_wave), FadeIn(shock_label)
        )
        self.play_timed("gibbs_in", 19.5, 21.0,
            Create(gibbs_approx), FadeIn(gibbs_label)
        )
        self.play_timed("ringing_in", 21.0, 22.0,
            Create(ringing_area), FadeIn(ringing_label)
        )
        
        # --- Warning: Grid Limitations ---
        # Icon cảnh báo đơn giản
        warning_icon = VGroup(
            Triangle(color=ORANGE, fill_opacity=0.2).scale(0.6),
            Text("!", color=ORANGE, font_size=31, weight=BOLD).move_to(DOWN*0.05)
        )
        warning_text = Text("Lưới đều/tuần hoàn\nGiới hạn với shock wave", font_size=18, color=ORANGE)
        warning_group = VGroup(warning_icon, warning_text).arrange(RIGHT, buff=0.2)
        warning_group.scale(1.4)
        warning_group.move_to(DOWN*1.2 + RIGHT*3.5)
        
        self.play_timed("warning_in", 22.0, 23.5, FadeIn(warning_group))
        
        self.wait_timed("hold_final", 23.5, 43.5)
        
        # --- Final Cleanup ---
        self.play_timed("cleanup", 43.5, 45.0,
            *[FadeOut(m) for m in self.mobjects]
        )
        
        self.pad_to(self.SCENE_DURATION)
