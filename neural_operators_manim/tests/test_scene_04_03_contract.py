import importlib
import inspect
import unittest

from manim import Scene


class Scene0403ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_04_03_three_errors_we_must_remember")
        scene_class = module.Scene0403ThreeErrorsWeMustRemember

        self.assertEqual(scene_class.SCRIPT_ID, "4.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "The three errors we must remember")
        self.assertEqual(scene_class.SCRIPT_START, 27 * 60 + 5)
        self.assertEqual(scene_class.SCRIPT_END, 29 * 60 + 10)
        self.assertEqual(scene_class.SCENE_DURATION, 125.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_04_03_three_errors_we_must_remember")

        for function_name in (
            "make_error_card",
            "make_error_triangle",
            "make_high_frequency_curve_panel",
            "make_coarse_sampling_panel",
            "make_precision_knob",
            "make_total_error_summary",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module("src.scenes.scene_04_03_three_errors_we_must_remember")

        for class_name in (
            "ErrorTriangle",
            "HighFreqCurve",
            "CoarseSampling",
            "PrecisionKnob",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module("src.scenes.scene_04_03_three_errors_we_must_remember")
        source = inspect.getsource(module.Scene0403ThreeErrorsWeMustRemember.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module("src.scenes.scene_04_03_three_errors_we_must_remember")
        source = inspect.getsource(module)

        for label in (
            "approximation error",
            "generalization error",
            "discretization error",
            "function class expressivity",
            "data supports correct pattern",
            "point evaluation",
            "mesh",
            "sensor",
            "snapshot",
            "information lost",
            "true continuum",
            "coarse samples",
            "wrong smooth reconstruction",
            r"\text{total error} \approx \text{approximation} + \text{generalization} + \text{discretization}",
            "fp16",
            "fp32",
            "fp64",
            "coarse mesh still dominates",
            "Section 5",
            "discretization challenge",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
