import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_05_03_discretization_convergent_intuition.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_05_03_discretization_convergent_intuition", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0503ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0503DiscretizationConvergentIntuition

        self.assertEqual(scene_class.SCRIPT_ID, "5.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Discretization-convergent intuition")
        self.assertEqual(scene_class.SCRIPT_START, 33 * 60 + 5)
        self.assertEqual(scene_class.SCRIPT_END, 35 * 60)
        self.assertEqual(scene_class.SCENE_DURATION, 115.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_continuum_field",
            "make_mesh_overlay",
            "make_sampled_prediction",
            "make_refinement_triptych",
            "make_unstable_vs_convergent_panel",
            "make_parameter_capsule",
            "make_finite_to_continuum_bridge",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0503DiscretizationConvergentIntuition.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "discretization-convergent",
            "mesh refinement → stable continuum limit",
            "coarse",
            "medium",
            "fine",
            "same operator",
            "distance to limit ↓",
            "runs on many resolutions",
            "converges under refinement",
            "runs ≠ converges",
            "same θ",
            "same underlying operator",
            "different discretizations",
            "finite computation → continuum operator",
            "Discretization is how we compute.",
            "The operator is what we learn.",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0503DiscretizationConvergentIntuition.construct)

        for comment in (
            "33:05.0 -> local 0.0",
            "33:18.0 -> local 13.0",
            "33:30.5 -> local 25.5",
            "33:46.0 -> local 41.0",
            "33:47.0 -> local 42.0",
            "34:02.5 -> local 57.5",
            "34:19.5 -> local 74.5",
            "35:00.0 -> local 115.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
