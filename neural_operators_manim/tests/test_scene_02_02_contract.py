import importlib
import inspect
import unittest

from manim import ThreeDScene


class Scene0202ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_02_02_seismology_functions_inside_earth"
        )
        scene_class = module.Scene0202SeismologyFunctionsInsideEarth

        self.assertEqual(scene_class.SCRIPT_ID, "2.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Seismology: functions inside Earth")
        self.assertEqual(scene_class.SCRIPT_START, 545.0)
        self.assertEqual(scene_class.SCRIPT_END, 645.0)
        self.assertEqual(scene_class.SCENE_DURATION, 100.0)

    def test_timed_three_d_scene_inherits_three_d_scene(self):
        timing = importlib.import_module("src.common.timing")

        self.assertTrue(hasattr(timing, "TimedThreeDScene"))
        self.assertTrue(issubclass(timing.TimedThreeDScene, ThreeDScene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedThreeDScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_02_02_seismology_functions_inside_earth"
        )
        scene_class = module.Scene0202SeismologyFunctionsInsideEarth

        for method_name in (
            "make_velocity_volume",
            "make_wavefronts",
            "make_fault_and_source",
            "make_sensor_array",
            "make_waveform_panel",
            "make_derivative_card",
            "make_inverse_problem_diagram",
            "make_surrogate_panel",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_construct_uses_timestamp_driven_scene_helpers_and_3d_camera(self):
        module = importlib.import_module(
            "src.scenes.scene_02_02_seismology_functions_inside_earth"
        )
        source = inspect.getsource(module.Scene0202SeismologyFunctionsInsideEarth.construct)

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
            "src.scenes.scene_02_02_seismology_functions_inside_earth"
        )
        source = inspect.getsource(module)

        for label in (
            "Seismology",
            "functions inside Earth",
            "subsurface velocity field",
            "earthquake source",
            "wave propagation in 3D + time",
            "physics lives in spatial + temporal derivatives",
            "surface observations",
            "inverse problem",
            "hidden volume",
            "fast differentiable surrogate",
            "inverse loop",
            "function-to-function surrogate for inverse science",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
