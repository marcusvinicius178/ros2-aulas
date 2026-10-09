"""Somente map_server + seu lifecycle manager; nao inicia AMCL nem Gazebo."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    sim = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    return LaunchDescription([
        DeclareLaunchArgument('map', description='Caminho absoluto para o YAML do mapa salvo'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(package='nav2_map_server', executable='map_server', name='map_server',
             output='screen', parameters=[{
                 'yaml_filename': LaunchConfiguration('map'),
                 'topic_name': 'map', 'frame_id': 'map', 'use_sim_time': sim}]),
        Node(package='nav2_lifecycle_manager', executable='lifecycle_manager',
             name='lifecycle_manager_mapper', output='screen',
             parameters=[{'use_sim_time': sim, 'autostart': True,
                          'node_names': ['map_server']}]),
    ])
