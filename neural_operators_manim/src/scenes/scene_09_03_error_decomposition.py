"""
Scene 9.3 - Error decomposition
Script: ../docs/full_voice_manim_script.md
Global time: 1:03:20.0-1:05:10.0
Local duration: 110.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_error_segment(label, width, color):
    box = RoundedRectangle(
        width=width,
        height=0.88,
        corner_radius=0.06,
        stroke_color=color,
        stroke_width=1.4,
        fill_color=color,
        fill_opacity=0.18,
    )
    text = SafeText(label, max_width=width - 0.22, max_height=0.30, font_size=19, color=TEXT)
    text.move_to(box)
    return VGroup(box, text)


def make_error_decomposition_bar():
    title = SafeText("operator-level error", max_width=4.2, max_height=0.40, font_size=30, color=TEXT, weight="BOLD")
    segments = VGroup(
        make_error_segment("approximation error", 3.35, INPUT),
        make_error_segment("discretization error", 3.35, OPERATOR),
        make_error_segment("generalization error", 3.35, PURPLE),
    ).arrange(RIGHT, buff=0.08)
    pluses = VGroup()
    for left, right in zip(segments, segments[1:]):
        plus = SafeText("+", max_width=0.22, max_height=0.28, font_size=24, color=MUTED)
        plus.move_to((left.get_right() + right.get_left()) / 2)
        pluses.add(plus)
    bar = VGroup(segments, pluses)
    group = VGroup(title, bar).arrange(DOWN, buff=0.35).move_to(UP * 1.55)
    group.segments = segments
    group.title = title
    return group


def make_resolution_experiment_table():
    headers = ("split", "resolution", "question")
    rows = (
        ("train 16", "16 x 16", "fit observed mesh"),
        ("test 32", "32 x 32", "transfer resolution"),
        ("test 64", "64 x 64", "mesh refinement"),
    )
    cells = VGroup()
    for r, row in enumerate((headers,) + rows):
        for c, text in enumerate(row):
            width = (1.55, 1.75, 2.55)[c]
            color = OPERATOR if r == 0 else (INPUT if c == 0 else TEXT)
            cell = RoundedRectangle(
                width=width,
                height=0.48,
                corner_radius=0.04,
                stroke_color=GRID,
                stroke_width=0.9,
                fill_color=CARD_BG,
                fill_opacity=0.72 if r else 0.88,
            )
            label = SafeText(text, max_width=width - 0.18, max_height=0.20, font_size=15 if r else 16, color=color)
            label.move_to(cell)
            cells.add(VGroup(cell, label))
    table = VGroup()
    index = 0
    for r in range(4):
        row_group = VGroup(*[cells[index + c] for c in range(3)]).arrange(RIGHT, buff=0.02)
        table.add(row_group)
        index += 3
    table.arrange(DOWN, buff=0.02)
    caption = SafeText("mesh refinement + evaluation metric", max_width=4.4, max_height=0.34, font_size=19, color=MUTED)
    group = VGroup(table, caption).arrange(DOWN, buff=0.24).move_to(DOWN * 0.95)
    group.table = table
    group.caption = caption
    return group


def make_same_grid_warning():
    warning = Chip("same-grid only is not full operator validation", max_width=5.65, height=0.52, stroke_color=WARNING, font_size=19)
    warning.move_to(DOWN * 3.35)
    return warning


def make_operator_validation_panel():
    body = VGroup(
        SafeText("fixed grid", max_width=2.1, max_height=0.25, font_size=20, color=WARNING),
        Arrow(LEFT * 0.55, RIGHT * 0.55, color=GRID, stroke_width=2.0),
        SafeText("operator behavior", max_width=2.3, max_height=0.25, font_size=20, color=OUTPUT),
    ).arrange(RIGHT, buff=0.20)
    panel = PanelCard("validation must move across discretizations", body=body, width=5.6, height=1.45, accent_color=OUTPUT, title_font_size=20)
    panel.move_to(UP * 3.20)
    return panel


class Scene0903ErrorDecomposition(TimedScene):
    SCRIPT_ID = "9.3"
    SCRIPT_TITLE = "Error decomposition"
    SCRIPT_START = 63 * 60 + 20
    SCRIPT_END = 65 * 60 + 10
    SCENE_DURATION = 110.0

    KEYFRAMES = (
        "KF01 0.0s operator-level error bar",
        "KF02 11.5s approximation error",
        "KF03 25.0s discretization error",
        "KF04 38.5s pause",
        "KF05 39.5s generalization error",
        "KF06 55.0s resolution experiment table",
        "KF07 71.0s same-grid warning",
        "KF08 110.0s final validation frame",
    )

    def construct(self):
        background = make_background_network(seed=903, n=68, dot_opacity=0.075, line_opacity=0.04)
        section_label = Chip("9.3  Error decomposition", max_width=3.20, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        error_bar = make_error_decomposition_bar()
        table = make_resolution_experiment_table()
        warning = make_same_grid_warning()
        validation = make_operator_validation_panel()

        assert_in_frame(VGroup(section_label, error_bar, table, warning), margin=0.30, label="scene_09_03_full")

        self.add(background)

        # Global 1:03:20.0 -> local 0.0; Global 1:03:31.5 -> local 11.5
        self.play_timed(
            "show_operator_level_error",
            0.0,
            11.5,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(error_bar.title, shift=UP * 0.04),
            FadeIn(error_bar.segments[0], shift=RIGHT * 0.04),
        )

        # Global 1:03:31.5 -> local 11.5; Global 1:03:45.0 -> local 25.0
        self.play_timed(
            "define_approximation_error",
            11.5,
            25.0,
            Circumscribe(error_bar.segments[0], color=INPUT, buff=0.06),
            FadeIn(error_bar.segments[1], shift=RIGHT * 0.04),
        )

        # Global 1:03:45.0 -> local 25.0; Global 1:03:58.5 -> local 38.5
        self.play_timed(
            "define_discretization_error",
            25.0,
            38.5,
            Circumscribe(error_bar.segments[1], color=OPERATOR, buff=0.06),
            FadeIn(error_bar.segments[2], shift=RIGHT * 0.04),
        )

        # Global 1:03:58.5 -> local 38.5; Global 1:03:59.5 -> local 39.5
        self.wait_timed("pause_after_two_error_parts", 38.5, 39.5)

        # Global 1:03:59.5 -> local 39.5; Global 1:04:15.0 -> local 55.0
        self.play_timed(
            "add_generalization_error",
            39.5,
            55.0,
            Circumscribe(error_bar.segments[2], color=PURPLE, buff=0.06),
            FadeIn(validation, shift=DOWN * 0.04),
        )

        # Global 1:04:15.0 -> local 55.0; Global 1:04:31.0 -> local 71.0
        self.play_timed(
            "show_resolution_experiment_design",
            55.0,
            71.0,
            FadeIn(table, shift=UP * 0.05),
            Circumscribe(table.table, color=OUTPUT, buff=0.08),
        )

        # Global 1:04:31.0 -> local 71.0; Global 1:05:10.0 -> local 110.0
        self.play_timed(
            "warn_against_same_grid_only",
            71.0,
            94.0,
            FadeIn(warning, shift=UP * 0.05),
            Circumscribe(warning, color=WARNING, buff=0.08),
        )
        self.play_timed(
            "hold_full_operator_validation_story",
            94.0,
            109.8,
            error_bar.animate.set_opacity(0.86),
            table.animate.set_opacity(0.92),
            validation.animate.set_opacity(0.92),
        )
        self.pad_to(self.SCENE_DURATION)
