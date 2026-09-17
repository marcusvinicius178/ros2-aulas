from launch import LaunchDescription
from launch_ros.actions import Node
 
 
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_lab01',
            executable='simple_pub',
            name='simple_pub',
            output='screen'
        ),
        Node(
            package='my_lab01',
            executable='simple_sub',
            name='simple_sub',
            output='screen'
        ),
    ])

