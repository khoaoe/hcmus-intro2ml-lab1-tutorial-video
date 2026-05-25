"""
Scene 3.4 - Scientific ML hypothesis
Script: ../docs/full_voice_manim_script.md
Global time: 21:35.0-23:20.0
Local duration: 105.0s

Neural operators learn a solution operator from many function pairs, then
reuse it across many scenarios and discretizations.
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import make_mesh_overlay, make_weather_sphere_icon, smooth_path
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    BG,
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
    WARNING,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()

PAIR_LABELS = (r"(a_1,u_1)", r"(a_2,u_2)", r"(a_N,u_N)")


def make_field_patch(width=1.18, height=0.78, rows=5, cols=8, seed=1, palette=None, accent=INPUT):
    rng = np.random.default_rng(seed)
    palette = palette or [accent, SCIENCE, OUTPUT, PURPLE]
    cells = VGroup()
    dx = width / cols
    dy = height / rows
    for row in range(rows):
        for col in range(cols):
            x = col / max(cols - 1, 1)
            y = row / max(rows - 1, 1)
            value = np.sin(2.2 * TAU * x + 0.45 * row) + 0.7 * np.cos(1.5 * TAU * y)
            value += rng.normal(0.0, 0.12)
            cell = Rectangle(
                width=dx,
                height=dy,
                stroke_width=0.16,
                stroke_color=BG,
                fill_color=palette[int(abs(value) * 2.3 + row + col) % len(palette)],
                fill_opacity=0.36 + 0.27 * (0.5 + 0.5 * np.sin(value)),
            )
            cell.move_to([-width / 2 + dx / 2 + col * dx, height / 2 - dy / 2 - row * dy, 0])
            cells.add(cell)
    frame = RoundedRectangle(
        width=width + 0.10,
        height=height + 0.10,
        corner_radius=0.06,
        stroke_color=accent,
        stroke_width=1.05,
        fill_color=CARD_BG,
        fill_opacity=0.36,
    )
    return VGroup(frame, cells)


def make_field_card(symbol, accent, seed, width=1.45, height=1.42, title=None):
    field = make_field_patch(seed=seed, accent=accent, palette=[accent, SCIENCE, OUTPUT, PURPLE])
    label = SafeMathTex(symbol, max_width=0.9, max_height=0.25, font_size=21, color=accent)
    title = title or ("input" if accent == INPUT else "output")
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.07,
        stroke_color=accent,
        stroke_width=1.05,
        fill_color=CARD_BG,
        fill_opacity=0.64,
    )
    title_mob = SafeText(title, max_width=width - 0.22, max_height=0.22, font_size=13, min_font_size=11, color=MUTED)
    title_mob.move_to(box.get_top() + DOWN * 0.18)
    body = VGroup(field, label).arrange(DOWN, buff=0.07)
    body.move_to(box.get_center() + DOWN * 0.10)
    return VGroup(box, title_mob, body)


def make_dataset_pair(index, pair_label, seed):
    input_card = make_field_card(r"a_%s(x)" % index, INPUT, seed)
    output_card = make_field_card(r"u_%s(x)" % index, OUTPUT, seed + 20)
    VGroup(input_card, output_card).arrange(RIGHT, buff=0.48)
    arrow = Arrow(input_card.get_right() + RIGHT * 0.06, output_card.get_left() + LEFT * 0.06, buff=0, color=MUTED, stroke_width=1.35)
    pair = VGroup(input_card, arrow, output_card)
    label = SafeMathTex(pair_label, max_width=1.55, max_height=0.26, font_size=22, color=TEXT)
    return VGroup(pair, label).arrange(DOWN, buff=0.12)


def make_sample_cloud(seed=5, n=18, width=1.5, height=0.85, color=INPUT):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        dots.add(Dot([rng.uniform(-width / 2, width / 2), rng.uniform(-height / 2, height / 2), 0], radius=0.027, color=color))
    frame = RoundedRectangle(width=width + 0.12, height=height + 0.12, corner_radius=0.06, stroke_color=color, stroke_width=1.0, fill_color=CARD_BG, fill_opacity=0.42)
    return VGroup(frame, dots)


def make_curved_domain_icon(radius=0.55):
    sphere = make_weather_sphere_icon(radius=radius)
    sphere[-1].scale(0.72)
    return sphere


def make_domain_card(title, icon, color, width=2.65, height=1.78):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.1,
        fill_color=CARD_BG,
        fill_opacity=0.66,
    )
    title_mob = SafeText(title, max_width=width - 0.22, max_height=0.28, font_size=15, min_font_size=11, color=TEXT, weight="BOLD")
    title_mob.move_to(box.get_top() + DOWN * 0.22)
    icon.move_to(box.get_center() + DOWN * 0.18)
    return VGroup(box, title_mob, icon)


class TrainingPairs(VGroup):
    """Dataset of function pairs: (a_i, u_i)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title = SafeText("Scientific ML hypothesis", max_width=7.1, max_height=0.58, font_size=38, color=TEXT, weight="BOLD")
        pairs = VGroup(
            make_dataset_pair("1", r"(a_1,u_1)", 4),
            make_dataset_pair("2", r"(a_2,u_2)", 9),
            make_dataset_pair("N", r"(a_N,u_N)", 16),
        ).arrange(RIGHT, buff=0.35)
        caption = SafeText("many input-function / output-function pairs", max_width=5.7, max_height=0.35, font_size=22, color=MUTED)
        self.title = title
        self.pairs = pairs
        self.add(VGroup(title, pairs, caption).arrange(DOWN, buff=0.34))


class LearnedOperatorBlock(VGroup):
    """Central learned solution operator block."""

    def __init__(self, mode="train", **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(
            width=3.25,
            height=2.05,
            corner_radius=0.12,
            stroke_color=OPERATOR,
            stroke_width=1.7,
            fill_color="#1F1B2E",
            fill_opacity=0.78,
        )
        glow = box.copy().set_stroke(OPERATOR, width=7.0, opacity=0.18).set_fill(opacity=0)
        top_label = SafeText("Learn", max_width=1.35, max_height=0.32, font_size=22, color=TEXT, weight="BOLD")
        formula = SafeMathTex(r"\mathcal{G}_{\theta}", max_width=1.55, max_height=0.54, font_size=39, color=OPERATOR)
        subtitle = SafeText("solution operator" if mode == "train" else "trained operator", max_width=2.25, max_height=0.26, font_size=17, color=MUTED)
        content = VGroup(top_label, formula, subtitle).arrange(DOWN, buff=0.10)
        content.move_to(box)
        self.add(glow, box, content)


class FastInferenceFanout(VGroup):
    """New input through trained operator to predicted output."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        input_card = make_field_card(r"a_{\mathrm{new}}(x)", INPUT, 41, width=2.0, height=1.65)
        operator = LearnedOperatorBlock(mode="infer")
        output_card = make_field_card(r"u_{\mathrm{pred}}(x)", OUTPUT, 61, width=2.0, height=1.65)
        input_card.move_to(LEFT * 4.3)
        operator.move_to(ORIGIN)
        output_card.move_to(RIGHT * 4.3)
        arrows = VGroup(
            Arrow(input_card.get_right() + RIGHT * 0.16, operator.get_left() + LEFT * 0.08, buff=0, color=MUTED, stroke_width=2.0),
            Arrow(operator.get_right() + RIGHT * 0.08, output_card.get_left() + LEFT * 0.16, buff=0, color=OUTPUT, stroke_width=2.4),
        )
        slow = Chip("traditional solver: minutes / hours", max_width=3.95, height=0.44, stroke_color=WARNING, font_size=16)
        fast = Chip("trained operator: milliseconds / seconds", max_width=4.25, height=0.44, stroke_color=OUTPUT, font_size=16)
        speed = VGroup(slow, fast).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.72)
        self.input_card = input_card
        self.operator = operator
        self.output_card = output_card
        self.arrows = arrows
        self.speed = speed
        self.add(arrows, input_card, operator, output_card, speed)


class ScenarioBatch(VGroup):
    """Many scenarios reuse one trained operator."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        operator = LearnedOperatorBlock(mode="infer").scale(0.83)
        operator.move_to(ORIGIN)
        lane_specs = [
            ("uncertainty quantification", INPUT, UP * 2.15),
            ("design optimization", SCIENCE, UP * 0.72),
            ("ensemble forecasting", OUTPUT, DOWN * 0.72),
            ("inverse problems", PURPLE, DOWN * 2.15),
        ]
        lanes = VGroup()
        arrows = VGroup()
        for index, (label, color, offset) in enumerate(lane_specs):
            scenarios = VGroup(
                make_field_patch(width=0.62, height=0.42, rows=3, cols=4, seed=80 + index * 5 + j, accent=color)
                for j in range(3)
            ).arrange(RIGHT, buff=0.07)
            scenarios.move_to(LEFT * 5.45 + offset)
            tag = Chip(label, max_width=3.2, height=0.38, stroke_color=color, font_size=15)
            tag.move_to(RIGHT * 4.55 + offset)
            arrows.add(Arrow(scenarios.get_right() + RIGHT * 0.12, operator.get_left() + offset * 0.18, buff=0, color=MUTED, stroke_width=1.3))
            arrows.add(Arrow(operator.get_right() + offset * 0.18, tag.get_left() + LEFT * 0.12, buff=0, color=color, stroke_width=1.4))
            lanes.add(VGroup(scenarios, tag))
        title = SafeText("ScenarioBatch: same trained operator, many runs", max_width=6.2, max_height=0.40, font_size=25, color=TEXT, weight="BOLD")
        title.to_edge(UP, buff=0.52)
        self.operator = operator
        self.lanes = lanes
        self.add(arrows, lanes, operator, title)


class ShapeMismatchWarning(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stamp = RoundedRectangle(
            width=3.4,
            height=0.74,
            corner_radius=0.08,
            stroke_color=WARNING,
            stroke_width=2.2,
            fill_color="#3A1020",
            fill_opacity=0.26,
        )
        text = SafeText("ShapeMismatchWarning", max_width=3.05, max_height=0.38, font_size=20, color=WARNING, weight="BOLD")
        text.move_to(stamp)
        self.add(stamp, text)


class FixedGridTrap(VGroup):
    """Fixed tensor neural network rejecting function-data layouts."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nn_box = RoundedRectangle(width=3.2, height=2.15, corner_radius=0.10, stroke_color=WARNING, stroke_width=1.55, fill_color=CARD_BG, fill_opacity=0.78)
        nn_title = SafeText("fixed-grid NN", max_width=2.55, max_height=0.34, font_size=23, color=TEXT, weight="BOLD")
        in_shape = Chip("input shape: 64x64", max_width=2.35, height=0.38, stroke_color=INPUT, font_size=15)
        out_shape = Chip("output shape: 64x64", max_width=2.35, height=0.38, stroke_color=OUTPUT, font_size=15)
        content = VGroup(nn_title, in_shape, out_shape).arrange(DOWN, buff=0.16)
        content.move_to(nn_box)
        network = VGroup(nn_box, content).move_to(ORIGIN)

        sample_specs = [("128x128", INPUT), ("irregular mesh", SCIENCE), ("sparse sensors", PURPLE)]
        samples = VGroup()
        for index, (label, color) in enumerate(sample_specs):
            if label == "128x128":
                icon = make_field_patch(width=1.15, height=0.72, rows=6, cols=10, seed=33, accent=color)
            elif label == "irregular mesh":
                icon = make_sample_cloud(seed=37, n=20, color=color)
                mesh = VGroup(*[Line(icon[1][i].get_center(), icon[1][(i + 3) % len(icon[1])].get_center(), color=GRID, stroke_width=0.5, stroke_opacity=0.45) for i in range(0, len(icon[1]), 3)])
                icon.add(mesh)
            else:
                icon = make_sample_cloud(seed=44, n=12, color=color)
            tag = Chip(label, max_width=2.15, height=0.46, stroke_color=color, font_size=15)
            samples.add(VGroup(icon, tag).arrange(DOWN, buff=0.10))
        samples.arrange(DOWN, buff=0.24).move_to(LEFT * 4.8)

        warning = ShapeMismatchWarning()
        warning.move_to(RIGHT * 4.3)
        message = SafeText("fixed-grid NN is too narrow", max_width=5.0, max_height=0.46, font_size=31, color=WARNING, weight="BOLD")
        message.to_edge(DOWN, buff=0.62)
        arrows = VGroup(*[Arrow(sample.get_right() + RIGHT * 0.12, network.get_left() + LEFT * 0.10, buff=0, color=MUTED, stroke_width=1.3) for sample in samples])
        block = Line(network.get_right() + RIGHT * 0.12 + DOWN * 0.55, warning.get_left() + LEFT * 0.12 + DOWN * 0.05, color=WARNING, stroke_width=5.0, stroke_opacity=0.85)
        self.samples = samples
        self.network = network
        self.warning = warning
        self.add(arrows, block, samples, network, warning, message)


class MultiMeshWorld(VGroup):
    """Many discretizations feeding one neural operator design."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cards = VGroup()
        specs = [
            ("regular grid", INPUT, make_field_patch(width=1.3, height=0.82, rows=5, cols=7, seed=70, accent=INPUT)),
            ("irregular mesh", SCIENCE, make_deformation_icon()),
            ("sparse sensor layout", PURPLE, make_sample_cloud(seed=73, n=13, color=PURPLE)),
            ("different input/output meshes", OUTPUT, make_dual_mesh_icon()),
            ("curved / spherical domain", OPERATOR, make_curved_domain_icon(radius=0.45)),
        ]
        for title, color, icon in specs:
            cards.add(make_domain_card(title, icon, color))
        cards.arrange_in_grid(rows=2, cols=3, buff=0.25)
        cards.move_to(LEFT * 3.75 + UP * 0.10)

        operator = LearnedOperatorBlock(mode="infer").scale(0.92).move_to(RIGHT * 3.65 + UP * 0.72)
        inputs = VGroup(
            Chip("sample points + values", max_width=2.95, height=0.42, stroke_color=INPUT, font_size=16),
            Chip("query points", max_width=1.75, height=0.42, stroke_color=OUTPUT, font_size=16),
        ).arrange(DOWN, buff=0.16)
        inputs.next_to(operator, DOWN, buff=0.30)
        arrows = VGroup()
        for card in cards:
            arrows.add(Arrow(card.get_right() + RIGHT * 0.08, operator.get_left() + LEFT * 0.08, buff=0, color=MUTED, stroke_width=1.0, max_tip_length_to_length_ratio=0.10))
        final = SafeText("Model must live across discretizations.", max_width=6.6, max_height=0.52, font_size=33, color=OUTPUT, weight="BOLD")
        subtitle = SafeText("Not just bigger NN. Different design principle.", max_width=6.7, max_height=0.36, font_size=22, color=TEXT)
        final_stack = VGroup(final, subtitle).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.48)
        content = VGroup(arrows, cards, operator, inputs, final_stack)
        glow = RoundedRectangle(
            width=content.width + 0.62,
            height=content.height + 0.48,
            corner_radius=0.16,
            stroke_color=OUTPUT,
            stroke_width=1.4,
            stroke_opacity=0.28,
            fill_color=OUTPUT,
            fill_opacity=0.025,
        )
        glow.move_to(content)
        self.cards = cards
        self.operator = operator
        self.arrows = arrows
        self.inputs = inputs
        self.final_stack = final_stack
        self.glow = glow
        self.add(glow, content)


def make_deformation_icon():
    frame = RoundedRectangle(width=1.45, height=0.88, corner_radius=0.06, stroke_color=SCIENCE, stroke_width=1.0, fill_color=CARD_BG, fill_opacity=0.45)
    lines = VGroup()
    for x in np.linspace(-0.58, 0.58, 5):
        points = [[x + 0.08 * np.sin(5 * y), y, 0] for y in np.linspace(-0.34, 0.34, 12)]
        lines.add(smooth_path(points, color=SCIENCE, stroke_width=0.75, stroke_opacity=0.65))
    for y in np.linspace(-0.34, 0.34, 4):
        points = [[x, y + 0.06 * np.sin(5 * x), 0] for x in np.linspace(-0.58, 0.58, 12)]
        lines.add(smooth_path(points, color=SCIENCE, stroke_width=0.75, stroke_opacity=0.65))
    return VGroup(frame, lines)


def make_dual_mesh_icon():
    left = make_mesh_overlay(width=0.76, height=0.62, nx=4, ny=3, color=INPUT)
    right = make_mesh_overlay(width=0.76, height=0.62, nx=7, ny=5, color=OUTPUT)
    left_frame = RoundedRectangle(width=0.86, height=0.72, corner_radius=0.05, stroke_color=INPUT, stroke_width=0.9, fill_color=CARD_BG, fill_opacity=0.38)
    right_frame = RoundedRectangle(width=0.86, height=0.72, corner_radius=0.05, stroke_color=OUTPUT, stroke_width=0.9, fill_color=CARD_BG, fill_opacity=0.38)
    left_group = VGroup(left_frame, left)
    right_group = VGroup(right_frame, right)
    arrow = Arrow(LEFT * 0.20, RIGHT * 0.20, buff=0, color=MUTED, stroke_width=1.0, max_tip_length_to_length_ratio=0.22)
    return VGroup(left_group, arrow, right_group).arrange(RIGHT, buff=0.10)


class Scene0304ScientificMLHypothesis(TimedScene):
    SCRIPT_ID = "3.4"
    SCRIPT_TITLE = "Scientific ML hypothesis"
    SCRIPT_START = 21 * 60 + 35
    SCRIPT_END = 23 * 60 + 20
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    KEYFRAMES = (
        "KF01 0.0s title + TrainingPairs dataset",
        "KF02 12.5s TrainingPairs flow into LearnedOperatorBlock",
        "KF03 26.0s FastInferenceFanout centered on G_theta",
        "KF04 40.0s ScenarioBatch parallel reuse",
        "KF05 54.5s FixedGridTrap + ShapeMismatchWarning",
        "KF06 68.0s MultiMeshWorld bridge to discretization challenge",
    )

    def make_training_pairs(self):
        view = TrainingPairs().move_to(ORIGIN)
        assert_in_frame(view, margin=0.38, label="training_pairs")
        return view

    def make_operator_learning_view(self):
        dataset = TrainingPairs().scale(0.62).to_edge(LEFT, buff=0.55)
        operator = LearnedOperatorBlock().move_to(RIGHT * 1.2 + UP * 0.40)
        formula = SafeMathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}", max_width=4.35, max_height=0.62, font_size=35, color=OPERATOR)
        formula.next_to(operator, DOWN, buff=0.22)
        solve = PanelCard("solve one instance", body=SafeText("one a -> one u", max_width=2.25, max_height=0.30, font_size=18, color=MUTED), width=3.0, height=1.32, accent_color=MUTED, title_font_size=20)
        learn = PanelCard("learn the solution operator", body=SafeText("many pairs -> one map", max_width=2.75, max_height=0.30, font_size=18, color=TEXT), width=4.25, height=1.32, accent_color=OUTPUT, title_font_size=20)
        contrast = VGroup(solve, learn).arrange(RIGHT, buff=0.30).to_edge(DOWN, buff=0.58)
        arrow = Arrow(dataset.get_right() + RIGHT * 0.18, operator.get_left() + LEFT * 0.12, buff=0, color=OPERATOR, stroke_width=2.1)
        view = VGroup(arrow, dataset, operator, formula, contrast)
        assert_in_frame(view, margin=0.38, label="operator_learning_view")
        return view

    def make_fast_inference_view(self):
        view = FastInferenceFanout().move_to(ORIGIN)
        assert_in_frame(view, margin=0.40, label="fast_inference_view")
        return view

    def make_scenario_batch(self):
        view = ScenarioBatch().move_to(ORIGIN)
        assert_in_frame(view, margin=0.36, label="scenario_batch")
        return view

    def make_fixed_grid_trap(self):
        view = FixedGridTrap().move_to(ORIGIN)
        assert_in_frame(view, margin=0.38, label="fixed_grid_trap")
        return view

    def make_multi_mesh_world(self):
        view = MultiMeshWorld().move_to(ORIGIN)
        assert_in_frame(view, margin=0.34, label="multi_mesh_world")
        return view

    def construct(self):
        background = make_background_network(seed=34, n=74, dot_opacity=0.16, line_opacity=0.12)
        self.add(background)

        training_pairs = self.make_training_pairs()
        self.play_timed("title_and_dataset", 0.0, 7.0, FadeIn(training_pairs.title, shift=UP * 0.12), FadeIn(training_pairs.pairs, lag_ratio=0.08))
        self.play_timed("dataset_feels_like_many_pairs", 7.0, 12.5, FadeIn(training_pairs[0][2], shift=UP * 0.08), Indicate(training_pairs.pairs, color=SCIENCE, scale_factor=1.02))

        operator_view = self.make_operator_learning_view()
        self.play_timed("pairs_flow_to_operator", 12.5, 19.0, ReplacementTransform(training_pairs, operator_view[1]), FadeIn(operator_view[0]), FadeIn(operator_view[2], shift=LEFT * 0.12))
        self.play_timed("operator_map_and_contrast", 19.0, 25.0, FadeIn(operator_view[3], shift=UP * 0.08), FadeIn(operator_view[4], lag_ratio=0.08), Indicate(operator_view[2], color=OPERATOR, scale_factor=1.03))
        self.wait_timed("pause_hold_learned_operator", 25.0, 26.0)

        inference_view = self.make_fast_inference_view()
        self.play_timed("switch_to_inference", 26.0, 32.0, FadeOut(operator_view, shift=UP * 0.10), FadeIn(inference_view.input_card, shift=RIGHT * 0.10), FadeIn(inference_view.operator))
        self.play_timed("fast_output_appears", 32.0, 36.0, Create(inference_view.arrows), FadeIn(inference_view.output_card, shift=RIGHT * 0.18))
        self.play_timed("speed_contrast", 36.0, 40.0, FadeIn(inference_view.speed, lag_ratio=0.08), Indicate(inference_view.output_card, color=OUTPUT, scale_factor=1.02))

        scenario_batch = self.make_scenario_batch()
        self.play_timed("scenario_batch_enter", 40.0, 47.0, FadeOut(inference_view, shift=UP * 0.10), FadeIn(scenario_batch.operator), FadeIn(scenario_batch.lanes, lag_ratio=0.07))
        self.play_timed("scenario_batch_parallel_reuse", 47.0, 54.5, FadeIn(scenario_batch[3], shift=UP * 0.08), Indicate(scenario_batch.operator, color=OPERATOR, scale_factor=1.03))

        fixed_grid_trap = self.make_fixed_grid_trap()
        self.play_timed("fixed_grid_nn_appears", 54.5, 60.0, FadeOut(scenario_batch, shift=UP * 0.10), FadeIn(fixed_grid_trap.network), FadeIn(fixed_grid_trap.samples, lag_ratio=0.06))
        self.play_timed("shape_mismatch_warning", 60.0, 68.0, FadeIn(fixed_grid_trap.warning, shift=LEFT * 0.10), FadeIn(fixed_grid_trap[-1], shift=UP * 0.08), Indicate(fixed_grid_trap.network, color=WARNING, scale_factor=1.02))

        multi_mesh_world = self.make_multi_mesh_world()
        self.play_timed("multi_mesh_world_build", 68.0, 80.0, FadeOut(fixed_grid_trap, shift=UP * 0.10), FadeIn(multi_mesh_world.cards, lag_ratio=0.06))
        self.play_timed("operator_accepts_discretizations", 80.0, 92.0, FadeIn(multi_mesh_world.operator, shift=LEFT * 0.12), Create(multi_mesh_world.arrows), FadeIn(multi_mesh_world.inputs, lag_ratio=0.08))
        self.play_timed("final_discretization_bridge", 92.0, 104.0, FadeIn(multi_mesh_world.glow), FadeIn(multi_mesh_world.final_stack, shift=UP * 0.08), multi_mesh_world.glow.animate.set_stroke(opacity=0.56))
        self.play_timed("ambient_hold", 104.0, 105.0, multi_mesh_world.glow.animate.set_fill(opacity=0.055).set_stroke(opacity=0.32))
        self.pad_to(self.SCENE_DURATION)
