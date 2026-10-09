#!/usr/bin/env python3
"""Servico /record_spot: registra /amcl_pose e salva spots.txt ao receber end."""

from pathlib import Path

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from spot_recorder_interfaces.srv import MyServiceMessage


class SpotRecorderNode(Node):
    def __init__(self):
        super().__init__('spot_recorder')
        self.current_pose = None
        self.spots = []
        # ros2 run: caminho relativo ao diretorio do processo.
        # O launch da aula fornece um caminho absoluto.
        self.declare_parameter('output_file', 'spots.txt')
        self.output_file = Path(
            str(self.get_parameter('output_file').value)
        ).expanduser()

        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_callback,
            10
        )
        self.service = self.create_service(
            MyServiceMessage,
            '/record_spot',
            self.record_spot_callback
        )
        self.get_logger().info(
            'SpotRecorderNode inicializado. Aguardando chamadas em /record_spot. '
            f'Arquivo de saida: {self.output_file.resolve()}'
        )

    def amcl_callback(self, msg: PoseWithCovarianceStamped):
        self.current_pose = msg

    def record_spot_callback(self, request, response):
        label = request.label.strip()
        self.get_logger().info(f"Servico chamado com label: '{label}'")
        if not label:
            response.navigation_successfull = False
            response.message = 'Informe uma etiqueta, por exemplo center, left ou end.'
            return response

        if label.lower() == 'end':
            if not self.spots:
                response.navigation_successfull = False
                response.message = 'Nenhum spot registrado para salvar.'
                return response
            try:
                self.output_file.parent.mkdir(parents=True, exist_ok=True)
                with self.output_file.open('w', encoding='utf-8') as handle:
                    for spot in self.spots:
                        line = (
                            f"{spot['label']}: "
                            f"x={spot['x']}, y={spot['y']}, z={spot['z']}, "
                            f"qx={spot['qx']}, qy={spot['qy']}, "
                            f"qz={spot['qz']}, qw={spot['qw']}\n"
                        )
                        handle.write(line)
                response.navigation_successfull = True
                response.message = (
                    f"{len(self.spots)} spots salvos em {self.output_file.resolve()}."
                )
                self.get_logger().info(response.message)
            except OSError as exc:
                response.navigation_successfull = False
                response.message = f'Erro ao salvar arquivo: {exc}'
                self.get_logger().error(response.message)
            return response

        if self.current_pose is None:
            response.navigation_successfull = False
            response.message = 'Nenhuma pose recebida ainda de /amcl_pose.'
            self.get_logger().warning(response.message)
            return response

        pose = self.current_pose.pose.pose
        self.spots.append({
            'label': label,
            'x': pose.position.x,
            'y': pose.position.y,
            'z': pose.position.z,
            'qx': pose.orientation.x,
            'qy': pose.orientation.y,
            'qz': pose.orientation.z,
            'qw': pose.orientation.w,
        })
        response.navigation_successfull = True
        response.message = f"Spot '{label}' registrado com sucesso."
        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = SpotRecorderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
