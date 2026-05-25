import importlib
import inspect
import unittest

from manim import Scene


class Scene0304ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_03_04_scientific_ml_hypothesis")
        scene_class = module.Scene0304ScientificMLHypothesis

        self.assertEqual(scene_class.SCRIPT_ID, "3.4")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Scientific ML hypothesis")
        self.assertEqual(scene_class.SCRIPT_START, 21 * 60 + 35)
        self.assertEqual(scene_class.SCRIPT_END, 23 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 105.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_03_04_scientific_ml_hypothesis")
        scene_class = module.Scene0304ScientificMLHypothesis

        for method_name in (
            "make_training_pairs",
            "make_operator_learning_view",
            "make_fast_inference_view",
            "make_scenario_batch",
            "make_fixed_grid_trap",
            "make_multi_mesh_world",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module("src.scenes.scene_03_04_scientific_ml_hypothesis")

        for class_name in (
            "TrainingPairs",
            "LearnedOperatorBlock",
            "FastInferenceFanout",
            "ScenarioBatch",
            "FixedGridTrap",
            "MultiMeshWorld",
            "ShapeMismatchWarning",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module("src.scenes.scene_03_04_scientific_ml_hypothesis")
        source = inspect.getsource(module.Scene0304ScientificMLHypothesis.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module("src.scenes.scene_03_04_scientific_ml_hypothesis")
        source = inspect.getsource(module)

        for label in (
            "Scientific ML hypothesis",
            r"(a_1,u_1)",
            r"(a_2,u_2)",
            r"(a_N,u_N)",
            "Learn",
            r"\mathcal{G}: \mathcal{A} \to \mathcal{U}",
            "solve one instance",
            "learn the solution operator",
            r"a_{\mathrm{new}}(x)",
            r"u_{\mathrm{pred}}(x)",
            "traditional solver: minutes / hours",
            "trained operator: milliseconds / seconds",
            "uncertainty quantification",
            "design optimization",
            "ensemble forecasting",
            "inverse problems",
            "64x64",
            "128x128",
            "irregular mesh",
            "sparse sensors",
            "fixed-grid NN is too narrow",
            "regular grid",
            "sparse sensor layout",
            "different input/output meshes",
            "curved / spherical domain",
            "sample points + values",
            "query points",
            "Model must live across discretizations.",
            "Not just bigger NN. Different design principle.",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
