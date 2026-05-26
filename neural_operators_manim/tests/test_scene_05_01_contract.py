import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_05_01_different_meshes.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_05_discretization", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0501ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0501DifferentMeshes

        self.assertEqual(scene_class.SCRIPT_ID, "5.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Input and output may live on different meshes")
        self.assertEqual(scene_class.SCRIPT_START, 29 * 60 + 10)
        self.assertEqual(scene_class.SCRIPT_END, 31 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 130.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_irregular_mesh_card",
            "make_regular_grid_card",
            "make_sparse_sensor_card",
            "make_standard_nn_gate",
            "make_neural_operator_gate",
            "make_query_points",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0501DifferentMeshes.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "input samples: (x_i, a(x_i))",
            "sample 1: irregular mesh",
            "sample 2: regular grid",
            "sample 3: sparse sensors + complex boundary",
            "fixed tensor H x W x C",
            "shape mismatch",
            "same underlying function, different discretizations",
            "sample points x_i",
            "values a(x_i)",
            "query points y_j",
            "coarse grid",
            "fine grid",
            "irregular points",
            r"\sum_i \kappa(y, x_i)a(x_i)\Delta x_i",
            r"\int \kappa(y,x)a(x)\,dx",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0501DifferentMeshes.construct)

        for comment in (
            "29:10.0 -> local 0.0",
            "29:22.0 -> local 12.0",
            "29:33.5 -> local 23.5",
            "29:46.0 -> local 36.0",
            "29:47.0 -> local 37.0",
            "30:00.0 -> local 50.0",
            "30:16.5 -> local 66.5",
            "30:35.0 -> local 85.0",
            "31:20.0 -> local 130.0",
        ):
            self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
