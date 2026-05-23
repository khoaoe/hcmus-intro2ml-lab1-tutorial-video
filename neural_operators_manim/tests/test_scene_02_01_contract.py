import importlib
import inspect
import unittest

from manim import ThreeDScene


class Scene0201ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_02_01_weather_functions_on_sphere"
        )
        scene_class = module.Scene0201WeatherFunctionsOnSphere

        self.assertEqual(scene_class.SCRIPT_ID, "2.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Weather: functions on a sphere")
        self.assertEqual(scene_class.SCRIPT_START, 440.0)
        self.assertEqual(scene_class.SCRIPT_END, 545.0)
        self.assertEqual(scene_class.SCENE_DURATION, 105.0)

    def test_timed_three_d_scene_inherits_three_d_scene(self):
        timing = importlib.import_module("src.common.timing")

        self.assertTrue(hasattr(timing, "TimedThreeDScene"))
        self.assertTrue(issubclass(timing.TimedThreeDScene, ThreeDScene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedThreeDScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_02_01_weather_functions_on_sphere"
        )
        scene_class = module.Scene0201WeatherFunctionsOnSphere

        for method_name in (
            "make_weather_sphere",
            "make_variable_list",
            "make_forecast_operator",
            "make_pixel_grid",
            "make_physics_glyphs",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_construct_uses_timestamp_driven_scene_helpers_and_3d_camera(self):
        module = importlib.import_module(
            "src.scenes.scene_02_01_weather_functions_on_sphere"
        )
        source = inspect.getsource(module.Scene0201WeatherFunctionsOnSphere.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("pad_to", source)
        self.assertIn("set_camera_orientation", source)
        self.assertIn("begin_ambient_camera_rotation", source)
        self.assertIn("add_fixed_in_frame_mobjects", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_02_01_weather_functions_on_sphere"
        )
        source = inspect.getsource(module)

        for label in (
            "Weather / Climate",
            "Domain",
            "sphere",
            "temperature",
            "wind velocity",
            "humidity",
            "pressure",
            "precipitation",
            "vorticity",
            "vector-valued function",
            "today",
            "tomorrow",
            "gradient",
            "divergence",
            "energy",
            "flux",
            "Output must remain a function",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
