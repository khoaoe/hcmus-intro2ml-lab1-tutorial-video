"""Automated geometry checks for obvious visual failures."""

from __future__ import annotations

from manim import Mobject, config


def get_bounds(mob: Mobject) -> dict[str, float]:
    left = float(mob.get_left()[0])
    right = float(mob.get_right()[0])
    bottom = float(mob.get_bottom()[1])
    top = float(mob.get_top()[1])
    return {
        "left": left,
        "right": right,
        "bottom": bottom,
        "top": top,
        "width": right - left,
        "height": top - bottom,
    }


def _format_bounds(bounds: dict[str, float]) -> str:
    return (
        f"L={bounds['left']:.3f}, R={bounds['right']:.3f}, "
        f"B={bounds['bottom']:.3f}, T={bounds['top']:.3f}"
    )


def assert_in_frame(
    mob: Mobject,
    frame_width: float | None = None,
    frame_height: float | None = None,
    margin: float = 0.20,
    label: str = "mobject",
) -> None:
    frame_width = frame_width or float(config.frame_width)
    frame_height = frame_height or float(config.frame_height)
    safe_left = -frame_width / 2 + margin
    safe_right = frame_width / 2 - margin
    safe_bottom = -frame_height / 2 + margin
    safe_top = frame_height / 2 - margin
    bounds = get_bounds(mob)
    if (
        bounds["left"] < safe_left
        or bounds["right"] > safe_right
        or bounds["bottom"] < safe_bottom
        or bounds["top"] > safe_top
    ):
        raise AssertionError(
            f"{label} outside safe frame: {_format_bounds(bounds)}; "
            f"safe L={safe_left:.3f}, R={safe_right:.3f}, "
            f"B={safe_bottom:.3f}, T={safe_top:.3f}"
        )


def assert_inside(
    child: Mobject,
    parent: Mobject,
    padding: float = 0.05,
    child_label: str = "child",
    parent_label: str = "parent",
) -> None:
    child_bounds = get_bounds(child)
    parent_bounds = get_bounds(parent)
    if (
        child_bounds["left"] < parent_bounds["left"] + padding
        or child_bounds["right"] > parent_bounds["right"] - padding
        or child_bounds["bottom"] < parent_bounds["bottom"] + padding
        or child_bounds["top"] > parent_bounds["top"] - padding
    ):
        raise AssertionError(
            f"{child_label} not inside {parent_label}: "
            f"{_format_bounds(child_bounds)} vs {_format_bounds(parent_bounds)} "
            f"with padding {padding:.3f}"
        )


def _overlap_amount(a: dict[str, float], b: dict[str, float]) -> tuple[float, float]:
    x_overlap = min(a["right"], b["right"]) - max(a["left"], b["left"])
    y_overlap = min(a["top"], b["top"]) - max(a["bottom"], b["bottom"])
    return x_overlap, y_overlap


def assert_no_overlap(
    a: Mobject,
    b: Mobject,
    min_gap: float = 0.02,
    label_a: str = "a",
    label_b: str = "b",
) -> None:
    a_bounds = get_bounds(a)
    b_bounds = get_bounds(b)
    x_overlap, y_overlap = _overlap_amount(a_bounds, b_bounds)
    if x_overlap + min_gap > 0 and y_overlap + min_gap > 0:
        raise AssertionError(
            f"{label_a} overlaps {label_b}: "
            f"{_format_bounds(a_bounds)} vs {_format_bounds(b_bounds)}"
        )


def assert_no_group_overlap(
    mobs: list[Mobject],
    min_gap: float = 0.02,
    labels: list[str] | None = None,
    ignore_pairs: set[tuple[int, int]] | None = None,
) -> None:
    labels = labels or [f"mobject[{index}]" for index in range(len(mobs))]
    ignore_pairs = ignore_pairs or set()
    normalized_ignore = {tuple(sorted(pair)) for pair in ignore_pairs}
    for i in range(len(mobs)):
        for j in range(i + 1, len(mobs)):
            if (i, j) in normalized_ignore:
                continue
            assert_no_overlap(mobs[i], mobs[j], min_gap, labels[i], labels[j])


def assert_readable_size(
    mob: Mobject,
    min_width: float = 0.05,
    min_height: float = 0.05,
    label: str = "mobject",
) -> None:
    bounds = get_bounds(mob)
    if bounds["width"] < min_width or bounds["height"] < min_height:
        raise AssertionError(
            f"{label} too small: width={bounds['width']:.3f}, "
            f"height={bounds['height']:.3f}"
        )


def assert_panel_integrity(panel: Mobject, label: str = "panel") -> None:
    if hasattr(panel, "box") and hasattr(panel, "title_mob"):
        assert_inside(panel.title_mob, panel.box, padding=0.04, child_label=f"{label}.title")
    if hasattr(panel, "box") and getattr(panel, "body", None) is not None:
        assert_inside(panel.body, panel.box, padding=0.04, child_label=f"{label}.body")
    if hasattr(panel, "title_mob") and getattr(panel, "body", None) is not None:
        assert_no_overlap(panel.title_mob, panel.body, min_gap=0.01, label_a=f"{label}.title", label_b=f"{label}.body")


def visual_safety_report(
    named_mobjects: dict[str, Mobject],
    frame_check: bool = True,
    overlap_check: bool = False,
) -> str:
    lines = ["# Visual Safety Report", ""]
    failures: list[str] = []
    for name, mob in named_mobjects.items():
        bounds = get_bounds(mob)
        lines.append(f"- `{name}`: {_format_bounds(bounds)}")
        if frame_check:
            try:
                assert_in_frame(mob, label=name)
                lines.append(f"  - frame: PASS")
            except AssertionError as exc:
                failures.append(str(exc))
                lines.append(f"  - frame: FAIL — {exc}")
        try:
            assert_readable_size(mob, label=name)
            lines.append(f"  - readable-size: PASS")
        except AssertionError as exc:
            failures.append(str(exc))
            lines.append(f"  - readable-size: FAIL — {exc}")

    if overlap_check:
        names = list(named_mobjects)
        mobs = [named_mobjects[name] for name in names]
        try:
            assert_no_group_overlap(mobs, labels=names)
            lines.append("")
            lines.append("- overlap: PASS")
        except AssertionError as exc:
            failures.append(str(exc))
            lines.append("")
            lines.append(f"- overlap: FAIL — {exc}")

    lines.append("")
    lines.append(f"Status: {'FAIL' if failures else 'PASS'}")
    if failures:
        lines.append("")
        lines.append("Failures:")
        lines.extend(f"- {failure}" for failure in failures)
    return "\n".join(lines)

