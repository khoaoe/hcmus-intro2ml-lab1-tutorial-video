"""
Scene 9.4 - Question embedded: what if input/output domains differ?
Script: ../docs/full_voice_manim_script.md
Global time: 1:05:10.0-1:07:40.0
Local duration: 150.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText
from src.common.theme import apply_global_config, CARD_BG, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_wall_surface():
    wall = Polygon(
        [-1.15, -1.15, 0],
        [1.15, -0.72, 0],
        [1.15, 1.15, 0],
        [-1.15, 0.72, 0],
        stroke_color=INPUT,
        stroke_width=1.6,
        fill_color="#0B3148",
        fill_opacity=0.70,
    )
    grid = VGroup()
    for alpha in (0.2, 0.4, 0.6, 0.8):
        grid.add(Line(wall.point_from_proportion(alpha * 0.24), wall.point_from_proportion(0.5 + alpha * 0.24), color=GRID, stroke_width=0.8))
    samples = VGroup(
        Dot([-0.72, -0.42, 0], radius=0.055, color=OPERATOR),
        Dot([-0.18, 0.18, 0], radius=0.055, color=OUTPUT),
        Dot([0.46, -0.12, 0], radius=0.055, color=WARNING),
        Dot([0.72, 0.50, 0], radius=0.055, color=PURPLE),
    )
    title = SafeText("input domain: 2D surface", max_width=3.1, max_height=0.30, font_size=21, color=INPUT)
    subtitle = SafeText("wall temperature", max_width=2.35, max_height=0.26, font_size=18, color=TEXT)
    labels = VGroup(title, subtitle).arrange(DOWN, buff=0.08).next_to(wall, UP, buff=0.18)
    group = VGroup(wall, grid, samples, labels).move_to(LEFT * 4.65 + DOWN * 0.15)
    group.wall = wall
    group.samples = samples
    group.labels = labels
    return group


def make_room_volume():
    back = Polygon(
        [-1.0, -0.72, 0],
        [0.65, -0.40, 0],
        [0.65, 0.96, 0],
        [-1.0, 0.72, 0],
        stroke_color=OUTPUT,
        stroke_width=1.2,
        fill_color="#083329",
        fill_opacity=0.42,
    )
    front = Polygon(
        [-0.55, -1.05, 0],
        [1.15, -0.68, 0],
        [1.15, 0.72, 0],
        [-0.55, 1.05, 0],
        stroke_color=OUTPUT,
        stroke_width=1.6,
        fill_color="#0D4A3A",
        fill_opacity=0.30,
    )
    connectors = VGroup(
        Line(back.get_vertices()[0], front.get_vertices()[0], color=GRID, stroke_width=1.0),
        Line(back.get_vertices()[1], front.get_vertices()[1], color=GRID, stroke_width=1.0),
        Line(back.get_vertices()[2], front.get_vertices()[2], color=GRID, stroke_width=1.0),
        Line(back.get_vertices()[3], front.get_vertices()[3], color=GRID, stroke_width=1.0),
    )
    query = Dot([0.23, 0.02, 0], radius=0.070, color=OPERATOR)
    query_label = SafeText("interior query", max_width=1.7, max_height=0.24, font_size=17, color=OPERATOR)
    query_label.next_to(query, UP, buff=0.12)
    title = SafeText("output domain: 3D volume", max_width=3.1, max_height=0.30, font_size=21, color=OUTPUT)
    title.next_to(front, UP, buff=0.20)
    group = VGroup(back, front, connectors, query, query_label, title).move_to(RIGHT * 4.65 + DOWN * 0.15)
    group.query = query
    group.title = title
    return group


def make_cross_domain_kernel(wall_surface, room_volume):
    label = SafeMathTex(r"\kappa(y,x)", max_width=1.75, max_height=0.42, font_size=32, color=OPERATOR)
    label.move_to(UP * 2.45)
    kernel_name = Chip("cross-domain kernel", max_width=2.75, height=0.42, stroke_color=OPERATOR, font_size=17)
    kernel_name.next_to(label, DOWN, buff=0.12)
    lines = VGroup()
    for dot in wall_surface.samples:
        lines.add(DashedLine(dot.get_center(), room_volume.query.get_center(), color=OPERATOR, stroke_width=1.4, stroke_opacity=0.62, dash_length=0.10))
    group = VGroup(lines, label, kernel_name)
    group.lines = lines
    group.label = label
    group.kernel_name = kernel_name
    return group


def make_learned_residual_bridge():
    no_identity = PanelCard(
        "residual issue",
        body=SafeText("identity residual unavailable", max_width=3.0, max_height=0.42, font_size=20, color=WARNING),
        width=3.75,
        height=1.45,
        accent_color=WARNING,
        title_font_size=21,
    )
    bridge = PanelCard(
        "learned residual bridge",
        body=SafeText("map features across domains", max_width=3.0, max_height=0.42, font_size=20, color=OUTPUT),
        width=3.75,
        height=1.45,
        accent_color=OUTPUT,
        title_font_size=21,
    )
    group = VGroup(no_identity, bridge).arrange(RIGHT, buff=0.45).move_to(DOWN * 2.95)
    group.no_identity = no_identity
    group.bridge = bridge
    return group


class Scene0904DifferentInputOutputDomains(TimedScene):
    SCRIPT_ID = "9.4"
    SCRIPT_TITLE = "Question embedded: what if input/output domains differ?"
    SCRIPT_START = 65 * 60 + 10
    SCRIPT_END = 67 * 60 + 40
    SCENE_DURATION = 150.0

    KEYFRAMES = (
        "KF01 0.0s question on different domains",
        "KF02 12.0s wall temperature example",
        "KF03 26.0s 2D surface to 3D volume",
        "KF04 39.0s pause",
        "KF05 40.0s cross-domain kernel",
        "KF06 55.0s operator maps domains",
        "KF07 70.5s residual subtlety",
        "KF08 86.0s geometry-first architecture",
        "KF09 150.0s final cross-domain frame",
    )

    def construct(self):
        background = make_background_network(seed=904, n=70, dot_opacity=0.075, line_opacity=0.04)
        section_label = Chip("9.4  Different domains", max_width=3.05, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        question = SafeText("What if input and output domains differ?", max_width=7.4, max_height=0.48, font_size=32, color=TEXT, weight="BOLD")
        question.move_to(UP * 3.10)
        wall = make_wall_surface()
        room = make_room_volume()
        kernel = make_cross_domain_kernel(wall, room)
        residual = make_learned_residual_bridge()
        geometry = Chip("geometry first, architecture second", max_width=4.45, height=0.50, stroke_color=SCIENCE, font_size=19)
        geometry.move_to(DOWN * 3.75)

        assert_in_frame(VGroup(section_label, question, wall, room, residual, geometry), margin=0.30, label="scene_09_04_full")

        self.add(background)

        # Global 1:05:10.0 -> local 0.0; Global 1:05:22.0 -> local 12.0
        self.play_timed(
            "ask_different_domain_question",
            0.0,
            12.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(question, shift=DOWN * 0.05),
        )

        # Global 1:05:22.0 -> local 12.0; Global 1:05:36.0 -> local 26.0
        self.play_timed(
            "show_wall_temperature_input",
            12.0,
            26.0,
            FadeIn(wall, shift=RIGHT * 0.06),
            Circumscribe(wall.samples, color=OPERATOR, buff=0.08),
        )

        # Global 1:05:36.0 -> local 26.0; Global 1:05:49.0 -> local 39.0
        self.play_timed(
            "show_surface_to_volume_domains",
            26.0,
            39.0,
            FadeIn(room, shift=LEFT * 0.06),
            Circumscribe(VGroup(wall.labels, room.title), color=OUTPUT, buff=0.08),
        )

        # Global 1:05:49.0 -> local 39.0; Global 1:05:50.0 -> local 40.0
        self.wait_timed("pause_before_kernel_answer", 39.0, 40.0)

        # Global 1:05:50.0 -> local 40.0; Global 1:06:05.0 -> local 55.0
        self.play_timed(
            "draw_cross_domain_kernel",
            40.0,
            55.0,
            Create(kernel.lines),
            FadeIn(kernel.label, shift=DOWN * 0.04),
            FadeIn(kernel.kernel_name, shift=DOWN * 0.04),
        )

        # Global 1:06:05.0 -> local 55.0; Global 1:06:20.5 -> local 70.5
        self.play_timed(
            "show_operator_maps_between_domains",
            55.0,
            70.5,
            Circumscribe(VGroup(wall, room), color=OUTPUT, buff=0.14),
            kernel.lines.animate.set_stroke(opacity=0.86, width=1.8),
        )

        # Global 1:06:20.5 -> local 70.5; Global 1:06:36.0 -> local 86.0
        self.play_timed(
            "explain_residual_bridge",
            70.5,
            86.0,
            FadeIn(residual, shift=UP * 0.05),
            Circumscribe(residual.no_identity, color=WARNING, buff=0.06),
        )

        # Global 1:06:36.0 -> local 86.0; Global 1:07:40.0 -> local 150.0
        self.play_timed(
            "geometry_first_architecture",
            86.0,
            116.0,
            FadeIn(geometry, shift=UP * 0.05),
            Circumscribe(residual.bridge, color=OUTPUT, buff=0.06),
        )
        self.play_timed(
            "hold_cross_domain_example",
            116.0,
            149.8,
            question.animate.set_opacity(0.78),
            geometry.animate.set_opacity(1.0),
            kernel.lines.animate.set_stroke(opacity=0.56, width=1.4),
        )
        self.pad_to(self.SCENE_DURATION)
