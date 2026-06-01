import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_09_02_universal_approximation_caveats.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_09_02_universal_approximation_caveats", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0902ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0902UniversalApproximationCaveats

        self.assertEqual(scene_class.SCRIPT_ID, "9.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Universal approximation, but with caveats")
        self.assertEqual(scene_class.SCRIPT_START, 61 * 60)
        self.assertEqual(scene_class.SCRIPT_END, 63 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 140.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_theorem_card",
            "make_caveat_cards",
            "make_research_questions",
            "make_expressivity_split",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0902UniversalApproximationCaveats.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "universal approximation",
            "continuous operators",
            "compact set",
            "expressivity",
            "training",
            "data",
            "metric",
            "physics",
            "domain knowledge",
            "parameterization",
            "loss",
            "research questions",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0902UniversalApproximationCaveats.construct)

        for comment in (
            "1:01:00.0 -> local 0.0",
            "1:01:14.0 -> local 14.0",
            "1:01:27.0 -> local 27.0",
            "1:01:28.2 -> local 28.2",
            "1:01:42.0 -> local 42.0",
            "1:01:58.0 -> local 58.0",
            "1:02:12.0 -> local 72.0",
            "1:02:34.0 -> local 94.0",
            "1:03:20.0 -> local 140.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
