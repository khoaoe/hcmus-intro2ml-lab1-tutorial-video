# src/s01_traditional_dl/scenes.py
from manim import *
import sys
import os

# Ensure utils can be imported when running from root
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.colors import *
from utils.math_helpers import create_discrete_vector

class TraditionalDL_Scene1_Intro(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # BEAT 1: Title & Data Types
        # ---------------------------------------------------------
        title = Tex("TRADITIONAL DEEP LEARNING", color=NVIDIA_GREEN).scale(1.2)
        title.to_edge(UP, buff=0.5)

        # SPEAKER: "Hello everyone, and welcome to this ICML tutorial. To understand the leap to Neural Operators, we must first ground ourselves in the conventional practice of traditional deep learning."
        self.play(Write(title))
        self.wait(7)

        subtitle = Tex("Text, speech, image, etc.", color=NVIDIA_GREEN).scale(0.8)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # SPEAKER: "Whether we are classifying an image, translating text, or processing speech..."
        self.play(FadeIn(subtitle, shift=UP*0.2))
        self.wait(4)

        # Visualizing Data
        img_grid = NumberPlane(x_range=[-1, 1, 0.5], y_range=[-1, 1, 0.5], 
                               background_line_style={"stroke_color": INPUT_BLUE, "stroke_width": 2}).scale(0.8)
        text_blocks = VGroup(*[Rectangle(width=0.4, height=0.2, fill_color=INPUT_BLUE, fill_opacity=0.8, stroke_width=0) for _ in range(5)])
        text_blocks.arrange(RIGHT, buff=0.1)
        wave = FunctionGraph(lambda x: 0.5 * np.sin(4 * x) * np.exp(-0.2 * x**2), x_range=[-3, 3], color=INPUT_BLUE)
        
        data_group = VGroup(img_grid, text_blocks, wave).arrange(RIGHT, buff=1.5).shift(UP*0.5)
        
        self.play(Create(img_grid), run_time=1.5)
        self.play(FadeIn(text_blocks, lag_ratio=0.2), run_time=1)
        self.play(Create(wave), run_time=1.5)
        self.wait(1)

        # ---------------------------------------------------------
        # BEAT 2: Finite Dimensional Objects
        # ---------------------------------------------------------
        finite_text = Tex("Data: Finite dimensional objects", color=TEXT_LIGHT)
        finite_text.to_edge(LEFT, buff=1).shift(UP*1.5)

        vector_1 = create_discrete_vector(6, color=INPUT_BLUE).move_to(img_grid)
        vector_2 = create_discrete_vector(5, color=INPUT_BLUE).move_to(text_blocks)
        vector_3 = create_discrete_vector(8, color=INPUT_BLUE).move_to(wave)

        # SPEAKER: "...traditional models treat all of these as finite-dimensional objects. We flatten a grid of pixels or a sequence of tokens into a fixed-length vector."
        self.play(Write(finite_text))
        self.play(
            ReplacementTransform(img_grid, vector_1),
            ReplacementTransform(text_blocks, vector_2),
            ReplacementTransform(wave, vector_3),
            run_time=2
        )
        self.wait(5)

        # ---------------------------------------------------------
        # BEAT 3: Architectures
        # ---------------------------------------------------------
        paradigm_text = Tex("Paradigm: Neural networks", color=TEXT_LIGHT).next_to(finite_text, DOWN, buff=0.8, aligned_edge=LEFT)
        arch_text = Tex("Architectures: CNN, AlexNet, LSTM, ResNet, Transformer...", color=TEXT_MUTED).scale(0.7)
        arch_text.next_to(paradigm_text, DOWN, buff=0.4, aligned_edge=LEFT)

        # SPEAKER: "The reigning paradigm to process this data is the standard neural network. We have built an incredible zoo of architectures: CNNs, LSTMs, ResNets, and Transformers."
        self.play(
            FadeOut(vector_1, vector_2, vector_3),
            Write(paradigm_text)
        )
        self.play(FadeIn(arch_text, shift=UP*0.2))
        self.wait(6)

        # Transition to next scene
        self.play(FadeOut(Group(*self.mobjects)))


class TraditionalDL_Scene2_Math(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # BEAT 4: The Mathematical Formulation
        # ---------------------------------------------------------
        title = Tex("TRADITIONAL DEEP LEARNING", color=NVIDIA_GREEN).scale(1.2).to_edge(UP, buff=0.5)
        self.add(title)

        practice_text = Tex("Conventional machine learning practice:", color=TEXT_LIGHT)
        practice_text.to_edge(LEFT, buff=1).shift(UP*1.5)
        
        math_eq = MathTex(
            "\\text{Learning a function between finite dimensional spaces, }",
            "f_\\theta", ":", "\\mathbb{R}^n", "\\rightarrow", "\\mathbb{R}^m"
        )
        math_eq.set_color_by_tex("f_\\theta", NVIDIA_GREEN)
        math_eq.set_color_by_tex("\\mathbb{R}^n", INPUT_BLUE)
        math_eq.set_color_by_tex("\\mathbb{R}^m", OUTPUT_ORANGE)
        math_eq.next_to(practice_text, DOWN, buff=0.5, aligned_edge=LEFT).shift(RIGHT)

        # SPEAKER: "But mathematically, every single one of these architectures is doing the exact same thing. They are learning a function between finite-dimensional spaces."
        self.play(Write(practice_text))
        self.play(Write(math_eq[0]))
        self.wait(2)
        
        # SPEAKER: "We learn a parameterized function f_theta that maps an input vector x in R^n to an output y in R^m."
        self.play(FadeIn(math_eq[1:], shift=LEFT*0.5))
        self.wait(4)

        # ---------------------------------------------------------
        # BEAT 5: The Mapping Diagram
        # ---------------------------------------------------------
        # Sets
        input_ellipse = Ellipse(width=3, height=4, color=TEXT_LIGHT).shift(DOWN*1.5 + LEFT*3)
        output_rect = RoundedRectangle(width=2.5, height=3.5, corner_radius=0.5, color=TEXT_LIGHT).shift(DOWN*1.5 + RIGHT*3)

        input_label = MathTex("x \\in \\mathbb{R}^n").next_to(input_ellipse, UP)
        input_label_title = Tex("Input vector").scale(0.8).next_to(input_label, UP, buff=0.1)
        
        output_label = MathTex("y \\in \\mathbb{R}^m").next_to(output_rect, UP)
        output_label_title = Tex("Output space").scale(0.8).next_to(output_label, UP, buff=0.1)

        # Points and Arrow
        x_dot = Dot(color=INPUT_BLUE).move_to(input_ellipse.get_center() + UP*0.5)
        y_dot = Dot(color=OUTPUT_ORANGE).move_to(output_rect.get_center() + DOWN*0.5)
        x_label = Tex("Image").scale(0.6).next_to(x_dot, LEFT)
        y_label = Tex("Label").scale(0.6).next_to(y_dot, RIGHT)

        arrow = CurvedArrow(x_dot.get_right(), y_dot.get_left(), angle=-TAU/6, color=NVIDIA_GREEN)
        f_label = MathTex("f").next_to(arrow, UP)

        # SPEAKER: "We take an input vector x in R^n—perhaps representing an image—and pass it through our function f to predict an output y in R^m, like a class label."
        self.play(
            Create(input_ellipse), Write(input_label), Write(input_label_title),
            Create(output_rect), Write(output_label), Write(output_label_title),
            run_time=2
        )
        self.play(FadeIn(x_dot, x_label))
        self.play(Create(arrow), Write(f_label))
        self.play(FadeIn(y_dot, y_label))
        self.wait(5)

        # ---------------------------------------------------------
        # BEAT 6: The Setup and The Limitation
        # ---------------------------------------------------------
        setup_group = VGroup(
            Tex("Datasets: UCI, MNITS, ImageNet...", color=TEXT_MUTED).scale(0.7),
            Tex("Loss: RMSE, L1, CLIP...", color=TEXT_MUTED).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=1)

        finite_box = SurroundingRectangle(Text("Finite dimension").scale(0.7), color=BOX_RED, buff=0.2)
        finite_box_text = Tex("Finite dimension", color=TEXT_LIGHT).scale(0.7).move_to(finite_box.get_center())
        finite_group = VGroup(finite_box, finite_box_text).next_to(input_ellipse, DOWN, buff=0.3)

        # SPEAKER: "We fuel this setup with static datasets, specific supervisions, and predefined metrics."
        self.play(FadeIn(setup_group, lag_ratio=0.3))
        self.wait(3)

        # SPEAKER: "But the defining characteristic—and the primary limitation we will transcend today—is that this entire framework is locked into a fixed, finite dimension."
        self.play(
            Create(finite_box),
            Write(finite_box_text)
        )
        self.play(Wiggle(finite_box, scale_value=1.1, rotation_angle=0.02), run_time=1.5)
        self.wait(5)

        self.play(FadeOut(Group(*self.mobjects)))