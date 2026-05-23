import importlib
import inspect
import unittest


class Scene0102ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_01_02_cv_nlp_habits")
        scene_class = module.Scene0102CVNLPHabits

        self.assertEqual(scene_class.SCRIPT_ID, "1.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Why CV/NLP shaped our habits")
        self.assertEqual(scene_class.SCRIPT_START, 215.0)
        self.assertEqual(scene_class.SCRIPT_END, 320.0)
        self.assertEqual(scene_class.SCENE_DURATION, 105.0)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_01_02_cv_nlp_habits")
        scene_class = module.Scene0102CVNLPHabits

        for method_name in (
            "make_metric_cards",
            "make_physics_constraint_cards",
            "make_warning_stamp",
            "make_architecture_chips",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module("src.scenes.scene_01_02_cv_nlp_habits")
        source = inspect.getsource(module.Scene0102CVNLPHabits.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("pad_to", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module("src.scenes.scene_01_02_cv_nlp_habits")
        source = inspect.getsource(module)

        for label in (
            "Dataset",
            "Benchmark",
            "Loss",
            "Metric",
            "Accuracy",
            "FID",
            "Inception Score",
            "CLIP Score",
            "L1 / L2",
            "RMSE",
            "Weather",
            "Seismology",
            "Molecular dynamics",
            "Fluid simulation",
            "conservation",
            "derivatives",
            "integrals",
            "PDE residual",
            "boundary conditions",
            "domain expert checks",
            "Not plug-and-play",
            "Function Spaces",
        ):
            self.assertIn(label, source, label)

    def test_warning_stamp_is_horizontal_and_cross_targets_wall_only(self):
        layout = importlib.import_module("src.common.layout")
        scene_module = importlib.import_module("src.scenes.scene_01_02_cv_nlp_habits")
        stamp_source = inspect.getsource(layout.make_warning_stamp)
        construct_source = inspect.getsource(scene_module.Scene0102CVNLPHabits.construct)

        self.assertNotIn("stamp.rotate", stamp_source)
        self.assertIn("Cross(pipeline[1][0]", construct_source)
        self.assertNotIn("Cross(pipeline[1],", construct_source)


if __name__ == "__main__":
    unittest.main()
