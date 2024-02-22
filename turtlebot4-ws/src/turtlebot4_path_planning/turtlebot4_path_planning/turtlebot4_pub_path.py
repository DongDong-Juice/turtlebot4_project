import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped,PoseWithCovarianceStamped
import json
import numpy as np
from rclpy.qos import *
import time

class turtlebot4_pub_path(Node):
    def __init__(self):
        super().__init__('turtlebot4_pub_path')
        qos = QoSProfile(reliability=QoSReliabilityPolicy.BEST_EFFORT,
                         depth=10,
                         durability=QoSDurabilityPolicy.VOLATILE)
        amcl_pose_qos = QoSProfile(
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1)
        #goal_pose는 도착점을 넘겨주는 역활 ,amcl_pose는 현재 로봇의 좌표를 기반으로 도착점에 도착해는지 확인 하는 토픽
        self.pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.robot_pose = self.create_subscription(PoseWithCovarianceStamped,
                                                   'amcl_pose',
                                                   self.checking_robot_pose,
                                                   amcl_pose_qos)
        self.goal_list = np.empty(shape=4)
        self.robot_pose_list = np.empty(shape=3)
        self.count = 0
        self.goal = None
        self.open_path_file()
        self.firstGoal()

    def getPoseStamped(self, positionX, positionXY, rotationZ, rotationW ):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = positionX
        pose.pose.position.y = positionXY
        pose.pose.orientation.z = rotationZ
        pose.pose.orientation.w = rotationW
        return pose

    def open_path_file(self):
        with open('/home/dong/turtlebot4_project/turtlebot4-ws/src/turtlebot4_path_planning/path/path.json','r') as f:
            data = json.load(f)
        self.path_plan_data(data)

    def path_plan_data(self, data): #datas
        index = [i['index'] for i in data]
        x = [i['x'] for i in data]
        y = [i['y'] for i in data]
        z = [i['z'] for i in data]
        w = [i['w'] for i in data]
        self.goal_list =np.array([index, x, y, z, w])

    def checking_robot_pose(self, msg): #데이터를 지속적으로 받아와서 현재 경로의 값에 근접한지 확인
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        self.robot_pose_list = np.array([x, y, z, w])
        self.path()

    def path(self):
        if np.round(self.robot_pose_list[1], 1) - 0.5 <= np.round(self.goal_list[2][self.count], 1) <= np.round(self.robot_pose_list[1], 1) + 0.5:
            self.count += 1
            self.delray()
            print("보냄")
        elif self.count == len(self.goal_list[0]):
            print("end path")
            exit(1)

    def delray(self):
        print("delray 4sec")
        self.goal = self.getPoseStamped(np.round(self.goal_list[1][self.count],1), np.round(self.goal_list[2][self.count],1),
                                        np.round(self.goal_list[3][self.count],1), np.round(self.goal_list[4][self.count],1))
        print(f"goal count : {self.count} , goal : {np.round(self.goal_list[1][self.count],1)},{np.round(self.goal_list[2][self.count],1)}")
        time.sleep(5)
        self.pub.publish(self.goal)
        print("delray 4sec end")

    def firstGoal(self):
        self.goal = self.getPoseStamped(self.goal_list[1][0], self.goal_list[2][0], self.goal_list[3][0],self.goal_list[4][0])
        self.delray()
        self.pub.publish(self.goal)


def main(args=None):
    rclpy.init(args=args)
    node = turtlebot4_pub_path()
    # node.open_path_file()
    # node.firstGoal()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()