"""Keyframe manifest helpers for contact-sheet QA."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class KeyframeSpec:
    label: str
    time: float
    description: str = ""


def write_keyframe_manifest(
    scene_name: str,
    keyframes: list[KeyframeSpec],
    out_path: str | Path,
) -> Path:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "scene": scene_name,
        "keyframes": [asdict(keyframe) for keyframe in keyframes],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def read_keyframe_manifest(path: str | Path) -> list[KeyframeSpec]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        KeyframeSpec(
            label=str(item["label"]),
            time=float(item["time"]),
            description=str(item.get("description", "")),
        )
        for item in payload.get("keyframes", [])
    ]


def default_keyframes_from_beats(
    beats: list[tuple[str, float, float, str]],
    include_ends: bool = True,
) -> list[KeyframeSpec]:
    keyframes: list[KeyframeSpec] = []
    seen: set[tuple[str, float]] = set()
    for label, start, end, description in beats:
        start_spec = KeyframeSpec(label=label, time=float(start), description=description)
        key = (start_spec.label, start_spec.time)
        if key not in seen:
            keyframes.append(start_spec)
            seen.add(key)
        if include_ends:
            end_spec = KeyframeSpec(label=f"{label}_end", time=float(end), description=description)
            key = (end_spec.label, end_spec.time)
            if key not in seen:
                keyframes.append(end_spec)
                seen.add(key)
    return sorted(keyframes, key=lambda spec: spec.time)

