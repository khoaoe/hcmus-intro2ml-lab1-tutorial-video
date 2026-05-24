#!/usr/bin/env python3
"""Build contact sheets from rendered Manim videos."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_timestamps(value: str) -> list[float]:
    timestamps = [float(part.strip()) for part in value.split(",") if part.strip()]
    if not timestamps:
        raise ValueError("timestamps must contain at least one value")
    if any(time < 0 for time in timestamps):
        raise ValueError("timestamps must be non-negative")
    return timestamps


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a labeled video contact sheet.")
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timestamps")
    parser.add_argument("--interval", type=float)
    parser.add_argument("--thumb-width", type=int, default=420)
    parser.add_argument("--cols", type=int, default=4)
    return parser


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True)


def _read_duration(video: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def _timestamps_from_interval(video: Path, interval: float) -> list[float]:
    if interval <= 0:
        raise ValueError("interval must be positive")
    duration = _read_duration(video)
    count = max(1, int(math.floor(duration / interval)) + 1)
    times = [round(index * interval, 3) for index in range(count)]
    if times[-1] < duration:
        times.append(round(duration, 3))
    return times


def _extract_frames(video: Path, timestamps: list[float], frame_dir: Path) -> list[Path]:
    frames: list[Path] = []
    for index, timestamp in enumerate(timestamps):
        frame = frame_dir / f"frame_{index:04d}.jpg"
        _run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(frame),
            ]
        )
        if not frame.exists():
            raise RuntimeError(f"ffmpeg did not create frame at {timestamp:.3f}s")
        frames.append(frame)
    return frames


def _make_sheet_with_pillow(
    frames: list[Path],
    timestamps: list[float],
    out_path: Path,
    thumb_width: int,
    cols: int,
) -> None:
    from PIL import Image, ImageDraw

    images = [Image.open(frame).convert("RGB") for frame in frames]
    if not images:
        raise ValueError("no frames to assemble")
    thumb_height = max(1, int(images[0].height * thumb_width / images[0].width))
    label_height = 28
    rows = math.ceil(len(images) / cols)
    sheet = Image.new("RGB", (cols * thumb_width, rows * (thumb_height + label_height)), "#0B1020")
    draw = ImageDraw.Draw(sheet)

    for index, image in enumerate(images):
        row = index // cols
        col = index % cols
        thumb = image.resize((thumb_width, thumb_height))
        x = col * thumb_width
        y = row * (thumb_height + label_height)
        sheet.paste(thumb, (x, y + label_height))
        draw.text((x + 8, y + 6), f"{timestamps[index]:.1f}s", fill="#E5E7EB")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def _make_sheet_with_ffmpeg(
    frames: list[Path],
    out_path: Path,
    thumb_width: int,
    cols: int,
) -> None:
    rows = math.ceil(len(frames) / cols)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pattern = str(frames[0].parent / "frame_%04d.jpg")
    _run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "1",
            "-i",
            pattern,
            "-vf",
            f"scale={thumb_width}:-1,tile={cols}x{rows}",
            str(out_path),
        ]
    )


def create_contact_sheet(
    video: Path,
    out_path: Path,
    timestamps: list[float],
    thumb_width: int = 420,
    cols: int = 4,
) -> Path:
    if not video.exists():
        raise FileNotFoundError(f"video not found: {video}")
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required to extract contact-sheet frames")
    if cols <= 0:
        raise ValueError("cols must be positive")
    if thumb_width <= 0:
        raise ValueError("thumb-width must be positive")

    with tempfile.TemporaryDirectory() as tmp:
        frames = _extract_frames(video, timestamps, Path(tmp))
        try:
            _make_sheet_with_pillow(frames, timestamps, out_path, thumb_width, cols)
        except ImportError:
            _make_sheet_with_ffmpeg(frames, out_path, thumb_width, cols)
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.timestamps and args.interval is not None:
            raise ValueError("use either --timestamps or --interval, not both")
        if args.timestamps:
            timestamps = parse_timestamps(args.timestamps)
        elif args.interval is not None:
            timestamps = _timestamps_from_interval(args.video, args.interval)
        else:
            raise ValueError("provide --timestamps or --interval")
        out_path = create_contact_sheet(args.video, args.out, timestamps, args.thumb_width, args.cols)
    except Exception as exc:
        print(f"contact sheet failed: {exc}", file=sys.stderr)
        return 1

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

