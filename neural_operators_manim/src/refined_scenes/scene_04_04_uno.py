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
            block.move_to(LEFT * 4 + DOWN * (i * 1.5 - 1))
            enc_blocks.add(block)

        # Latent space
        latent_box = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.08,
                                      stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.2)
        latent_text = Text("Latent", font_size=14, color=PURPLE).move_to(latent_box)
        latent = VGroup(latent_box, latent_text).move_to(DOWN * 2)

        # Decoder side (ascending)
        dec_blocks = VGroup()
        dec_labels = ["¼ res", "½ res", "Full res"]
        dec_widths = [1.5, 2.0, 2.5]

        for i, (label, w) in enumerate(zip(dec_labels, dec_widths)):
            box = RoundedRectangle(width=w, height=0.9, corner_radius=0.08,
                                   stroke_color=OUTPUT, fill_color=CARD_BG, fill_opacity=0.6)
            text = Text(label, font_size=14, color=OUTPUT).move_to(box)
            block = VGroup(box, text)
            block.move_to(RIGHT * 4 + DOWN * ((2 - i) * 1.5 - 1))
            dec_blocks.add(block)

        # Down arrows
        down_arrows = VGroup()
        for i in range(2):
            a = Arrow(enc_blocks[i].get_bottom(), enc_blocks[i + 1].get_top(),
                      color=GRID, buff=0.08, stroke_width=1.5)
            down_arrows.add(a)
        down_arrows.add(Arrow(enc_blocks[2].get_bottom(), latent.get_left(),
                              color=GRID, buff=0.08, stroke_width=1.5))

        # Up arrows
        up_arrows = VGroup()
        up_arrows.add(Arrow(latent.get_right(), dec_blocks[0].get_bottom(),
                            color=GRID, buff=0.08, stroke_width=1.5))
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
                          color=NVIDIA_GREEN, weight=BOLD).shift(UP * 3.2 + RIGHT * 2)

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

        skip_title = Text("Chìa khóa: Skip Connections", font_size=26,
                          color=NVIDIA_GREEN, weight=BOLD).to_edge(UP, buff=0.5)

        skip_eq = MathTex(
            r"v_{dec} = \sigma(T_{dec}\, u_{dec} + u_{enc})",
            font_size=34, color=TEXT
        ).shift(UP * 1)

        explanation = VGroup(
            Text("Tích phân → làm mịn dữ liệu", font_size=20, color=OPERATOR),
            Text("Skip → bơm chi tiết hình học từ encoder", font_size=20, color=NVIDIA_GREEN),
            Text("Kết quả: vật lý toàn cục + chi tiết cục bộ", font_size=20, color=OUTPUT),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 0.8)

        # Map analogy
        analogy = VGroup(
            Text("🗺️ Giống vẽ bản đồ:", font_size=20, color=MUTED),
            Text("Toàn cảnh cho cao tốc + Chi tiết cho tên đường nhỏ",
                 font_size=18, color=MUTED),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)

        self.play_timed("skip_title", 35.5, 37, FadeIn(skip_title))
        self.play_timed("skip_eq", 37, 40, FadeIn(skip_eq))
        self.play_timed("explanation", 40, 48, FadeIn(explanation))
        self.play_timed("analogy", 48, 52, FadeIn(analogy))
        self.wait_timed("hold_end", 52, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
