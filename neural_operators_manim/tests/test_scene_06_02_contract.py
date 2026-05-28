import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_06_02_three_desired_properties.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_06_02_three_desired_properties", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0602ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0602ThreeDesiredProperties

        self.assertEqual(scene_class.SCRIPT_ID, "6.2")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Three desired properties")
        self.assertEqual(scene_class.SCRIPT_START, 36 * 60 + 45)
        self.assertEqual(scene_class.SCRIPT_END, 38 * 60 + 40)
        self.assertEqual(scene_class.SCENE_DURATION, 115.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_property_cards",
            "make_input_discretization_visual",
            "make_output_query_visual",
            "make_refinement_limit_visual",
            "make_architecture_constraints",
            "make_matrix_vs_continuum_view",
            "make_neural_layer_zoom",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0602ThreeDesiredProperties.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_property_card_contents_fade_in_without_card_morph(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0602ThreeDesiredProperties.construct)

        self.assertIn("FadeIn(filled_cards[0].body", source)
        self.assertIn("FadeIn(filled_cards[1].body", source)
        self.assertIn("FadeIn(filled_cards[2].body", source)
        self.assertNotIn("ReplacementTransform(empty_cards[0]", source)
        self.assertNotIn("ReplacementTransform(empty_cards[1]", source)
        self.assertNotIn("ReplacementTransform(empty_cards[2]", source)

    def test_required_script_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "Three properties of a good Neural Operator",
            "Input: many discretizations",
            "Output: query anywhere",
            "Refinement: stable limit",
            "coarse grid",
            "fine grid",
            "irregular",
            "u(y_1)",
            "u(y_2)",
            "u(y_3)",
            "Architecture constraints",
            "coordinate-aware",
            "quadrature-aware",
            "output as function u(y)",
            "continuum operation",
            "K_ij on fixed grid",
            "fixed index",
            "integral operator",
            "Next: view this layer as a Riemann sum",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0602ThreeDesiredProperties.construct)

        for comment in (
            "36:45.0 -> local 0.0",
            "36:55.5 -> local 10.5",
            "37:06.5 -> local 21.5",
            "37:18.0 -> local 33.0",
            "37:33.0 -> local 48.0",
            "37:34.0 -> local 49.0",
            "37:48.5 -> local 63.5",
            "38:02.5 -> local 77.5",
            "38:40.0 -> local 115.0",
        ):
            self.assertIn(comment, source, comment)

    def test_scene_avoids_full_integral_derivation(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for forbidden in (
            r"\int",
            r"\sum",
            "Riemann rectangles",
            "Fourier",
            "FNO",
        ):
            self.assertNotIn(forbidden, source, forbidden)

    def test_layer_zoom_arrow_connects_real_objects(self):
        module = load_scene_module()
        layer = module.make_neural_layer_zoom()

        for attr in ("input_column", "matrix_block", "output_column", "left_arrow", "right_arrow"):
            self.assertTrue(hasattr(layer, attr), attr)
        self.assertLess(layer.input_column.get_right()[0], layer.left_arrow.get_start()[0] + 0.08)
        self.assertGreater(layer.matrix_block.get_left()[0], layer.left_arrow.get_end()[0] - 0.08)
        self.assertLess(layer.matrix_block.get_right()[0], layer.right_arrow.get_start()[0] + 0.08)
        self.assertGreater(layer.output_column.get_left()[0], layer.right_arrow.get_end()[0] - 0.08)

    def test_continuum_panel_curves_stay_inside_oval(self):
        module = load_scene_module()
        view = module.make_matrix_vs_continuum_view()

        self.assertTrue(hasattr(view, "continuum_blob"))
        self.assertTrue(hasattr(view, "continuum_curves"))
        blob = view.continuum_blob
        center = blob.get_center()
        rx = blob.width / 2 - 0.05
        ry = blob.height / 2 - 0.05
        for curve in view.continuum_curves:
            self.assertGreaterEqual(curve.get_left()[0], blob.get_left()[0] + 0.04)
            self.assertLessEqual(curve.get_right()[0], blob.get_right()[0] - 0.04)
            self.assertGreaterEqual(curve.get_bottom()[1], blob.get_bottom()[1] + 0.04)
            self.assertLessEqual(curve.get_top()[1], blob.get_top()[1] - 0.04)
            for point in curve.get_all_points():
                normalized = ((point[0] - center[0]) / rx) ** 2 + ((point[1] - center[1]) / ry) ** 2
                self.assertLessEqual(normalized, 1.0)

    def test_refinement_prediction_curves_stay_inside_meshes(self):
        module = load_scene_module()
        visual = module.make_refinement_limit_visual()

        self.assertTrue(hasattr(visual, "meshes"))
        self.assertTrue(hasattr(visual, "prediction_curves"))
        for mesh, curve in zip(visual.meshes, visual.prediction_curves):
            self.assertGreaterEqual(curve.get_left()[0], mesh.get_left()[0] + 0.02)
            self.assertLessEqual(curve.get_right()[0], mesh.get_right()[0] - 0.02)
            self.assertGreaterEqual(curve.get_bottom()[1], mesh.get_bottom()[1] + 0.02)
            self.assertLessEqual(curve.get_top()[1], mesh.get_top()[1] - 0.02)


if __name__ == "__main__":
    unittest.main()
