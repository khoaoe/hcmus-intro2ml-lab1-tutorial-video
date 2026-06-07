"""
Scene 5.1 — FourCastNet & Spherical FNO: Dự báo thời tiết
Source: original_outline.tex, Section 5, Scene 5.1
Global time: 17:25 – 19:10
Duration: 105s
"""
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
        # ── Beat 1: [17:25–18:10] Globe, ERA5 layers & Speed race ──
        title = Text("FourCastNet: Dự báo thời tiết", font_size=28,
                     color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.4)

        # 1. Stylized 2D Globe
        globe = Circle(radius=2.2, color=WHITE, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.2)
        globe.shift(LEFT * 3.5)
        
        # Lat/Lon lines giả lập 3D
        lat_lines = VGroup(*[Ellipse(width=4.4, height=h, color=WHITE, stroke_width=1, stroke_opacity=0.3) 
                             for h in [0.5, 1.5, 2.5, 3.5]])
        lat_lines.move_to(globe.get_center())
        
        # Weather layers (Temperature/Wind bands)
        weather_bands = VGroup()
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        for i, color in enumerate(colors):
            band = Arc(radius=2.2, start_angle=PI/6 + i*0.2, angle=0.4, 
                       color=color, stroke_width=6, stroke_opacity=0.6)
            band.move_arc_center_to(globe.get_center())
            weather_bands.add(band)
            
        globe_group = VGroup(globe, lat_lines, weather_bands)

        # Time Arrow
        today_label = Text("Hôm nay", font_size=18, color=TEXT).next_to(globe, DOWN, buff=0.3)
        tomorrow_label = Text("Ngày mai", font_size=18, color=TEXT).shift(RIGHT * 3.5 + DOWN * 2.5)
        time_arrow = Arrow(globe.get_right() + RIGHT*0.2, tomorrow_label.get_left() + LEFT*0.2, 
                           color=NVIDIA_GREEN, stroke_width=3, buff=0.1)

        self.play_timed("title_globe", 0, 5, FadeIn(title), Create(globe), FadeIn(lat_lines))
        self.play_timed("weather_layers", 5, 10, *[Create(b) for b in weather_bands])
        self.play_timed("time_arrow", 10, 15, 
                        FadeIn(today_label), GrowArrow(time_arrow), FadeIn(tomorrow_label))

        # 2. Speed Race: IFS vs FourCastNet
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
        
        # Animate bars growing (IFS slow, FC instant)
        self.play_timed("race_ifs", 20, 25, 
                        ifs_bar.animate.stretch_to_fit_width(4.0, about_edge=LEFT),
                        FadeIn(ifs_time))
        
        self.play_timed("race_fc", 25, 27, 
                        fc_bar.animate.stretch_to_fit_width(4.0, about_edge=LEFT),
                        FadeIn(fc_time), Flash(fc_time, color=NVIDIA_GREEN))

        # Metrics overlay
        metrics = VGroup(
            Text("Nhanh hơn 45,000 lần", font_size=18, color=NVIDIA_GREEN, weight=BOLD),
            Text("Tiết kiệm năng lượng 25,000 lần", font_size=18, color=NVIDIA_GREEN),
            Text("Độ chính xác tương đương (ngắn/trung hạn)", font_size=16, color=MUTED)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 3.5 + DOWN * 1.8)
        
        self.play_timed("metrics", 27, 35, FadeIn(metrics))
        self.wait_timed("hold_beat1", 35, 40)

        # ── Beat 2: [18:10–18:40] Ensemble Forecasting ──
        self.play_timed("clear_beat1", 40, 41,
                        *[FadeOut(m) for m in [title, globe_group, today_label, time_arrow, 
                                               tomorrow_label, race_title, ifs_bar, ifs_label, ifs_time,
                                               fc_bar, fc_label, fc_time, metrics]])

        ens_title = Text("Hệ quả thực tế: Ensemble Forecasting", font_size=26,
                         color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.5)
        
        # Axes for time-series prediction (e.g., Temperature over 10 days)
        axes = Axes(
            x_range=[0, 10, 2], y_range=[15, 35, 5],
            x_length=10, y_length=4,
            axis_config={"color": GRID, "stroke_width": 1, "include_ticks": False},
        ).shift(DOWN * 0.5)
        
        x_label = Text("Thời gian (Ngày)", font_size=14, color=MUTED).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Nhiệt độ", font_size=14, color=MUTED).next_to(axes.y_axis, UP, buff=0.2)

        # Single deterministic line
        det_line = axes.plot(lambda x: 25 + 3 * np.sin(x/2) + 0.5 * x, color=WHITE, stroke_width=3)
        det_label = Text("1 Dự báo duy nhất\n(Deterministic)", font_size=16, color=WHITE).next_to(det_line, UR, buff=0.2)

        self.play_timed("ens_title", 41, 43, FadeIn(ens_title))
        self.play_timed("axes_det", 43, 48, Create(axes), FadeIn(x_label), FadeIn(y_label), Create(det_line), FadeIn(det_label))

        # Spaghetti plot (Ensemble cloud)
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
        
        # Highlight probability band
        # Upper and lower bounds
        upper_bound = axes.plot(lambda x: 25 + 1.5 * np.sin(x/2) + 0.5 * x + 1.5, color=RED, stroke_width=2, stroke_opacity=0.5)
        lower_bound = axes.plot(lambda x: 25 + 0.8 * np.sin(x/2) + 0.5 * x - 1.0, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        
        prob_text = Text("70% khả năng 24-26°C | 20% rủi ro cực đoan", font_size=16, color=TEXT).to_edge(DOWN, buff=0.2)
        
        self.play_timed("prob_band", 55, 62, 
                        Create(upper_bound), Create(lower_bound),
                        FadeOut(ens_note), FadeIn(prob_text))
        
        self.wait_timed("hold_beat2", 62, 68)

        # ── Beat 3: [18:40–19:10] Spherical FNO & Pole Singularity ──
        self.play_timed("clear_beat2", 68, 69,
                        *[FadeOut(m) for m in [ens_title, axes, x_label, y_label, det_line, 
                                               ens_paths, upper_bound, lower_bound, prob_text]])

        sfno_title = Text("Spherical FNO (SFNO)", font_size=26,
                          color=SCIENCE, weight=BOLD).to_edge(UP, buff=0.5)

        # So sánh FNO thường vs SFNO tại Bắc Cực
        # Left: Planar FNO (Grid chiếu lên cầu -> rách ở cực)
        planar_globe = Circle(radius=1.5, color=WHITE, stroke_width=1.5, fill_color=BLUE_E, fill_opacity=0.1)
        planar_globe.shift(LEFT * 3.5)
        
        # Grid lines hội tụ ở cực (gây singularity)
        planar_grid = VGroup()
        for i in range(5):
            line = Line(planar_globe.get_bottom(), planar_globe.get_top(), color=GRID, stroke_width=1)
            line.shift(LEFT * (i - 2) * 0.3)
            planar_grid.add(line)
        for i in range(4):
            line = Line(planar_globe.get_left(), planar_globe.get_right(), color=GRID, stroke_width=1)
            line.shift(UP * (i - 1.5) * 0.4)
            planar_grid.add(line)
            
        # Glitch effect at the pole
        pole_glitch = Cross(color=RED, stroke_width=4).scale(0.3).move_to(planar_globe.get_top())
        planar_label = Text("FNO thường (Planar)", font_size=16, color=RED).next_to(planar_globe, DOWN, buff=0.3)
        planar_note = Text("Sai số kỳ dị tại hai cực", font_size=14, color=RED).next_to(planar_label, DOWN, buff=0.1)

        # Right: SFNO (Smooth harmonic gradient)
        sfno_globe = Circle(radius=1.5, color=WHITE, stroke_width=1.5, fill_color=BLUE_E, fill_opacity=0.1)
        sfno_globe.shift(RIGHT * 3.5)
        
        # Bão di chuyển mượt mà qua cực
        storm = Dot(radius=0.2, color=RED).move_to(sfno_globe.get_top() + DOWN*0.5)
        storm_path = Arc(radius=1.0, start_angle=PI/2 + 0.5, angle=-1.0, color=YELLOW, stroke_width=2, stroke_opacity=0.5)
        storm_path.move_arc_center_to(sfno_globe.get_center())
        
        sfno_label = Text("Spherical FNO", font_size=16, color=NVIDIA_GREEN).next_to(sfno_globe, DOWN, buff=0.3)
        sfno_note = Text("Hàm điều hòa cầu (Harmonics)", font_size=14, color=NVIDIA_GREEN).next_to(sfno_label, DOWN, buff=0.1)

        self.play_timed("sfno_title", 69, 71, FadeIn(sfno_title))
        self.play_timed("planar_setup", 71, 75, 
                        Create(planar_globe), FadeIn(planar_grid), 
                        FadeIn(pole_glitch), FadeIn(planar_label), FadeIn(planar_note))
        
        self.play_timed("sfno_setup", 75, 79, 
                        Create(sfno_globe), FadeIn(sfno_label), FadeIn(sfno_note),
                        Create(storm_path), MoveAlongPath(storm, storm_path, rate_func=smooth))

        # "Nói cùng ngôn ngữ với Domain Experts"
        # Morph equation
        no_eq = MathTex(r"\mathcal{G}_\theta(u) = \text{Fourier}^{-1}(R \cdot \text{Fourier}(u))", 
                        font_size=28, color=OPERATOR).shift(DOWN * 2.5)
        
        spectral_eq = MathTex(r"\frac{\partial u}{\partial t} = \sum_{l,m} \hat{u}_{l,m} Y_l^m(\theta, \phi)", 
                              font_size=28, color=SCIENCE).shift(DOWN * 2.5)
        
        lang_note = Text("Neural Operator nói cùng ngôn ngữ với Solver truyền thống", 
                         font_size=18, color=MUTED).next_to(spectral_eq, DOWN, buff=0.4)

        self.play_timed("eq_morph", 79, 85, 
                        FadeIn(no_eq), 
                        TransformMatchingTex(no_eq, spectral_eq),
                        FadeIn(lang_note))

        self.wait_timed("hold_beat3", 85, 103)

        self.play_timed("cut", 103, 105, *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
