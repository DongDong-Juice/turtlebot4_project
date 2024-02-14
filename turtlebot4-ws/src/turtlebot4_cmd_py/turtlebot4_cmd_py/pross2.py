import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import String

class test2(Node):
    def __init__(self):
        super().__init__('test2')
        self.publisher_ = self.create_publisher(Int32,'test2',10)
        self.timer = self.create_timer(5, self.callback)

    def callback(self):
        msg = Int32()
        msg.data = 0
        msg.data += 1
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = test2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:

        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
