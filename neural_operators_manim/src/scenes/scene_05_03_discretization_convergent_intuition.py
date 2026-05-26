"""
Scene 5.3 - Discretization-convergent intuition
Script: ../docs/full_voice_manim_script.md
Global time: 33:05.0-35:00.0
Local duration: 115.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import smooth_path
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
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
    WARNING,
)
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


VO_LINES = (
    (0.0, 13.0, "Một model discretization-convergent có nghĩa trực giác như sau."),
    (13.0, 25.5, "Khi ta refine mesh — làm lưới mịn hơn — prediction của model không nên nhảy lung tung."),
    (25.5, 41.0, "Nó nên tiến gần về một limit continuum duy nhất, giống như Riemann sum tiến về integral."),
    (41.0, 42.0, "Pause: 1.0s."),
    (42.0, 57.5, "Đây là khác biệt giữa “chạy được trên nhiều resolution” và “có nguyên lý toán học khi resolution thay đổi”."),
    (57.5, 74.5, "Một model có thể resize input và vẫn chạy. Nhưng neural operator muốn mạnh hơn: cùng một set parameters, cùng một operator underlying, nhiều discretization khác nhau."),
    (74.5, 115.0, "Đó là cây cầu nối finite computation trên máy tính với infinite-dimensional problem trong toán học."),
)


def field_value(point):
    x = float(point[0])
    y = float(point[1])
    return np.sin(1.2 * x) * np.cos(1.1 * y) + 0.25 * np.sin(2.2 * x + 0.5 * y)


def _field_color(value):
    normalized = np.clip((value + 1.35) / 2.70, 0.0, 0.999)
    colors = [PURPLE, INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR]
    return colors[int(normalized * (len(colors) - 1))]


def make_mesh_overlay(nx=8, ny=5, width=3.6, height=2.1, opacity=0.32, color=TEXT):
    lines = VGroup()
    for i in range(nx + 1):
        x = -width / 2 + width * i / nx
        lines.add(Line([x, -height / 2, 0], [x, height / 2, 0], color=color, stroke_width=0.55, stroke_opacity=opacity))
    for j in range(ny + 1):
        y = -height / 2 + height * j / ny
        lines.add(Line([-width / 2, y, 0], [width / 2, y, 0], color=color, stroke_width=0.55, stroke_opacity=opacity))
    return lines


def _sampled_cells(nx, ny, width, height, closeness=1.0, phase=0.0, fill_opacity=0.62):
    cells = VGroup()
    for ix in range(nx):
        for iy in range(ny):
            x = -width / 2 + width * (ix + 0.5) / nx
            y = -height / 2 + height * (iy + 0.5) / ny
            artifact = np.sin((ix + 1) * 1.7 + phase) * np.cos((iy + 2) * 1.1 - phase)
            value = closeness * field_value([x, y, 0]) + (1.0 - closeness) * 0.85 * artifact
            cells.add(
                Rectangle(
                    width=width / nx + 0.008,
                    height=height / ny + 0.008,
                    stroke_width=0,
                    fill_color=_field_color(value),
                    fill_opacity=fill_opacity,
                ).move_to([x, y, 0])
            )
    return cells


def make_continuum_field(width=7.2, height=3.8, resolution=(24, 13)):
    cells = _sampled_cells(resolution[0], resolution[1], width, height, closeness=1.0, fill_opacity=0.48)
    glow = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=OPERATOR,
        stroke_width=2.0,
        stroke_opacity=0.78,
        fill_opacity=0,
    )
    label = SafeText("continuum limit", max_width=2.7, max_height=0.35, font_size=22, color=OPERATOR, weight="BOLD")
    label.next_to(glow, DOWN, buff=0.14)
    field = VGroup(cells, glow, label)
    field.glow = glow
    return field


def make_sampled_prediction(nx=8, ny=5, closeness=0.65, width=3.45, height=2.0, title=None, phase=0.0):
    cells = _sampled_cells(nx, ny, width, height, closeness=closeness, phase=phase, fill_opacity=0.64)
    mesh = make_mesh_overlay(nx, ny, width=width, height=height, opacity=0.23)
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.06, stroke_color=SCIENCE, stroke_width=1.1, fill_opacity=0)
    body = VGroup(cells, mesh, frame)
    if title is None:
        return body
    label = SafeText(title, max_width=width, max_height=0.33, font_size=20, color=TEXT, weight="BOLD")
    label.next_to(body, DOWN, buff=0.10)
    return VGroup(body, label)


def _field_panel(title, nx, ny, closeness=1.0, phase=0.0, width=3.15, height=2.34, accent=SCIENCE):
    field = make_sampled_prediction(nx, ny, closeness=closeness, width=2.55, height=1.45, phase=phase)
    return PanelCard(title, body=field, width=width, height=height, accent_color=accent, title_font_size=20)


def make_refinement_triptych():
    cards = VGroup(
        _field_panel("coarse", 5, 3, accent=WARNING),
        _field_panel("medium", 9, 5, accent=SCIENCE),
        _field_panel("fine", 15, 8, accent=OPERATOR),
    ).arrange(RIGHT, buff=0.36)
    arrow_y = cards.get_top()[1] + 0.34
    arrow = Arrow(
        [cards.get_left()[0] + 0.18, arrow_y, 0],
        [cards.get_right()[0] - 0.18, arrow_y, 0],
        buff=0.02,
        color=OPERATOR,
        stroke_width=3.0,
    )
    arrow_label = Chip("same operator", max_width=2.45, height=0.44, stroke_color=OPERATOR, font_size=18)
    arrow_label.next_to(arrow, UP, buff=0.08)
    triptych = VGroup(arrow, arrow_label, cards).move_to(ORIGIN)
    return triptych


def make_prediction_convergence_view():
    continuum = make_continuum_field(width=3.2, height=1.86, resolution=(18, 10))
    continuum.set_opacity(0.36)
    continuum_label = SafeText("limit", max_width=1.2, max_height=0.28, font_size=18, color=OPERATOR)
    continuum_label.next_to(continuum, DOWN, buff=0.06)
    fine = make_sampled_prediction(15, 8, 0.96, width=3.2, height=1.86)
    fine_group = VGroup(continuum, fine, continuum_label)

    cards = VGroup(
        PanelCard("coarse prediction", body=make_sampled_prediction(5, 3, 0.54, width=2.65, height=1.55), width=3.15, height=2.50, accent_color=WARNING, title_font_size=19),
        PanelCard("medium prediction", body=make_sampled_prediction(9, 5, 0.76, width=2.65, height=1.55), width=3.15, height=2.50, accent_color=SCIENCE, title_font_size=19),
        PanelCard("fine prediction", body=fine_group, width=3.15, height=2.50, accent_color=OPERATOR, title_font_size=19),
    ).arrange(RIGHT, buff=0.28)

    graph_frame = RoundedRectangle(width=4.3, height=1.45, corner_radius=0.08, stroke_color=GRID, stroke_width=1.0, fill_color=CARD_BG, fill_opacity=0.64)
    label = SafeText("distance to limit ↓", max_width=3.6, max_height=0.32, font_size=20, color=OPERATOR, weight="BOLD")
    label.move_to(graph_frame.get_top() + DOWN * 0.26)
    axes = VGroup(
        Line(graph_frame.get_left() + RIGHT * 0.38 + DOWN * 0.40, graph_frame.get_right() + LEFT * 0.30 + DOWN * 0.40, color=MUTED, stroke_width=1.1),
        Line(graph_frame.get_left() + RIGHT * 0.38 + DOWN * 0.40, graph_frame.get_left() + RIGHT * 0.38 + UP * 0.34, color=MUTED, stroke_width=1.1),
    )
    curve = smooth_path(
        [
            graph_frame.get_left() + RIGHT * 0.50 + UP * 0.22,
            graph_frame.get_left() + RIGHT * 1.45 + UP * 0.02,
            graph_frame.get_left() + RIGHT * 2.55 + DOWN * 0.22,
            graph_frame.get_right() + LEFT * 0.42 + DOWN * 0.34,
        ],
        color=OPERATOR,
        stroke_width=3.0,
    )
    graph = VGroup(graph_frame, label, axes, curve)
    view = VGroup(cards, graph).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    view.limit_glow = continuum.glow
    return view


def make_unstable_vs_convergent_panel():
    left_fields = VGroup(
        make_sampled_prediction(5, 3, 0.42, width=1.65, height=0.95, phase=0.2),
        make_sampled_prediction(9, 5, 0.38, width=1.65, height=0.95, phase=1.7),
        make_sampled_prediction(15, 8, 0.46, width=1.65, height=0.95, phase=3.1),
    ).arrange(DOWN, buff=0.12)
    warning = Chip("warning: unstable pattern", max_width=3.15, height=0.42, stroke_color=WARNING, font_size=15)
    left_body = VGroup(left_fields, warning).arrange(DOWN, buff=0.16)
    left = PanelCard("runs on many resolutions", body=left_body, width=5.0, height=4.65, accent_color=WARNING, title_font_size=22)

    right_fields = VGroup(
        make_sampled_prediction(5, 3, 0.58, width=1.65, height=0.95),
        make_sampled_prediction(9, 5, 0.78, width=1.65, height=0.95),
        make_sampled_prediction(15, 8, 0.96, width=1.65, height=0.95),
    ).arrange(DOWN, buff=0.12)
    limit = Chip("aligns with limit", max_width=2.75, height=0.42, stroke_color=OPERATOR, font_size=15)
    right_body = VGroup(right_fields, limit).arrange(DOWN, buff=0.16)
    right = PanelCard("converges under refinement", body=right_body, width=5.0, height=4.65, accent_color=OPERATOR, title_font_size=22)

    contrast = SafeText("runs ≠ converges", max_width=4.0, max_height=0.48, font_size=32, color=WARNING, weight="BOLD")
    row = VGroup(left, right).arrange(RIGHT, buff=0.70)
    return VGroup(contrast, row).arrange(DOWN, buff=0.34).move_to(ORIGIN)


def make_parameter_capsule():
    theta = SafeMathTex(r"\theta", max_width=0.65, max_height=0.56, font_size=42, color=OPERATOR)
    capsule = RoundedRectangle(width=2.25, height=1.08, corner_radius=0.22, stroke_color=OPERATOR, stroke_width=2.0, fill_color="#211B32", fill_opacity=0.88)
    theta.move_to(capsule)
    operator = VGroup(capsule, theta)
    same_theta = Chip("same θ", max_width=1.75, height=0.44, stroke_color=OPERATOR, font_size=18)
    same_theta.next_to(operator, UP, buff=0.18)
    same_operator = Chip("same underlying operator", max_width=3.30, height=0.46, stroke_color=SCIENCE, font_size=17)
    same_operator.next_to(operator, RIGHT, buff=0.28)

    meshes = VGroup(
        _field_panel("coarse", 4, 3, width=2.45, height=1.95, accent=WARNING),
        _field_panel("medium", 8, 5, width=2.45, height=1.95, accent=SCIENCE),
        _field_panel("fine", 14, 8, width=2.45, height=1.95, accent=OPERATOR),
    )
    meshes.arrange_in_grid(rows=1, cols=3, buff=0.38)
    mesh_label = Chip("different discretizations", max_width=3.25, height=0.46, stroke_color=INPUT, font_size=17)
    mesh_row = VGroup(meshes, mesh_label).arrange(DOWN, buff=0.22)
    mesh_row.next_to(operator, DOWN, buff=0.92)
    targets = [operator.get_left() + DOWN * 0.16, operator.get_bottom() + DOWN * 0.04, operator.get_right() + DOWN * 0.16]
    arrows = VGroup(
        *[
            Arrow(card.get_top() + UP * 0.05, target, buff=0.08, color=INPUT, stroke_width=1.6)
            for card, target in zip(meshes, targets)
        ]
    )
    return VGroup(same_theta, operator, same_operator, mesh_row, arrows).move_to(ORIGIN)


def make_finite_to_continuum_bridge():
    grids = VGroup()
    for k, (nx, ny) in enumerate([(4, 3), (7, 4), (10, 6)]):
        grid = VGroup(
            Rectangle(width=2.0, height=1.20, stroke_color=[WARNING, SCIENCE, OPERATOR][k], stroke_width=1.2, fill_color=CARD_BG, fill_opacity=0.48),
            make_mesh_overlay(nx, ny, width=2.0, height=1.20, opacity=0.30),
        ).shift(RIGHT * 0.15 * k + UP * 0.10 * k)
        grids.add(grid)
    left_label = SafeText("finite computation", max_width=3.2, max_height=0.36, font_size=24, color=TEXT, weight="BOLD")
    left_label.next_to(grids, DOWN, buff=0.18)
    left = VGroup(grids, left_label)

    continuum = make_continuum_field(width=3.25, height=1.90, resolution=(20, 11))
    continuum[-1].become(SafeText("continuum function space", max_width=3.8, max_height=0.36, font_size=22, color=OPERATOR, weight="BOLD"))
    continuum[-1].next_to(continuum[1], DOWN, buff=0.16)

    bridge = Arrow(LEFT * 1.55, RIGHT * 1.55, buff=0.08, color=OPERATOR, stroke_width=3.2)
    bridge_label = Chip("finite computation → continuum operator", max_width=4.35, height=0.48, stroke_color=OPERATOR, font_size=17)
    bridge_label.next_to(bridge, UP, buff=0.16)
    row = VGroup(left, VGroup(bridge, bridge_label), continuum).arrange(RIGHT, buff=0.55)

    final = VGroup(
        SafeText("Discretization is how we compute.", max_width=7.4, max_height=0.44, font_size=29, color=TEXT, weight="BOLD"),
        SafeText("The operator is what we learn.", max_width=7.4, max_height=0.44, font_size=29, color=OPERATOR, weight="BOLD"),
    ).arrange(DOWN, buff=0.12)
    return VGroup(row, final).arrange(DOWN, buff=0.44).move_to(ORIGIN)


class Scene0503DiscretizationConvergentIntuition(TimedScene):
    SCRIPT_ID = "5.3"
    SCRIPT_TITLE = "Discretization-convergent intuition"
    SCRIPT_START = 33 * 60 + 5
    SCRIPT_END = 35 * 60
    SCENE_DURATION = 115.0

    KEYFRAMES = (
        "KF01 0.0s continuum field behind coarse mesh",
        "KF02 13.0s coarse medium fine refinement triptych",
        "KF03 25.5s predictions approach continuum limit",
        "KF04 42.0s runs many resolutions versus converges",
        "KF05 57.5s same theta with changing mesh cards",
        "KF06 74.5s finite computation to continuum operator bridge",
    )

    def construct(self):
        background = make_background_network(seed=503, n=72, dot_opacity=0.10, line_opacity=0.08)
        self.add(background)

        continuum = make_continuum_field(width=6.9, height=3.55, resolution=(22, 12))
        coarse_mesh = make_mesh_overlay(5, 3, width=6.9, height=3.55, opacity=0.52, color=TEXT)
        title = SafeText("discretization-convergent", max_width=7.6, max_height=0.58, font_size=39, color=OPERATOR, weight="BOLD")
        subtitle = SafeText("mesh refinement → stable continuum limit", max_width=7.9, max_height=0.42, font_size=26, color=TEXT)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.12).next_to(continuum, UP, buff=0.26)
        opening = VGroup(continuum, coarse_mesh, title_group).move_to(ORIGIN)
        assert_in_frame(opening, margin=0.35, label="opening")
        self.add(opening)

        triptych = make_refinement_triptych()
        assert_in_frame(triptych, margin=0.35, label="triptych")

        # VO exact: Một model discretization-convergent có nghĩa trực giác như sau.
        # Global 33:05.0-33:18.0 => 33:05.0 -> local 0.0, 33:18.0 -> local 13.0
        self.play_timed(
            "coarse_mesh_over_hidden_continuum",
            0.0,
            12.2,
            FadeIn(title_group, shift=DOWN * 0.08),
            Indicate(continuum.glow, color=OPERATOR, scale_factor=1.01),
        )
        self.play_timed(
            "transition_to_refinement_triptych",
            12.2,
            13.0,
            FadeOut(opening, shift=UP * 0.10),
            FadeIn(triptych, shift=UP * 0.08),
        )

        convergence = make_prediction_convergence_view()
        assert_in_frame(convergence, margin=0.35, label="convergence")

        # VO exact: Khi ta refine mesh — làm lưới mịn hơn — prediction của model không nên nhảy lung tung.
        # Global 33:18.0-33:30.5 => 33:18.0 -> local 13.0, 33:30.5 -> local 25.5
        self.play_timed(
            "coarse_medium_fine_same_operator",
            13.0,
            25.1,
            Indicate(triptych[1], color=OPERATOR, scale_factor=1.01),
        )
        self.play_timed(
            "transition_to_prediction_convergence",
            25.1,
            25.5,
            FadeOut(triptych, shift=UP * 0.10),
            FadeIn(convergence, shift=DOWN * 0.08),
        )

        # VO exact: Nó nên tiến gần về một limit continuum duy nhất, giống như Riemann sum tiến về integral.
        # Global 33:30.5-33:46.0 => 33:30.5 -> local 25.5, 33:46.0 -> local 41.0
        self.play_timed(
            "predictions_approach_continuum_limit",
            25.5,
            41.0,
            Circumscribe(convergence.limit_glow, color=OPERATOR, buff=0.05),
        )

        contrast = make_unstable_vs_convergent_panel()
        assert_in_frame(contrast, margin=0.35, label="contrast")

        # VO exact: Pause: 1.0s.
        # Global 33:46.0-33:47.0 => 33:46.0 -> local 41.0, 33:47.0 -> local 42.0
        self.play_timed(
            "pause_continuum_limit_pulse",
            41.0,
            41.5,
            Indicate(convergence.limit_glow, color=OPERATOR, scale_factor=1.01),
        )
        self.wait_timed("hold_continuum_limit_pulse", 41.5, 41.6)
        self.play_timed(
            "transition_to_resolution_contrast",
            41.6,
            42.0,
            FadeOut(convergence, shift=UP * 0.10),
            FadeIn(contrast[0], shift=DOWN * 0.08),
            FadeIn(contrast[1], shift=UP * 0.08),
        )

        parameters = make_parameter_capsule()
        assert_in_frame(parameters, margin=0.35, label="parameters")

        # VO exact: Đây là khác biệt giữa “chạy được trên nhiều resolution” và “có nguyên lý toán học khi resolution thay đổi”.
        # Global 33:47.0-34:02.5 => 33:47.0 -> local 42.0, 34:02.5 -> local 57.5
        self.play_timed(
            "runs_many_resolutions_versus_converges",
            42.0,
            57.1,
            Indicate(contrast[0], color=WARNING, scale_factor=1.01),
        )
        self.play_timed(
            "transition_to_same_parameters",
            57.1,
            57.5,
            FadeOut(contrast, shift=UP * 0.10),
            FadeIn(parameters, shift=DOWN * 0.08),
        )

        # VO exact: Một model có thể resize input và vẫn chạy. Nhưng neural operator muốn mạnh hơn: cùng một set parameters, cùng một operator underlying, nhiều discretization khác nhau.
        # Global 34:02.5-34:19.5 => 34:02.5 -> local 57.5, 34:19.5 -> local 74.5
        self.play_timed(
            "same_parameters_same_operator_different_discretizations",
            57.5,
            74.1,
            Circumscribe(parameters[0], color=OPERATOR, buff=0.07),
            Circumscribe(parameters[2], color=SCIENCE, buff=0.07),
        )

        bridge = make_finite_to_continuum_bridge()
        assert_in_frame(bridge, margin=0.35, label="bridge")

        self.play_timed(
            "transition_to_finite_continuum_bridge",
            74.1,
            74.5,
            FadeOut(parameters, shift=UP * 0.10),
            FadeIn(bridge[0], shift=UP * 0.08),
        )

        # VO exact: Đó là cây cầu nối finite computation trên máy tính với infinite-dimensional problem trong toán học.
        # Global 34:19.5-35:00.0 => 34:19.5 -> local 74.5, 35:00.0 -> local 115.0
        self.play_timed(
            "finite_computation_to_continuum_operator_bridge",
            74.5,
            95.0,
            Indicate(bridge[0][1], color=OPERATOR, scale_factor=1.01),
        )

        # Global 34:40.0-35:00.0 => local 95.0-115.0, 35:00.0 -> local 115.0
        self.play_timed(
            "final_compute_vs_learn_sentence",
            95.0,
            114.85,
            FadeIn(bridge[1], shift=UP * 0.08),
            Circumscribe(bridge[1], color=OPERATOR, buff=0.10),
        )

        # Manim frame concatenation for this many partial clips adds 3 frames at 20fps.
        self.t = self.SCENE_DURATION
        self.pad_to(self.SCENE_DURATION)
