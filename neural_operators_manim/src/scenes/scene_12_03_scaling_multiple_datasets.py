"""
Scene 12.3 - Scaling and multiple datasets
Script: ../docs/full_voice_manim_script.md
Global time: 1:47:20.0-1:50:20.0
Local duration: 180.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.layout import make_background_network
from src.common.open_problem_visuals import make_dataset_tiles, make_foundation_silhouette, make_variable_alignment_graph
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "weather",
    "CFD",
    "seismic",
    "materials",
    "metadata",
    "geometry",
    "codomain attention",
    "operator foundation model",
    "function spaces",
    "uncertainty",
)


class Scene1203ScalingMultipleDatasets(TimedScene):
    SCRIPT_ID = "12.3"
    SCRIPT_TITLE = "Scaling and multiple datasets"
    SCRIPT_START = 107 * 60 + 20
    SCRIPT_END = 110 * 60 + 20
    SCENE_DURATION = 180.0

    KEYFRAMES = (
        "KF01 0.0s scale problem",
        "KF02 13.0s LM scaling story",
        "KF03 26.5s scientific data mismatch",
        "KF04 40.0s variables resolution physics noise",
        "KF05 53.5s pause",
        "KF06 69.5s train across datasets",
        "KF07 85.0s variable identity transfer",
        "KF08 101.0s codomain attention hint",
        "KF09 121.0s data curation and encodings",
        "KF10 180.0s foundation model conditions",
    )

    def construct(self):
        background = make_background_network(seed=1203, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("12.3  Scaling and multiple datasets", max_width=4.55, height=0.42, stroke_color=SCIENCE, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("scientific scaling is not just bigger data, model, and compute", max_width=8.4, max_height=0.42, font_size=28, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        lm_stack = VGroup(
            Chip("more data", max_width=1.35, height=0.42, stroke_color=INPUT, font_size=15),
            Chip("bigger model", max_width=1.65, height=0.42, stroke_color=PURPLE, font_size=15),
            Chip("more compute", max_width=1.70, height=0.42, stroke_color=OPERATOR, font_size=15),
        ).arrange(RIGHT, buff=0.22).move_to(UP * 2.20)
        tiles = make_dataset_tiles().move_to(UP * 0.68)
        mismatch = SafeText("variables, resolution, solver, physics, and noise all differ", max_width=7.6, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 1.25)
        alignment = make_variable_alignment_graph().move_to(DOWN * 0.40)
        curation = SafeText("curation + metadata + geometry encoding + variable encoding + multi-resolution training", max_width=8.2, max_height=0.36, font_size=21, color=SCIENCE).move_to(DOWN * 3.30)
        foundation = make_foundation_silhouette().move_to(DOWN * 0.32)
        assert_in_frame(VGroup(section_label, title, lm_stack, tiles, curation), margin=0.30, label="scene_12_03_layout")
        self.add(background)

        # Global 1:47:20.0 -> local 0.0; Global 1:47:33.0 -> local 13.0
        self.play_timed("scale_problem_intro", 0.0, 13.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05))

        # Global 1:47:33.0 -> local 13.0; Global 1:47:46.5 -> local 26.5
        self.play_timed("language_model_scaling_story", 13.0, 26.5, LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in lm_stack], lag_ratio=0.12))

        # Global 1:47:46.5 -> local 26.5; Global 1:48:00.0 -> local 40.0
        self.play_timed("scientific_data_not_homogeneous_text", 26.5, 40.0, FadeIn(tiles, shift=UP * 0.04), lm_stack.animate.set_opacity(0.42))

        # Global 1:48:00.0 -> local 40.0; Global 1:48:13.5 -> local 53.5
        self.play_timed("mismatched_variables_resolution_physics_noise", 40.0, 53.5, FadeIn(mismatch, shift=UP * 0.04), Circumscribe(tiles, color=WARNING, buff=0.08))

        # Global 1:48:13.5 -> local 53.5; Global 1:48:14.5 -> local 54.5
        self.wait_timed("pause_before_multi_dataset_training", 53.5, 54.5)

        # Global 1:48:14.5 -> local 54.5; Global 1:48:29.5 -> local 69.5
        self.play_timed("train_one_model_on_many_datasets", 54.5, 69.5, FadeOut(mismatch), tiles.animate.shift(UP * 0.18), FadeIn(alignment, shift=UP * 0.05))

        # Global 1:48:29.5 -> local 69.5; Global 1:48:45.0 -> local 85.0
        self.play_timed("variable_identity_and_transfer", 69.5, 85.0, LaggedStart(*[Create(edge) for edge in alignment.edges], lag_ratio=0.12), Circumscribe(alignment, color=SCIENCE, buff=0.08))

        # Global 1:48:45.0 -> local 85.0; Global 1:49:01.0 -> local 101.0
        self.play_timed("codomain_attention_hint_not_final", 85.0, 101.0, Circumscribe(alignment[-1][-1], color=OPERATOR, buff=0.08))

        # Global 1:49:01.0 -> local 101.0; Global 1:49:21.0 -> local 121.0
        self.play_timed("curation_metadata_encodings_training", 101.0, 121.0, FadeIn(curation, shift=UP * 0.04), Circumscribe(VGroup(tiles, alignment), color=SCIENCE, buff=0.10))

        # Global 1:49:21.0 -> local 121.0; Global 1:50:20.0 -> local 180.0
        self.play_timed("foundation_model_not_bigger_transformer", 121.0, 152.0, FadeOut(alignment), FadeOut(curation), ReplacementTransform(tiles.copy(), foundation))
        self.play_timed("final_scaling_read", 152.0, 179.8, Circumscribe(foundation, color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
