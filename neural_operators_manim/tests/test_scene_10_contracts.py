import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_DIR = Path(__file__).resolve().parents[1] / "src" / "scenes"


SCENES = [
    {
        "module": "scene_10_01_graph_neural_operator",
        "class": "Scene1001GraphNeuralOperator",
        "id": "10.1",
        "title": "Graph Neural Operator: learn the kernel directly",
        "start": 67 * 60 + 40,
        "end": 70 * 60 + 10,
        "duration": 150.0,
        "factories": ("make_gno_stage", "make_refinement_strip"),
        "labels": (
            "kernel NN",
            "kernel neural operator",
            "quadrature weight",
            "graph comes from domain metric",
            "local radius",
            "global kernel",
            "compute grows with edges",
        ),
        "comments": (
            "1:07:40.0 -> local 0.0",
            "1:07:53.5 -> local 13.5",
            "1:08:08.0 -> local 28.0",
            "1:08:09.0 -> local 29.0",
            "1:08:21.5 -> local 41.5",
            "1:08:36.0 -> local 56.0",
            "1:08:50.0 -> local 70.0",
            "1:09:07.0 -> local 87.0",
            "1:10:10.0 -> local 150.0",
        ),
    },
    {
        "module": "scene_10_02_basis_projection",
        "class": "Scene1002BasisProjection",
        "id": "10.2",
        "title": "Basis projection: integrate by changing representation",
        "start": 70 * 60 + 10,
        "end": 72 * 60 + 20,
        "duration": 130.0,
        "factories": ("make_basis_functions", "make_basis_pipeline", "make_basis_menu"),
        "labels": (
            "basis functions",
            "coefficient space",
            "residual skip",
            "Fourier",
            "wavelet",
            "Laplacian eigenbasis",
            "basis encodes geometry",
        ),
        "comments": (
            "1:10:10.0 -> local 0.0",
            "1:10:22.0 -> local 12.0",
            "1:10:34.5 -> local 24.5",
            "1:10:47.0 -> local 37.0",
            "1:10:48.0 -> local 38.0",
            "1:11:03.5 -> local 53.5",
            "1:11:18.0 -> local 68.0",
            "1:11:36.0 -> local 86.0",
            "1:12:20.0 -> local 130.0",
        ),
    },
    {
        "module": "scene_10_03_fourier_neural_operator",
        "class": "Scene1003FourierNeuralOperator",
        "id": "10.3",
        "title": "Fourier Neural Operator",
        "start": 72 * 60 + 20,
        "end": 75 * 60 + 40,
        "duration": 200.0,
        "factories": ("make_fno_pipeline", "make_sharp_feature_demo"),
        "labels": (
            "regular grid field",
            "selected modes",
            "learned mode weights",
            "inverse FFT",
            "sharp boundary",
            "semi-generalized convolution",
            "not a magic continuum guarantee",
        ),
        "comments": (
            "1:12:20.0 -> local 0.0",
            "1:12:31.5 -> local 11.5",
            "1:12:45.0 -> local 25.0",
            "1:12:58.0 -> local 38.0",
            "1:12:59.0 -> local 39.0",
            "1:13:13.5 -> local 53.5",
            "1:13:30.0 -> local 70.0",
            "1:13:46.0 -> local 86.0",
            "1:14:02.0 -> local 102.0",
            "1:14:20.0 -> local 120.0",
            "1:14:36.0 -> local 136.0",
            "1:14:53.0 -> local 153.0",
            "1:15:40.0 -> local 200.0",
        ),
    },
    {
        "module": "scene_10_04_numerical_analysis_family",
        "class": "Scene1004NumericalAnalysisFamily",
        "id": "10.4",
        "title": "Numerical-analysis family: quadrature, Galerkin, multigrid, U-NO",
        "start": 75 * 60 + 40,
        "end": 78 * 60 + 20,
        "duration": 160.0,
        "factories": ("make_quadrature_panel", "make_galerkin_panel", "make_vcycle_panel", "make_uno_panel", "make_numerical_family_grid"),
        "labels": (
            "quadrature",
            "Galerkin",
            "multigrid",
            "U-NO",
            "operator-learning rewrite",
            "copy finite ML",
        ),
        "comments": (
            "1:15:40.0 -> local 0.0",
            "1:15:53.0 -> local 13.0",
            "1:16:06.0 -> local 26.0",
            "1:16:18.0 -> local 38.0",
            "1:16:32.0 -> local 52.0",
            "1:16:49.0 -> local 69.0",
            "1:17:05.0 -> local 85.0",
            "1:17:19.0 -> local 99.0",
            "1:18:20.0 -> local 160.0",
        ),
    },
    {
        "module": "scene_10_05_transformer_neural_operator",
        "class": "Scene1005TransformerNeuralOperator",
        "id": "10.5",
        "title": "Transformer Neural Operator",
        "start": 78 * 60 + 20,
        "end": 80 * 60 + 30,
        "duration": 130.0,
        "factories": ("make_attention_operator_stage", "make_grid_weight_comparison"),
        "labels": (
            "attention weights",
            "Q(x)",
            "K(x)",
            "V(x)",
            "regular grid",
            "irregular grid",
            "measure factors",
            "function space",
        ),
        "comments": (
            "1:18:20.0 -> local 0.0",
            "1:18:33.0 -> local 13.0",
            "1:18:46.0 -> local 26.0",
            "1:19:00.0 -> local 40.0",
            "1:19:01.0 -> local 41.0",
            "1:19:17.0 -> local 57.0",
            "1:19:31.0 -> local 71.0",
            "1:19:48.0 -> local 88.0",
            "1:20:30.0 -> local 130.0",
        ),
    },
    {
        "module": "scene_10_06_codomain_attention",
        "class": "Scene1006CodomainAttention",
        "id": "10.6",
        "title": "Codomain attention: variables as function tokens",
        "start": 80 * 60 + 30,
        "end": 82 * 60 + 30,
        "duration": 120.0,
        "factories": ("make_variable_function_cards", "make_codomain_attention_graph"),
        "labels": (
            "temperature",
            "pressure",
            "velocity",
            "humidity",
            "different variable subsets",
            "function token",
            "VSPE",
            "scientific foundation models",
        ),
        "comments": (
            "1:20:30.0 -> local 0.0",
            "1:20:43.0 -> local 13.0",
            "1:20:56.0 -> local 26.0",
            "1:21:10.0 -> local 40.0",
            "1:21:11.0 -> local 41.0",
            "1:21:26.5 -> local 56.5",
            "1:21:43.0 -> local 73.0",
            "1:22:00.0 -> local 90.0",
            "1:22:30.0 -> local 120.0",
        ),
    },
    {
        "module": "scene_10_07_local_differential_kernels",
        "class": "Scene1007LocalDifferentialKernels",
        "id": "10.7",
        "title": "Local and differential kernels",
        "start": 82 * 60 + 30,
        "end": 84 * 60 + 10,
        "duration": 100.0,
        "factories": ("make_differential_stage",),
        "labels": (
            "CNN stencil",
            "derivative stencil",
            "refined grid",
            "forcing / residual",
            "1 / h",
            "1 / (h/2)",
            "resolution-aware limit",
            "local physics",
        ),
        "comments": (
            "1:22:30.0 -> local 0.0",
            "1:22:43.5 -> local 13.5",
            "1:22:56.0 -> local 26.0",
            "1:23:09.5 -> local 39.5",
            "1:23:10.5 -> local 40.5",
            "1:23:26.0 -> local 56.0",
            "1:23:41.0 -> local 71.0",
            "1:24:10.0 -> local 100.0",
        ),
    },
]


def load_scene_module(module_name):
    path = SCENE_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Section10SceneContractTest(unittest.TestCase):
    def test_scene_classes_expose_script_timing_contract(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                scene_class = getattr(module, spec["class"])

                self.assertEqual(scene_class.SCRIPT_ID, spec["id"])
                self.assertEqual(scene_class.SCRIPT_TITLE, spec["title"])
                self.assertEqual(scene_class.SCRIPT_START, spec["start"])
                self.assertEqual(scene_class.SCRIPT_END, spec["end"])
                self.assertEqual(scene_class.SCENE_DURATION, spec["duration"])

    def test_required_visual_factories_exist(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                for function_name in spec["factories"]:
                    self.assertTrue(hasattr(module, function_name), function_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(getattr(module, spec["class"]).construct)

                self.assertIn("self.play_timed", source)
                self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
                self.assertNotIn("self.play(", source)
                self.assertNotIn("self.wait(", source)

    def test_required_labels_are_present(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(module)

                for label in spec["labels"]:
                    self.assertIn(label, source, label)

    def test_global_timestamps_are_documented_as_local_comments(self):
        for spec in SCENES:
            with self.subTest(scene=spec["id"]):
                module = load_scene_module(spec["module"])
                source = inspect.getsource(getattr(module, spec["class"]).construct)

                for comment in spec["comments"]:
                    self.assertIn(comment, source, comment)


if __name__ == "__main__":
    unittest.main()
