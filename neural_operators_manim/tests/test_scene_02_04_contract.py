import importlib
import unittest


class Scene0204ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module("src.scenes.scene_02_04_the_core_warning")
        scene_class = module.Scene0204TheCoreWarning

        self.assertEqual(scene_class.SCRIPT_ID, "2.4")
        self.assertEqual(scene_class.SCRIPT_TITLE, "The core warning")
        self.assertEqual(scene_class.SCRIPT_START, 12 * 60 + 55)
        self.assertEqual(scene_class.SCRIPT_END, 15 * 60 + 45)
        self.assertEqual(scene_class.SCENE_DURATION, 170.0)


if __name__ == "__main__":
    unittest.main()
