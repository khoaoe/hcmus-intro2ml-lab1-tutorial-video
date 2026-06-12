
from manim import *
import numpy as np
from PIL import Image
import os

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0101_HookFiniteDimensionalLimit(TimedScene):
    SCRIPT_ID = "1.1"
    SCRIPT_TITLE = "Hook — Giới hạn của DL hữu hạn chiều"
    SCRIPT_START = 0.0
    SCRIPT_END = 45.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def make_neural_network_graph(self):
        layer_sizes = [4, 5, 3]
        layers = VGroup()
        for layer_index, size in enumerate(layer_sizes):
            nodes = VGroup(
                *[
                    Circle(
                        radius=0.105,
                        stroke_color=[INPUT, OPERATOR, OUTPUT][layer_index],
                        stroke_width=1.3,
                        fill_color=CARD_BG,
                        fill_opacity=0.85,
                    )
                    for _ in range(size)
                ]
            )
            nodes.arrange(DOWN, buff=0.18)
            layers.add(nodes)
        layers.arrange(RIGHT, buff=0.55)

        edges = VGroup()
        for left_layer, right_layer in zip(layers[:-1], layers[1:]):
            for left_node in left_layer:
                for right_node in right_layer:
                    edges.add(
                        Line(
                            left_node.get_center(),
                            right_node.get_center(),
                            color=GRID,
                            stroke_width=0.65,
                            stroke_opacity=0.64,
                        )
                    )
        nodes = VGroup(*layers)
        return VGroup(edges, nodes)

    def make_vector_stack(self):
        entries = VGroup(
            MathTex(r"x_1", color=TEXT, font_size=26),
            MathTex(r"x_2", color=TEXT, font_size=26),
            MathTex(r"\vdots", color=MUTED, font_size=26),
            MathTex(r"x_n", color=TEXT, font_size=26),
        ).arrange(DOWN, buff=0.06)
        left = Line(UP * 0.82, DOWN * 0.82, color=MUTED, stroke_width=2)
        right = left.copy()
        left.next_to(entries, LEFT, buff=0.1)
        right.next_to(entries, RIGHT, buff=0.1)
        vector = VGroup(left, entries, right)

        label = Text("vector / tensor / sequence of numbers", font_size=22, color=TEXT)
        label.next_to(vector, DOWN, buff=0.18)
        tensor_sheets = VGroup()
        for i in range(3):
            sheet = RoundedRectangle(
                width=1.05,
                height=1.28,
                corner_radius=0.04,
                stroke_color=INPUT,
                stroke_width=1.0,
                fill_color="#0F243A",
                fill_opacity=0.22,
            )
            sheet.shift(RIGHT * (0.08 * i) + UP * (0.06 * i))
            tensor_sheets.add(sheet)
        tensor_sheets.move_to(vector)
        tensor_sheets.set_z_index(-1)
        return VGroup(tensor_sheets, vector, label)

    def make_output_block(self):
        chip_specs = [
            ("label", OUTPUT),
            ("embedding", PURPLE),
            ("vector", INPUT),
        ]
        chips = VGroup()
        for name, color in chip_specs:
            box = RoundedRectangle(
                width=1.35,
                height=0.38,
                corner_radius=0.06,
                stroke_color=color,
                stroke_width=1.2,
                fill_color=CARD_BG,
                fill_opacity=0.74,
            )
            font_size = 16 if name == "embedding" else 18
            text = Text(name, font_size=font_size, color=TEXT)
            text.move_to(box)
            chips.add(VGroup(box, text))
        chips.arrange(DOWN, buff=0.13)
        return chips

    def make_chip(self, name, color):
        box = RoundedRectangle(
            width=1.25,
            height=0.42,
            corner_radius=0.07,
            stroke_color=color,
            stroke_width=1.15,
            fill_color=CARD_BG,
            fill_opacity=0.82,
        )
        font_size = 16 if name == "Transformer" else 18
        text = Text(name, font_size=font_size, color=TEXT)
        text.move_to(box)
        return VGroup(box, text)

    def construct(self):
        cat_image_path = "/home/bui-anh-quan/hcmus-intro2ml-lab1-tutorial-video/cat_image.jpeg"
        cropped_path = "media/cropped_cat.jpg"
        
        img = Image.open(cat_image_path).convert("RGB")
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(cropped_path)
        
        grid_size = 64
        img_resized = img_cropped.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
        cat_pixels = np.array(img_resized) / 255.0

        square_size = 4.0 / grid_size
        squares = VGroup()
        cat_colors = []
        random_colors = []
        
        offset = grid_size * square_size / 2
        center_x = 0.0
        center_y = 0.0
        
        for i in range(grid_size):
            for j in range(grid_size):
                sq = Square(side_length=square_size, stroke_width=0)
                sq.move_to(np.array([j * square_size - offset + square_size/2 + center_x, 
                                     -i * square_size + offset - square_size/2 + center_y, 0]))
                squares.add(sq)
                
                rgb = cat_pixels[i, j]
                hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
                cat_colors.append(hex_color)
                
                colors = [INPUT, OUTPUT, OPERATOR, PURPLE, NVIDIA_GREEN, WARNING]
                random_colors.append(np.random.choice(colors))
        
        for sq, c in zip(squares, random_colors):
            sq.set_fill(c, opacity=1.0)
            
        grid_label = Text("64 × 64", font_size=20, color=MUTED).next_to(squares, DOWN, buff=0.3)
        self.play_timed("grid_fadein", 0, 2, FadeIn(squares), FadeIn(grid_label))
        
        squares_cat = squares.copy()
        for sq, c in zip(squares_cat, cat_colors):
            sq.set_fill(c, opacity=1.0)
            
        self.play_timed("morph_cat", 2, 4, Transform(squares, squares_cat))
        
        high_res_img = ImageMobject(cropped_path)
        high_res_img.width = 4.0
        high_res_img.move_to(np.array([center_x, center_y, 0]))
        
        img_label = Text("Ảnh Mèo", font_size=28, color=TEXT, weight=BOLD).next_to(high_res_img, UP, buff=0.3)
        
        self.play_timed("high_res", 4, 5, FadeIn(high_res_img), FadeIn(img_label))
        self.wait_timed("hold_img", 5, 12)

        vector_stack = self.make_vector_stack()
        vector_stack.move_to(LEFT * 4.5 + DOWN * 0.05)
        
        neural_network = self.make_neural_network_graph()
        neural_network.move_to(RIGHT * 0.2 + DOWN * 0.08)
        
        input_to_network = Arrow(
            vector_stack.get_right(),
            neural_network.get_left(),
            buff=0.18,
            color=OPERATOR,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.07,
        )
        
        output_block = self.make_output_block()
        output_block.move_to(RIGHT * 4.2 + DOWN * 0.06)
        
        network_to_output = Arrow(
            neural_network.get_right(),
            output_block.get_left(),
            buff=0.18,
            color=OPERATOR,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.07,
        )
        
        formula = MathTex(r"f:\mathbb{R}^n \to \mathbb{R}^m", color=TEXT, font_size=38)
        formula.next_to(neural_network, UP, buff=0.42)
        
        pipeline = VGroup(vector_stack, input_to_network, neural_network, network_to_output, output_block, formula)

        chip_specs = [
            ("CNN", INPUT),
            ("ResNet", NVIDIA_GREEN),
            ("U-Net", OUTPUT),
            ("Transformer", PURPLE),
            ("ViT", OPERATOR),
        ]
        chips = VGroup(*[self.make_chip(name, color) for name, color in chip_specs])
        chips.arrange(RIGHT, buff=0.16)
        chips.next_to(pipeline, DOWN, buff=0.7)
        chips.set_x(0) # Center the chips horizontally

        self.play_timed("morph_to_tensor", 12, 14, 
                        FadeOut(high_res_img), FadeOut(img_label), FadeOut(grid_label),
                        Transform(squares, vector_stack[0])) # Transform the 4096 squares into the tensor sheets
        
        self.play_timed("tensor_show", 14, 15, FadeIn(vector_stack[1:])) 
        
        self.play_timed("network_show", 15, 17, 
                        FadeIn(input_to_network),
                        Create(neural_network),
                        GrowArrow(network_to_output),
                        FadeIn(output_block, shift=RIGHT * 0.16),
                        Write(formula))

        self.play_timed("arch_labels", 17, 19, 
                        LaggedStart(*[FadeIn(chip, shift=UP * 0.12) for chip in chips], lag_ratio=0.16))
                        
        self.wait_timed("hold_arch", 19, 28)

        self.play_timed("clear_beat2", 28, 28.8,
                        FadeOut(input_to_network), FadeOut(neural_network), 
                        FadeOut(network_to_output), FadeOut(output_block), 
                        FadeOut(formula), FadeOut(chips),
                        FadeOut(vector_stack[1:]))

        rn_frame = RoundedRectangle(
            width=10, height=5.5, corner_radius=0.2,
            stroke_color=INPUT, stroke_width=2, fill_opacity=0
        ).shift(UP * 0.2)

        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=np.array([np.random.uniform(-4.5, 4.5), np.random.uniform(-2.2, 2.6), 0]),
                radius=0.03, color=MUTED)
            for _ in range(len(squares))
        ])

        overlay_text = VGroup(
            Text("Finite-dimensional Euclidean Space", font_size=30, color=NVIDIA_GREEN, weight=BOLD),
            MathTex(r"\mathbb{R}^n", font_size=36, color=INPUT)
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)

        self.play_timed("rn_frame", 28.8, 30, FadeIn(rn_frame))
        
        self.play_timed("morph_to_dots", 30, 33, Transform(squares, dots))
                        
        self.play_timed("overlay", 33, 35, FadeIn(overlay_text))
        self.wait_timed("hold_end", 35, 44)

        self.play_timed("cut_to_black", 44, 45,
                        *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
