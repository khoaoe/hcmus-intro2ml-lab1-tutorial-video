import importlib
import inspect
import unittest

from manim import Scene


class Scene0402ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")
        scene_class = module.Scene0402OperatorLearningNotBiggerTensors

        self.assertEqual(scene_class.SCRIPT_ID, "4.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Operator learning is not just supervised learning with bigger tensors")
        self.assertEqual(scene_class.SCRIPT_START, 25 * 60)
        self.assertEqual(scene_class.SCRIPT_END, 27 * 60 + 5)
        self.assertEqual(scene_class.SCENE_DURATION, 125.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")

        for function_name in (
            "make_tensor_block",
            "make_cracked_tensor",
            "make_sampled_curve",
            "make_resolution_strip",
            "make_domain_icon_sphere",
            "make_domain_icon_car_mesh",
            "make_domain_icon_volume",
            "make_continuum_operator_panel",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")

        for class_name in (
            "TensorBlock",
            "CrackAnimation",
            "SampledFunction",
            "ContinuumOperator",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")
        source = inspect.getsource(module.Scene0402OperatorLearningNotBiggerTensors.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_resolution_cards_do_not_duplicate_sample_labels(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")
        source = inspect.getsource(module.make_resolution_strip)

        self.assertIn("make_sampled_curve(n, label, show_label=False)", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module("src.scenes.scene_04_02_operator_learning_not_bigger_tensors")
        source = inspect.getsource(module)

        for label in (
            "Not just bigger tensors",
            "bigger tensor != operator learning",
            "8 samples",
            "16 samples",
            "64 samples",
            "same function",
            "coarse train mesh",
            "fine test mesh",
            "irregular sensors",
            "regular query points",
            "sphere",
            "car surface mesh",
            "3D volume",
            "fixed-grid CNN",
            "resize can run",
            "does not guarantee same continuum operator",
            r"\mathcal{G}: \mathcal{A} \to \mathcal{U}",
            r"a(x)",
            r"u(y)",
            "continuum problem",
            "discretization = observation",
            "table on this grid",
            "relation between functions",
            "sampled tables are observations",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
