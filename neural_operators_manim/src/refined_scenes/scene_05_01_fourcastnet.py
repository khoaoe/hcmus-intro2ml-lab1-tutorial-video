from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0501_FourCastNet(TimedScene):
    SCRIPT_ID = "5.1"
    SCRIPT_TITLE = "FourCastNet & Spherical FNO"
    SCRIPT_START = 1045.0
    SCRIPT_END = 1150.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("FourCastNet: Dự báo thời tiết", font_size=28,
                     color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.4)

        globe_base = Circle(radius=2.2, color=WHITE, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.2)
        
        E05 = Ellipse(width=4.4, height=0.5)
        E15 = Ellipse(width=4.4, height=1.5)
        E25 = Ellipse(width=4.4, height=2.5)
        E35 = Ellipse(width=4.4, height=3.5)
        
        lat_lines = VGroup(E05, E15, E25, E35).set_color(WHITE).set_stroke(width=1, opacity=0.3)

        top_mask = Rectangle(width=5, height=5).move_to(UP * 2.5)
        bot_mask = Rectangle(width=5, height=5).move_to(DOWN * 2.5)

        def get_diff_regions(outer, inner):
            diff = Difference(outer, inner).set_stroke(width=0)
            top_part = Intersection(diff, top_mask).set_stroke(width=0)
            bot_part = Intersection(diff, bot_mask).set_stroke(width=0)
            return top_part, bot_part

        R5 = Ellipse(width=4.4, height=0.5).set_stroke(width=0)
        R4, R6 = get_diff_regions(E15, E05)
        R3, R7 = get_diff_regions(E25, E15)
        R2, R8 = get_diff_regions(E35, E25)
        R1, R9 = get_diff_regions(globe_base, E35)

        R1.set_fill(RED, opacity=0.6)
        R2.set_fill(ORANGE, opacity=0.6)
        R3.set_fill(YELLOW, opacity=0.6)
        nhiet_group = VGroup(R1, R2, R3)

        R4.set_fill(TEAL, opacity=0.6)
        R5.set_fill(BLUE, opacity=0.6)
        R6.set_fill(DARK_BLUE, opacity=0.6)
        gio_group = VGroup(R4, R5, R6)

        R7.set_fill(PURPLE, opacity=0.6)
        R8.set_fill(PINK, opacity=0.6)
        R9.set_fill(LIGHT_PINK, opacity=0.6)
        ap_suat_group = VGroup(R7, R8, R9)

        weather_bands = VGroup(nhiet_group, gio_group, ap_suat_group)

        globe_group = VGroup(globe_base, weather_bands, lat_lines)
        globe_group.shift(LEFT * 3.5)

        nhiet_label = Text("Nhiệt độ", font_size=16, color=RED).move_to(globe_base.get_right() + RIGHT * 0.7 + UP * 1.5)
        gio_label = Text("Gió", font_size=16, color=TEAL).move_to(globe_base.get_right() + RIGHT * 0.7)
        ap_suat_label = Text("Áp suất", font_size=16, color=PINK).move_to(globe_base.get_right() + RIGHT * 0.7 + DOWN * 1.5)
        feature_labels = VGroup(nhiet_label, gio_label, ap_suat_label)

        today_label = Text("Hôm nay", font_size=18, color=TEXT).next_to(globe_base, DOWN, buff=0.3)
        tomorrow_label = Text("Ngày mai", font_size=18, color=TEXT).shift(RIGHT * 3.5)
        tomorrow_label.set_y(today_label.get_y())
        
        time_arrow = Arrow(today_label.get_right() + RIGHT*0.2, tomorrow_label.get_left() + LEFT*0.2, 
                           color=NVIDIA_GREEN, stroke_width=3, buff=0.1)

        self.play_timed("title_globe", 0, 4, FadeIn(title), Create(globe_base), FadeIn(lat_lines))
        self.play_timed("weather_nhiet", 4, 6, FadeIn(nhiet_group), FadeIn(nhiet_label))
        self.play_timed("weather_gio", 6, 8, FadeIn(gio_group), FadeIn(gio_label))
        self.play_timed("weather_ap_suat", 8, 10, FadeIn(ap_suat_group), FadeIn(ap_suat_label))
        self.play_timed("time_arrow", 10, 15, FadeIn(today_label), GrowArrow(time_arrow), FadeIn(tomorrow_label))

        race_title = Text("Cuộc đua tốc độ", font_size=20, color=TEXT, weight=BOLD).shift(RIGHT * 3.5 + UP * 2)
        
        ifs_bar = Rectangle(width=0.1, height=0.4, color=RED, fill_opacity=0.8)
        ifs_bar.shift(RIGHT * 2 + UP * 0.5)
        ifs_label = Text("IFS (Truyền thống)", font_size=14, color=RED).next_to(ifs_bar, LEFT, buff=0.2)
        ifs_time = Text("1 Giờ", font_size=16, color=RED, weight=BOLD).next_to(ifs_bar, RIGHT, buff=0.2)
        
        fc_bar = Rectangle(width=0.1, height=0.4, color=NVIDIA_GREEN, fill_opacity=0.8)
        fc_bar.shift(RIGHT * 2 + DOWN * 0.5)
        fc_label = Text("FourCastNet", font_size=14, color=NVIDIA_GREEN).next_to(fc_bar, LEFT, buff=0.2)
        fc_time = Text("< 1 Giây", font_size=16, color=NVIDIA_GREEN, weight=BOLD).next_to(fc_bar, RIGHT, buff=0.2)

        self.play_timed("race_setup", 15, 20, 
                        FadeIn(race_title), FadeIn(ifs_label), FadeIn(fc_label),
                        FadeIn(ifs_bar), FadeIn(fc_bar))
        
        self.play_timed("race_ifs", 20, 25, 
                        ifs_bar.animate.stretch_to_fit_width(4.0, about_edge=LEFT),
                        FadeIn(ifs_time))
        
        self.play_timed("race_fc", 25, 27, 
                        fc_bar.animate.stretch_to_fit_width(4.0, about_edge=LEFT),
                        FadeIn(fc_time), Flash(fc_time, color=NVIDIA_GREEN))

        metrics = VGroup(
            Text("Nhanh hơn 45,000 lần", font_size=18, color=NVIDIA_GREEN, weight=BOLD),
            Text("Tiết kiệm năng lượng 25,000 lần", font_size=18, color=NVIDIA_GREEN),
            Text("Độ chính xác tương đương (ngắn/trung hạn)", font_size=16, color=MUTED)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 3.5 + DOWN * 1.8)
        
        self.play_timed("metrics", 27, 35, FadeIn(metrics))
        self.wait_timed("hold_beat1", 35, 40)

        self.play_timed("clear_beat1", 40, 41,
                        *[FadeOut(m) for m in [title, globe_group, feature_labels, today_label, time_arrow, 
                                               tomorrow_label, race_title, ifs_bar, ifs_label, ifs_time,
                                               fc_bar, fc_label, fc_time, metrics]])

        ens_title = Text("Hệ quả thực tế: Ensemble Forecasting", font_size=26,
                         color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.5)
        
        axes = Axes(
            x_range=[0, 10, 2], y_range=[15, 35, 5],
            x_length=10, y_length=4,
            axis_config={"color": GRID, "stroke_width": 1, "include_ticks": False},
        ).shift(DOWN * 0.5)
        
        x_label = Text("Thời gian (Ngày)", font_size=14, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Nhiệt độ", font_size=14, color=MUTED).next_to(axes.y_axis, UP, buff=0.2)

        det_line = axes.plot(lambda x: 25 + 3 * np.sin(x/2) + 0.5 * x, color=WHITE, stroke_width=3)
        det_label = Text("1 Dự báo duy nhất\n(Deterministic)", font_size=16, color=WHITE).next_to(det_line, UR, buff=0.2)

        self.play_timed("ens_title", 41, 43, FadeIn(ens_title))
        self.play_timed("axes_det", 43, 48, Create(axes), FadeIn(x_label), FadeIn(y_label), Create(det_line), FadeIn(det_label))

        np.random.seed(42)
        ens_paths = VGroup()
        for i in range(60):
            phase = np.random.uniform(0, TAU)
            amp = np.random.uniform(0.8, 1.5)
            noise = np.random.uniform(-0.5, 0.5)
            path = axes.plot(lambda x, p=phase, a=amp, n=noise: 25 + a * np.sin(x/2 + p) + 0.5 * x + n, 
                             color=YELLOW, stroke_width=1.5, stroke_opacity=0.15)
            ens_paths.add(path)

        ens_note = Text("Tương lai là ngẫu nhiên (Stochastic)", font_size=18, color=YELLOW).to_edge(DOWN, buff=0.5)

        self.play_timed("ensemble_cloud", 48, 55, 
                        FadeOut(det_label),
                        TransformFromCopy(VGroup(det_line), ens_paths),
                        FadeIn(ens_note))
        
        upper_bound = axes.plot(lambda x: 25 + 1.5 * np.sin(x/2) + 0.5 * x + 1.5, color=RED, stroke_width=2, stroke_opacity=0.5)
        lower_bound = axes.plot(lambda x: 25 + 0.8 * np.sin(x/2) + 0.5 * x - 1.0, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        
        prob_text = Text("70% khả năng 24-26°C | 20% rủi ro cực đoan", font_size=16, color=TEXT).to_edge(DOWN, buff=0.2)
        
        self.play_timed("prob_band", 55, 62, 
                        Create(upper_bound), Create(lower_bound),
                        FadeOut(ens_note), FadeIn(prob_text))
        
        self.wait_timed("hold_beat2", 62, 68)

        self.play_timed("clear_beat2", 68, 69,
                        *[FadeOut(m) for m in [ens_title, axes, x_label, y_label, det_line, 
                                               ens_paths, upper_bound, lower_bound, prob_text]])

        sfno_title = Text("Spherical FNO (SFNO)", font_size=26,
                          color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.5)

        planar_globe = Circle(radius=1.5, color=WHITE, stroke_width=1.5, fill_color=BLUE_E, fill_opacity=0.1)
        planar_globe.shift(LEFT * 3.5)
        
        planar_grid = VGroup()
        for i in range(5):
            line = Line(planar_globe.get_bottom(), planar_globe.get_top(), color=GRID, stroke_width=1)
            line.shift(LEFT * (i - 2) * 0.3)
            planar_grid.add(line)
        for i in range(4):
            line = Line(planar_globe.get_left(), planar_globe.get_right(), color=GRID, stroke_width=1)
            line.shift(UP * (i - 1.5) * 0.4)
            planar_grid.add(line)
            
        pole_glitch = Cross(color=RED, stroke_width=4).scale(0.3).move_to(planar_globe.get_top())
        planar_label = Text("FNO thường (Planar)", font_size=16, color=RED).next_to(planar_globe, DOWN, buff=0.3)
        planar_note = Text("Sai số kỳ dị tại hai cực", font_size=14, color=RED).next_to(planar_label, DOWN, buff=0.1)

        sfno_globe = Circle(radius=1.5, color=WHITE, stroke_width=1.5, fill_color=BLUE_E, fill_opacity=0.1)
        sfno_globe.shift(RIGHT * 3.5)
        
        storm_path = VMobject(color=YELLOW, stroke_width=2, stroke_opacity=0.8)
        c = sfno_globe.get_center()
        storm_path.set_points_smoothly([
            c + LEFT*1.2 + DOWN*0.2,
            c + LEFT*0.8 + UP*0.8,
            c + LEFT*0.1 + UP*1.4,   # Gần cực Bắc (bán kính 1.5)
            c + RIGHT*0.4 + UP*0.8,  # Vòng xuống
            c + LEFT*0.2 + UP*1.0,   # Vòng ngược lại (loop)
            c + RIGHT*0.5 + UP*1.4,  # Cắt qua cực một lần nữa
            c + RIGHT*1.0 + UP*0.5,
            c + RIGHT*1.2 + DOWN*0.5
        ])
        storm = Dot(radius=0.15, color=RED).move_to(storm_path.get_start())
        
        sfno_label = Text("Spherical FNO", font_size=16, color=NVIDIA_GREEN).next_to(sfno_globe, DOWN, buff=0.3)
        sfno_note = Text("Hàm điều hòa cầu (Harmonics)", font_size=14, color=NVIDIA_GREEN).next_to(sfno_label, DOWN, buff=0.1)

        self.play_timed("sfno_title", 69, 71, FadeIn(sfno_title))
        self.play_timed("planar_setup", 71, 75, 
                        Create(planar_globe), FadeIn(planar_grid), 
                        FadeIn(pole_glitch), FadeIn(planar_label), FadeIn(planar_note))
        
        self.play_timed("sfno_setup", 75, 77, 
                        Create(sfno_globe), FadeIn(sfno_label), FadeIn(sfno_note),
                        Create(storm_path), FadeIn(storm))

        no_eq = MathTex(r"\mathcal{G}_\theta(u) = \text{Fourier}^{-1}(R \cdot \text{Fourier}(u))", 
                        font_size=28, color=OPERATOR).shift(DOWN * 2.5)
        
        spectral_eq = MathTex(r"\frac{\partial u}{\partial t} = \sum_{l,m} \hat{u}_{l,m} Y_l^m(\theta, \phi)", 
                              font_size=28, color=SCIENCE).shift(DOWN * 2.5)
        
        lang_note = Text("Neural Operator nói cùng ngôn ngữ với Solver truyền thống", 
                         font_size=18, color=MUTED).next_to(spectral_eq, DOWN, buff=0.4)

        self.play_timed("sfno_action_and_eq", 77, 85,
                        MoveAlongPath(storm, storm_path, rate_func=linear),
                        Succession(
                            Wait(2),
                            FadeIn(no_eq, run_time=1),
                            TransformMatchingTex(no_eq, spectral_eq, run_time=3),
                            FadeIn(lang_note, run_time=1),
                            Wait(1)
                        ))

        self.wait_timed("hold_beat3", 85, 103)

        self.play_timed("cut", 103, 105, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
