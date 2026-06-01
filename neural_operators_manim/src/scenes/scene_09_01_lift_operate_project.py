"""
Scene 9.1 - Lift, operate, project
Script: ../docs/full_voice_manim_script.md
Global time: 58:50.0-1:01:00.0
Local duration: 130.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
    NVIDIA_GREEN,
    OPERATOR,
    OUTPUT,
    PURPLE,
    SCIENCE,
    TEXT,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_field_panel(label, color, width=2.55, height=0.58):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.3,
        fill_color=CARD_BG,
        fill_opacity=0.76,
    )
    wave = VMobject(color=color, stroke_width=2.1, stroke_opacity=0.86)
    xs = np.linspace(-width / 2 + 0.18, width / 2 - 0.18, 18)
    points = [[x, 0.10 * np.sin(4.0 * x), 0] for x in xs]
    wave.set_points_smoothly(points)
    caption = SafeText(label, max_width=width - 0.25, max_height=0.24, font_size=15, color=TEXT)
    caption.move_to(box.get_bottom() + UP * 0.14)
    wave.move_to(box.get_center() + UP * 0.08)
    return VGroup(box, wave, caption)


def make_channel_stack():
    """Weather channel stack: temperature, velocity, humidity, land mask."""
    labels = ("temperature", "velocity", "humidity", "land mask")
    colors = (INPUT, SCIENCE, NVIDIA_GREEN, PURPLE)
    panels = VGroup(*[make_field_panel(label, color) for label, color in zip(labels, colors)])
    panels.arrange(DOWN, buff=0.08)
    title = SafeMathTex(r"a(x)", max_width=1.2, max_height=0.45, font_size=34, color=INPUT)
    title.next_to(panels, UP, buff=0.16)
    group = VGroup(title, panels)
    group.move_to(LEFT * 5.65 + DOWN * 0.15)
    group.title = title
    group.panels = panels
    return group


def make_feature_field_stack():
    """Abstract hidden feature fields after pointwise lift."""
    colors = (PURPLE, OPERATOR, SCIENCE)
    fields = VGroup()
    for index, color in enumerate(colors):
        rect = RoundedRectangle(
            width=2.45,
            height=1.02,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.2,
            fill_color=color,
            fill_opacity=0.11,
        )
        dots = VGroup()
        for row in range(3):
            for col in range(6):
                dots.add(Dot(
                    rect.get_left() + RIGHT * (0.32 + 0.34 * col) + UP * (-0.28 + 0.28 * row),
                    radius=0.018,
                    color=color,
                    fill_opacity=0.75,
                ))
        field = VGroup(rect, dots).shift(UP * (0.10 * index) + RIGHT * (0.12 * index))
        fields.add(field)
    label = SafeText("hidden feature fields", max_width=2.55, max_height=0.25, font_size=18, color=PURPLE)
    label.next_to(fields, DOWN, buff=0.15)
    group = VGroup(fields, label)
    group.move_to(LEFT * 2.05 + DOWN * 0.20)
    group.fields = fields
    group.label = label
    return group


def make_operator_layer_stack():
    layers = VGroup()
    for i in range(3):
        layer = RoundedRectangle(
            width=1.12,
            height=2.75,
            corner_radius=0.08,
            stroke_color=OPERATOR,
            stroke_width=1.35,
            fill_color=CARD_BG,
            fill_opacity=0.78,
        )
        kernel = SafeMathTex(r"\int \kappa v", max_width=1.02, max_height=0.42, font_size=23, color=OPERATOR)
        residual = SafeText("residual", max_width=0.94, max_height=0.20, font_size=14, color=MUTED)
        nonlinearity = SafeText("sigma", max_width=0.86, max_height=0.20, font_size=14, color=OUTPUT)
        stack = VGroup(kernel, residual, nonlinearity).arrange(DOWN, buff=0.22).move_to(layer)
        layers.add(VGroup(layer, stack).shift(RIGHT * i * 1.28))
    layers.move_to(RIGHT * 1.45 + DOWN * 0.20)
    label = SafeText("function-to-function layers", max_width=3.9, max_height=0.28, font_size=20, color=OPERATOR)
    label.next_to(layers, DOWN, buff=0.18)
    group = VGroup(layers, label)
    group.layers = layers
    group.label = label
    return group


def make_output_field():
    axes = Axes(
        x_range=[0, 4, 1],
        y_range=[0, 2, 1],
        x_length=2.65,
        y_length=1.55,
        tips=False,
        axis_config={"color": GRID, "stroke_width": 1.0, "include_ticks": False},
    )
    curve = axes.plot(lambda x: 1 + 0.35 * np.sin(1.7 * x), x_range=[0, 4], color=OUTPUT, stroke_width=3)
    label = SafeMathTex(r"u(x)", max_width=1.0, max_height=0.38, font_size=32, color=OUTPUT)
    label.next_to(axes, UP, buff=0.12)
    group = VGroup(axes, curve, label).move_to(RIGHT * 5.75 + DOWN * 0.10)
    group.curve = curve
    group.label = label
    return group


def make_architecture_pipeline():
    channel_stack = make_channel_stack()
    feature_stack = make_feature_field_stack()
    operator_layers = make_operator_layer_stack()
    output_field = make_output_field()

    lift = Chip("lift  P", max_width=1.20, height=0.54, stroke_color=PURPLE, font_size=21)
    lift.move_to(LEFT * 3.75 + DOWN * 0.12)
    project = Chip("project  Q", max_width=1.55, height=0.54, stroke_color=OUTPUT, font_size=20)
    project.move_to(RIGHT * 3.85 + DOWN * 0.12)

    formula_lift = SafeMathTex(r"P(a(x))", max_width=1.45, max_height=0.42, font_size=29, color=PURPLE)
    formula_lift.next_to(lift, UP, buff=0.20)
    formula_project = SafeMathTex(r"Q(v(x))", max_width=1.45, max_height=0.42, font_size=29, color=OUTPUT)
    formula_project.next_to(project, UP, buff=0.20)

    anchors = (channel_stack, lift, feature_stack, operator_layers, project, output_field)
    arrows = VGroup()
    for left, right in zip(anchors, anchors[1:]):
        arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.18, color=GRID, stroke_width=2.4))

    phase_chips = VGroup(
        Chip("lift", max_width=0.84, height=0.44, stroke_color=PURPLE, font_size=15),
        Chip("operate", max_width=1.18, height=0.44, stroke_color=OPERATOR, font_size=15),
        Chip("project", max_width=1.18, height=0.44, stroke_color=OUTPUT, font_size=15),
    ).arrange(RIGHT, buff=0.50)
    phase_chips.move_to(UP * 3.15)

    interpretation = SafeText(
        "physical variables stay interpreted at function space level",
        max_width=8.2,
        max_height=0.36,
        font_size=23,
        color=TEXT,
    )
    interpretation.move_to(DOWN * 3.45)

    group = VGroup(
        channel_stack,
        lift,
        feature_stack,
        operator_layers,
        project,
        output_field,
        arrows,
        formula_lift,
        formula_project,
        phase_chips,
        interpretation,
    )
    group.channel_stack = channel_stack
    group.lift = lift
    group.feature_stack = feature_stack
    group.operator_layers = operator_layers
    group.project = project
    group.output_field = output_field
    group.arrows = arrows
    group.formula_lift = formula_lift
    group.formula_project = formula_project
    group.phase_chips = phase_chips
    group.interpretation = interpretation
    return group


class Scene0901LiftOperateProject(TimedScene):
    SCRIPT_ID = "9.1"
    SCRIPT_TITLE = "Lift, operate, project"
    SCRIPT_START = 58 * 60 + 50
    SCRIPT_END = 61 * 60
    SCENE_DURATION = 130.0

    KEYFRAMES = (
        "KF01 0.0s three-phase architecture",
        "KF02 13.0s physical channel stack",
        "KF03 26.0s pointwise lift",
        "KF04 39.0s operator layer stack",
        "KF05 53.0s projection to output variables",
        "KF06 66.0s familiar encoder-hidden-decoder comparison",
        "KF07 84.0s function-space interpretation",
        "KF08 130.0s final pipeline",
    )

    def construct(self):
        background = make_background_network(seed=901, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("9.1  Lift - operate - project", max_width=3.30, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        pipeline = make_architecture_pipeline()

        familiar_label = SafeText(
            "encoder -> hidden layers -> decoder",
            max_width=5.2,
            max_height=0.36,
            font_size=24,
            color=MUTED,
        ).move_to(UP * 2.45)

        function_layer_badge = Chip(
            "hidden layers are function-to-function layers",
            max_width=5.4,
            height=0.48,
            stroke_color=OPERATOR,
            font_size=18,
        )
        function_layer_badge.next_to(familiar_label, DOWN, buff=0.20)

        assert_in_frame(VGroup(section_label, pipeline), margin=0.30, label="scene_09_01_pipeline")

        self.add(background)

        # Global 58:50.0 -> local 0.0; Global 59:03.0 -> local 13.0
        self.play_timed(
            "show_three_phase_skeleton",
            0.0,
            13.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(pipeline.phase_chips, shift=DOWN * 0.04),
            FadeIn(VGroup(pipeline.lift, pipeline.operator_layers.layers, pipeline.project), shift=UP * 0.04),
        )

        # Global 59:03.0 -> local 13.0; Global 59:16.0 -> local 26.0
        self.play_timed(
            "reveal_physical_channels",
            13.0,
            26.0,
            FadeIn(pipeline.channel_stack, shift=RIGHT * 0.06),
            Create(pipeline.arrows[0]),
        )

        # Global 59:16.0 -> local 26.0; Global 59:29.0 -> local 39.0
        self.play_timed(
            "lift_to_hidden_feature_space",
            26.0,
            39.0,
            FadeIn(pipeline.formula_lift, shift=UP * 0.05),
            Create(pipeline.arrows[1]),
            FadeIn(pipeline.feature_stack, shift=RIGHT * 0.05),
            Circumscribe(pipeline.lift, color=PURPLE, buff=0.08),
        )

        # Global 59:29.0 -> local 39.0; Global 59:43.0 -> local 53.0
        self.play_timed(
            "operate_across_domain",
            39.0,
            53.0,
            Create(pipeline.arrows[2]),
            LaggedStart(*[FadeIn(layer, shift=UP * 0.04) for layer in pipeline.operator_layers.layers], lag_ratio=0.18),
            FadeIn(pipeline.operator_layers.label, shift=UP * 0.03),
        )

        # Global 59:43.0 -> local 53.0; Global 59:56.0 -> local 66.0
        self.play_timed(
            "project_to_output_variables",
            53.0,
            66.0,
            Create(pipeline.arrows[3]),
            FadeIn(pipeline.formula_project, shift=UP * 0.05),
            Create(pipeline.arrows[4]),
            FadeIn(pipeline.output_field, shift=LEFT * 0.05),
            Circumscribe(pipeline.project, color=OUTPUT, buff=0.08),
        )

        # Global 59:56.0 -> local 66.0; Global 1:00:14.0 -> local 84.0
        self.play_timed(
            "compare_with_encoder_hidden_decoder",
            66.0,
            84.0,
            FadeIn(familiar_label, shift=DOWN * 0.04),
            FadeIn(function_layer_badge, shift=DOWN * 0.04),
            Circumscribe(pipeline.operator_layers, color=OPERATOR, buff=0.10),
        )

        # Global 1:00:14.0 -> local 84.0; Global 1:01:00.0 -> local 130.0
        self.play_timed(
            "hold_function_space_interpretation",
            84.0,
            110.0,
            FadeIn(pipeline.interpretation, shift=UP * 0.05),
            pipeline.channel_stack.panels.animate.set_opacity(0.92),
            pipeline.output_field.curve.animate.set_stroke(width=4.2),
        )
        self.play_timed(
            "final_pipeline_read",
            110.0,
            129.8,
            Circumscribe(VGroup(pipeline.channel_stack, pipeline.feature_stack, pipeline.output_field), color=SCIENCE, buff=0.12),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
