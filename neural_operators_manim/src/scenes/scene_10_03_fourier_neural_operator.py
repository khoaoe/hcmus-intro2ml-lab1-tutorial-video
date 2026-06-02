"""
Scene 10.3 - Fourier Neural Operator
Script: ../docs/full_voice_manim_script.md
Global time: 1:12:20.0-1:15:40.0
Local duration: 200.0s
"""

from pathlib import Path
import sys

from manim import *

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.architecture_visuals import make_kernel_formula, make_spectrum_bars, make_wave_panel
from src.common.layout import make_background_network
from src.common.panels import Chip
from src.common.safe_text import SafeText
from src.common.theme import apply_global_config, GRID, INPUT, MUTED, OPERATOR, OUTPUT, PURPLE, SCIENCE, TEXT, WARNING
from src.common.timing import TimedScene
from src.common.visual_safety import assert_in_frame


apply_global_config()


def make_fno_pipeline():
    physical = make_wave_panel("regular grid field", color=INPUT, width=2.65, height=1.45).move_to(LEFT * 5.45 + UP * 0.15)
    fft = Chip("FFT", max_width=0.92, height=0.52, stroke_color=OPERATOR, font_size=19).move_to(LEFT * 3.35 + UP * 0.15)
    spectrum = make_spectrum_bars(n=15, width=3.2, height=1.55, selected=5).move_to(LEFT * 0.70 + UP * 0.38)
    weights = Chip("learned mode weights", max_width=2.45, height=0.48, stroke_color=PURPLE, font_size=16).move_to(RIGHT * 1.95 + UP * 1.32)
    ifft = Chip("inverse FFT", max_width=1.48, height=0.52, stroke_color=OPERATOR, font_size=18).move_to(RIGHT * 3.20 + UP * 0.15)
    output = make_wave_panel("updated field", color=OUTPUT, width=2.65, height=1.45).move_to(RIGHT * 5.55 + UP * 0.15)
    arrows = VGroup(
        Arrow(physical.get_right(), fft.get_left(), buff=0.18, color=GRID, stroke_width=2.2),
        Arrow(fft.get_right(), spectrum.get_left(), buff=0.18, color=GRID, stroke_width=2.2),
        Arrow(spectrum.get_right(), ifft.get_left(), buff=0.18, color=GRID, stroke_width=2.2),
        Arrow(ifft.get_right(), output.get_left(), buff=0.18, color=GRID, stroke_width=2.2),
    )
    group = VGroup(physical, fft, spectrum, weights, ifft, output, arrows)
    group.physical = physical
    group.fft = fft
    group.spectrum = spectrum
    group.weights = weights
    group.ifft = ifft
    group.output = output
    group.arrows = arrows
    return group


def make_sharp_feature_demo():
    smooth = make_wave_panel("smooth global modes", color=OUTPUT, width=3.1, height=1.35)
    sharp = make_wave_panel("sharp boundary / shock", color=WARNING, width=3.1, height=1.35, freq=3.1)
    group = VGroup(smooth, sharp).arrange(RIGHT, buff=0.60).move_to(DOWN * 2.35)
    label = SafeText("global Fourier interaction is not the same as resolving every local feature", max_width=7.8, max_height=0.34, font_size=21, color=WARNING)
    label.next_to(group, DOWN, buff=0.20)
    bundle = VGroup(group, label)
    bundle.smooth = smooth
    bundle.sharp = sharp
    bundle.label = label
    return bundle


class Scene1003FourierNeuralOperator(TimedScene):
    SCRIPT_ID = "10.3"
    SCRIPT_TITLE = "Fourier Neural Operator"
    SCRIPT_START = 72 * 60 + 20
    SCRIPT_END = 75 * 60 + 40
    SCENE_DURATION = 200.0

    KEYFRAMES = (
        "KF01 0.0s Fourier basis to FNO",
        "KF02 11.5s forward transform",
        "KF03 25.0s mode weights",
        "KF04 38.0s inverse transform",
        "KF05 53.5s FFT regular grid",
        "KF06 70.0s PDE surrogate",
        "KF07 86.0s global interaction",
        "KF08 102.0s local limitation",
        "KF09 120.0s hybrid correction",
        "KF10 136.0s semi-generalized convolution",
        "KF11 153.0s FNO strong not magic",
    )

    def construct(self):
        background = make_background_network(seed=1003, n=72, dot_opacity=0.07, line_opacity=0.04)
        section_label = Chip("10.3  Fourier Neural Operator", max_width=3.60, height=0.42, stroke_color=OPERATOR, font_size=17)
        section_label.to_corner(UP + LEFT, buff=0.35)
        title = SafeText("mix selected Fourier modes, then return to physical space", max_width=8.0, max_height=0.42, font_size=28, color=TEXT, weight="BOLD")
        title.move_to(UP * 3.50)
        pipeline = make_fno_pipeline()
        formula = make_kernel_formula(r"u \xrightarrow{\mathcal{F}} \hat{u}\;\;,\;\;\hat{u}_k \mapsto R_k\hat{u}_k\;\;,\;\;\mathcal{F}^{-1}", color=OPERATOR, max_width=6.4)
        formula.move_to(UP * 2.55)
        regular = Chip("fast on regular grids via FFT", max_width=3.15, height=0.48, stroke_color=SCIENCE, font_size=17)
        regular.move_to(DOWN * 1.25)
        surrogate = Chip("PDE surrogate on regular grid", max_width=3.30, height=0.48, stroke_color=INPUT, font_size=17)
        surrogate.next_to(regular, DOWN, buff=0.18)
        global_label = SafeText("selected modes give large receptive field", max_width=4.8, max_height=0.34, font_size=21, color=PURPLE)
        global_label.move_to(DOWN * 2.18)
        sharp_demo = make_sharp_feature_demo()
        hybrid = Chip("hybrid local + global kernels", max_width=3.05, height=0.48, stroke_color=OUTPUT, font_size=17)
        hybrid.move_to(DOWN * 1.25)
        caveat = SafeText("FNO is strong, but not a magic continuum guarantee", max_width=6.9, max_height=0.36, font_size=22, color=WARNING)
        caveat.move_to(DOWN * 3.50)
        assert_in_frame(VGroup(section_label, title, pipeline, formula, caveat), margin=0.30, label="scene_10_03_layout")
        self.add(background)

        # Global 1:12:20.0 -> local 0.0; Global 1:12:31.5 -> local 11.5
        self.play_timed(
            "fourier_basis_to_fno",
            0.0,
            11.5,
            FadeIn(section_label, shift=DOWN * 0.04),
            FadeIn(title, shift=DOWN * 0.05),
            FadeIn(pipeline.physical, shift=RIGHT * 0.05),
        )

        # Global 1:12:31.5 -> local 11.5; Global 1:12:45.0 -> local 25.0
        self.play_timed(
            "fft_to_frequency_domain",
            11.5,
            25.0,
            Create(pipeline.arrows[0]),
            FadeIn(pipeline.fft, shift=UP * 0.04),
            Create(pipeline.arrows[1]),
            FadeIn(pipeline.spectrum, shift=UP * 0.05),
        )

        # Global 1:12:45.0 -> local 25.0; Global 1:12:58.0 -> local 38.0
        self.play_timed(
            "mix_selected_modes",
            25.0,
            38.0,
            FadeIn(pipeline.weights, shift=DOWN * 0.04),
            Circumscribe(pipeline.spectrum, color=OPERATOR, buff=0.08),
            pipeline.spectrum.bars[:5].animate.set_fill(opacity=0.90),
        )

        # Global 1:12:58.0 -> local 38.0; Global 1:12:59.0 -> local 39.0
        self.wait_timed("pause_after_fno_recipe", 38.0, 39.0)

        # Global 1:12:59.0 -> local 39.0; Global 1:13:13.5 -> local 53.5
        self.play_timed(
            "inverse_fft_return",
            39.0,
            53.5,
            Create(pipeline.arrows[2]),
            FadeIn(pipeline.ifft, shift=UP * 0.04),
            Create(pipeline.arrows[3]),
            FadeIn(pipeline.output, shift=LEFT * 0.05),
            FadeIn(formula, shift=DOWN * 0.04),
        )

        # Global 1:13:13.5 -> local 53.5; Global 1:13:30.0 -> local 70.0
        self.play_timed("fft_fast_on_regular_grid", 53.5, 70.0, FadeIn(regular, shift=UP * 0.04), Circumscribe(pipeline.fft, color=SCIENCE, buff=0.08))

        # Global 1:13:30.0 -> local 70.0; Global 1:13:46.0 -> local 86.0
        self.play_timed("pde_surrogate_global_interaction", 70.0, 86.0, FadeIn(surrogate, shift=UP * 0.04), FadeIn(global_label, shift=UP * 0.04))

        # Global 1:13:46.0 -> local 86.0; Global 1:14:02.0 -> local 102.0
        self.play_timed(
            "sharp_feature_limitation",
            86.0,
            102.0,
            FadeOut(regular),
            FadeOut(surrogate),
            FadeOut(global_label),
            FadeIn(sharp_demo, shift=UP * 0.05),
        )

        # Global 1:14:02.0 -> local 102.0; Global 1:14:20.0 -> local 120.0
        self.play_timed("hybrid_local_global_correction", 102.0, 120.0, FadeIn(hybrid, shift=UP * 0.04), Circumscribe(sharp_demo.sharp, color=WARNING, buff=0.08))

        # Global 1:14:20.0 -> local 120.0; Global 1:14:36.0 -> local 136.0
        semi = Chip("semi-generalized convolution", max_width=3.35, height=0.48, stroke_color=PURPLE, font_size=17).move_to(DOWN * 1.90)
        self.play_timed("semi_generalized_convolution", 120.0, 136.0, FadeIn(semi, shift=UP * 0.04), Circumscribe(pipeline.spectrum, color=PURPLE, buff=0.08))

        # Global 1:14:36.0 -> local 136.0; Global 1:14:53.0 -> local 153.0
        resolution = SafeText("higher resolution with fixed modes does not recover every small feature", max_width=7.2, max_height=0.34, font_size=21, color=WARNING).move_to(DOWN * 2.70)
        self.play_timed("fixed_modes_resolution_caveat", 136.0, 153.0, FadeIn(resolution, shift=UP * 0.04), sharp_demo.smooth.curve.animate.set_stroke(width=4.1))

        # Global 1:14:53.0 -> local 153.0; Global 1:15:40.0 -> local 200.0
        self.play_timed(
            "fno_strong_not_magic",
            153.0,
            180.0,
            FadeOut(resolution),
            FadeOut(sharp_demo.label),
            FadeIn(caveat, shift=UP * 0.05),
            Circumscribe(VGroup(formula, caveat), color=WARNING, buff=0.10),
        )
        self.play_timed("final_fno_read", 180.0, 199.8, Circumscribe(pipeline, color=SCIENCE, buff=0.10), rate_func=there_and_back)
        self.pad_to(self.SCENE_DURATION)
