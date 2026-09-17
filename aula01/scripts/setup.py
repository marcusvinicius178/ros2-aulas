from setuptools import setup
 
package_name = 'my_lab01'
 
setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],  # mantém pacote Python (pasta my_lab01/) se quiser evoluir
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # instala a pasta de launch dentro de share/my_lab01/launch
        ('share/' + package_name + '/launch', ['launch/demo.launch.py']),
    ],
    # expõe executáveis Python colocados em scripts/
    scripts=[
        'scripts/simple_pub.py',
        'scripts/simple_sub.py',
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcus Vinicius',
    maintainer_email='marcus@example.com',
    description='Aula 1: nós simples pub/sub em ROS 2 (Jazzy), executáveis a partir de scripts/.',
    license='Apache-2.0',
    tests_require=['pytest'],
)
 
