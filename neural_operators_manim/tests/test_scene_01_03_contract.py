import importlib
import inspect
import unittest


class Scene0103ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_01_03_university_departments_to_function_data"
        )
        scene_class = module.Scene0103UniversityDepartmentsToFunctionData

        self.assertEqual(scene_class.SCRIPT_ID, "1.3")
        self.assertEqual(
            scene_class.SCRIPT_TITLE,
            "From university departments to function data",
        )
        self.assertEqual(scene_class.SCRIPT_START, 320.0)
        self.assertEqual(scene_class.SCRIPT_END, 440.0)
        self.assertEqual(scene_class.SCENE_DURATION, 120.0)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_01_03_university_departments_to_function_data"
        )
        scene_class = module.Scene0103UniversityDepartmentsToFunctionData

        for method_name in (
            "make_campus_map",
            "make_department_labels",
            "make_field_visuals",
            "make_mesh_overlay",
            "make_zoomed_grid",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_01_03_university_departments_to_function_data"
        )

        for class_name in (
            "CampusMap",
            "DepartmentLabels",
            "FieldVisuals",
            "MeshOverlay",
            "ZoomedGrid",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module(
            "src.scenes.scene_01_03_university_departments_to_function_data"
        )
        source = inspect.getsource(
            module.Scene0103UniversityDepartmentsToFunctionData.construct
        )

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("pad_to", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_01_03_university_departments_to_function_data"
        )
        source = inspect.getsource(module)

        for label in (
            "Mechanical Engineering",
            "Geophysics",
            "Chemistry / Medicine",
            "Climate Science",
            "Materials Science",
            "not image",
            "function",
            "looks like an image",
            "but behaves like a function",
            "change mesh",
            "query anywhere",
            "differentiate",
            "integrate",
            "Euclidean vectors",
            "Function Spaces",
            "same visual pixels, different mathematical object",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
