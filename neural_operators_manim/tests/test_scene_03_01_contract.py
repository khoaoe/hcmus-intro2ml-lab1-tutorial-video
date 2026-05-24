import importlib
import inspect
import unittest

from manim import Scene


class Scene0301ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_03_01_model_phenomena_with_equations"
        )
        scene_class = module.Scene0301ModelPhenomenaWithEquations

        self.assertEqual(scene_class.SCRIPT_ID, "3.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Model phenomena with equations")
        self.assertEqual(scene_class.SCRIPT_START, 15 * 60 + 45)
        self.assertEqual(scene_class.SCRIPT_END, 17 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 95.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_01_model_phenomena_with_equations"
        )
        scene_class = module.Scene0301ModelPhenomenaWithEquations

        for method_name in (
            "make_equation_board",
            "make_continuum_mesh",
            "make_solver_pipeline",
            "make_toolbox",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_01_model_phenomena_with_equations"
        )

        for class_name in (
            "EquationBoard",
            "Mesh",
            "SolverBox",
            "Toolbox",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module(
            "src.scenes.scene_03_01_model_phenomena_with_equations"
        )
        source = inspect.getsource(module.Scene0301ModelPhenomenaWithEquations.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_03_01_model_phenomena_with_equations"
        )
        source = inspect.getsource(module)

        for label in (
            "Traditional Scientific Computing",
            "First principles",
            "physics",
            "geometry",
            "constraints",
            "Differential equations",
            "Algebraic equations",
            "Conservation laws",
            "Boundary conditions",
            "Initial conditions",
            "Navier-Stokes",
            "Maxwell",
            "Schrodinger",
            "Darcy",
            "Helmholtz",
            "Heat",
            "Wave",
            r"\mathcal{E}(u; a, f)=0",
            "continuum",
            "discretize domain -> mesh / grid",
            "Equation + Mesh",
            "Numerical Solver",
            "Discrete Solution",
            "finite difference",
            "finite volume",
            "finite element",
            "spectral",
            "PDE Solvers",
            "Machine Learning / Neural Operators",
            "Not replacement. Complementary tool.",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
