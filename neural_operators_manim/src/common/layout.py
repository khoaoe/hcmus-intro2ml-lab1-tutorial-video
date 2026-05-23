import numpy as np
from manim import DOWN, Dot, Line, RoundedRectangle, Text, VGroup

from src.common.theme import CARD_BG, GRID, MUTED, STAMP_RED, TEXT


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


def make_card(title, subtitle=None, width=1.65, height=0.78, color="#38BDF8"):
    card = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=color,
        stroke_width=1.25,
        fill_color=CARD_BG,
        fill_opacity=0.78,
    )
    title_text = Text(title, font_size=19, color=TEXT)
    if subtitle:
        subtitle_text = Text(subtitle, font_size=12, color=MUTED)
        text = VGroup(title_text, subtitle_text).arrange(DOWN, buff=0.05)
    else:
        text = VGroup(title_text)
    text.move_to(card)
    return VGroup(card, text)


def make_chip(label, color="#38BDF8", width=None, height=0.38, font_size=16):
    chip_width = width or max(0.76, 0.18 * len(label) + 0.44)
    chip = RoundedRectangle(
        width=chip_width,
        height=height,
        corner_radius=0.07,
        stroke_color=color,
        stroke_width=1.1,
        fill_color=CARD_BG,
        fill_opacity=0.84,
    )
    text = Text(label, font_size=font_size, color=TEXT)
    text.move_to(chip)
    return VGroup(chip, text)


def make_warning_stamp(text="not plug-and-play"):
    frame = RoundedRectangle(
        width=2.86,
        height=0.64,
        corner_radius=0.07,
        stroke_color=STAMP_RED,
        stroke_width=2.6,
        fill_color="#3A1020",
        fill_opacity=0.2,
    )
    label = Text(text, font_size=23, color=STAMP_RED, weight="BOLD")
    label.move_to(frame)
    return VGroup(frame, label)


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
