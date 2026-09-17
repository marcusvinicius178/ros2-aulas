#!/usr/bin/env python3
# simple_pub.py — publica String em /chatter a cada 0.5 s
 
from datetime import datetime
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
 
 
class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.tick)
        self.i = 0
        self.get_logger().info(f'SimplePublisher ON -> topic: /chatter. Contador inicial: {self.i}')
 
    def tick(self):
        msg = String()
        msg.data = f'Hello ROS 2 #{self.i} @ {datetime.now().isoformat(timespec="seconds")}'
        self.pub.publish(msg)
        self.get_logger().info(f'Publicando contador: {self.i}')
        self.i += 1
 
 
def main():
    rclpy.init()
    node = SimplePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()

