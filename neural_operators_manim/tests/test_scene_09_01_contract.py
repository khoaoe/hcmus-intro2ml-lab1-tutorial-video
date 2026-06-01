import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_09_01_lift_operate_project.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_09_01_lift_operate_project", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0901ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0901LiftOperateProject

        self.assertEqual(scene_class.SCRIPT_ID, "9.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Lift, operate, project")
        self.assertEqual(scene_class.SCRIPT_START, 58 * 60 + 50)
        self.assertEqual(scene_class.SCRIPT_END, 61 * 60)
        self.assertEqual(scene_class.SCENE_DURATION, 130.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_channel_stack",
            "make_architecture_pipeline",
            "make_operator_layer_stack",
            "make_feature_field_stack",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0901LiftOperateProject.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "lift",
            "operate",
            "project",
            "temperature",
            "velocity",
            "humidity",
            "land mask",
            r"a(x)",
            r"P(a(x))",
            "function-to-function layers",
            r"Q(v(x))",
            r"u(x)",
            "physical variables",
            "function space",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0901LiftOperateProject.construct)

        for comment in (
            "58:50.0 -> local 0.0",
            "59:03.0 -> local 13.0",
            "59:16.0 -> local 26.0",
            "59:29.0 -> local 39.0",
            "59:43.0 -> local 53.0",
            "59:56.0 -> local 66.0",
            "1:00:14.0 -> local 84.0",
            "1:01:00.0 -> local 130.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
