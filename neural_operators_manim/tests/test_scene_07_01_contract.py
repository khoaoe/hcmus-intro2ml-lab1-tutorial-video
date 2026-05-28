import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_PATH = Path(__file__).resolve().parents[1] / "src" / "scenes" / "scene_07_01_riemann_sum_computation_recipe.py"


def load_scene_module():
    spec = importlib.util.spec_from_file_location("scene_07_01_riemann_sum_computation_recipe", SCENE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Scene0701ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = load_scene_module()
        scene_class = module.Scene0701RiemannSumComputationRecipe

        self.assertEqual(scene_class.SCRIPT_ID, "7.1")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Riemann sum as a computation recipe")
        self.assertEqual(scene_class.SCRIPT_START, 42 * 60 + 30)
        self.assertEqual(scene_class.SCRIPT_END, 44 * 60 + 20)
        self.assertEqual(scene_class.SCENE_DURATION, 110.0)

    def test_required_visual_factories_exist(self):
        module = load_scene_module()

        for function_name in (
            "sample_function",
            "make_riemann_stage",
            "make_uniform_rectangles",
            "make_nonuniform_rectangles",
            "make_formula_sequence",
            "make_discretization_tags",
            "make_neural_operator_teaser",
        ):
            self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0701RiemannSumComputationRecipe.construct)

        self.assertIn("self.play_timed", source)
        self.assertIn("self.wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for label in (
            "known only at sample points",
            "height = f(x_i)",
            "width = \\Delta x",
            "true integral",
            "same integral",
            "different discretizations",
            "nonuniform samples",
            "local weight",
            r"\sum_i f(x_i)\,w_i \approx \int_D f(x)\,dx",
            r"\sum_j \kappa(y,x_j)\,a(x_j)\,w_j",
            "Neural operator layer",
        ):
            self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0701RiemannSumComputationRecipe.construct)

        for comment in (
            "42:30.0 -> local 0.0",
            "42:41.0 -> local 11.0",
            "42:54.0 -> local 24.0",
            "43:07.5 -> local 37.5",
            "43:08.5 -> local 38.5",
            "43:22.0 -> local 52.0",
            "43:37.0 -> local 67.0",
            "44:20.0 -> local 110.0",
        ):
            self.assertIn(comment, source, comment)

    def test_scene_stays_riemann_only_before_teaser(self):
        module = load_scene_module()
        source = inspect.getsource(module)

        for forbidden in (
            "finite difference",
            "derivative",
            r"\frac{f(x+h)-f(x)}{h}",
            "slope",
        ):
            self.assertNotIn(forbidden, source, forbidden)

    def test_nonuniform_rectangles_have_visibly_different_widths(self):
        module = load_scene_module()
        stage = module.make_riemann_stage()
        rectangles = module.make_nonuniform_rectangles(stage.axes, module.NONUNIFORM_EDGES)
        widths = [round(rect.width, 3) for rect in rectangles]

        self.assertGreater(max(widths) - min(widths), 0.35)

    def test_weighted_formula_column_does_not_overlap_plot(self):
        module = load_scene_module()
        stage = module.make_riemann_stage()
        rectangles = module.make_nonuniform_rectangles(stage.axes, module.NONUNIFORM_EDGES)
        formulas = module.make_formula_sequence()
        teaser = module.make_neural_operator_teaser()

        plot_right = rectangles.get_right()[0]
        self.assertGreater(formulas.weighted_sum.get_left()[0], plot_right + 0.18)

        formulas.weighted_sum.move_to(module.RIGHT_FORMULA_CENTER + module.FINAL_WEIGHTED_FORMULA_OFFSET)
        teaser.move_to(module.RIGHT_FORMULA_CENTER + module.TEASER_OFFSET)
        self.assertGreater(formulas.weighted_sum.get_left()[0], plot_right + 0.18)
        self.assertGreater(teaser.get_left()[0], plot_right + 0.18)

    def test_true_integral_label_exits_before_weight_labels_enter(self):
        module = load_scene_module()
        source = inspect.getsource(module.Scene0701RiemannSumComputationRecipe.construct)

        self.assertIn(
            "FadeOut(VGroup(fine_rectangles, alternate_rectangles, sample_dots, sample_chip, true_integral_label, recipe_callouts)",
            source,
        )


if __name__ == "__main__":
    unittest.main()
