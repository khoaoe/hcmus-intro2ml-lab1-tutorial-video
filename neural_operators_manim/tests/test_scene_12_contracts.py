import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_DIR = Path(__file__).resolve().parents[1] / "src" / "scenes"


SCENES = [
    {
        "module": "scene_12_01_accuracy_not_just_lower_loss",
        "class": "Scene1201AccuracyNotJustLowerLoss",
        "id": "12.1",
        "title": "Accuracy is not just lower loss",
        "start": 101 * 60 + 40,
        "end": 104 * 60 + 5,
        "duration": 145.0,
        "labels": ("MSE low", "rare event missed", "anomaly correlation", "energy spectrum", "drag coefficient", "mass conservation", "PDE residual", "calibration error", "problem formulation"),
        "comments": ("1:41:40.0 -> local 0.0", "1:41:53.0 -> local 13.0", "1:42:06.5 -> local 26.5", "1:42:19.0 -> local 39.0", "1:42:20.0 -> local 40.0", "1:42:35.5 -> local 55.5", "1:42:52.0 -> local 72.0", "1:43:13.0 -> local 93.0", "1:44:05.0 -> local 145.0"),
    },
    {
        "module": "scene_12_02_discretization_chaos_uncertainty",
        "class": "Scene1202DiscretizationChaosUncertainty",
        "id": "12.2",
        "title": "Discretization, chaos, uncertainty",
        "start": 104 * 60 + 5,
        "end": 107 * 60 + 20,
        "duration": 195.0,
        "labels": ("mesh change", "error behavior", "nearby initial states diverge", "distribution, not one line", "calibrated uncertainty", "probabilistic NO", "conformal prediction", "sampling in function space"),
        "comments": ("1:44:05.0 -> local 0.0", "1:44:19.0 -> local 14.0", "1:44:33.0 -> local 28.0", "1:44:48.0 -> local 43.0", "1:44:49.0 -> local 44.0", "1:45:04.0 -> local 59.0", "1:45:19.5 -> local 74.5", "1:45:35.0 -> local 90.0", "1:45:51.0 -> local 106.0", "1:46:13.0 -> local 128.0", "1:47:20.0 -> local 195.0"),
    },
    {
        "module": "scene_12_03_scaling_multiple_datasets",
        "class": "Scene1203ScalingMultipleDatasets",
        "id": "12.3",
        "title": "Scaling and multiple datasets",
        "start": 107 * 60 + 20,
        "end": 110 * 60 + 20,
        "duration": 180.0,
        "labels": ("weather", "CFD", "seismic", "materials", "metadata", "geometry", "codomain attention", "operator foundation model", "function spaces", "uncertainty"),
        "comments": ("1:47:20.0 -> local 0.0", "1:47:33.0 -> local 13.0", "1:47:46.5 -> local 26.5", "1:48:00.0 -> local 40.0", "1:48:13.5 -> local 53.5", "1:48:14.5 -> local 54.5", "1:48:29.5 -> local 69.5", "1:48:45.0 -> local 85.0", "1:49:01.0 -> local 101.0", "1:49:21.0 -> local 121.0", "1:50:20.0 -> local 180.0"),
    },
    {
        "module": "scene_12_04_physics_domain_knowledge",
        "class": "Scene1204PhysicsDomainKnowledge",
        "id": "12.4",
        "title": "Incorporating physics and domain knowledge",
        "start": 110 * 60 + 20,
        "end": 113 * 60 + 5,
        "duration": 165.0,
        "labels": ("flexibility", "physics prior", "symmetry", "conservation", "boundary", "local kernels", "PDE loss", "ML", "applied math", "domain expert"),
        "comments": ("1:50:20.0 -> local 0.0", "1:50:33.0 -> local 13.0", "1:50:46.0 -> local 26.0", "1:51:00.0 -> local 40.0", "1:51:01.0 -> local 41.0", "1:51:16.0 -> local 56.0", "1:51:33.0 -> local 73.0", "1:51:50.0 -> local 90.0", "1:52:10.0 -> local 110.0", "1:53:05.0 -> local 165.0"),
    },
    {
        "module": "scene_12_05_honest_state_of_field",
        "class": "Scene1205HonestStateOfField",
        "id": "12.5",
        "title": "The honest state of the field",
        "start": 113 * 60 + 5,
        "end": 115 * 60 + 20,
        "duration": 135.0,
        "labels": ("open problems", "accuracy", "metrics", "scaling", "OOD behavior", "uncertainty", "discretization", "weather", "CFD", "geophysics"),
        "comments": ("1:53:05.0 -> local 0.0", "1:53:18.0 -> local 13.0", "1:53:32.0 -> local 27.0", "1:53:46.0 -> local 41.0", "1:53:47.0 -> local 42.0", "1:54:04.0 -> local 59.0", "1:54:21.0 -> local 76.0", "1:54:39.0 -> local 94.0", "1:55:20.0 -> local 135.0"),
    },
]


def load_scene_module(module_name):
    path = SCENE_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Section12SceneContractTest(unittest.TestCase):
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
