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