# AGENTS.md — ICML Neural Operators Manim Production Guide

Repository: `hcmus-intro2ml-lab1-tutorial-video`  
Working project root: `hcmus-intro2ml-lab1-tutorial-video/neural_operators_manim`  
Primary task: build a polished Manim animation-only Vietnamese voice-over video for the ICML 2024 tutorial:

```text
Machine Learning on Function Spaces — Neural Operators
```

This file is the operating contract for coding agents working on this repo.

---

## 0. Non-negotiable mission

Create a complete animated lecture, not a slide conversion.

The final video must be:

- animation-first,
- synchronized with Vietnamese voice-over,
- technically faithful to the ICML Neural Operators tutorial,
- visually clean enough for a research-level classroom presentation,
- implemented scene-by-scene with exact timing,
- verified by render duration and visual QA.

Do **not** copy the slide deck as static screenshots.  
Do **not** summarize slides mechanically.  
Do **not** redesign the narrative unless the user explicitly asks.  
Do **not** report a scene as done after syntax check only.

---

## 1. Operating model

Use this workflow by default:

```text
ChatGPT = technical director / researcher / storyboard writer / prompt engineer / QA reviewer
Codex    = implementation agent / render runner / visual-fix executor
Repo     = gatekeeper through scripts, tests, duration checks, and contact sheets
```

Codex should implement code only after the scene has a clear implementation spec or storyboard.

For visually complex scenes, do **not** jump directly into full animation. First create or follow a static keyframe plan.

---

## 2. Source of truth

The canonical production script is:

```text
../docs/full_voice_manim_script.md
```

Relative to the working project root:

```text
hcmus-intro2ml-lab1-tutorial-video/neural_operators_manim
```

the script is at:

```text
../docs/full_voice_manim_script.md
```

This file controls:

- section order,
- scene IDs,
- scene titles,
- global timestamps,
- Vietnamese narration,
- pauses,
- visual beats,
- Manim direction,
- required animation objects.

Before implementing any scene, read the exact scene from this file.

Never generate scene code from memory.

---

## 3. Supporting sources

Use these only for grounding and technical correctness:

```text
../docs/ICML-NeuralOperators-2024-Kamyar-Azizzadenesheli.pdf
../docs/presentation's-transcripts.txt
../docs/reference-papers'-links.txt
../docs/Neural-Operators-Library's-source-code.txt
```

Source priority:

1. `full_voice_manim_script.md`
2. ICML slide deck
3. transcript
4. reference papers
5. neuraloperator source-code context

If sources conflict, follow the production script for narrative and timing. Use supporting sources only to clarify meaning, equations, terminology, or architecture details.

---

## 4. Actual project root

The production Manim code lives inside:

```text
hcmus-intro2ml-lab1-tutorial-video/neural_operators_manim
```

Run implementation, tests, and render commands from this directory unless a command explicitly says otherwise.

At the start of a coding session:

```bash
cd hcmus-intro2ml-lab1-tutorial-video/neural_operators_manim
git status -sb
git branch --show-current
find . -maxdepth 3 -type f | sort | sed 's#^\./##' | head -200
```

Do not assume the current branch.  
Do not overwrite user experiments unless asked.

---

## 5. Hard priority stack

When trade-offs appear, use this order:

1. Correct concept
2. Faithfulness to `full_voice_manim_script.md`
3. Exact scene timing
4. Visual clarity
5. Runnable/renderable code
6. Verified duration
7. Modular implementation
8. Polish

Visual effects never outrank correctness, timing, or readability.

---

## 6. Definition of done

A scene is done only if all required checks pass:

```text
[ ] exact scene read from full_voice_manim_script.md
[ ] global timestamps extracted
[ ] local timestamps computed
[ ] visual storyboard/keyframes defined for dense scenes
[ ] code implemented with shared timing/layout helpers
[ ] syntax check passes
[ ] unit/contract tests pass
[ ] low-quality render succeeds
[ ] actual duration is verified
[ ] keyframes/contact sheet generated
[ ] visual QA passes
[ ] unresolved issues are reported honestly
```

A scene is **not** done if:

- duration is unverified,
- only syntax check was run,
- the scene renders but has visible overlap/overflow,
- visual QA was skipped,
- contact sheet/keyframes were not inspected for dense scenes.

No fake “done.” Report uncertainty.

---

## 7. Absolute timing contract

Every scene must be timestamp-driven.

Scene duration is binding:

```text
scene_duration = scene_end_time - scene_start_time
```

Use local time inside each scene:

```text
local_time = global_time - scene_start_time
```

Example:

```text
Scene 2.3 global: 10:45.0–12:55.0
Scene start: 645.0s
Scene end:   775.0s
Duration:    130.0s

Global 10:55.5 -> local 10.5
Global 11:07.0 -> local 22.0
```

A scene fails timing if:

- script requires 130 seconds but render is 98 seconds,
- animation ends early and scene cuts before target time,
- rough `self.wait(1)` calls are used instead of target alignment,
- `pad_to(...)` is missing,
- duration is not verified.

---

## 8. Timing helper requirement

Use `TimedScene` or `TimedThreeDScene` from shared timing utilities.

Required API:

```python
self.play_timed(label, start, end, *animations, **kwargs)
self.wait_timed(label, start, end)
self.pad_to(target_time)
```

Required behavior:

- reject negative or zero-duration beats,
- reject beats that start before current local scene time,
- wait automatically if a beat starts after current scene time,
- use exact `run_time=end-start`,
- fail if `pad_to(...)` target is already exceeded.

Do not weaken this contract.

Preferred shared file:

```text
src/common/timing.py
```

Recommended helpers:

```python
parse_timecode("1:07:40.0")
global_to_local(global_seconds, scene_start_seconds)
assert_scene_duration(expected, actual, tolerance=0.25)
```

---

## 9. Render-duration verification

After rendering, verify actual duration.

Preferred command:

```bash
python scripts/verify_duration.py media/videos --scene <SceneClassName> --expected <seconds>
```

If needed, use `ffprobe`:

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  media/videos/**/<SceneClassName>*.mp4
```

Do not claim production readiness without measured duration.

---

## 10. Visual Production Gate v2

Syntax and duration are necessary but not sufficient.

Every production scene must pass visual QA.

A scene visually fails if:

- text overlaps other text,
- text overflows cards/chips/panels,
- formulas are clipped or unreadable,
- objects leave the frame unintentionally,
- arrows or connectors cross labels or important objects,
- stale objects remain visible after transitions,
- scene layout is cramped, misaligned, clipped, or unintentionally stacked,
- a dashboard layout contains too much simultaneous information,
- camera movement hurts readability,
- old visual states remain under new visual states.

For dense scenes, implement in two passes:

```text
Pass 1: static keyframes / debug layout
Pass 2: full animation
```

Do not implement full animation first for dense scenes.

Dense scenes include scenes with:

- four or more panels,
- multiple formulas and labels,
- montage layouts,
- 3D objects plus labels,
- final summary dashboards,
- architecture diagrams,
- derivation steps with many moving symbols.

---

## 11. Visual System v2

Production scene code should use reusable visual components.

Required shared modules:

```text
src/common/safe_text.py
src/common/panels.py
src/common/visual_safety.py
src/common/keyframes.py
src/common/layout.py
src/common/theme.py
```

If these files do not exist, create them before implementing more dense scenes.

Required components:

```text
SafeText
SafeMathTex
Chip
PanelCard
PanelGrid
FocusStage
VisualSafety
```

Scene files should describe intent. They should not manually micromanage every pixel.

Avoid raw long text placement in scenes. Use safe wrappers.

---

## 12. Text and formula safety

Do not use raw `Text`, `Paragraph`, or `MathTex` directly for long labels, chips, captions, card titles, or explanatory text.

Use wrappers:

```python
SafeText(...)
SafeMathTex(...)
Chip(...)
```

Safe wrappers must:

- accept max width,
- accept max height when appropriate,
- reduce font size within a minimum readable limit,
- wrap or reject text that still does not fit,
- never silently overflow,
- expose mobjects that can be checked by visual safety assertions.

Minimum practical readability:

```text
Main title:      36–52
Panel title:     26–34
Caption/chip:    16–24
Formula:         24–40
Tiny labels:     avoid below 14
```

If a label cannot fit, shorten it or move it to narration. Do not shrink it into unreadable dust.

### Text inside boxes, chips, and panels

Most recurring typography bugs come from treating text labels as geometry that can be squeezed into a box. For all production scenes:

- Use the shared text/container helpers (`SafeText`, `SafeMathTex`, `Chip`, `PanelCard`) for labels inside cards, chips, badges, tabs, stamps, and panels. Do not hand-build `RoundedRectangle + Text` for UI labels unless you are also following the same helper contract.
- For plain UI labels such as `change mesh`, `query anywhere`, `solve u`, or `predict u`, use `SafeText`/`Chip`, not `MathTex` or raw `Text`.
- Create text first, measure the rendered `text.width`/`text.height`, then size the box from real text dimensions plus padding. Never estimate text width with `len(label)` or fixed character-count formulas.
- Fit overflowing text only by reducing font size or applying uniform scaling. Never use `stretch_to_fit_width`, `stretch_to_fit_height`, `.stretch(...)`, direct `text.width = ...`, direct `text.height = ...`, or `space_out_submobjects(...)` on text.
- Do not call `.arrange(...)` directly on a `Text` object; `Text` is character-submobject based. Arrange groups of separate text objects, not the glyphs inside one label.
- Avoid scaling a `VGroup` that contains both a box and its text after the box/text layout is finalized, except for intentional whole-scene uniform scaling followed by visual QA.
- Every rendered contact sheet must include a check for broken letter spacing inside chips/cards/panels. If spacing looks wrong, fix the shared helper first, not each scene locally.

---

## 13. Layout safety

Use frame-safe margins.

For 16:9 frame:

```text
frame width:  16
frame height: 9
safe margin:  0.35–0.50
```

No important object should exceed the safe frame.

Use `VisualSafety` checks where possible:

```python
VisualSafety.assert_in_frame(mobject, margin=0.35)
VisualSafety.assert_inside(child, parent, padding=0.12)
VisualSafety.assert_no_overlap(a, b, min_gap=0.05)
VisualSafety.assert_all_in_frame(group, margin=0.35)
```

Connectors:

- route behind objects,
- use low opacity,
- avoid crossing labels,
- remove them if they reduce readability.

Layering:

- background motifs below all content,
- connectors behind labels,
- labels above panels,
- active focus object above faded context.

---

## 14. Visual density budget

Each beat should have one main idea.

Default maximum per frame:

```text
main idea:        1
large panels:     1
mini panels:      <= 4
formulas:         <= 2
chips:            <= 4
long text blocks: <= 1
```

If more information is needed, stage it over time.

Avoid “dashboard cosplay”: four panels, many chips, formulas, arrows, and summary text all visible at once.

For four-panel overview beats:

- mini panels may show icon + title + one formula,
- no long internal chips,
- no dense text inside mini panels,
- details must have been introduced earlier or appear later in focus view.

---

## 15. Keyframes and contact sheets

For visually dense scenes, create a keyframe plan before full animation.

A keyframe plan must list:

```text
keyframe id
local timestamp
visual focus
visible objects
layout type
text budget
forbidden clutter
```

Example:

```text
KF01 | 0.0s   | CFD focus only       | single panel
KF02 | 10.5s  | Material focus only  | single panel
KF03 | 22.0s  | Molecule focus only  | single panel
KF04 | 35.0s  | Robotics focus only  | single panel
KF05 | 48.0s  | Four mini panels     | low-detail overview
KF06 | 61.0s  | Physics operations   | center focus
KF07 | 85.0s  | Model contract       | left/right cards
```

After render, generate a contact sheet.

Preferred command:

```bash
python scripts/make_contact_sheet.py \
  --video <rendered_video.mp4> \
  --out reports/<scene_id>/contact_sheet.jpg \
  --timestamps <comma-separated-local-times>
```

If `scripts/make_contact_sheet.py` does not exist, create it.

For any dense scene, do not report done without a contact sheet path.

---

## 16. One-command scene check

Create and maintain:

```text
scripts/check_scene.py
```

Preferred usage:

```bash
python scripts/check_scene.py \
  --scene <SceneClassName> \
  --file src/scenes/<scene_file>.py \
  --expected <seconds>
```

This script should run:

```text
1. python -m compileall src tests
2. python -m unittest discover tests
3. manim -ql <scene_file> <SceneClassName>
4. scripts/verify_duration.py
5. scripts/make_contact_sheet.py when timestamps are provided
6. visual safety report when available
```

Output should go to:

```text
reports/<scene_id>/
  duration.txt
  contact_sheet.jpg
  visual_report.md
  keyframes/
```

---

## 17. Scene implementation workflow

For each scene:

1. Read exact scene from `../docs/full_voice_manim_script.md`.
2. Extract:
   - section number,
   - scene ID,
   - title,
   - global start/end,
   - VO lines,
   - pauses,
   - visual direction,
   - required Manim objects.
3. Convert all global timestamps to local timestamps.
4. Decide whether the scene is dense.
5. If dense, create or follow a visual storyboard/keyframe plan.
6. Reuse shared visual components.
7. Implement using `TimedScene` or `TimedThreeDScene`.
8. Run syntax and unit tests.
9. Render low quality.
10. Verify duration.
11. Generate contact sheet for dense scenes.
12. Fix visual issues.
13. Report exact commands and unresolved issues.

Do not skip steps 1, 3, 8, 10.

---

## 18. Scene file template

Use this pattern:

```python
"""
Scene X.Y — <title>
Script: ../docs/full_voice_manim_script.md
Global time: HH:MM.S–HH:MM.S
Local duration: N.Ns
"""

from manim import *

from src.common.timing import TimedScene
from src.common.theme import *
from src.common.safe_text import SafeText, SafeMathTex
from src.common.panels import PanelCard, Chip
from src.common.visual_safety import VisualSafety


class SceneXXYYTitle(TimedScene):
    SCRIPT_ID = "X.Y"
    SCRIPT_TITLE = "<title>"
    SCRIPT_START = <seconds>
    SCRIPT_END = <seconds>
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # Global HH:MM.S–HH:MM.S => local A.B–C.D
        ...
        self.play_timed("beat_name", A, C, ...)
        ...
        self.pad_to(self.SCENE_DURATION)
```

Every beat should have a meaningful label.

---

## 19. Project structure

Recommended production structure:

```text
neural_operators_manim/
├── manim.cfg
├── requirements.txt
├── reports/
├── scripts/
│   ├── verify_duration.py
│   ├── make_contact_sheet.py
│   ├── check_scene.py
│   └── render_scene.sh
├── src/
│   ├── common/
│   │   ├── theme.py
│   │   ├── timing.py
│   │   ├── layout.py
│   │   ├── safe_text.py
│   │   ├── panels.py
│   │   ├── visual_safety.py
│   │   ├── keyframes.py
│   │   ├── function_visuals.py
│   │   └── operator_blocks.py
│   └── scenes/
│       ├── scene_00_01_from_pixels_to_fields.py
│       ├── scene_00_02_roadmap.py
│       └── ...
└── tests/
    ├── test_scene_00_01_contract.py
    └── ...
```

The old modules `s01` through `s08`, if present, are experimental. Do not treat them as required production structure.

---

## 20. Shared theme

Use one canonical theme.

Create or reuse:

```text
src/common/theme.py
```

Baseline:

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
INPUT = "#38BDF8"
OUTPUT = "#34D399"
OPERATOR = "#FBBF24"
WARNING = "#FB7185"
PURPLE = "#A78BFA"
```

Do not duplicate palette constants inside scene files.

Color semantics:

```text
INPUT        = input functions / observed fields
OUTPUT       = output functions / solutions
OPERATOR     = operators / kernels / maps
WARNING      = limitations / errors / caveats
PURPLE       = latent/function-space abstractions
MUTED        = context / inactive elements
```

---

## 21. Visual language

Use recurring motifs consistently:

```text
VectorWorld      = finite grid, pixels, tokens, vectors
FunctionWorld    = continuous curve, surface, field, mesh
SolutionOperator = glowing map from input function to output function
Discretization   = coarse mesh -> fine mesh -> continuum limit
KernelLens       = kernel/integral operator transforming fields
```

Preferred representations:

- finite-dimensional vector: dots, bars, small grids, column vectors,
- function: continuous curve, surface, mesh field, sphere field,
- operator: glowing arrow or kernel lens,
- neural network: finite node graph,
- neural operator: integral-kernel lens,
- discretization: mesh refinement sequence.

---

## 22. Manim coding standards

Required:

- Manim Community Edition unless repo config says otherwise.
- Code runnable from project root.
- Modular scene files.
- Explicit scene class names.
- Deterministic random seeds.
- No internet access during render.
- No absolute local paths.
- No hidden dependencies.
- No large generated media committed unless asked.
- No duplicated palette/config in scene files.
- No old objects left on screen unintentionally.

Naming:

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

## 23. 3D scene standards

Use 3D only when it adds meaning.

For 3D scenes:

- keep labels in screen space when possible,
- avoid tiny 3D text,
- avoid camera moves while dense labels are visible,
- render keyframes early,
- use simple geometry over complex decorative meshes,
- prefer clear layered volumes/surfaces to “realistic” but unreadable objects.

If a 3D object looks confusing or fake, simplify it into a 2.5D diagram.

Visual clarity beats realism.

---

## 24. Asset policy

Allowed:

- Manim primitives,
- generated vector graphics,
- generated fields/meshes,
- local repo assets,
- simple SVG icons created in-repo,
- small supporting textures when necessary.

Avoid:

- internet downloads at render time,
- raw slide screenshots as main visuals,
- hardcoded absolute paths,
- assets outside repo,
- large copyrighted visuals,
- cluttered borrowed diagrams.

Use slide deck imagery as reference, not as the final visual language.

---

## 25. Narration and language policy

Narration language: Vietnamese.

Do not rewrite Vietnamese VO unless the user explicitly asks.

Keep standard English terms when clearer:

```text
Neural Operator
operator learning
function space
solution operator
discretization
discretization-agnostic
discretization-convergent
PDE
Riemann sum
finite difference
integral operator
kernel
residual connection
Fourier Neural Operator / FNO
Graph Neural Operator / GNO
Transformer Neural Operator
Codomain Attention / CoDA-NO
universal approximation
approximation error
generalization error
discretization error
```

Formula narration rule:

- formulas are mostly visual,
- voice-over explains meaning,
- do not read every symbol unless useful.

---

## 26. TTS and audio alignment

The production script assumes each VO line is independently recordable.

Audio rules:

- prefer one audio file per scene or per VO block,
- keep explicit pauses as silence,
- do not generate one giant audio file for the whole video,
- if TTS duration differs from planned timing by more than 5%, report before retiming,
- retiming must preserve scene structure,
- do not silently desync visual beats from narration.

Recommended layout:

```text
assets/audio/
  scene_02_03/
    vo_0000_0010_5.wav
    vo_0010_5_0022_0.wav
    pause_0047_0048.wav
```

---

## 27. Conceptual correctness guardrails

### 27.1 Traditional deep learning

Conventional deep learning usually learns maps between finite-dimensional objects:

```text
f: R^n -> R^m
```

Do not claim standard ML cannot handle scientific data. The precise point is that many standard architectures assume fixed finite tensor representations, while scientific fields often need continuum-aware behavior.

### 27.2 Function-valued data

Many scientific/engineering data are functions over domains:

- weather fields on a sphere,
- seismic waves in subsurface volumes,
- pressure/velocity fields around cars or aircraft,
- molecular trajectories,
- material deformation fields,
- tissue imaging fields,
- plasma evolution,
- robotics trajectories.

They may be visualized as images/videos, but they are not merely images/videos. Domain, geometry, derivatives, integrals, and physical laws matter.

### 27.3 Traditional solvers

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
- differentiability challenges for inverse problems,
- barrier to entry,
- difficulty incorporating real data or expert knowledge.

ML complements solvers; it does not magically replace all scientific computing.

### 27.4 Solution operator

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

### 27.5 Discretization

Scientific data may appear on:

- regular grids,
- irregular meshes,
- point clouds,
- sparse sensors,
- different train/test resolutions,
- different input/output meshes,
- surfaces,
- volumes,
- spheres,
- geometry-dependent meshes.

Discretization is the observation/computation layer, not necessarily the mathematical object itself.

### 27.6 Discretization-convergent intuition

Discretization-convergent does not merely mean “runs on resized inputs.”

Distinguish:

```text
runs on many tensor sizes        != discretization-convergent
accepts resized image-like data  != learns a continuum operator
mesh refinement -> stable limit  =  discretization-convergent behavior
```

### 27.7 Neural network layer to integral operator

Core derivation:

1. Start with a finite-dimensional neural network layer.
2. Interpret vector entries as samples `a(x_j)` of a function.
3. Replace matrix entries `K_ij` with kernel values `κ(y_i, x_j)`.
4. Replace normalized sums with weighted Riemann sums.
5. Take the continuum limit.
6. Obtain a linear integral operator.
7. Add pointwise nonlinearity.
8. Add residual connection, bias function, and measure/quadrature weights.
9. Stack layers to form a neural operator.

This derivation is the conceptual core of the tutorial. Keep it visually clean.

### 27.8 Full neural-operator architecture

High-level structure:

```text
a(x) -> pointwise lift P -> operator layers -> pointwise projection Q -> u(x)
```

Operator layers may include:

```text
integral transform + residual/skip + bias function + nonlinearity
```

### 27.9 Error analysis

Operator-learning error has at least:

- approximation error,
- generalization error,
- discretization error.

Do not evaluate only on one fixed grid and claim full operator validity.

### 27.10 Universal approximation

Universal approximation supports expressivity under assumptions. It does not guarantee:

- easy training,
- enough data,
- robustness,
- correct metrics,
- physics consistency,
- uncertainty calibration,
- OOD success.

---

## 28. Architecture vocabulary

Use names accurately.

### GNO / Kernel Neural Operator

- Kernel is parameterized directly, often by a neural network.
- Natural for point clouds and irregular geometry.
- Message passing resembles GNNs but must account for domain geometry and measure.
- Can be local or global.
- Needs quadrature/measure awareness for discretization consistency.

### FNO / Fourier Neural Operator

- Uses Fourier basis / spectral transform.
- Applies learned weights to selected Fourier modes.
- Efficient on regular grids via FFT.
- Good for global interactions.
- Can struggle with sharp local features, discontinuities, complex boundaries, or non-periodic geometry.

### SFNO / Spherical FNO

- Uses spherical harmonics or sphere-aware basis.
- Useful for weather/climate on spherical domains.

### Basis projection operators

- Project function to basis coefficients.
- Manipulate coefficients.
- Project back.
- Basis choice encodes assumptions about domain and regularity.

### U-NO / multiscale operators

- Use multiscale contraction/expansion.
- Similar visual spirit to U-Net, but explain it in operator-learning language.
- Useful for multi-resolution interactions.

### Transformer Neural Operator

- Attention can be interpreted as an integral-like weighted sum over samples.
- Must account for measure/quadrature on irregular grids.

### CoDA-NO / Codomain Attention

- Treats physical variables as function-valued tokens.
- Useful for multiphysics and variable-subset datasets.
- Requires variable-specific encoding.

### Local / differential kernels

- Capture local physics and derivative-like behavior.
- Must scale correctly with grid spacing to have continuum-consistent meaning.

Do not invent architecture claims beyond the script and sources.

---

## 29. Mathematical notation policy

Use readable `MathTex`.

Prefer:

```python
MathTex(r"\mathcal{G}: \mathcal{A} \to \mathcal{U}")
MathTex(r"u = \mathcal{G}(a)")
MathTex(r"\int_D \kappa(y,x)a(x)\,dx")
```

Avoid giant equations unless central to the beat.

When an equation is too dense:

- show only the meaningful part,
- animate transformation step by step,
- move details into narration or later scene.

---

## 30. Scene-by-scene order

Follow the production script order:

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

Do not implement scenes according to old experimental folders.

---

## 31. Handling failed visual scenes

If a scene has broad visual failure across many beats, do not patch it object by object.

Broad visual failure includes:

- repeated overlap,
- repeated overflow,
- unreadable dashboard layout,
- stale objects across transitions,
- conceptual clutter across the whole scene.

In that case:

```text
1. preserve narration and timing,
2. discard the failed visual layout,
3. write a keyframe storyboard,
4. rebuild using Visual System v2 components,
5. render contact sheet,
6. fix only against the contact sheet.
```

Scene 2.3 is the benchmark for this rule.

---

## 32. Git safety

Before changes:

```bash
git status -sb
git branch --show-current
```

Rules:

- do not use `git reset --hard`,
- do not use `git clean -fd`,
- do not delete user work,
- do not commit unless asked,
- do not change unrelated files,
- do not add secrets,
- do not add generated media to git unless explicitly intended,
- keep patches reviewable.

---

## 33. Test and render commands

Run from:

```bash
cd hcmus-intro2ml-lab1-tutorial-video/neural_operators_manim
```

Basic checks:

```bash
python -m compileall src tests
python -m unittest discover tests
```

Render one scene:

```bash
manim -ql src/scenes/<scene_file>.py <SceneClassName>
```

Verify duration:

```bash
python scripts/verify_duration.py media/videos --scene <SceneClassName> --expected <seconds>
```

Full check when available:

```bash
python scripts/check_scene.py \
  --scene <SceneClassName> \
  --file src/scenes/<scene_file>.py \
  --expected <seconds>
```

Use `-ql` first. Use higher quality only after visual and timing checks pass.

---

## 34. Report format

When reporting completion:

```text
Done: Scene X.Y — <title>

Changed:
- <file>
- <file>

Checked:
- <command>
- <command>

Expected duration: <N>s
Measured duration: <N>s
Duration status: PASS/FAIL

Visual QA:
- contact sheet: <path>
- visual report: <path>
- status: PASS/FAIL

Notes:
- <assumptions>
- <unresolved issues>
```

If render was not possible:

```text
I could not verify render duration in this environment.

I did run:
- <commands>

Expected duration from script: <N>s

Please run:
- <render command>
- <verify command>

Status:
Not production-ready until render duration and visual QA pass.
```

Do not hide uncertainty.

---

## 35. Response behavior for coding agents

When the user asks for a scene implementation, do not immediately produce large ad-hoc code for dense scenes.

First produce or follow:

```text
1. script extraction,
2. local timing table,
3. visual keyframe plan,
4. component/layout plan,
5. implementation steps,
6. verification commands,
7. acceptance criteria.
```

Then implement.

If the user explicitly asks for direct code, still obey timing and visual-system rules.

---

## 36. Final philosophy

The central question of the video:

```text
When data are functions, how must machine learning change?
```

Every scene should help answer that question.

The production stack is:

```text
correct concept
-> exact timing
-> clean visual layout
-> runnable code
-> verified render
-> polish
```

No vibes-only Manim.  
No timing roulette.  
No slide karaoke.  
No dashboard clutter.  
No “syntax passed therefore done.”

## Optional reference: Math-To-Manim

If available locally at `~/reference-repos/Math-To-Manim`, Codex may inspect it only as a reference for:

- staged mathematical explanation patterns,
- MathTex / TransformMatchingTex usage,
- formula readability and spacing patterns,
- static validation / render-review ideas.

Do not import Math-To-Manim as a runtime dependency.
Do not run its full generation pipeline for production scenes.
Do not let it override `docs/full_voice_manim_script.md`.
Do not copy large blocks of code. Reimplement small reusable ideas inside `neural_operators_manim/src/common/`.