import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class test1(Node):
    def __init__(self):
        super().__init__('test1')
        self.publisher_ = self.create_publisher(Int32,'test1',10)
        self.sub = self.create_subscription(Int32,'test',self.callback,10)

    def callback(self,msg):
        msg = Int32()
        msg.data = 0
        msg.data += 1
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = test1()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:

        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
