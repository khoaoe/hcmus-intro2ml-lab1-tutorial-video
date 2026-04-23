# Machine Learning on Function Spaces: Neural Operators

This repository contains the source code for generating the Manim mathematical animations for the ICML 2024 presentation on Neural Operators. 

## Project Structure

The project is modularized by presentation section to ensure isolated rendering and easy maintenance:

* `src/`: Contains all scene definitions, split by section (`s01` through `s08`).
* `utils/`: Shared utilities, including global theme colors (`colors.py`), custom math Mobjects, and base scene classes.
* `assets/`: Directory for static assets like fonts, SVGs, and raster images.
* `notebooks/`: Jupyter notebooks designed for rapid prototyping of complex mathematical animations using the `%%manim` magic command.

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
```

## 🎬 How to Render the Videos

Once your environment is set up and activated (`conda activate manim_env`), you can render the scenes using the Manim command-line interface. 

### Basic Rendering Commands

Run the following commands from the root directory of the project. You must specify the path to the Python file and the exact name of the Scene class you want to render.

**1. Preview Quality (Fast rendering for testing)**
Use the `-ql` flag (Quality Low, 480p at 15fps). This is recommended while drafting to save time:

```bash
manim -ql src/s01_traditional_dl/scenes.py Scene1_1_Hook
```

**2. High Quality (Production ready)**
Use the `-qh` flag (Quality High, 1080p at 60fps). Use this for the final output:

```bash
manim -qh src/s01_traditional_dl/scenes.py Scene1_1_Hook
```

### Rendering All Scenes in a File

If a Python file contains multiple scenes (like `Scene1_1_Hook` and `Scene1_2_PlotTwist`) and you want to render all of them sequentially, replace the scene name with the `-a` (all) flag:

```bash
manim -qh src/s01_traditional_dl/scenes.py -a
```

### Common Flags Explained:

* `-p`: Plays the video automatically in your default media player after rendering is complete.
* `-q`: Specifies the render quality. Options include `l` (low), `m` (medium), `h` (high), and `k` (4K).
* `-a`: Renders all `Scene` classes found in the specified file.

*Note: All rendered output files (.mp4) will be automatically saved in the `media/videos/` directory within your project root.*
