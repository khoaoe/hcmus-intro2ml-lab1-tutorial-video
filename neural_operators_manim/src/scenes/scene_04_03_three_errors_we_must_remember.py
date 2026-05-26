"""
Scene 4.3 - The three errors we must remember
Script: ../docs/full_voice_manim_script.md
Global time: 27:05.0-29:10.0
Local duration: 125.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import make_mesh_overlay, smooth_path
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import (
    apply_global_config,
    CARD_BG,
    GRID,
    INPUT,
    MUTED,
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


def _true_function(x):
    return 0.42 * np.sin(2.0 * TAU * x + 0.25) + 0.18 * np.sin(9.0 * TAU * x - 0.30)


def _smooth_reconstruction(x):
    return 0.38 * np.sin(2.0 * TAU * x + 0.25)


def _curve_points(fn, width=4.9, height=1.62, n=180):
    xs = np.linspace(0.0, 1.0, n)
    return [[-width / 2 + width * x, height * fn(x), 0] for x in xs]


def _sample_points(count=8, width=4.9, height=1.62):
    xs = np.linspace(0.0, 1.0, count)
    return [[-width / 2 + width * x, height * _true_function(x), 0] for x in xs]


def make_error_card(title, subtitle="", color=INPUT, width=4.55, height=1.85):
    body = VGroup()
    if subtitle:
        body.add(SafeText(subtitle, max_width=width - 0.65, max_height=0.40, font_size=18, color=MUTED))
    else:
        body.add(SafeText("familiar ML error", max_width=width - 0.65, max_height=0.32, font_size=17, color=MUTED))
    return PanelCard(title, body=body, width=width, height=height, accent_color=color, title_font_size=24)


def make_error_triangle(highlight_discretization=False):
    vertices = {
        "approximation error": np.array([-3.35, -1.38, 0.0]),
        "generalization error": np.array([3.35, -1.38, 0.0]),
        "discretization error": np.array([0.0, 2.15, 0.0]),
    }
    colors = {
        "approximation error": INPUT,
        "generalization error": OUTPUT,
        "discretization error": WARNING,
    }
    subtitles = {
        "approximation error": "model class",
        "generalization error": "data pattern",
        "discretization error": "mesh / samples",
    }
    edges = VGroup(
        Line(vertices["approximation error"], vertices["generalization error"], color=GRID, stroke_width=2.0),
        Line(vertices["generalization error"], vertices["discretization error"], color=GRID, stroke_width=2.0),
        Line(vertices["discretization error"], vertices["approximation error"], color=GRID, stroke_width=2.0),
    )
    cards = VGroup()
    for label, position in vertices.items():
        card = make_error_card(label, subtitles[label], color=colors[label], width=3.65, height=1.18)
        card.move_to(position)
        if highlight_discretization and label == "discretization error":
            card.box.set_stroke(WARNING, width=3.4, opacity=1.0)
            card.box.set_fill("#2A1826", opacity=0.92)
        cards.add(card)
    title = SafeText("three-error view", max_width=5.0, max_height=0.45, font_size=32, color=TEXT, weight="BOLD")
    title.move_to(UP * 3.42)
    triangle = VGroup(edges, cards, title)
    triangle.vertices = cards
    triangle.discretization_card = cards[2]
    return triangle


def make_observation_icons():
    point_eval = VGroup(
        Dot(LEFT * 0.34, radius=0.055, color=OUTPUT),
        Dot(ORIGIN, radius=0.055, color=OUTPUT),
        Dot(RIGHT * 0.34, radius=0.055, color=OUTPUT),
        SafeText("point evaluation", max_width=2.25, max_height=0.28, font_size=16, color=TEXT),
    ).arrange(DOWN, buff=0.16)
    mesh = VGroup(
        make_mesh_overlay(width=1.20, height=0.62, nx=5, ny=3, color=INPUT),
        SafeText("mesh", max_width=1.1, max_height=0.26, font_size=16, color=TEXT),
    ).arrange(DOWN, buff=0.15)
    rng = np.random.default_rng(403)
    sensors = VGroup(*[Dot([rng.uniform(-0.50, 0.50), rng.uniform(-0.28, 0.28), 0], radius=0.032, color=WARNING) for _ in range(11)])
    sensor = VGroup(sensors, SafeText("sensor", max_width=1.2, max_height=0.26, font_size=16, color=TEXT)).arrange(DOWN, buff=0.15)
    snapshot = VGroup(
        Rectangle(width=1.05, height=0.66, stroke_color=PURPLE, stroke_width=1.0, fill_color="#20183A", fill_opacity=0.55),
        SafeText("snapshot", max_width=1.55, max_height=0.26, font_size=16, color=TEXT),
    ).arrange(DOWN, buff=0.15)
    return VGroup(point_eval, mesh, sensor, snapshot).arrange(RIGHT, buff=0.54)


def make_high_frequency_curve_panel():
    true_curve = smooth_path(_curve_points(_true_function), color=INPUT, stroke_width=3.0)
    low_curve = smooth_path(_curve_points(_smooth_reconstruction), color=OUTPUT, stroke_width=2.5).set_opacity(0.34)
    axis = Line(LEFT * 2.45 + DOWN * 0.90, RIGHT * 2.45 + DOWN * 0.90, color=GRID, stroke_width=1.0)
    label = SafeText("true continuum", max_width=2.4, max_height=0.32, font_size=18, color=INPUT, weight="BOLD")
    label.next_to(true_curve, UP, buff=0.10)
    chip = Chip("high-frequency detail", max_width=2.85, height=0.40, stroke_color=INPUT, font_size=16)
    chip.next_to(axis, DOWN, buff=0.12)
    body = VGroup(axis, low_curve, true_curve, label, chip)
    panel = PanelCard("function continuum", body=body, width=6.40, height=3.25, accent_color=INPUT, title_font_size=24)
    panel.true_curve = true_curve
    return panel


def make_coarse_sampling_panel():
    true_curve = smooth_path(_curve_points(_true_function), color=INPUT, stroke_width=2.8)
    wrong_curve = smooth_path(_curve_points(_smooth_reconstruction), color=WARNING, stroke_width=3.0)
    wrong_curve.set_opacity(0.92)
    dots = VGroup(*[Dot(point, radius=0.065, color=OUTPUT) for point in _sample_points(8)])
    axis = Line(LEFT * 2.45 + DOWN * 0.90, RIGHT * 2.45 + DOWN * 0.90, color=GRID, stroke_width=1.0)
    true_label = SafeText("true continuum", max_width=2.05, max_height=0.28, font_size=16, color=INPUT)
    true_label.move_to(LEFT * 1.55 + UP * 1.05)
    wrong_label = SafeText("wrong smooth reconstruction", max_width=3.25, max_height=0.30, font_size=15, color=WARNING)
    wrong_label.move_to(RIGHT * 1.28 + DOWN * 1.30)
    sample_label = Chip("coarse samples", max_width=2.35, height=0.40, stroke_color=OUTPUT, font_size=16)
    sample_label.move_to(LEFT * 1.40 + DOWN * 1.22)
    lost = Chip("information lost", max_width=2.55, height=0.44, stroke_color=WARNING, font_size=17)
    lost.move_to(RIGHT * 1.55 + UP * 1.05)
    body = VGroup(axis, true_curve, wrong_curve, dots, true_label, wrong_label, sample_label, lost)
    panel = PanelCard("coarse sampling loses detail", body=body, width=7.35, height=3.90, accent_color=WARNING, title_font_size=24)
    panel.dots = dots
    panel.true_curve = true_curve
    panel.wrong_curve = wrong_curve
    return panel


def make_precision_knob(initial_index=0):
    title = SafeText("precision knob", max_width=3.2, max_height=0.40, font_size=24, color=TEXT, weight="BOLD")
    track = Line(LEFT * 2.30, RIGHT * 2.30, color=GRID, stroke_width=5.0)
    positions = [track.point_from_proportion(p) for p in (0.0, 0.5, 1.0)]
    ticks = VGroup(*[Line(pos + DOWN * 0.12, pos + UP * 0.12, color=MUTED, stroke_width=2.0) for pos in positions])
    labels = VGroup(
        SafeText("fp16", max_width=0.9, max_height=0.25, font_size=17, color=MUTED),
        SafeText("fp32", max_width=0.9, max_height=0.25, font_size=17, color=MUTED),
        SafeText("fp64", max_width=0.9, max_height=0.25, font_size=17, color=MUTED),
    )
    for label, pos in zip(labels, positions):
        label.next_to(pos, DOWN, buff=0.24)
    marker = Dot(positions[initial_index], radius=0.105, color=OPERATOR)
    note = SafeText("coarse mesh still dominates", max_width=4.6, max_height=0.35, font_size=20, color=WARNING, weight="BOLD")
    note.next_to(labels, DOWN, buff=0.35)
    group = VGroup(title, VGroup(track, ticks, labels, marker), note).arrange(DOWN, buff=0.28)
    group.marker = marker
    group.fp_positions = positions
    group.fp_ticks = ticks
    return group


def make_total_error_summary():
    formula = SafeMathTex(
        r"\text{total error} \approx \text{approximation} + \text{generalization} + \text{discretization}",
        max_width=10.8,
        max_height=0.62,
        font_size=30,
        color=TEXT,
    )
    chips = VGroup(
        Chip("approximation", max_width=2.25, height=0.42, stroke_color=INPUT, font_size=17),
        Chip("generalization", max_width=2.35, height=0.42, stroke_color=OUTPUT, font_size=17),
        Chip("discretization", max_width=2.45, height=0.42, stroke_color=WARNING, font_size=17),
    ).arrange(RIGHT, buff=0.28)
    return VGroup(formula, chips).arrange(DOWN, buff=0.34)


def make_precision_view():
    sampling = make_coarse_sampling_panel().scale(0.82)
    knob = make_precision_knob()
    knob.next_to(sampling, RIGHT, buff=0.55)
    title = SafeText("higher precision does not recover missing samples", max_width=8.8, max_height=0.48, font_size=30, color=TEXT, weight="BOLD")
    view = VGroup(title, VGroup(sampling, knob).arrange(RIGHT, buff=0.55)).arrange(DOWN, buff=0.35).move_to(ORIGIN)
    view.knob = knob
    return view


def make_final_bridge_view():
    triangle = make_error_triangle(highlight_discretization=True).scale(0.86)
    summary = make_total_error_summary().scale(0.82)
    cue = VGroup(
        SafeText("Section 5", max_width=2.1, max_height=0.36, font_size=24, color=OPERATOR, weight="BOLD"),
        SafeText("discretization challenge", max_width=4.0, max_height=0.36, font_size=23, color=TEXT),
    ).arrange(RIGHT, buff=0.22)
    arrow = Arrow(LEFT * 1.20, RIGHT * 1.20, color=OPERATOR, stroke_width=2.5)
    cue_group = VGroup(arrow, cue).arrange(RIGHT, buff=0.24)
    return VGroup(triangle, summary, cue_group).arrange(DOWN, buff=0.20).move_to(ORIGIN)


class ErrorTriangle(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_error_triangle())


class HighFreqCurve(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_high_frequency_curve_panel())


class CoarseSampling(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_coarse_sampling_panel())


class PrecisionKnob(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_precision_knob())


class Scene0403ThreeErrorsWeMustRemember(TimedScene):
    SCRIPT_ID = "4.3"
    SCRIPT_TITLE = "The three errors we must remember"
    SCRIPT_START = 27 * 60 + 5
    SCRIPT_END = 29 * 60 + 10
    SCENE_DURATION = 125.0

    KEYFRAMES = (
        "KF01 0.0s familiar ML errors: approximation and generalization",
        "KF02 26.0s discretization enters as third vertex",
        "KF03 40.0s continuum only observed through samples and meshes",
        "KF04 55.0s coarse samples lose high-frequency detail",
        "KF05 70.0s total error triangle",
        "KF06 86.0s fp16 to fp64 precision knob, same coarse reconstruction",
        "KF07 116.0s discretization glows as bridge to Section 5",
    )

    def construct(self):
        background = make_background_network(seed=403, n=72, dot_opacity=0.12, line_opacity=0.09)
        self.add(background)

        familiar_cards = VGroup(
            make_error_card("approximation error", "function class expressivity", color=INPUT),
            make_error_card("generalization error", "data supports correct pattern", color=OUTPUT),
        ).arrange(RIGHT, buff=0.65)
        title = SafeText("familiar ML errors", max_width=5.5, max_height=0.48, font_size=34, color=TEXT, weight="BOLD")
        familiar_view = VGroup(title, familiar_cards).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        assert_in_frame(familiar_view, margin=0.35, label="familiar_view")

        # Global 27:05.0-27:17.0 => local 0.0-12.0
        self.play_timed(
            "familiar_ml_errors",
            0.0,
            12.0,
            FadeIn(familiar_view[0], shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in familiar_cards], lag_ratio=0.18),
        )

        expressivity_focus = VGroup(
            Chip("expressivity?", max_width=2.1, height=0.42, stroke_color=INPUT, font_size=18),
            Chip("enough data?", max_width=2.1, height=0.42, stroke_color=OUTPUT, font_size=18),
        ).arrange(RIGHT, buff=0.45)
        expressivity_focus.next_to(familiar_view, DOWN, buff=0.35)
        assert_in_frame(VGroup(familiar_view, expressivity_focus), margin=0.35, label="familiar_with_chips")

        # Global 27:17.0-27:30.0 => local 12.0-25.0
        self.play_timed(
            "expressivity_and_generalization_questions",
            12.0,
            25.0,
            LaggedStart(*[FadeIn(chip, shift=UP * 0.06) for chip in expressivity_focus], lag_ratio=0.20),
        )

        # Global 27:30.0-27:31.0 => local 25.0-26.0
        self.wait_timed("pause_before_third_error", 25.0, 26.0)

        triangle = make_error_triangle()
        assert_in_frame(triangle, margin=0.30, label="error_triangle")

        # Global 27:31.0-27:45.0 => local 26.0-40.0
        self.play_timed(
            "discretization_enters_triangle",
            26.0,
            40.0,
            FadeOut(VGroup(familiar_view, expressivity_focus), shift=UP * 0.10),
            FadeIn(triangle[2], shift=DOWN * 0.08),
            FadeIn(triangle[0]),
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in triangle[1]], lag_ratio=0.16),
        )

        continuum_panel = make_high_frequency_curve_panel()
        observations = make_observation_icons()
        observations.next_to(continuum_panel, RIGHT, buff=0.48)
        continuum_view = VGroup(
            SafeText("we never see the whole continuum", max_width=6.6, max_height=0.45, font_size=31, color=TEXT, weight="BOLD"),
            VGroup(continuum_panel, observations),
        ).arrange(DOWN, buff=0.36).move_to(ORIGIN)
        assert_in_frame(continuum_view, margin=0.35, label="continuum_view")

        # Global 27:45.0-28:00.0 => local 40.0-55.0
        self.play_timed(
            "continuum_observed_by_discretization",
            40.0,
            55.0,
            FadeOut(triangle, shift=UP * 0.10),
            FadeIn(continuum_view[0], shift=DOWN * 0.08),
            FadeIn(continuum_panel, shift=RIGHT * 0.08),
            LaggedStart(*[FadeIn(icon, shift=UP * 0.08) for icon in observations], lag_ratio=0.10),
        )

        coarse_panel = make_coarse_sampling_panel()
        assert_in_frame(coarse_panel, margin=0.35, label="coarse_panel")

        # Global 28:00.0-28:15.0 => local 55.0-70.0
        self.play_timed(
            "coarse_sampling_loses_high_frequency_information",
            55.0,
            70.0,
            FadeOut(continuum_view, shift=UP * 0.10),
            FadeIn(coarse_panel, shift=UP * 0.08),
            LaggedStart(*[Flash(dot, color=OUTPUT, flash_radius=0.18) for dot in coarse_panel.dots], lag_ratio=0.08),
        )

        triangle_summary = make_error_triangle(highlight_discretization=True).scale(0.86)
        total_summary = make_total_error_summary()
        total_view = VGroup(triangle_summary, total_summary).arrange(DOWN, buff=0.22).move_to(ORIGIN)
        assert_in_frame(total_view, margin=0.35, label="total_view")

        # Global 28:15.0-28:31.0 => local 70.0-86.0
        self.play_timed(
            "three_error_analysis_summary",
            70.0,
            86.0,
            FadeOut(coarse_panel, shift=UP * 0.10),
            FadeIn(triangle_summary, shift=DOWN * 0.08),
            FadeIn(total_summary, shift=UP * 0.08),
        )

        precision_view = make_precision_view()
        assert_in_frame(precision_view, margin=0.35, label="precision_view")

        # Global 28:31.0-28:46.0 => local 86.0-101.0
        self.play_timed(
            "precision_knob_appears_fp16",
            86.0,
            101.0,
            FadeOut(total_view, shift=UP * 0.10),
            FadeIn(precision_view, shift=UP * 0.08),
        )

        # Global 28:46.0-28:58.0 => local 101.0-113.0
        self.play_timed(
            "precision_increases_but_reconstruction_same",
            101.0,
            113.0,
            precision_view.knob.marker.animate.move_to(precision_view.knob.fp_ticks[2].get_center()),
        )

        # Global 28:58.0-29:01.0 => local 113.0-116.0
        self.play_timed(
            "coarse_mesh_bottleneck_holds",
            113.0,
            116.0,
            Circumscribe(precision_view.knob[-1], color=WARNING, buff=0.08),
        )

        final_bridge = make_final_bridge_view()
        assert_in_frame(final_bridge, margin=0.35, label="final_bridge")

        # Global 29:01.0-29:10.0 => local 116.0-125.0
        self.play_timed(
            "bridge_to_section_5_discretization_challenge",
            116.0,
            125.0,
            FadeOut(precision_view, shift=UP * 0.10),
            FadeIn(final_bridge, shift=UP * 0.08),
            Circumscribe(final_bridge[0].discretization_card, color=WARNING, buff=0.10),
        )

        self.pad_to(self.SCENE_DURATION)
