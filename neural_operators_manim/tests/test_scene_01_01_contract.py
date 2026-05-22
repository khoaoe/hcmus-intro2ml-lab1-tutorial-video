import importlib
import unittest


class Scene0101ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_01_01_finite_dimensional_comfort_zone"
        )
        scene_class = module.Scene0101FiniteDimensionalComfortZone

        self.assertEqual(scene_class.SCRIPT_ID, "1.1")
        self.assertEqual(scene_class.SCRIPT_START, 140.0)
        self.assertEqual(scene_class.SCRIPT_END, 215.0)
        self.assertEqual(scene_class.SCENE_DURATION, 75.0)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_01_01_finite_dimensional_comfort_zone"
        )
        scene_class = module.Scene0101FiniteDimensionalComfortZone

        for method_name in (
            "make_matrix_grid",
            "make_token_sequence",
            "make_waveform_samples",
            "make_neural_network_graph",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)


if __name__ == "__main__":
    unittest.main()
