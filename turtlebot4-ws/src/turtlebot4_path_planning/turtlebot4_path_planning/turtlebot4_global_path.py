import json
import os
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.node import Node


class Turtlebot4PathPlanning(Node):
    def __init__(self):
        super().__init__('Turtlebot4PathPlanning')
        self.sub= self.create_subscription(PoseStamped,'/goal_pose',
                                           self.path_plan,10)
        self.plan=list()
        self.index=1

    def path_plan(self,msg):
        point={'index':self.index,
               'x':msg.pose.position.x,
               'y':msg.pose.position.y,
               'z':msg.pose.orientation.z,
               'w':msg.pose.orientation.w}
        self.plan.append(point)
        self.index +=1
        print(self.plan)


def main(args=None):
    rclpy.init(args=args)
    node = Turtlebot4PathPlanning()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        with open('/home/dong/turtlebot4_project/turtlebot4-ws/src/turtlebot4_path_planning/path/path.json','w') as f:
            json.dump(node.plan,f,indent=4)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


