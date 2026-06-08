# Machine Learning on Function Spaces: Neural Operators

This repository contains the source code for generating the Manim mathematical animations for the ICML 2024 presentation on Neural Operators. 

## Project Structure

The project is modularized by scene within the `neural_operators_manim/` working directory:

* `src/refined_scenes/`: **Production scene files** — all finalized Manim scenes, named by section and scene number (e.g., `scene_01_01_hook.py`, `scene_04_01_fno.py`).
* `src/common/`: Shared utilities including `theme.py` (global colors/config), `timing.py` (TimedScene base class), `safe_text.py`, `panels.py`, `visual_safety.py`, and `layout.py`.
* `docs/`: Production script (`full_voice_manim_script.md`), outline (`original_outline.tex`), ICML slide deck, and reference materials.
* `scripts/`: Helper scripts for duration verification (`verify_duration.py`), contact sheet generation (`make_contact_sheet.py`), and scene checking (`check_scene.py`).
* `reports/`: Generated reports, contact sheets, and visual QA outputs.
* `assets/`: Directory for static assets like fonts, SVGs, and raster images.

## ⚙️ Environment Setup & Dependencies

Manim requires both system-level binary dependencies (for video processing and text rendering) and a Python environment.

### 1. System Dependencies

To keep the host system clean and avoid conflicting binaries, we only install LaTeX system-wide.

**For Linux:**

```bash
sudo pacman -S texlive-basic texlive-latexextra texlive-fontsrecommended
```

### 2. Python Environment Setup

```bash
# 1. Create a dedicated conda environment
conda create -n manim_env python=3.10 -y

# 2. Activate the environment
conda activate manim_env

# 3. Install required Python packages
pip install manim numpy scipy jupyterlab
pip install -U manim
```

## 🎬 How to Render the Videos

Once your environment is set up and activated (`conda activate manim_env`), you can render the scenes using the Manim command-line interface. 

**Important:** All commands should be run from the `neural_operators_manim/` directory with `PYTHONPATH=.` so that shared modules are importable.

### Basic Rendering Commands

**1. Preview Quality (Fast rendering for testing)**
Use the `-ql` flag (Quality Low, 480p at 15fps). This is recommended while drafting to save time:

```bash
cd neural_operators_manim
PYTHONPATH=. manim -ql src/refined_scenes/scene_01_01_hook.py Scene0101_Hook
```

**2. High Quality (Production ready)**
Use the `-qh` flag (Quality High, 1080p at 60fps). Use this for the final output:

```bash
PYTHONPATH=. manim -qh src/refined_scenes/scene_01_01_hook.py Scene0101_Hook
```

### Scene Reference Table

| Scene File | Class Name | Duration |
|---|---|---|
| `scene_01_01_hook.py` | `Scene0101_Hook` | 45s |
| `scene_01_02_plot_twist.py` | `Scene0102_PlotTwist` | 60s |
| `scene_01_03_grid_mismatch.py` | `Scene0103_GridMismatch` | 45s |
| `scene_01_04_traditional_solvers.py` | `Scene0104_TraditionalSolvers` | 60s |
| `scene_01_05_key_question.py` | `Scene0105_KeyQuestion` | 30s |
| `scene_02_01_scientific_data.py` | `Scene0201_ScientificData` | 60s |
| `scene_02_02_image_not_function.py` | `Scene0202_ImageNotFunction` | 60s |
| `scene_02_03_from_dl_to_operator_learning.py` | `Scene0203_FromDLToOperatorLearning` | 60s |
| `scene_02_04_challenges_definition.py` | `Scene0204_ChallengesDefinition` | 50s |
| `scene_03_01_integral_derivative.py` | `Scene0301_IntegralDerivative` | 45s |
| `scene_03_02_mlp_to_integral.py` | `Scene0302_MLPToIntegral` | 60s |
| `scene_03_03_mlp_vs_no.py` | `Scene0303_MLPvsNO` | 60s |
| `scene_03_04_deep_no_errors.py` | `Scene0304_DeepNOErrors` | 60s |
| `scene_04_01_fno.py` | `Scene0401_FNO` | 75s |
| `scene_04_02_fno_properties.py` | `Scene0402_FNOProperties` | 45s |
| `scene_04_03_gno.py` | `Scene0403_GNO` | 75s |
| `scene_04_04_uno.py` | `Scene0404_UNO` | 75s |
| `scene_04_05_codano_spherical_deriv.py` | `Scene0405_CoDANO` | 75s |
| `scene_04_06_architecture_summary.py` | `Scene0406_ArchSummary` | 25s |
| `scene_05_01_fourcastnet.py` | `Scene0501_FourCastNet` | 105s |
| `scene_05_02_carbon_aero.py` | `Scene0502_CarbonAero` | 105s |
| `scene_05_03_md_pino.py` | `Scene0503_MDPINO` | 105s |
| `scene_05_04_gano_summary.py` | `Scene0504_GANOSummary` | 90s |
| `scene_06_01_openproblems_archphysics.py` | `Scene0601_OpenProblems` | 75s |
| `scene_06_02_theory_uq.py` | `Scene0602_TheoryUQ` | 75s |
| `scene_06_03_activelearning_rl.py` | `Scene0603_ActiveLearning_RL` | 75s |
| `scene_06_04_collaboration_recap.py` | `Scene0604_Collaboration_Recap` | 60s |
| `scene_06_05_resources_closing.py` | `Scene0605_Resources_Closing` | 30s |

### Rendering All Scenes

To render all scenes sequentially, you can use a simple loop:

```bash
cd neural_operators_manim
for f in src/refined_scenes/scene_*.py; do
  PYTHONPATH=. manim -ql "$f" -a
done
```

### Common Flags Explained:

* `-p`: Plays the video automatically in your default media player after rendering is complete.
* `-q`: Specifies the render quality. Options include `l` (low), `m` (medium), `h` (high), and `k` (4K).
* `-a`: Renders all `Scene` classes found in the specified file.

*Note: All rendered output files (.mp4) will be automatically saved in the `media/videos/` directory within the `neural_operators_manim/` project root.*
