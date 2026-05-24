import importlib
import inspect
import unittest

from manim import Scene


class Scene0302ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_03_02_darcy_flow_clean_toy_example"
        )
        scene_class = module.Scene0302DarcyFlowCleanToyExample

        self.assertEqual(scene_class.SCRIPT_ID, "3.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Darcy flow as the clean toy example")
        self.assertEqual(scene_class.SCRIPT_START, 17 * 60 + 20)
        self.assertEqual(scene_class.SCRIPT_END, 19 * 60 + 35)
        self.assertEqual(scene_class.SCENE_DURATION, 135.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_02_darcy_flow_clean_toy_example"
        )
        scene_class = module.Scene0302DarcyFlowCleanToyExample

        for method_name in (
            "make_porous_medium",
            "make_random_field",
            "make_solution_field",
            "make_pde_pipeline",
            "make_operator_view",
            "make_finite_difference_demo",
            "make_refinement_panels",
            "make_compute_meter",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_02_darcy_flow_clean_toy_example"
        )

        for class_name in (
            "RandomField",
            "SolutionField",
            "ComputeMeter",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module(
            "src.scenes.scene_03_02_darcy_flow_clean_toy_example"
        )
        source = inspect.getsource(module.Scene0302DarcyFlowCleanToyExample.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_03_02_darcy_flow_clean_toy_example"
        )
        source = inspect.getsource(module)

        for label in (
            "Darcy flow: clean toy example",
            "flow through porous media",
            "input function",
            "a(x): permeability / diffusion coefficient",
            "output function",
            "u(x): pressure / potential",
            r"-\nabla\cdot(a(x)\nabla u(x))=f(x)",
            "equation",
            "boundary conditions",
            "solver finds u",
            r"\mathcal{G}",
            "Solution operator",
            r"\mathcal{G}: a \mapsto u",
            r"\frac{u_{i+1}-u_i}{\Delta x}",
            "continuum PDE -> finite-dimensional system",
            "finer mesh -> better approximation",
            "time",
            "memory",
            "energy",
            "Accuracy is not free.",
            "better solution ~= more computation",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
