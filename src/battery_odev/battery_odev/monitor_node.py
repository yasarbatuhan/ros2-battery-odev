import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.subscription = self.create_subscription(
            Float32,
            '/battery_level',
            self.battery_callback,
            10
        )
        self.was_low = False

    def battery_callback(self, msg: Float32):
        level = msg.data
        self.get_logger().info(f'Pil seviyesi: %{level:.1f}')

        if level < 20.0:
            self.get_logger().warn(f'Düşük pil uyarısı! Seviye: %{level:.1f}')
            self.was_low = True
        elif self.was_low:
            self.get_logger().info('Pil seviyesi normal düzeye döndü, uyarı sona erdi.')
            self.was_low = False


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
