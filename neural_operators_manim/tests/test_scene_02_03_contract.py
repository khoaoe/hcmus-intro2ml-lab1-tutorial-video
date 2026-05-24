import importlib
import inspect
import unittest

from manim import Scene


class Scene0203ContractTest(unittest.TestCase):
    def test_scene_class_exposes_script_timing_contract(self):
        module = importlib.import_module(
            "src.scenes.scene_02_03_fluids_materials_molecules_robots"
        )
        scene_class = module.Scene0203FluidsMaterialsMoleculesRobots

        self.assertEqual(scene_class.SCRIPT_ID, "2.3")
        self.assertEqual(scene_class.SCRIPT_TITLE, "Fluids, materials, molecules, robots")
        self.assertEqual(scene_class.SCRIPT_START, 645.0)
        self.assertEqual(scene_class.SCRIPT_END, 775.0)
        self.assertEqual(scene_class.SCENE_DURATION, 130.0)

    def test_timed_scene_helpers_are_used(self):
        timing = importlib.import_module("src.common.timing")
        self.assertTrue(hasattr(timing, "TimedScene"))
        self.assertTrue(issubclass(timing.TimedScene, Scene))
        for method_name in ("play_timed", "wait_timed", "pad_to"):
            self.assertTrue(hasattr(timing.TimedScene, method_name), method_name)

    def test_required_visual_component_factories_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_02_03_fluids_materials_molecules_robots"
        )
        scene_class = module.Scene0203FluidsMaterialsMoleculesRobots

        for method_name in (
            "make_panel_grid",
            "make_flow_field",
            "make_deformation_mesh",
            "make_molecule_trajectory",
            "make_robot_joint_path",
            "make_domain_markers",
            "make_error_stack",
            "make_function_contract",
        ):
            self.assertTrue(hasattr(scene_class, method_name), method_name)

    def test_named_visual_objects_exist(self):
        module = importlib.import_module(
            "src.scenes.scene_02_03_fluids_materials_molecules_robots"
        )

        for class_name in (
            "PanelGrid",
            "FlowField",
            "DeformationMesh",
            "TrajectoryCurve",
            "RobotJointPath",
            "BoundaryHighlight",
        ):
            self.assertTrue(hasattr(module, class_name), class_name)

    def test_construct_uses_timestamp_driven_scene_helpers(self):
        module = importlib.import_module(
            "src.scenes.scene_02_03_fluids_materials_molecules_robots"
        )
        source = inspect.getsource(module.Scene0203FluidsMaterialsMoleculesRobots.construct)

        self.assertIn("play_timed", source)
        self.assertIn("wait_timed", source)
        self.assertIn("self.pad_to(self.SCENE_DURATION)", source)
        self.assertNotIn("self.play(", source)
        self.assertNotIn("self.wait(", source)

    def test_required_script_labels_are_present(self):
        module = importlib.import_module(
            "src.scenes.scene_02_03_fluids_materials_molecules_robots"
        )
        source = inspect.getsource(module)

        for label in (
            "CFD: v(x,t), p(x,t)",
            "Material",
            "deformation: d(x,t)",
            "Molecules",
            "state: q(t)",
            "Robotics",
            "joint motion: theta(t)",
            "Not images. Functions on domains.",
            "domain",
            "geometry",
            "boundary",
            "physics law",
            "physics laws",
            "wrong derivative",
            "breaks conservation",
            "bad boundary",
            "respect domain",
            "respect discretization",
            "support derivatives & integrals",
            "mesh is only the measurement layer",
            "data is function",
            "technical contract",
        ):
            self.assertIn(label, source, label)


if __name__ == "__main__":
    unittest.main()
