"""Text helpers that fail before labels overflow."""

from __future__ import annotations

import textwrap
from typing import Iterable

from manim import MathTex, Mobject, Paragraph, Text

from src.common.theme import TEXT


EPSILON = 1e-6


def _fits(mob: Mobject, max_width: float, max_height: float | None = None) -> bool:
    if mob.width > max_width + EPSILON:
        return False
    if max_height is not None and mob.height > max_height + EPSILON:
        return False
    return True


def _attach_safe_metadata(
    mob: Mobject,
    *,
    name: str | None,
    max_width: float,
    max_height: float | None,
) -> Mobject:
    mob.safe_name = name
    mob.safe_max_width = max_width
    mob.safe_max_height = max_height
    return mob


def ensure_mobject_fits(
    mob: Mobject,
    max_width: float,
    max_height: float | None = None,
    label: str = "mobject",
) -> None:
    """Raise if a mobject exceeds given dimensions."""
    if mob.width > max_width + EPSILON:
        raise ValueError(
            f"{label} width {mob.width:.3f} exceeds max_width {max_width:.3f}"
        )
    if max_height is not None and mob.height > max_height + EPSILON:
        raise ValueError(
            f"{label} height {mob.height:.3f} exceeds max_height {max_height:.3f}"
        )


def fit_mobject_to_box(
    mob: Mobject,
    max_width: float,
    max_height: float | None = None,
    preserve_readability: bool = True,
) -> Mobject:
    """Scale a mobject down to fit a box. Never upscale."""
    del preserve_readability
    scale = 1.0
    if mob.width > 0:
        scale = min(scale, max_width / mob.width)
    if max_height is not None and mob.height > 0:
        scale = min(scale, max_height / mob.height)
    if scale < 1.0:
        mob.scale(scale)
    return mob


def safe_text(
    text: str,
    max_width: float,
    max_height: float | None = None,
    font_size: int = 28,
    min_font_size: int = 14,
    color=None,
    weight=None,
    font=None,
    name: str | None = None,
) -> Text:
    """Create Text that fits or raises."""
    kwargs = {
        "font_size": font_size,
        "color": color or TEXT,
    }
    if weight is not None:
        kwargs["weight"] = weight
    if font is not None:
        kwargs["font"] = font

    for size in range(font_size, min_font_size - 1, -1):
        kwargs["font_size"] = size
        mob = Text(text, **kwargs)
        if _fits(mob, max_width, max_height):
            return _attach_safe_metadata(
                mob,
                name=name,
                max_width=max_width,
                max_height=max_height,
            )

    raise ValueError(
        f"{name or 'text'} does not fit {max_width:.3f}x"
        f"{max_height if max_height is not None else '∞'} at min font {min_font_size}"
    )


def _wrap_lines(lines: list[str], max_width: float, font_size: int, chars: int | None = None) -> list[str]:
    chars = chars or max(8, int(max_width * 9.0 * 24 / max(font_size, 1)))
    wrapped: list[str] = []
    for line in lines:
        if not line:
            wrapped.append("")
            continue
        wrapped.extend(
            textwrap.wrap(
                line,
                width=chars,
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [line]
        )
    return wrapped


def safe_paragraph(
    lines: list[str] | str,
    max_width: float,
    max_height: float | None = None,
    font_size: int = 24,
    min_font_size: int = 14,
    color=None,
    alignment: str = "left",
    line_spacing: float = -1,
    name: str | None = None,
) -> Paragraph:
    """Create a wrapped Paragraph that fits or raises."""
    raw_lines = [lines] if isinstance(lines, str) else list(lines)
    for size in range(font_size, min_font_size - 1, -1):
        initial_chars = max(8, int(max_width * 9.0 * 24 / max(size, 1)))
        for chars in range(initial_chars, 7, -2):
            wrapped = _wrap_lines(raw_lines, max_width, size, chars=chars)
            mob = Paragraph(
                *wrapped,
                font_size=size,
                color=color or TEXT,
                alignment=alignment,
                line_spacing=line_spacing,
            )
            if _fits(mob, max_width, max_height):
                return _attach_safe_metadata(
                    mob,
                    name=name,
                    max_width=max_width,
                    max_height=max_height,
                )

    raise ValueError(
        f"{name or 'paragraph'} does not fit {max_width:.3f}x"
        f"{max_height if max_height is not None else '∞'} at min font {min_font_size}"
    )


def safe_math(
    tex: str,
    max_width: float,
    max_height: float | None = None,
    font_size: int = 32,
    min_font_size: int = 16,
    color=None,
    name: str | None = None,
) -> MathTex:
    """Create MathTex that remains readable and bounded."""
    for size in range(font_size, min_font_size - 1, -1):
        mob = MathTex(tex, font_size=size, color=color or TEXT)
        if _fits(mob, max_width, max_height):
            return _attach_safe_metadata(
                mob,
                name=name,
                max_width=max_width,
                max_height=max_height,
            )

    raise ValueError(
        f"{name or 'math'} does not fit {max_width:.3f}x"
        f"{max_height if max_height is not None else '∞'} at min font {min_font_size}"
    )


SafeText = safe_text
SafeMathTex = safe_math
