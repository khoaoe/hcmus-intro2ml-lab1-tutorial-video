"""
Scene 4.3 — Graph Neural Operator (GNO): Xử lý lưới bất quy tắc
Source: original_outline.tex, Section 4, Scene 4.3
Global time: 13:15 – 14:30
Duration: 75s
"""

from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()


class Scene0403_GNO(TimedScene):
    SCRIPT_ID = "4.3"
    SCRIPT_TITLE = "GNO — Xử lý lưới bất quy tắc"
    SCRIPT_START = 795.0
    SCRIPT_END = 870.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        # ── Beat 1: [13:15–13:50] Mesh → graph G=(V,E), Voronoi, w_ij ──
        title = Text("Graph Neural Operator", font_size=30,
                     color=PURPLE, weight=BOLD).to_edge(UP, buff=0.4)

        # Irregular point cloud
        np.random.seed(123)
        n_points = 25
        positions = [
            np.array([np.random.uniform(-5, 5), np.random.uniform(-2.5, 2.5), 0])
            for _ in range(n_points)
        ]
        nodes = VGroup(*[
            Dot(point=pos, radius=0.1, color=PURPLE) for pos in positions
        ])

        self.play_timed("title", 0, 2, FadeIn(title))
        self.play_timed("nodes", 2, 4, FadeIn(nodes, lag_ratio=0.03))

        # Build edges within radius r
        edges = VGroup()
        r = 2.5
        for i in range(n_points):
            for j in range(i + 1, n_points):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < r:
                    edge = Line(positions[i], positions[j],
                                color=GRID, stroke_width=0.8, stroke_opacity=0.5)
                    edges.add(edge)

        self.play_timed("edges", 4, 8, FadeIn(edges, lag_ratio=0.01))

        # Radius circle around center node
        center_idx = n_points // 2
        radius_circle = Circle(radius=r * 0.35, color=OPERATOR, stroke_width=2,
                               stroke_opacity=0.6).move_to(positions[center_idx])
        r_label = MathTex(r"r", font_size=22, color=OPERATOR).next_to(radius_circle, UR, buff=0.1)

        self.play_timed("radius", 8, 10, FadeIn(radius_circle), FadeIn(r_label))

        # Graph label
        graph_eq = MathTex(r"G = (V, E)", font_size=30, color=PURPLE).shift(DOWN * 3.5)
        voronoi_note = Text(
            "w_ij ∝ thể tích Voronoi → hội tụ tích phân",
            font_size=18, color=MUTED
        ).to_edge(DOWN, buff=0.3)

        key_diff = Text(
            "Hội tụ tích phân ≠ GNN thường",
            font_size=22, color=NVIDIA_GREEN, weight=BOLD
        ).shift(DOWN * 3.5 + RIGHT * 3)

        self.play_timed("graph_eq", 10, 12, FadeIn(graph_eq))
        self.play_timed("voronoi", 12, 14, FadeIn(voronoi_note))
        self.play_timed("key_diff", 14, 16, FadeIn(key_diff))
        self.wait_timed("hold_graph", 16, 35)

        # ── Beat 2: [13:50–14:30] Message passing animation ──
        self.play_timed("clear_beat1", 35, 35.5,
                        *[FadeOut(m) for m in [nodes, edges, radius_circle, r_label,
                                               graph_eq, voronoi_note, key_diff]])

        # Simplified message passing diagram
        mp_title = Text("Message Passing trong không gian hàm", font_size=24,
                        color=TEXT, weight=BOLD).to_edge(UP, buff=0.8)

        # Center node + neighbors
        center = Dot(ORIGIN, radius=0.2, color=PURPLE)
        center_label = Text("Node i", font_size=16, color=PURPLE).next_to(center, DOWN, buff=0.25)
        neighbors = VGroup()
        neighbor_positions = [
            UP * 2, UP * 1.5 + RIGHT * 2, RIGHT * 2.5,
            DOWN * 1.5 + RIGHT * 1.5, DOWN * 2, DOWN * 1 + LEFT * 2, LEFT * 2.5,
        ]
        for pos in neighbor_positions:
            dot = Dot(pos, radius=0.12, color=INPUT)
            neighbors.add(dot)

        # Edges to center
        msg_edges = VGroup(*[
            Arrow(n.get_center(), center.get_center(), color=GRID,
                  buff=0.15, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
            for n in neighbors
        ])

        # MLP kernel box on one edge
        mlp_box = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.05,
                                   stroke_color=OPERATOR, fill_color=CARD_BG, fill_opacity=0.8)
        mlp_label = MathTex(r"\kappa_\theta", font_size=20, color=OPERATOR).move_to(mlp_box)
        mlp_group = VGroup(mlp_box, mlp_label).move_to(neighbor_positions[2] / 2)

        self.play_timed("mp_title", 35.5, 37, FadeIn(mp_title))
        self.play_timed("center_neighbors", 37, 40,
                        FadeIn(center), FadeIn(center_label), FadeIn(neighbors))
        self.play_timed("msg_edges", 40, 44, FadeIn(msg_edges))
        self.play_timed("mlp_kernel", 44, 46, FadeIn(mlp_group))

        # Aggregation highlight
        agg_text = Text(
            "Tổng hợp có trọng số Voronoi → σ(·)",
            font_size=20, color=OUTPUT
        ).shift(DOWN * 3)
        self.play_timed("agg", 46, 49, FadeIn(agg_text))

        multi_hop = Text(
            "Nhiều lớp → thông tin nhảy xa → tương tác toàn cục",
            font_size=18, color=MUTED
        ).to_edge(DOWN, buff=0.3)
        self.play_timed("multi_hop", 49, 52, FadeIn(multi_hop))
        self.wait_timed("hold_end", 52, 74)

        self.play_timed("cut", 74, 75, *[FadeOut(m, run_time=0.3) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
