import numpy as np
from manim import DOWN, Dot, Line, RoundedRectangle, Text, VGroup

from src.common.theme import CARD_BG, GRID, MUTED, TEXT


def labeled_card(content, label, width=3.5, height=2.2, accent="#38BDF8"):
    card = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=accent,
        stroke_width=1.4,
        fill_color=CARD_BG,
        fill_opacity=0.58,
    )
    label_mob = Text(label, font_size=24, color=TEXT)
    content.move_to(card.get_center())
    label_mob.next_to(card, DOWN, buff=0.16)
    return VGroup(card, content, label_mob)


def make_background_network(
    seed=11,
    n=68,
    x_range=(-14.0, 14.0),
    y_range=(-4.3, 4.3),
    neighbor_count=2,
    max_distance=2.4,
    dot_opacity=0.24,
    line_opacity=0.22,
):
    """Canonical subtle node-network background for production scenes."""
    rng = np.random.default_rng(seed)
    points = [
        np.array([rng.uniform(*x_range), rng.uniform(*y_range), 0])
        for _ in range(n)
    ]
    dots = VGroup(
        *[
            Dot(p, radius=rng.uniform(0.01, 0.025), color=MUTED, fill_opacity=dot_opacity)
            for p in points
        ]
    )
    lines = VGroup()
    for i, p in enumerate(points):
        neighbors = sorted(
            [
                (np.linalg.norm(p - q), q)
                for j, q in enumerate(points)
                if i != j
            ],
            key=lambda item: item[0],
        )
        for dist, q in neighbors[:neighbor_count]:
            if dist < max_distance:
                lines.add(
                    Line(
                        p,
                        q,
                        color=GRID,
                        stroke_width=0.55,
                        stroke_opacity=line_opacity,
                    )
                )
    return VGroup(lines, dots)
