"""
Scene 9.2 - Universal approximation, but with caveats
Script: ../docs/full_voice_manim_script.md
Global time: 1:01:00.0-1:03:20.0
Local duration: 140.0s
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
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_theorem_card():
    title = SafeText("universal approximation", max_width=4.9, max_height=0.42, font_size=30, color=TEXT, weight="BOLD")
    formula = SafeMathTex(
        r"\mathcal{G}: \mathcal{A} \to \mathcal{U}",
        max_width=4.4,
        max_height=0.52,
        font_size=38,
        color=OPERATOR,
    )
    claim = SafeText(
        "continuous operators can be approximated",
        max_width=5.2,
        max_height=0.70,
        font_size=21,
        color=TEXT,
    )
    compact = Chip("compact set", max_width=1.75, height=0.38, stroke_color=PURPLE, font_size=16)
    regularity = Chip("regularity", max_width=1.55, height=0.38, stroke_color=PURPLE, font_size=16)
    assumptions = VGroup(compact, regularity).arrange(RIGHT, buff=0.22)
    body = VGroup(formula, claim, assumptions).arrange(DOWN, buff=0.28)
    card = PanelCard("Theorem intuition", body=body, width=6.1, height=3.15, accent_color=OPERATOR, title_font_size=25)
    card.move_to(UP * 0.45)
    card.title_text = title
    return card


def make_expressivity_split():
    expressivity_body = VGroup(
        SafeText("architecture can represent", max_width=2.9, max_height=0.28, font_size=21, color=TEXT),
        SafeText("target operator class", max_width=2.9, max_height=0.28, font_size=21, color=INPUT),
    ).arrange(DOWN, buff=0.18)
    caveat_body = VGroup(
        SafeText("does not guarantee", max_width=3.1, max_height=0.28, font_size=21, color=WARNING),
        SafeText("easy training or enough data", max_width=3.2, max_height=0.28, font_size=20, color=TEXT),
    ).arrange(DOWN, buff=0.18)
    left = PanelCard("expressivity", body=expressivity_body, width=3.7, height=2.1, accent_color=INPUT, title_font_size=24)
    right = PanelCard("training / data / metric", body=caveat_body, width=4.0, height=2.1, accent_color=WARNING, title_font_size=22)
    split = VGroup(left, right).arrange(RIGHT, buff=0.65).move_to(UP * 0.40)
    split.expressivity = left
    split.caveats = right
    return split


def make_caveat_cards():
    cards = VGroup()
    labels = (
        ("training", "optimization hard", WARNING),
        ("data", "finite samples", OPERATOR),
        ("metric", "wrong metric", PURPLE),
        ("physics", "domain knowledge", INPUT),
    )
    for title, body, color in labels:
        body_mob = SafeText(body, max_width=2.6, max_height=0.48, font_size=18, color=TEXT)
        cards.add(PanelCard(title, body=body_mob, width=3.05, height=1.55, accent_color=color, title_font_size=21))
    cards.arrange_in_grid(rows=2, cols=2, buff=0.28)
    cards.move_to(DOWN * 0.35)
    return cards


def make_research_questions():
    label = SafeText("research questions", max_width=3.3, max_height=0.36, font_size=25, color=TEXT, weight="BOLD")
    chips = VGroup(
        Chip("parameterization", max_width=2.15, height=0.44, stroke_color=OPERATOR, font_size=17),
        Chip("loss", max_width=0.96, height=0.44, stroke_color=INPUT, font_size=17),
        Chip("data", max_width=0.96, height=0.44, stroke_color=PURPLE, font_size=17),
        Chip("physics", max_width=1.24, height=0.44, stroke_color=WARNING, font_size=17),
    ).arrange(RIGHT, buff=0.26)
    group = VGroup(label, chips).arrange(DOWN, buff=0.22).move_to(DOWN * 2.85)
    group.label = label
    group.chips = chips
    return group


class Scene0902UniversalApproximationCaveats(TimedScene):
    SCRIPT_ID = "9.2"
    SCRIPT_TITLE = "Universal approximation, but with caveats"
    SCRIPT_START = 61 * 60
    SCRIPT_END = 63 * 60 + 20
    SCENE_DURATION = 140.0

    KEYFRAMES = (
        "KF01 0.0s theorem card",
        "KF02 14.0s intuition on nice target operators",
        "KF03 27.0s pause",
        "KF04 28.2s caveat split",
        "KF05 42.0s expressivity only",
        "KF06 58.0s caveats are core problem",
        "KF07 72.0s theorem as baseline confidence",
        "KF08 94.0s research questions",
        "KF09 140.0s final caveat board",
    )

    def construct(self):
        background = make_background_network(seed=902, n=68, dot_opacity=0.075, line_opacity=0.04)
        section_label = Chip("9.2  Universal approximation", max_width=3.55, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        theorem = make_theorem_card()
        split = make_expressivity_split()
        caveats = make_caveat_cards()
        questions = make_research_questions()
        baseline = Chip("baseline confidence: not ruled out by expressivity", max_width=5.8, height=0.48, stroke_color=OUTPUT, font_size=18)
        baseline.move_to(UP * 3.10)

        assert_in_frame(VGroup(section_label, theorem, questions), margin=0.30, label="scene_09_02_intro")
        assert_in_frame(VGroup(section_label, split, caveats, questions), margin=0.30, label="scene_09_02_split")

        self.add(background)

        # Global 1:01:00.0 -> local 0.0; Global 1:01:14.0 -> local 14.0
        self.play_timed(
            "introduce_universal_approximation_theorem",
            0.0,
            14.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(theorem, shift=UP * 0.05),
        )

        # Global 1:01:14.0 -> local 14.0; Global 1:01:27.0 -> local 27.0
        self.play_timed(
            "highlight_nice_target_and_compact_set",
            14.0,
            27.0,
            Circumscribe(theorem.body, color=OPERATOR, buff=0.09),
            rate_func=there_and_back,
        )

        # Global 1:01:27.0 -> local 27.0; Global 1:01:28.2 -> local 28.2
        self.wait_timed("pause_after_theorem_intuition", 27.0, 28.2)

        # Global 1:01:28.2 -> local 28.2; Global 1:01:42.0 -> local 42.0
        self.play_timed(
            "split_theorem_from_caveats",
            28.2,
            42.0,
            FadeOut(theorem, shift=UP * 0.05),
            FadeIn(split, shift=DOWN * 0.05),
        )

        # Global 1:01:42.0 -> local 42.0; Global 1:01:58.0 -> local 58.0
        self.play_timed(
            "stress_expressivity_not_training",
            42.0,
            58.0,
            Circumscribe(split.expressivity, color=INPUT, buff=0.08),
            Circumscribe(split.caveats, color=WARNING, buff=0.08),
        )

        # Global 1:01:58.0 -> local 58.0; Global 1:02:12.0 -> local 72.0
        self.play_timed(
            "show_scientific_caveat_cards",
            58.0,
            72.0,
            FadeOut(split, shift=UP * 0.05),
            LaggedStart(*[FadeIn(card, shift=UP * 0.04) for card in caveats], lag_ratio=0.12),
        )

        # Global 1:02:12.0 -> local 72.0; Global 1:02:34.0 -> local 94.0
        self.play_timed(
            "theorem_as_baseline_confidence",
            72.0,
            94.0,
            FadeIn(baseline, shift=DOWN * 0.05),
            caveats.animate.scale(0.90).move_to(DOWN * 0.18),
        )

        # Global 1:02:34.0 -> local 94.0; Global 1:03:20.0 -> local 140.0
        self.play_timed(
            "research_questions_complete_the_picture",
            94.0,
            124.0,
            FadeIn(questions, shift=UP * 0.05),
            LaggedStart(*[Circumscribe(chip, color=OPERATOR, buff=0.04) for chip in questions.chips], lag_ratio=0.12),
        )
        self.play_timed(
            "hold_research_questions",
            124.0,
            140.0,
            caveats.animate.set_opacity(0.74),
            questions.chips.animate.set_opacity(1.0),
        )
        self.pad_to(self.SCENE_DURATION)
