import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_06_03_the_suspense_line.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_06_03_the_suspense_line", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0603ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0603TheSuspenseLine

        self.assertEqual(scene_class.SCRIPT_ID, "6.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "The suspense line")
        self.assertEqual(scene_class.SCRIPT_START, 38 * 60 + 40)
        self.assertEqual(scene_class.SCRIPT_END, 42 * 60 + 30)
        self.assertEqual(scene_class.SCENE_DURATION, 230.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_neural_layer_closeup",
            "make_formula_dump_warning",
            "make_future_architecture_chips",
            "make_tool_cards",
            "make_riemann_panel",
            "make_finite_difference_panel",
            "make_bridge_graphic",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0603TheSuspenseLine.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "The key bridge",
            "Neural network layer → integral operator",
            "not first",
            "Build it step by step",
            "integral operator",
            "GNO",
            "FNO",
            "Transformer NO",
            "Why do these architectures make sense?",
            "Integral approximation",
            "Derivative approximation",
            "Old tools, new role",
            "finite difference",
            "function continuum",
            "sampled tensor computation",
            "Next: Riemann sum",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0603TheSuspenseLine.construct)

        for comment in (
            "38:40.0 -> local 0.0",
            "38:52.0 -> local 12.0",
            "39:03.5 -> local 23.5",
            "39:15.0 -> local 35.0",
            "39:16.0 -> local 36.0",
            "39:29.5 -> local 49.5",
            "39:44.0 -> local 64.0",
            "39:57.0 -> local 77.0",
            "40:13.0 -> local 93.0",
            "40:28.0 -> local 108.0",
            "40:45.0 -> local 125.0",
            "42:30.0 -> local 230.0",
        ):
            self.assertIn(comment, source, comment)

    def test_scene_avoids_neural_operator_kernel_derivation(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for forbidden in (
            r"K(x,y)",
            r"\kappa",
            "kernel",
            "Fourier Neural Operator",
        ):
            self.assertNotIn(forbidden, source, forbidden)

    def test_bridge_arrow_connects_continuum_to_tensor(self):
        module = load_scene_module()
        bridge = module.make_bridge_graphic()

        for attr in ("continuum", "tensor", "bridge_arrow"):
            self.assertTrue(hasattr(bridge, attr), attr)
        self.assertLess(bridge.continuum.get_right()[0], bridge.bridge_arrow.get_start()[0] + 0.08)
        self.assertGreater(bridge.tensor.get_left()[0], bridge.bridge_arrow.get_end()[0] - 0.08)

    def test_riemann_rectangles_stay_inside_axes_window(self):
        module = load_scene_module()
        panel = module.make_riemann_panel()

        self.assertTrue(hasattr(panel, "rectangles"))
        self.assertTrue(hasattr(panel, "plot_window"))
        for rect in panel.rectangles:
            self.assertGreaterEqual(rect.get_left()[0], panel.plot_window.get_left()[0] - 0.02)
            self.assertLessEqual(rect.get_right()[0], panel.plot_window.get_right()[0] + 0.02)
            self.assertGreaterEqual(rect.get_bottom()[1], panel.plot_window.get_bottom()[1] - 0.02)
            self.assertLessEqual(rect.get_top()[1], panel.plot_window.get_top()[1] + 0.02)


if __name__ == "__main__":
    unittest.main()
