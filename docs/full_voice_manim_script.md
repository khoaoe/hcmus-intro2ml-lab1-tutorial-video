# Full Voice-over + Manim Direction Script  
## ICML 2024 Tutorial: *Machine Learning on Function Spaces — Neural Operators*  
### Version: production draft v1 — research-level, animation-first, Vietnamese narration

**Target duration:** ~58 phút 20 giây  
**Narration style:** tiếng Việt, trực giác kiểu 3Blue1Brown, nhưng vẫn research-level.  
**Technical policy:** giữ English term khi cần; lần đầu giải thích đầy đủ, các lần sau dùng English term.  
**Timing assumption:** ~130–145 từ/phút tiếng Việt, có pause tự nhiên. Khi tạo TTS thật, nên dùng scene id + line id để retime tự động nếu voice model đọc nhanh/chậm hơn.

---

## Global Manim Style Guide

- **Canvas:** 16:9, dark background `#0b1020`, accent green `#76B900` inspired by NVIDIA, secondary cyan/purple for function-space objects.
- **Visual grammar:**
  - Finite-dimensional vector: dots / bars / small grid / column vectors.
  - Function: continuous curve, surface, field on mesh, sphere field.
  - Operator: glowing arrow between function spaces.
  - Neural network: finite node graph.
  - Neural operator: integral-kernel “lens” transforming an input field into an output field.
- **Recurring motifs:**
  - `VectorWorld`: finite grid, pixels, tokens.
  - `FunctionWorld`: continuous domain, mesh refinement, query points.
  - `SolutionOperator`: map from input function `a` to output function `u`.
  - `Discretization`: coarse mesh → fine mesh → continuum limit.
  - `KernelLens`: moving kernel `κ(y,x)` sweeping over input field.
- **Voice alignment rule:** each `VO` line is independently recordable. Avoid combining multiple `VO` lines into one TTS generation unless the timestamps are regenerated.

---

# Section Timing Overview

| Section | Time | Purpose |
|---|---:|---|
| 0. Cold open | 00:00–02:20 | Establish thesis: ML must move from vectors to functions |
| 1. What deep learning already solved | 02:20–07:20 | finite-dimensional ML, CV/NLP bias |
| 2. Real-world data are functions | 07:20–15:45 | weather, seismology, CFD, molecules, medicine |
| 3. Traditional scientific computing | 15:45–23:20 | PDEs, solvers, Darcy example, compute wall |
| 4. Learn the solution operator | 23:20–29:10 | from solving to predicting function-to-function maps |
| 5. Discretization challenge | 29:10–35:00 | irregular grids, output must be function |
| 6. Neural operators | 35:00–42:30 | discretization-agnostic, convergent, function query |
| 7. Pre-req: integrals and derivatives | 42:30–46:20 | Riemann sum, finite difference |
| 8. From neural networks to neural operators | 46:20–58:50 | matrix layer → integral operator |
| 9. Full neural operator architecture | 58:50–1:07:40 | residual, bias, composition, universal approximation, error |
| 10. Architectures | 1:07:40–1:24:10 | GNO, FNO, basis, U-NO, Transformer NO, CoDA-NO, local/differential kernels |
| 11. Domains, not just applications | 1:24:10–1:41:40 | weather, seismology, carbon storage, molecular dynamics, car CFD |
| 12. Open problems | 1:41:40–1:55:20 | accuracy, metrics, chaos, uncertainty, scaling, physics |
| 13. Closing | 1:55:20–1:58:20 | final synthesis |

> Note: Total file is designed as a *near-original tutorial replacement*. If you want a 45-minute classroom version later, cut Sections 10.4, 10.5, and compress Section 11.

---

# 0. Cold Open — Why This Tutorial Exists

## Scene 0.1 — Title: “From pixels to fields”
**Time:** 00:00.0–00:42.0  
**Source anchor:** original title + tutorial thesis.

### Voice-over
- **[00:00.0–00:05.5] VO:** Hãy bắt đầu bằng một câu hỏi nghe có vẻ hơi vô lý: nếu deep learning đã rất giỏi với ảnh, văn bản, âm thanh… vậy tại sao khoa học tính toán vẫn còn khó đến thế?
- **[00:05.5–00:06.3] Pause:** 0.8s.
- **[00:06.3–00:13.5] VO:** Câu trả lời ngắn gọn là: rất nhiều dữ liệu ngoài đời không thật sự là ảnh, cũng không thật sự là chuỗi token.
- **[00:13.5–00:14.2] Pause:** 0.7s.
- **[00:14.2–00:23.0] VO:** Nó là một hàm. Một trường nhiệt độ trên Trái Đất. Một trường vận tốc trong lòng đất. Một dòng chảy quanh cánh máy bay.
- **[00:23.0–00:24.0] Pause:** 1.0s.
- **[00:24.0–00:33.5] VO:** Tutorial này nói về một hướng học máy cho kiểu dữ liệu đó: machine learning on function spaces — học máy trên không gian hàm.
- **[00:33.5–00:42.0] VO:** Và nhân vật chính của chúng ta là neural operator: một generalization của neural network, nhưng không còn học map từ vector sang vector, mà học map từ hàm sang hàm.

### Visual / Manim direction
- Fade in dark background.
- Left: pixel dog image decomposes into finite grid blocks.
- Right: smooth temperature field on sphere appears as continuous surface.
- A glowing label: `Finite-dimensional data` over image; `Function-valued data` over field.
- Title forms: **Machine Learning on Function Spaces — Neural Operators**.
- Use one small animated arrow from “vector → vector” to “function → function”.

### Manim objects
- `PixelGrid`, `SphereField`, `ContinuousSurface`, `Arrow`, `MathTex("f: \\mathbb{R}^n \\to \\mathbb{R}^m")`, `MathTex("\\mathcal{G}: \\mathcal{A} \\to \\mathcal{U}")`.

---

## Scene 0.2 — Roadmap
**Time:** 00:42.0–02:20.0

### Voice-over
- **[00:42.0–00:49.0] VO:** Flow của video sẽ đi theo đúng tinh thần tutorial gốc, nhưng thay vì chiếu slide, ta sẽ xây câu chuyện bằng animation.
- **[00:49.0–00:50.0] Pause:** 1.0s.
- **[00:50.0–01:01.5] VO:** Đầu tiên, ta nhìn lại deep learning truyền thống: vì sao nó thành công với ảnh và ngôn ngữ, nhưng lại không đủ tự nhiên cho dữ liệu khoa học.
- **[01:01.5–01:10.5] VO:** Sau đó, ta xem cách khoa học tính toán thường giải bài toán: mô hình hóa bằng phương trình, rồi dùng solver.
- **[01:10.5–01:18.5] VO:** Tiếp theo là bước nhảy quan trọng: thay vì solve từng bài toán, liệu ta có thể học luôn solution operator không?
- **[01:18.5–01:19.3] Pause:** 0.8s.
- **[01:19.3–01:31.0] VO:** Rồi ta xây neural operator từ những mảnh rất quen thuộc: tích phân, đạo hàm, Riemann sum, và một lớp neural network cơ bản.
- **[01:31.0–01:43.0] VO:** Sau đó là các kiến trúc: Graph Neural Operator, Fourier Neural Operator, U-shaped operator, Transformer Neural Operator, codomain attention, và các kernel local hoặc differential.
- **[01:43.0–01:54.5] VO:** Cuối cùng, ta quay về các domain thật: weather, seismology, carbon storage, molecular dynamics, car CFD — và các open problems vẫn còn rất lớn.
- **[01:54.5–02:20.0] VO:** Hãy giữ một câu hỏi xuyên suốt video: khi dữ liệu là hàm, thì học máy phải thay đổi ở đâu — ở input, ở architecture, ở loss, hay ở toàn bộ cách ta định nghĩa một bài toán?

### Visual / Manim direction
- Draw a roadmap as a horizontal timeline with six glowing nodes.
- Each node has icon:
  1. pixel/vector,
  2. PDE/solver,
  3. operator arrow,
  4. integral kernel,
  5. architectures,
  6. open problems.
- Camera pans slowly from left to right.

### Manim objects
- `Timeline`, `VGroup` of roadmap nodes, icons using simple primitives.

---

# 1. What Traditional Deep Learning Already Solved

## Scene 1.1 — The finite-dimensional comfort zone
**Time:** 02:20.0–03:35.0

### Voice-over
- **[02:20.0–02:28.0] VO:** Deep learning truyền thống, theo nghĩa quen thuộc nhất, sống khá thoải mái trong thế giới finite-dimensional.
- **[02:28.0–02:36.5] VO:** Một ảnh được biến thành ma trận pixel. Một câu được biến thành sequence token. Một âm thanh được biến thành waveform hoặc spectrogram.
- **[02:36.5–02:37.4] Pause:** 0.9s.
- **[02:37.4–02:47.0] VO:** Tức là trước khi học, ta thường đã đóng gói thế giới thành một object hữu hạn chiều: một vector, một tensor, một chuỗi số.
- **[02:47.0–02:58.5] VO:** Và model học một function, ví dụ từ vector đầu vào sang label, embedding, hoặc vector đầu ra.
- **[02:58.5–03:12.0] VO:** Đây là pipeline đã tạo ra CNN, ResNet, U-Net, Transformer, ViT, rồi cả language model hiện đại.
- **[03:12.0–03:35.0] VO:** Không có gì sai ở đây. Đây là một chiến thắng cực lớn. Nhưng cũng chính thành công đó khiến ta dễ quên rằng không phải mọi thứ trong thế giới thật đều sinh ra để trở thành một ảnh 224 nhân 224.

### Visual / Manim direction
- Show image as `64x64` grid, text as token boxes, audio waveform as samples.
- Each object flattens into a vector.
- A neural network maps vector to label.
- At the end, zoom out and show “finite-dimensional comfort zone” as a glowing box.

### Manim objects
- `MatrixGrid`, `TokenSequence`, `WaveformSamples`, `NeuralNetworkGraph`, `SurroundingRectangle`.

---

## Scene 1.2 — Why CV/NLP shaped our habits
**Time:** 03:35.0–05:20.0

### Voice-over
- **[03:35.0–03:44.5] VO:** Trong nhiều thập kỷ, computer vision và natural language processing không chỉ cho ta model. Chúng cho ta cả cách nghĩ.
- **[03:44.5–03:55.5] VO:** Ta có dataset chuẩn, benchmark chuẩn, loss quen thuộc, metric quen thuộc, và cả một hệ sinh thái để so sánh model.
- **[03:55.5–04:07.0] VO:** Với ảnh, ta quen với accuracy, FID, Inception score, CLIP score. Với regression, ta quen với L1, L2, RMSE.
- **[04:07.0–04:08.0] Pause:** 1.0s.
- **[04:08.0–04:20.0] VO:** Nhưng khi chuyển sang weather forecasting, seismology, molecular dynamics, hay fluid simulation, câu hỏi không đơn giản là: metric nào có sẵn?
- **[04:20.0–04:34.0] VO:** Câu hỏi đúng hơn là: đại lượng vật lý nào cần bảo toàn, đạo hàm nào phải đúng, tích phân nào phải có nghĩa, và domain expert sẽ kiểm tra model bằng luật nào?
- **[04:34.0–04:49.5] VO:** Nói hơi phũ: không thể bê nguyên tư duy ImageNet sang Navier–Stokes rồi hy vọng vũ trụ tự ngoan.
- **[04:49.5–05:20.0] VO:** Vì vậy tutorial này không xem neural operator như “một architecture mới nữa”. Nó xem đây là một paradigm mới cho những domain mà dữ liệu là hàm.

### Visual / Manim direction
- Show a shelf of familiar ML metrics, then animate it sliding aside.
- Bring in physics constraints: `conservation`, `derivatives`, `integrals`, `PDE residual`.
- A red stamp: “not plug-and-play”.
- Transition to a large label: `Function Spaces`.

### Manim objects
- `MetricCards`, `PhysicsConstraintCards`, `Cross`, `Text("Not plug-and-play")`.

---

## Scene 1.3 — From university departments to function data
**Time:** 05:20.0–07:20.0

### Voice-over
- **[05:20.0–05:31.0] VO:** Hãy tưởng tượng ta đi một vòng quanh một trường đại học: mechanical engineering, geophysics, chemistry, medicine, climate science, materials science.
- **[05:31.0–05:45.0] VO:** Phần lớn các bài toán quan trọng ở đó không phải là “ảnh này là mèo hay chó”, cũng không phải là “token tiếp theo là gì”.
- **[05:45.0–05:56.5] VO:** Chúng hỏi: dòng khí quanh xe sẽ tạo áp suất như thế nào? Sóng động đất lan trong lòng đất ra sao? Protein biến đổi cấu trúc theo thời gian thế nào?
- **[05:56.5–06:07.0] VO:** Và những đối tượng này thường là field — trường vật lý — được định nghĩa trên không gian và thời gian.
- **[06:07.0–06:08.2] Pause:** 1.2s.
- **[06:08.2–06:20.5] VO:** Ta có thể visualize chúng như ảnh, nhưng đó là cái bẫy thị giác. Một field được vẽ thành ảnh không có nghĩa nó là ảnh.
- **[06:20.5–06:35.0] VO:** Nếu ta zoom vào, đổi mesh, lấy đạo hàm, tích phân trên bề mặt, hoặc query tại một điểm chưa có trong grid, bản chất function mới lộ ra.
- **[06:35.0–07:20.0] VO:** Đây là lý do tutorial bắt đầu từ một đổi trục rất cơ bản: không còn chỉ học trên Euclidean vectors, mà học trên function spaces.

### Visual / Manim direction
- Build a stylized campus map; departments light up.
- Each department emits a different function visualization: sphere weather, underground wave, car CFD, molecular trajectory.
- Each visualization gets label `not image → function`.
- Camera zooms through one image to reveal mesh and continuous interpolation.

### Manim objects
- `CampusMap`, `DepartmentLabels`, `FieldVisuals`, `MeshOverlay`, `ZoomedGrid`.

---

# 2. Real-world Data Are Functions

## Scene 2.1 — Weather: functions on a sphere
**Time:** 07:20.0–09:05.0

### Voice-over
- **[07:20.0–07:30.5] VO:** Ví dụ đầu tiên là weather và climate. Ở đây domain không phải một grid phẳng đơn giản, mà là gần như một sphere — bề mặt Trái Đất.
- **[07:30.5–07:42.5] VO:** Tại mỗi điểm trên sphere, ta có nhiều biến: temperature, wind velocity, humidity, pressure, precipitation, vorticity.
- **[07:42.5–07:54.0] VO:** Một trạng thái thời tiết tại một thời điểm không phải một vector nhỏ. Nó là một vector-valued function trên một domain hình học.
- **[07:54.0–08:06.5] VO:** Và bài toán forecast có thể được nói rất gọn: từ các hàm hôm nay, dự đoán các hàm ngày mai.
- **[08:06.5–08:07.5] Pause:** 1.0s.
- **[08:07.5–08:25.0] VO:** Nhưng domain expert không chỉ cần màu đẹp trên bản đồ. Họ cần gradient, divergence, energy, flux — những thứ phụ thuộc vào đạo hàm và tích phân của field.
- **[08:25.0–09:05.0] VO:** Vậy nếu model chỉ output một ảnh rời rạc, ta mất ngay khả năng kiểm tra physics ở level liên tục. Đây là một recurring theme: output phải có ý nghĩa như một function.

### Visual / Manim direction
- Rotate Earth sphere with animated scalar and vector fields.
- Show small arrows for wind, color field for temperature.
- Turn `today` field into `tomorrow` field through an operator arrow.
- Add small derivative/integral glyphs on surface.

### Manim objects
- `Sphere`, `ParametricSurface`, `VectorField`, `OperatorArrow`, `MathTex("\\nabla, \\int")`.

---

## Scene 2.2 — Seismology: functions inside Earth
**Time:** 09:05.0–10:45.0

### Voice-over
- **[09:05.0–09:15.0] VO:** Trong seismology, input có thể là velocity field của lớp đất đá dưới bề mặt.
- **[09:15.0–09:27.5] VO:** Một trận động đất xảy ra, và ta muốn biết wave sẽ propagate như thế nào trong không gian ba chiều, theo thời gian.
- **[09:27.5–09:39.5] VO:** Đây là một function của cả space và time. Và lần nữa, physics nằm trong đạo hàm theo không gian và thời gian.
- **[09:39.5–09:40.7] Pause:** 1.2s.
- **[09:40.7–09:55.0] VO:** Có một bài toán ngược còn khó hơn: ta chỉ đo được tín hiệu trên bề mặt, rồi muốn suy ra cấu trúc bên dưới.
- **[09:55.0–10:06.5] VO:** Tức là từ observation function trên surface, ta muốn infer một hidden function trong volume.
- **[10:06.5–10:45.0] VO:** Neural operator hấp dẫn ở đây vì nếu nó nhanh và differentiable, ta có thể dùng nó như một surrogate để làm inverse problem nhanh hơn.

### Visual / Manim direction
- Show 3D block of Earth with layered velocity field.
- Animate wavefront propagating from fault.
- Surface sensors record waves.
- Reverse arrow: surface observations → subsurface structure.

### Manim objects
- `ThreeDLayeredVolume`, `Wavefront`, `SensorDots`, `InverseArrow`.

---

## Scene 2.3 — Fluids, materials, molecules, robots
**Time:** 10:45.0–12:55.0

### Voice-over
- **[10:45.0–10:55.5] VO:** Bức tranh này lặp lại ở rất nhiều nơi. Trong CFD, fluid quanh xe hoặc máy bay là velocity field, pressure field, turbulence field.
- **[10:55.5–11:07.0] VO:** Trong material science, deformation của vật liệu theo không gian và thời gian cũng là field.
- **[11:07.0–11:20.0] VO:** Trong molecular dynamics, vị trí và trạng thái của phân tử tiến hóa liên tục theo thời gian, không phải chỉ là vài frame rời rạc.
- **[11:20.0–11:32.0] VO:** Trong robotics, motion của joint cũng có thể xem như continuous trajectory, một function theo thời gian.
- **[11:32.0–11:33.0] Pause:** 1.0s.
- **[11:33.0–11:46.0] VO:** Điểm chung không phải là chúng đều “trông giống ảnh”. Điểm chung là chúng có domain, có smoothness hoặc discontinuity, có geometry, và có luật vật lý.
- **[11:46.0–12:10.0] VO:** Nếu ta dùng model mà không hiểu domain đó, ta có thể có một prediction nhìn hợp lý nhưng sai về derivative, sai về conservation, hoặc sai ở vùng boundary.
- **[12:10.0–12:55.0] VO:** Vì vậy, khi nói “data is function”, ta đang nói về một yêu cầu kỹ thuật: model phải tôn trọng domain, discretization, và các phép toán liên tục mà domain expert cần dùng sau đó.

### Visual / Manim direction
- Four panels: car CFD, material deformation, molecule trajectory, robot joint path.
- Each panel morphs into a mathematical object: `u(x,t)`, `p(x,t)`, `q(t)`.
- Overlay geometry/boundary/domain markers.

### Manim objects
- `PanelGrid`, `FlowField`, `DeformationMesh`, `TrajectoryCurve`, `BoundaryHighlight`.

---

## Scene 2.4 — The core warning
**Time:** 12:55.0–15:45.0

### Voice-over
- **[12:55.0–13:05.5] VO:** Tới đây có một warning rất quan trọng: visualization không quyết định bản chất của dữ liệu.
- **[13:05.5–13:17.0] VO:** Một weather field có thể được render thành ảnh màu. Một seismic wave cũng có thể được render thành video.
- **[13:17.0–13:29.0] VO:** Nhưng nếu ta chỉ xử lý chúng như ảnh hoặc video, ta đang ném mất phần domain knowledge đắt giá nhất.
- **[13:29.0–13:30.0] Pause:** 1.0s.
- **[13:30.0–13:42.5] VO:** Câu hỏi không phải là: “model có nhìn thấy pattern không?” Câu hỏi là: “model có học đúng map giữa hai function spaces không?”
- **[13:42.5–13:57.0] VO:** Và đây là lúc từ “operator” xuất hiện. Trong toán học, operator thường là một map nhận một function và trả ra một function khác.
- **[13:57.0–14:12.5] VO:** Ví dụ: nhận coefficient field của một PDE, trả ra solution field. Nhận trạng thái khí quyển hôm nay, trả ra trạng thái ngày mai.
- **[14:12.5–14:28.5] VO:** Nói ngắn gọn: neural operator học một operator bằng dữ liệu.
- **[14:28.5–14:45.5] VO:** Nhưng để hiểu tại sao chuyện này khác neural network thường, ta cần đi qua cách scientific computing truyền thống giải bài toán.
- **[14:45.5–15:45.0] VO:** Đây là đoạn chuyển quan trọng: từ dữ liệu là hàm, ta chuyển sang câu hỏi “trước khi có neural operator, ta đã giải các hàm này bằng cách nào?”

### Visual / Manim direction
- A rendered field labeled “image?” is crossed out, replaced by `function`.
- Draw two large spaces: `𝒜` and `𝒰`, with infinite curves inside.
- Arrow labeled `operator`.
- Fade into PDE board.

### Manim objects
- `FunctionSpaceBlob`, `CurvesInsideSpace`, `OperatorArrow`, `MathTex("\\mathcal{G}: \\mathcal{A}\\to\\mathcal{U}")`.

---

# 3. Traditional Scientific Computing

## Scene 3.1 — Model phenomena with equations
**Time:** 15:45.0–17:20.0

### Voice-over
- **[15:45.0–15:55.0] VO:** Trong khoa học tính toán truyền thống, ta thường bắt đầu bằng first principles.
- **[15:55.0–16:07.0] VO:** Ta dùng phương trình vi phân, phương trình đại số, conservation laws, boundary conditions, initial conditions.
- **[16:07.0–16:20.0] VO:** Tùy domain, đó có thể là Navier–Stokes, Maxwell, Schrödinger, Darcy, Helmholtz, heat equation, wave equation.
- **[16:20.0–16:21.0] Pause:** 1.0s.
- **[16:21.0–16:35.5] VO:** Sau đó, vì máy tính không xử lý trực tiếp continuum, ta discretize domain thành mesh hoặc grid.
- **[16:35.5–16:51.0] VO:** Rồi dùng finite difference, finite volume, finite element, spectral method, hoặc nhiều solver chuyên biệt khác.
- **[16:51.0–17:20.0] VO:** Đây là một trong những thành tựu lớn của applied math. Neural operator không thay thế toàn bộ thứ này. Nó cố gắng bổ sung một công cụ mới vào toolbox.

### Visual / Manim direction
- Equations write themselves on chalkboard.
- Grid appears over continuous domain.
- Solver machinery transforms equation + grid into numerical solution.
- Toolbox icon: solver + ML side by side.

### Manim objects
- `EquationBoard`, `Mesh`, `SolverBox`, `Toolbox`.

---

## Scene 3.2 — Darcy flow as the clean toy example
**Time:** 17:20.0–19:35.0

### Voice-over
- **[17:20.0–17:31.0] VO:** Để có một toy example sạch, ta dùng Darcy flow: dòng chảy qua môi trường xốp.
- **[17:31.0–17:44.0] VO:** Input là một hàm mô tả diffusion coefficient hoặc permeability field. Hãy gọi nó là `a`.
- **[17:44.0–17:56.5] VO:** Output là solution field, ví dụ pressure hoặc potential. Hãy gọi nó là `u`.
- **[17:56.5–17:57.5] Pause:** 1.0s.
- **[17:57.5–18:10.5] VO:** PDE định nghĩa quan hệ giữa `a` và `u`. Với mỗi `a`, solver tìm ra `u` thỏa equation và boundary conditions.
- **[18:10.5–18:23.0] VO:** Nếu nhìn từ xa, toàn bộ quá trình này là một map: đưa vào function `a`, trả ra function `u`.
- **[18:23.0–18:34.5] VO:** Map đó gọi là solution operator — toán tử nghiệm.
- **[18:34.5–18:53.0] VO:** Finite difference chỉ là một cách biến bài toán continuum thành hệ phương trình hữu hạn chiều: lấy giá trị ở các grid point, xấp xỉ derivative bằng hiệu chia cho bước lưới.
- **[18:53.0–19:09.5] VO:** Mesh càng mịn, xấp xỉ thường càng tốt. Nhưng compute cũng tăng.
- **[19:09.5–19:35.0] VO:** Và đây là trade-off cổ điển: muốn solution chính xác hơn, ta thường phải trả bằng thời gian, bộ nhớ, và năng lượng tính toán.

### Visual / Manim direction
- Show `a(x)` as random binary/continuous permeability field.
- PDE appears but voice does not read full formula.
- Solver arrow outputs smooth `u(x)`.
- Grid refinement: coarse → fine, solution improves; compute meter rises.

### Manim objects
- `RandomField`, `MathTex("-\\nabla\\cdot(a(x)\\nabla u(x))=f(x)")`, `SolutionField`, `ComputeMeter`.

---

## Scene 3.3 — Why not just keep hand-designing solvers?
**Time:** 19:35.0–21:35.0

### Voice-over
- **[19:35.0–19:46.5] VO:** Nếu solvers mạnh như vậy, tại sao không cứ tiếp tục hand-design solution operator?
- **[19:46.5–20:00.0] VO:** Lý do đầu tiên: real world không sạch như toy PDE. Weather forecasting chẳng hạn có rất nhiều thành phần không thể mô hình hóa hoàn hảo.
- **[20:00.0–20:13.5] VO:** Clouds, mountains, ocean waves, turbulence, radiation, microphysics — nhiều thứ phải parameterize bằng heuristic.
- **[20:13.5–20:14.5] Pause:** 1.0s.
- **[20:14.5–20:29.0] VO:** Parameterization giúp bài toán chạy được, nhưng cũng đưa error vào hệ thống.
- **[20:29.0–20:43.5] VO:** Lý do thứ hai: compute. Một mô hình khí hậu ở resolution cao hơn không chỉ đắt hơn một chút. Nó có thể đắt hơn nhiều bậc độ lớn.
- **[20:43.5–20:58.0] VO:** Nếu giảm grid size và time step đồng thời, compute có thể bùng nổ đến mức không thực tế.
- **[20:58.0–21:16.0] VO:** Lý do thứ ba: inverse problems. Nếu solver không differentiable, hoặc rất chậm, việc tối ưu ngược từ observation về hidden parameter trở nên cực khó.
- **[21:16.0–21:35.0] VO:** Vậy vấn đề không phải “traditional methods tệ”. Vấn đề là chúng có limitations, và machine learning có thể complement chúng.

### Visual / Manim direction
- Weather equations multiply into a dense wall.
- Parameterization blocks appear as approximations.
- Resolution ladder: 100km → 10km → 1km → 100m; compute curve explodes.
- Inverse problem arrow loops back and gets stuck.

### Manim objects
- `EquationWall`, `ApproximationBlocks`, `ResolutionLadder`, `ExponentialCurve`, `InverseLoop`.

---

## Scene 3.4 — Scientific ML hypothesis
**Time:** 21:35.0–23:20.0

### Voice-over
- **[21:35.0–21:47.5] VO:** Neural operators bắt đầu từ một hypothesis rất táo bạo: nếu ta có data gồm nhiều cặp input function và output function, ta có thể học luôn map giữa chúng.
- **[21:47.5–22:00.0] VO:** Không phải học một lời giải riêng lẻ. Không phải fit một function cho một instance. Mà học cả solution operator.
- **[22:00.0–22:01.0] Pause:** 1.0s.
- **[22:01.0–22:15.0] VO:** Sau khi train, inference có thể nhanh hơn rất nhiều so với solver truyền thống, đặc biệt khi cần chạy hàng nghìn hoặc hàng triệu scenario.
- **[22:15.0–22:29.5] VO:** Điểm này cực quan trọng trong uncertainty quantification, design optimization, ensemble forecasting, và inverse problems.
- **[22:29.5–22:43.0] VO:** Nhưng nếu chỉ dùng neural network thường trên một grid cố định, ta mắc ngay một lỗi thiết kế.
- **[22:43.0–23:20.0] VO:** Dữ liệu function không đến với ta ở một resolution duy nhất. Nó có thể nằm trên nhiều mesh, nhiều sensor layout, nhiều domain geometry. Model phải sống được trong thế giới đó.

### Visual / Manim direction
- Dataset of pairs `(a_i, u_i)` as stacks of fields.
- Training process learns glowing operator `𝒢θ`.
- Inference meter: solver slow, learned operator fast.
- Grid mismatch warning.

### Manim objects
- `FieldPairDataset`, `LearnedOperator`, `SpeedGauge`, `GridMismatchIcon`.

---

# 4. Learn the Solution Operator

## Scene 4.1 — From “solve u” to “predict u”
**Time:** 23:20.0–25:00.0

### Voice-over
- **[23:20.0–23:31.5] VO:** Trong solver-based view, ta nói: cho `a`, hãy giải phương trình để tìm `u`.
- **[23:31.5–23:44.0] VO:** Trong operator learning view, ta nói: cho nhiều ví dụ `a` và `u`, hãy học map `a` sang `u`.
- **[23:44.0–23:45.0] Pause:** 1.0s.
- **[23:45.0–23:58.0] VO:** Đây là một shift nhỏ về ngôn ngữ, nhưng rất lớn về computational strategy.
- **[23:58.0–24:13.5] VO:** Solver phải làm lại quá trình tính toán cho từng input mới. Neural operator cố gắng amortize quá trình đó vào training.
- **[24:13.5–24:27.0] VO:** Sau training, mỗi query mới không còn là một bài toán PDE đầy đủ, mà là một forward pass.
- **[24:27.0–25:00.0] VO:** Dĩ nhiên, cái giá là data, training, generalization, và rất nhiều câu hỏi mở. Nhưng payoff tiềm năng là cực lớn.

### Visual / Manim direction
- Split screen: left solver loop per input; right train once / infer many.
- Animate amortization: many expensive solves compressed into learned operator.

### Manim objects
- `SolverLoop`, `TrainingCompression`, `ForwardPassArrow`.

---

## Scene 4.2 — Operator learning is not just supervised learning with bigger tensors
**Time:** 25:00.0–27:05.0

### Voice-over
- **[25:00.0–25:12.0] VO:** Một hiểu nhầm phổ biến: “operator learning chỉ là supervised learning, nhưng tensor to hơn.”
- **[25:12.0–25:13.0] Pause:** 1.0s.
- **[25:13.0–25:22.5] VO:** Không hẳn.
- **[25:22.5–25:36.0] VO:** Nếu input và output là function, model cần có hành vi nhất quán khi discretization thay đổi.
- **[25:36.0–25:49.5] VO:** Train ở mesh thô, test ở mesh mịn. Input sensor không đều, output query đều. Domain có thể là sphere, mesh quanh xe, hoặc volume 3D.
- **[25:49.5–26:02.0] VO:** Một CNN thường được thiết kế cho một grid cụ thể. Resize input có thể chạy được về mặt code, nhưng không đảm bảo đang approximate cùng một operator continuum.
- **[26:02.0–26:18.5] VO:** Neural operator thì đặt continuum problem làm trung tâm, còn discretization chỉ là cách ta quan sát và tính gần đúng.
- **[26:18.5–27:05.0] VO:** Đây là điểm triết học quan trọng nhất: model không nên học “bảng số trên grid này”; model nên học “quan hệ giữa các hàm”, rồi bảng số chỉ là sampling của quan hệ đó.

### Visual / Manim direction
- Show tensor grows larger, then cracks.
- Show same underlying curve sampled at 8, 16, 64 points.
- The operator arrow remains same; sample points change.

### Manim objects
- `TensorBlock`, `CrackAnimation`, `SampledFunction`, `ContinuumOperator`.

---

## Scene 4.3 — The three errors we must remember
**Time:** 27:05.0–29:10.0

### Voice-over
- **[27:05.0–27:17.0] VO:** Trong machine learning truyền thống, ta hay nói về approximation error và generalization error.
- **[27:17.0–27:30.0] VO:** Approximation error: function class có đủ expressivity không? Generalization error: data có đủ để model học pattern đúng không?
- **[27:30.0–27:31.0] Pause:** 1.0s.
- **[27:31.0–27:45.0] VO:** Trong operator learning, có thêm một nhân vật rất khó chịu: discretization error.
- **[27:45.0–28:00.0] VO:** Vì ta không bao giờ thấy toàn bộ function continuum. Ta chỉ thấy các point evaluation, các mesh, các sensor, các snapshot.
- **[28:00.0–28:15.0] VO:** Nếu discretization quá thô, không model nào có thể phục hồi thông tin đã mất một cách thần kỳ.
- **[28:15.0–28:31.0] VO:** Vì vậy error analysis của neural operator phải nhìn ba góc: approximation, generalization, và discretization.
- **[28:31.0–29:10.0] VO:** Và khi precision tính toán bước vào, còn có trade-off thú vị: nếu discretization error đang chi phối, tăng floating-point precision chưa chắc là bottleneck thật.

### Visual / Manim direction
- Triangle of errors: approximation, generalization, discretization.
- Discretized curve loses high-frequency detail.
- Precision knob appears but no improvement when mesh coarse.

### Manim objects
- `ErrorTriangle`, `HighFreqCurve`, `CoarseSampling`, `PrecisionKnob`.

---

# 5. Discretization Challenge

## Scene 5.1 — Input and output may live on different meshes
**Time:** 29:10.0–31:20.0

### Voice-over
- **[29:10.0–29:22.0] VO:** Bây giờ hãy nhìn dữ liệu thật trong scientific computing. Input function có thể được đo trên một mesh.
- **[29:22.0–29:33.5] VO:** Output function có thể được lưu trên một mesh khác. Sample tiếp theo lại dùng một resolution khác nữa.
- **[29:33.5–29:46.0] VO:** Có dữ liệu trên regular grid, có dữ liệu trên irregular mesh, có sensor sparse, có boundary phức tạp.
- **[29:46.0–29:47.0] Pause:** 1.0s.
- **[29:47.0–30:00.0] VO:** Nếu model buộc input và output phải là tensor cùng shape cố định, ta đã tự khóa mình vào một setup quá hẹp.
- **[30:00.0–30:16.5] VO:** Trong khi đó, bài toán vật lý thật không quan tâm ta lưu nó bằng grid nào. Nó tồn tại ở continuum level.
- **[30:16.5–30:35.0] VO:** Neural operator cố gắng làm điều ngược lại với resizing hack: nó định nghĩa computation sao cho có ý nghĩa khi mesh thay đổi.
- **[30:35.0–31:20.0] VO:** Đây là lý do ta cần các operation giống tích phân hơn là chỉ matrix multiplication trên index cố định.

### Visual / Manim direction
- Show input mesh irregular, output grid regular, next sample different.
- A standard NN rejects shape mismatch.
- Neural operator accepts sample points + values + query points.

### Manim objects
- `IrregularMesh`, `RegularGrid`, `ShapeMismatchWarning`, `QueryPointSet`.

---

## Scene 5.2 — Output must be queryable
**Time:** 31:20.0–33:05.0

### Voice-over
- **[31:20.0–31:31.0] VO:** Requirement thứ hai: output của model nên có thể query ở bất kỳ điểm nào ta cần.
- **[31:31.0–31:44.5] VO:** Không phải vì ta thích đẹp. Mà vì physics thường hỏi local derivative, boundary value, surface integral, hoặc average over region.
- **[31:44.5–31:57.0] VO:** Trong car design, drag liên quan đến tích phân pressure trên bề mặt xe.
- **[31:57.0–32:09.0] VO:** Trong weather, energy và flux cũng là các đại lượng tích phân trên domain.
- **[32:09.0–32:10.0] Pause:** 1.0s.
- **[32:10.0–32:25.5] VO:** Nếu output chỉ là một tensor cố định, ta có thể interpolate sau đó. Nhưng khi đó interpolation không còn là phần được học và kiểm soát trong architecture.
- **[32:25.5–33:05.0] VO:** Neural operator muốn output thật sự là một function approximation: ta đưa query point `y` vào, và model trả ra giá trị `u(y)`.

### Visual / Manim direction
- Output field appears.
- Query point moves around; value label updates.
- Show derivative stencil and surface integral paths.

### Manim objects
- `MovingQueryDot`, `ValueTrackerLabel`, `DerivativeStencil`, `SurfaceIntegralPath`.

---

## Scene 5.3 — Discretization-convergent intuition
**Time:** 33:05.0–35:00.0

### Voice-over
- **[33:05.0–33:18.0] VO:** Một model discretization-convergent có nghĩa trực giác như sau.
- **[33:18.0–33:30.5] VO:** Khi ta refine mesh — làm lưới mịn hơn — prediction của model không nên nhảy lung tung.
- **[33:30.5–33:46.0] VO:** Nó nên tiến gần về một limit continuum duy nhất, giống như Riemann sum tiến về integral.
- **[33:46.0–33:47.0] Pause:** 1.0s.
- **[33:47.0–34:02.5] VO:** Đây là khác biệt giữa “chạy được trên nhiều resolution” và “có nguyên lý toán học khi resolution thay đổi”.
- **[34:02.5–34:19.5] VO:** Một model có thể resize input và vẫn chạy. Nhưng neural operator muốn mạnh hơn: cùng một set parameters, cùng một operator underlying, nhiều discretization khác nhau.
- **[34:19.5–35:00.0] VO:** Đó là cây cầu nối finite computation trên máy tính với infinite-dimensional problem trong toán học.

### Visual / Manim direction
- Mesh refinement sequence over airfoil.
- Predictions converge visually to same smooth field.
- Contrast with unstable model predictions flickering.

### Manim objects
- `MeshRefinementSequence`, `ConvergingFields`, `ContinuumLimitGlow`.

---

# 6. Neural Operators

## Scene 6.1 — Definition by contrast
**Time:** 35:00.0–36:45.0

### Voice-over
- **[35:00.0–35:13.0] VO:** Neural network truyền thống học một function giữa finite-dimensional spaces: vector vào, vector ra.
- **[35:13.0–35:28.0] VO:** Neural operator học một operator giữa function spaces: input là function, output cũng là function.
- **[35:28.0–35:29.0] Pause:** 1.0s.
- **[35:29.0–35:43.0] VO:** Nếu neural network hỏi: “given vector x, y là gì?”, neural operator hỏi: “given function a, function u là gì?”
- **[35:43.0–35:57.0] VO:** Ở đây `a` có thể là coefficient field, geometry field, initial condition, hoặc trạng thái hệ thống.
- **[35:57.0–36:12.0] VO:** `u` có thể là solution field, future state, wave propagation, pressure distribution, hoặc displacement field.
- **[36:12.0–36:45.0] VO:** Cốt lõi không phải tên biến. Cốt lõi là map từ một object vô hạn chiều sang một object vô hạn chiều khác.

### Visual / Manim direction
- Left: NN diagram `R^n → R^m`.
- Right: NO diagram `𝒜 → 𝒰`.
- Infinite curves inside function spaces animate softly.

### Manim objects
- `FiniteDiagram`, `FunctionSpaceDiagram`, `Curves`.

---

## Scene 6.2 — Three desired properties
**Time:** 36:45.0–38:40.0

### Voice-over
- **[36:45.0–36:55.5] VO:** Một neural operator tốt cần ít nhất ba property.
- **[36:55.5–37:06.5] VO:** Thứ nhất: input có thể được cung cấp ở nhiều discretization.
- **[37:06.5–37:18.0] VO:** Thứ hai: output có thể query ở các điểm ta muốn, không bị khóa vào một grid duy nhất.
- **[37:18.0–37:33.0] VO:** Thứ ba: khi mesh refinement tiến dần về continuum, model converges về một operator limit nhất quán.
- **[37:33.0–37:34.0] Pause:** 1.0s.
- **[37:34.0–37:48.5] VO:** Đây là lý do các operation bên trong model thường được xây như xấp xỉ của operation continuum.
- **[37:48.5–38:02.5] VO:** Matrix multiplication trên index cố định không đủ tự nhiên. Integral operator thì tự nhiên hơn.
- **[38:02.5–38:40.0] VO:** Vậy để xây neural operator từ neural network, ta cần một trick đẹp: nhìn lại một layer neural network như một Riemann sum.

### Visual / Manim direction
- Three property cards appear.
- Cards become constraints on architecture.
- Camera moves into a neural network layer.

### Manim objects
- `PropertyCards`, `ConstraintArrows`, `NeuralLayerZoom`.

---

## Scene 6.3 — The suspense line
**Time:** 38:40.0–42:30.0

### Voice-over
- **[38:40.0–38:52.0] VO:** Từ đây đến vài phút tới là phần quan trọng nhất của tutorial.
- **[38:52.0–39:03.5] VO:** Ta sẽ không định nghĩa neural operator bằng cách ném ra một công thức rồi hy vọng mọi người tin.
- **[39:03.5–39:15.0] VO:** Ta sẽ bắt đầu từ neural network layer quen thuộc, rồi biến nó từng bước thành integral operator.
- **[39:15.0–39:16.0] Pause:** 1.0s.
- **[39:16.0–39:29.5] VO:** Nếu phần này click, các kiến trúc phía sau — GNO, FNO, Transformer Neural Operator — sẽ trở nên hợp lý hơn rất nhiều.
- **[39:29.5–39:44.0] VO:** Nhưng trước khi làm điều đó, cần hai mảnh toán rất cũ: xấp xỉ tích phân và xấp xỉ đạo hàm.
- **[39:44.0–39:57.0] VO:** Đây là những thứ ta đã gặp từ calculus hoặc numerical methods.
- **[39:57.0–40:13.0] VO:** Tích phân có thể xấp xỉ bằng tổng các giá trị function nhân với độ rộng ô lưới.
- **[40:13.0–40:28.0] VO:** Đạo hàm có thể xấp xỉ bằng finite difference: lấy hiệu hai giá trị gần nhau, chia cho khoảng cách.
- **[40:28.0–40:45.0] VO:** Hai ý tưởng này nghe đơn giản, nhưng chúng là cầu nối giữa function continuum và tensor computation.
- **[40:45.0–42:30.0] VO:** Và bây giờ, ta đi vào chiếc cầu đó.

### Visual / Manim direction
- Slow zoom into chalkboard.
- Show Riemann rectangles and finite difference arrows.
- No heavy equation reading; equations appear as visual support.

### Manim objects
- `RiemannRectangles`, `FiniteDifferenceSecant`, `BridgeGraphic`.

---

# 7. Pre-req: Integrals and Derivatives

## Scene 7.1 — Riemann sum as a computation recipe
**Time:** 42:30.0–44:20.0

### Voice-over
- **[42:30.0–42:41.0] VO:** Giả sử ta có một function một chiều, và chỉ biết giá trị của nó tại các điểm sample.
- **[42:41.0–42:54.0] VO:** Muốn xấp xỉ diện tích dưới đường cong, ta cộng các cột nhỏ: chiều cao là giá trị function, chiều rộng là bước lưới.
- **[42:54.0–43:07.5] VO:** Lưới càng mịn, tổng này càng tiến gần tích phân thật.
- **[43:07.5–43:08.5] Pause:** 1.0s.
- **[43:08.5–43:22.0] VO:** Điều quan trọng ở đây là: cùng một integral continuum có thể được tính gần đúng từ nhiều discretization khác nhau.
- **[43:22.0–43:37.0] VO:** Nếu sample không đều, mỗi điểm không nên đóng góp như nhau. Ta cần weight tương ứng với local cell size hoặc quadrature rule.
- **[43:37.0–44:20.0] VO:** Chính ý tưởng “sum có trọng số như xấp xỉ integral” sẽ xuất hiện lại trong neural operator layer.

### Visual / Manim direction
- Curve with rectangles.
- Switch uniform grid to nonuniform grid; rectangle widths change.
- Label `sum ≈ integral`.

### Manim objects
- `Axes`, `Curve`, `RiemannRectangles`, `NonUniformTicks`.

---

## Scene 7.2 — Finite difference as local physics probe
**Time:** 44:20.0–46:20.0

### Voice-over
- **[44:20.0–44:31.5] VO:** Bây giờ là đạo hàm. Nếu function là một đường cong, đạo hàm tại một điểm đo độ nghiêng local.
- **[44:31.5–44:43.0] VO:** Với dữ liệu rời rạc, ta lấy chênh lệch giữa hai điểm gần nhau, chia cho khoảng cách.
- **[44:43.0–44:56.0] VO:** Lưới càng mịn, finite difference càng có cơ hội xấp xỉ đạo hàm tốt hơn.
- **[44:56.0–44:57.0] Pause:** 1.0s.
- **[44:57.0–45:10.5] VO:** Trong physics, derivative không phải chi tiết phụ. Nó nằm ngay trong PDE.
- **[45:10.5–45:24.5] VO:** Vì vậy một model output function phải cho phép ta tính derivative một cách có nghĩa.
- **[45:24.5–45:41.5] VO:** Từ đây, hãy nhớ hai phép toán: integral để tổng hợp thông tin toàn domain, derivative để đọc local structure.
- **[45:41.5–46:20.0] VO:** Neural operator sẽ cần cả hai: integral operator để map function sang function, và đôi khi differential component để bắt local physics.

### Visual / Manim direction
- Tangent line at a point.
- Two finite difference stencils appear.
- PDE residual icon depends on derivative.

### Manim objects
- `TangentLine`, `Stencil`, `PDEResidualBubble`.

---

# 8. From Neural Networks to Neural Operators

## Scene 8.1 — A basic neural network layer
**Time:** 46:20.0–47:50.0

### Voice-over
- **[46:20.0–46:31.5] VO:** Hãy bắt đầu với một layer neural network cực cơ bản.
- **[46:31.5–46:43.0] VO:** Input là một vector gồm các giá trị `a_1`, `a_2`, đến `a_n`.
- **[46:43.0–46:56.0] VO:** Layer nhân vector này với một matrix weight, cộng lại, rồi đưa qua nonlinearity.
- **[46:56.0–46:57.0] Pause:** 1.0s.
- **[46:57.0–47:10.0] VO:** Nhưng bây giờ hãy tưởng tượng vector đó không chỉ là vector ngẫu nhiên.
- **[47:10.0–47:25.0] VO:** Nó là các point evaluation của một function `a`, tại các điểm `x_1`, `x_2`, đến `x_n`.
- **[47:25.0–47:50.0] VO:** Tức là `a_j` thật ra là `a` tại điểm `x_j`.

### Visual / Manim direction
- Draw vector column.
- Each entry unfolds to sample point on curve.
- Matrix multiplication shown as weighted sum.

### Manim objects
- `ColumnVector`, `SampledCurve`, `WeightMatrix`.

---

## Scene 8.2 — Replace indices by locations
**Time:** 47:50.0–49:40.0

### Voice-over
- **[47:50.0–48:02.0] VO:** Trong neural network thường, weight matrix được index bằng hai số: output index `i` và input index `j`.
- **[48:02.0–48:14.5] VO:** Nhưng nếu input index `j` tương ứng với location `x_j`, và output index `i` tương ứng với location `y_i`, ta có thể đổi cách nhìn.
- **[48:14.5–48:28.5] VO:** Weight không chỉ là `K_ij`. Nó có thể được xem như giá trị của một kernel function tại cặp điểm `y_i` và `x_j`.
- **[48:28.5–48:29.5] Pause:** 1.0s.
- **[48:29.5–48:44.0] VO:** Đây là bước đổi vai rất đẹp: matrix rời rạc trở thành sampling của một kernel continuum.
- **[48:44.0–49:00.5] VO:** Khi đó weighted sum của neural network bắt đầu trông giống Riemann sum.
- **[49:00.5–49:40.0] VO:** Và nếu ta thay hệ số `1/n` hoặc bước lưới bằng `delta x`, tổng này tiến gần một tích phân.

### Visual / Manim direction
- Weight matrix entries glow.
- Matrix rows/columns map to `y_i` and `x_j` axes.
- Matrix becomes a continuous heatmap kernel `κ(y,x)`.
- Summation morphs into integral.

### Manim objects
- `MatrixHeatmap`, `KernelSurface`, `MorphSumToIntegral`.

---

## Scene 8.3 — The linear integral operator
**Time:** 49:40.0–51:25.0

### Voice-over
- **[49:40.0–49:53.0] VO:** Sau khi lấy limit continuum, ta nhận được một linear integral operator.
- **[49:53.0–50:07.0] VO:** Nó nhận input function `a`, quét qua domain bằng kernel, tích hợp thông tin, và trả ra một function mới theo query point `y`.
- **[50:07.0–50:08.0] Pause:** 1.0s.
- **[50:08.0–50:20.5] VO:** Đây là analog của linear layer trong finite-dimensional neural network.
- **[50:20.5–50:35.0] VO:** Matrix-vector product trở thành integral-kernel transform.
- **[50:35.0–50:48.0] VO:** Và giống neural network, sau linear part ta đặt nonlinearity pointwise.
- **[50:48.0–51:25.0] VO:** Một neural operator layer cơ bản vì vậy là: integral operator, cộng thêm nonlinearity, và được tính gần đúng trên discretization ta đang có.

### Visual / Manim direction
- Kernel lens sweeps across input curve and produces output curve.
- Show equation visually, but voice avoids reading symbols.
- Nonlinearity bends output.

### Manim objects
- `KernelLens`, `InputFunction`, `OutputFunction`, `PointwiseNonlinearity`.

---

## Scene 8.4 — Why this is familiar, not alien
**Time:** 51:25.0–52:55.0

### Voice-over
- **[51:25.0–51:38.0] VO:** Linear integral operator nghe có vẻ abstract, nhưng thật ra nó xuất hiện khắp nơi.
- **[51:38.0–51:50.0] VO:** Impulse response trong signal processing. Green’s function trong PDE. Frequency response. Convolution.
- **[51:50.0–52:03.5] VO:** Rất nhiều lời giải của phương trình vật lý có thể được viết theo dạng kernel tích phân.
- **[52:03.5–52:04.5] Pause:** 1.0s.
- **[52:04.5–52:19.5] VO:** Vì vậy neural operator không phải phép thuật từ trên trời rơi xuống. Nó lấy một cấu trúc rất cổ điển trong toán và biến nó thành learnable layer.
- **[52:19.5–52:55.0] VO:** Cái mới là: kernel không nhất thiết được hand-design. Nó có thể được parameterize và học từ data.

### Visual / Manim direction
- Cards: Green’s function, convolution, impulse response.
- Cards merge into `Kernel Operator`.
- A learnable parameter knob appears on kernel.

### Manim objects
- `ConceptCards`, `KernelOperatorCard`, `LearnableKnob`.

---

## Scene 8.5 — Any discretization can approximate the same layer
**Time:** 52:55.0–54:50.0

### Voice-over
- **[52:55.0–53:08.0] VO:** Trong thực tế, ta không bao giờ tính integral thật. Ta tính một sum trên các điểm sample.
- **[53:08.0–53:21.5] VO:** Nhưng đây chính là chỗ neural operator thắng về thiết kế: cùng một integral layer có thể được approximate trên grid thô, grid mịn, hoặc mesh không đều.
- **[53:21.5–53:34.5] VO:** Nếu input function được cho ở các điểm khác nhau, ta chỉ thay các điểm sample và weight tích phân tương ứng.
- **[53:34.5–53:35.5] Pause:** 1.0s.
- **[53:35.5–53:49.0] VO:** Output cũng vậy. Ta muốn giá trị ở điểm nào, ta query ở điểm đó.
- **[53:49.0–54:05.0] VO:** Vì vậy layer không bị định nghĩa bởi số pixel cố định. Nó được định nghĩa bởi kernel trên domain.
- **[54:05.0–54:50.0] VO:** Đây là tinh thần discretization-agnostic: computation vẫn rời rạc, nhưng architecture được nghĩ từ continuum xuống, không phải từ tensor shape đi lên.

### Visual / Manim direction
- Same kernel layer applied to three sampling patterns.
- Output query points move independently.
- Show “same parameters” badge.

### Manim objects
- `SamplingPatternSet`, `SameKernelBadge`, `QueryGrid`.

---

## Scene 8.6 — Natural question: why not just interpolate?
**Time:** 54:50.0–58:50.0

### Voice-over
- **[54:50.0–55:02.0] VO:** Một câu hỏi tự nhiên là: tại sao không interpolate mọi thứ về một grid chung, rồi dùng CNN hoặc Transformer thường?
- **[55:02.0–55:03.0] Pause:** 1.0s.
- **[55:03.0–55:15.0] VO:** Đôi khi làm vậy vẫn hữu ích. Nhưng nó đưa một quyết định numerical preprocessing vào trước model.
- **[55:15.0–55:31.0] VO:** Nếu interpolation làm mất high-frequency detail, làm mờ boundary, hoặc xử lý sai geometry, model phía sau sẽ học trên một representation đã bị méo.
- **[55:31.0–55:44.5] VO:** Neural operator muốn trực tiếp reason trên function samples và query points, thay vì giả vờ mọi domain đều là ảnh vuông.
- **[55:44.5–55:45.5] Pause:** 1.0s.
- **[55:45.5–56:01.5] VO:** Một câu hỏi khác: nếu integral operator có xu hướng smooth input, làm sao giữ identity hoặc local detail?
- **[56:01.5–56:16.0] VO:** Đây là lý do residual connection rất quan trọng. Nó cho phép model truyền thông tin pointwise qua layer, giống skip connection trong neural network.
- **[56:16.0–56:31.0] VO:** Và vì output là function, bias cũng không chỉ là bias vector nữa. Nó trở thành bias function, phụ thuộc vào query point.
- **[56:31.0–56:46.0] VO:** Ta cũng có thể dùng measure hoặc quadrature phù hợp với domain, thay vì mặc định mọi điểm có weight giống nhau.
- **[56:46.0–57:05.0] VO:** Vậy một neural operator layer thực tế thường gồm: integral transform, pointwise residual, bias function, measure hoặc quadrature weight, và nonlinearity.
- **[57:05.0–57:25.0] VO:** Khi stack nhiều layer như vậy, ta nhận được một deep neural operator.
- **[57:25.0–58:50.0] VO:** Và bây giờ ta đã đi từ neural network layer cơ bản tới neural operator layer bằng một chain rất tự nhiên: vector sample → weighted sum → Riemann sum → integral operator → nonlinear function-to-function map.

### Visual / Manim direction
- Interpolation grid blurs boundary; warning.
- Residual path appears as bypass arrow.
- Bias function drawn as small curve added to output.
- Final layer block diagram forms.

### Manim objects
- `InterpolationBlurDemo`, `ResidualArrow`, `BiasFunction`, `NeuralOperatorLayerBlock`.

---

# 9. Full Neural Operator Architecture

## Scene 9.1 — Lift, operate, project
**Time:** 58:50.0–1:01:00.0

### Voice-over
- **[58:50.0–59:03.0] VO:** Kiến trúc neural operator đầy đủ thường có ba pha: lift, operate, project.
- **[59:03.0–59:16.0] VO:** Đầu tiên, input function `a` có thể có nhiều channel vật lý: temperature, velocity, humidity, land mask.
- **[59:16.0–59:29.0] VO:** Một pointwise encoder lift các giá trị này lên hidden feature space.
- **[59:29.0–59:43.0] VO:** Sau đó, ta apply nhiều neural operator layers để truyền thông tin trên domain.
- **[59:43.0–59:56.0] VO:** Cuối cùng, pointwise decoder project hidden features về các biến output ta cần.
- **[59:56.0–1:00:14.0] VO:** Nhìn rất giống neural network: encoder, hidden layers, decoder. Nhưng hidden layers ở đây là function-to-function layers.
- **[1:00:14.0–1:01:00.0] VO:** Điều này giúp model vừa xử lý nhiều physical variables, vừa giữ được interpretation ở level function space.

### Visual / Manim direction
- Pipeline: `a(x)` → `P(a(x))` → operator layers → `Q(v(x))` → `u(x)`.
- Weather channels as stacked colored fields.
- Feature channels as abstract glowing fields.

### Manim objects
- `ArchitecturePipeline`, `ChannelStack`, `OperatorLayerStack`.

---

## Scene 9.2 — Universal approximation, but with caveats
**Time:** 1:01:00.0–1:03:20.0

### Voice-over
- **[1:01:00.0–1:01:14.0] VO:** Một điểm lý thuyết quan trọng: neural operators có universal approximation result cho continuous operators giữa function spaces, dưới các điều kiện regularity phù hợp.
- **[1:01:14.0–1:01:27.0] VO:** Nói trực giác: nếu target operator đủ “nice”, tồn tại một neural operator có thể approximate nó tùy ý tốt trên compact set.
- **[1:01:27.0–1:01:28.2] Pause:** 1.2s.
- **[1:01:28.2–1:01:42.0] VO:** Nhưng đây không phải giấy phép để bỏ qua data, optimization, physics, hay domain knowledge.
- **[1:01:42.0–1:01:58.0] VO:** Universal approximation nói về expressivity: architecture có thể biểu diễn. Nó không tự động nói training sẽ dễ, data sẽ đủ, hay metric sẽ đúng.
- **[1:01:58.0–1:02:12.0] VO:** Trong scientific computing, những caveat này không phải footnote. Chúng thường là toàn bộ bài toán.
- **[1:02:12.0–1:02:34.0] VO:** Vì vậy ta nên hiểu theorem như một baseline niềm tin: neural operator không bị loại ngay từ đầu vì thiếu khả năng biểu diễn operator.
- **[1:02:34.0–1:03:20.0] VO:** Phần còn lại là câu hỏi research: parameterization nào hiệu quả, loss nào đúng, data nào đủ, và physics nào cần encode vào architecture.

### Visual / Manim direction
- A theorem card appears, then splits into “expressivity” vs “training/generalization/domain”.
- Avoid presenting proof; show conceptual theorem.

### Manim objects
- `TheoremCard`, `CaveatCards`, `ResearchQuestions`.

---

## Scene 9.3 — Error decomposition
**Time:** 1:03:20.0–1:05:10.0

### Voice-over
- **[1:03:20.0–1:03:31.5] VO:** Error của neural operator có thể được nhìn như hai phần chính ở operator level.
- **[1:03:31.5–1:03:45.0] VO:** Một phần là approximation error: operator đã học gần target operator continuum đến đâu.
- **[1:03:45.0–1:03:58.5] VO:** Phần kia là discretization error: khi ta chỉ có function samples trên mesh hữu hạn, xấp xỉ này sai bao nhiêu.
- **[1:03:58.5–1:03:59.5] Pause:** 1.0s.
- **[1:03:59.5–1:04:15.0] VO:** Generalization error vẫn tồn tại, vì training data có hạn. Nhưng discretization là dimension mới mà ML truyền thống thường không phải đối mặt rõ ràng.
- **[1:04:15.0–1:04:31.0] VO:** Điều này ảnh hưởng cả experiment design: train resolution, test resolution, mesh refinement, precision, và evaluation metric.
- **[1:04:31.0–1:05:10.0] VO:** Nếu report một model neural operator mà chỉ đánh giá trên cùng một grid cố định, ta mới kiểm tra được một phần rất nhỏ của câu chuyện.

### Visual / Manim direction
- Error bar decomposes into approximation + discretization + generalization.
- Experiment table: train 16, test 32, test 64; mesh refinement.
- Warning badge: “same-grid only ≠ full operator validation”.

### Manim objects
- `ErrorDecompositionBar`, `ResolutionExperimentTable`, `WarningBadge`.

---

## Scene 9.4 — Question embedded: what if input/output domains differ?
**Time:** 1:05:10.0–1:07:40.0

### Voice-over
- **[1:05:10.0–1:05:22.0] VO:** Một câu hỏi rất hay: nếu input domain và output domain khác nhau thì sao?
- **[1:05:22.0–1:05:36.0] VO:** Ví dụ, ta biết temperature trên các bức tường của một căn phòng, nhưng muốn dự đoán temperature trong volume 3D bên trong.
- **[1:05:36.0–1:05:49.0] VO:** Input là function trên surface 2D. Output là function trong volume 3D.
- **[1:05:49.0–1:05:50.0] Pause:** 1.0s.
- **[1:05:50.0–1:06:05.0] VO:** Integral kernel không bắt buộc `x` và `y` nằm trong cùng domain. Kernel có thể nhận một điểm input-domain và một điểm output-domain.
- **[1:06:05.0–1:06:20.5] VO:** Vì vậy operator layer vẫn có thể map từ domain này sang domain khác.
- **[1:06:20.5–1:06:36.0] VO:** Phần tinh tế là residual connection. Nếu không có identity map tự nhiên giữa hai domain, ta cần thiết kế residual hoặc pointwise map phù hợp.
- **[1:06:36.0–1:07:40.0] VO:** Đây là một ví dụ đẹp cho tinh thần chung: architecture phải được thiết kế theo geometry của bài toán, không phải ép bài toán theo architecture sẵn có.

### Visual / Manim direction
- 2D wall surface with boundary temperature.
- 3D room volume field appears.
- Kernel connects wall points to interior query point.
- Residual arrow appears only when domains compatible; otherwise a learned map bridge.

### Manim objects
- `WallSurface`, `RoomVolume`, `CrossDomainKernel`, `LearnedResidualBridge`.

---

# 10. Architectures

## Scene 10.1 — Graph Neural Operator: learn the kernel directly
**Time:** 1:07:40.0–1:10:10.0

### Voice-over
- **[1:07:40.0–1:07:53.5] VO:** Cách implement đầu tiên rất trực tiếp: parameterize kernel bằng một neural network.
- **[1:07:53.5–1:08:08.0] VO:** Với mỗi output query point `y`, ta nhìn các input sample point `x`, tính kernel value, nhân với feature tại `x`, rồi sum theo quadrature weight.
- **[1:08:08.0–1:08:09.0] Pause:** 1.0s.
- **[1:08:09.0–1:08:21.5] VO:** Đây là Graph Neural Operator, hay kernel neural operator.
- **[1:08:21.5–1:08:36.0] VO:** Nó giống Graph Neural Network ở chỗ ta truyền message giữa các điểm. Nhưng graph được xây từ metric space và discretization của domain.
- **[1:08:36.0–1:08:50.0] VO:** Nếu thiết kế đúng, khi mesh refine, computation vẫn approximate cùng một integral operator.
- **[1:08:50.0–1:09:07.0] VO:** Kernel có thể local, chỉ nhìn neighborhood gần `y`, hoặc global, nhìn toàn domain.
- **[1:09:07.0–1:10:10.0] VO:** Trade-off là compute. Kernel trực tiếp rất linh hoạt cho irregular geometry, nhưng nếu kết nối quá nhiều điểm, chi phí có thể lớn.

### Visual / Manim direction
- Irregular point cloud.
- Query point receives weighted messages from neighbors.
- Local radius grows/shrinks.
- Compare local sparse graph vs global dense graph.

### Manim objects
- `PointCloud`, `QueryNode`, `MessageEdges`, `RadiusCircle`.

---

## Scene 10.2 — Basis projection: integrate by changing representation
**Time:** 1:10:10.0–1:12:20.0

### Voice-over
- **[1:10:10.0–1:10:22.0] VO:** Một cách khác để tính integral là không học kernel trực tiếp trong physical space.
- **[1:10:22.0–1:10:34.5] VO:** Ta project input function lên một tập basis functions, xử lý các coefficient, rồi project ngược ra output space.
- **[1:10:34.5–1:10:47.0] VO:** Ý tưởng này cực quen thuộc trong numerical analysis và signal processing.
- **[1:10:47.0–1:10:48.0] Pause:** 1.0s.
- **[1:10:48.0–1:11:03.5] VO:** Nhưng khi project lên hữu hạn basis, ta có nguy cơ bỏ mất thông tin ở các mode không giữ lại.
- **[1:11:03.5–1:11:18.0] VO:** Đây lại là lý do residual connection quan trọng: nó giúp thông tin pointwise không bị ném sạch qua bottleneck basis.
- **[1:11:18.0–1:11:36.0] VO:** Basis có thể là Fourier, wavelet, PCA basis, Laplacian eigenbasis, hoặc learned basis.
- **[1:11:36.0–1:12:20.0] VO:** Mỗi lựa chọn basis encode một giả định về domain và regularity của solution.

### Visual / Manim direction
- Function decomposes into basis waves.
- Coefficients are manipulated by learned matrix.
- Reconstruct output.
- Residual skip carries original function around projection.

### Manim objects
- `BasisFunctions`, `CoefficientBars`, `Reconstruction`, `ResidualSkip`.

---

## Scene 10.3 — Fourier Neural Operator
**Time:** 1:12:20.0–1:15:40.0

### Voice-over
- **[1:12:20.0–1:12:31.5] VO:** Nếu basis là Fourier basis, ta đến Fourier Neural Operator, hay FNO.
- **[1:12:31.5–1:12:45.0] VO:** Trực giác rất gọn: đưa function sang frequency domain, học cách mix một số Fourier modes, rồi inverse transform về physical domain.
- **[1:12:45.0–1:12:58.0] VO:** Với regular grid, Fourier transform có thể được tính bằng FFT, nên FNO rất nhanh.
- **[1:12:58.0–1:12:59.0] Pause:** 1.0s.
- **[1:12:59.0–1:13:13.5] VO:** Đây là lý do FNO trở thành một kiến trúc rất nổi bật cho PDE surrogate, đặc biệt trên grid đều.
- **[1:13:13.5–1:13:30.0] VO:** Nó học global interaction tốt, vì một Fourier mode có support toàn domain.
- **[1:13:30.0–1:13:46.0] VO:** Nhưng global không phải lúc nào cũng đủ. Nếu hiện tượng có local shock, boundary layer, hoặc discontinuity, Fourier-only có thể smooth quá mức.
- **[1:13:46.0–1:14:02.0] VO:** Đây là lúc các hybrid local/global operator, local integral kernels, hoặc differential kernels trở nên quan trọng.
- **[1:14:02.0–1:14:20.0] VO:** Một câu hỏi tự nhiên: tại sao nói FNO là “semi-generalization” của convolution?
- **[1:14:20.0–1:14:36.0] VO:** Vì khi ta giữ một số Fourier modes, trong spatial domain nó tương ứng với một kernel có receptive field lớn.
- **[1:14:36.0–1:14:53.0] VO:** Nhưng nếu resolution tăng mà số modes giữ lại không tăng tương ứng để cover toàn spectrum, ta không đơn giản recover mọi convolution nhỏ như CNN truyền thống.
- **[1:14:53.0–1:15:40.0] VO:** Vì vậy FNO rất mạnh, nhưng không phải cây đũa thần. Nó là một lựa chọn parameterization, tốt khi giả định frequency-domain phù hợp với physics.

### Visual / Manim direction
- Function → Fourier transform: spectrum bars.
- Low-frequency modes retained, high modes faded.
- Learned complex weights on modes.
- Inverse transform reconstructs output.
- Show global waves vs local sharp feature.

### Manim objects
- `FourierTransformAnimation`, `SpectrumBars`, `ModeWeights`, `InverseFFT`, `SharpFeatureDemo`.

---

## Scene 10.4 — Numerical-analysis family: quadrature, Galerkin, multigrid, U-NO
**Time:** 1:15:40.0–1:18:20.0

### Voice-over
- **[1:15:40.0–1:15:53.0] VO:** Tutorial gốc nhấn mạnh một ý rất hay: integration đã được con người nghiên cứu hàng nghìn năm.
- **[1:15:53.0–1:16:06.0] VO:** Vì vậy có nhiều cách đưa numerical analysis vào neural operator.
- **[1:16:06.0–1:16:18.0] VO:** Quadrature nói rằng mỗi sample point nên có weight phù hợp, không chỉ delta x đơn giản.
- **[1:16:18.0–1:16:32.0] VO:** Galerkin-style methods nghĩ theo projection lên subspaces và xử lý ở nhiều resolution.
- **[1:16:32.0–1:16:49.0] VO:** Multigrid intuition nói: near field cần chi tiết cao; far field có thể được tóm tắt ở resolution thấp hơn.
- **[1:16:49.0–1:17:05.0] VO:** Và U-shaped neural operator, như U-NO hoặc multipole-style operator, đưa tinh thần encoder-decoder của U-Net sang function space.
- **[1:17:05.0–1:17:19.0] VO:** Domain được co lại ở hidden levels, rồi mở lại, để capture interaction ở nhiều scale.
- **[1:17:19.0–1:18:20.0] VO:** Đây là một pattern mạnh: nhiều architecture deep learning quen thuộc có bản operator-learning tương ứng, nhưng chỉ khi ta viết lại chúng bằng ngôn ngữ function space.

### Visual / Manim direction
- Quick montage:
  - quadrature weights over points,
  - projection to basis,
  - multigrid V-cycle,
  - U-shaped operator architecture.
- Each component gets 5–8 seconds.

### Manim objects
- `QuadratureWeights`, `ProjectionDiagram`, `VCycle`, `UNoArchitecture`.

---

## Scene 10.5 — Transformer Neural Operator
**Time:** 1:18:20.0–1:20:30.0

### Voice-over
- **[1:18:20.0–1:18:33.0] VO:** Bây giờ đến Transformer. Attention layer thường tính weighted sum giữa tokens.
- **[1:18:33.0–1:18:46.0] VO:** Nếu tokens là sample points của một function, ta lại gặp cùng một câu chuyện: sum nên trở thành approximation của integral.
- **[1:18:46.0–1:19:00.0] VO:** Query, key, value không còn chỉ là vector tại token index. Chúng là functions hoặc pointwise features trên domain.
- **[1:19:00.0–1:19:01.0] Pause:** 1.0s.
- **[1:19:01.0–1:19:17.0] VO:** Với regular grid, một số weight theo delta x có thể cancel, nên implementation nhìn rất giống attention thường.
- **[1:19:17.0–1:19:31.0] VO:** Nhưng khi grid irregular, hoặc resolution thay đổi, những measure factor này không được quên.
- **[1:19:31.0–1:19:48.0] VO:** Đây là bài học lặp lại: nếu ta chỉ copy architecture từ finite-dimensional ML, ta dễ bỏ sót yếu tố continuum.
- **[1:19:48.0–1:20:30.0] VO:** Transformer Neural Operator vì vậy không chỉ là “attention trên grid lớn”, mà là attention được diễn giải như operator trên function space.

### Visual / Manim direction
- Attention matrix between sample points.
- Sum morphs into integral attention.
- Regular grid cancels weights; irregular grid shows weights remain.

### Manim objects
- `AttentionMatrix`, `IntegralAttention`, `GridWeightFactors`.

---

## Scene 10.6 — Codomain attention: variables as function tokens
**Time:** 1:20:30.0–1:22:30.0

### Voice-over
- **[1:20:30.0–1:20:43.0] VO:** Có một biến thể rất thú vị: attention không chỉ trên domain points, mà trên codomain variables.
- **[1:20:43.0–1:20:56.0] VO:** Trong weather hoặc multiphysics, mỗi sample có thể chứa rất nhiều variables: pressure, velocity, humidity, displacement, temperature.
- **[1:20:56.0–1:21:10.0] VO:** Các dataset khác nhau có thể lưu các subset variables khác nhau. Dataset này có 100 biến, dataset kia có 5 biến.
- **[1:21:10.0–1:21:11.0] Pause:** 1.0s.
- **[1:21:11.0–1:21:26.5] VO:** Codomain Attention Neural Operator xem mỗi physical variable như một token — nhưng token này không phải một vector nhỏ, mà là một function.
- **[1:21:26.5–1:21:43.0] VO:** Attention giữa variables cho phép transfer knowledge giữa PDE systems có overlapping variables.
- **[1:21:43.0–1:22:00.0] VO:** Mỗi variable cần variable-specific positional encoding, vì không có thứ tự token cố định như trong câu văn.
- **[1:22:00.0–1:22:30.0] VO:** Đây là bước đi về hướng foundation model cho scientific fields: train trên nhiều systems, adapt sang system mới mà không redesign architecture từ đầu.

### Visual / Manim direction
- Weather variables as stacked functions.
- Each variable becomes a token-function card.
- Attention graph between variable cards.
- New variable added; architecture still works.

### Manim objects
- `VariableFunctionCards`, `CodomainAttentionGraph`, `VSPELabel`.

---

## Scene 10.7 — Local and differential kernels
**Time:** 1:22:30.0–1:24:10.0

### Voice-over
- **[1:22:30.0–1:22:43.5] VO:** Đến đây, ta có integral operators. Nhưng physics cũng rất thích derivatives.
- **[1:22:43.5–1:22:56.0] VO:** Nếu bài toán yêu cầu map từ `u` sang forcing hoặc residual, derivative có thể là operation trung tâm.
- **[1:22:56.0–1:23:09.5] VO:** CNN kernels đã lâu được dùng để detect edges, tức là bắt local differences.
- **[1:23:09.5–1:23:10.5] Pause:** 1.0s.
- **[1:23:10.5–1:23:26.0] VO:** Nhưng để trở thành differential operator nhất quán khi resolution thay đổi, kernel coefficients phải scale theo grid size.
- **[1:23:26.0–1:23:41.0] VO:** Nếu grid size giảm một nửa, stencil derivative cũng phải scale tương ứng.
- **[1:23:41.0–1:24:10.0] VO:** Local integral kernels và differential kernels là cách đưa local physics vào neural operator mà vẫn giữ tinh thần predict-at-any-resolution.

### Visual / Manim direction
- CNN stencil becomes derivative stencil.
- Grid refined; coefficients scale.
- Compare regular kernel collapsing vs differential kernel limit.

### Manim objects
- `CNNStencil`, `DerivativeStencil`, `ScalingAnnotation`, `KernelLimitDiagram`.

---

# 11. Domains, Not Just Applications

## Scene 11.1 — “These are domains, not applications”
**Time:** 1:24:10.0–1:26:10.0

### Voice-over
- **[1:24:10.0–1:24:23.0] VO:** Một điểm rất đáng nhớ trong tutorial: weather, seismology, automotive CFD, molecular dynamics không chỉ là applications.
- **[1:24:23.0–1:24:35.0] VO:** Chúng là domains của machine learning.
- **[1:24:35.0–1:24:48.0] VO:** Nghĩa là mỗi domain cần problem setup, dataset, loss, metric, architecture bias, và validation protocol riêng.
- **[1:24:48.0–1:24:49.0] Pause:** 1.0s.
- **[1:24:49.0–1:25:04.0] VO:** Giống như computer vision mất nhiều năm để biết benchmark nào có nghĩa, scientific ML cũng cần xây lại hệ sinh thái đó.
- **[1:25:04.0–1:25:19.5] VO:** Không có một loss universal kiểu “cứ L2 là xong”. Có domain cần conservation. Có domain cần rare event. Có domain cần uncertainty.
- **[1:25:19.5–1:26:10.0] VO:** Vì vậy neural operator nên được hiểu như một framework để xây ML cho scientific domains, không phải một nút bấm auto-solve mọi PDE.

### Visual / Manim direction
- App icons become domain pillars.
- Each pillar has dataset/loss/metric/physics/architecture labels.
- “No plug-and-play” stamp.

### Manim objects
- `DomainPillars`, `EcosystemLabels`, `NoPlugAndPlayStamp`.

---

## Scene 11.2 — Weather forecast
**Time:** 1:26:10.0–1:29:00.0

### Voice-over
- **[1:26:10.0–1:26:23.0] VO:** Weather forecasting là một trong những domain quan trọng nhất cho ML trên function spaces.
- **[1:26:23.0–1:26:37.0] VO:** Input là trạng thái khí quyển và đại dương; output là trạng thái tương lai.
- **[1:26:37.0–1:26:50.0] VO:** Vì domain là sphere, Fourier basis phẳng không phải lúc nào cũng là lựa chọn tự nhiên nhất.
- **[1:26:50.0–1:27:06.0] VO:** Một hướng là Spherical Fourier Neural Operator, dùng spherical harmonics để làm convolution trên sphere.
- **[1:27:06.0–1:27:07.0] Pause:** 1.0s.
- **[1:27:07.0–1:27:22.5] VO:** Đây là ví dụ rất đẹp của domain-informed architecture: basis được chọn theo geometry của Trái Đất.
- **[1:27:22.5–1:27:39.0] VO:** Vì inference nhanh, model có thể chạy nhiều ensemble members để estimate distribution của future weather.
- **[1:27:39.0–1:27:54.5] VO:** Nhưng đây cũng là nơi open problems nổi rõ: chaos, uncertainty, extremes, calibration, và metrics.
- **[1:27:54.5–1:29:00.0] VO:** Model forecast nhìn đẹp chưa đủ. Nó phải đúng với domain metric, đúng với event quan trọng, và đáng tin khi quyết định thật phụ thuộc vào nó.

### Visual / Manim direction
- Sphere weather field.
- Spherical harmonic waves wrap around sphere.
- Ensemble forecasts split into many translucent futures.
- Uncertainty cloud.

### Manim objects
- `SphereField`, `SphericalHarmonicModes`, `EnsembleTrajectories`, `UncertaintyBand`.

---

## Scene 11.3 — Geophysics and inverse solvers
**Time:** 1:29:00.0–1:31:20.0

### Voice-over
- **[1:29:00.0–1:29:13.5] VO:** Trong geophysics, neural operator có thể học forward map: từ Earth structure và earthquake source sang wave propagation.
- **[1:29:13.5–1:29:26.0] VO:** Nhưng giá trị lớn nằm ở inverse problem.
- **[1:29:26.0–1:29:41.0] VO:** Ta quan sát sóng trên surface, rồi muốn suy ra cấu trúc bên dưới và source gây ra tín hiệu.
- **[1:29:41.0–1:29:42.0] Pause:** 1.0s.
- **[1:29:42.0–1:29:57.0] VO:** Vì neural operator nhanh và differentiable, nó có thể làm surrogate trong optimization hoặc Bayesian inversion.
- **[1:29:57.0–1:30:13.5] VO:** Nhưng inversion thường ill-posed: nhiều cấu trúc bên dưới có thể tạo observation tương tự.
- **[1:30:13.5–1:30:30.0] VO:** Vì vậy output tốt không chỉ là một estimate, mà là distribution hoặc uncertainty over possible structures.
- **[1:30:30.0–1:31:20.0] VO:** Đây là nơi neural operator gặp các algorithm như Langevin dynamics, diffusion-style sampling, hoặc MCMC trong function space.

### Visual / Manim direction
- Forward wave simulation.
- Surface sensors.
- Inverse loop with gradient arrows.
- Posterior distribution over subsurface fields.

### Manim objects
- `ForwardWaveOperator`, `SurfaceSensors`, `GradientInversionLoop`, `PosteriorFieldSamples`.

---

## Scene 11.4 — Carbon storage and climate mitigation
**Time:** 1:31:20.0–1:33:35.0

### Voice-over
- **[1:31:20.0–1:31:33.0] VO:** Một domain khác là carbon capture and storage: bơm CO2 xuống subsurface để giảm lượng carbon trong khí quyển.
- **[1:31:33.0–1:31:47.0] VO:** Bài toán là dự đoán plume CO2 lan thế nào trong lòng đất, dưới uncertainty rất lớn về cấu trúc địa chất.
- **[1:31:47.0–1:32:00.0] VO:** Mỗi realization của subsurface có thể cần một simulation đắt đỏ.
- **[1:32:00.0–1:32:01.0] Pause:** 1.0s.
- **[1:32:01.0–1:32:15.5] VO:** Nếu neural operator thay solver bằng surrogate nhanh hơn nhiều bậc độ lớn, ta có thể chạy nhiều scenario hơn.
- **[1:32:15.5–1:32:31.0] VO:** Điều này hỗ trợ uncertainty quantification và optimization cho reservoir engineers.
- **[1:32:31.0–1:32:47.0] VO:** Nhưng một lần nữa, physics và domain constraints rất quan trọng. Sai một chút ở plume boundary có thể ảnh hưởng lớn đến quyết định.
- **[1:32:47.0–1:33:35.0] VO:** Đây là ví dụ cho payoff thật của operator learning: không chỉ dự đoán nhanh, mà mở ra kiểu analysis trước đây quá đắt để làm ở scale lớn.

### Visual / Manim direction
- Underground reservoir cross-section.
- Injection wells.
- CO2 plume expands.
- Many realizations run in parallel like thumbnails.

### Manim objects
- `ReservoirCrossSection`, `InjectionWell`, `PlumeAnimation`, `ScenarioGrid`.

---

## Scene 11.5 — Molecular dynamics as continuous-time function
**Time:** 1:33:35.0–1:35:30.0

### Voice-over
- **[1:33:35.0–1:33:47.0] VO:** Molecular dynamics thường được visualize như một chuỗi frame.
- **[1:33:47.0–1:33:59.0] VO:** Nhưng bản chất tiến hóa của hệ là continuous in time.
- **[1:33:59.0–1:34:12.5] VO:** Nếu chỉ predict frame tiếp theo, ta có thể bỏ lỡ cấu trúc operator trên trajectory.
- **[1:34:12.5–1:34:13.5] Pause:** 1.0s.
- **[1:34:13.5–1:34:29.0] VO:** Operator learning cho phép nghĩ về map từ condition hoặc force field sang toàn bộ trajectory function.
- **[1:34:29.0–1:34:44.5] VO:** Trong protein engineering hoặc drug discovery, việc query trajectory, uncertainty, và long-time behavior đều quan trọng.
- **[1:34:44.5–1:35:30.0] VO:** Đây là domain mà ML không chỉ cần nhanh, mà còn phải respect symmetry, conservation, và stability qua thời gian.

### Visual / Manim direction
- Molecule frames morph into continuous trajectory curves.
- Operator maps initial condition to path.
- Symmetry icons rotate/translate.

### Manim objects
- `MoleculeGraph`, `TrajectoryTube`, `SymmetryIcons`.

---

## Scene 11.6 — Automotive CFD and domain knowledge
**Time:** 1:35:30.0–1:38:10.0

### Voice-over
- **[1:35:30.0–1:35:43.0] VO:** Trong automotive CFD, input có thể là geometry của xe, flow condition, hoặc mesh quanh bề mặt.
- **[1:35:43.0–1:35:55.5] VO:** Output là pressure, velocity, hoặc drag-related fields.
- **[1:35:55.5–1:36:09.0] VO:** Đây là bài toán cực nhạy với geometry và boundary.
- **[1:36:09.0–1:36:10.0] Pause:** 1.0s.
- **[1:36:10.0–1:36:25.0] VO:** Một câu hỏi tự nhiên từ Q&A gốc là: nếu output có discontinuity hoặc sharp feature thì sao?
- **[1:36:25.0–1:36:40.0] VO:** Câu trả lời thẳng: sẽ khó. Neural operator không tự động giải quyết discontinuity nếu architecture không có inductive bias phù hợp.
- **[1:36:40.0–1:36:57.0] VO:** Nếu domain expert biết loại discontinuity có thể xuất hiện, ta nên encode knowledge đó vào representation hoặc basis.
- **[1:36:57.0–1:37:15.0] VO:** Trong tutorial, điểm nhấn là domain knowledge giúp sample efficiency rất nhiều. Có những setting dùng vài trăm data points thay vì hàng triệu.
- **[1:37:15.0–1:38:10.0] VO:** Nhưng điều này không magic. Nó đến từ việc architecture được thiết kế cho physics, geometry, và regularity của domain.

### Visual / Manim direction
- Car mesh and pressure field.
- Sharp boundary layer highlighted.
- Generic smooth model blurs feature; domain-informed basis preserves it.
- Small data icon vs huge data icon.

### Manim objects
- `CarMesh`, `PressureField`, `BoundaryLayerHighlight`, `DomainKnowledgeModule`.

---

## Scene 11.7 — Physics verification
**Time:** 1:38:10.0–1:41:40.0

### Voice-over
- **[1:38:10.0–1:38:24.0] VO:** Một câu hỏi nữa: domain expert kiểm tra model output như thế nào?
- **[1:38:24.0–1:38:38.0] VO:** Không chỉ bằng mắt. Họ có thể đưa predicted function vào equation, tính residual, kiểm tra conservation, hoặc phát hiện tipping point.
- **[1:38:38.0–1:38:52.0] VO:** Ví dụ trong climate, khi thay đổi CO2 concentration, hệ có thể đi qua tipping point — một thay đổi đột ngột và đôi khi không đảo ngược.
- **[1:38:52.0–1:38:53.0] Pause:** 1.0s.
- **[1:38:53.0–1:39:08.0] VO:** Nếu model output là function theo thời gian, domain expert có thể kiểm tra nó bằng physical equations.
- **[1:39:08.0–1:39:25.0] VO:** Đây là lý do “output as function” không phải aesthetic choice. Nó là điều kiện để verification có nghĩa.
- **[1:39:25.0–1:39:42.0] VO:** Trong engineering, một field nhìn đẹp nhưng sai conservation có thể nguy hiểm hơn một model biết nói “tôi không chắc”.
- **[1:39:42.0–1:40:05.0] VO:** Vì vậy operator learning phải đi cùng uncertainty, calibration, physics-informed loss, và domain validation.
- **[1:40:05.0–1:41:40.0] VO:** Nếu chỉ tối ưu L2 trên snapshot, ta có thể thắng leaderboard nhỏ nhưng thua bài toán thật. Và đây là lý do phần cuối của tutorial dành cho open problems.

### Visual / Manim direction
- Predicted field is inserted into PDE residual checker.
- Conservation gauge.
- Tipping point curve vs CO2 level.
- L2 leaderboard cracks, physics validation remains.

### Manim objects
- `ResidualChecker`, `ConservationGauge`, `TippingPointCurve`, `LeaderboardCard`.

---

# 12. Open Problems

## Scene 12.1 — Accuracy is not just lower loss
**Time:** 1:41:40.0–1:44:05.0

### Voice-over
- **[1:41:40.0–1:41:53.0] VO:** Open problem đầu tiên: làm thế nào để accuracy trở thành absolute, không chỉ relative to benchmark?
- **[1:41:53.0–1:42:06.5] VO:** Trong image classification, sai một label là rõ. Trong weather hoặc fluid, sai một pattern nhỏ có thể tích lũy thành error lớn.
- **[1:42:06.5–1:42:19.0] VO:** Và L2 thấp không đảm bảo rare event đúng.
- **[1:42:19.0–1:42:20.0] Pause:** 1.0s.
- **[1:42:20.0–1:42:35.5] VO:** Domain cần metric riêng: anomaly correlation, energy spectrum, drag coefficient, mass conservation, PDE residual, calibration error.
- **[1:42:35.5–1:42:52.0] VO:** Đây là câu hỏi research: metric nào phản ánh đúng value của prediction?
- **[1:42:52.0–1:43:13.0] VO:** Một model có thể đẹp trên MSE nhưng sai high-frequency spectrum, sai boundary, hoặc sai physical invariant.
- **[1:43:13.0–1:44:05.0] VO:** Vì vậy “loss function là gì?” không phải implementation detail. Nó là một phần của problem formulation.

### Visual / Manim direction
- MSE loss bar low, but rare event missed.
- Multiple metric gauges appear.
- Loss function card becomes “problem formulation”.

### Manim objects
- `LossBar`, `RareEventMiss`, `MetricGauges`, `ProblemFormulationCard`.

---

## Scene 12.2 — Discretization, chaos, uncertainty
**Time:** 1:44:05.0–1:47:20.0

### Voice-over
- **[1:44:05.0–1:44:19.0] VO:** Open problem thứ hai: discretization error. Ta cần biết model thay đổi thế nào khi mesh thay đổi.
- **[1:44:19.0–1:44:33.0] VO:** Nếu train ở resolution này và deploy ở resolution khác, error có predictable không?
- **[1:44:33.0–1:44:48.0] VO:** Mesh refinement có làm solution hội tụ không, hay chỉ tạo ra artifact đẹp hơn?
- **[1:44:48.0–1:44:49.0] Pause:** 1.0s.
- **[1:44:49.0–1:45:04.0] VO:** Open problem thứ ba: chaos. Nhiều hệ như weather rất nhạy với initial condition.
- **[1:45:04.0–1:45:19.5] VO:** Trong hệ chaotic, dự đoán point estimate rất xa trong tương lai có thể không có nghĩa bằng dự đoán distribution hoặc statistics.
- **[1:45:19.5–1:45:35.0] VO:** Open problem thứ tư: uncertainty. Model cần biết khi nào nó không chắc.
- **[1:45:35.0–1:45:51.0] VO:** Điều này quan trọng trong forecast, inverse problem, và bất kỳ quyết định engineering nào có risk.
- **[1:45:51.0–1:46:13.0] VO:** Ta cần calibrated uncertainty, probabilistic neural operators, ensembles, conformal prediction, hoặc sampling trong function space.
- **[1:46:13.0–1:47:20.0] VO:** Đây là nơi operator learning giao với probabilistic modeling, dynamical systems, và numerical analysis. Một stack khá căng, nhưng cũng chính là chỗ research thú vị nhất.

### Visual / Manim direction
- Mesh refinement uncertainty.
- Chaotic trajectories diverge.
- Prediction cone/distribution instead of single line.
- Uncertainty band around function output.

### Manim objects
- `MeshErrorPlot`, `ChaoticTrajectories`, `ProbabilityCone`, `UncertaintyBand`.

---

## Scene 12.3 — Scaling and multiple datasets
**Time:** 1:47:20.0–1:50:20.0

### Voice-over
- **[1:47:20.0–1:47:33.0] VO:** Open problem tiếp theo là scale.
- **[1:47:33.0–1:47:46.5] VO:** Trong language model, scale story tương đối rõ: nhiều data hơn, model lớn hơn, compute lớn hơn.
- **[1:47:46.5–1:48:00.0] VO:** Trong scientific domains, data không đồng nhất như text trên web.
- **[1:48:00.0–1:48:13.5] VO:** Dataset khác nhau có variables khác nhau, resolution khác nhau, solver khác nhau, physics khác nhau, noise khác nhau.
- **[1:48:13.5–1:48:14.5] Pause:** 1.0s.
- **[1:48:14.5–1:48:29.5] VO:** Vậy train một model trên nhiều datasets như thế nào?
- **[1:48:29.5–1:48:45.0] VO:** Làm sao model biết variable nào là pressure, variable nào là velocity, và relation nào transfer được?
- **[1:48:45.0–1:49:01.0] VO:** Codomain attention là một gợi ý, nhưng chưa phải lời giải cuối.
- **[1:49:01.0–1:49:21.0] VO:** Ta cần data curation, metadata, geometry encoding, variable encoding, multi-resolution training, và domain-specific pretraining objective.
- **[1:49:21.0–1:50:20.0] VO:** Nếu operator foundation model tồn tại, nó sẽ không chỉ là Transformer to hơn. Nó phải biết function spaces, geometry, physics, và uncertainty.

### Visual / Manim direction
- Many datasets as mismatched tiles.
- Variables align partially.
- A model tries to connect them via metadata and codomain attention.
- Foundation model silhouette.

### Manim objects
- `DatasetTiles`, `VariableAlignmentGraph`, `FoundationModelSilhouette`.

---

## Scene 12.4 — Incorporating physics and domain knowledge
**Time:** 1:50:20.0–1:53:05.0

### Voice-over
- **[1:50:20.0–1:50:33.0] VO:** Open problem lớn nhất có lẽ là: encode physics thế nào cho đúng mức?
- **[1:50:33.0–1:50:46.0] VO:** Quá ít domain knowledge, model cần quá nhiều data và có thể violate physical laws.
- **[1:50:46.0–1:51:00.0] VO:** Quá nhiều hand-designed bias, model có thể mất flexibility và không học được unknown physics.
- **[1:51:00.0–1:51:01.0] Pause:** 1.0s.
- **[1:51:01.0–1:51:16.0] VO:** Ta cần tìm điểm cân bằng: symmetry, conservation, boundary conditions, basis choice, local kernels, differential operators, physics-informed losses.
- **[1:51:16.0–1:51:33.0] VO:** Mỗi domain sẽ có câu trả lời khác nhau.
- **[1:51:33.0–1:51:50.0] VO:** Đây là lý do tutorial gốc nhấn mạnh rằng chúng ta đang ở giai đoạn đầu của một field mới.
- **[1:51:50.0–1:52:10.0] VO:** Neural operator mở cửa, nhưng bước qua cửa đó cần collaboration giữa ML researchers, applied mathematicians, physicists, engineers, và domain experts.
- **[1:52:10.0–1:53:05.0] VO:** Nếu chỉ có ML, ta có thể tối ưu sai objective. Nếu chỉ có solver truyền thống, ta có thể bỏ lỡ tốc độ và khả năng học từ data. Sức mạnh nằm ở kết hợp cả hai.

### Visual / Manim direction
- Balance scale: data-driven flexibility vs physics prior.
- Physics modules slot into neural operator block.
- Collaboration graph between disciplines.

### Manim objects
- `BalanceScale`, `PhysicsPriorBlocks`, `CollaborationNetwork`.

---

## Scene 12.5 — The honest state of the field
**Time:** 1:53:05.0–1:55:20.0

### Voice-over
- **[1:53:05.0–1:53:18.0] VO:** Nói thẳng: neural operators chưa phải lời giải cuối cho scientific computing.
- **[1:53:18.0–1:53:32.0] VO:** Accuracy chưa luôn đủ. Metrics chưa thống nhất. Scaling chưa rõ. OOD behavior còn khó.
- **[1:53:32.0–1:53:46.0] VO:** Nhưng chúng đưa ra một language rất mạnh để nói về ML trên function spaces.
- **[1:53:46.0–1:53:47.0] Pause:** 1.0s.
- **[1:53:47.0–1:54:04.0] VO:** Thay vì ép mọi thứ thành ảnh hoặc vector, ta hỏi: operator underlying là gì? Domain là gì? Discretization ảnh hưởng thế nào?
- **[1:54:04.0–1:54:21.0] VO:** Và model có hội tụ về một object continuum có nghĩa không?
- **[1:54:21.0–1:54:39.0] VO:** Những câu hỏi này đưa machine learning gần hơn với ngôn ngữ của scientific computing.
- **[1:54:39.0–1:55:20.0] VO:** Đó là lý do neural operator không chỉ là một architecture trend. Nó là một cách định nghĩa lại nơi ML gặp physics.

### Visual / Manim direction
- Open problems list remains on board.
- Some items glow unresolved.
- Function-space operator diagram returns, now surrounded by domains.

### Manim objects
- `OpenProblemsBoard`, `FunctionSpaceDiagram`, `DomainOrbit`.

---

# 13. Closing

## Scene 13.1 — Final synthesis
**Time:** 1:55:20.0–1:57:30.0

### Voice-over
- **[1:55:20.0–1:55:33.0] VO:** Hãy tóm lại toàn bộ câu chuyện bằng một đường thẳng.
- **[1:55:33.0–1:55:46.0] VO:** Deep learning truyền thống học function giữa finite-dimensional spaces.
- **[1:55:46.0–1:55:59.0] VO:** Scientific computing thường cần map giữa function spaces.
- **[1:55:59.0–1:56:12.0] VO:** Traditional solvers solve từng instance bằng phương trình và discretization.
- **[1:56:12.0–1:56:26.0] VO:** Operator learning hỏi: liệu ta có thể học solution operator từ data không?
- **[1:56:26.0–1:56:41.0] VO:** Neural operator trả lời bằng architecture dựa trên integral operators, nonlinearities, residuals, và discretization-aware computation.
- **[1:56:41.0–1:56:58.0] VO:** GNO học kernel trên graph geometry. FNO dùng Fourier modes và FFT. Transformer NO diễn giải attention như integral. CoDA-NO đưa attention sang variables.
- **[1:56:58.0–1:57:30.0] VO:** Và toàn bộ field vẫn đang mở: metrics, uncertainty, chaos, scaling, physics, multi-dataset learning.

### Visual / Manim direction
- A single flowing diagram from finite vectors → functions → solvers → operators → architectures → domains → open problems.
- Each previous motif appears briefly.

### Manim objects
- `GrandSummaryFlow`, `MotifReplays`.

---

## Scene 13.2 — Last line
**Time:** 1:57:30.0–1:58:20.0

### Voice-over
- **[1:57:30.0–1:57:42.0] VO:** Nếu phải giữ lại một câu, hãy giữ câu này.
- **[1:57:42.0–1:57:43.0] Pause:** 1.0s.
- **[1:57:43.0–1:58:00.0] VO:** Khi dữ liệu là function, model cũng phải được thiết kế như một object sống trên function space.
- **[1:58:00.0–1:58:12.0] VO:** Neural operators là một trong những bước nghiêm túc nhất theo hướng đó.
- **[1:58:12.0–1:58:20.0] VO:** Và phần thú vị nhất là: field này mới chỉ bắt đầu.

### Visual / Manim direction
- Fade all visuals into one clean operator arrow `𝒢: 𝒜 → 𝒰`.
- Final text: **Learning in infinite dimensions.**
- Fade out.

### Manim objects
- `FinalOperatorArrow`, `Text("Learning in infinite dimensions")`.

---

# Appendix A — Voice Production Notes

1. **Do not generate one giant audio file.** Generate per section or per scene using scene IDs.
2. **Recommended TTS chunk:** one scene at a time. If a scene is longer than 2 minutes, split by VO lines.
3. **Alignment method:** render silent Manim scenes using `duration` from this file; generate voice per scene; then retime animation with `voice_duration / planned_duration` only if mismatch > 5%.
4. **Pause handling:** keep explicit pauses as silent audio segments, not just punctuation.
5. **Formula reading rule:** formulas are mostly visual. Voice should describe meaning, not read symbols verbatim, except short terms like “G maps A to U” if needed.
6. **Terminology rule:** first mention: English + Vietnamese explanation. Later: English term.

---

# Appendix B — Manim File Organization Suggestion

```text
scenes/
  00_cold_open.py
  01_traditional_deep_learning.py
  02_real_world_functions.py
  03_traditional_methods.py
  04_solution_operator.py
  05_discretization.py
  06_neural_operator_definition.py
  07_prereq_integrals_derivatives.py
  08_from_nn_to_no.py
  09_full_architecture.py
  10_architectures.py
  11_domains.py
  12_open_problems.py
  13_closing.py

assets/
  fields/
  meshes/
  icons/
  equations/
  audio/
```

---

# Appendix C — Cutdown Plan if Needed

- **45-minute version:** cut Scene 10.4, shorten Scene 10.6, shorten Section 11 to three domains: weather, seismology, CFD.
- **30-minute version:** keep Sections 0–9, use only FNO as architecture example, compress applications into montage.
- **15-minute version:** focus only on thesis, Darcy flow, discretization-agnostic learning, neural operator layer, FNO, open problems.
