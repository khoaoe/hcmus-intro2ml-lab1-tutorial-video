import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_DIR = Path(__file__).resolve().parents[1] / "src" / "scenes"


SCENES = [
    {
        "module": "scene_13_01_final_synthesis",
        "class": "Scene1301FinalSynthesis",
        "id": "13.1",
        "title": "Final synthesis",
        "start": 115 * 60 + 20,
        "end": 117 * 60 + 30,
        "duration": 130.0,
        "labels": (
            "finite vectors",
            "functions",
            "solvers",
            "solution operator",
            "NO architectures",
            "domains",
            "open problems",
            "GNO",
            "FNO",
            "Transformer NO",
            "CoDA-NO",
            "metrics",
            "uncertainty",
            "chaos",
            "scaling",
            "physics",
            "multi-dataset",
        ),
        "comments": (
            "1:55:20.0 -> local 0.0",
            "1:55:33.0 -> local 13.0",
            "1:55:46.0 -> local 26.0",
            "1:55:59.0 -> local 39.0",
            "1:56:12.0 -> local 52.0",
            "1:56:26.0 -> local 66.0",
            "1:56:41.0 -> local 81.0",
            "1:56:58.0 -> local 98.0",
            "1:57:30.0 -> local 130.0",
        ),
    },
    {
        "module": "scene_13_02_last_line",
        "class": "Scene1302LastLine",
        "id": "13.2",
        "title": "Last line",
        "start": 117 * 60 + 30,
        "end": 118 * 60 + 20,
        "duration": 50.0,
        "labels": (
            "Learning in infinite dimensions",
            r"\mathcal{G}: \mathcal{A} \to \mathcal{U}",
            "field này mới chỉ bắt đầu",
        ),
        "comments": (
            "1:57:30.0 -> local 0.0",
            "1:57:42.0 -> local 12.0",
            "1:57:43.0 -> local 13.0",
            "1:58:00.0 -> local 30.0",
            "1:58:12.0 -> local 42.0",
            "1:58:20.0 -> local 50.0",
        ),
    },
]


def load_scene_module(module_name):
    path = SCENE_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Section13SceneContractTest(unittest.TestCase):
    def test_scene_classes_expose_script_timing_contract(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                scene_class = getattr(module, spec["class"])

                self.assertEqual(scene_class.SCRIPT_ID, spec["id"])
                self.assertEqual(scene_class.SCRIPT_TITLE, spec["title"])
                self.assertEqual(scene_class.SCRIPT_START, spec["start"])
                self.assertEqual(scene_class.SCRIPT_END, spec["end"])
                self.assertEqual(scene_class.SCENE_DURATION, spec["duration"])

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(getattr(module, spec["class"]).construct)

                self.assertIn("self.play_timed", source)
                self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
                self.assertNotIn("self.play(", source)
                self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(module)

                for label in spec["labels"]:
                    self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(getattr(module, spec["class"]).construct)

                for comment in spec["comments"]:
                    self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
