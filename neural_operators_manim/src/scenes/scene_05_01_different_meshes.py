"""
Scene 5.1 - Input and output may live on different meshes
Script: ../docs/full_voice_manim_script.md
Global time: 29:10.0-31:20.0
Local duration: 130.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.function_visuals import make_mesh_overlay, smooth_path
from src.common.layout import make_background_network
from src.common.panels import Chip, PanelCard
from src.common.safe_text import SafeMathTex, SafeText, fit_mobject_to_box
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


VO_LINES = (
    (0.0, 12.0, "Bây giờ hãy nhìn dữ liệu thật trong scientific computing. Input function có thể được đo trên một mesh."),
    (12.0, 23.5, "Output function có thể được lưu trên một mesh khác. Sample tiếp theo lại dùng một resolution khác nữa."),
    (23.5, 36.0, "Có dữ liệu trên regular grid, có dữ liệu trên irregular mesh, có sensor sparse, có boundary phức tạp."),
    (36.0, 37.0, "Pause: 1.0s."),
    (37.0, 50.0, "Nếu model buộc input và output phải là tensor cùng shape cố định, ta đã tự khóa mình vào một setup quá hẹp."),
    (50.0, 66.5, "Trong khi đó, bài toán vật lý thật không quan tâm ta lưu nó bằng grid nào. Nó tồn tại ở continuum level."),
    (66.5, 85.0, "Neural operator cố gắng làm điều ngược lại với resizing hack: nó định nghĩa computation sao cho có ý nghĩa khi mesh thay đổi."),
    (85.0, 130.0, "Đây là lý do ta cần các operation giống tích phân hơn là chỉ matrix multiplication trên index cố định."),
)


def _field_value(x, y):
    return 0.52 + 0.26 * np.sin(2.7 * x + 1.4 * y) + 0.18 * np.cos(3.5 * y - 0.8 * x)


def _field_color(value):
    colors = [PURPLE, INPUT, SCIENCE, NVIDIA_GREEN, OPERATOR]
    index = int(np.clip(value, 0.0, 0.999) * (len(colors) - 1))
    return colors[index]


def make_scalar_field(width=5.4, height=3.0, nx=18, ny=10, opacity=0.50):
    cells = VGroup()
    for ix in range(nx):
        for iy in range(ny):
            x = -2.0 + 4.0 * (ix + 0.5) / nx
            y = -1.3 + 2.6 * (iy + 0.5) / ny
            value = np.clip(_field_value(x, y), 0.0, 1.0)
            cells.add(
                Rectangle(
                    width=width / nx + 0.012,
                    height=height / ny + 0.012,
                    stroke_width=0,
                    fill_color=_field_color(value),
                    fill_opacity=opacity * (0.55 + 0.45 * value),
                ).move_to(
                    [
                        -width / 2 + width * (ix + 0.5) / nx,
                        -height / 2 + height * (iy + 0.5) / ny,
                        0,
                    ]
                )
            )
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=SCIENCE,
        stroke_width=1.0,
        stroke_opacity=0.45,
        fill_opacity=0,
    )
    return VGroup(cells, frame)


def _irregular_points(seed=501, point_count=34, width=4.9, height=2.45):
    rng = np.random.default_rng(seed)
    pts = []
    for _ in range(point_count):
        x = rng.uniform(-width / 2 + 0.12, width / 2 - 0.12)
        y = rng.uniform(-height / 2 + 0.12, height / 2 - 0.12)
        pts.append(np.array([x, y, 0.0]))
    return pts


def make_irregular_mesh(width=4.9, height=2.45, seed=501, point_count=34, color=INPUT):
    pts = _irregular_points(seed=seed, point_count=point_count, width=width, height=height)
    lines = VGroup()
    for i, p in enumerate(pts):
        neighbors = sorted(
            [(np.linalg.norm(p - q), q) for j, q in enumerate(pts) if i != j],
            key=lambda item: item[0],
        )[:3]
        for dist, q in neighbors:
            if dist < 1.25:
                lines.add(Line(p, q, color=color, stroke_width=0.65, stroke_opacity=0.34))
    dots = VGroup(*[Dot(p, radius=0.040, color=OUTPUT) for p in pts])
    return VGroup(lines, dots)


def make_regular_grid(width=4.7, height=2.45, nx=7, ny=5, color=OUTPUT):
    mesh = make_mesh_overlay(width=width, height=height, nx=nx, ny=ny, color=color)
    dots = VGroup()
    for ix in range(nx + 1):
        for iy in range(ny + 1):
            dots.add(
                Dot(
                    [
                        -width / 2 + width * ix / nx,
                        -height / 2 + height * iy / ny,
                        0,
                    ],
                    radius=0.026,
                    color=color,
                )
            )
    return VGroup(mesh, dots)


def make_complex_boundary(width=4.5, height=2.35, color=PURPLE):
    pts = [
        [-width / 2, -0.55, 0],
        [-1.62, 0.78, 0],
        [-0.62, 1.10, 0],
        [0.22, 0.60, 0],
        [1.22, 1.02, 0],
        [width / 2, 0.15, 0],
        [1.72, -0.92, 0],
        [0.20, -1.05, 0],
        [-0.72, -0.72, 0],
        [-1.55, -1.05, 0],
    ]
    return Polygon(*pts, stroke_color=color, stroke_width=1.5, fill_color="#20183A", fill_opacity=0.32)


def make_irregular_mesh_card(title, seed=501, point_count=34):
    field = make_scalar_field(width=4.65, height=2.35, nx=12, ny=7, opacity=0.26)
    mesh = make_irregular_mesh(width=4.65, height=2.25, seed=seed, point_count=point_count, color=INPUT)
    label = Chip("input samples: (x_i, a(x_i))", max_width=3.55, height=0.42, stroke_color=INPUT, font_size=16)
    body = VGroup(field, mesh, label)
    label.next_to(field, DOWN, buff=0.16)
    body.move_to(ORIGIN)
    card = PanelCard(title, body=body, width=5.45, height=3.45, accent_color=INPUT, title_font_size=23)
    card.mesh_outline = field[1]
    card.sample_dots = mesh[1]
    return card


def make_regular_grid_card(title, nx=7, ny=5):
    field = make_scalar_field(width=4.55, height=2.28, nx=12, ny=7, opacity=0.24)
    grid = make_regular_grid(width=4.55, height=2.28, nx=nx, ny=ny, color=OUTPUT)
    label = Chip("output function on another mesh", max_width=3.65, height=0.42, stroke_color=OUTPUT, font_size=16)
    body = VGroup(field, grid, label)
    label.next_to(field, DOWN, buff=0.16)
    card = PanelCard(title, body=body, width=5.45, height=3.45, accent_color=OUTPUT, title_font_size=23)
    card.mesh_outline = field[1]
    card.grid = grid
    return card


def make_sparse_sensor_card(title, seed=503):
    rng = np.random.default_rng(seed)
    boundary = make_complex_boundary()
    sensors = VGroup(
        *[
            Dot([rng.uniform(-1.95, 1.95), rng.uniform(-0.88, 0.88), 0], radius=0.052, color=WARNING)
            for _ in range(12)
        ]
    )
    label = Chip("sparse sensors + complex boundary", max_width=3.85, height=0.42, stroke_color=WARNING, font_size=15)
    label.next_to(boundary, DOWN, buff=0.18)
    body = VGroup(boundary, sensors, label)
    card = PanelCard(title, body=body, width=6.35, height=3.25, accent_color=WARNING, title_font_size=21)
    card.mesh_outline = boundary
    card.sensors = sensors
    return card


def make_dataset_cards():
    cards = VGroup(
        make_irregular_mesh_card("sample 1: irregular mesh", seed=501, point_count=30).scale(0.70),
        make_regular_grid_card("sample 2: regular grid", nx=6, ny=4).scale(0.70),
        make_sparse_sensor_card("sample 3: sparse sensors + complex boundary", seed=503).scale(0.70),
    ).arrange(RIGHT, buff=0.28)
    title = SafeText("one dataset, changing discretizations", max_width=8.2, max_height=0.46, font_size=31, color=TEXT, weight="BOLD")
    return VGroup(title, cards).arrange(DOWN, buff=0.34).move_to(ORIGIN)


def make_standard_nn_gate():
    box = RoundedRectangle(
        width=3.35,
        height=2.05,
        corner_radius=0.10,
        stroke_color=WARNING,
        stroke_width=1.8,
        fill_color="#2A1422",
        fill_opacity=0.88,
    )
    title = SafeText("standard NN", max_width=2.75, max_height=0.36, font_size=25, color=TEXT, weight="BOLD")
    tensor = SafeText("fixed tensor H x W x C", max_width=2.75, max_height=0.32, font_size=18, color=MUTED)
    slots = VGroup(*[Rectangle(width=0.42, height=0.42, stroke_color=GRID, stroke_width=1.0, fill_color=CARD_BG, fill_opacity=0.8) for _ in range(12)])
    slots.arrange_in_grid(rows=3, cols=4, buff=0.045)
    content = VGroup(title, tensor, slots).arrange(DOWN, buff=0.18).move_to(box)
    return VGroup(box, content)


def make_shape_mismatch_warning():
    cross = VGroup(
        Line(LEFT * 0.34 + DOWN * 0.34, RIGHT * 0.34 + UP * 0.34, color=WARNING, stroke_width=5.0),
        Line(LEFT * 0.34 + UP * 0.34, RIGHT * 0.34 + DOWN * 0.34, color=WARNING, stroke_width=5.0),
    )
    label = Chip("shape mismatch", max_width=2.70, height=0.52, stroke_color=WARNING, fill_color="#351321", font_size=22)
    return VGroup(cross, label).arrange(DOWN, buff=0.16)


def make_neural_operator_gate():
    box = RoundedRectangle(
        width=3.70,
        height=2.45,
        corner_radius=0.10,
        stroke_color=OPERATOR,
        stroke_width=1.8,
        fill_color="#211B32",
        fill_opacity=0.90,
    )
    title = SafeText("Neural Operator", max_width=3.05, max_height=0.38, font_size=25, color=OPERATOR, weight="BOLD")
    chips = VGroup(
        Chip("sample points x_i", max_width=2.72, height=0.42, stroke_color=INPUT, font_size=15),
        Chip("values a(x_i)", max_width=2.72, height=0.42, stroke_color=OUTPUT, font_size=15),
        Chip("query points y_j", max_width=2.72, height=0.42, stroke_color=PURPLE, font_size=15),
    ).arrange(DOWN, buff=0.10)
    content = VGroup(title, chips).arrange(DOWN, buff=0.18).move_to(box)
    return VGroup(box, content)


def make_query_points(layout="coarse", width=2.35, height=1.35):
    if layout == "coarse":
        xs = np.linspace(-width / 2, width / 2, 4)
        ys = np.linspace(-height / 2, height / 2, 3)
        points = [[x, y, 0] for x in xs for y in ys]
        label = "coarse grid"
        color = OUTPUT
    elif layout == "fine":
        xs = np.linspace(-width / 2, width / 2, 8)
        ys = np.linspace(-height / 2, height / 2, 5)
        points = [[x, y, 0] for x in xs for y in ys]
        label = "fine grid"
        color = SCIENCE
    else:
        rng = np.random.default_rng(511)
        points = [[rng.uniform(-width / 2, width / 2), rng.uniform(-height / 2, height / 2), 0] for _ in range(20)]
        label = "irregular points"
        color = PURPLE

    frame = RoundedRectangle(width=width + 0.25, height=height + 0.25, corner_radius=0.07, stroke_color=color, stroke_width=1.1, fill_color=CARD_BG, fill_opacity=0.36)
    dots = VGroup(*[Dot(point, radius=0.024 if layout == "fine" else 0.037, color=color) for point in points])
    chip = Chip(label, max_width=2.25, height=0.42, stroke_color=color, font_size=15)
    chip.next_to(frame, DOWN, buff=0.10)
    return VGroup(frame, dots, chip)


def make_continuum_focus():
    field = make_scalar_field(width=8.0, height=4.0, nx=20, ny=11, opacity=0.52)
    irregular = make_irregular_mesh(width=7.75, height=3.70, seed=521, point_count=34, color=INPUT).set_opacity(0.20)
    regular = make_regular_grid(width=7.75, height=3.70, nx=9, ny=5, color=OUTPUT).set_opacity(0.16)
    title = SafeText("same underlying function, different discretizations", max_width=9.2, max_height=0.52, font_size=34, color=TEXT, weight="BOLD")
    title.next_to(field, UP, buff=0.28)
    return VGroup(field, irregular, regular, title).move_to(ORIGIN)


def make_neural_operator_view():
    input_card = make_irregular_mesh_card("observed input", seed=531, point_count=30).scale(0.70)
    gate = make_neural_operator_gate()
    outputs = VGroup(
        make_query_points("coarse").scale(0.82),
        make_query_points("fine").scale(0.82),
        make_query_points("irregular").scale(0.82),
    ).arrange(DOWN, buff=0.20)
    row = VGroup(input_card, gate, outputs).arrange(RIGHT, buff=0.62)
    arrows = VGroup(
        Arrow(input_card.get_right() + RIGHT * 0.05, gate.get_left() + LEFT * 0.05, buff=0, color=MUTED, stroke_width=1.8),
        Arrow(gate.get_right() + RIGHT * 0.05, outputs.get_left() + LEFT * 0.05, buff=0, color=OUTPUT, stroke_width=2.0),
    )
    title = SafeText("same operator block, new query layout", max_width=8.4, max_height=0.46, font_size=31, color=TEXT, weight="BOLD")
    view = VGroup(title, VGroup(arrows, row)).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    view.gate = gate
    view.outputs = outputs
    return view


def make_integral_view():
    fixed = VGroup(
        SafeText("fixed tensor index", max_width=2.65, max_height=0.32, font_size=20, color=MUTED, weight="BOLD"),
        SafeMathTex(r"W_{ij}v_j", max_width=1.8, max_height=0.45, font_size=32, color=MUTED),
        make_mesh_overlay(width=2.20, height=1.20, nx=5, ny=3, color=MUTED),
    ).arrange(DOWN, buff=0.18)
    fixed.set_opacity(0.34)

    samples = VGroup(
        Chip("sample/query/weights", max_width=3.25, height=0.46, stroke_color=OPERATOR, font_size=18),
        SafeMathTex(r"\sum_i \kappa(y, x_i)a(x_i)\Delta x_i", max_width=5.70, max_height=0.58, font_size=35, color=TEXT),
        Arrow(LEFT * 1.45, RIGHT * 1.45, color=OPERATOR, stroke_width=2.3),
        SafeMathTex(r"\int \kappa(y,x)a(x)\,dx", max_width=4.40, max_height=0.58, font_size=36, color=OPERATOR),
    ).arrange(DOWN, buff=0.28)

    lens = Circle(radius=0.56, color=OPERATOR, stroke_width=2.0, fill_color="#2B2142", fill_opacity=0.52)
    dots = VGroup(*[Dot([np.cos(t) * 0.42, np.sin(t) * 0.28, 0], radius=0.035, color=INPUT) for t in np.linspace(0, TAU, 10, endpoint=False)])
    query = Dot(RIGHT * 0.95, radius=0.060, color=PURPLE)
    weights = VGroup(*[Line(dot.get_center(), query.get_center(), color=OPERATOR, stroke_width=0.8, stroke_opacity=0.35) for dot in dots])
    diagram = VGroup(weights, lens, dots, query)
    diagram.next_to(samples, RIGHT, buff=0.72)

    view = VGroup(fixed, samples, diagram).arrange(RIGHT, buff=0.80).move_to(ORIGIN)
    view.fixed = fixed
    view.samples = samples
    view.diagram = diagram
    return view


class Scene0501DifferentMeshes(TimedScene):
    SCRIPT_ID = "5.1"
    SCRIPT_TITLE = "Input and output may live on different meshes"
    SCRIPT_START = 29 * 60 + 10
    SCRIPT_END = 31 * 60 + 20
    SCENE_DURATION = 130.0

    KEYFRAMES = (
        "KF01 0.0s hidden continuum with irregular input samples",
        "KF02 12.0s output function stored on different regular grid",
        "KF03 23.5s three data samples with mismatched layouts",
        "KF04 37.0s standard NN rejects fixed tensor shape mismatch",
        "KF05 50.0s same underlying function, different discretizations",
        "KF06 66.5s neural operator accepts samples and query points",
        "KF07 85.0s integral-like aggregation replaces fixed indices",
    )

    def construct(self):
        background = make_background_network(seed=501, n=76, dot_opacity=0.11, line_opacity=0.08)
        self.add(background)

        input_card = make_irregular_mesh_card("input function measured on a mesh", seed=501, point_count=38)
        input_card.move_to(ORIGIN)
        assert_in_frame(input_card, margin=0.35, label="input_card")
        self.add(input_card)

        # VO exact: Bây giờ hãy nhìn dữ liệu thật trong scientific computing. Input function có thể được đo trên một mesh.
        # Global 29:10.0-29:22.0 => 29:10.0 -> local 0.0, 29:22.0 -> local 12.0
        self.play_timed(
            "irregular_input_samples_over_hidden_continuum",
            0.0,
            12.0,
            LaggedStart(*[Flash(dot, color=OUTPUT, flash_radius=0.16) for dot in input_card.sample_dots[::5]], lag_ratio=0.12),
        )

        output_card = make_regular_grid_card("output stored on different mesh", nx=7, ny=5)
        row = VGroup(input_card.copy().scale(0.86), output_card.scale(0.86)).arrange(RIGHT, buff=1.38)
        arrow = Arrow(row[0].get_right() + RIGHT * 0.08, row[1].get_left() + LEFT * 0.08, buff=0, color=OPERATOR, stroke_width=2.4)
        arrow_label = Chip("same physical sample", max_width=2.65, height=0.42, stroke_color=OPERATOR, font_size=16)
        arrow_label.next_to(arrow, UP, buff=0.16)
        input_output_view = VGroup(row, arrow, arrow_label).move_to(ORIGIN)
        assert_in_frame(input_output_view, margin=0.35, label="input_output_view")

        # VO exact: Output function có thể được lưu trên một mesh khác. Sample tiếp theo lại dùng một resolution khác nữa.
        # Global 29:22.0-29:33.5 => 29:22.0 -> local 12.0, 29:33.5 -> local 23.5
        self.play_timed(
            "different_output_mesh_regular_grid",
            12.0,
            23.5,
            Transform(input_card, row[0]),
            FadeIn(row[1], shift=LEFT * 0.08),
            GrowArrow(arrow),
            FadeIn(arrow_label, shift=UP * 0.06),
        )

        dataset_view = make_dataset_cards()
        assert_in_frame(dataset_view, margin=0.35, label="dataset_view")

        # VO exact: Có dữ liệu trên regular grid, có dữ liệu trên irregular mesh, có sensor sparse, có boundary phức tạp.
        # Global 29:33.5-29:46.0 => 29:33.5 -> local 23.5, 29:46.0 -> local 36.0
        self.play_timed(
            "three_samples_show_mismatched_layouts",
            23.5,
            36.0,
            FadeOut(VGroup(input_card, row[1], arrow, arrow_label), shift=UP * 0.08),
            FadeIn(dataset_view[0], shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in dataset_view[1]], lag_ratio=0.14),
        )

        pulse_targets = VGroup(*[card.mesh_outline for card in dataset_view[1]])
        # VO exact: Pause: 1.0s.
        # Global 29:46.0-29:47.0 => 29:46.0 -> local 36.0, 29:47.0 -> local 37.0
        self.play_timed(
            "pause_with_subtle_mesh_pulse",
            36.0,
            36.8,
            LaggedStart(*[Indicate(target, color=OPERATOR, scale_factor=1.02) for target in pulse_targets], lag_ratio=0.08),
        )
        self.wait_timed("hold_after_subtle_mesh_pulse", 36.8, 37.0)

        small_cards = dataset_view[1].copy().scale(0.64).arrange(DOWN, buff=0.16)
        gate = make_standard_nn_gate()
        warning = make_shape_mismatch_warning()
        reject_row = VGroup(small_cards, gate, warning).arrange(RIGHT, buff=0.65).move_to(ORIGIN)
        reject_arrows = VGroup(
            Arrow(small_cards.get_right() + RIGHT * 0.08, gate.get_left() + LEFT * 0.08, buff=0, color=MUTED, stroke_width=1.8),
            Arrow(gate.get_right() + RIGHT * 0.08, warning.get_left() + LEFT * 0.08, buff=0, color=WARNING, stroke_width=2.2),
        )
        reject_view = VGroup(reject_arrows, reject_row)
        assert_in_frame(reject_view, margin=0.35, label="reject_view")

        # VO exact: Nếu model buộc input và output phải là tensor cùng shape cố định, ta đã tự khóa mình vào một setup quá hẹp.
        # Global 29:47.0-30:00.0 => 29:47.0 -> local 37.0, 30:00.0 -> local 50.0
        self.play_timed(
            "standard_nn_rejects_shape_mismatch",
            37.0,
            50.0,
            FadeOut(dataset_view, shift=UP * 0.08),
            FadeIn(small_cards, shift=RIGHT * 0.08),
            FadeIn(gate, shift=LEFT * 0.08),
            GrowArrow(reject_arrows[0]),
            GrowArrow(reject_arrows[1]),
            FadeIn(warning, scale=0.92),
        )

        continuum = make_continuum_focus()
        assert_in_frame(continuum, margin=0.35, label="continuum_focus")

        # VO exact: Trong khi đó, bài toán vật lý thật không quan tâm ta lưu nó bằng grid nào. Nó tồn tại ở continuum level.
        # Global 30:00.0-30:16.5 => 30:00.0 -> local 50.0, 30:16.5 -> local 66.5
        self.play_timed(
            "fade_mesh_layers_emphasize_same_continuum",
            50.0,
            66.5,
            FadeOut(reject_view, shift=UP * 0.10),
            FadeIn(continuum[0], shift=DOWN * 0.08),
            FadeIn(continuum[1], shift=RIGHT * 0.04),
            FadeIn(continuum[2], shift=LEFT * 0.04),
            FadeIn(continuum[3], shift=UP * 0.06),
        )

        operator_view = make_neural_operator_view()
        assert_in_frame(operator_view, margin=0.35, label="operator_view")

        # VO exact: Neural operator cố gắng làm điều ngược lại với resizing hack: nó định nghĩa computation sao cho có ý nghĩa khi mesh thay đổi.
        # Global 30:16.5-30:35.0 => 30:16.5 -> local 66.5, 30:35.0 -> local 85.0
        self.play_timed(
            "neural_operator_accepts_samples_values_and_queries",
            66.5,
            85.0,
            FadeOut(continuum, shift=UP * 0.10),
            FadeIn(operator_view[0], shift=DOWN * 0.06),
            FadeIn(operator_view[1], shift=UP * 0.08),
            LaggedStart(*[Flash(output[1], color=OPERATOR, flash_radius=0.10) for output in operator_view.outputs], lag_ratio=0.24),
        )

        integral_view = make_integral_view()
        assert_in_frame(integral_view, margin=0.35, label="integral_view")

        # VO exact: Đây là lý do ta cần các operation giống tích phân hơn là chỉ matrix multiplication trên index cố định.
        # Global 30:35.0-30:50.0 => 30:35.0 -> local 85.0, 30:50.0 -> local 100.0
        self.play_timed(
            "integral_like_sum_replaces_fixed_tensor_index",
            85.0,
            100.0,
            FadeOut(operator_view, shift=UP * 0.10),
            FadeIn(integral_view.fixed, shift=RIGHT * 0.08),
            FadeIn(integral_view.samples[0], shift=DOWN * 0.06),
            Write(integral_view.samples[1]),
            FadeIn(integral_view.diagram, scale=0.96),
        )

        # Global 30:50.0-31:03.0 => local 100.0-113.0
        self.play_timed(
            "riemann_sum_points_toward_integral",
            100.0,
            113.0,
            GrowArrow(integral_view.samples[2]),
            Write(integral_view.samples[3]),
            Circumscribe(integral_view.diagram, color=OPERATOR, buff=0.10),
        )

        glow_targets = VGroup(integral_view.samples, integral_view.diagram)
        # Global 31:03.0-31:20.0 => 31:03.0 -> local 113.0, 31:20.0 -> local 130.0
        self.play_timed(
            "end_with_sample_query_weights_glowing",
            113.0,
            130.0,
            integral_view.fixed.animate.set_opacity(0.18),
            Indicate(glow_targets, color=OPERATOR, scale_factor=1.03),
        )

        self.pad_to(self.SCENE_DURATION)
