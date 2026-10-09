"""Publica x, y e yaw (radianos) no frame map, com covariance e quaternion."""
import argparse
import math
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.utilities import remove_ros_args
from geometry_msgs.msg import PoseWithCovarianceStamped
from localization_server.pose_utils import yaw_to_quaternion


def main(args=None):
    argv = sys.argv if args is None else ['set_initial_pose'] + list(args)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parser.add_argument('yaw', type=float)
    values = parser.parse_args(remove_ros_args(args=argv)[1:])
    if not all(math.isfinite(v) for v in (values.x, values.y, values.yaw)):
        parser.error('x, y e yaw devem ser finitos')
    rclpy.init(args=argv[1:])
    node = Node('aula02_initial_pose')
    publisher = node.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
    try:
        deadline = time.monotonic() + 10.0
        while rclpy.ok():
            clock_ready = (not node.get_parameter('use_sim_time').value or
                           node.get_clock().now().nanoseconds > 0)
            if clock_ready and publisher.get_subscription_count() > 0:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError('Sem clock ou assinante de /initialpose apos 10 s')
            rclpy.spin_once(node, timeout_sec=0.1)
        if not rclpy.ok():
            return
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = node.get_clock().now().to_msg()
        msg.pose.pose.position.x, msg.pose.pose.position.y = values.x, values.y
        qz, qw = yaw_to_quaternion(values.yaw)
        msg.pose.pose.orientation.z, msg.pose.pose.orientation.w = qz, qw
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = math.radians(15.0) ** 2
        publisher.publish(msg)
        deadline = time.monotonic() + 1.0
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
        node.get_logger().info('Pose inicial publicada; confira a convergencia no RViz.')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
