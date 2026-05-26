import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_05_02_output_must_be_queryable.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_05_02_output_must_be_queryable", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0502ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0502OutputMustBeQueryable

        self.assertEqual(scene_class.SCRIPT_ID, "5.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Output must be queryable")
        self.assertEqual(scene_class.SCRIPT_START, 31 * 60 + 20)
        self.assertEqual(scene_class.SCRIPT_END, 33 * 60 + 5)
        self.assertEqual(scene_class.SCENE_DURATION, 105.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_output_field",
            "value_at_point",
            "make_query_label",
            "make_derivative_stencil",
            "make_surface_integral_demo",
            "make_weather_integral_demo",
            "make_fixed_tensor_vs_callable_panel",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0502OutputMustBeQueryable.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "output ≠ fixed tensor",
            "output ≈ function u(y)",
            "u(y) =",
            "local derivative",
            r"\text{drag} \propto \int_{\text{surface}} p(y)n(y)\,dS",
            "average over region",
            "flux across boundary",
            "energy integral",
            "fixed tensor output",
            "post interpolation",
            "warning: interpolation outside architecture",
            "query point y",
            "model returns u(y)",
            "derivative / integral tools",
            "Neural operator output: callable approximation of a function",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0502OutputMustBeQueryable.construct)

        for comment in (
            "31:20.0 -> local 0.0",
            "31:31.0 -> local 11.0",
            "31:44.5 -> local 24.5",
            "31:57.0 -> local 37.0",
            "32:09.0 -> local 49.0",
            "32:10.0 -> local 50.0",
            "32:25.5 -> local 65.5",
            "33:05.0 -> local 105.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
