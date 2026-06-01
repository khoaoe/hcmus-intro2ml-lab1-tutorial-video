import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_09_03_error_decomposition.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_09_03_error_decomposition", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0903ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0903ErrorDecomposition

        self.assertEqual(scene_class.SCRIPT_ID, "9.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Error decomposition")
        self.assertEqual(scene_class.SCRIPT_START, 63 * 60 + 20)
        self.assertEqual(scene_class.SCRIPT_END, 65 * 60 + 10)
        self.assertEqual(scene_class.SCENE_DURATION, 110.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_error_decomposition_bar",
            "make_resolution_experiment_table",
            "make_same_grid_warning",
            "make_operator_validation_panel",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0903ErrorDecomposition.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "operator-level error",
            "approximation error",
            "discretization error",
            "generalization error",
            "train 16",
            "test 32",
            "test 64",
            "mesh refinement",
            "evaluation metric",
            "same-grid only",
            "full operator validation",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0903ErrorDecomposition.construct)

        for comment in (
            "1:03:20.0 -> local 0.0",
            "1:03:31.5 -> local 11.5",
            "1:03:45.0 -> local 25.0",
            "1:03:58.5 -> local 38.5",
            "1:03:59.5 -> local 39.5",
            "1:04:15.0 -> local 55.0",
            "1:04:31.0 -> local 71.0",
            "1:05:10.0 -> local 110.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
