"""Validacao local sem ROS. Executar: python3 -m unittest discover -s aula02/tests -v."""
import ast
import importlib.util
import math
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'pose_utils', ROOT / 'exemplos/localization_server/localization_server/pose_utils.py')
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)


class CourseTests(unittest.TestCase):
    def test_python_syntax(self):
        for path in ROOT.rglob('*.py'):
            with self.subTest(path=path):
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))

    def test_shell_syntax(self):
        for path in (ROOT / 'scripts').glob('*.bash'):
            with self.subTest(path=path):
                subprocess.run(['bash', '-n', str(path)], check=True)

    def test_teleop_dispatch_without_ros(self):
        # Executa o script real com ambiente/CLI simulados; nao testa ROS ou movimento.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            shutil.copy2(ROOT / 'scripts/03_teleop.bash', folder / '03_teleop.bash')
            (folder / 'ambiente.bash').write_text('# Ambiente de teste sem ROS\n')
            fake = folder / 'ros2'
            fake.write_text(
                '#!/usr/bin/env bash\n'
                'if [[ "$1" == topic ]]; then printf "%s\\n" "$FAKE_TOPIC_TYPE"; '
                'else printf "%s\\n" "$@"; fi\n')
            fake.chmod(0o755)
            for message_type, expected in (
                    ('geometry_msgs/msg/TwistStamped', 'true'),
                    ('geometry_msgs/msg/Twist', 'false'),
                    ('', None),
                    ('geometry_msgs/msg/Twist\ngeometry_msgs/msg/TwistStamped', None)):
                with self.subTest(message_type=message_type):
                    env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ['PATH'],
                               FAKE_TOPIC_TYPE=message_type)
                    result = subprocess.run(['bash', str(folder / '03_teleop.bash')],
                                            env=env, text=True, capture_output=True, timeout=15)
                    if expected is None:
                        self.assertNotEqual(result.returncode, 0)
                    else:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn('stamped:=' + expected, result.stdout)
                        self.assertEqual('frame_id:=base_footprint' in result.stdout,
                                         expected == 'true')

    def test_package_names(self):
        names = set()
        for path in (ROOT / 'exemplos').glob('*/package.xml'):
            node = ET.parse(path).getroot()
            self.assertEqual(node.findtext('name'), path.parent.name)
            names.add(node.findtext('name'))
        self.assertEqual(names, {'cartographer_slam', 'map_server',
                                'localization_server', 'spot_recorder_interfaces'})

    def test_python_package_markers(self):
        for path in (ROOT / 'exemplos').glob('*/setup.py'):
            package = path.parent.name
            self.assertTrue((path.parent / package / '__init__.py').is_file())
            self.assertTrue((path.parent / 'resource' / package).is_file())
            self.assertTrue((path.parent / 'setup.cfg').is_file())
            self.assertTrue(list((path.parent / 'launch').glob('*.launch.py')))

    def test_amcl_config(self):
        path = ROOT / 'exemplos/localization_server/config/amcl_config.yaml'
        params = yaml.safe_load(path.read_text())['amcl']['ros__parameters']
        self.assertIs(params['use_sim_time'], True)
        self.assertEqual(params['robot_model_type'], 'nav2_amcl::DifferentialMotionModel')
        self.assertEqual(params['base_frame_id'], 'base_footprint')
        self.assertAlmostEqual(params['z_hit'] + params['z_rand'], 1.0)
        self.assertIs(params['set_initial_pose'], False)

    def test_interface_contract(self):
        text = (ROOT / 'exemplos/spot_recorder_interfaces/srv/MyServiceMessage.srv').read_text()
        lines = [line.strip() for line in text.splitlines()
                 if line.strip() and not line.lstrip().startswith('#')]
        self.assertEqual(lines, ['string label', '---', 'bool success', 'string message'])

    def test_quaternion_roundtrip(self):
        for angle in (-math.pi, -1.2, 0.0, 0.328028, math.pi / 2, math.pi):
            z, w = utils.yaw_to_quaternion(angle)
            self.assertAlmostEqual(z * z + w * w, 1.0)
            self.assertAlmostEqual(utils.quaternion_to_yaw(0.0, 0.0, z, w), angle)

    def test_invalid_numbers(self):
        for angle in (math.inf, math.nan):
            with self.assertRaises(ValueError):
                utils.yaw_to_quaternion(angle)
        with self.assertRaises(ValueError):
            utils.quaternion_to_yaw(0, 0, 0, 0)

    def test_labels(self):
        for label in ('center', 'left', 'ponto_2', 'porta-A'):
            self.assertTrue(utils.valid_label(label))
        for label in ('end', '', '../bad', 'a b', '3point', 'a' * 65):
            self.assertFalse(utils.valid_label(label))

    @staticmethod
    def records():
        return {'center': {'position': {'x': 1.0, 'y': 2.0, 'z': 0.0},
                           'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0},
                           'yaw': 0.0, 'stamp': {'sec': 1, 'nanosec': 0}}}

    def test_save_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'spots.yaml'
            a, b = utils.save_spots(path, self.records(), 'map', 'base_footprint')
            original = a.read_text()
            self.assertIn('center', yaml.safe_load(original)['spots'])
            self.assertIn('center 1 2 0', b.read_text())
            with self.assertRaises(FileExistsError):
                utils.save_spots(path, self.records(), 'map', 'base_footprint')
            self.assertEqual(a.read_text(), original)

    def test_partial_failure_preserves_existing_txt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'spots.yaml'
            path.with_suffix('.txt').write_text('arquivo anterior')
            with self.assertRaises(FileExistsError):
                utils.save_spots(path, self.records(), 'map', 'base_footprint')
            self.assertFalse(path.exists())
            self.assertEqual(path.with_suffix('.txt').read_text(), 'arquivo anterior')

    def test_empty_save(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                utils.save_spots(Path(directory) / 'spots.yaml', {}, 'map', 'base_footprint')


if __name__ == '__main__':
    unittest.main()
