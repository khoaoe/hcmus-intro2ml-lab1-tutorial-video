from manim import *
import numpy as np

BG_COLOR = "#0b1020"
ACCENT_GREEN = "#76B900"

class SectionBumper(Scene):
    def __init__(self, sec_num="", title="", subtitle="", **kwargs):
        self.sec_num = sec_num
        self.title_text = title
        self.subtitle_text = subtitle
        super().__init__(**kwargs)

    def construct(self):
        self.camera.background_color = BG_COLOR
        
        num_bg = Text(self.sec_num, font_size=250, weight=BOLD, color=ACCENT_GREEN, fill_opacity=0.2)
        num_bg.shift(UP * 0.5)
        
        title_lines = [Text(t, font_size=52, weight=BOLD, color=WHITE) for t in self.title_text.split('\n')]
        title = VGroup(*title_lines).arrange(DOWN, buff=0.2)
        
        line = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT_GREEN, stroke_width=3)
        line.next_to(title, DOWN, buff=0.4)
        
        if "R^n" in self.subtitle_text:
            parts = self.subtitle_text.split("R^n")
            sub_part1 = Text(parts[0], font_size=24, color=GRAY_B)
            sub_math = MathTex(r"\mathbb{R}^n", font_size=32, color=GRAY_B).shift(UP*0.05)
            sub_part2 = Text(parts[1], font_size=24, color=GRAY_B)
            subtitle = VGroup(sub_part1, sub_math, sub_part2).arrange(RIGHT, buff=0.1)
        else:
            subtitle = Text(self.subtitle_text, font_size=24, color=GRAY_B)
            
        subtitle.next_to(line, DOWN, buff=0.4)
        
        content = VGroup(title, line, subtitle)
        content.move_to(ORIGIN) # Đảm bảo cụm này nằm chính giữa màn hình
        
        self.play(FadeIn(num_bg, scale=1.2), run_time=1.0)
        self.play(Write(title), run_time=1.2)
        
        self.play(Create(line), run_time=0.6)
        self.play(FadeIn(subtitle, shift=UP*0.2), run_time=0.8)
        
        self.wait(1.5)
        
        self.play(*[FadeOut(mob, shift=UP*0.5) for mob in [num_bg, title, line, subtitle]], run_time=1.0)
        self.wait(0.5) # Đệm thêm 0.5s đen tuyệt đối để editor nối clip

class Bumper_01(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="01",
            title="TỪ DEEP LEARNING\nĐẾN OPERATOR LEARNING",
            subtitle="Vì sao cần học trên không gian hàm?",
            **kwargs
        )

class Bumper_02(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="02",
            title="TỪ PIXEL ĐẾN HÀM LIÊN TỤC",
            subtitle="Những giới hạn của biểu diễn rời rạc",
            **kwargs
        )

class Bumper_03(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="03",
            title="NEURAL OPERATOR\nHOẠT ĐỘNG NHƯ THẾ NÀO?",
            subtitle="Kernel, tích phân và không gian hàm",
            **kwargs
        )

class Bumper_04(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="04",
            title="CÁC KIẾN TRÚC\nNEURAL OPERATOR PHỔ BIẾN",
            subtitle="FNO, GNO, UNO và các biến thể",
            **kwargs
        )

class Bumper_05(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="05",
            title="NEURAL OPERATOR\nTRONG THẾ GIỚI THỰC",
            subtitle="Thời tiết, vật lý và kỹ thuật",
            **kwargs
        )

class Bumper_06(SectionBumper):
    def __init__(self, **kwargs):
        super().__init__(
            sec_num="06",
            title="NHỮNG VẤN ĐỀ MỞ VÀ THÁCH THỨC",
            subtitle="Điều gì vẫn chưa được giải quyết?",
            **kwargs
        )
