"""
Scene 1.3 — Grid Mismatch & Ràng buộc vật lý
Source: original_outline.tex, Section 1, Scene 1.3
Global time: 1:45 – 2:30
Duration: 45s

Beat 1 [0–15s]: Two grids side-by-side, same continuous field sampled differently
Beat 2 [15–30s]: "The Stretched Kernel" — CNN kernel shrinks on finer grid → noise
Beat 3 [30–45s]: "The Derivative Trap" — Finite difference instability → physics violation
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


# ═══════════════════════════════════════════════════════════════
# Helper: Dark-mode scalar field (same palette as Scene 1.2)
# ═══════════════════════════════════════════════════════════════

def temp_func(x, y):
    """Smooth scalar field simulating a temperature-like distribution."""
    return np.clip(
        np.exp(-((x - 1)**2 + (y - 0.5)**2) * 2)
        + 0.5 * np.exp(-((x + 1.5)**2 + (y + 1)**2) * 3),
        0, 1
    )


def field_color(val):
    """Dark-mode colormap: Deep Navy → Slate Purple → Soft Amber."""
    colors = [
        np.array([0.04, 0.06, 0.15]),
        np.array([0.12, 0.10, 0.35]),
        np.array([0.35, 0.18, 0.45]),
        np.array([0.75, 0.40, 0.15]),
        np.array([0.95, 0.65, 0.25]),
    ]
    val = np.clip(val, 0, 1)
    t = val * (len(colors) - 1)
    idx = int(t)
    frac = t - idx
    if idx >= len(colors) - 1:
        rgb = colors[-1]
    else:
        rgb = colors[idx] * (1 - frac) + colors[idx + 1] * frac
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))


def make_pixel_field(res, width, height, center):
    """Create a pixel-based raster field using the dark-mode colormap."""
    grid = VGroup()
    dx, dy = width / res, height / res
    for i in range(res):
        for j in range(res):
            x_val = -1.5 + 3.0 * j / res
            y_val = -1.0 + 2.0 * i / res
            val = temp_func(x_val * 1.5, y_val * 1.5)
            sq = Square(
                side_length=min(dx, dy) + 0.01,
                stroke_width=0,
                fill_color=field_color(val),
                fill_opacity=0.92,
            )
            sq.move_to(
                center
                + RIGHT * (-width / 2 + (j + 0.5) * dx)
                + UP * (-height / 2 + (i + 0.5) * dy)
            )
            grid.add(sq)
    return grid


class Scene0103_GridMismatch(TimedScene):
    SCRIPT_ID = "1.3"
    SCRIPT_TITLE = "Grid Mismatch & Ràng buộc vật lý"
    SCRIPT_START = 105.0
    SCRIPT_END = 150.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: [1:45–2:00] (local 0–15s)
        # Two grids side-by-side, same continuous function
        # ═══════════════════════════════════════════════════════════════

        # Title
        title = Text(
            "Cùng 1 hàm nhiệt độ — hai lưới khác nhau",
            font_size=24, color=MUTED
        ).to_edge(UP, buff=0.45)

        # Coarse grid (16x16 visual → represents 64x64)
        coarse_center = LEFT * 4 + DOWN * 0.3
        coarse_field = make_pixel_field(16, 5.5, 3.5, coarse_center)
        coarse_label = Text("64 × 64 (thô)", font_size=20, color=INPUT)
        coarse_label.next_to(coarse_field, DOWN, buff=0.2)

        # Fine grid (32x32 visual → represents 128x128)
        fine_center = RIGHT * 4 + DOWN * 0.3
        fine_field = make_pixel_field(32, 5.5, 3.5, fine_center)
        fine_label = Text("128 × 128 (mịn)", font_size=20, color=PURPLE)
        fine_label.next_to(fine_field, DOWN, buff=0.2)

        # Divider
        divider = Line(UP * 3.8, DOWN * 3.8, color=MUTED, stroke_width=1.2)

        self.play_timed("title_in", 0, 1, FadeIn(title))
        self.play_timed("grids_in", 1, 4,
                        FadeIn(coarse_field), FadeIn(coarse_label),
                        FadeIn(fine_field), FadeIn(fine_label),
                        FadeIn(divider))

        # VO: "Nếu ta cố ép một mô hình DL truyền thống..."
        self.wait_timed("hold_grids", 4, 15)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: [2:00–2:15] (local 15–30s)
        # "The Stretched Kernel" — CNN kernel shrinks on finer grid
        # ═══════════════════════════════════════════════════════════════

        # Clear title
        self.play_timed("clear_title", 15, 15.5, FadeOut(title))

        # --- Kernel on coarse grid (covers a physically meaningful area) ---
        kernel_size_coarse = 1.4  # visually large
        kernel_coarse = Square(
            side_length=kernel_size_coarse,
            color=YELLOW, stroke_width=3.5, fill_opacity=0
        )
        kernel_coarse.move_to(coarse_center + UP * 0.3 + RIGHT * 0.4)

        kernel_label = Text("CNN Kernel 3×3", font_size=16, color=YELLOW, weight=BOLD)
        kernel_label.next_to(kernel_coarse, UP, buff=0.1)

        # HUD pill for kernel info
        kernel_info_text = Text(
            "Receptive Field = vùng nhìn thấy",
            font_size=14, color=YELLOW
        )
        kernel_info_bg = SurroundingRectangle(
            kernel_info_text, color=YELLOW, fill_color=BLACK,
            fill_opacity=0.85, buff=0.1, corner_radius=0.12, stroke_width=1.2
        )
        kernel_info = VGroup(kernel_info_bg, kernel_info_text)
        kernel_info.next_to(kernel_coarse, DOWN, buff=0.15)

        self.play_timed("kernel_appear", 15.5, 17.5,
                        Create(kernel_coarse), FadeIn(kernel_label),
                        FadeIn(kernel_info))

        # VO: "Model học được một pattern vật lý..."
        self.wait_timed("hold_kernel_coarse", 17.5, 20)

        # --- Kernel on fine grid: SAME 3x3 pixel kernel, but physically TINY ---
        kernel_size_fine = 0.65  # visually much smaller
        kernel_fine = Square(
            side_length=kernel_size_fine,
            color=YELLOW, stroke_width=3.5, fill_opacity=0
        )
        kernel_fine.move_to(fine_center + UP * 0.3 + RIGHT * 0.4)

        # Animate the kernel "teleporting" to the fine grid and shrinking
        kernel_fine_label = Text("CNN Kernel 3×3", font_size=12, color=YELLOW, weight=BOLD)
        kernel_fine_label.next_to(kernel_fine, UP, buff=0.08)

        # "Semantic Shift" HUD
        semantic_text = Text("Semantic Shift!", font_size=28, color=WARNING, weight=BOLD)
        semantic_bg = SurroundingRectangle(
            semantic_text, color=WARNING, fill_color=BLACK,
            fill_opacity=0.85, buff=0.12, corner_radius=0.15, stroke_width=1.5
        )
        semantic_hud = VGroup(semantic_bg, semantic_text).to_edge(UP, buff=0.4)

        self.play_timed("kernel_shrink", 20, 22.5,
                        TransformFromCopy(kernel_coarse, kernel_fine),
                        TransformFromCopy(kernel_label, kernel_fine_label),
                        FadeIn(semantic_hud, shift=DOWN * 0.2))

        # Noise overlay on fine grid (glitch effect)
        np.random.seed(42)
        noise_overlay = VGroup()
        for sq in fine_field:
            if np.random.rand() > 0.65:
                n = Square(
                    side_length=sq.width,
                    stroke_width=0,
                    fill_color=WARNING,
                    fill_opacity=np.random.uniform(0.15, 0.45)
                )
                n.move_to(sq.get_center())
                noise_overlay.add(n)

        self.play_timed("noise_glitch", 22.5, 24,
                        LaggedStart(*[FadeIn(n, scale=0.5) for n in noise_overlay], lag_ratio=0.005))

        # VO: "...kernel chỉ nhìn thấy noise. Grid Mismatch."
        self.wait_timed("hold_mismatch", 24, 30)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: [2:15–2:30] (local 30–45s)
        # "The Derivative Trap" — Finite difference instability
        # ═══════════════════════════════════════════════════════════════

        # Clear Beat 2
        beat2_objects = [
            coarse_field, coarse_label, fine_field, fine_label, divider,
            kernel_coarse, kernel_label, kernel_info,
            kernel_fine, kernel_fine_label,
            semantic_hud, noise_overlay,
        ]
        self.play_timed("clear_beat2", 30, 31,
                        *[FadeOut(m) for m in beat2_objects])

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-1, 3.5, 1],
            x_length=10, y_length=5,
            tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.0, "include_numbers": False}
        ).shift(DOWN * 0.3)

        x_ax_label = MathTex("x", font_size=22, color=MUTED).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_ax_label = MathTex("u(x)", font_size=22, color=NVIDIA_GREEN).next_to(axes.y_axis, UP, buff=0.1)

        # Physics ground-truth curve
        def physics_func(x):
            return 0.12 * x**3 - 0.5 * x**2 + 2.5

        curve = axes.plot(physics_func, x_range=[-2.5, 2.8], color=NVIDIA_GREEN, stroke_width=3)
        curve_label = Text("Ground Truth (Vật lý)", font_size=16, color=NVIDIA_GREEN, weight=BOLD)
        curve_label.next_to(curve, UR, buff=0.15)

        self.play_timed("axes_curve", 31, 33,
                        Create(axes), FadeIn(x_ax_label), FadeIn(y_ax_label),
                        Create(curve), FadeIn(curve_label))

        # 3 discrete sample points
        x_pts = [-1.5, 0.5, 2.0]
        dots = VGroup(*[
            Dot(axes.c2p(x, physics_func(x)), color=YELLOW, radius=0.1)
            for x in x_pts
        ])

        dots_label = Text("Discrete output", font_size=14, color=YELLOW)
        dots_label.next_to(dots, DOWN, buff=0.3)

        self.play_timed("dots_in", 33, 34.5,
                        LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.15),
                        FadeIn(dots_label))

        # Secant line (finite difference) between first two points
        p0 = axes.c2p(x_pts[0], physics_func(x_pts[0]))
        p1 = axes.c2p(x_pts[1], physics_func(x_pts[1]))
        secant = Line(p0, p1, color=INPUT, stroke_width=2.5)
        # Extend the line beyond the points for visibility
        direction = (p1 - p0)
        direction = direction / np.linalg.norm(direction)
        secant_extended = Line(
            p0 - direction * 1.2,
            p1 + direction * 1.2,
            color=INPUT, stroke_width=2.5
        )

        deriv_label = MathTex(
            r"\frac{\Delta u}{\Delta x}", font_size=30, color=INPUT
        )
        deriv_bg = SurroundingRectangle(
            deriv_label, color=INPUT, fill_color=BLACK,
            fill_opacity=0.85, buff=0.1, corner_radius=0.12, stroke_width=1.2
        )
        deriv_hud = VGroup(deriv_bg, deriv_label)
        deriv_hud.next_to(secant_extended, UP, buff=0.2)

        self.play_timed("secant_in", 34.5, 36,
                        Create(secant_extended), FadeIn(deriv_hud))

        # VO: "Đầu ra chỉ là vector rời rạc..."
        self.wait_timed("hold_secant", 36, 37.5)

        # Plot twist: shift middle point up (model error) → secant rotates wildly
        shifted_y = physics_func(x_pts[1]) + 0.9
        dot_shifted = Dot(axes.c2p(x_pts[1], shifted_y), color=WARNING, radius=0.1)

        p1_shifted = axes.c2p(x_pts[1], shifted_y)
        new_direction = (p1_shifted - p0)
        new_direction = new_direction / np.linalg.norm(new_direction)
        secant_shifted = Line(
            p0 - new_direction * 1.2,
            p1_shifted + new_direction * 1.5,
            color=WARNING, stroke_width=3
        )

        error_arrow = Arrow(
            axes.c2p(x_pts[1], physics_func(x_pts[1])),
            axes.c2p(x_pts[1], shifted_y),
            color=WARNING, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.3
        )
        error_label = MathTex(r"\epsilon", font_size=24, color=WARNING)
        error_label.next_to(error_arrow, RIGHT, buff=0.1)

        self.play_timed("shift_dot", 37.5, 39.5,
                        Transform(dots[1], dot_shifted),
                        Transform(secant_extended, secant_shifted),
                        GrowArrow(error_arrow), FadeIn(error_label))

        # Navier-Stokes equation → crossed out
        ns_eq = MathTex(
            r"\frac{\partial \mathbf{u}}{\partial t}",
            r"+ (\mathbf{u} \cdot \nabla)\mathbf{u}",
            r"= -\frac{1}{\rho}\nabla p",
            r"+ \nu \nabla^2 \mathbf{u}",
            font_size=28, color=TEXT
        ).to_edge(DOWN, buff=0.6)

        ns_bg = SurroundingRectangle(
            ns_eq, color=MUTED, fill_color=BLACK,
            fill_opacity=0.85, buff=0.15, corner_radius=0.15, stroke_width=1
        )
        ns_group = VGroup(ns_bg, ns_eq)

        cross_line = Line(
            ns_eq.get_left() + LEFT * 0.1,
            ns_eq.get_right() + RIGHT * 0.1,
            color=WARNING, stroke_width=4
        )

        warning_text = Text("Physics Violated!", font_size=22, color=WARNING, weight=BOLD)
        warning_text.next_to(ns_group, UP, buff=0.15)

        self.play_timed("ns_eq", 39.5, 41, FadeIn(ns_group))
        self.play_timed("cross_out", 41, 42,
                        Create(cross_line), FadeIn(warning_text, shift=DOWN * 0.1))

        # VO: "Các định luật bảo toàn bị phá vỡ."
        self.wait_timed("hold_end", 42, 44)

        # Hard cut to black
        self.play_timed("cut", 44, 45,
                        *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
