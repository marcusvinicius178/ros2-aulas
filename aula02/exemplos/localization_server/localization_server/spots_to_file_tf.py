"""Servico /record_spot: captura TF map->base_footprint e salva ao receber end."""
from datetime import datetime
import math
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener
from spot_recorder_interfaces.srv import MyServiceMessage
from localization_server.pose_utils import quaternion_to_yaw, save_spots, valid_label


class SpotRecorder(Node):
    def __init__(self):
        super().__init__('spot_recorder')
        default = Path.home() / 'ros2_aula02_dados' / (
            'spots_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.yaml')
        self.declare_parameter('output_file', str(default))
        self.declare_parameter('global_frame', 'map')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('max_tf_age', 5.0)
        self.output = Path(self.get_parameter('output_file').value).expanduser()
        self.frame = self.get_parameter('global_frame').value
        self.base = self.get_parameter('base_frame').value
        self.max_age = float(self.get_parameter('max_tf_age').value)
        if not math.isfinite(self.max_age) or self.max_age <= 0:
            raise ValueError('max_tf_age deve ser positivo e finito')
        self.records = {}
        self.saved = False
        self.buffer = Buffer(node=self)
        self.listener = TransformListener(self.buffer, self)
        self.service = self.create_service(MyServiceMessage, '/record_spot', self.record)
        self.get_logger().info(f'Saida: {self.output}. Grave etiquetas e finalize com end.')

    def record(self, request, response):
        label = request.label.strip()
        try:
            if self.saved:
                raise ValueError('Sessao ja salva; reinicie o gravador para outra sessao')
            if label == 'end':
                paths = save_spots(self.output, self.records, self.frame, self.base)
                self.saved = True
                response.navigation_successfull = True
                response.message = 'Arquivos salvos: ' + ', '.join(str(p) for p in paths)
                self.get_logger().info(response.message)
                return response
            if not valid_label(label):
                raise ValueError('Use letras, numeros, _ ou -; comece com letra (1-64 caracteres)')
            if label in self.records:
                raise ValueError('Etiqueta ja gravada; escolha outro nome')
            # Nao bloqueia o callback: o listener precisa do mesmo executor para receber TF.
            transform = self.buffer.lookup_transform(self.frame, self.base, Time())
            now = self.get_clock().now().nanoseconds / 1e9
            stamp = transform.header.stamp.sec + transform.header.stamp.nanosec / 1e9
            if now <= 0 or stamp <= 0 or now - stamp > self.max_age or stamp - now > self.max_age:
                raise ValueError('TF/clock ausente ou desatualizado; verifique simulacao e AMCL')
            p, q = transform.transform.translation, transform.transform.rotation
            if not all(math.isfinite(v) for v in (p.x, p.y, p.z)):
                raise ValueError('Posicao nao finita')
            self.records[label] = {
                'position': {'x': p.x, 'y': p.y, 'z': p.z},
                'orientation': {'x': q.x, 'y': q.y, 'z': q.z, 'w': q.w},
                'yaw': quaternion_to_yaw(q.x, q.y, q.z, q.w),
                'stamp': {'sec': transform.header.stamp.sec,
                          'nanosec': transform.header.stamp.nanosec},
            }
            response.navigation_successfull = True
            response.message = f'Pose {label} capturada em {self.frame}; end salva os arquivos.'
        except (ValueError, OSError, TransformException) as exc:
            response.navigation_successfull = False
            response.message = str(exc)
            self.get_logger().warning(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = SpotRecorder()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            if node.records and not node.saved:
                node.get_logger().warning('Posicoes NAO salvas: faltou chamar end com sucesso.')
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
