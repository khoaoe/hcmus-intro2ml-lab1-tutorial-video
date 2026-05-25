import importlib
import inspect
import unittest

from manim import Scene


class Scene0401ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_04_01_from_solve_u_to_predict_u")
        scene_class = module.Scene0401FromSolveUToPredictU

        self.assertEqual(scene_class.SCRIPT_ID, "4.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, 'From "solve u" to "predict u"')
        self.assertEqual(scene_class.SCRIPT_START, 23 * 60 + 20)
        self.assertEqual(scene_class.SCRIPT_END, 25 * 60)
        self.assertEqual(scene_class.SCENE_DURATION, 100.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_04_01_from_solve_u_to_predict_u")

        for function_name in (
            "make_function_panel",
            "make_solver_block",
            "make_operator_block",
            "make_dataset_pairs",
            "make_speed_meter",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module("src.scenes.scene_04_01_from_solve_u_to_predict_u")

        for class_name in (
            "SolverLoop",
            "TrainingCompression",
            "ForwardPassArrow",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module("src.scenes.scene_04_01_from_solve_u_to_predict_u")
        source = inspect.getsource(module.Scene0401FromSolveUToPredictU.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module("src.scenes.scene_04_01_from_solve_u_to_predict_u")
        source = inspect.getsource(module)

        for label in (
            "solver-based view",
            "operator learning view",
            "solve u",
            "predict u",
            r"a(x)",
            r"u(x)",
            "PDE solver",
            "mesh + stencil",
            "linear system",
            "solve again",
            r"(a_i,u_i)",
            r"\mathcal{G}_{\theta}",
            r"a_{\mathrm{new}}(x)",
            r"u_{\mathrm{pred}}(x)",
            "forward pass",
            "cost",
            "data",
            "training",
            "generalization",
            "open questions",
            "payoff",
            "fast many-query inference",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
