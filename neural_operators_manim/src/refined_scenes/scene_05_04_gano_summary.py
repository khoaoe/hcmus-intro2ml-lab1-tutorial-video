from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

class Scene0504_GANO_Summary(TimedScene):
    SCRIPT_ID = "5.4"
    SCRIPT_TITLE = "Mô hình sinh GANO & Tổng kết"
    SCRIPT_START = 1360.0
    SCRIPT_END = 1450.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Mô hình sinh GANO", font_size=36, color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("b1_title", 0, 2, Write(title))
        
        y_center = 0.5  # Cao hơn 1 chút để chừa chỗ cho text dưới
        
        gp_label = Text("Gaussian Process", font_size=18, color=INPUT).shift(LEFT*6.5 + UP*(y_center+1.2))
        gp_sublabel = Text("noise", font_size=18, color=INPUT).shift(LEFT*6.5 + UP*(y_center+0.9))
        gp_dot = Dot(radius=0.12, color=INPUT).shift(LEFT*6.5 + DOWN*(y_center-0.3))
        
        self.play_timed("b1_gp", 2, 5, FadeIn(gp_label), FadeIn(gp_sublabel), Create(gp_dot))
        
        gen_box = RoundedRectangle(width=2.0, height=1.2, corner_radius=0.12, 
                                   stroke_color=OUTPUT, fill_color=BLACK, fill_opacity=0.8, stroke_width=2.5)
        gen_box.shift(LEFT*3.8 + DOWN*y_center)
        gen_label = Text("Generator", font_size=20, color=OUTPUT).next_to(gen_box, UP, buff=0.25)
        gen_sublabel = Text("(Neural Operator)", font_size=14, color=OUTPUT).next_to(gen_label, UP, buff=0.1)
        
        arrow_gp_gen = Arrow(gp_dot.get_right(), gen_box.get_left(), buff=0.2, color=WHITE, stroke_width=2)
        
        self.play_timed("b1_gen", 5, 8, 
                        Create(gen_box), Write(gen_label), Write(gen_sublabel), 
                        Create(arrow_gp_gen))
        
        output_curves = VGroup()
        for i in range(3):
            curve = ParametricFunction(
                lambda t, idx=i: np.array([t, 0.25*np.sin(2*t + idx*1.2) + 0.15*np.cos(3*t - idx), 0]),
                t_range=[-1.0, 1.0],
                color=OUTPUT,
                stroke_width=2.5
            ).shift(LEFT*0.8 + DOWN*y_center + RIGHT*0.15*i)
            output_curves.add(curve)
        
        output_label = Text("Hàm output", font_size=18, color=OUTPUT).next_to(output_curves, DOWN, buff=0.3)
        arrow_gen_out = Arrow(gen_box.get_right(), output_curves.get_left(), buff=0.2, color=WHITE, stroke_width=2)
        
        self.play_timed("b1_out", 8, 12,
                        Create(output_curves), Write(output_label), Create(arrow_gen_out))
        
        distribution_cloud = VGroup()
        np.random.seed(42)
        for _ in range(60):  # Ít dots hơn
            point = Dot(radius=0.025, color=INPUT, fill_opacity=0.7)
            point.move_to(RIGHT*2.0 + DOWN*y_center + RIGHT*0.25*np.random.randn() + UP*0.25*np.random.randn())
            distribution_cloud.add(point)
        
        cloud_center = RIGHT*2.0 + DOWN*y_center
        confidence_band = VGroup(
            Line(cloud_center + UP*0.6 + LEFT*0.8, cloud_center + UP*0.6 + RIGHT*0.8, 
                 color=WARNING, stroke_width=2),
            Line(cloud_center + DOWN*0.6 + LEFT*0.8, cloud_center + DOWN*0.6 + RIGHT*0.8, 
                 color=WARNING, stroke_width=2),
            DashedLine(cloud_center + UP*0.6 + LEFT*0.8, cloud_center + DOWN*0.6 + LEFT*0.8, 
                       color=WARNING, stroke_width=1.5),
            DashedLine(cloud_center + UP*0.6 + RIGHT*0.8, cloud_center + DOWN*0.6 + RIGHT*0.8, 
                       color=WARNING, stroke_width=1.5)
        )
        
        dist_label = Text("Phân phối dự đoán", font_size=16, color=INPUT).next_to(confidence_band, UP, buff=0.35)
        conf_label = Text("Khoảng tin cậy", font_size=16, color=WARNING).next_to(confidence_band, DOWN, buff=0.2)
        
        arrow_out_dist = Arrow(output_curves.get_right(), confidence_band.get_left(), buff=0.2, color=WHITE, stroke_width=2)
        
        self.play_timed("b1_dist", 12, 17,
                        FadeIn(distribution_cloud), Create(confidence_band),
                        Write(dist_label), Write(conf_label), Create(arrow_out_dist))
        
        disc_box = RoundedRectangle(width=2.0, height=1.2, corner_radius=0.12, 
                                    stroke_color=PURPLE, fill_color=BLACK, fill_opacity=0.8, stroke_width=2.5)
        disc_box.shift(RIGHT*5 + DOWN*y_center)
        disc_label = Text("Discriminator", font_size=20, color=PURPLE).next_to(disc_box, UP, buff=0.25)
        
        scalar = Text("Scalar", font_size=18, color=PURPLE).next_to(disc_box, RIGHT, buff=0.6)
        arrow_dist_disc = Arrow(confidence_band.get_right(), disc_box.get_left(), buff=0.2, color=WHITE, stroke_width=2)
        arrow_disc_scalar = Arrow(disc_box.get_right(), scalar.get_left(), buff=0.2, color=WHITE, stroke_width=2)
        
        self.play_timed("b1_disc", 17, 21,
                        Create(disc_box), Write(disc_label),
                        Create(arrow_dist_disc), Create(arrow_disc_scalar), Write(scalar))
        
        vo_text1 = VGroup(
            Text("Khoa học thường cần phân phối output.", font_size=20),
            Text("GANO tổng quát hóa GAN lên không gian hàm.", font_size=20),
            Text("Hữu ích cho data augmentation & khám phá không gian thiết kế.", font_size=20)
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        
        self.play_timed("b1_vo", 21, 25, FadeIn(vo_text1))
        
        self.wait_timed("b1_hold", 25, 45)
        
        part1_group = VGroup(
            gp_label, gp_sublabel, gp_dot, gen_box, gen_label, gen_sublabel, 
            arrow_gp_gen, output_curves, output_label, arrow_gen_out, 
            distribution_cloud, confidence_band, dist_label, conf_label, arrow_out_dist,
            disc_box, disc_label, arrow_dist_disc, scalar, arrow_disc_scalar,
            vo_text1
        )
        
        self.play_timed("clear_p1", 45, 47, FadeOut(part1_group), FadeOut(title))
        
        summary_title = Text("Tổng kết ứng dụng", font_size=36, color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.5)
        self.play_timed("b2_title", 47, 49, FadeIn(summary_title))
        
        sun = Circle(radius=0.3, color=YELLOW, fill_color=YELLOW, fill_opacity=1)
        rays = VGroup(*[
            Line(ORIGIN, 0.45*UP).rotate(angle).set_color(YELLOW) 
            for angle in np.linspace(0, 2*PI, 8, endpoint=False)
        ])
        weather_icon = VGroup(sun, rays).scale(1.5)
        weather_label = Text("Dự báo thời tiết", font_size=20, color=INPUT).next_to(weather_icon, DOWN, buff=0.4)
        weather_group = VGroup(weather_icon, weather_label)
        
        leaf1 = ParametricFunction(lambda t: np.array([0.25*np.sin(t), 0.4*np.cos(t), 0]), 
                                    t_range=[0, PI], color=OUTPUT, fill_opacity=1)
        leaf2 = ParametricFunction(lambda t: np.array([-0.25*np.sin(t), 0.4*np.cos(t), 0]), 
                                    t_range=[0, PI], color=OUTPUT, fill_opacity=1)
        carbon_icon = VGroup(leaf1, leaf2).scale(1.8)
        carbon_label = Text("Carbon Capture", font_size=20, color=OUTPUT).next_to(carbon_icon, DOWN, buff=0.4)
        carbon_group = VGroup(carbon_icon, carbon_label)
        
        orbit1 = Ellipse(width=1.0, height=0.4, color=WARNING).rotate(PI/4)
        orbit2 = Ellipse(width=1.0, height=0.4, color=WARNING).rotate(-PI/4)
        nucleus = Dot(color=WARNING, radius=0.1)
        molecular_icon = VGroup(orbit1, orbit2, nucleus).scale(1.8)
        molecular_label = Text("Động lực học phân tử", font_size=20, color=WARNING).next_to(molecular_icon, DOWN, buff=0.4)
        molecular_group = VGroup(molecular_icon, molecular_label)
        
        apps_grid = VGroup(weather_group, carbon_group, molecular_group).arrange(RIGHT, buff=2.0).shift(UP*0.8)
        
        self.play_timed("b2_icons", 49, 54,
                        FadeIn(apps_grid[0], shift=UP),
                        FadeIn(apps_grid[1], shift=UP),
                        FadeIn(apps_grid[2], shift=UP))
                        
        vo_text2 = VGroup(
            Text("Neural Operators đang thay đổi:", font_size=22),
            Text("Dự báo thời tiết, tối ưu carbon capture, động lực học phân tử,", font_size=22),
            Text("và mô hình hóa bất định qua GANO.", font_size=22)
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.8)
        
        self.play_timed("b2_vo", 54, 58, FadeIn(vo_text2, shift=UP))
        
        self.wait_timed("b2_hold", 58, 65)
        
        self.play_timed("b2_fadeout", 65, 68, 
                        FadeOut(apps_grid), FadeOut(vo_text2), FadeOut(summary_title))
        
        next_section = Text("Section 6: Bài toán mở & Tương lai", font_size=40, color=PURPLE, weight=BOLD)
        self.play_timed("b2_next_section", 68, 71, FadeIn(next_section))
        
        self.wait_timed("b2_end", 71, 75)
        
        self.play_timed("cut", 75, 77, FadeOut(next_section))
        self.pad_to(self.SCENE_DURATION)
