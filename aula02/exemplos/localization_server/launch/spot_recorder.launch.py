"""Inicia o gravador didatico da aula: /amcl_pose -> spots.txt."""
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    default_output = str(Path.home() / 'ros2_aula02_dados' / 'spots.txt')
    return LaunchDescription([
        DeclareLaunchArgument(
            'output_file',
            default_value=default_output,
            description='Arquivo TXT salvo apos label=end'
        ),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(
            package='localization_server',
            executable='spots_to_file',
            name='spot_recorder',
            output='screen',
            parameters=[{
                'use_sim_time': ParameterValue(
                    LaunchConfiguration('use_sim_time'), value_type=bool),
                'output_file': LaunchConfiguration('output_file'),
            }],
        ),
    ])
