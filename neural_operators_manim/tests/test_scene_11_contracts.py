import importlib.util
import inspect
import unittest
from pathlib import Path


SCENE_DIR = Path(__file__).resolve().parents[1] / "src" / "scenes"


SCENES = [
    {
        "module": "scene_11_01_domains_not_applications",
        "class": "Scene1101DomainsNotApplications",
        "id": "11.1",
        "title": "These are domains, not applications",
        "start": 84 * 60 + 10,
        "end": 86 * 60 + 10,
        "duration": 120.0,
        "factories": ("make_domain_pillars", "make_ecosystem_labels"),
        "labels": ("weather", "seismology", "CFD", "molecules", "problem setup", "validation", "not auto-solve every PDE"),
        "comments": ("1:24:10.0 -> local 0.0", "1:24:23.0 -> local 13.0", "1:24:35.0 -> local 25.0", "1:24:48.0 -> local 38.0", "1:24:49.0 -> local 39.0", "1:25:04.0 -> local 54.0", "1:25:19.5 -> local 79.5", "1:26:10.0 -> local 120.0"),
    },
    {
        "module": "scene_11_02_weather_forecast",
        "class": "Scene1102WeatherForecast",
        "id": "11.2",
        "title": "Weather forecast",
        "start": 86 * 60 + 10,
        "end": 89 * 60,
        "duration": 170.0,
        "factories": ("make_weather_system",),
        "labels": ("state now", "future state", "SFNO", "spherical basis", "ensemble futures", "chaos", "calibration", "domain metrics"),
        "comments": ("1:26:10.0 -> local 0.0", "1:26:23.0 -> local 13.0", "1:26:37.0 -> local 27.0", "1:26:50.0 -> local 40.0", "1:27:06.0 -> local 56.0", "1:27:07.0 -> local 57.0", "1:27:22.5 -> local 72.5", "1:27:39.0 -> local 89.0", "1:27:54.5 -> local 104.5", "1:29:00.0 -> local 170.0"),
    },
    {
        "module": "scene_11_03_geophysics_inverse_solvers",
        "class": "Scene1103GeophysicsInverseSolvers",
        "id": "11.3",
        "title": "Geophysics and inverse solvers",
        "start": 89 * 60,
        "end": 91 * 60 + 20,
        "duration": 140.0,
        "factories": ("make_forward_wave_operator",),
        "labels": ("Earth structure", "surface sensors", "forward neural operator", "inverse loop", "Bayesian inversion", "ill-posed", "MCMC"),
        "comments": ("1:29:00.0 -> local 0.0", "1:29:13.5 -> local 13.5", "1:29:26.0 -> local 26.0", "1:29:41.0 -> local 41.0", "1:29:42.0 -> local 42.0", "1:29:57.0 -> local 57.0", "1:30:13.5 -> local 73.5", "1:30:30.0 -> local 90.0", "1:31:20.0 -> local 140.0"),
    },
    {
        "module": "scene_11_04_carbon_storage",
        "class": "Scene1104CarbonStorage",
        "id": "11.4",
        "title": "Carbon storage and climate mitigation",
        "start": 91 * 60 + 20,
        "end": 93 * 60 + 35,
        "duration": 135.0,
        "factories": (),
        "labels": ("CO2 plume", "many scenarios", "fast neural-operator surrogate", "uncertainty quantification", "plume-boundary", "analysis at scale"),
        "comments": ("1:31:20.0 -> local 0.0", "1:31:33.0 -> local 13.0", "1:31:47.0 -> local 27.0", "1:32:00.0 -> local 40.0", "1:32:01.0 -> local 41.0", "1:32:15.5 -> local 55.5", "1:32:31.0 -> local 71.0", "1:32:47.0 -> local 87.0", "1:33:35.0 -> local 135.0"),
    },
    {
        "module": "scene_11_05_molecular_dynamics",
        "class": "Scene1105MolecularDynamics",
        "id": "11.5",
        "title": "Molecular dynamics as continuous-time function",
        "start": 93 * 60 + 35,
        "end": 95 * 60 + 30,
        "duration": 115.0,
        "factories": ("make_molecule_frame_strip",),
        "labels": ("frame sequence", "continuous trajectory function", "trajectory function", "uncertainty", "long-time behavior", "symmetry", "stability"),
        "comments": ("1:33:35.0 -> local 0.0", "1:33:47.0 -> local 12.0", "1:33:59.0 -> local 24.0", "1:34:12.5 -> local 37.5", "1:34:13.5 -> local 38.5", "1:34:29.0 -> local 54.0", "1:34:44.5 -> local 69.5", "1:35:30.0 -> local 115.0"),
    },
    {
        "module": "scene_11_06_automotive_cfd",
        "class": "Scene1106AutomotiveCFD",
        "id": "11.6",
        "title": "Automotive CFD and domain knowledge",
        "start": 95 * 60 + 30,
        "end": 98 * 60 + 10,
        "duration": 160.0,
        "factories": (),
        "labels": ("car geometry", "pressure / velocity field", "sharp boundary", "geometry + boundary sensitive", "inductive bias", "domain-informed", "sample", "not millions"),
        "comments": ("1:35:30.0 -> local 0.0", "1:35:43.0 -> local 13.0", "1:35:55.5 -> local 25.5", "1:36:09.0 -> local 39.0", "1:36:10.0 -> local 40.0", "1:36:25.0 -> local 55.0", "1:36:40.0 -> local 70.0", "1:36:57.0 -> local 87.0", "1:37:15.0 -> local 105.0", "1:38:10.0 -> local 160.0"),
    },
    {
        "module": "scene_11_07_physics_verification",
        "class": "Scene1107PhysicsVerification",
        "id": "11.7",
        "title": "Physics verification",
        "start": 98 * 60 + 10,
        "end": 101 * 60 + 40,
        "duration": 210.0,
        "factories": ("make_residual_checker",),
        "labels": ("predicted function", "PDE residual", "conservation", "tipping point", "calibration", "physics-informed loss", "leaderboard", "L2 benchmark"),
        "comments": ("1:38:10.0 -> local 0.0", "1:38:24.0 -> local 14.0", "1:38:38.0 -> local 28.0", "1:38:52.0 -> local 42.0", "1:38:53.0 -> local 43.0", "1:39:08.0 -> local 58.0", "1:39:25.0 -> local 75.0", "1:39:42.0 -> local 92.0", "1:40:05.0 -> local 115.0", "1:41:40.0 -> local 210.0"),
    },
]


def load_scene_module(module_name):
    path = SCENE_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Section11SceneContractTest(unittest.TestCase):
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
