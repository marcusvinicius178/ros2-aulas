from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
 
 
def generate_launch_description():
    pkg_share = get_package_share_directory('meu_robo_urdf_aula')
 
    urdf_file = os.path.join(pkg_share, 'urdf', 'simple_robot_step2.urdf')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'step1.rviz')
 
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()
 
    return LaunchDescription([
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description_content
            }]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file]
        )
    ])
