"""
Scene 4.4 — U-shaped Neural Operator (U-NO): Đa tỷ lệ & Skip Connection
Source: original_outline.tex, Section 4, Scene 4.4
Global time: 14:30 – 15:45
Duration: 75s
"""

from manim import *

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0404_UNO(TimedScene):
    SCRIPT_ID = "4.4"
    SCRIPT_TITLE = "U-NO — Đa tỷ lệ & Skip Connection"
    SCRIPT_START = 870.0
    SCRIPT_END = 945.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [14:30–15:05] U-shape architecture ──
        title = Text("U-shaped Neural Operator (U-NO)", font_size=28,
                     color=INPUT, weight=BOLD).to_edge(UP, buff=0.4)

        # Build U-shape manually
        # Encoder side (descending)
        enc_blocks = VGroup()
        enc_labels = ["Full res", "½ res", "¼ res"]
        enc_widths = [2.5, 2.0, 1.5]
        enc_colors = [INPUT, INPUT, INPUT]

        for i, (label, w) in enumerate(zip(enc_labels, enc_widths)):
            box = RoundedRectangle(width=w, height=0.9, corner_radius=0.08,
                                   stroke_color=enc_colors[i], fill_color=CARD_BG, fill_opacity=0.6)
            text = Text(label, font_size=14, color=INPUT).move_to(box)
            block = VGroup(box, text)
            block.move_to(LEFT * 4 + DOWN * (i * 1.5 - 1.5))
            enc_blocks.add(block)

        # Latent space
        latent_box = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.08,
                                      stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.2)
        latent_text = Text("Latent", font_size=14, color=PURPLE).move_to(latent_box)
        latent = VGroup(latent_box, latent_text).move_to(DOWN * 2.5)

        # Decoder side (ascending)
        dec_blocks = VGroup()
        dec_labels = ["¼ res", "½ res", "Full res"]
        dec_widths = [1.5, 2.0, 2.5]

        for i, (label, w) in enumerate(zip(dec_labels, dec_widths)):
            box = RoundedRectangle(width=w, height=0.9, corner_radius=0.08,
                                   stroke_color=OUTPUT, fill_color=CARD_BG, fill_opacity=0.6)
            text = Text(label, font_size=14, color=OUTPUT).move_to(box)
            block = VGroup(box, text)
            block.move_to(RIGHT * 4 + DOWN * ((2 - i) * 1.5 - 1.5))
            dec_blocks.add(block)

        # Down arrows
        down_arrows = VGroup()
        for i in range(2):
            a = Arrow(enc_blocks[i].get_bottom(), enc_blocks[i + 1].get_top(),
                      color=GRID, buff=0.08, stroke_width=1.5)
            down_arrows.add(a)
        down_arrows.add(Arrow(enc_blocks[2].get_right(), latent.get_left(),
                              color=GRID, buff=0.1, stroke_width=1.5))

        up_arrows = VGroup()
        up_arrows.add(Arrow(latent.get_right(), dec_blocks[0].get_left(),
                            color=GRID, buff=0.1, stroke_width=1.5))
        for i in range(2):
            a = Arrow(dec_blocks[i].get_top(), dec_blocks[i + 1].get_bottom(),
                      color=GRID, buff=0.08, stroke_width=1.5)
            up_arrows.add(a)

        # Skip connections
        skip_arrows = VGroup()
        skip_colors = [NVIDIA_GREEN, NVIDIA_GREEN, NVIDIA_GREEN]
        for i in range(3):
            enc = enc_blocks[i]
            dec = dec_blocks[2 - i]
            skip = Arrow(enc.get_right(), dec.get_left(),
                         color=skip_colors[i], buff=0.1, stroke_width=2,
                         stroke_opacity=0.7, max_tip_length_to_length_ratio=0.1)
            skip_arrows.add(skip)

        skip_label = Text("Skip Connections", font_size=18,
                          color=NVIDIA_GREEN, weight=BOLD).next_to(title, DOWN, buff=0.3)

        self.play_timed("title", 0, 2, FadeIn(title))
        self.play_timed("encoder", 2, 6, FadeIn(enc_blocks), FadeIn(down_arrows))
        self.play_timed("latent", 6, 8, FadeIn(latent))
        self.play_timed("decoder", 8, 12, FadeIn(dec_blocks), FadeIn(up_arrows))
        self.play_timed("skip", 12, 16, FadeIn(skip_arrows), FadeIn(skip_label))

        # Blur vs sharp contrast note
        contrast_note = VGroup(
            Text("Encoder: nắm tương tác tầm xa", font_size=16, color=INPUT),
            Text("Latent: nén trạng thái tổng thể", font_size=16, color=PURPLE),
            Text("Decoder: tái tạo chi tiết sắc nét", font_size=16, color=OUTPUT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.3)

        self.play_timed("contrast", 16, 20, FadeIn(contrast_note))
        self.wait_timed("hold_u_shape", 20, 35)

        # ── Beat 2: [15:05–15:45] Skip connection formula + analogy ──
        self.play_timed("clear_beat1", 35, 35.5,
                        *[FadeOut(m) for m in [title, enc_blocks, down_arrows, latent,
                                               dec_blocks, up_arrows, skip_arrows,
                                               skip_label, contrast_note]])

        # ── Thêm Animation minh họa Blur vs Sharp (Shockwave) ──
        # 1. Vẽ hàm có đỉnh nhọn (Shock wave)
        sharp_func = VMobject(stroke_color=YELLOW, stroke_width=3)
        sharp_func.set_points_smoothly([
            LEFT*3, LEFT*1.5, LEFT*0.2 + UP*2, RIGHT*0.2 + UP*2, RIGHT*1.5, RIGHT*3
        ]).shift(DOWN * 1.0) # Tạo dạng hình thang / đỉnh nhọn
        
        # 2. Hàm bị làm mờ do tích phân (Low-pass filter)
        blurred_func = VMobject(stroke_color=RED, stroke_width=3, stroke_opacity=0.8)
        blurred_func.set_points_smoothly([
            LEFT*3, LEFT*1.5, LEFT*0.5 + UP*1.2, RIGHT*0.5 + UP*1.2, RIGHT*1.5, RIGHT*3
        ]).shift(DOWN * 1.0) # Đỉnh thấp xuống và thoải hơn

        shock_label = Text("Shock Wave / Boundary Layer", font_size=18, color=YELLOW).next_to(sharp_func, UP, buff=0.8)
        
        self.play_timed("show_shock", 35.5, 38, Create(sharp_func), Write(shock_label))
        
        # Hiệu ứng "Tích phân làm mờ"
        blur_label = Text("Tích phân → Mất chi tiết", font_size=16, color=RED).next_to(blurred_func, DOWN, buff=0.2)
        self.play_timed("blur_effect", 38, 41, 
                        TransformFromCopy(sharp_func, blurred_func), 
                        FadeIn(blur_label))
        
        # 3. Skip Connection phục hồi
        skip_arrow = Arrow(LEFT*2 + UP*2.2, RIGHT*2 + UP*2.2, color=NVIDIA_GREEN, stroke_width=4, buff=0)
        skip_arrow.shift(UP*0.5)
        skip_text = Text("Skip Connection", font_size=16, color=NVIDIA_GREEN).next_to(skip_arrow, UP)
        
        self.play_timed("skip_restore", 41, 45, 
                        GrowArrow(skip_arrow), Write(skip_text),
                        Transform(blurred_func, sharp_func), # Phục hồi lại hình dạng sắc nét
                        FadeOut(blur_label))
        
        self.wait_timed("hold_sharp", 45, 46)

        self.play_timed("clear_shock", 46, 47, 
                        FadeOut(sharp_func), FadeOut(shock_label), FadeOut(blurred_func), 
                        FadeOut(skip_arrow), FadeOut(skip_text))

        # Title
        skip_title = Text("Chìa khóa: Skip Connections", font_size=26,
                          color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.5)

        # Công thức - hiện từng thành phần
        skip_eq = MathTex(
            r"v_{dec} = \sigma(",
            r"T_{dec}\, u_{dec}",
            r" + ",
            r"u_{enc}",
            r")",
            font_size=34, color=TEXT
        ).shift(UP * 1.5)

        # Color code từng thành phần
        skip_eq[1].set_color(OPERATOR)  # T_dec u_dec - cam/đỏ
        skip_eq[3].set_color(NVIDIA_GREEN)  # u_enc - xanh lá

        self.play_timed("skip_title", 47, 48.5, FadeIn(skip_title))
        self.play_timed("eq_part1", 48.5, 50, Write(skip_eq[0]), Write(skip_eq[1]))  # σ(T_dec u_dec
        self.play_timed("eq_part2", 50, 51, Write(skip_eq[2]))  # +
        self.play_timed("eq_part3", 51, 52.5, Write(skip_eq[3]))  # u_enc
        self.play_timed("eq_part4", 52.5, 53.5, Write(skip_eq[4]))  # )

        # 3. Visual minh họa: 2 đường cong merge
        # Đường "Global" (mượt, từ T_dec)
        global_curve = VMobject(stroke_color=OPERATOR, stroke_width=2.5)
        global_curve.set_points_smoothly([
            LEFT*2.5 + DOWN*0.5, LEFT*1 + DOWN*0.3, LEFT*0.5 + UP*0.5, 
            RIGHT*0.5 + UP*0.5, RIGHT*1 + DOWN*0.3, RIGHT*2.5 + DOWN*0.5
        ]).shift(DOWN * 1.5)

        global_label = VGroup(
            MathTex(r"T_{dec}\, u_{dec}", font_size=20, color=OPERATOR),
            Text("(Global)", font_size=14, color=OPERATOR)
        ).arrange(DOWN, buff=0.1).next_to(global_curve, LEFT, buff=0.3)

        # Đường "Local" (có đỉnh nhọn, từ u_enc)
        local_curve = VMobject(stroke_color=NVIDIA_GREEN, stroke_width=2.5)
        local_curve.set_points_smoothly([
            LEFT*2.5 + DOWN*0.8, LEFT*1 + DOWN*0.8, LEFT*0.3 + DOWN*0.8,
            LEFT*0.1 + UP*1.5, RIGHT*0.1 + UP*1.5, RIGHT*0.3 + DOWN*0.8,
            RIGHT*1 + DOWN*0.8, RIGHT*2.5 + DOWN*0.8
        ]).shift(DOWN * 1.5)

        local_label = VGroup(
            MathTex(r"u_{enc}", font_size=20, color=NVIDIA_GREEN),
            Text("(Local)", font_size=14, color=NVIDIA_GREEN)
        ).arrange(DOWN, buff=0.1).next_to(local_curve, RIGHT, buff=0.3)

        self.play_timed("show_curves", 53.5, 56, 
                        Create(global_curve), FadeIn(global_label),
                        Create(local_curve), FadeIn(local_label))

        # 4. Merge animation: 2 đường cong hợp nhất
        merged_curve = VMobject(stroke_color=WHITE, stroke_width=3)
        merged_curve.set_points_smoothly([
            LEFT*2.5 + DOWN*0.3, LEFT*1 + DOWN*0.1, LEFT*0.3 + DOWN*0.2,
            LEFT*0.1 + UP*2, RIGHT*0.1 + UP*2, RIGHT*0.3 + DOWN*0.2,
            RIGHT*1 + DOWN*0.1, RIGHT*2.5 + DOWN*0.3
        ]).shift(DOWN * 1.5)

        merge_arrow = Arrow(DOWN * 2.5, DOWN * 1.8, color=WHITE, stroke_width=2)
        merge_label = MathTex(r"\text{Merge} \rightarrow v_{dec}", font_size=20, color=WHITE).next_to(merge_arrow, DOWN, buff=0.2)

        self.play_timed("merge", 56, 59,
                        Transform(global_curve, merged_curve),
                        Transform(local_curve, merged_curve.copy().set_stroke(width=1, opacity=0.5)),
                        GrowArrow(merge_arrow), Write(merge_label))

        self.wait_timed("hold_merge", 59, 61)

        # 5. Ẩn dụ bản đồ - VẼ THẬT, không phải icon xấu
        # Vẽ 2 lớp bản đồ chồng lên nhau
        # Layer 1: Đường cao tốc (nét to, mượt)
        highway = VMobject(stroke_color=OPERATOR, stroke_width=4)
        highway.set_points_smoothly([
            LEFT*3 + DOWN*1, LEFT*1 + DOWN*0.5, RIGHT*0.5 + DOWN*0.8, RIGHT*3 + DOWN*1.5
        ])

        # Layer 2: Đường nhỏ chi tiết (nét nhỏ, nhiều khúc cua)
        street = VMobject(stroke_color=NVIDIA_GREEN, stroke_width=1.5)
        street.set_points_smoothly([
            LEFT*2.5 + UP*0.5, LEFT*2 + UP*0.8, LEFT*1.5 + UP*0.6, LEFT*1 + UP*0.9,
            LEFT*0.5 + UP*0.7, LEFT*0 + UP*1, RIGHT*0.5 + UP*0.8, RIGHT*1 + UP*1.1,
            RIGHT*1.5 + UP*0.9, RIGHT*2 + UP*1.2, RIGHT*2.5 + UP*1
        ])

        map_title = Text("Ẩn dụ: Vẽ bản đồ", font_size=18, color=MUTED).to_edge(DOWN, buff=1.2)
        highway_label = Text("Cao tốc (Global)", font_size=14, color=OPERATOR).next_to(highway, UP, buff=0.2)
        street_label = Text("Đường nhỏ (Local)", font_size=14, color=NVIDIA_GREEN).next_to(street, DOWN, buff=0.2)

        self.play_timed("map_highway", 61, 63, 
                        *[FadeOut(m) for m in [skip_eq, global_label, local_label, global_curve, local_curve, merge_arrow, merge_label]],
                        Create(highway), FadeIn(highway_label), FadeIn(map_title))

        self.play_timed("map_street", 63, 65, Create(street), FadeIn(street_label))

        # Zoom effect: từ toàn cảnh → chi tiết
        zoom_box = Rectangle(width=1.5, height=1, color=WHITE, stroke_width=2).move_to(RIGHT * 1 + UP * 0.9)
        zoom_label = Text("Chi tiết", font_size=12, color=WHITE).next_to(zoom_box, UP, buff=0.1)

        self.play_timed("zoom", 65, 67, Create(zoom_box), FadeIn(zoom_label))

        self.wait_timed("hold_end", 67, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
