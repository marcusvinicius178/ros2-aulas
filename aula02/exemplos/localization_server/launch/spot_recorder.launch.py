"""Inicia apenas o gravador; AMCL e simulacao devem estar ativos."""
from datetime import datetime
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    output = Path.home() / 'ros2_aula02_dados' / (
        'spots_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('output_file', default_value=str(output)),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(package='localization_server', executable='spots_to_file',
             name='spot_recorder', output='screen', parameters=[{
                 'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
                 'output_file': LaunchConfiguration('output_file'),
                 'global_frame': 'map', 'base_frame': 'base_footprint', 'max_tf_age': 5.0}]),
    ])
