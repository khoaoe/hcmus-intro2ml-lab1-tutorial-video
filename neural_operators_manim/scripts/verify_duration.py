#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def find_scene_video(media_root: Path, scene_name: str) -> Path:
    matches = sorted(media_root.rglob(f"{scene_name}.mp4"))
    if not matches:
        raise FileNotFoundError(f"No rendered video found for scene {scene_name!r} under {media_root}")
    return matches[-1]


def read_duration(video_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def duration_within_tolerance(duration: float, expected: float, tolerance: float) -> bool:
    return abs(duration - expected) <= tolerance + 1e-9


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify rendered Manim scene duration.")
    parser.add_argument("media_root", type=Path)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--expected", required=True, type=float)
    parser.add_argument("--tolerance", type=float, default=0.05)
    args = parser.parse_args()

    video_path = find_scene_video(args.media_root, args.scene)
    duration = read_duration(video_path)
    delta = abs(duration - args.expected)

    print(f"{args.scene}: {duration:.3f}s (expected {args.expected:.3f}s, delta {delta:.3f}s)")
    print(video_path)

    if not duration_within_tolerance(duration, args.expected, args.tolerance):
        print(
            f"Duration mismatch: delta {delta:.3f}s exceeds tolerance {args.tolerance:.3f}s",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
