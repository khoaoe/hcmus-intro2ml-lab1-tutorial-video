import tempfile
import unittest
from pathlib import Path

from manim import RIGHT, Circle, Rectangle, Text


class VisualSystemV2Test(unittest.TestCase):
    def test_safe_text_fits_width(self):
        from src.common.safe_text import safe_text

        label = safe_text("Function space", max_width=2.8, font_size=32)

        self.assertLessEqual(label.width, 2.8)
        self.assertEqual(label.safe_max_width, 2.8)

    def test_safe_text_raises_on_impossible_constraints(self):
        from src.common.safe_text import safe_text

        with self.assertRaises(ValueError):
            safe_text("This cannot fit", max_width=0.01, font_size=18, min_font_size=14)

    def test_safe_paragraph_wraps_and_fits(self):
        from src.common.safe_text import safe_paragraph

        paragraph = safe_paragraph(
            "Scientific fields need derivatives and integrals, not only pixels.",
            max_width=3.4,
            max_height=1.4,
            font_size=22,
        )

        self.assertLessEqual(paragraph.width, 3.4)
        self.assertLessEqual(paragraph.height, 1.4)

    def test_chip_label_is_inside_chip_box(self):
        from src.common.panels import Chip
        from src.common.visual_safety import assert_inside

        chip = Chip("operator", max_width=1.8)

        assert_inside(chip.label, chip.box, padding=0.04)

    def test_panel_card_title_and_body_are_inside_card(self):
        from src.common.panels import PanelCard
        from src.common.visual_safety import assert_inside, assert_panel_integrity

        body = Circle(radius=0.4)
        panel = PanelCard("Solution operator", body=body, width=3.2, height=2.2)

        assert_inside(panel.title_mob, panel.box, padding=0.04)
        assert_inside(panel.body, panel.box, padding=0.04)
        assert_panel_integrity(panel)

    def test_assert_no_overlap_detects_overlap(self):
        from src.common.visual_safety import assert_no_overlap

        a = Rectangle(width=1, height=1)
        b = Rectangle(width=1, height=1)

        with self.assertRaises(AssertionError):
            assert_no_overlap(a, b)

        b.shift(RIGHT * 2)
        assert_no_overlap(a, b)

    def test_assert_in_frame_detects_object_outside_frame(self):
        from src.common.visual_safety import assert_in_frame

        mob = Text("outside", font_size=20).shift(RIGHT * 20)

        with self.assertRaises(AssertionError):
            assert_in_frame(mob)

    def test_keyframe_manifest_roundtrip(self):
        from src.common.keyframes import (
            KeyframeSpec,
            read_keyframe_manifest,
            write_keyframe_manifest,
        )

        keyframes = [
            KeyframeSpec("open", 0.0, "title"),
            KeyframeSpec("focus", 10.5, "main panel"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "keyframes.json"
            written = write_keyframe_manifest("SceneTest", keyframes, path)

            self.assertEqual(written, path)
            self.assertEqual(read_keyframe_manifest(path), keyframes)


if __name__ == "__main__":
    unittest.main()
