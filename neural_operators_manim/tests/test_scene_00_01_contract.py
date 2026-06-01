import importlib
import unittest


class Scene0001ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_00_01_from_pixels_to_fields"
        )
        scene_class = module.Scene0001FromPixelsToFields

        self.assertEqual(scene_class.SCRIPT_ID, "0.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "From pixels to fields")
        self.assertEqual(scene_class.SCRIPT_START, 0.0)
        self.assertEqual(scene_class.SCRIPT_END, 42.0)
        self.assertEqual(scene_class.SCENE_DURATION, 42.0)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_00_01_from_pixels_to_fields"
        )
        scene_class = module.Scene0001FromPixelsToFields

        for method_name in (
            "make_pixel_grid",
            "make_sphere_field",
            "make_continuous_surface",
            "make_transition_arrow",
            "make_vector_formula",
            "make_operator_formula",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)


if __name__ == "__main__":
    unittest.main()
