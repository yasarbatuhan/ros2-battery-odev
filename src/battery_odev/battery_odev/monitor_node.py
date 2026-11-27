import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.subscription = self.create_subscription(
            Float32,
            '/battery_level',
            self.battery_callback,
            10
        )
        self.client = self.create_client(Trigger, '/recharge')
        self.was_low = False
        self.recharge_in_progress = False

    def battery_callback(self, msg: Float32):
        level = msg.data
        self.get_logger().info(f'Pil seviyesi: %{level:.1f}')

        if level < 20.0:
            self.get_logger().warn(f'Düşük pil uyarısı! Seviye: %{level:.1f}')
            self.was_low = True
        elif self.was_low:
            self.get_logger().info('Pil seviyesi normal düzeye döndü, uyarı sona erdi.')
            self.was_low = False

        if level < 5.0 and not self.recharge_in_progress:
            if self.client.service_is_ready():
                self.recharge_in_progress = True
                self.get_logger().info('Pil %5 altına indi, /recharge servisi çağrılıyor...')
                future = self.client.call_async(Trigger.Request())
                future.add_done_callback(self.recharge_response_callback)
            else:
                self.get_logger().warn('/recharge servisi henüz hazır değil.')

    def recharge_response_callback(self, future):
        self.recharge_in_progress = False
        try:
            response = future.result()
            self.get_logger().info(
                f'Servis cevabı (success={response.success}): {response.message}'
            )
        except Exception as e:
            self.get_logger().error(f'Servis çağrısı başarısız: {e}')


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
