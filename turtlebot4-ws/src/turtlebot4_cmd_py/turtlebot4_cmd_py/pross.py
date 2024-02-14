import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class test(Node):
    def __init__(self):
        super().__init__('test')
        self.publisher_ = self.create_publisher(Int32,'test',10)
        self.timer = self.create_timer(5,self.callback)

    def callback(self):
        msg = Int32()
        msg.data = 1
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = test()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:

        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
