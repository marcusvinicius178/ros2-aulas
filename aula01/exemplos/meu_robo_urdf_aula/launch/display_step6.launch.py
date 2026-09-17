from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
 
def generate_launch_description():
    pkg_share = FindPackageShare('meu_robo_urdf_aula')
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'simple_robot_step5.urdf.xacro'])
    rviz_config_file = PathJoinSubstitution([pkg_share, 'rviz', 'step5.rviz'])
    world_file = PathJoinSubstitution([pkg_share, 'worlds', 'empty_camera.world.sdf'])
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
 
    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments={'gz_args': [' -r ', world_file]}.items()
    )
 
    spawn_robot_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_spawn_model.launch.py'])
        ),
        launch_arguments={
            'world': 'empty_camera',
            'topic': 'robot_description',
            'entity_name': 'simple_robot',
            'x': '0.0', 'y': '0.0', 'z': '0.3', 'R': '0.0', 'P': '0.0', 'Y': '0.0'
        }.items()
    )
 
    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        parameters=[{'use_sim_time': True}]
    )
 
    return LaunchDescription([
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui', name='joint_state_publisher_gui', parameters=[{'use_sim_time': True}]),
        Node(package='robot_state_publisher', executable='robot_state_publisher', name='robot_state_publisher', output='screen', parameters=[{'robot_description': robot_description}, {'use_sim_time': True}]),
        Node(package='rviz2', executable='rviz2', name='rviz2', output='screen', arguments=['-d', rviz_config_file], parameters=[{'use_sim_time': True}]),
        gazebo_node,
        TimerAction(period=2.0, actions=[spawn_robot_node, gz_bridge_node])
    ])
 

