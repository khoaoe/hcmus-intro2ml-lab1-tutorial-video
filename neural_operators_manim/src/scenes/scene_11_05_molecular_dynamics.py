"""
Scene 11.5 - Molecular dynamics as continuous-time function
Script: ../docs/full_voice_manim_script.md
Global time: 1:33:35.0-1:35:30.0
Local duration: 115.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.domain_visuals import make_molecule_graph, make_trajectory_tube
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, INPUT, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


REQUIRED_VISUAL_LABELS = (
    "frame sequence",
    "continuous trajectory function",
    "trajectory function",
    "uncertainty",
    "long-time behavior",
    "symmetry",
    "stability",
)


def make_molecule_frame_strip():
    frames = VGroup()
    for i in range(4):
        frame = make_molecule_graph().scale(0.72)
        frame.shift(RIGHT * i * 1.75)
        frame[1].rotate(0.20 * i)
        frames.add(frame)
    frames.arrange(RIGHT, buff=0.24)
    label = SafeText("frame sequence", max_width=2.4, max_height=0.28, font_size=18, color=TEXT)
    label.next_to(frames, DOWN, buff=0.16)
    return VGroup(frames, label)


class Scene1105MolecularDynamics(TimedScene):
    SCRIPT_ID = "11.5"
    SCRIPT_TITLE = "Molecular dynamics as continuous-time function"
    SCRIPT_START = 93 * 60 + 35
    SCRIPT_END = 95 * 60 + 30
    SCENE_DURATION = 115.0

    KEYFRAMES = (
        "KF01 0.0s molecule frame sequence",
        "KF02 12.0s continuous in time",
        "KF03 24.0s frame prediction misses operator",
        "KF04 37.5s pause",
        "KF05 54.0s map to trajectory function",
        "KF06 69.5s query uncertainty long-time behavior",
        "KF07 115.0s symmetry conservation stability",
    )

    def construct(self):
        background = make_background_network(seed=1105, n=68, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("11.5  Molecular dynamics", max_width=3.35, height=0.42, stroke_color=OUTPUT, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("molecular dynamics is a trajectory function, not just frames", max_width=8.0, max_height=0.42, font_size=29, color=TEXT, weight="BOLD").move_to(UP * 3.50)
        frames = make_molecule_frame_strip().move_to(UP * 1.00)
        trajectory = make_trajectory_tube().move_to(DOWN * 0.88)
        operator = Chip("condition / force field -> trajectory function", max_width=4.95, height=0.50, stroke_color=OPERATOR, font_size=17).move_to(DOWN * 2.28)
        query = SafeText("protein engineering needs queryable paths, uncertainty, and long-time behavior", max_width=8.1, max_height=0.36, font_size=21, color=SCIENCE).move_to(DOWN * 3.22)
        stability = SafeText("respect symmetry, conservation, and stability over time", max_width=6.8, max_height=0.36, font_size=22, color=WARNING).move_to(DOWN * 3.22)
        symmetry = VGroup(
            Chip("rotate", max_width=1.02, height=0.38, stroke_color=PURPLE, font_size=14),
            Chip("translate", max_width=1.28, height=0.38, stroke_color=INPUT, font_size=14),
            Chip("energy", max_width=1.08, height=0.38, stroke_color=OUTPUT, font_size=14),
        ).arrange(RIGHT, buff=0.20).move_to(DOWN * 2.52)
        assert_in_frame(VGroup(section_label, title, frames, trajectory, query), margin=0.30, label="scene_11_05_layout")
        self.add(background)

        # Global 1:33:35.0 -> local 0.0; Global 1:33:47.0 -> local 12.0
        self.play_timed("molecule_visualized_as_frames", 0.0, 12.0, FadeIn(section_label, shift=DOWN * 0.04), FadeIn(title, shift=DOWN * 0.05), LaggedStart(*[FadeIn(frame, shift=UP * 0.04) for frame in frames[0]], lag_ratio=0.10), FadeIn(frames[1], shift=UP * 0.03))

        # Global 1:33:47.0 -> local 12.0; Global 1:33:59.0 -> local 24.0
        self.play_timed("continuous_time_evolution", 12.0, 24.0, FadeIn(trajectory, shift=UP * 0.05), Circumscribe(trajectory, color=OUTPUT, buff=0.08))

        # Global 1:33:59.0 -> local 24.0; Global 1:34:12.5 -> local 37.5
        self.play_timed("next_frame_can_miss_operator", 24.0, 37.5, frames.animate.set_opacity(0.42), Circumscribe(frames, color=WARNING, buff=0.10))

        # Global 1:34:12.5 -> local 37.5; Global 1:34:13.5 -> local 38.5
        self.wait_timed("pause_before_trajectory_operator", 37.5, 38.5)

        # Global 1:34:13.5 -> local 38.5; Global 1:34:29.0 -> local 54.0
        self.play_timed("operator_maps_condition_to_trajectory", 38.5, 54.0, FadeIn(operator, shift=UP * 0.04), trajectory.animate.set_opacity(1.0))

        # Global 1:34:29.0 -> local 54.0; Global 1:34:44.5 -> local 69.5
        self.play_timed("query_uncertainty_long_time_behavior", 54.0, 69.5, FadeIn(query, shift=UP * 0.04), Circumscribe(operator, color=OPERATOR, buff=0.08))

        # Global 1:34:44.5 -> local 69.5; Global 1:35:30.0 -> local 115.0
        self.play_timed("symmetry_conservation_stability", 69.5, 96.0, FadeOut(query), FadeIn(stability, shift=UP * 0.04), LaggedStart(*[FadeIn(chip, shift=UP * 0.04) for chip in symmetry], lag_ratio=0.12))
        self.play_timed("final_molecular_read", 96.0, 114.8, Circumscribe(VGroup(trajectory, symmetry), color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
