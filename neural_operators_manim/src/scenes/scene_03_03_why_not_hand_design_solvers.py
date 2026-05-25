"""
Scene 3.3 - Why not just keep hand-designing solvers?
Script: ../docs/full_voice_manim_script.md
Global time: 19:35.0-21:35.0
Local duration: 120.0s

Traditional solvers are powerful, but real systems expose modeling gaps,
parameterization error, compute walls, and inverse-problem bottlenecks.
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


def make_field_patch(width=2.8, height=1.5, rows=8, cols=13, seed=8, palette=None):
    rng = np.random.default_rng(seed)
    palette = palette or [INPUT, SCIENCE, OUTPUT, OPERATOR, PURPLE]
    cells = VGroup()
    dx = width / cols
    dy = height / rows
    for row in range(rows):
        for col in range(cols):
            x = col / max(cols - 1, 1)
            y = row / max(rows - 1, 1)
            value = np.sin(2.8 * TAU * x + 0.7 * y) + 0.55 * np.cos(1.7 * TAU * y)
            value += rng.normal(0.0, 0.16)
            cell = Rectangle(
                width=dx,
                height=dy,
                stroke_width=0.18,
                stroke_color=BG,
                fill_color=palette[int(abs(value) * 2.6 + row) % len(palette)],
                fill_opacity=0.34 + 0.26 * (0.5 + 0.5 * np.sin(value)),
            )
            cell.move_to(
                [
                    -width / 2 + dx / 2 + col * dx,
                    height / 2 - dy / 2 - row * dy,
                    0,
                ]
            )
            cells.add(cell)
    frame = RoundedRectangle(
        width=width + 0.14,
        height=height + 0.14,
        corner_radius=0.08,
        stroke_color=SCIENCE,
        stroke_width=1.1,
        fill_color=CARD_BG,
        fill_opacity=0.32,
    )
    return VGroup(frame, cells)


def make_toy_pde_box():
    formula = SafeMathTex(
        r"\partial_t u=\nu\Delta u",
        max_width=2.45,
        max_height=0.45,
        font_size=30,
        color=OPERATOR,
    )
    body = VGroup(
        formula,
        SafeText("toy PDE", max_width=1.5, max_height=0.28, font_size=18, color=TEXT, weight="BOLD"),
        SafeText("clean assumptions", max_width=2.3, max_height=0.24, font_size=15, color=MUTED),
    ).arrange(DOWN, buff=0.12)
    return PanelCard("clean model", body=body, width=3.1, height=2.0, accent_color=OPERATOR, title_font_size=21)


def make_subsystem_card(label, color):
    icon = Dot(radius=0.055, color=color)
    text = SafeText(label, max_width=1.65, max_height=0.26, font_size=17, min_font_size=13, color=TEXT)
    body = VGroup(icon, text).arrange(RIGHT, buff=0.12)
    box = RoundedRectangle(
        width=2.05,
        height=0.58,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.05,
        fill_color=CARD_BG,
        fill_opacity=0.76,
    )
    body.move_to(box)
    return VGroup(box, body)


class EquationWall(VGroup):
    """Dense but readable wall of weather-model equations."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        formulas = [
            (r"\partial_t u + u\cdot\nabla u", "momentum", INPUT),
            (r"\nabla\cdot u = 0", "mass", SCIENCE),
            (r"\partial_t T + u\cdot\nabla T", "temperature", OPERATOR),
            (r"q_{\mathrm{cloud}}(x,t)", "cloud state", PURPLE),
            (r"R_{\mathrm{rad}}(T,q)", "radiation", WARNING),
            (r"\tau_{\mathrm{turb}}", "turbulence", NVIDIA_GREEN),
            (r"S_{\mathrm{ocean}}", "ocean coupling", OUTPUT),
            (r"M_{\mathrm{micro}}", "microphysics", SCIENCE),
        ]
        entries = VGroup()
        for tex, label, color in formulas:
            formula = SafeMathTex(tex, max_width=2.15, max_height=0.34, font_size=22, min_font_size=17, color=color)
            chip = Chip(label, max_width=1.75, height=0.36, stroke_color=color, font_size=13, min_font_size=10)
            entry = VGroup(formula, chip).arrange(DOWN, buff=0.06)
            panel = RoundedRectangle(
                width=2.52,
                height=0.92,
                corner_radius=0.07,
                stroke_color=color,
                stroke_width=0.9,
                fill_color="#0F172A",
                fill_opacity=0.62,
            )
            entry.move_to(panel)
            entries.add(VGroup(panel, entry))
        entries.arrange_in_grid(rows=2, cols=4, buff=0.22)
        title = SafeText("EquationWall", max_width=3.0, max_height=0.34, font_size=22, color=TEXT, weight="BOLD")
        subtitle = SafeText("Weather equations multiply into coupled subsystems", max_width=6.2, max_height=0.30, font_size=18, color=MUTED)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.05)
        group = VGroup(header, entries).arrange(DOWN, buff=0.28)
        self.add(PanelCard("real system: coupled physics", body=group, width=11.6, height=3.75, accent_color=SCIENCE, title_font_size=24))


class ApproximationBlocks(VGroup):
    """Parameterization blocks added when equations are not enough."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        labels = [
            ("heuristic closure", WARNING),
            ("lookup table", OPERATOR),
            ("empirical rule", PURPLE),
            ("sub-grid model", INPUT),
        ]
        blocks = VGroup(*[Chip(label, max_width=2.25, height=0.48, stroke_color=color, font_size=17) for label, color in labels])
        blocks.arrange(RIGHT, buff=0.28)
        title = SafeText("ApproximationBlocks", max_width=3.7, max_height=0.34, font_size=22, color=TEXT, weight="BOLD")
        subtitle = SafeText("parameterization makes missing physics runnable", max_width=5.6, max_height=0.30, font_size=18, color=MUTED)
        self.add(VGroup(title, blocks, subtitle).arrange(DOWN, buff=0.20))


class ResolutionLadder(VGroup):
    """Grid refinement ladder: 100 km -> 10 km -> 1 km -> 100 m."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        steps = [("100 km", 4, INPUT), ("10 km", 7, SCIENCE), ("1 km", 11, OPERATOR), ("100 m", 16, WARNING)]
        cards = VGroup()
        for label, n, color in steps:
            mesh = make_mesh_overlay(width=1.55, height=1.05, nx=n, ny=max(3, n // 2), color=TEXT)
            mesh.set_stroke(width=max(0.35, 1.0 - n * 0.025), opacity=0.48)
            field = make_field_patch(width=1.55, height=1.05, rows=max(3, n // 2), cols=n, seed=n, palette=[color, SCIENCE, OUTPUT, PURPLE])
            label_mob = SafeText(label, max_width=1.2, max_height=0.28, font_size=20, color=color, weight="BOLD")
            body = VGroup(VGroup(field, mesh), label_mob).arrange(DOWN, buff=0.12)
            cards.add(PanelCard("resolution", body=body, width=2.25, height=2.45, accent_color=color, title_font_size=20))
        cards.arrange(RIGHT, buff=0.34)
        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(Arrow(left.get_right() + RIGHT * 0.05, right.get_left() + LEFT * 0.05, buff=0, color=MUTED, stroke_width=1.8))
        message = SafeText("higher resolution -> more detail", max_width=4.9, max_height=0.38, font_size=25, color=OUTPUT, weight="BOLD")
        meter = ComputeWallMeter(levels=(0.22, 0.45, 0.72, 1.0)).next_to(cards, DOWN, buff=0.22)
        self.add(VGroup(message, VGroup(cards, arrows), meter).arrange(DOWN, buff=0.25))


class ComputeWallMeter(VGroup):
    def __init__(self, levels=(0.25, 0.55, 0.92), **kwargs):
        super().__init__(**kwargs)
        title = SafeText("compute meter", max_width=1.8, max_height=0.24, font_size=15, color=WARNING)
        bars = VGroup()
        for index, level in enumerate(levels):
            slot = RoundedRectangle(
                width=0.32,
                height=0.95,
                corner_radius=0.04,
                stroke_color=GRID,
                stroke_width=0.75,
                fill_color="#0F172A",
                fill_opacity=0.75,
            )
            fill = Rectangle(width=0.23, height=0.12 + 0.72 * level, stroke_width=0, fill_color=[INPUT, SCIENCE, OPERATOR, WARNING][index], fill_opacity=0.82)
            fill.move_to(slot.get_bottom() + UP * (fill.height / 2 + 0.06))
            bars.add(VGroup(slot, fill))
        bars.arrange(RIGHT, buff=0.11)
        self.add(VGroup(title, bars).arrange(DOWN, buff=0.08))


class ExponentialCurve(VGroup):
    """Compute curve exploding as resolution increases."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            x_length=7.6,
            y_length=3.9,
            axis_config={"color": GRID, "stroke_width": 1.4, "include_tip": True},
            tips=True,
        )
        curve = axes.plot(lambda x: 0.34 * np.exp(0.82 * x), x_range=[0.2, 3.82], color=WARNING, stroke_width=4.0)
        glow = curve.copy().set_stroke(WARNING, width=9.0, opacity=0.18)
        x_label = SafeText("resolution ↑", max_width=1.7, max_height=0.28, font_size=17, color=TEXT)
        y_label = SafeText("compute ↑", max_width=1.35, max_height=0.28, font_size=17, color=TEXT)
        x_label.next_to(axes.x_axis.get_end(), DOWN, buff=0.18)
        y_label.next_to(axes.y_axis.get_end(), LEFT, buff=0.16)
        callouts = VGroup(
            Chip("grid size ↓", max_width=1.55, height=0.38, stroke_color=INPUT, font_size=15),
            Chip("time step ↓", max_width=1.65, height=0.38, stroke_color=SCIENCE, font_size=15),
            Chip("more cells", max_width=1.45, height=0.38, stroke_color=OPERATOR, font_size=15),
            Chip("more steps", max_width=1.45, height=0.38, stroke_color=WARNING, font_size=15),
        ).arrange(DOWN, buff=0.14)
        callouts.next_to(axes, RIGHT, buff=0.55)
        title = SafeText("Compute wall", max_width=3.2, max_height=0.45, font_size=31, color=WARNING, weight="BOLD")
        title.next_to(axes, UP, buff=0.20)
        self.axes = axes
        self.curve = curve
        self.glow = glow
        self.add(VGroup(title, axes, glow, curve, x_label, y_label, callouts))


class InverseLoop(VGroup):
    """Observation-to-parameter optimization loop blocked by solver."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        specs = [
            ("observation", "data", INPUT),
            ("hidden parameter", r"\theta", PURPLE),
            ("solver", "PDE step", OPERATOR),
            ("prediction", r"\hat{u}", OUTPUT),
            ("loss", "metric", WARNING),
        ]
        cards = VGroup()
        positions = [LEFT * 4.65 + UP * 1.15, LEFT * 1.9 + UP * 1.15, RIGHT * 0.9 + UP * 1.15, RIGHT * 3.65 + UP * 1.15, RIGHT * 1.55 + DOWN * 1.45]
        for label, body_label, color in specs:
            if body_label.startswith("\\"):
                body = SafeMathTex(body_label, max_width=1.2, max_height=0.34, font_size=25, color=color)
            else:
                body = SafeText(body_label, max_width=2.1, max_height=0.30, font_size=18, color=TEXT)
            pos = positions[len(cards)]
            card = PanelCard(label, body=body, width=2.75, height=1.2, accent_color=color, title_font_size=17)
            card.move_to(pos)
            cards.add(card)
        arrows = VGroup()
        path_pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)]
        for start, end in path_pairs:
            arrows.add(
                Arrow(
                    cards[start].get_center(),
                    cards[end].get_center(),
                    buff=0.76,
                    color=MUTED,
                    stroke_width=1.85,
                    max_tip_length_to_length_ratio=0.12,
                )
            )
        blocked = Line(cards[4].get_center() + LEFT * 0.55 + UP * 0.42, cards[1].get_center() + RIGHT * 0.55 + DOWN * 0.42, color=WARNING, stroke_width=6.0, stroke_opacity=0.86)
        cross = VGroup(
            Line(LEFT * 0.20 + DOWN * 0.20, RIGHT * 0.20 + UP * 0.20, color=WARNING, stroke_width=4.0),
            Line(LEFT * 0.20 + UP * 0.20, RIGHT * 0.20 + DOWN * 0.20, color=WARNING, stroke_width=4.0),
        )
        cross.move_to(blocked.get_center())
        label = Chip("slow / non-differentiable", max_width=2.75, height=0.44, stroke_color=WARNING, font_size=17)
        label.next_to(cards[2], DOWN, buff=0.16)
        message = SafeText("inverse problem bottleneck", max_width=4.2, max_height=0.42, font_size=28, color=WARNING, weight="BOLD")
        message.to_edge(DOWN, buff=0.62)
        self.cards = cards
        self.arrows = arrows
        self.blocked = VGroup(blocked, cross, label)
        self.add(arrows, cards, self.blocked, message)


class Scene0303WhyNotHandDesignSolvers(TimedScene):
    SCRIPT_ID = "3.3"
    SCRIPT_TITLE = "Why not just keep hand-designing solvers?"
    SCRIPT_START = 19 * 60 + 35
    SCRIPT_END = 21 * 60 + 35
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def make_clean_solver_question(self):
        toolbox = VGroup()
        for index, (label, color) in enumerate(
            [("PDEs", SCIENCE), ("mesh", INPUT), ("solver", OPERATOR), ("validation", OUTPUT)]
        ):
            tool = Chip(label, max_width=1.35, height=0.48, stroke_color=color, font_size=17)
            tool.shift(RIGHT * (index - 1.5) * 1.55)
            toolbox.add(tool)
        question_top = SafeText("If solvers are powerful...", max_width=6.4, max_height=0.60, font_size=40, color=TEXT, weight="BOLD")
        question_bottom = SafeText("why not hand-design everything?", max_width=7.1, max_height=0.58, font_size=38, color=OPERATOR, weight="BOLD")
        subtitle = Chip("Not replacement. Complement.", max_width=3.1, height=0.46, stroke_color=OUTPUT, font_size=18)
        group = VGroup(toolbox, question_top, question_bottom, subtitle).arrange(DOWN, buff=0.30)
        assert_in_frame(group, margin=0.45, label="clean_solver_question")
        return group

    def make_weather_system(self):
        weather = make_weather_sphere_icon(radius=0.72)
        weather.scale(1.12)
        toy = make_toy_pde_box()
        subsystems = VGroup(
            make_subsystem_card("clouds", INPUT),
            make_subsystem_card("mountains", SCIENCE),
            make_subsystem_card("ocean waves", OUTPUT),
            make_subsystem_card("radiation", WARNING),
            make_subsystem_card("turbulence", OPERATOR),
            make_subsystem_card("microphysics", PURPLE),
        ).arrange_in_grid(rows=2, cols=3, buff=0.20)
        toy.next_to(weather, RIGHT, buff=0.95)
        subsystems.next_to(toy, RIGHT, buff=0.80)
        message = SafeText("real world is not a clean toy PDE", max_width=6.4, max_height=0.44, font_size=30, color=WARNING, weight="BOLD")
        group = VGroup(VGroup(weather, toy, subsystems), message).arrange(DOWN, buff=0.45)
        assert_in_frame(group, margin=0.42, label="weather_system")
        return group

    def make_equation_wall(self):
        wall = EquationWall()
        approximations = ApproximationBlocks()
        approximations.next_to(wall, DOWN, buff=0.36)
        group = VGroup(wall, approximations)
        group.move_to(ORIGIN)
        assert_in_frame(group, margin=0.35, label="equation_wall")
        return group

    def make_parameterization_error(self):
        runnable_field = make_field_patch(seed=18, palette=[INPUT, SCIENCE, OUTPUT, NVIDIA_GREEN])
        error_field = make_field_patch(seed=28, palette=[WARNING, OPERATOR, PURPLE, TEXT])
        ripple = VGroup()
        for index, radius in enumerate((0.24, 0.42, 0.62)):
            ripple.add(Circle(radius=radius, stroke_color=WARNING, stroke_width=1.4, stroke_opacity=0.42 - index * 0.08).shift(RIGHT * 0.24 + UP * 0.10))
        clean_body = VGroup(runnable_field, SafeText("parameterization closes missing pieces", max_width=3.85, max_height=0.42, font_size=18, color=TEXT)).arrange(DOWN, buff=0.20)
        error_body = VGroup(VGroup(error_field, ripple), SafeText("error drifts with forecast", max_width=3.35, max_height=0.42, font_size=18, color=TEXT)).arrange(DOWN, buff=0.20)
        left = PanelCard("runnable model", body=clean_body, width=4.8, height=3.6, accent_color=OUTPUT, title_font_size=25)
        right = PanelCard("approximation error", body=error_body, width=4.8, height=3.6, accent_color=WARNING, title_font_size=25)
        VGroup(left, right).arrange(RIGHT, buff=0.95)
        arrow = Arrow(left.get_right() + RIGHT * 0.25, right.get_left() + LEFT * 0.25, buff=0, color=MUTED, stroke_width=2.0)
        tag = Chip("parameterization", max_width=2.35, height=0.46, stroke_color=OPERATOR, font_size=18)
        tag.next_to(arrow, UP, buff=0.18)
        group = VGroup(left, arrow, right, tag)
        assert_in_frame(group, margin=0.40, label="parameterization_error")
        return group

    def make_resolution_ladder(self):
        ladder = ResolutionLadder()
        ladder.move_to(ORIGIN)
        assert_in_frame(ladder, margin=0.35, label="resolution_ladder")
        return ladder

    def make_exponential_curve(self):
        curve = ExponentialCurve()
        curve.move_to(ORIGIN)
        assert_in_frame(curve, margin=0.40, label="exponential_curve")
        return curve

    def make_inverse_loop(self):
        loop = InverseLoop()
        loop.move_to(ORIGIN)
        assert_in_frame(loop, margin=0.45, label="inverse_loop")
        return loop

    def make_final_complement_view(self):
        limitation_cards = VGroup()
        for label, detail, color in [
            ("modeling gap", "missing physics", WARNING),
            ("compute wall", "cost explodes", OPERATOR),
            ("inverse bottleneck", "blocked gradients", PURPLE),
        ]:
            body = SafeText(detail, max_width=2.2, max_height=0.32, font_size=19, color=TEXT, weight="BOLD")
            limitation_cards.add(PanelCard(label, body=body, width=3.05, height=1.38, accent_color=color, title_font_size=20))
        limitation_cards.arrange(DOWN, buff=0.22)
        solver = PanelCard("traditional solvers", body=SafeMathTex(r"\mathcal{E}(u)=0", max_width=1.9, max_height=0.42, font_size=27, color=SCIENCE), width=3.25, height=1.75, accent_color=SCIENCE, title_font_size=21)
        ml = PanelCard("Machine Learning", body=SafeText("learn from data", max_width=2.3, max_height=0.30, font_size=19, color=TEXT), width=3.25, height=1.75, accent_color=OUTPUT, title_font_size=21)
        no = PanelCard("Neural Operators", body=SafeMathTex(r"\mathcal{G}: \mathcal{A}\to\mathcal{U}", max_width=2.35, max_height=0.42, font_size=27, color=OPERATOR), width=3.25, height=1.75, accent_color=OPERATOR, title_font_size=21)
        complement_stack = VGroup(solver, ml, no).arrange(DOWN, buff=0.24)
        plus = SafeText("+", max_width=0.45, max_height=0.55, font_size=42, color=OUTPUT, weight="BOLD")
        left_label = SafeText("limitations", max_width=2.4, max_height=0.34, font_size=22, color=MUTED)
        left_group = VGroup(left_label, limitation_cards).arrange(DOWN, buff=0.18)
        final_message = SafeText("Not replacement. Complement.", max_width=5.4, max_height=0.62, font_size=39, color=OUTPUT, weight="BOLD")
        body = VGroup(left_group, plus, complement_stack).arrange(RIGHT, buff=0.55)
        group = VGroup(body, final_message).arrange(DOWN, buff=0.42)
        glow = RoundedRectangle(
            width=group.width + 0.55,
            height=group.height + 0.42,
            corner_radius=0.15,
            stroke_color=OUTPUT,
            stroke_width=1.5,
            stroke_opacity=0.35,
            fill_color=OUTPUT,
            fill_opacity=0.035,
        )
        glow.move_to(group)
        result = VGroup(glow, group)
        assert_in_frame(result, margin=0.40, label="final_complement_view")
        return result

    def construct(self):
        background = make_background_network(seed=33, n=76, dot_opacity=0.16, line_opacity=0.12)
        self.add(background)

        clean_question = self.make_clean_solver_question()
        self.play_timed("question_appears", 0.0, 4.5, FadeIn(clean_question[0], shift=UP * 0.18), FadeIn(clean_question[1], shift=UP * 0.12))
        self.play_timed("question_deepens", 4.5, 8.5, FadeIn(clean_question[2], shift=UP * 0.10))
        self.play_timed("complement_subtitle", 8.5, 11.5, FadeIn(clean_question[3], shift=UP * 0.08), clean_question[0].animate.set_opacity(0.74))

        weather_system = self.make_weather_system()
        self.play_timed("weather_replaces_question", 11.5, 16.0, FadeOut(clean_question, shift=UP * 0.18), FadeIn(weather_system[0][0], shift=DOWN * 0.15), FadeIn(weather_system[0][1], shift=LEFT * 0.12))
        self.play_timed("subsystems_split", 16.0, 22.0, FadeIn(weather_system[0][2], lag_ratio=0.08), weather_system[0][1].animate.set_opacity(0.68))
        self.play_timed("not_toy_pde_message", 22.0, 25.0, FadeIn(weather_system[1], shift=UP * 0.08))

        equation_view = self.make_equation_wall()
        self.play_timed("equation_wall_build", 25.0, 32.5, FadeOut(weather_system, shift=UP * 0.12), FadeIn(equation_view[0], shift=DOWN * 0.12))
        self.play_timed("approximation_blocks_enter", 32.5, 38.5, FadeIn(equation_view[1], lag_ratio=0.10), equation_view[0].animate.set_opacity(0.86))
        self.wait_timed("pause_hold_parameterization", 38.5, 39.5)

        parameterization_view = self.make_parameterization_error()
        self.play_timed("runnable_model_error_view", 39.5, 45.0, FadeOut(equation_view, shift=UP * 0.12), FadeIn(parameterization_view[0], shift=LEFT * 0.12), FadeIn(parameterization_view[1:3], shift=RIGHT * 0.12))
        self.play_timed("parameterization_tag", 45.0, 49.0, FadeIn(parameterization_view[3], shift=UP * 0.08))
        self.play_timed("error_ripple", 49.0, 54.0, Indicate(parameterization_view[2], color=WARNING, scale_factor=1.02), parameterization_view[0].animate.set_opacity(0.82))

        resolution_ladder = self.make_resolution_ladder()
        self.play_timed("resolution_ladder_build", 54.0, 62.0, FadeOut(parameterization_view, shift=UP * 0.12), FadeIn(resolution_ladder[0][0], shift=DOWN * 0.10), FadeIn(resolution_ladder[0][1], lag_ratio=0.08))
        self.play_timed("compute_meter_rises", 62.0, 68.5, FadeIn(resolution_ladder[0][2], shift=UP * 0.08), Indicate(resolution_ladder[0][2], color=WARNING, scale_factor=1.04))

        compute_curve = self.make_exponential_curve()
        self.play_timed("compute_curve_axes", 68.5, 73.0, FadeOut(resolution_ladder, shift=UP * 0.10), FadeIn(compute_curve.axes), FadeIn(compute_curve[0][0]))
        self.play_timed("compute_curve_explodes", 73.0, 79.0, Create(compute_curve.glow), Create(compute_curve.curve))
        self.play_timed("compute_curve_callouts", 79.0, 83.0, FadeIn(compute_curve[0][5:], lag_ratio=0.06), Indicate(compute_curve.curve, color=WARNING, scale_factor=1.02))

        inverse_loop = self.make_inverse_loop()
        self.play_timed("inverse_loop_build", 83.0, 90.0, FadeOut(compute_curve, shift=UP * 0.10), FadeIn(inverse_loop.cards, lag_ratio=0.08))
        self.play_timed("inverse_loop_arrows", 90.0, 95.5, Create(inverse_loop.arrows))
        self.play_timed("inverse_loop_blocked", 95.5, 101.0, FadeIn(inverse_loop.blocked, shift=UP * 0.08), Indicate(inverse_loop.blocked, color=WARNING, scale_factor=1.02))

        final_view = self.make_final_complement_view()
        self.play_timed("final_limitations_collapse", 101.0, 108.0, FadeOut(inverse_loop, shift=UP * 0.10), FadeIn(final_view[1][0][0], lag_ratio=0.06))
        self.play_timed("final_complement_enter", 108.0, 115.0, FadeIn(final_view[0]), FadeIn(final_view[1][0][1:], lag_ratio=0.08))
        self.play_timed("final_message_hold", 115.0, 119.2, FadeIn(final_view[1][1], shift=UP * 0.08), final_view[0].animate.set_stroke(opacity=0.65))
        self.play_timed("ambient_glow_hold", 119.2, 120.0, final_view[0].animate.set_fill(opacity=0.07).set_stroke(opacity=0.38))
        self.pad_to(self.SCENE_DURATION)
