#!/usr/bin/env python3
# read_navigate.py — Anda em frente lendo /scan; ao detectar obstáculo no setor frontal,
# aplica frenagem com margem dinâmica e para antes da parede.
# Publica /cmd_vel como TwistStamped (compatível com ros_gz_bridge no Jazzy).
 
from __future__ import annotations
import math
import time
from typing import Optional, Tuple
 
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
 
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped, Twist
 
 
def clamp(v: float, vmin: float, vmax: float) -> float:
    return max(vmin, min(v, vmax))
 
 
class ReadNavigate(Node):
    """
    Estratégia:
      - Assina /scan (QoS de sensor).
      - Considera só um setor frontal [−sector_deg, +sector_deg] (graus).
      - Mantém v até que d_min_frente ≤ margem_dinamica (stop_distance + v²/2a + v·τ + offset_sensor).
      - Freia em rampa até zerar. Se muito perto, freio de emergência (zera já).
    Parâmetros:
      forward_speed (m/s)    : velocidade de cruzeiro.
      stop_distance (m)      : distância alvo que você quer parar ANTES do obstáculo.
      brake_decel (m/s^2)    : desaceleração nominal.
      react_time (s)         : latência para margem v·τ (bridge/loop/latência humana).
      sensor_offset (m)      : nariz do sensor até a “frente segura” do robô.
      sector_deg (deg)       : meia abertura do setor frontal (ex.: 30 => ±30°).
      cmd_topic (str)        : tópico de saída (TwistStamped).
      emergency_dist (m)     : abaixo disso, zera na hora (failsafe).
    """
 
    def __init__(self) -> None:
        super().__init__('read_navigate')
 
        # Parâmetros
        self.declare_parameter('forward_speed', 0.25)
        self.declare_parameter('stop_distance', 0.30)   # recomendo >= 0.20 no mundo TB3
        self.declare_parameter('brake_decel', 0.8)
        self.declare_parameter('react_time', 0.10)
        self.declare_parameter('sensor_offset', 0.05)
        self.declare_parameter('sector_deg', 30.0)
        self.declare_parameter('cmd_topic', '/cmd_vel')
        self.declare_parameter('emergency_dist', 0.08)
 
        self.forward_speed: float = float(self.get_parameter('forward_speed').value)
        self.stop_distance: float = float(self.get_parameter('stop_distance').value)
        self.brake_decel:   float = float(self.get_parameter('brake_decel').value)
        self.react_time:    float = float(self.get_parameter('react_time').value)
        self.sensor_offset: float = float(self.get_parameter('sensor_offset').value)
        self.sector_deg:    float = float(self.get_parameter('sector_deg').value)
        self.cmd_topic:     str   = str(self.get_parameter('cmd_topic').value)
        self.emergency_dist:float = float(self.get_parameter('emergency_dist').value)
 
        # Assinatura do LaserScan
        self._scan_sub = self.create_subscription(
            LaserScan, '/scan', self._on_scan, qos_profile_sensor_data
        )
 
        # Publicadores
        pub_qos = QoSProfile(depth=10)
        pub_qos.reliability = QoSReliabilityPolicy.RELIABLE
        pub_qos.history = QoSHistoryPolicy.KEEP_LAST
        self._pub_stamped = self.create_publisher(TwistStamped, self.cmd_topic, qos_profile=pub_qos)
        self._pub_twist_dbg = self.create_publisher(Twist, '/cmd_vel_twist', qos_profile=pub_qos)
 
        # Estados
        self._last_scan: Optional[LaserScan] = None
        self._current_v: float = 0.0
 
        # Rate limit de logs
        self._last_log = 0.0
        self._log_period = 1.0
 
        # Loop de controle
        self._dt = 0.05   # 20 Hz
        self._timer = self.create_timer(self._dt, self._control_step)
 
        self.get_logger().info(
            f'{self.get_name()} ON | v={self.forward_speed:.2f} m/s, '
            f'stop={self.stop_distance:.2f} m, sector=±{self.sector_deg:.1f}°, '
            f'τ={self.react_time:.2f}s, a={self.brake_decel:.2f} m/s², '
            f'offset={self.sensor_offset:.2f} m, emerg={self.emergency_dist:.2f} m.'
        )
 
    # -------------------- Utils --------------------
 
    @staticmethod
    def _sector_indices(msg: LaserScan, deg_half: float) -> Tuple[int, int]:
        """Retorna índices [i0, i1] do setor frontal ±deg_half (0 rad = frente)."""
        a_min = msg.angle_min
        inc = msg.angle_increment
        if inc == 0.0:
            return 0, len(msg.ranges) - 1
        # Em muitos sensores, 0 rad já é frente. Garantimos limites.
        ang0 = -math.radians(deg_half)
        ang1 = +math.radians(deg_half)
        i0 = int((ang0 - a_min) / inc)
        i1 = int((ang1 - a_min) / inc)
        i0 = clamp(i0, 0, len(msg.ranges) - 1)
        i1 = clamp(i1, 0, len(msg.ranges) - 1)
        if i0 > i1:
            i0, i1 = i1, i0
        return i0, i1
 
    def _front_min(self, msg: LaserScan) -> Optional[float]:
        """Menor distância válida no setor frontal."""
        i0, i1 = self._sector_indices(msg, self.sector_deg)
        vals = []
        rmin = msg.range_min if msg.range_min > 0.0 else 0.0
        rmax = msg.range_max if msg.range_max > 0.0 else float('inf')
        for r in msg.ranges[i0:i1+1]:
            if r is None or math.isnan(r) or math.isinf(r):
                continue
            if r < rmin or r > rmax:
                continue
            vals.append(r)
        return min(vals) if vals else None
 
    # -------------------- Callbacks --------------------
 
    def _on_scan(self, msg: LaserScan) -> None:
        self._last_scan = msg
 
    def _control_step(self) -> None:
        if self._last_scan is None:
            self._log_throttled('Aguardando /scan...')
            return
 
        dmin = self._front_min(self._last_scan)
        if dmin is None:
            self._log_throttled('Sem leituras válidas no setor frontal.')
            self._pub_cmd(0.0)  # segurança: zera se “cego”
            self._current_v = 0.0
            return
 
        v = self._current_v
        a = max(1e-3, self.brake_decel)
 
        # Margem dinâmica: onde queremos começar a frear para parar antes da parede
        stopping = (v * v) / (2.0 * a)
        margin = self.stop_distance + stopping + (v * self.react_time) + self.sensor_offset
 
        # Emergência: se muito perto, para já
        if dmin <= self.emergency_dist:
            v_cmd = 0.0
            self._pub_cmd(v_cmd)
            self._current_v = v_cmd
            self._log_throttled(f'EMERGÊNCIA: dmin={dmin:.3f} m ≤ {self.emergency_dist:.3f} m, parando agora.')
            return
 
        # Regra de controle
        if dmin <= margin:
            # freia em rampa
            v_cmd = max(0.0, v - a * self._dt)
            if v_cmd == 0.0:
                self._log_throttled(f'Parado a {dmin:.3f} m (margem={margin:.3f} m).')
        else:
            # acelera até cruzeiro
            v_cmd = min(self.forward_speed, v + a * self._dt)
 
        self._pub_cmd(v_cmd)
        self._current_v = v_cmd
 
    # -------------------- Publicadores --------------------
 
    def _pub_cmd(self, v: float, w: float = 0.0) -> None:
        msg_s = TwistStamped()
        msg_s.header.stamp = self.get_clock().now().to_msg()
        msg_s.header.frame_id = 'base_link'
        msg_s.twist.linear.x = float(v)
        msg_s.twist.angular.z = float(w)
        self._pub_stamped.publish(msg_s)
 
        # debug opcional
        msg = Twist()
        msg.linear.x = float(v)
        msg.angular.z = float(w)
        self._pub_twist_dbg.publish(msg)
 
    # -------------------- Logs --------------------
 
    def _log_throttled(self, text: str, period: float = None) -> None:
        now = time.time()
        per = self._log_period if period is None else period
        if now - self._last_log >= per:
            self.get_logger().info(text)
            self._last_log = now
 
    # -------------------- Encerramento --------------------
 
    def destroy_node(self) -> bool:
        try:
            self._pub_cmd(0.0, 0.0)
            _ = self.get_clock().now() + Duration(seconds=0.05)
        except Exception:
            pass
        return super().destroy_node()
 
 
def main() -> None:
    rclpy.init()
    node = ReadNavigate()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()
 
