#!/usr/bin/env python3
"""One-command automated scene QA."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StepResult:
    name: str
    command: list[str]
    ok: bool
    output: str


def parse_keyframes(value: str | None) -> list[float]:
    if not value:
        return []
    keyframes = [float(part.strip()) for part in value.split(",") if part.strip()]
    if any(time < 0 for time in keyframes):
        raise ValueError("keyframes must be non-negative")
    return keyframes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run compile, tests, render, duration, contact-sheet QA.")
    parser.add_argument("--scene", required=True)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--expected", required=True, type=float)
    parser.add_argument("--quality", default="ql")
    parser.add_argument("--keyframes")
    return parser


def find_newest_video(media_root: Path, scene_name: str) -> Path:
    matches = [path for path in media_root.rglob("*.mp4") if scene_name in path.name]
    if not matches:
        raise FileNotFoundError(f"No rendered mp4 containing {scene_name!r} under {media_root}")
    return max(matches, key=lambda path: path.stat().st_mtime)


def _quality_flag(quality: str) -> str:
    return f"-{quality}" if quality.startswith("q") else f"-q{quality}"


def run_step(name: str, command: list[str]) -> StepResult:
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    if result.stderr:
        output += ("\n" if output else "") + result.stderr
    return StepResult(name=name, command=command, ok=result.returncode == 0, output=output)


def _format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def write_qa_report(
    report_path: Path,
    scene: str,
    source_file: Path,
    expected: float,
    results: list[StepResult],
    rendered_video: Path | None,
    contact_sheet: Path | None,
    unresolved: list[str],
) -> Path:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    status = "SELF_REVIEW_PASS" if results and all(result.ok for result in results) and not unresolved else "SELF_REVIEW_FAIL"
    lines = [
        f"# QA Report: {scene}",
        "",
        f"- source file: `{source_file}`",
        f"- expected duration: `{expected:.3f}`",
        f"- rendered video: `{rendered_video}`" if rendered_video else "- rendered video: `None`",
        f"- contact sheet: `{contact_sheet}`" if contact_sheet else "- contact sheet: `None`",
        f"- status: `{status}`",
        "",
        "## Commands",
    ]
    for result in results:
        lines.extend(
            [
                f"### {result.name}: {'PASS' if result.ok else 'FAIL'}",
                "",
                f"```bash\n{_format_command(result.command)}\n```",
                "",
                "```text",
                result.output.strip() or "(no output)",
                "```",
                "",
            ]
        )
    lines.append("## Unresolved Issues")
    if unresolved:
        lines.extend(f"- {issue}" for issue in unresolved)
    else:
        lines.append("- None from automated checks. Visual beauty still requires external review.")
    lines.append("")
    lines.append(f"Status: {status}")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    report_dir = Path("reports") / args.scene
    report_path = report_dir / "qa_report.md"
    rendered_video: Path | None = None
    contact_sheet: Path | None = None
    unresolved: list[str] = []
    results: list[StepResult] = []

    try:
        keyframes = parse_keyframes(args.keyframes)
        commands = [
            ("compile", [sys.executable, "-m", "compileall", "src", "tests"]),
            ("unittest", [sys.executable, "-m", "unittest"]),
            ("render", ["manim", _quality_flag(args.quality), str(args.file), args.scene]),
        ]

        for name, command in commands:
            result = run_step(name, command)
            results.append(result)
            if not result.ok:
                unresolved.append(f"{name} failed")
                write_qa_report(report_path, args.scene, args.file, args.expected, results, rendered_video, contact_sheet, unresolved)
                print(report_path)
                return 1

        rendered_video = find_newest_video(Path("media/videos"), args.scene)

        duration_result = run_step(
            "duration",
            [
                sys.executable,
                "scripts/verify_duration.py",
                "media/videos",
                "--scene",
                args.scene,
                "--expected",
                f"{args.expected}",
            ],
        )
        results.append(duration_result)
        if not duration_result.ok:
            unresolved.append("duration verification failed")
            write_qa_report(report_path, args.scene, args.file, args.expected, results, rendered_video, contact_sheet, unresolved)
            print(report_path)
            return 1

        if keyframes:
            contact_sheet = report_dir / "contact_sheet.jpg"
            sheet_result = run_step(
                "contact_sheet",
                [
                    sys.executable,
                    "scripts/make_contact_sheet.py",
                    "--video",
                    str(rendered_video),
                    "--out",
                    str(contact_sheet),
                    "--timestamps",
                    ",".join(str(time) for time in keyframes),
                ],
            )
            results.append(sheet_result)
            if not sheet_result.ok:
                unresolved.append("contact sheet generation failed")
                write_qa_report(report_path, args.scene, args.file, args.expected, results, rendered_video, contact_sheet, unresolved)
                print(report_path)
                return 1

        write_qa_report(report_path, args.scene, args.file, args.expected, results, rendered_video, contact_sheet, unresolved)
    except Exception as exc:
        unresolved.append(str(exc))
        write_qa_report(report_path, args.scene, args.file, args.expected, results, rendered_video, contact_sheet, unresolved)
        print(report_path)
        return 1

    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

