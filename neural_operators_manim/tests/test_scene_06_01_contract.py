import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_06_01_definition_by_contrast.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_06_01_definition_by_contrast", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0601ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0601DefinitionByContrast

        self.assertEqual(scene_class.SCRIPT_ID, "6.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Definition by contrast")
        self.assertEqual(scene_class.SCRIPT_START, 35 * 60)
        self.assertEqual(scene_class.SCRIPT_END, 36 * 60 + 45)
        self.assertEqual(scene_class.SCENE_DURATION, 105.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "make_vector_column",
            "make_neural_network_diagram",
            "make_function_space_blob",
            "make_neural_operator_diagram",
            "make_question_cards",
            "make_input_chips",
            "make_output_chips",
            "make_final_focus",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0601DefinitionByContrast.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "Neural Network",
            "Neural Operator",
            r"f:\mathbb{R}^n\to\mathbb{R}^m",
            r"\mathcal{G}:\mathcal{A}\to\mathcal{U}",
            "vector x",
            "vector y",
            "given vector x → y?",
            "given function a → function u?",
            "coefficient field",
            "geometry field",
            "initial condition",
            "system state",
            "solution field",
            "future state",
            "wave",
            "pressure",
            "displacement",
            "infinite-dimensional object → infinite-dimensional object",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0601DefinitionByContrast.construct)

        for comment in (
            "35:00.0 -> local 0.0",
            "35:13.0 -> local 13.0",
            "35:28.0 -> local 28.0",
            "35:29.0 -> local 29.0",
            "35:43.0 -> local 43.0",
            "35:57.0 -> local 57.0",
            "36:12.0 -> local 72.0",
            "36:45.0 -> local 105.0",
        ):
            self.assertIn(comment, source, comment)

    def test_scene_does_not_introduce_later_operator_derivation(self):
        module = load_scene_module()
        source = inspect.getsource(module).lower()

        for forbidden in ("riemann", "kernel", "fno", "fourier neural operator"):
            self.assertNotIn(forbidden, source)

    def test_function_space_curves_remain_inside_blob_bounds(self):
        module = load_scene_module()
        diagram = module.make_neural_operator_diagram()

        for space in (diagram.space_a, diagram.space_u):
            blob = space.blob
            center = blob.get_center()
            rx = blob.width / 2 - 0.08
            ry = blob.height / 2 - 0.08
            for curve in space.curves:
                self.assertGreaterEqual(curve.get_left()[0], blob.get_left()[0] + 0.08)
                self.assertLessEqual(curve.get_right()[0], blob.get_right()[0] - 0.08)
                self.assertGreaterEqual(curve.get_bottom()[1], blob.get_bottom()[1] + 0.08)
                self.assertLessEqual(curve.get_top()[1], blob.get_top()[1] - 0.08)
                for point in curve.get_all_points():
                    normalized = ((point[0] - center[0]) / rx) ** 2 + ((point[1] - center[1]) / ry) ** 2
                    self.assertLessEqual(normalized, 1.0)

    def test_final_focus_arrow_connects_two_labeled_objects(self):
        module = load_scene_module()
        final_focus = module.make_final_focus()
        statement = final_focus[1]

        for attr in ("source_box", "target_box", "map_arrow"):
            self.assertTrue(hasattr(statement, attr), attr)
        self.assertLess(statement.source_box.get_right()[0], statement.map_arrow.get_start()[0] + 0.08)
        self.assertGreater(statement.target_box.get_left()[0], statement.map_arrow.get_end()[0] - 0.08)
        self.assertGreater(statement.map_arrow.width, 0.55)

    def test_final_focus_fades_out_question_cards(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0601DefinitionByContrast.construct)

        self.assertIn("FadeOut(question_cards", source)


if __name__ == "__main__":
    unittest.main()
