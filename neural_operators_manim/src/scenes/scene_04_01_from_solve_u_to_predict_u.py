"""
Scene 4.1 - From "solve u" to "predict u"
Script: ../docs/full_voice_manim_script.md
Global time: 23:20.0-25:00.0
Local duration: 100.0s
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


LEFT_CENTER = LEFT * 3.86 + DOWN * 0.08
RIGHT_CENTER = RIGHT * 3.86 + DOWN * 0.08


def make_function_panel(symbol, accent, seed, width=1.62, height=1.06, title=None):
    rng = np.random.default_rng(seed)
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.07,
        stroke_color=accent,
        stroke_width=1.15,
        fill_color=CARD_BG,
        fill_opacity=0.70,
    )
    xs = np.linspace(-width * 0.36, width * 0.36, 8)
    phase = rng.uniform(0.0, np.pi)
    amp = rng.uniform(0.16, 0.25)
    points = [
        [x, amp * np.sin(4.2 * x + phase) + 0.06 * np.cos(7.0 * x - phase), 0]
        for x in xs
    ]
    curve = smooth_path(points, color=accent, stroke_width=2.4)
    mesh = make_mesh_overlay(width=width * 0.72, height=height * 0.44, nx=5, ny=3, color=GRID)
    body = VGroup(mesh, curve).move_to(box.get_center() + DOWN * 0.05)
    label = SafeMathTex(symbol, max_width=width * 0.65, max_height=0.26, font_size=23, color=accent)
    label.move_to(box.get_top() + DOWN * 0.18)
    parts = [box, body, label]
    if title:
        title_mob = SafeText(title, max_width=width - 0.18, max_height=0.20, font_size=12, min_font_size=10, color=MUTED)
        title_mob.move_to(box.get_bottom() + UP * 0.14)
        parts.append(title_mob)
    return VGroup(*parts)


def make_solver_block(width=1.82, height=1.18):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.09,
        stroke_color=WARNING,
        stroke_width=1.25,
        fill_color="#241826",
        fill_opacity=0.82,
    )
    title = SafeText("PDE solver", max_width=width - 0.22, max_height=0.26, font_size=18, color=TEXT, weight="BOLD")
    mesh = make_mesh_overlay(width=0.78, height=0.42, nx=4, ny=3, color=WARNING)
    stencil = VGroup(
        Dot(ORIGIN, radius=0.025, color=WARNING),
        Dot(LEFT * 0.14, radius=0.020, color=MUTED),
        Dot(RIGHT * 0.14, radius=0.020, color=MUTED),
        Dot(UP * 0.14, radius=0.020, color=MUTED),
        Dot(DOWN * 0.14, radius=0.020, color=MUTED),
    )
    glyph = VGroup(mesh, stencil).arrange(RIGHT, buff=0.14)
    subtitle = SafeText("mesh + stencil", max_width=width - 0.24, max_height=0.20, font_size=12, min_font_size=10, color=MUTED)
    linear = SafeText("linear system", max_width=width - 0.24, max_height=0.20, font_size=12, min_font_size=10, color=MUTED)
    content = VGroup(title, glyph, subtitle, linear).arrange(DOWN, buff=0.06)
    content.move_to(box)
    return VGroup(box, content)


def make_operator_block(width=2.08, height=1.32, trained=False):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.11,
        stroke_color=OPERATOR,
        stroke_width=1.45,
        fill_color="#211B32",
        fill_opacity=0.86,
    )
    glow = box.copy().set_stroke(OPERATOR, width=7.0, opacity=0.16).set_fill(opacity=0)
    formula = SafeMathTex(r"\mathcal{G}_{\theta}", max_width=1.25, max_height=0.42, font_size=35, color=OPERATOR)
    title = SafeText("trained operator" if trained else "train once", max_width=width - 0.24, max_height=0.24, font_size=16, color=TEXT, weight="BOLD")
    subtitle = SafeText("predict u", max_width=width - 0.30, max_height=0.22, font_size=14, color=MUTED)
    content = VGroup(title, formula, subtitle).arrange(DOWN, buff=0.05).move_to(box)
    return VGroup(glow, box, content)


def make_dataset_pairs(scale=0.58):
    rows = VGroup()
    for i, seed in enumerate((11, 17, 23), start=1):
        in_panel = make_function_panel(rf"a_{i}(x)", INPUT, seed, width=1.18, height=0.74)
        out_panel = make_function_panel(rf"u_{i}(x)", OUTPUT, seed + 30, width=1.18, height=0.74)
        arrow = Arrow(
            in_panel.get_right() + RIGHT * 0.04,
            out_panel.get_left() + LEFT * 0.04,
            buff=0,
            color=MUTED,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )
        row = VGroup(in_panel, arrow, out_panel).arrange(RIGHT, buff=0.20)
        rows.add(row)
    rows.arrange(DOWN, buff=0.12).scale(scale)
    label = SafeMathTex(r"(a_i,u_i)", max_width=1.45, max_height=0.28, font_size=22, color=TEXT)
    return VGroup(rows, label).arrange(DOWN, buff=0.10)


def make_speed_meter():
    base = Line(LEFT * 1.45, RIGHT * 1.45, color=GRID, stroke_width=4.0)
    slow = Dot(base.get_left(), radius=0.055, color=WARNING)
    fast = Dot(base.get_right(), radius=0.070, color=OUTPUT)
    label = Chip("forward pass", max_width=2.15, height=0.42, stroke_color=OUTPUT, font_size=16)
    payoff = Chip("fast many-query inference", max_width=3.35, height=0.42, stroke_color=OUTPUT, font_size=15)
    return VGroup(VGroup(base, slow, fast), VGroup(label, payoff).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.18)


def make_solve_icon(index):
    badge = RoundedRectangle(
        width=0.66,
        height=0.42,
        corner_radius=0.06,
        stroke_color=WARNING,
        stroke_width=1.0,
        fill_color="#331722",
        fill_opacity=0.82,
    )
    label = SafeText(f"solve {index}", max_width=0.54, max_height=0.18, font_size=10, min_font_size=8, color=WARNING)
    label.move_to(badge)
    return VGroup(badge, label)


class SolverLoop(VGroup):
    """Left split-screen: solve again per input."""

    def __init__(self, repeated=False, **kwargs):
        super().__init__(**kwargs)
        frame = RoundedRectangle(
            width=7.12,
            height=6.82,
            corner_radius=0.10,
            stroke_color=GRID,
            stroke_width=1.1,
            fill_color="#0E1729",
            fill_opacity=0.44,
        )
        title = SafeText("solver-based view", max_width=3.4, max_height=0.32, font_size=22, color=TEXT, weight="BOLD")
        mode = Chip("solve u", max_width=1.35, height=0.38, stroke_color=WARNING, font_size=17)
        header = VGroup(title, mode).arrange(RIGHT, buff=0.26)
        header.move_to(frame.get_top() + DOWN * 0.34)

        pipelines = VGroup()
        count = 3 if repeated else 1
        for i in range(count):
            y_offset = (1.42 - i * 1.42) if repeated else 0.0
            input_panel = make_function_panel(r"a(x)" if i == 0 else rf"a_{i+1}(x)", INPUT, 40 + i)
            solver = make_solver_block()
            output_panel = make_function_panel(r"u(x)" if i == 0 else rf"u_{i+1}(x)", OUTPUT, 70 + i)
            row = VGroup(input_panel, solver, output_panel).arrange(RIGHT, buff=0.34)
            arrows = VGroup(
                Arrow(input_panel.get_right() + RIGHT * 0.05, solver.get_left() + LEFT * 0.05, buff=0, color=MUTED, stroke_width=1.45),
                Arrow(solver.get_right() + RIGHT * 0.05, output_panel.get_left() + LEFT * 0.05, buff=0, color=OUTPUT, stroke_width=1.55),
            )
            row_with_arrows = VGroup(arrows, row).scale(0.74 if repeated else 1.0)
            row_with_arrows.move_to(frame.get_center() + LEFT * (0.52 if repeated else 0.0) + DOWN * 0.08 + UP * y_offset)
            if repeated:
                loop_label = Chip("solve again", max_width=1.72, height=0.42, stroke_color=WARNING, font_size=13)
                loop_label.move_to([frame.get_right()[0] - 0.96, row_with_arrows.get_center()[1], 0])
                row_with_arrows = VGroup(row_with_arrows, loop_label)
            pipelines.add(row_with_arrows)

        self.frame = frame
        self.header = header
        self.pipelines = pipelines
        self.add(frame, header, pipelines)
        self.move_to(LEFT_CENTER)


class TrainingCompression(VGroup):
    """Right split-screen: dataset and costly solves compress into G_theta."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        frame = RoundedRectangle(
            width=7.12,
            height=6.82,
            corner_radius=0.10,
            stroke_color=GRID,
            stroke_width=1.1,
            fill_color="#101827",
            fill_opacity=0.44,
        )
        title = SafeText("operator learning view", max_width=3.6, max_height=0.32, font_size=22, color=TEXT, weight="BOLD")
        mode = Chip("predict u", max_width=1.45, height=0.38, stroke_color=OPERATOR, font_size=17)
        header = VGroup(title, mode).arrange(RIGHT, buff=0.26)
        header.move_to(frame.get_top() + DOWN * 0.34)

        dataset = make_dataset_pairs(scale=0.54)
        dataset.move_to(frame.get_left() + RIGHT * 1.35 + DOWN * 0.18)
        operator = make_operator_block()
        operator.move_to(frame.get_right() + LEFT * 1.35 + DOWN * 0.18)
        solve_icons = VGroup(*[make_solve_icon(i) for i in range(1, 7)])
        solve_icons.arrange_in_grid(rows=2, cols=3, buff=0.10)
        solve_icons.move_to(frame.get_center() + DOWN * 0.18)
        train_arrow = Arrow(dataset.get_right() + RIGHT * 0.12, operator.get_left() + LEFT * 0.12, buff=0, color=OPERATOR, stroke_width=2.0)
        caption = SafeText("many examples -> one map", max_width=3.4, max_height=0.28, font_size=17, color=MUTED)
        caption.move_to(frame.get_bottom() + UP * 0.42)
        self.frame = frame
        self.header = header
        self.dataset = dataset
        self.operator = operator
        self.solve_icons = solve_icons
        self.train_arrow = train_arrow
        self.caption = caption
        self.add(frame, header, dataset, train_arrow, solve_icons, operator, caption)
        self.move_to(RIGHT_CENTER)


class ForwardPassArrow(VGroup):
    """Right split-screen: a_new through trained operator to u_pred."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        frame = RoundedRectangle(
            width=7.12,
            height=6.82,
            corner_radius=0.10,
            stroke_color=GRID,
            stroke_width=1.1,
            fill_color="#101827",
            fill_opacity=0.44,
        )
        title = SafeText("after training", max_width=2.3, max_height=0.32, font_size=22, color=TEXT, weight="BOLD")
        title.move_to(frame.get_top() + DOWN * 0.34)
        input_panel = make_function_panel(r"a_{\mathrm{new}}(x)", INPUT, 91, width=1.58, height=1.08)
        operator = make_operator_block(width=1.92, height=1.26, trained=True)
        output_panel = make_function_panel(r"u_{\mathrm{pred}}(x)", OUTPUT, 111, width=1.66, height=1.08)
        row = VGroup(input_panel, operator, output_panel).arrange(RIGHT, buff=0.30)
        row.move_to(frame.get_center() + UP * 0.20)
        arrows = VGroup(
            Arrow(input_panel.get_right() + RIGHT * 0.06, operator.get_left() + LEFT * 0.06, buff=0, color=MUTED, stroke_width=1.7),
            Arrow(operator.get_right() + RIGHT * 0.06, output_panel.get_left() + LEFT * 0.06, buff=0, color=OUTPUT, stroke_width=2.2),
        )
        speed = make_speed_meter()
        speed.move_to(frame.get_bottom() + UP * 1.28)
        self.frame = frame
        self.title = title
        self.input_panel = input_panel
        self.operator = operator
        self.output_panel = output_panel
        self.arrows = arrows
        self.speed = speed
        self.add(frame, title, arrows, row, speed)
        self.move_to(ORIGIN + DOWN * 0.05)


def make_strategy_bridge():
    solve = Chip("solve u", max_width=1.35, height=0.40, stroke_color=WARNING, font_size=17)
    arrow = Arrow(LEFT * 0.55, RIGHT * 0.55, buff=0, color=MUTED, stroke_width=1.6)
    predict = Chip("predict u", max_width=1.48, height=0.40, stroke_color=OPERATOR, font_size=17)
    top = VGroup(solve, arrow, predict).arrange(RIGHT, buff=0.18)
    line = SafeText("small language shift, big computational strategy shift", max_width=6.4, max_height=0.32, font_size=20, color=TEXT)
    return VGroup(top, line).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.42)


def make_final_balance():
    cost_chips = VGroup(
        Chip("data", max_width=1.15, height=0.40, stroke_color=WARNING, font_size=16),
        Chip("training", max_width=1.45, height=0.40, stroke_color=WARNING, font_size=16),
        Chip("generalization", max_width=2.20, height=0.40, stroke_color=WARNING, font_size=16),
        Chip("open questions", max_width=2.25, height=0.40, stroke_color=WARNING, font_size=16),
    ).arrange(DOWN, buff=0.13)
    cost = PanelCard("cost", body=cost_chips, width=4.10, height=3.22, accent_color=WARNING, title_font_size=25)

    payoff_body = VGroup(
        make_speed_meter().scale(0.88),
        SafeText("one trained map, many new queries", max_width=3.45, max_height=0.28, font_size=18, color=MUTED),
    ).arrange(DOWN, buff=0.18)
    payoff = PanelCard("payoff", body=payoff_body, width=4.10, height=3.22, accent_color=OUTPUT, title_font_size=25)
    operator = make_operator_block(width=2.25, height=1.42, trained=True)
    balance = VGroup(cost, operator, payoff).arrange(RIGHT, buff=0.55)
    title = SafeText("honest trade-off", max_width=4.2, max_height=0.44, font_size=30, color=TEXT, weight="BOLD")
    final = VGroup(title, balance).arrange(DOWN, buff=0.42).move_to(ORIGIN + DOWN * 0.05)
    return final


class Scene0401FromSolveUToPredictU(TimedScene):
    SCRIPT_ID = "4.1"
    SCRIPT_TITLE = 'From "solve u" to "predict u"'
    SCRIPT_START = 23 * 60 + 20
    SCRIPT_END = 25 * 60
    SCENE_DURATION = 100.0

    KEYFRAMES = (
        "KF01 0.0s solver-based view: a(x) -> PDE solver -> u(x)",
        "KF02 11.5s operator learning view: dataset pairs -> G_theta",
        "KF03 25.0s solve u -> predict u strategy bridge",
        "KF04 38.0s repeated solver loop + amortization compression",
        "KF05 53.5s a_new forward pass through trained operator",
        "KF06 67.0s cost/payoff balanced final frame",
        "KF07 92.0s final hold for visual QA",
    )

    def construct(self):
        background = make_background_network(seed=401, n=72, dot_opacity=0.13, line_opacity=0.10)
        self.add(background)

        solver_single = SolverLoop(repeated=False)
        assert_in_frame(solver_single, margin=0.35, label="solver_single")

        # Global 23:20.0-23:31.5 => local 0.0-11.5
        self.play_timed(
            "solver_based_view_solve_u",
            0.0,
            11.5,
            FadeIn(solver_single.frame),
            FadeIn(solver_single.header, shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(mob, shift=RIGHT * 0.08) for mob in solver_single.pipelines[0]], lag_ratio=0.12),
        )

        training_view = TrainingCompression()
        assert_in_frame(training_view, margin=0.35, label="training_view")

        # Global 23:31.5-23:44.0 => local 11.5-24.0
        self.play_timed(
            "operator_learning_view_many_pairs_to_map",
            11.5,
            24.0,
            FadeIn(training_view.frame),
            FadeIn(training_view.header, shift=DOWN * 0.08),
            FadeIn(training_view.dataset, lag_ratio=0.08),
            FadeIn(training_view.train_arrow),
            FadeIn(training_view.operator, shift=LEFT * 0.10),
            FadeIn(training_view.caption, shift=UP * 0.08),
        )

        # Global 23:44.0-23:45.0 => local 24.0-25.0
        self.wait_timed("pause_hold_split_screen", 24.0, 25.0)

        bridge = make_strategy_bridge()
        assert_in_frame(bridge, margin=0.35, label="strategy_bridge")

        # Global 23:45.0-23:58.0 => local 25.0-38.0
        self.play_timed(
            "language_shift_strategy_shift",
            25.0,
            38.0,
            FadeIn(bridge, shift=DOWN * 0.08),
            Indicate(solver_single.header[1], color=WARNING, scale_factor=1.05),
            Indicate(training_view.operator, color=OPERATOR, scale_factor=1.03),
        )

        solver_repeated = SolverLoop(repeated=True)
        assert_in_frame(solver_repeated, margin=0.35, label="solver_repeated")

        # Global 23:58.0-24:13.5 => local 38.0-53.5
        self.play_timed(
            "solve_again_every_input_amortize_training",
            38.0,
            53.5,
            ReplacementTransform(solver_single, solver_repeated),
            FadeIn(training_view.solve_icons, lag_ratio=0.10),
            LaggedStart(*[icon.animate.move_to(training_view.operator).set_opacity(0.18) for icon in training_view.solve_icons], lag_ratio=0.10),
            Indicate(training_view.operator, color=OPERATOR, scale_factor=1.04),
        )

        forward_view = ForwardPassArrow()
        assert_in_frame(forward_view, margin=0.35, label="forward_view")

        # Global 24:13.5-24:17.0 => local 53.5-57.0
        self.play_timed(
            "clear_split_screen_before_forward_pass",
            53.5,
            57.0,
            FadeOut(training_view, shift=UP * 0.10),
            FadeOut(solver_repeated, shift=UP * 0.10),
            FadeOut(bridge, shift=UP * 0.08),
        )
        # Global 24:17.0-24:20.5 => local 57.0-60.5
        self.play_timed(
            "forward_pass_enters_center_stage",
            57.0,
            60.5,
            FadeIn(forward_view.frame),
            FadeIn(forward_view.title, shift=DOWN * 0.08),
            FadeIn(forward_view.input_panel, shift=RIGHT * 0.08),
            FadeIn(forward_view.operator, shift=UP * 0.06),
            FadeIn(forward_view.output_panel, shift=LEFT * 0.08),
            Create(forward_view.arrows),
            FadeIn(forward_view.speed, shift=UP * 0.08),
        )
        # Global 24:20.5-24:27.0 => local 60.5-67.0
        self.play_timed(
            "new_query_is_forward_pass",
            60.5,
            67.0,
            Indicate(forward_view.output_panel, color=OUTPUT, scale_factor=1.03),
        )

        final_balance = make_final_balance()
        assert_in_frame(final_balance, margin=0.38, label="final_balance")

        # Global 24:27.0-25:00.0 => local 67.0-100.0
        self.play_timed(
            "balanced_cost_and_payoff",
            67.0,
            84.0,
            FadeOut(forward_view, shift=UP * 0.10),
            FadeIn(final_balance[0], shift=DOWN * 0.08),
            FadeIn(final_balance[1][0], shift=RIGHT * 0.08),
            FadeIn(final_balance[1][1], shift=UP * 0.06),
            FadeIn(final_balance[1][2], shift=LEFT * 0.08),
        )
        self.play_timed(
            "honest_final_hold",
            84.0,
            100.0,
            Indicate(final_balance[1][1], color=OPERATOR, scale_factor=1.03),
            final_balance[1][2].animate.set_opacity(1.0),
        )
        self.pad_to(self.SCENE_DURATION)
