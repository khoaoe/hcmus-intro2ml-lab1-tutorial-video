"""
Scene 4.2 - Operator learning is not just supervised learning with bigger tensors
Script: ../docs/full_voice_manim_script.md
Global time: 25:00.0-27:05.0
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
    BG,
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


def _function_value(x):
    return 0.42 * np.sin(1.7 * TAU * x + 0.25) + 0.16 * np.cos(4.1 * TAU * x - 0.4)


def _curve_points(width=3.4, height=1.45, n=80):
    xs = np.linspace(0.0, 1.0, n)
    return [[-width / 2 + width * x, height * _function_value(x), 0] for x in xs]


def make_tensor_block(label, cells=5, width=1.55, height=1.55, color=INPUT):
    cell_w = width / cells
    cell_h = height / cells
    grid = VGroup()
    for r in range(cells):
        for c in range(cells):
            value = 0.5 + 0.5 * np.sin(0.7 * r + 1.1 * c)
            grid.add(
                Rectangle(
                    width=cell_w,
                    height=cell_h,
                    stroke_color=BG,
                    stroke_width=0.35,
                    fill_color=color if value > 0.5 else SCIENCE,
                    fill_opacity=0.24 + 0.30 * value,
                ).move_to(
                    [
                        -width / 2 + cell_w / 2 + c * cell_w,
                        height / 2 - cell_h / 2 - r * cell_h,
                        0,
                    ]
                )
            )
    frame = RoundedRectangle(
        width=width + 0.12,
        height=height + 0.12,
        corner_radius=0.07,
        stroke_color=color,
        stroke_width=1.2,
        fill_color=CARD_BG,
        fill_opacity=0.42,
    )
    text = SafeText(label, max_width=width + 0.10, max_height=0.28, font_size=17, color=TEXT)
    text.next_to(frame, DOWN, buff=0.10)
    return VGroup(frame, grid, text)


def make_cracked_tensor():
    block = make_tensor_block("128x128 tensor", cells=7, width=2.05, height=2.05, color=WARNING)
    crack = VGroup(
        Line([-0.20, 1.02, 0], [-0.04, 0.47, 0], color=WARNING, stroke_width=3.4),
        Line([-0.04, 0.47, 0], [-0.28, 0.12, 0], color=WARNING, stroke_width=3.2),
        Line([-0.28, 0.12, 0], [0.06, -0.34, 0], color=WARNING, stroke_width=3.1),
        Line([0.06, -0.34, 0], [-0.08, -1.03, 0], color=WARNING, stroke_width=3.0),
        Line([-0.04, 0.47, 0], [0.40, 0.20, 0], color=WARNING, stroke_width=2.4),
        Line([0.06, -0.34, 0], [0.48, -0.60, 0], color=WARNING, stroke_width=2.2),
    )
    warning = Chip("bigger tensor != operator learning", max_width=4.25, height=0.48, stroke_color=WARNING, font_size=17)
    warning.next_to(block, DOWN, buff=0.34)
    return VGroup(block, crack, warning)


def make_sampled_curve(sample_count, label, width=3.28, height=1.20, color=INPUT, show_label=True):
    curve = smooth_path(_curve_points(width=width, height=height, n=100), color=color, stroke_width=2.5)
    xs = np.linspace(0.0, 1.0, sample_count)
    dots = VGroup(
        *[
            Dot(
                [-width / 2 + width * x, height * _function_value(x), 0],
                radius=0.035 if sample_count < 64 else 0.020,
                color=OUTPUT,
            )
            for x in xs
        ]
    )
    axis = Line([-width / 2, -height * 0.54, 0], [width / 2, -height * 0.54, 0], color=GRID, stroke_width=1.0)
    group = VGroup(axis, curve, dots)
    if show_label:
        title = SafeText(label, max_width=2.15, max_height=0.30, font_size=19, color=TEXT, weight="BOLD")
        title.next_to(curve, UP, buff=0.16)
        group.add(title)
    group.dots = dots
    group.curve = curve
    return group


def make_resolution_strip():
    panels = VGroup()
    for n, label in ((8, "8 samples"), (16, "16 samples"), (64, "64 samples")):
        sampled = make_sampled_curve(n, label, show_label=False)
        card = PanelCard(label, body=sampled, width=4.35, height=2.35, accent_color=INPUT, title_font_size=22)
        panels.add(card)
    panels.arrange(RIGHT, buff=0.40)
    title = SafeText("same function, different discretizations", max_width=7.8, max_height=0.45, font_size=31, color=TEXT, weight="BOLD")
    subtitle = SafeText("continuous curve stays stable; sample dots change", max_width=7.3, max_height=0.34, font_size=20, color=MUTED)
    view = VGroup(title, panels, subtitle).arrange(DOWN, buff=0.30).move_to(ORIGIN)
    return view


def make_domain_icon_sphere():
    sphere = Circle(radius=0.54, stroke_color=SCIENCE, stroke_width=1.6, fill_color="#0A3142", fill_opacity=0.74)
    lats = VGroup(*[Ellipse(width=1.02, height=0.18, stroke_color=GRID, stroke_width=0.8).shift(UP * y) for y in (-0.25, 0, 0.25)])
    longs = VGroup(*[Ellipse(width=w, height=1.08, stroke_color=GRID, stroke_width=0.8) for w in (0.30, 0.62)])
    return VGroup(sphere, lats, longs)


def make_domain_icon_car_mesh():
    body = Polygon(
        [-0.68, -0.12, 0],
        [-0.42, 0.22, 0],
        [0.28, 0.24, 0],
        [0.68, -0.04, 0],
        [0.54, -0.22, 0],
        [-0.68, -0.22, 0],
        stroke_color=TEXT,
        stroke_width=1.2,
        fill_color=CARD_BG,
        fill_opacity=0.92,
    )
    mesh = VGroup()
    for x in np.linspace(-0.55, 0.45, 5):
        mesh.add(Line([x, -0.20, 0], [x + 0.10, 0.16, 0], color=INPUT, stroke_width=0.8, stroke_opacity=0.65))
    for y in np.linspace(-0.16, 0.12, 4):
        mesh.add(Line([-0.54, y, 0], [0.52, y + 0.05, 0], color=INPUT, stroke_width=0.8, stroke_opacity=0.65))
    wheels = VGroup(Dot(LEFT * 0.36 + DOWN * 0.22, radius=0.06, color=MUTED), Dot(RIGHT * 0.38 + DOWN * 0.22, radius=0.06, color=MUTED))
    return VGroup(body, mesh, wheels)


def make_domain_icon_volume():
    front = Rectangle(width=0.86, height=0.70, stroke_color=PURPLE, stroke_width=1.3, fill_color="#20183A", fill_opacity=0.55)
    back = front.copy().shift(RIGHT * 0.32 + UP * 0.22).set_stroke(opacity=0.72)
    edges = VGroup(
        Line(front.get_corner(UL), back.get_corner(UL), color=PURPLE, stroke_width=1.1),
        Line(front.get_corner(UR), back.get_corner(UR), color=PURPLE, stroke_width=1.1),
        Line(front.get_corner(DL), back.get_corner(DL), color=PURPLE, stroke_width=1.1),
        Line(front.get_corner(DR), back.get_corner(DR), color=PURPLE, stroke_width=1.1),
    )
    slices = VGroup(*[Rectangle(width=0.70, height=0.48, stroke_color=GRID, stroke_width=0.7).shift(RIGHT * 0.07 * i + UP * 0.05 * i) for i in range(3)])
    return VGroup(back, front, edges, slices)


def make_continuum_operator_panel():
    left = make_sampled_curve(10, r"a(x)", width=2.9, height=0.95, color=INPUT)
    right = make_sampled_curve(18, r"u(y)", width=2.9, height=0.95, color=OUTPUT)
    operator_box = RoundedRectangle(
        width=2.45,
        height=1.42,
        corner_radius=0.10,
        stroke_color=OPERATOR,
        stroke_width=1.6,
        fill_color="#211B32",
        fill_opacity=0.86,
    )
    formula = SafeMathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}", max_width=2.14, max_height=0.48, font_size=34, color=OPERATOR)
    caption = SafeText("same operator", max_width=1.8, max_height=0.24, font_size=16, color=MUTED)
    VGroup(formula, caption).arrange(DOWN, buff=0.08).move_to(operator_box)
    operator = VGroup(operator_box, formula, caption)
    row = VGroup(left, operator, right).arrange(RIGHT, buff=0.55)
    arrows = VGroup(
        Arrow(left.get_right() + RIGHT * 0.10, operator.get_left() + LEFT * 0.10, buff=0, color=MUTED, stroke_width=1.8),
        Arrow(operator.get_right() + RIGHT * 0.10, right.get_left() + LEFT * 0.10, buff=0, color=OUTPUT, stroke_width=2.0),
    )
    title = SafeText("continuum problem at center", max_width=5.9, max_height=0.43, font_size=30, color=TEXT, weight="BOLD")
    note = Chip("discretization = observation", max_width=3.65, height=0.46, stroke_color=SCIENCE, font_size=17)
    panel = VGroup(title, VGroup(arrows, row), note).arrange(DOWN, buff=0.36).move_to(ORIGIN)
    panel.operator = operator
    panel.left = left
    panel.right = right
    panel.arrows = arrows
    panel.row = row
    return panel


class TensorBlock(VGroup):
    def __init__(self, label="64x64 tensor", **kwargs):
        super().__init__(**kwargs)
        self.add(make_tensor_block(label, cells=6, width=1.85, height=1.85, color=INPUT))


class CrackAnimation(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_cracked_tensor())


class SampledFunction(VGroup):
    def __init__(self, sample_count=16, label="16 samples", **kwargs):
        super().__init__(**kwargs)
        self.add(make_sampled_curve(sample_count, label))


class ContinuumOperator(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(make_continuum_operator_panel())


def make_misconception_view():
    title = SafeText("Misconception", max_width=4.2, max_height=0.55, font_size=38, color=TEXT, weight="BOLD")
    blocks = VGroup(
        make_tensor_block("32x32", cells=4, width=1.35, height=1.35, color=INPUT),
        make_tensor_block("64x64", cells=6, width=1.65, height=1.65, color=INPUT),
        make_cracked_tensor(),
    ).arrange(RIGHT, buff=0.70)
    arrows = VGroup(
        Arrow(blocks[0].get_right() + RIGHT * 0.12, blocks[1].get_left() + LEFT * 0.12, buff=0, color=MUTED, stroke_width=1.5),
        Arrow(blocks[1].get_right() + RIGHT * 0.12, blocks[2].get_left() + LEFT * 0.12, buff=0, color=MUTED, stroke_width=1.5),
    )
    label = Chip("Not just bigger tensors", max_width=3.45, height=0.48, stroke_color=WARNING, font_size=19)
    view = VGroup(title, VGroup(arrows, blocks), label).arrange(DOWN, buff=0.40).move_to(ORIGIN)
    return view


def make_discretization_shift_view():
    coarse = VGroup(make_mesh_overlay(width=1.70, height=1.05, nx=4, ny=3, color=INPUT), Chip("coarse train mesh", max_width=2.35, height=0.40, stroke_color=INPUT, font_size=15)).arrange(DOWN, buff=0.18)
    fine = VGroup(make_mesh_overlay(width=1.70, height=1.05, nx=9, ny=6, color=OUTPUT), Chip("fine test mesh", max_width=2.05, height=0.40, stroke_color=OUTPUT, font_size=15)).arrange(DOWN, buff=0.18)
    mesh_pair = VGroup(coarse, fine).arrange(RIGHT, buff=1.05)
    mesh_arrow = Arrow(coarse.get_right() + RIGHT * 0.14, fine.get_left() + LEFT * 0.14, buff=0, color=MUTED, stroke_width=1.6)
    mesh_panel = PanelCard("mesh shift", body=VGroup(mesh_pair, mesh_arrow), width=4.65, height=2.35, accent_color=INPUT, title_font_size=22)

    rng = np.random.default_rng(42)
    sensors = VGroup(*[Dot([rng.uniform(-0.78, 0.78), rng.uniform(-0.44, 0.44), 0], radius=0.040, color=WARNING) for _ in range(15)])
    queries = VGroup(*[Dot([x, y, 0], radius=0.029, color=OUTPUT) for x in np.linspace(-0.70, 0.70, 6) for y in np.linspace(-0.38, 0.38, 4)])
    sensor_panel = PanelCard(
        "sensor/query shift",
        body=VGroup(
            VGroup(sensors, Chip("irregular sensors", max_width=2.35, height=0.38, stroke_color=WARNING, font_size=14)).arrange(DOWN, buff=0.18),
            Arrow(LEFT * 0.35, RIGHT * 0.35, color=MUTED, stroke_width=1.4),
            VGroup(queries, Chip("regular query points", max_width=2.55, height=0.38, stroke_color=OUTPUT, font_size=14)).arrange(DOWN, buff=0.18),
        ).arrange(RIGHT, buff=0.28),
        width=4.85,
        height=2.35,
        accent_color=WARNING,
        title_font_size=22,
    )

    domain_icons = VGroup(
        VGroup(make_domain_icon_sphere(), SafeText("sphere", max_width=1.2, max_height=0.25, font_size=16, color=TEXT)).arrange(DOWN, buff=0.16),
        VGroup(make_domain_icon_car_mesh(), SafeText("car surface mesh", max_width=2.2, max_height=0.25, font_size=15, color=TEXT)).arrange(DOWN, buff=0.16),
        VGroup(make_domain_icon_volume(), SafeText("3D volume", max_width=1.5, max_height=0.25, font_size=16, color=TEXT)).arrange(DOWN, buff=0.16),
    ).arrange(RIGHT, buff=0.38)
    domain_panel = PanelCard("domain shift", body=domain_icons, width=5.15, height=2.35, accent_color=PURPLE, title_font_size=22)
    title = SafeText("discretization can change", max_width=6.2, max_height=0.45, font_size=31, color=TEXT, weight="BOLD")
    view = VGroup(title, VGroup(mesh_panel, sensor_panel, domain_panel).arrange_in_grid(rows=2, cols=2, buff=0.42)).arrange(DOWN, buff=0.34).move_to(ORIGIN)
    return view


def make_fixed_grid_cnn_view():
    grid = make_tensor_block("fixed grid", cells=7, width=1.85, height=1.85, color=INPUT)
    cnn = RoundedRectangle(width=2.35, height=1.35, corner_radius=0.10, stroke_color=WARNING, stroke_width=1.5, fill_color="#2A1826", fill_opacity=0.82)
    cnn_label = SafeText("fixed-grid CNN", max_width=2.0, max_height=0.30, font_size=21, color=TEXT, weight="BOLD").move_to(cnn.get_center() + UP * 0.20)
    assumption = SafeText("grid assumption", max_width=1.85, max_height=0.25, font_size=16, color=MUTED).move_to(cnn.get_center() + DOWN * 0.22)
    resized = make_tensor_block("resized input", cells=6, width=1.60, height=1.60, color=SCIENCE)
    row = VGroup(grid, Arrow(LEFT * 0.40, RIGHT * 0.40, color=MUTED, stroke_width=1.5), VGroup(cnn, cnn_label, assumption), Arrow(LEFT * 0.40, RIGHT * 0.40, color=MUTED, stroke_width=1.5), resized).arrange(RIGHT, buff=0.38)
    continuum_warning_text = "does not guarantee same continuum operator"
    warning = PanelCard(
        "warning",
        body=VGroup(
            SafeText("resize can run", max_width=2.8, max_height=0.30, font_size=19, color=SCIENCE, weight="BOLD"),
            VGroup(
                SafeText(continuum_warning_text.replace(" same continuum operator", ""), max_width=3.8, max_height=0.28, font_size=18, color=TEXT),
                SafeText("same continuum operator", max_width=4.25, max_height=0.28, font_size=18, color=WARNING),
            ).arrange(DOWN, buff=0.05),
        ).arrange(DOWN, buff=0.16),
        width=5.75,
        height=1.85,
        accent_color=WARNING,
        title_font_size=22,
    )
    note = SafeText("fixed-grid CNN is a limited abstraction, not useless", max_width=6.8, max_height=0.34, font_size=20, color=MUTED)
    title = SafeText("code can run; concept may not transfer", max_width=7.2, max_height=0.45, font_size=31, color=TEXT, weight="BOLD")
    return VGroup(title, row, warning, note).arrange(DOWN, buff=0.34).move_to(ORIGIN)


def make_final_relation_view():
    table = PanelCard(
        "table on this grid",
        body=make_tensor_block("numbers", cells=5, width=1.45, height=1.00, color=WARNING),
        width=3.15,
        height=2.20,
        accent_color=WARNING,
        title_font_size=21,
    )
    cross = VGroup(
        Line(table.get_corner(UL) + DR * 0.18, table.get_corner(DR) + UL * 0.18, color=WARNING, stroke_width=4.0),
        Line(table.get_corner(DL) + UR * 0.18, table.get_corner(UR) + DL * 0.18, color=WARNING, stroke_width=4.0),
    )
    relation = PanelCard(
        "relation between functions",
        body=make_continuum_operator_panel().scale(0.72),
        width=7.30,
        height=3.25,
        accent_color=OPERATOR,
        title_font_size=25,
    )
    shadows = VGroup(
        make_tensor_block("sample 1", cells=3, width=0.92, height=0.62, color=INPUT),
        make_tensor_block("sample 2", cells=4, width=1.06, height=0.70, color=SCIENCE),
        make_tensor_block("sample 3", cells=5, width=1.20, height=0.78, color=OUTPUT),
    ).arrange(RIGHT, buff=0.28)
    obs = VGroup(shadows, SafeText("sampled tables are observations", max_width=4.6, max_height=0.30, font_size=18, color=MUTED)).arrange(DOWN, buff=0.12)
    title = SafeText("philosophy: learn functions, not one table", max_width=8.2, max_height=0.46, font_size=31, color=TEXT, weight="BOLD")
    body = VGroup(VGroup(table, cross), relation).arrange(RIGHT, buff=0.65)
    return VGroup(title, body, obs).arrange(DOWN, buff=0.34).move_to(ORIGIN)


class Scene0402OperatorLearningNotBiggerTensors(TimedScene):
    SCRIPT_ID = "4.2"
    SCRIPT_TITLE = "Operator learning is not just supervised learning with bigger tensors"
    SCRIPT_START = 25 * 60
    SCRIPT_END = 27 * 60 + 5
    SCENE_DURATION = 125.0

    KEYFRAMES = (
        "KF01 0.0s misconception tensor grows and cracks",
        "KF02 13.0s Not quite",
        "KF03 22.5s same function sampled at 8/16/64",
        "KF04 36.0s discretization shift examples",
        "KF05 49.5s fixed-grid CNN warning",
        "KF06 62.0s continuum operator stays stable",
        "KF07 78.5s final relation between functions",
    )

    def construct(self):
        background = make_background_network(seed=402, n=76, dot_opacity=0.13, line_opacity=0.10)
        self.add(background)

        misconception = make_misconception_view()
        assert_in_frame(misconception, margin=0.35, label="misconception")

        # Global 25:00.0-25:12.0 => local 0.0-12.0
        self.play_timed(
            "misconception_bigger_tensor_cracks",
            0.0,
            12.0,
            FadeIn(misconception[0], shift=DOWN * 0.08),
            FadeIn(misconception[1], lag_ratio=0.10),
            FadeIn(misconception[2], shift=UP * 0.08),
        )

        # Global 25:12.0-25:13.0 => local 12.0-13.0
        self.wait_timed("pause_after_misconception", 12.0, 13.0)

        not_quite = SafeText("Not quite.", max_width=4.2, max_height=0.68, font_size=48, color=WARNING, weight="BOLD").move_to(ORIGIN)
        assert_in_frame(not_quite, margin=0.35, label="not_quite")

        # Global 25:13.0-25:22.5 => local 13.0-22.5
        self.play_timed(
            "not_quite_reframe",
            13.0,
            22.5,
            FadeOut(misconception, shift=UP * 0.10),
            FadeIn(not_quite, shift=DOWN * 0.10),
        )

        resolution_strip = make_resolution_strip()
        assert_in_frame(resolution_strip, margin=0.32, label="resolution_strip")

        # Global 25:22.5-25:36.0 => local 22.5-36.0
        self.play_timed(
            "same_function_many_discretizations",
            22.5,
            36.0,
            FadeOut(not_quite, shift=UP * 0.10),
            FadeIn(resolution_strip[0], shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(panel, shift=UP * 0.08) for panel in resolution_strip[1]], lag_ratio=0.12),
            FadeIn(resolution_strip[2], shift=UP * 0.08),
        )

        shift_view = make_discretization_shift_view()
        assert_in_frame(shift_view, margin=0.32, label="shift_view")

        # Global 25:36.0-25:49.5 => local 36.0-49.5
        self.play_timed(
            "train_test_sensor_domain_shift",
            36.0,
            49.5,
            FadeOut(resolution_strip, shift=UP * 0.10),
            FadeIn(shift_view[0], shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(panel, shift=UP * 0.08) for panel in shift_view[1]], lag_ratio=0.10),
        )

        cnn_view = make_fixed_grid_cnn_view()
        assert_in_frame(cnn_view, margin=0.34, label="cnn_view")

        # Global 25:49.5-26:02.0 => local 49.5-62.0
        self.play_timed(
            "fixed_grid_cnn_warning",
            49.5,
            62.0,
            FadeOut(shift_view, shift=UP * 0.10),
            FadeIn(cnn_view[0], shift=DOWN * 0.08),
            FadeIn(cnn_view[1], shift=UP * 0.08),
            FadeIn(cnn_view[2], shift=UP * 0.08),
            FadeIn(cnn_view[3], shift=UP * 0.08),
        )

        continuum = make_continuum_operator_panel()
        assert_in_frame(continuum, margin=0.34, label="continuum")

        # Global 26:02.0-26:04.0 => local 62.0-64.0
        self.play_timed(
            "clear_fixed_grid_cnn",
            62.0,
            64.0,
            FadeOut(cnn_view, shift=UP * 0.10),
        )

        # Global 26:04.0-26:09.5 => local 64.0-69.5
        self.play_timed(
            "continuum_problem_objects",
            64.0,
            69.5,
            FadeIn(continuum[0], shift=DOWN * 0.08),
            FadeIn(continuum.left, shift=RIGHT * 0.08),
            FadeIn(continuum.operator, shift=UP * 0.08),
            FadeIn(continuum.right, shift=LEFT * 0.08),
        )

        # Global 26:09.5-26:18.5 => local 69.5-78.5
        self.play_timed(
            "continuum_problem_arrows_and_observation",
            69.5,
            78.5,
            FadeIn(continuum.arrows),
            FadeIn(continuum[2], shift=UP * 0.08),
        )

        final_relation = make_final_relation_view()
        assert_in_frame(final_relation, margin=0.35, label="final_relation")

        # Global 26:18.5-26:36.0 => local 78.5-96.0
        self.play_timed(
            "cross_out_table_on_this_grid",
            78.5,
            96.0,
            FadeOut(continuum, shift=UP * 0.10),
            FadeIn(final_relation[0], shift=DOWN * 0.08),
            FadeIn(final_relation[1][0], shift=RIGHT * 0.08),
        )

        # Global 26:36.0-26:52.0 => local 96.0-112.0
        self.play_timed(
            "emphasize_relation_between_functions",
            96.0,
            112.0,
            FadeIn(final_relation[1][1], shift=LEFT * 0.10),
            Indicate(final_relation[1][1], color=OPERATOR, scale_factor=1.02),
        )

        # Global 26:52.0-27:05.0 => local 112.0-125.0
        self.play_timed(
            "sampled_tables_are_observations",
            112.0,
            125.0,
            FadeIn(final_relation[2], shift=UP * 0.08),
            final_relation[1][1].animate.set_opacity(1.0),
        )
        self.pad_to(self.SCENE_DURATION)
