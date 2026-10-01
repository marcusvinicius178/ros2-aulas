from glob import glob
from setuptools import find_packages, setup

package_name = 'localization_server'
setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcus Vinicius Leal de Carvalho',
    maintainer_email='43826438+marcusvinicius178@users.noreply.github.com',
    description='Localizacao AMCL e gravacao de posicoes',
    license='UNLICENSED',
    entry_points={'console_scripts': ['spots_to_file = localization_server.spots_to_file:main', 'set_initial_pose = localization_server.set_initial_pose:main']},
)
