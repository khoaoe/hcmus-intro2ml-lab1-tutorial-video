"""
Scene 10.6 - Codomain attention: variables as function tokens
Script: ../docs/full_voice_manim_script.md
Global time: 1:20:30.0-1:22:30.0
Local duration: 120.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_variable_card
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, NVIDIA_GREEN, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_variable_function_cards():
    cards = VGroup(
        make_variable_card("temperature", color=INPUT),
        make_variable_card("pressure", color=OPERATOR),
        make_variable_card("velocity", color=OUTPUT),
        make_variable_card("humidity", color=PURPLE),
        make_variable_card("tracer", color=SCIENCE),
    ).arrange(RIGHT, buff=0.32)
    cards.move_to(UP * 1.55)
    return cards


def make_codomain_attention_graph(cards):
    edges = VGroup()
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            if (i + j) % 2 == 0 or abs(i - j) == 1:
                edges.add(Line(cards[i].get_center(), cards[j].get_center(), color=GRID, stroke_width=1.2, stroke_opacity=0.50))
    return edges


class Scene1006CodomainAttention(TimedScene):
    SCRIPT_ID = "10.6"
    SCRIPT_TITLE = "Codomain attention: variables as function tokens"
    SCRIPT_START = 80 * 60 + 30
    SCRIPT_END = 82 * 60 + 30
    SCENE_DURATION = 120.0

    KEYFRAMES = (
        "KF01 0.0s attention on variables",
        "KF02 13.0s multiphysics variables",
        "KF03 26.0s variable subsets",
        "KF04 40.0s pause",
        "KF05 56.5s each variable is a token-function",
        "KF06 73.0s attention transfers across systems",
        "KF07 90.0s VSPE and foundation direction",
        "KF08 120.0s final codomain graph",
    )

    def construct(self):
        background = make_background_network(seed=1006, n=70, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.6  Codomain attention", max_width=3.40, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("physical variables become function-valued tokens", max_width=7.3, max_height=0.42, font_size=29, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        cards = make_variable_function_cards()
        edges = make_codomain_attention_graph(cards)
        subset = Chip("datasets may expose different variable subsets", max_width=4.75, height=0.48, stroke_color=PURPLE, font_size=17).move_to(DOWN * 0.20)
        token_label = Chip("one variable = one function token", max_width=3.50, height=0.50, stroke_color=OPERATOR, font_size=18).move_to(DOWN * 1.15)
        transfer = SafeText("attention between variables can transfer across PDE systems", max_width=6.7, max_height=0.34, font_size=21, color=SCIENCE).move_to(DOWN * 2.15)
        vspe = Chip("VSPE: variable-specific positional encoding", max_width=4.35, height=0.48, stroke_color=NVIDIA_GREEN, font_size=16).move_to(DOWN * 3.04)
        assert_in_frame(VGroup(section_label, title, cards, subset, transfer, vspe), margin=0.30, label="scene_10_06_layout")
        self.add(background)

        # Global 1:20:30.0 -> local 0.0; Global 1:20:43.0 -> local 13.0
        self.play_timed("attention_on_codomain_variables", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), FadeIn(cards[0], shift=UP * 0.04), FadeIn(cards[1], shift=UP * 0.04))

        # Global 1:20:43.0 -> local 13.0; Global 1:20:56.0 -> local 26.0
        self.play_timed("weather_multiphysics_variables", 13.0, 26.0, FadeIn(cards[2], shift=UP * 0.04), FadeIn(cards[3], shift=UP * 0.04), LaggedStart(*[Create(edge) for edge in edges[:3]], lag_ratio=0.12))

        # Global 1:20:56.0 -> local 26.0; Global 1:21:10.0 -> local 40.0
        self.play_timed("different_variable_subsets", 26.0, 40.0, FadeIn(subset, shift=UP * 0.04), cards[3].animate.set_opacity(0.35))

        # Global 1:21:10.0 -> local 40.0; Global 1:21:11.0 -> local 41.0
        self.wait_timed("pause_after_variable_subset", 40.0, 41.0)

        # Global 1:21:11.0 -> local 41.0; Global 1:21:26.5 -> local 56.5
        self.play_timed("variable_as_token_function", 41.0, 56.5, FadeIn(token_label, shift=UP * 0.04), Circumscribe(cards[0], color=INPUT, buff=0.08), cards[3].animate.set_opacity(0.92))

        # Global 1:21:26.5 -> local 56.5; Global 1:21:43.0 -> local 73.0
        self.play_timed("attention_transfers_across_pde_systems", 56.5, 73.0, LaggedStart(*[Create(edge) for edge in edges[3:]], lag_ratio=0.10), FadeIn(transfer, shift=UP * 0.04))

        # Global 1:21:43.0 -> local 73.0; Global 1:22:00.0 -> local 90.0
        self.play_timed("variable_specific_positional_encoding", 73.0, 90.0, FadeIn(cards[4], shift=UP * 0.04), FadeIn(vspe, shift=UP * 0.04), Circumscribe(vspe, color=NVIDIA_GREEN, buff=0.08))

        # Global 1:22:00.0 -> local 90.0; Global 1:22:30.0 -> local 120.0
        foundation = SafeText("toward scientific foundation models", max_width=5.3, max_height=0.34, font_size=22, color=TEXT).move_to(DOWN * 3.58)
        self.play_timed("scientific_foundation_model_direction", 90.0, 112.0, FadeIn(foundation, shift=UP * 0.04), Circumscribe(VGroup(cards, edges), color=SCIENCE, buff=0.12))
        self.play_timed("final_codomain_read", 112.0, 119.8, Circumscribe(token_label, color=OPERATOR, buff=0.08), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
