import importlib
import unittest


class Scene0002ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_00_02_roadmap")
        scene_class = module.Scene0002Roadmap

        self.assertEqual(scene_class.SCRIPT_ID, "0.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Roadmap")
        self.assertEqual(scene_class.SCRIPT_START, 42.0)
        self.assertEqual(scene_class.SCRIPT_END, 140.0)
        self.assertEqual(scene_class.SCENE_DURATION, 98.0)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module("src.scenes.scene_00_02_roadmap")
        scene_class = module.Scene0002Roadmap

        for method_name in (
            "make_timeline",
            "make_roadmap_nodes",
            "make_pixel_vector_icon",
            "make_solver_icon",
            "make_operator_icon",
            "make_kernel_icon",
            "make_architecture_icon",
            "make_domains_icon",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)


if __name__ == "__main__":
    unittest.main()
