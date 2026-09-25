"""Step 7: visualização cinemática isolada; não inicia Gazebo/ros2_control.

Execução sem compilar:
  ros2 launch /caminho/ros2-aulas/aula01/exemplos/meu_robo_urdf_aula/launch/display_step7.launch.py

Também pode ser instalado no pacote existente, pois usa somente caminhos
relativos às pastas launch/, urdf/ e rviz/.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    base = Path(__file__).resolve().parent.parent
    model = base / "urdf" / "simple_robot_step7.urdf"
    rviz_config = base / "rviz" / "step7.rviz"
    for path in (model, rviz_config):
        if not path.is_file():
            raise FileNotFoundError(f"Arquivo necessário não encontrado: {path}")

    description = model.read_text(encoding="utf-8")
    if ET.fromstring(description).tag != "robot":
        raise ValueError("O modelo precisa ter <robot> como elemento raiz.")

    namespace = "urdf_step7"
    tf_remaps = [("/tf", "tf"), ("/tf_static", "tf_static")]

    return LaunchDescription([
        LogInfo(msg="Step 7: RViz + sliders. Sem física, controladores ou imagens."),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            namespace=namespace,
            parameters=[{
                "robot_description": ParameterValue(description, value_type=str),
                "publish_frequency": 30.0,
                "use_sim_time": False,
            }],
            remappings=tf_remaps,
            output="screen",
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            namespace=namespace,
            arguments=[str(model)],
            parameters=[{
                "rate": 30,
                "use_mimic_tags": True,
                "use_smallest_joint_limits": True,
                "use_sim_time": False,
            }],
            output="screen",
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            namespace=namespace,
            arguments=["-d", str(rviz_config)],
            parameters=[{"use_sim_time": False}],
            remappings=tf_remaps,
            output="screen",
        ),
    ])
