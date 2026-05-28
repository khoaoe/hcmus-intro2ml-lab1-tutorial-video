import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_07_02_finite_difference_local_physics_probe.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_07_02_finite_difference_local_physics_probe", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0702ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0702FiniteDifferenceLocalPhysicsProbe

        self.assertEqual(scene_class.SCRIPT_ID, "7.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Finite difference as local physics probe")
        self.assertEqual(scene_class.SCRIPT_START, 44 * 60 + 20)
        self.assertEqual(scene_class.SCRIPT_END, 46 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 120.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "sample_function",
            "sample_derivative",
            "make_derivative_stage",
            "make_tangent_probe",
            "make_secant_probe",
            "make_pde_residual_bubble",
            "make_output_function_panel",
            "make_integral_derivative_cards",
            "make_neural_operator_bridge",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0702FiniteDifferenceLocalPhysicsProbe.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "derivative = local slope",
            r"\frac{a(x_{i+1})-a(x_i)}{\Delta x}",
            "vertical difference",
            "horizontal spacing",
            "finer mesh -> better derivative approximation",
            r"R[u] = u_t - F(u,\nabla u,\nabla^2 u)",
            "derivative terms",
            "output must support meaningful derivatives",
            "flat raster",
            "insufficient for physics checks",
            "integral = global aggregation",
            "derivative = local physics probe",
            "Neural Operator layer",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0702FiniteDifferenceLocalPhysicsProbe.construct)

        for comment in (
            "44:20.0 -> local 0.0",
            "44:31.5 -> local 11.5",
            "44:43.0 -> local 23.0",
            "44:56.0 -> local 36.0",
            "44:57.0 -> local 37.0",
            "45:10.5 -> local 50.5",
            "45:24.5 -> local 64.5",
            "45:41.5 -> local 81.5",
            "46:20.0 -> local 120.0",
        ):
            self.assertIn(comment, source, comment)

    def test_scene_avoids_section_8_derivation(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for forbidden in (
            r"\kappa(y,x_j)",
            "matrix weight",
            "basic neural network layer",
            "Riemann",
        ):
            self.assertNotIn(forbidden, source, forbidden)

    def test_secant_points_converge_toward_tangent_spacing(self):
        module = load_scene_module()
        coarse = module.make_secant_probe(module.make_derivative_stage().axes, module.X0, module.COARSE_H)
        fine = module.make_secant_probe(module.make_derivative_stage().axes, module.X0, module.FINE_H)

        self.assertGreater(coarse.dx, fine.dx)
        self.assertLess(fine.dx, 0.5)

    def test_secant_callout_labels_do_not_overlap_plot(self):
        module = load_scene_module()
        stage = module.make_derivative_stage()
        probe = module.make_secant_probe(stage.axes, module.X0, module.COARSE_H)

        labels = probe.measure_labels
        self.assertGreater(labels.get_left()[0], stage.axes.get_right()[0] + 0.25)
        self.assertLess(labels.get_top()[1], probe.formula.get_bottom()[1] - 0.08)

    def test_measurement_callouts_clear_before_refinement_note_enters(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0702FiniteDifferenceLocalPhysicsProbe.construct)

        self.assertIn("clear_measurement_callouts_before_refinement_note", source)
        clear_start = source.index("clear_measurement_callouts_before_refinement_note")
        note_start = source.index("show_refinement_message")
        self.assertLess(clear_start, note_start)
        self.assertLess(source.index("FadeOut(secant_probe.measure_labels"), source.index("FadeIn(refinement_note"))

    def test_later_transitions_do_not_reintroduce_hidden_secant_callouts(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0702FiniteDifferenceLocalPhysicsProbe.construct)

        self.assertIn("fine_secant_visible", source)
        self.assertNotIn("VGroup(stage, tangent_probe, fine_secant_probe,", source)

    def test_final_bridge_cards_do_not_overlap_layer(self):
        module = load_scene_module()
        bridge = module.make_neural_operator_bridge()

        self.assertLess(bridge.integral_card.get_right()[0], bridge.layer.get_left()[0] - 0.10)
        self.assertGreater(bridge.derivative_card.get_left()[0], bridge.layer.get_right()[0] + 0.10)


if __name__ == "__main__":
    unittest.main()
