# AGENTS.md — ICML Neural Operators Manim Production Guide

Repository: `hcmus-intro2ml-lab1-tutorial-video`  
Primary task: build a Manim animation-only Vietnamese voice-over video for the ICML 2024 tutorial  
**“Machine Learning on Function Spaces — Neural Operators.”**

---

## 0. Read this first

This repository is not a normal slide-to-video conversion project.

The goal is to create a complete animated lecture in a 3Blue1Brown-inspired style: intuitive, visual, research-level, mathematically faithful, and synchronized with Vietnamese narration.

Do **not** copy the original slides into Manim as static screenshots.  
Do **not** summarize slides mechanically.  
Do **not** redesign the narrative unless the user explicitly asks.

The production script is the source of truth. The code must serve the script.

---

## 1. Canonical production source

The most important file in this repository is:

```text
docs/full_voice_manim_script.md
```

This file contains the full Vietnamese voice-over, section structure, scene IDs, timestamps, visual direction, Manim scene notes, required animation objects, and voice production notes.

Before implementing any scene, always read the relevant scene from:

```text
docs/full_voice_manim_script.md
```

For each scene, extract:

- section number,
- scene ID,
- scene title,
- start time,
- end time,
- all VO lines,
- pause timings,
- visual / Manim direction,
- listed Manim objects,
- source anchor if present.

Never generate Manim code from memory. Always implement from the script.

---

## 2. Important timing clarification

The script header may mention a target duration around `58 phút 20 giây`, but the section timing overview and the final scene currently run until:

```text
1:58:20
```

Treat **individual scene timestamps** as authoritative.

For implementation:

- Scene duration must equal `scene_end_time - scene_start_time`.
- The full video duration should follow the scene table and final scene timing unless the user later edits the script.
- If total-duration metadata conflicts with per-scene timestamps, keep scene timestamps and report the mismatch.

Example:

```text
Scene 0.1: 00:00.0–00:42.0 => duration 42.0s
Scene 0.2: 00:42.0–02:20.0 => duration 98.0s
```

Do not compress a scene just because the animation content ends early. Hold the final composition, add subtle ambient motion, or use `pad_to(...)`.

---

## 3. Source priority

Use sources in this order:

1. `docs/full_voice_manim_script.md`
   - Canonical production script.
   - Controls narrative, scene order, timestamps, narration, visual beats, and required objects.

2. `docs/ICML-NeuralOperators-2024-Kamyar-Azizzadenesheli.pdf`
   - Original ICML tutorial slide deck.
   - Use for technical grounding, equations, figure references, architecture names, and tutorial flow.
   - Do not copy slide layouts directly.

3. `docs/presentation's-transcripts.txt`
   - Original tutorial transcript.
   - Use to understand speaker intent, nuance, and transitions.
   - Do not paste transcript text into narration unless the production script says so.

4. `docs/reference-papers'-links.txt`
   - Academic reference list.
   - Use for architecture lineage and paper names.

5. `docs/Neural-Operators-Library's-source-code.txt`
   - Context from the `neuraloperator` library.
   - Use for implementation vocabulary and technical grounding: FNO, GNO, GINO, UNO, CoDA-NO, SFNO, losses, datasets, layers.
   - Do not vendor library source code into the Manim project.

If sources conflict, follow `docs/full_voice_manim_script.md` first. If the script is ambiguous or internally inconsistent, preserve scene-level timing and report the issue.

---

## 4. Project objective

Create a polished Manim video that teaches the tutorial as an animated story.

Core thesis:

```text
Traditional deep learning mostly learns maps between finite-dimensional objects.
Scientific computing often needs maps between function spaces.
Neural operators learn function-to-function maps that can be discretization-aware.
```

The final lecture should explain:

- why images, text, and audio fit finite-dimensional deep learning,
- why weather, seismology, fluids, materials, molecules, medicine, and robotics often produce function-valued data,
- why visualized fields are not merely images,
- how traditional PDE solvers work and why they are powerful but expensive,
- the Darcy flow example and solution operator concept,
- why model output must be queryable as a function,
- the discretization challenge,
- the intuition of discretization-agnostic and discretization-convergent learning,
- Riemann sums and finite differences as prerequisites,
- the derivation from neural-network layers to integral operators,
- the full neural-operator architecture: lift, operator layers, project,
- residual connections, bias functions, measure/quadrature weights,
- approximation/generalization/discretization errors,
- GNO, FNO, basis projection, U-NO, Transformer Neural Operator, CoDA-NO, local/differential kernels,
- domains and open problems.

---

## 5. What this project is not

This project is not:

- a static slide video,
- a slide summary,
- a PDF recreation,
- a generic Neural Operator explainer detached from the ICML tutorial,
- a playground for flashy effects over correctness,
- a Manim demo where duration is approximate,
- a code-only repo without voice-over synchronization.

The video must be animation-first, narration-synchronized, and technically faithful.

---

## 6. Language and narration policy

Narration language: Vietnamese.

Keep English terms when they are standard or clearer, especially:

- Neural Operator
- operator learning
- function space
- solution operator
- discretization
- discretization-agnostic
- discretization-convergent
- PDE
- Riemann sum
- finite difference
- integral operator
- kernel
- residual connection
- Fourier Neural Operator / FNO
- Graph Neural Operator / GNO
- Transformer Neural Operator
- Codomain Attention / CoDA-NO
- universal approximation
- approximation error
- generalization error
- discretization error

Formula narration rule:

- Formulas are mostly visual.
- Voice-over should explain meaning, not read every symbol.
- Read short expressions only when useful, e.g. “G maps A to U.”

Do not rewrite Vietnamese VO unless the user explicitly asks.

---

## 7. Absolute timing contract

Every scene must be timestamp-driven.

A scene is wrong if:

- comments say `00:00–00:42`, but rendered duration is not 42 seconds,
- the script requires 45 seconds, but the render is 31 seconds,
- animation ends early and the scene cuts before the timestamp,
- timing is controlled only by rough `self.wait(1)` calls without target alignment,
- duration is not verified before reporting completion.

Required implementation pattern:

```python
class SceneXXX(TimedScene):
    SCRIPT_START = 0.0
    SCRIPT_END = 42.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        ...
        self.play_timed("beat_name", 0.0, 5.5, FadeIn(obj))
        self.wait_timed("pause", 5.5, 6.3)
        ...
        self.pad_to(self.SCENE_DURATION)
```

Important:

- Timings inside a scene are local to that scene.
- If the script line is global `[02:20.0–02:28.0]`, convert to local time by subtracting the scene start.
- Keep a comment mapping global timestamps to local timing.

Example:

```python
# Global 02:20.0–02:28.0 => local 0.0–8.0
self.play_timed("finite_world_intro", 0.0, 8.0, ...)
```

---

## 8. Visual quality contract

Every rendered scene must be checked visually before reporting completion.

A scene is wrong if:

- text overlaps other text, icons, frames, paths, or formulas,
- text overflows its intended card, chip, frame, or screen boundary,
- connection lines/arrows run through labels or primary objects in a confusing way,
- old objects remain visible under new objects after a transition,
- new objects start appearing before outgoing objects are visually clear when that causes overlap,
- layout reads as misaligned, cramped, clipped, or unintentionally stacked,
- animation timing technically matches but visual state looks wrong at any beat.

Implementation requirements:

- Keep readable margins at 16:9; do not place long text near frame edges unless it is fitted.
- Fit or wrap long labels inside cards/chips; never rely on default text width for long strings.
- Prefer staging transitions: fade old groups fully before introducing dense new groups when both would occupy the same region.
- Draw connectors behind objects, with low opacity, and route them around labels/icons. If a connector harms readability, remove it or replace it with a clearer motion cue.
- When using `Transform`, include every visible object that must move or fade; otherwise explicitly `FadeOut` stale objects before the next beat.
- After rendering, inspect the video across the full timeline, not only the final frame. Sample representative frames from all beats and check layout, overlap, overflow, alignment, spacing, text readability, animation transitions, and visual clarity.
- Do not mark a scene complete until duration verification and visual inspection both pass.

---

## 9. Timing helper requirements

If timing helpers do not exist, create them in a shared module such as:

```text
src/common/timing.py
```

Minimal contract:

```python
class TimedScene(Scene):
    def setup(self):
        self.t = 0.0

    def play_timed(self, label: str, start: float, end: float, *animations, **kwargs):
        if start < self.t - 1e-6:
            raise ValueError(f"{label}: start={start} before current time={self.t}")
        if start > self.t:
            self.wait(start - self.t)
        duration = end - start
        if duration <= 0:
            raise ValueError(f"{label}: non-positive duration")
        self.play(*animations, run_time=duration, **kwargs)
        self.t = end

    def wait_timed(self, label: str, start: float, end: float):
        if start < self.t - 1e-6:
            raise ValueError(f"{label}: start={start} before current time={self.t}")
        if start > self.t:
            self.wait(start - self.t)
        duration = end - start
        if duration > 0:
            self.wait(duration)
        self.t = end

    def pad_to(self, target_time: float):
        if target_time < self.t - 1e-6:
            raise ValueError(f"Scene exceeded target={target_time}; current={self.t}")
        if target_time > self.t:
            self.wait(target_time - self.t)
        self.t = target_time
```

You may improve this implementation, but do not weaken the contract.

Recommended additions:

- `global_to_local(global_time, scene_start)`
- `parse_timecode("1:07:40.0")`
- `assert_scene_duration(expected, actual, tolerance=0.25)`
- a render manifest mapping scene class to expected duration.

---

## 10. Render-duration verification

After rendering a scene, verify actual duration.

Use `ffprobe` if available:

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  media/videos/**/SceneName*.mp4
```

Or create a project helper:

```bash
python scripts/verify_duration.py media/videos --scene SceneName --expected 42.0
```

If `scripts/verify_duration.py` does not exist, implement it.

Do not claim a scene is production-ready without at least one of:

- successful render + duration check,
- or, if rendering is impossible in the current environment, syntax check plus a clear statement that render duration was not verified.

No fake “done.” Be explicit.

---

## 11. Existing repo structure rule

The existing modules `s01` through `s08` are experimental. Do not treat them as the required production architecture.

Before editing, inspect the repo:

```bash
git status -sb
git branch --show-current
find . -maxdepth 3 -type f | sort | sed 's#^\./##' | head -200
```

Rules:

- Do not assume the current branch.
- Do not overwrite experiments unless asked.
- Reuse existing utilities and repo conventions when useful.
- Prefer a clean production structure if the old structure is experimental.
- Keep changes small and reviewable.
- Do not add unrelated refactors while implementing a scene.

Suggested production structure, if compatible:

```text
.
├── AGENTS.md
├── docs/
│   ├── full_voice_manim_script.md
│   ├── ICML-NeuralOperators-2024-Kamyar-Azizzadenesheli.pdf
│   ├── presentation's-transcripts.txt
│   ├── reference-papers'-links.txt
│   └── Neural-Operators-Library's-source-code.txt
├── assets/
│   ├── images/
│   ├── icons/
│   ├── fields/
│   ├── meshes/
│   ├── equations/
│   └── audio/
├── src/
│   ├── common/
│   │   ├── theme.py
│   │   ├── timing.py
│   │   ├── layout.py
│   │   ├── math_objects.py
│   │   ├── function_visuals.py
│   │   └── operator_blocks.py
│   └── scenes/
│       ├── scene_00_01_from_pixels_to_fields.py
│       ├── scene_00_02_roadmap.py
│       ├── scene_01_01_finite_dimensional_comfort_zone.py
│       └── ...
└── scripts/
    ├── render_scene.sh
    ├── render_all.sh
    ├── verify_duration.py
    └── make_scene_stub.py
```

This is a recommendation, not a mandate. Follow actual repo conventions after inspection.

---

## 12. Shared Manim style and theme

Do not duplicate global Manim config or palette constants inside every scene.
Do not create scene-local versions of recurring visual motifs such as
background networks, cards, chips, arrows, vector columns, or operator boxes
when a shared helper exists or should exist. Put reusable consistency-critical
components in `neural_operators_manim/src/common/` and import them from scenes.
In particular, production scenes should use one canonical dark background color
and one canonical subtle background motif unless the script explicitly calls for
a different visual world.

Create or reuse:

```text
src/common/theme.py
src/common/layout.py
```

Canonical baseline:

```python
from manim import config

config.background_color = "#0B1020"
config.frame_width = 16
config.frame_height = 9

BG = "#0B1020"
CARD_BG = "#111827"
GRID = "#2A3346"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"

NVIDIA_GREEN = "#76B900"
INPUT = "#38BDF8"      # blue/cyan for input functions
OUTPUT = "#34D399"     # green for output functions
OPERATOR = "#FBBF24"   # yellow/gold for operators/kernels/arrows
WARNING = "#FB7185"    # red-pink for limitations/warnings
PURPLE = "#A78BFA"     # abstract spaces / latent states
```

Visual language:

- finite-dimensional vector: dots, bars, small grids, column vectors,
- function: continuous curve, surface, mesh field, sphere field,
- operator: glowing arrow or kernel lens,
- neural network: finite node graph,
- neural operator: integral-kernel lens transforming input field into output field,
- discretization: coarse mesh → fine mesh → continuum limit.

Recurring motifs from the script:

- `VectorWorld`
- `FunctionWorld`
- `SolutionOperator`
- `Discretization`
- `KernelLens`

Use these names in code where reasonable.

---

## 13. Visual style target

Aim for 3Blue1Brown-like clarity:

- smooth transformations,
- few objects on screen at once,
- mathematical meaning before decoration,
- consistent color semantics,
- dark background,
- object permanence across transformations,
- readable equations,
- camera movement only when it helps reasoning,
- animation beats aligned to voice-over.

Avoid:

- excessive particles,
- clutter,
- too many simultaneous labels,
- random colors,
- screenshot-driven scenes,
- unreadable tiny equations,
- over-stylized assets that hide the concept.

Hierarchy:

1. Technical correctness.
2. Timing synchronization.
3. Visual clarity.
4. Code modularity.
5. Polish.

If forced to choose, pick correctness and timing.

---

## 14. Manim implementation standards

Generated code must be runnable from the repository root.

Required:

- Use Manim Community Edition unless repo config says otherwise.
- Keep scenes modular.
- Use explicit scene class names.
- Map class/file names to script scene IDs.
- Add comments mapping visual beats to script timestamps.
- Use deterministic random seeds for generated points/fields.
- Avoid hidden dependencies.
- Avoid internet downloads at render time.
- Avoid absolute local paths.
- Avoid hardcoding assets outside repo.
- Use Manim primitives or generated vector graphics where possible.
- Use images only as supporting textures/backgrounds, not as the main explanation.

Object naming:

Good:

```python
input_function_curve
solution_operator_arrow
kernel_lens
coarse_grid_samples
function_space_A
function_space_U
```

Bad:

```python
m1
tmp
thing
obj2
aaa
```

---

## 15. Scene file template

Recommended structure:

```python
"""
Scene 0.1 — From pixels to fields
Script: docs/full_voice_manim_script.md
Global time: 00:00.0–00:42.0
Local duration: 42.0s
"""

from manim import *
from src.common.timing import TimedScene
from src.common.theme import *
from src.common.function_visuals import make_sphere_field, make_pixel_grid


class Scene0001FromPixelsToFields(TimedScene):
    SCRIPT_ID = "0.1"
    SCRIPT_TITLE = "From pixels to fields"
    SCRIPT_START = 0.0
    SCRIPT_END = 42.0
    SCENE_DURATION = 42.0

    def construct(self):
        # Global 00:00.0–00:05.5 => local 0.0–5.5
        ...
        self.play_timed("opening_question", 0.0, 5.5, FadeIn(...))

        # Global 00:05.5–00:06.3 => local 5.5–6.3
        self.wait_timed("pause_after_question", 5.5, 6.3)

        ...
        self.pad_to(self.SCENE_DURATION)
```

---

## 16. Production workflow for any scene

When implementing a scene:

1. Read the exact scene in `docs/full_voice_manim_script.md`.
2. Extract global start and end time.
3. Convert global VO line timestamps to local scene timings.
4. Inspect existing utilities.
5. Create/reuse shared visual objects.
6. Implement the scene with `TimedScene`.
7. Syntax-check.
8. Render at low quality first.
9. Verify actual duration.
10. Report changed files, render command, test command, measured duration, and unresolved issues.

Do not skip steps 1, 7, 9.

---

## 17. Render commands

Prefer commands from repo root.

Examples:

```bash
python -m compileall src
manim -pql src/scenes/scene_00_01_from_pixels_to_fields.py Scene0001FromPixelsToFields
manim -pqh src/scenes/scene_00_01_from_pixels_to_fields.py Scene0001FromPixelsToFields
```

If using a different structure, document the command in the response.

For batch rendering, maintain a manifest:

```text
scene_id | class_name | file | expected_duration
0.1      | Scene0001FromPixelsToFields | src/scenes/... | 42.0
0.2      | Scene0002Roadmap            | src/scenes/... | 98.0
```

---

## 18. TTS and audio alignment

The script says each VO line is independently recordable.

Audio production rules:

- Do not generate one giant audio file for the whole video.
- Prefer one audio file per scene.
- If a scene is longer than 2 minutes, split by VO lines or logical blocks.
- Keep explicit pauses as actual silence, not only punctuation.
- If voice duration differs from planned duration by more than 5%, report it before retiming.
- Retiming must preserve scene structure and not silently desync visual beats.
- Formulas are mostly visual; narration describes meaning.

Recommended audio layout:

```text
assets/audio/
  scene_00_01/
    vo_0000_0005_5.wav
    pause_0005_5_0006_3.wav
    ...
  scene_00_02/
    ...
```

---

## 19. Conceptual correctness guardrails

### 18.1 Traditional deep learning

Conventional deep learning usually learns maps between finite-dimensional objects:

```text
f: R^n -> R^m
```

Images, tokens, audio samples, embeddings, and labels are usually represented as vectors/tensors.

Do not overclaim that standard ML cannot handle scientific data. The point is more precise: standard architectures often assume fixed discretizations and finite-dimensional tensor shapes, while scientific fields often require continuum-aware behavior.

### 18.2 Function-valued data

Many scientific/engineering data are functions over domains:

- weather fields on a sphere,
- seismic waves in subsurface volumes,
- pressure/velocity fields around cars or aircraft,
- molecular trajectories,
- material deformation fields,
- tissue imaging fields,
- plasma evolution,
- robotics trajectories.

These may be visualized as images/videos, but they are not merely images/videos. Domain, geometry, derivatives, integrals, and physical laws matter.

### 18.3 Traditional solvers

Traditional numerical solvers are powerful and data-efficient. Do not portray them as obsolete.

They use:

- PDEs,
- conservation laws,
- boundary/initial conditions,
- finite difference,
- finite volume,
- finite element,
- spectral methods.

Limitations include:

- modeling unknown physics,
- parameterization error,
- massive compute at high resolution,
- difficulty with differentiability/inverse problems,
- barrier to entry,
- difficulty incorporating real data and domain knowledge.

ML complements solvers; it does not magically replace all scientific computing.

### 18.4 Solution operator

For PDE problems, the solution operator maps an input function to an output solution function.

Darcy example:

```text
input:  a(x)  diffusion/permeability coefficient field
output: u(x)  solution field
operator: G: A -> U
```

The operator-learning question:

```text
Given many pairs (a_i, u_i), can we learn G?
```

### 18.5 Discretization

Scientific data may be given on:

- regular grids,
- irregular meshes,
- point clouds,
- sparse sensors,
- different train/test resolutions,
- different input/output meshes,
- domains such as surfaces, volumes, spheres, or geometry-dependent meshes.

A neural operator should be designed around the continuum relationship, with discretization as observation/computation.

### 18.6 Discretization-convergent intuition

A discretization-convergent model should not merely “run” at different resolutions. As the mesh is refined, predictions should approach a consistent continuum limit.

Distinguish:

```text
runs on resized input      != discretization-convergent
works on many tensor sizes != learns a continuum operator
```

### 18.7 From neural networks to integral operators

Core derivation:

1. Start with a finite-dimensional neural network layer.
2. Interpret input vector entries as samples `a(x_j)` of a function.
3. Replace matrix entries `K_ij` with kernel values `κ(y_i, x_j)`.
4. Replace normalized sums with weighted Riemann sums.
5. Take the continuum limit.
6. Get a linear integral operator.
7. Add pointwise nonlinearity.
8. Add residual connection, bias function, and measure/quadrature weights.
9. Stack layers to form a deep neural operator.

Keep this derivation visually clear. It is the conceptual core of the video.

### 18.8 Full neural-operator architecture

Standard high-level structure:

```text
a(x) -> pointwise lift P -> operator layers -> pointwise projection Q -> u(x)
```

Operator layers may include:

```text
integral transform + residual/skip + bias function + nonlinearity
```

### 18.9 Error analysis

For operator learning, remember:

- approximation error,
- generalization error,
- discretization error.

Do not evaluate only on a fixed grid and claim full operator validity. Same-grid evaluation checks only part of the story.

### 18.10 Universal approximation

Neural operators have universal approximation results under regularity assumptions.

Use this carefully:

- It supports expressivity.
- It does not guarantee easy training.
- It does not guarantee enough data.
- It does not solve metrics, physics, OOD, chaos, or uncertainty.

---

## 20. Architecture vocabulary

Use names accurately.

### GNO / Kernel Neural Operator

- Kernel is parameterized directly, often by a neural network.
- Works naturally with point clouds and irregular geometry.
- Message passing resembles GNNs but is tied to metric/domain discretization.
- Can be local or global.
- Needs quadrature/measure awareness for discretization consistency.

### FNO / Fourier Neural Operator

- Uses Fourier basis / spectral transform.
- Applies learned weights to selected Fourier modes.
- Efficient on regular grids via FFT.
- Good for global interactions.
- Can struggle with sharp local features, discontinuities, boundaries, or geometry where Fourier basis is not natural.

### SFNO / Spherical FNO

- Uses spherical harmonics or sphere-aware basis.
- Useful for weather/climate on spherical domains.

### Basis projection operators

- Project input function to basis coefficients.
- Manipulate coefficients.
- Project back to output representation.
- Basis choice encodes assumptions about domain and regularity.

### U-NO / Multipole / multiscale operators

- Use multiscale domain contraction/expansion.
- Similar spirit to U-Net but in operator-learning language.
- Useful for near/far and multi-resolution interactions.

### Transformer Neural Operator

- Interprets attention as an integral-like weighted sum over function samples.
- Must account for measure/quadrature factors, especially on irregular grids.

### CoDA-NO / Codomain Attention

- Treats physical variables as function-valued tokens.
- Useful for multiphysics and datasets with different variable subsets.
- Requires variable-specific encoding.

### Local / differential kernels

- Capture local physics and derivative-like behavior.
- Must scale correctly with grid spacing to have a continuum-consistent interpretation.

Do not invent architecture claims beyond the production script and sources.

---

## 21. Scene-by-scene implementation map

The script currently has these sections:

```text
0. Cold open
1. What traditional deep learning already solved
2. Real-world data are functions
3. Traditional scientific computing
4. Learn the solution operator
5. Discretization challenge
6. Neural operators
7. Pre-req: integrals and derivatives
8. From neural networks to neural operators
9. Full neural operator architecture
10. Architectures
11. Domains, not just applications
12. Open problems
13. Closing
```

Use this order. Do not implement scenes according to old experimental module names.

If old folders `s01` to `s08` exist, treat them as experiments only.

---

## 22. Asset policy

Allowed:

- Manim primitives,
- generated meshes,
- generated fields,
- simple SVG icons created in-repo,
- small local images when needed,
- public-domain or self-created assets,
- extracted visual references only when legally and practically appropriate.

Avoid:

- large external assets,
- internet downloads at render time,
- raw slide screenshots as main visuals,
- copyrighted visual-heavy copying from the slide deck,
- hardcoded absolute paths,
- assets outside repo.

If using original slide deck imagery, use it as reference, not as the final visual language.

---

## 23. Git safety

Before making changes:

```bash
git status -sb
git branch --show-current
```

Rules:

- Do not use `git reset --hard`.
- Do not use `git clean -fd`.
- Do not delete user work.
- Do not commit unless asked.
- Do not change unrelated files.
- Do not move large folders unless asked.
- Do not add secrets or API keys.
- Do not add generated media to git unless the repo intentionally tracks renders.
- Keep patches reviewable.

---

## 24. Quality checklist before reporting done

For every scene:

- [ ] Read exact scene from `docs/full_voice_manim_script.md`.
- [ ] Used correct scene ID and title.
- [ ] Used exact global timestamps.
- [ ] Converted timestamps to local scene time.
- [ ] Used shared `theme.py`.
- [ ] Used shared `TimedScene` or equivalent.
- [ ] No duplicated global palette/config in scene file.
- [ ] Visual beats match VO lines.
- [ ] Required Manim objects are represented or intentionally adapted.
- [ ] Scene can be rendered from repo root.
- [ ] Syntax check passed.
- [ ] Render check passed, or inability to render is clearly reported.
- [ ] Actual video duration measured.
- [ ] Duration matches expected within tolerance.
- [ ] No slide screenshot dependency as the main explanation.
- [ ] No unrelated files changed.

A scene is not production-ready if duration is unverified.

---

## 25. Response format for coding tasks

When reporting back to the user, use this structure:

```text
Done. I implemented Scene X.Y — <title>.

Changed:
- <file>
- <file>

Checked:
- <command>
- <command>
- Expected duration: <N>s
- Actual duration: <N>s

Run:
- <render command>

Notes:
- <any assumptions or unresolved issues>
```

If render was not possible:

```text
I could not verify render duration in this environment.
I did run:
- python -m compileall src
The expected duration is <N>s from docs/full_voice_manim_script.md.
Please run:
- <render command>
- <ffprobe command>
```

Do not hide uncertainty.

---

## 26. Specific lesson from the Scene 1 issue

A previous implementation rendered a scene around 31 seconds even though the script required a longer target.

Do not repeat this.

For every scene:

- scene duration is binding,
- add `pad_to(...)`,
- verify with `ffprobe`,
- if animation ends early, hold final composition or add subtle ambient motion,
- do not claim completion until timing is checked.

This is a hard rule.

---

## 27. Preferred implementation strategy

Start with shared infrastructure before building many scenes:

1. `src/common/theme.py`
2. `src/common/timing.py`
3. `src/common/layout.py`
4. `src/common/function_visuals.py`
5. `src/common/operator_blocks.py`
6. `scripts/verify_duration.py`
7. first production scene from the script.

Do not over-engineer, but avoid copy-paste chaos.

Build reusable components for:

- pixel grids,
- token sequences,
- function curves,
- sampled functions,
- mesh refinement,
- function-space blobs,
- operator arrows,
- kernel lenses,
- Riemann rectangles,
- finite difference stencils,
- Fourier spectrum bars,
- architecture blocks,
- domain montage panels,
- warning/error cards.

---

## 28. Naming convention

Recommended file naming:

```text
src/scenes/scene_00_01_from_pixels_to_fields.py
src/scenes/scene_00_02_roadmap.py
src/scenes/scene_01_01_finite_dimensional_comfort_zone.py
```

Recommended class naming:

```python
Scene0001FromPixelsToFields
Scene0002Roadmap
Scene0101FiniteDimensionalComfortZone
```

Use names that sort naturally and map to the script.

---

## 29. Mathematical notation policy

Use readable MathTex.

Prefer:

```python
MathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}")
MathTex(r"u = \mathcal{G}(a)")
MathTex(r"\int_D \kappa(y,x)a(x)\,dx")
```

Avoid giant equations unless they are central to the beat.

When an equation is too dense:

- show only the meaningful part,
- animate its transformation,
- explain it visually.

---

## 30. Handling source conflicts

If the script, slide deck, transcript, or code context disagree:

1. Follow the production script for narrative/timing.
2. Use slide deck/transcript to check technical meaning.
3. Use reference papers/library context for terminology.
4. Report the discrepancy if it affects correctness.

Never silently “fix” the narrative flow.

---

## 31. Final philosophy

This project is about making a technically correct, synchronized, beautiful explanation of Neural Operators.

The key question throughout the video:

```text
When data are functions, how must machine learning change?
```

Every scene should help answer that question.

Keep the stack sane:

```text
correct concept -> exact timing -> clear animation -> clean code -> polish
```

No vibes-only Manim. No timing roulette. No slide karaoke.
