import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_09_04_different_input_output_domains.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_09_04_different_input_output_domains", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0904ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0904DifferentInputOutputDomains

        self.assertEqual(scene_class.SCRIPT_ID, "9.4")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Question embedded: what if input/output domains differ?")
        self.assertEqual(scene_class.SCRIPT_START, 65 * 60 + 10)
        self.assertEqual(scene_class.SCRIPT_END, 67 * 60 + 40)
        self.assertEqual(scene_class.SCENE_DURATION, 150.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_wall_surface",
            "make_room_volume",
            "make_cross_domain_kernel",
            "make_learned_residual_bridge",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0904DifferentInputOutputDomains.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "input domain",
            "output domain",
            "wall temperature",
            "2D surface",
            "3D volume",
            "interior query",
            r"\kappa(y,x)",
            "cross-domain kernel",
            "identity residual unavailable",
            "learned residual bridge",
            "geometry first",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0904DifferentInputOutputDomains.construct)

        for comment in (
            "1:05:10.0 -> local 0.0",
            "1:05:22.0 -> local 12.0",
            "1:05:36.0 -> local 26.0",
            "1:05:49.0 -> local 39.0",
            "1:05:50.0 -> local 40.0",
            "1:06:05.0 -> local 55.0",
            "1:06:20.5 -> local 70.5",
            "1:06:36.0 -> local 86.0",
            "1:07:40.0 -> local 150.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
