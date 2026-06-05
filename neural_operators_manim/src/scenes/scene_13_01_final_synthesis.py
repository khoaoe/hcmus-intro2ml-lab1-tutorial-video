"""
Scene 13.1 - Final synthesis
Script: ../docs/full_voice_manim_script.md
Global time: 1:55:20.0-1:57:30.0
Local duration: 130.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.closing_visuals import make_grand_summary_flow, make_motif_replays
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "finite vectors",
    "functions",
    "solvers",
    "solution operator",
    "NO architectures",
    "domains",
    "open problems",
    "GNO",
    "FNO",
    "Transformer NO",
    "CoDA-NO",
    "metrics",
    "uncertainty",
    "chaos",
    "scaling",
    "physics",
    "multi-dataset",
)


class Scene1301FinalSynthesis(TimedScene):
    SCRIPT_ID = "13.1"
    SCRIPT_TITLE = "Final synthesis"
    SCRIPT_START = 115 * 60 + 20
    SCRIPT_END = 117 * 60 + 30
    SCENE_DURATION = 130.0

    KEYFRAMES = (
        "KF01 0.0s one-line recap frame",
        "KF02 13.0s finite vectors active",
        "KF03 26.0s functions active",
        "KF04 39.0s solvers active",
        "KF05 52.0s solution operator active",
        "KF06 66.0s neural operator architecture active",
        "KF07 81.0s architecture families replay",
        "KF08 98.0s open problems replay",
        "KF09 130.0s full synthesis held",
    )

    def construct(self):
        background = make_background_network(seed=1301, n=76, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("13.1  Final synthesis", max_width=3.30, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("the whole story as one line", max_width=8.2, max_height=0.46, font_size=31, color=TEXT, weight="BOLD").move_to(UP * 3.48)
        subtitle = SafeText(
            "finite representations -> function spaces -> learned solution operators",
            max_width=8.8,
            max_height=0.30,
            font_size=19,
            color=SCIENCE,
        ).move_to(UP * 3.02)
        flow = make_grand_summary_flow().move_to(UP * 1.72)
        tiles = make_motif_replays()
        for tile in tiles:
            tile.move_to(DOWN * 1.10)
        architecture_caption = SafeText(
            "integral operators + nonlinearities + residuals + discretization-aware computation",
            max_width=9.2,
            max_height=0.34,
            font_size=21,
            color=OPERATOR,
        ).move_to(DOWN * 3.22)
        open_caption = SafeText(
            "metrics, uncertainty, chaos, scaling, physics, multi-dataset learning",
            max_width=8.6,
            max_height=0.34,
            font_size=21,
            color=WARNING,
        ).move_to(DOWN * 3.24)
        assert_in_frame(VGroup(section_label, title, subtitle, flow, tiles[0], architecture_caption, open_caption), margin=0.30, label="scene_13_01_layout")
        self.add(background)

        # Global 1:55:20.0 -> local 0.0; Global 1:55:33.0 -> local 13.0
        self.play_timed(
            "single_flowing_diagram",
            0.0,
            13.0,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(title, shift=DOWN * 0.05),
            FadeIn(subtitle, shift=DOWN * 0.04),
            LaggedStart(*[FadeIn(node, shift=UP * 0.04) for node in flow.nodes], lag_ratio=0.06),
            LaggedStart(*[Create(arrow) for arrow in flow.arrows], lag_ratio=0.06),
        )

        # Global 1:55:33.0 -> local 13.0; Global 1:55:46.0 -> local 26.0
        self.play_timed(
            "traditional_deep_learning_finite_vectors",
            13.0,
            26.0,
            FadeIn(tiles[0], shift=UP * 0.05),
            Circumscribe(flow.nodes[0], color=INPUT, buff=0.06),
        )

        # Global 1:55:46.0 -> local 26.0; Global 1:55:59.0 -> local 39.0
        self.play_timed(
            "scientific_computing_function_spaces",
            26.0,
            39.0,
            ReplacementTransform(tiles[0], tiles[1]),
            Circumscribe(flow.nodes[1], color=OUTPUT, buff=0.06),
        )

        # Global 1:55:59.0 -> local 39.0; Global 1:56:12.0 -> local 52.0
        self.play_timed(
            "traditional_solvers_each_instance",
            39.0,
            52.0,
            ReplacementTransform(tiles[1], tiles[2]),
            Circumscribe(flow.nodes[2], color=SCIENCE, buff=0.06),
        )

        # Global 1:56:12.0 -> local 52.0; Global 1:56:26.0 -> local 66.0
        self.play_timed(
            "operator_learning_solution_operator",
            52.0,
            66.0,
            ReplacementTransform(tiles[2], tiles[3]),
            Circumscribe(flow.nodes[3], color=OPERATOR, buff=0.06),
        )

        # Global 1:56:26.0 -> local 66.0; Global 1:56:41.0 -> local 81.0
        self.play_timed(
            "neural_operator_architecture_components",
            66.0,
            81.0,
            ReplacementTransform(tiles[3], tiles[4]),
            FadeIn(architecture_caption, shift=UP * 0.04),
            Circumscribe(flow.nodes[4], color=PURPLE, buff=0.06),
        )

        # Global 1:56:41.0 -> local 81.0; Global 1:56:58.0 -> local 98.0
        self.play_timed(
            "gno_fno_transformer_coda_replay",
            81.0,
            98.0,
            ReplacementTransform(architecture_caption, tiles[5]),
            Circumscribe(flow.nodes[5], color=INPUT, buff=0.06),
            Circumscribe(tiles[4], color=PURPLE, buff=0.08),
        )

        # Global 1:56:58.0 -> local 98.0; Global 1:57:30.0 -> local 130.0
        self.play_timed(
            "field_still_open",
            98.0,
            118.0,
            ReplacementTransform(tiles[4], tiles[6]),
            FadeOut(tiles[5]),
            FadeIn(open_caption, shift=UP * 0.04),
            Circumscribe(flow.nodes[6], color=WARNING, buff=0.06),
        )
        self.play_timed(
            "full_synthesis_hold",
            118.0,
            129.8,
            Circumscribe(VGroup(flow.nodes[3], flow.nodes[4], flow.nodes[6]), color=OPERATOR, buff=0.08),
            rate_func=there_and_back,
        )
        self.pad_to(self.SCENE_DURATION)
