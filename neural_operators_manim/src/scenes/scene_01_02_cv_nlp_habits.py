"""
Scene 1.2 - Why CV/NLP shaped our habits
Script: docs/full_voice_manim_script.md
Global time: 03:35.0-05:20.0
Local duration: 105.0s
"""

from pathlib import Path
import sys

from manim import *
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import (
    make_background_network,
    make_card,
    make_chip,
    make_warning_stamp,
)
from src.common.theme import (
    apply_global_config,
    BG,
    CARD_BG,
    GRID,
    TEXT,
    MUTED,
    INPUT,
    OUTPUT,
    OPERATOR,
    WARNING,
    PURPLE,
    NVIDIA_GREEN,
    PHYSICS,
    SCIENCE,
    STAMP_RED,
)
from src.common.timing import TimedScene


apply_global_config()


class MetricCards(VGroup):
    def __init__(self, labels, colors, **kwargs):
        cards = [
            make_card(label, width=1.78, height=0.66, color=colors[i % len(colors)])
            for i, label in enumerate(labels)
        ]
        super().__init__(*cards, **kwargs)
        self.arrange_in_grid(rows=2, cols=3, buff=(0.18, 0.16))


class PhysicsConstraintCards(VGroup):
    def __init__(self, specs, **kwargs):
        cards = []
        for label, glyph, color in specs:
            frame = RoundedRectangle(
                width=2.18,
                height=0.82,
                corner_radius=0.08,
                stroke_color=color,
                stroke_width=1.25,
                fill_color=CARD_BG,
                fill_opacity=0.82,
            )
            glyph_mob = glyph
            glyph_mob.scale(0.78)
            label_mob = Text(label, font_size=16, color=TEXT)
            content = VGroup(glyph_mob, label_mob).arrange(RIGHT, buff=0.14)
            content.move_to(frame)
            cards.append(VGroup(frame, content))
        super().__init__(*cards, **kwargs)
        self.arrange_in_grid(rows=3, cols=2, buff=(0.2, 0.16))


class Scene0102CVNLPHabits(TimedScene):
    SCRIPT_ID = "1.2"
    SCRIPT_TITLE = "Why CV/NLP shaped our habits"
    SCRIPT_START = 215.0
    SCRIPT_END = 320.0
    SCENE_DURATION = 105.0

    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def make_architecture_chips(self):
        specs = [
            ("CNN", INPUT),
            ("ResNet", NVIDIA_GREEN),
            ("U-Net", OUTPUT),
            ("Transformer", PURPLE),
            ("ViT", OPERATOR),
        ]
        chips = VGroup(*[make_chip(label, color=color, font_size=15) for label, color in specs])
        chips.arrange(RIGHT, buff=0.12)
        return chips

    def make_metric_cards(self):
        labels = [
            "Accuracy",
            "FID",
            "Inception Score",
            "CLIP Score",
            "L1 / L2",
            "RMSE",
        ]
        colors = [OUTPUT, INPUT, OPERATOR, PURPLE, NVIDIA_GREEN, SCIENCE]
        return MetricCards(labels, colors)

    def make_physics_constraint_cards(self):
        specs = [
            ("conservation", self.make_conservation_glyph(), PHYSICS),
            ("derivatives", MathTex(r"\nabla", color=INPUT, font_size=30), INPUT),
            ("integrals", MathTex(r"\int", color=OPERATOR, font_size=30), OPERATOR),
            ("PDE residual", MathTex(r"\mathcal{R}_{PDE}", color=PURPLE, font_size=26), PURPLE),
            ("boundary conditions", self.make_boundary_glyph(), SCIENCE),
            ("domain expert checks", self.make_check_glyph(), NVIDIA_GREEN),
        ]
        return PhysicsConstraintCards(specs)

    def make_warning_stamp(self, text="Not plug-and-play"):
        return make_warning_stamp(text)

    def make_pillar(self, label, color):
        core = RoundedRectangle(
            width=2.35,
            height=1.7,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.8,
            fill_color=CARD_BG,
            fill_opacity=0.66,
        )
        glow = VGroup(
            *[
                RoundedRectangle(
                    width=2.35 + 0.12 * i,
                    height=1.7 + 0.12 * i,
                    corner_radius=0.09,
                    stroke_color=color,
                    stroke_width=1.0,
                    stroke_opacity=0.23 / (i + 1),
                )
                for i in range(4)
            ]
        )
        title = Text(label, font_size=25, color=TEXT, weight=BOLD)
        title.move_to(core)
        return VGroup(glow, core, title)

    def make_standard_shelf(self):
        labels = ["Dataset", "Benchmark", "Loss", "Metric", "Leaderboard"]
        colors = [INPUT, OUTPUT, OPERATOR, PURPLE, NVIDIA_GREEN]
        cards = VGroup(
            *[make_card(label, width=1.68, height=0.72, color=colors[i]) for i, label in enumerate(labels)]
        )
        cards.arrange(RIGHT, buff=0.16)
        rail = Line(cards.get_left() + DOWN * 0.58, cards.get_right() + DOWN * 0.58, color=GRID, stroke_width=3)
        label = Text("The standard ML ecosystem", font_size=25, color=TEXT)
        label.next_to(cards, UP, buff=0.24)
        box = SurroundingRectangle(VGroup(cards, label, rail), buff=0.22, color=GRID, stroke_width=1.1)
        return VGroup(box, label, cards, rail)

    def make_domain_cards(self):
        specs = [
            ("Weather", INPUT),
            ("Seismology", OPERATOR),
            ("Molecular dynamics", PURPLE),
            ("Fluid simulation", SCIENCE),
        ]
        cards = VGroup(
            *[make_card(label, width=2.18, height=0.72, color=color) for label, color in specs]
        )
        cards.arrange(DOWN, buff=0.18)
        label = Text("scientific domains", font_size=23, color=TEXT)
        label.next_to(cards, UP, buff=0.24)
        return VGroup(label, cards)

    def make_conservation_glyph(self):
        loop = Arc(radius=0.18, start_angle=0.35, angle=TAU * 0.82, color=PHYSICS, stroke_width=2.2)
        tip = Triangle(color=PHYSICS, fill_color=PHYSICS, fill_opacity=0.9).scale(0.06)
        tip.move_to(loop.point_from_proportion(0.82))
        tip.rotate(-0.2)
        return VGroup(loop, tip)

    def make_boundary_glyph(self):
        box = Square(side_length=0.36, color=SCIENCE, stroke_width=2)
        left = Line(box.get_left(), box.get_left() + UP * 0.34, color=SCIENCE, stroke_width=2)
        right = Line(box.get_right(), box.get_right() + DOWN * 0.34, color=SCIENCE, stroke_width=2)
        return VGroup(box, left, right)

    def make_check_glyph(self):
        return MathTex(r"\checkmark", color=NVIDIA_GREEN, font_size=28)

    def make_pipeline_attempt(self):
        imagenet = make_card("ImageNet mindset", width=2.32, height=0.84, color=INPUT)
        navier = make_card("Navier-Stokes", width=2.28, height=0.84, color=SCIENCE)
        wall = RoundedRectangle(
            width=0.25,
            height=1.85,
            corner_radius=0.05,
            stroke_color=PHYSICS,
            stroke_width=1.8,
            fill_color=PHYSICS,
            fill_opacity=0.12,
        )
        physics_label = Text("physics", font_size=17, color=PHYSICS)
        physics_label.next_to(wall, DOWN, buff=0.1)
        arrow = Arrow(LEFT * 1.0, RIGHT * 1.0, buff=0.12, color=OPERATOR, stroke_width=2.4)
        group = VGroup(imagenet, arrow, wall, physics_label, navier).arrange(RIGHT, buff=0.28)
        wall.move_to(group.get_center() + RIGHT * 0.23)
        physics_label.next_to(wall, DOWN, buff=0.1)
        arrow.put_start_and_end_on(imagenet.get_right() + RIGHT * 0.12, wall.get_left() + LEFT * 0.08)
        navier.next_to(wall, RIGHT, buff=0.38)
        bounce = VGroup(imagenet, arrow)
        barrier = VGroup(wall, physics_label)
        return VGroup(bounce, barrier, navier)

    def construct(self):
        background = make_background_network(seed=12)

        title = Text("CV/NLP shaped our habits", font_size=47, color=TEXT, weight=BOLD)
        title.set_color_by_gradient(TEXT, INPUT)
        title.move_to(UP * 3.0)
        cv_pillar = self.make_pillar("Computer Vision", INPUT)
        nlp_pillar = self.make_pillar("Natural Language Processing", PURPLE)
        pillars = VGroup(cv_pillar, nlp_pillar).arrange(RIGHT, buff=0.65).move_to(DOWN * 0.08)
        arch_chips = self.make_architecture_chips()
        arch_chips.next_to(pillars, DOWN, buff=0.36)

        # Global 03:35.0-03:44.5 => local 0.0-9.5
        self.play_timed(
            "cv_nlp_habits_intro",
            0.0,
            9.5,
            FadeIn(background),
            Write(title),
            LaggedStart(FadeIn(cv_pillar, shift=UP * 0.18), FadeIn(nlp_pillar, shift=UP * 0.18), lag_ratio=0.25),
            LaggedStart(*[FadeIn(chip, shift=DOWN * 0.08) for chip in arch_chips], lag_ratio=0.12),
        )

        shelf = self.make_standard_shelf()
        shelf.move_to(DOWN * 0.04)
        title_small = title.copy().scale(0.62).to_edge(UP, buff=0.28)

        # Global 03:44.5-03:55.5 => local 9.5-20.5
        self.play_timed(
            "standard_ecosystem_shelf",
            9.5,
            20.5,
            Transform(title, title_small),
            FadeOut(pillars, shift=LEFT * 0.16),
            arch_chips.animate.scale(0.82).next_to(title_small, DOWN, buff=0.2),
            LaggedStart(*[FadeIn(part, shift=UP * 0.16) for part in shelf], lag_ratio=0.12),
        )

        metric_cards = self.make_metric_cards()
        metric_cards.next_to(shelf, DOWN, buff=0.42)
        familiar_label = Text("familiar, useful comparison tools", font_size=21, color=MUTED)
        familiar_label.next_to(metric_cards, DOWN, buff=0.18)
        checks = VGroup(
            *[
                MathTex(r"\checkmark", color=NVIDIA_GREEN, font_size=22).move_to(card.get_corner(UR) + LEFT * 0.18 + DOWN * 0.17)
                for card in metric_cards
            ]
        )

        # Global 03:55.5-04:07.0 => local 20.5-32.0
        self.play_timed(
            "metric_cards_expand",
            20.5,
            32.0,
            shelf.animate.shift(UP * 0.34).scale(0.94),
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in metric_cards], lag_ratio=0.11),
            LaggedStart(*[FadeIn(check, scale=0.6) for check in checks], lag_ratio=0.08),
            FadeIn(familiar_label, shift=UP * 0.1),
        )

        # Global 04:07.0-04:08.0 => local 32.0-33.0
        self.wait_timed("one_second_pause", 32.0, 33.0)

        domains = self.make_domain_cards()
        domains.move_to(RIGHT * 4.55 + DOWN * 0.12)
        old_ecosystem = VGroup(shelf, metric_cards, checks, familiar_label, arch_chips)
        old_target = old_ecosystem.copy().scale(0.72).move_to(LEFT * 4.25 + DOWN * 0.22)
        old_target.set_opacity(0.42)
        environment_frame = RoundedRectangle(
            width=4.5,
            height=4.95,
            corner_radius=0.08,
            stroke_color=SCIENCE,
            stroke_width=1.3,
            fill_color="#062C2C",
            fill_opacity=0.12,
        )
        environment_frame.move_to(domains)

        # Global 04:08.0-04:20.0 => local 33.0-45.0
        self.play_timed(
            "scientific_domains_enter",
            33.0,
            45.0,
            Transform(old_ecosystem, old_target),
            FadeIn(environment_frame, shift=RIGHT * 0.22),
            LaggedStart(*[FadeIn(item, shift=LEFT * 0.18) for item in domains], lag_ratio=0.14),
            title.animate.set_color(TEXT),
        )

        physics_cards = self.make_physics_constraint_cards()
        physics_cards.move_to(RIGHT * 1.2 + DOWN * 0.1)
        domains_target = domains.copy().scale(0.74).move_to(LEFT * 4.55 + DOWN * 0.05)
        domains_target.set_opacity(0.72)
        domain_card_group = domains_target[1]
        arrows = VGroup(
            *[
                Arrow(
                    domain_card_group[i % len(domain_card_group)].get_right(),
                    physics_cards[i].get_left(),
                    buff=0.18,
                    color=SCIENCE,
                    stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.08,
                )
                for i in range(len(physics_cards))
            ]
        )
        physics_title = Text("which law matters?", font_size=25, color=PHYSICS)
        physics_title.next_to(physics_cards, UP, buff=0.24)

        # Global 04:20.0-04:34.0 => local 45.0-59.0
        self.play_timed(
            "physics_constraints_take_priority",
            45.0,
            59.0,
            FadeOut(old_ecosystem, shift=LEFT * 0.18),
            FadeOut(environment_frame),
            Transform(domains, domains_target),
            FadeIn(physics_title, shift=DOWN * 0.12),
            LaggedStart(*[FadeIn(card, shift=RIGHT * 0.13) for card in physics_cards], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.08),
        )

        pipeline = self.make_pipeline_attempt()
        pipeline.move_to(DOWN * 0.16)
        wall_cross = Cross(pipeline[1][0], stroke_color=STAMP_RED, stroke_width=4.0, scale_factor=0.92)
        stamp = self.make_warning_stamp("Not plug-and-play")
        stamp.next_to(pipeline, UP, buff=0.42)
        old_context = VGroup(domains, physics_title, physics_cards, arrows)
        context_target = old_context.copy().scale(0.58).to_edge(UP, buff=0.45).set_opacity(0.33)

        # Global 04:34.0-04:49.5 => local 59.0-74.5
        self.play_timed(
            "not_plug_and_play_stamp",
            59.0,
            68.0,
            Transform(old_context, context_target),
            FadeIn(pipeline, shift=UP * 0.16),
            Create(wall_cross),
            FadeIn(stamp, scale=1.2),
        )
        self.play_timed(
            "pipeline_hits_physics_wall",
            68.0,
            74.5,
            pipeline[0].animate.shift(LEFT * 0.18),
            stamp.animate.scale(1.03),
            wall_cross.animate.set_stroke(width=4.8),
            rate_func=there_and_back,
        )

        finite_label = Text("finite-dimensional habits", font_size=20, color=MUTED)
        compact_shelf = self.make_standard_shelf().scale(0.52)
        compact_metric = self.make_metric_cards().scale(0.45)
        compact_metric.next_to(compact_shelf, DOWN, buff=0.12)
        finite_group = VGroup(compact_shelf, compact_metric, finite_label).arrange(DOWN, buff=0.12)
        finite_group.to_corner(DL, buff=0.45).set_opacity(0.52)

        destination = Text("Function Spaces", font_size=64, color=TEXT, weight=BOLD)
        destination.set_color_by_gradient(TEXT, PHYSICS)
        destination.move_to(RIGHT * 1.15 + UP * 0.2)
        destination_glow = VGroup(
            *[
                SurroundingRectangle(
                    destination,
                    buff=0.18 + 0.08 * i,
                    color=PHYSICS,
                    stroke_width=1.2,
                    stroke_opacity=0.2 / (i + 1),
                    corner_radius=0.08,
                )
                for i in range(5)
            ]
        )
        next_rules = Text("new domain, new rules", font_size=28, color=MUTED)
        next_rules.next_to(destination, DOWN, buff=0.22)
        physics_motes = VGroup(
            MathTex(r"\nabla", color=INPUT, font_size=28),
            MathTex(r"\int", color=OPERATOR, font_size=28),
            MathTex(r"\mathcal{R}_{PDE}", color=PURPLE, font_size=24),
            Text("conservation", font_size=19, color=PHYSICS),
        ).arrange(RIGHT, buff=0.34)
        physics_motes.next_to(next_rules, DOWN, buff=0.35)
        final_group = VGroup(destination_glow, destination, next_rules, physics_motes)

        # Global 04:49.5-05:20.0 => local 74.5-105.0
        self.play_timed(
            "function_spaces_reframe",
            74.5,
            88.0,
            FadeOut(old_context),
            FadeOut(pipeline),
            FadeOut(wall_cross),
            FadeOut(stamp),
            FadeIn(finite_group, shift=DOWN * 0.12),
            LaggedStart(
                FadeIn(destination_glow),
                Write(destination),
                FadeIn(next_rules, shift=UP * 0.12),
                LaggedStart(*[FadeIn(mote, shift=UP * 0.08) for mote in physics_motes], lag_ratio=0.12),
                lag_ratio=0.18,
            ),
        )
        self.play_timed(
            "function_spaces_ambient_glow",
            88.0,
            101.5,
            destination_glow.animate.set_stroke(opacity=0.34),
            destination.animate.scale(1.025),
            physics_motes.animate.set_opacity(0.78),
            rate_func=there_and_back,
        )
        self.wait_timed("final_hold", 101.5, 105.0)
        self.pad_to(self.SCENE_DURATION)
