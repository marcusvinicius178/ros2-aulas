"""Mapa + AMCL + lifecycle; encerrar Cartographer e map_server anterior antes."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    default_config = os.path.join(
        get_package_share_directory('localization_server'), 'config', 'amcl_config.yaml')
    sim = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=os.path.expanduser('~/ros2_ws/src/map_server/maps/turtlebot_area.yaml'),
            description='Caminho absoluto do YAML do mapa salvo'
        ),
        DeclareLaunchArgument('params_file', default_value=default_config),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        Node(package='nav2_map_server', executable='map_server', name='map_server',
             output='screen', parameters=[{'use_sim_time': sim,
                 'yaml_filename': LaunchConfiguration('map'), 'frame_id': 'map'}]),
        Node(package='nav2_amcl', executable='amcl', name='amcl', output='screen',
             parameters=[LaunchConfiguration('params_file'), {'use_sim_time': sim}]),
        Node(package='nav2_lifecycle_manager', executable='lifecycle_manager',
             name='lifecycle_manager_localization', output='screen',
             parameters=[{'use_sim_time': sim, 'autostart': True,
                          'node_names': ['map_server', 'amcl']}]),
    ])
