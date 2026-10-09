from glob import glob
from setuptools import find_packages, setup
import os

package_name = 'localization_server'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            os.path.join('share', package_name),
            ['package.xml'],
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py')),
        ),
        # Copia .srv como recurso, se existir. A geracao real da interface
        # acontece em spot_recorder_interfaces via rosidl + ament_cmake.
        (
            os.path.join('share', package_name, 'srv'),
            glob(os.path.join('srv', '*.srv')),
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*.yaml')),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcus Vinicius Leal de Carvalho',
    maintainer_email='43826438+marcusvinicius178@users.noreply.github.com',
    description='Localizacao AMCL e gravacao de posicoes',
    license='UNLICENSED',
    entry_points={
        'console_scripts': [
            'spots_to_file = localization_server.spots_to_file:main',
            'spots_to_file_tf = localization_server.spots_to_file_tf:main',
            'set_initial_pose = localization_server.set_initial_pose:main',
        ],
    },
)
