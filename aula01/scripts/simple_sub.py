#!/usr/bin/env python3
# simple_sub.py — escuta String em /chatter
 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
 
class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
        self.sub = self.create_subscription(String, 'chatter', self.on_msg, 10)
        self.get_logger().info('SimpleSubscriber ON -> topic: /chatter')
 
    def on_msg(self, msg: String):
        self.get_logger().info(f'Recebido: "{msg.data}"')
 
def main():
    rclpy.init()
    node = SimpleSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
 
if __name__ == '__main__':
    main()
