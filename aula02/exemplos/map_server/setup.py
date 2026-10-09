from glob import glob
from setuptools import find_packages, setup

package_name = 'map_server'
setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/maps', glob('maps/*.yaml') + glob('maps/*.pgm') + glob('maps/*.png')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcus Vinicius Leal de Carvalho',
    maintainer_email='43826438+marcusvinicius178@users.noreply.github.com',
    description='Publicacao de mapa e demonstracao de lifecycle',
    license='UNLICENSED',
    entry_points={'console_scripts': []},
)
