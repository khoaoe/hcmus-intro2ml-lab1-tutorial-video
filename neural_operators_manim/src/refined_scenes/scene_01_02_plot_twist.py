
from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


def scalar_field(x, y):
    return (
        0.5
        + 0.3 * np.sin(1.2 * x) * np.cos(0.9 * y)
        + 0.2 * np.cos(2.1 * x + 0.5 * y)
        + 0.15 * np.sin(0.7 * x - 1.3 * y)
    )


def field_color(val):
    colors = [
        np.array([0.04, 0.06, 0.15]),  # Deep Navy (hòa vào background)
        np.array([0.12, 0.10, 0.35]),  # Dark Slate Purple
        np.array([0.35, 0.18, 0.45]),  # Muted Magenta
        np.array([0.75, 0.40, 0.15]),  # Warm Amber
        np.array([0.95, 0.65, 0.25]),  # Soft Gold
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


def make_continuous_field(x_range, y_range, resolution, center, width, height):
    field = VGroup()
    sq_w = width / resolution
    sq_h = height / resolution
    x_start, x_end = x_range
    y_start, y_end = y_range
    for i in range(resolution):
        for j in range(resolution):
            x_val = x_start + (x_end - x_start) * j / resolution
            y_val = y_start + (y_end - y_start) * i / resolution
            val = scalar_field(x_val, y_val)
            sq = Square(side_length=min(sq_w, sq_h) + 0.01, stroke_width=0)
            sq.set_fill(field_color(val), opacity=0.92)
            sq.move_to(center + RIGHT * (j * sq_w - width/2 + sq_w/2) + UP * (height/2 - i * sq_h - sq_h/2))
            field.add(sq)
    return field


class Scene0102_PlotTwistFunctionData(TimedScene):
    SCRIPT_ID = "1.2"
    SCRIPT_TITLE = "Plot twist — Đầu dò và Trường liên tục"
    SCRIPT_START = 45.0
    SCRIPT_END = 105.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):

        rn_frame = RoundedRectangle(
            width=10, height=5.5, corner_radius=0.2,
            stroke_color=INPUT, stroke_width=2, fill_opacity=0
        )
        rn_label = MathTex(r"\mathbb{R}^n", font_size=52, color=INPUT).move_to(rn_frame)
        rn_group = VGroup(rn_frame, rn_label)
        self.add(rn_group)

        shards = VGroup()
        np.random.seed(7)
        for _ in range(18):
            shard = Triangle(fill_color=INPUT, fill_opacity=0.3, stroke_color=INPUT, stroke_width=1)
            shard.scale(np.random.uniform(0.3, 0.7))
            shard.move_to(np.array([np.random.uniform(-4, 4), np.random.uniform(-2, 2), 0]))
            shard.rotate(np.random.uniform(0, TAU))
            shards.add(shard)

        self.play_timed("shatter_rn", 0, 2,
                        FadeOut(rn_label),
                        Transform(rn_frame, shards))

        field_res = 32  # 32x32 grid for the continuous field (smooth enough, fast to render)
        field_center = ORIGIN + UP * 0.3
        field_width = 8.0
        field_height = 4.5
        continuous_field = make_continuous_field(
            x_range=(-3, 3), y_range=(-2, 2),
            resolution=field_res, center=field_center,
            width=field_width, height=field_height
        )

        field_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=field_width, y_length=field_height,
            tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.0, "include_numbers": False},
        ).move_to(field_center)

        x_label = MathTex("x", font_size=24, color=MUTED).next_to(field_axes.x_axis, RIGHT, buff=0.15)
        y_label = MathTex("y", font_size=24, color=MUTED).next_to(field_axes.y_axis, UP, buff=0.15)

        field_title = MathTex(r"u(x, y)", font_size=36, color=TEXT).to_edge(UP, buff=0.4)
        subtitle = Text("Trường liên tục (Continuous Field)", font_size=20, color=MUTED)
        subtitle.next_to(field_title, DOWN, buff=0.15)

        self.play_timed("field_appear", 2, 5,
                        FadeOut(rn_frame),
                        FadeIn(continuous_field),
                        FadeIn(field_axes), FadeIn(x_label), FadeIn(y_label),
                        FadeIn(field_title), FadeIn(subtitle))

        
        probe_ring = Circle(radius=0.15, color=YELLOW, stroke_width=2.5)
        probe_cross_h = Line(LEFT*0.25, RIGHT*0.25, color=YELLOW, stroke_width=1.5)
        probe_cross_v = Line(UP*0.25, DOWN*0.25, color=YELLOW, stroke_width=1.5)
        probe = VGroup(probe_ring, probe_cross_h, probe_cross_v)
        probe.move_to(field_axes.c2p(-2, 1))

        probe_label = Text("Sensor Probe", font_size=18, color=YELLOW, weight=BOLD)
        probe_label.next_to(probe, DR, buff=0.15)

        probe_vline = DashedLine(
            probe.get_center(), field_axes.c2p(probe.get_center()[0], -2),
            color=YELLOW, stroke_width=1.5, dash_length=0.1, stroke_opacity=0.6
        )

        px, py = -2, 1
        val = scalar_field(px, py)
        temp = 15 + val * 25 
        
        value_text = MathTex(
            f"T({px:.1f}, {py:.1f}) = {temp:.1f}^\\circ C",
            font_size=24, color=YELLOW
        )
        hud_bg = SurroundingRectangle(
            value_text, color=YELLOW, fill_color=BLACK, 
            fill_opacity=0.85, buff=0.12, corner_radius=0.15, stroke_width=1.5
        )
        readout_group = VGroup(hud_bg, value_text).next_to(probe, UP, buff=0.25)

        self.play_timed("probe_appear", 5, 7,
                        FadeIn(probe), FadeIn(probe_label))
        self.play_timed("probe_line", 7, 8,
                        Create(probe_vline), FadeIn(readout_group))

        probe_path = [(-2, 1), (0, 0.5), (1.5, -0.8), (-0.5, -1.2), (2, 1.5)]

        for i in range(1, len(probe_path)):
            px_new, py_new = probe_path[i]
            val_new = scalar_field(px_new, py_new)
            temp_new = 15 + val_new * 25

            new_pos = field_axes.c2p(px_new, py_new)
            new_vline = DashedLine(
                new_pos, field_axes.c2p(px_new, -2),
                color=YELLOW, stroke_width=1.5, dash_length=0.1, stroke_opacity=0.6
            )
            
            new_text = MathTex(
                f"T({px_new:.1f}, {py_new:.1f}) = {temp_new:.1f}^\\circ C",
                font_size=24, color=YELLOW
            )
            new_hud_bg = SurroundingRectangle(
                new_text, color=YELLOW, fill_color=BLACK, 
                fill_opacity=0.85, buff=0.12, corner_radius=0.15, stroke_width=1.5
            )
            new_readout = VGroup(new_hud_bg, new_text).next_to(new_pos, UP, buff=0.25)

            t_start = 8 + (i - 1) * 2.5
            t_end = t_start + 2.0

            self.play_timed(f"probe_move_{i}", t_start, t_end,
                            probe.animate.move_to(new_pos),
                            Transform(probe_vline, new_vline),
                            Transform(readout_group, new_readout),
                            probe_label.animate.next_to(new_pos, DR, buff=0.15))

        self.wait_timed("hold_probe", 18, 20)


        self.play_timed("clear_beat1", 20, 21,
                        FadeOut(probe), FadeOut(probe_vline), FadeOut(readout_group),
                        FadeOut(probe_label), FadeOut(field_title), FadeOut(subtitle),
                        FadeOut(field_axes), FadeOut(x_label), FadeOut(y_label),
                        FadeOut(continuous_field))

        divider = Line(UP * 4, DOWN * 4, color=MUTED, stroke_width=1.5)

        left_title = Text("Camera / CNN", font_size=26, color=INPUT, weight=BOLD)
        left_title.move_to(LEFT * 4 + UP * 3.8)

        left_field = make_continuous_field(
            x_range=(-3, 3), y_range=(-2, 2),
            resolution=24, center=LEFT * 4 + DOWN * 0.2,
            width=6.0, height=3.5
        )

        grid_lines = VGroup()
        grid_n = 16
        gw, gh = 6.0, 3.5
        gcx, gcy = -4.0, -0.2
        for i in range(grid_n + 1):
            x = gcx - gw/2 + i * gw / grid_n
            grid_lines.add(Line(
                np.array([x, gcy - gh/2, 0]), np.array([x, gcy + gh/2, 0]),
                color=WARNING, stroke_width=0.8, stroke_opacity=0.7
            ))
        for j in range(grid_n + 1):
            y = gcy - gh/2 + j * gh / grid_n
            grid_lines.add(Line(
                np.array([gcx - gw/2, y, 0]), np.array([gcx + gw/2, y, 0]),
                color=WARNING, stroke_width=0.8, stroke_opacity=0.7
            ))

        grid_label_64 = Text("64 × 64 grid", font_size=16, color=WARNING)
        grid_label_64.next_to(left_field, DOWN, buff=0.2)

        right_title = Text("Neural Operator", font_size=26, color=NVIDIA_GREEN, weight=BOLD)
        right_title.move_to(RIGHT * 4 + UP * 3.8)

        right_field = make_continuous_field(
            x_range=(-3, 3), y_range=(-2, 2),
            resolution=24, center=RIGHT * 4 + DOWN * 0.2,
            width=6.0, height=3.5
        )

        func_label = MathTex(r"u(x)", font_size=32, color=NVIDIA_GREEN)
        func_label.next_to(right_field, DOWN, buff=0.2)

        np.random.seed(42)
        probes_right = VGroup()
        for _ in range(25):
            px = np.random.uniform(-3, 3)
            py = np.random.uniform(-2, 2)
            screen_x = 4 + px * (6.0 / 6.0)
            screen_y = -0.2 + py * (3.5 / 4.0)
            
            p = Circle(
                radius=0.06, color=NVIDIA_GREEN, stroke_width=2.0, fill_opacity=0
            ).move_to(np.array([screen_x, screen_y, 0]))
            probes_right.add(p)

        query_label = Text("Query Anywhere", font_size=24, color=NVIDIA_GREEN, weight=BOLD)
        query_label.next_to(right_field, UP, buff=0.15)

        self.play_timed("split_divider", 21, 22,
                        FadeIn(divider), FadeIn(left_title), FadeIn(right_title))

        self.play_timed("left_field", 22, 24,
                        FadeIn(left_field))

        self.play_timed("grid_drop", 24, 26,
                        FadeIn(grid_lines, shift=DOWN * 0.5),
                        FadeIn(grid_label_64))

        self.play_timed("right_field", 26, 28,
                        FadeIn(right_field), FadeIn(func_label))

        self.play_timed("probes_fly", 28, 31,
                        LaggedStart(*[FadeIn(p, scale=0.3) for p in probes_right], lag_ratio=0.05),
                        FadeIn(query_label))

        self.wait_timed("hold_split", 31, 40)


        dial_center = ORIGIN + DOWN * 3.6
        dial_bg = Circle(radius=0.55, color=MUTED, stroke_width=2, fill_color=CARD_BG, fill_opacity=0.9)
        dial_bg.move_to(dial_center)
        dial_label = Text("Resolution", font_size=14, color=TEXT).move_to(dial_center + DOWN * 0.15)
        dial_needle = Line(dial_center, dial_center + UP * 0.4, color=WARNING, stroke_width=3)
        dial_ticks = VGroup()
        for angle in np.linspace(PI * 0.75, PI * 0.25, 5):
            tick_start = dial_center + 0.45 * np.array([np.cos(angle), np.sin(angle), 0])
            tick_end = dial_center + 0.55 * np.array([np.cos(angle), np.sin(angle), 0])
            dial_ticks.add(Line(tick_start, tick_end, color=MUTED, stroke_width=1.5))
        min_label = Text("Min", font_size=10, color=MUTED).next_to(dial_bg, LEFT, buff=0.1).shift(UP * 0.1)
        max_label = Text("Max", font_size=10, color=WARNING).next_to(dial_bg, RIGHT, buff=0.1).shift(UP * 0.1)
        dial_group = VGroup(dial_bg, dial_ticks, dial_needle, dial_label, min_label, max_label)

        self.play_timed("dial_appear", 40, 42,
                        FadeOut(grid_label_64), FadeOut(func_label), FadeOut(query_label),
                        FadeIn(dial_group))

        dense_grid = VGroup()
        dense_n = 32
        for i in range(dense_n + 1):
            x = gcx - gw/2 + i * gw / dense_n
            dense_grid.add(Line(
                np.array([x, gcy - gh/2, 0]), np.array([x, gcy + gh/2, 0]),
                color=WARNING, stroke_width=0.6, stroke_opacity=0.8
            ))
        for j in range(dense_n + 1):
            y = gcy - gh/2 + j * gh / dense_n
            dense_grid.add(Line(
                np.array([gcx - gw/2, y, 0]), np.array([gcx + gw/2, y, 0]),
                color=WARNING, stroke_width=0.6, stroke_opacity=0.8
            ))

        heavy_label = Text("Heavy & Discrete", font_size=18, color=WARNING)
        heavy_label.next_to(left_field, DOWN, buff=0.2)

        np.random.seed(99)
        more_probes = VGroup()
        for _ in range(40):
            px = np.random.uniform(-3, 3)
            py = np.random.uniform(-2, 2)
            screen_x = 4 + px * (6.0 / 6.0)
            screen_y = -0.2 + py * (3.5 / 4.0)
            
            p = Circle(
                radius=0.04, color=NVIDIA_GREEN, stroke_width=1.5, fill_opacity=0
            ).move_to(np.array([screen_x, screen_y, 0]))
            more_probes.add(p)

        invariance_label = Text("Discretization Invariance", font_size=22, color=NVIDIA_GREEN, weight=BOLD)
        invariance_label.next_to(right_field, DOWN, buff=0.2)

        needle_target = dial_needle.copy().rotate(-PI * 0.5, about_point=dial_center)

        self.play_timed("dial_turn", 42, 46,
                        Transform(dial_needle, needle_target),
                        Transform(grid_lines, dense_grid),
                        FadeIn(heavy_label),
                        LaggedStart(*[FadeIn(p, scale=0.3) for p in more_probes], lag_ratio=0.03),
                        FadeIn(invariance_label))

        self.wait_timed("hold_resolution", 46, 58)

        self.play_timed("cut_to_black", 58, 60,
                        *[FadeOut(m, run_time=0.5) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
