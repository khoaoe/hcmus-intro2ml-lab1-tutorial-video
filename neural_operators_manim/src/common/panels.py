"""Reusable panel components for production scenes."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    MathTex,
    Mobject,
    Rectangle,
    RoundedRectangle,
    VGroup,
)

from src.common.safe_text import fit_mobject_to_box, safe_math, safe_text
from src.common.theme import CARD_BG, GRID, MUTED, OPERATOR, TEXT
from src.common.visual_safety import assert_inside, assert_no_group_overlap, assert_panel_integrity


class Chip(VGroup):
    def __init__(
        self,
        text: str,
        max_width: float = 2.0,
        height: float = 0.36,
        stroke_color=None,
        fill_color=None,
        text_color=None,
        font_size: int = 18,
        min_font_size: int = 12,
        corner_radius: float = 0.08,
        padding: float = 0.10,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=max_width,
            height=height,
            corner_radius=corner_radius,
            stroke_color=stroke_color or GRID,
            stroke_width=1.1,
            fill_color=fill_color or CARD_BG,
            fill_opacity=0.86,
        )
        self.label = safe_text(
            text,
            max_width=max_width - 2 * padding,
            max_height=height - 2 * padding,
            font_size=font_size,
            min_font_size=min_font_size,
            color=text_color or TEXT,
            name=f"chip:{text}",
        )
        self.label.move_to(self.box)
        assert_inside(self.label, self.box, padding=padding * 0.35, child_label="chip.label")
        self.add(self.box, self.label)


class PanelCard(VGroup):
    def __init__(
        self,
        title: str,
        body: Mobject | None = None,
        width: float = 4.0,
        height: float = 2.6,
        accent_color=None,
        title_color=None,
        fill_color=None,
        stroke_color=None,
        title_font_size: int = 24,
        padding: float = 0.18,
        title_height: float = 0.42,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.padding = padding
        self.box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=stroke_color or accent_color or GRID,
            stroke_width=1.35,
            fill_color=fill_color or CARD_BG,
            fill_opacity=0.68,
        )
        self.title_mob = safe_text(
            title,
            max_width=width - 2 * padding,
            max_height=title_height,
            font_size=title_font_size,
            min_font_size=16,
            color=title_color or TEXT,
            weight="BOLD",
            name=f"panel-title:{title}",
        )
        self.title_mob.move_to(
            [
                self.box.get_left()[0] + padding + self.title_mob.width / 2,
                self.box.get_top()[1] - padding - self.title_mob.height / 2,
                0,
            ]
        )
        body_width = width - 2 * padding
        body_height = height - title_height - 3 * padding
        if body_height <= 0:
            raise ValueError("PanelCard body area must be positive")
        self.body_area = Rectangle(
            width=body_width,
            height=body_height,
            stroke_opacity=0,
            fill_opacity=0,
        )
        self.body_area.move_to(
            [
                self.box.get_center()[0],
                self.box.get_bottom()[1] + padding + body_height / 2,
                0,
            ]
        )
        self.body: Mobject | None = None
        self.add(self.box, self.title_mob)
        if body is not None:
            self.set_body(body)
        assert_panel_integrity(self)

    def get_body_width(self) -> float:
        return float(self.body_area.width)

    def get_body_height(self) -> float:
        return float(self.body_area.height)

    def set_body(self, mob: Mobject):
        if self.body is not None:
            self.remove(self.body)
        self.body = fit_mobject_to_box(mob, self.get_body_width(), self.get_body_height())
        self.body.move_to(self.body_area)
        assert_inside(self.body, self.body_area, padding=0.0, child_label="panel.body")
        assert_inside(self.body, self.box, padding=0.04, child_label="panel.body")
        self.add(self.body)
        return self


class PanelGrid(VGroup):
    def __init__(
        self,
        panels: list[Mobject],
        rows: int,
        cols: int,
        width: float = 13.8,
        height: float = 6.8,
        buff: float = 0.35,
        **kwargs,
    ):
        if rows * cols < len(panels):
            raise ValueError(f"PanelGrid capacity {rows * cols} smaller than {len(panels)} panels")
        super().__init__(*panels, **kwargs)
        self.rows = rows
        self.cols = cols
        self.arrange_in_grid(rows=rows, cols=cols, buff=buff)
        fit_mobject_to_box(self, width, height)
        assert_no_group_overlap(list(self.submobjects), min_gap=0.01)


class FocusStage(VGroup):
    def __init__(
        self,
        width: float = 14.4,
        height: float = 7.6,
        title: str | None = None,
        subtitle: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.stage_area = Rectangle(width=width, height=height, stroke_opacity=0, fill_opacity=0)
        self.add(self.stage_area)
        current_top = self.stage_area.get_top()[1]
        if title:
            self.title_mob = safe_text(title, max_width=width, max_height=0.62, font_size=34, color=TEXT, weight="BOLD")
            self.title_mob.move_to([0, current_top - 0.34, 0])
            self.add(self.title_mob)
            current_top = self.title_mob.get_bottom()[1]
        else:
            self.title_mob = None
        if subtitle:
            self.subtitle_mob = safe_text(subtitle, max_width=width, max_height=0.42, font_size=22, color=MUTED)
            self.subtitle_mob.next_to(self.title_mob or self.stage_area, DOWN, buff=0.08)
            self.add(self.subtitle_mob)
        else:
            self.subtitle_mob = None


def make_section_label(
    text: str,
    max_width: float = 3.2,
    height: float = 0.38,
    color=None,
    text_color=None,
) -> Chip:
    label = Chip(
        text,
        max_width=max_width,
        height=height,
        stroke_color=color or OPERATOR,
        text_color=text_color or TEXT,
        font_size=17,
    )
    label.to_corner(UP + LEFT, buff=0.36)
    return label


def make_formula_badge(
    tex: str,
    max_width: float = 3.4,
    height: float = 0.62,
    stroke_color=None,
    fill_color=None,
    text_color=None,
    font_size: int = 28,
) -> VGroup:
    formula = safe_math(
        tex,
        max_width=max_width - 0.28,
        max_height=height - 0.16,
        font_size=font_size,
        min_font_size=16,
        color=text_color or TEXT,
        name=f"formula:{tex}",
    )
    box = RoundedRectangle(
        width=max_width,
        height=height,
        corner_radius=0.08,
        stroke_color=stroke_color or OPERATOR,
        stroke_width=1.2,
        fill_color=fill_color or CARD_BG,
        fill_opacity=0.8,
    )
    formula.move_to(box)
    return VGroup(box, formula).move_to(ORIGIN)

