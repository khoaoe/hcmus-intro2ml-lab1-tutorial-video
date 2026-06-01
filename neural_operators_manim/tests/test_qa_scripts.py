import tempfile
import time
import unittest
from pathlib import Path


class QAScriptsTest(unittest.TestCase):
    def test_parse_timestamps(self):
        from scripts.make_contact_sheet import parse_timestamps

        self.assertEqual(parse_timestamps("0,10.5, 22"), [0.0, 10.5, 22.0])

    def test_contact_sheet_argument_parser_accepts_timestamp_mode(self):
        from scripts.make_contact_sheet import build_parser

        args = build_parser().parse_args(
            [
                "--video",
                "video.mp4",
                "--out",
                "sheet.jpg",
                "--timestamps",
                "0,1",
            ]
        )

        self.assertEqual(args.video, Path("video.mp4"))
        self.assertEqual(args.out, Path("sheet.jpg"))
        self.assertEqual(args.timestamps, "0,1")

    def test_find_newest_video_path(self):
        from scripts.check_scene import find_newest_video

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "a" / "SceneDemo.mp4"
            new = root / "b" / "SceneDemo.mp4"
            old.parent.mkdir()
            new.parent.mkdir()
            old.write_bytes(b"old")
            time.sleep(0.01)
            new.write_bytes(b"new")

            self.assertEqual(find_newest_video(root, "SceneDemo"), new)

    def test_check_scene_parse_keyframes(self):
        from scripts.check_scene import parse_keyframes

        self.assertEqual(parse_keyframes("0,10.5,130"), [0.0, 10.5, 130.0])
        self.assertEqual(parse_keyframes(None), [])

    def test_duration_boundary_accepts_one_frame_tolerance(self):
        from scripts.verify_duration import duration_within_tolerance

        self.assertTrue(duration_within_tolerance(139.95, expected=140.0, tolerance=0.05))
        self.assertFalse(duration_within_tolerance(139.94, expected=140.0, tolerance=0.05))

    def test_qa_report_creation(self):
        from scripts.check_scene import StepResult, write_qa_report

        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "qa_report.md"
            write_qa_report(
                report_path=report_path,
                scene="SceneDemo",
                source_file=Path("src/scenes/demo.py"),
                expected=12.0,
                results=[
                    StepResult("compile", ["python", "-m", "compileall"], True, ""),
                    StepResult("render", ["manim"], False, "boom"),
                ],
                rendered_video=Path("media/videos/SceneDemo.mp4"),
                contact_sheet=None,
                unresolved=["render failed"],
            )

            text = report_path.read_text(encoding="utf-8")
            self.assertIn("SELF_REVIEW_FAIL", text)
            self.assertIn("SceneDemo", text)
            self.assertIn("render failed", text)


if __name__ == "__main__":
    unittest.main()
