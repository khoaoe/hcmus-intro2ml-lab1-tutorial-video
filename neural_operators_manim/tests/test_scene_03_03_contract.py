import importlib
import inspect
import unittest

from manim import Scene


class Scene0303ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )
        scene_class = module.Scene0303WhyNotHandDesignSolvers

        self.assertEqual(scene_class.SCRIPT_ID, "3.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Why not just keep hand-designing solvers?")
        self.assertEqual(scene_class.SCRIPT_START, 19 * 60 + 35)
        self.assertEqual(scene_class.SCRIPT_END, 21 * 60 + 35)
        self.assertEqual(scene_class.SCENE_DURATION, 120.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )
        scene_class = module.Scene0303WhyNotHandDesignSolvers

        for method_name in (
            "make_clean_solver_question",
            "make_weather_system",
            "make_equation_wall",
            "make_parameterization_error",
            "make_resolution_ladder",
            "make_exponential_curve",
            "make_inverse_loop",
            "make_final_complement_view",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )

        for class_name in (
            "EquationWall",
            "ApproximationBlocks",
            "ResolutionLadder",
            "ExponentialCurve",
            "InverseLoop",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )
        source = inspect.getsource(module.Scene0303WhyNotHandDesignSolvers.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )
        source = inspect.getsource(module)

        for label in (
            "If solvers are powerful...",
            "why not hand-design everything?",
            "Not replacement. Complement.",
            "real world is not a clean toy PDE",
            "toy PDE",
            "clouds",
            "mountains",
            "ocean waves",
            "radiation",
            "turbulence",
            "microphysics",
            "heuristic closure",
            "lookup table",
            "empirical rule",
            "sub-grid model",
            "parameterization",
            "runnable model",
            "approximation error",
            "100 km",
            "10 km",
            "1 km",
            "100 m",
            "higher resolution -> more detail",
            "resolution ↑",
            "compute ↑",
            "grid size ↓",
            "time step ↓",
            "more cells",
            "more steps",
            "slow / non-differentiable",
            "inverse problem bottleneck",
            "modeling gap",
            "compute wall",
            "inverse bottleneck",
            "Machine Learning",
            "Neural Operators",
        ):
            self.assertIn(label, source, label)

    def test_cards_do_not_repeat_title_as_body_text(self):
        module = importlib.import_module(
            "src.scenes.scene_03_03_why_not_hand_design_solvers"
        )
        source = inspect.getsource(module)

        duplicate_patterns = (
            'PanelCard(label, body=SafeText(label',
            'PanelCard("modeling gap", body=SafeText("modeling gap"',
            'PanelCard("compute wall", body=SafeText("compute wall"',
            'PanelCard("inverse bottleneck", body=SafeText("inverse bottleneck"',
        )
        for pattern in duplicate_patterns:
            self.assertNotIn(pattern, source, pattern)


if __name__ == "__main__":
    unittest.main()
