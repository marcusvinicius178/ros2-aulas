"""Cartographer publica map->odom; o simulador continua dono de odom->base."""
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os


def generate_launch_description():
    config = os.path.join(get_package_share_directory('cartographer_slam'), 'config')
    sim = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(package='cartographer_ros', executable='cartographer_node',
             name='cartographer_node', output='screen',
             parameters=[{'use_sim_time': sim}],
             arguments=['-configuration_directory', config,
                        '-configuration_basename', 'cartographer.lua'],
             remappings=[('scan', '/scan'), ('odom', '/odom')]),
        Node(package='cartographer_ros', executable='cartographer_occupancy_grid_node',
             name='cartographer_occupancy_grid_node', output='screen',
             parameters=[{'use_sim_time': sim}],
             arguments=['-resolution', '0.05', '-publish_period_sec', '1.0']),
    ])
