import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped,PoseWithCovarianceStamped
import json
import numpy as np
from rclpy.clock import Clock
from rclpy.qos import *
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import math




class turtlebot4_pub_path(BasicNavigator):
    def __init__(self):
        super().__init__('turtlebot4_pub_path')
        qos = QoSProfile(reliability=QoSReliabilityPolicy.BEST_EFFORT,
                         depth=10,
                         durability=QoSDurabilityPolicy.VOLATILE)
        #goal_pose는 도착점을 넘겨주는 역활 ,amcl_pose는 현재 로봇의 좌표를 기반으로 도착점에 도착해는지 확인 하는 토픽
        self.pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        # self.goal_pub = self.create_publisher(PoseWithCovarianceStamped, 'amcl_pose',10)
        self.robot_pose = self.create_subscription(PoseWithCovarianceStamped,
                                                   'amcl_pose',
                                                   self.checking_robot_pose,
                                                   10)
        # self.robot_pose_goal = self.create_subscription(PoseStamped, 'goal_pose', self.checking_robot_pose_goal, 10)
        self.robot_pose_goal = self.create_subscription(PoseStamped, 'goal_pose', self.checking_robot_pose_goal, 10)
        self.goal = PoseStamped()
        # self.goal.header.frame_id = 'map'
        # self.goal.header.stamp = self.get_clock().now().to_msg()
        # self.goal.pose.position.x = 0.0
        # self.goal.pose.position.y = 0.0
        # self.goal.pose.position.z = 0.0
        # self.goal.pose.orientation.x = 0.0
        # self.goal.pose.orientation.y = 0.0
        # self.goal.pose.orientation.z = 0.0
        # self.goal.pose.orientation.w = 0.0
        # print("첫쨰 ")
        # print(self.goal)
        self.goal_list = np.empty(shape=4)
        self.robot_pose_list = np.empty(shape=3)

    def getPoseStamped(self, positionX, positionXY, rotationZ, rotationW ):
        """
        Fill and return a PoseStamped message.

        :param position: A list consisting of the x and y positions for the Pose. e.g [0.5, 1.2]
        :param rotation: Rotation of the pose about the Z axis in degrees.
        :return: PoseStamped message
        """
        pose = PoseStamped()

        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = positionX
        pose.pose.position.y = positionXY

        # Convert Z rotation to quaternion
        pose.pose.orientation.z = rotationZ
        pose.pose.orientation.w = rotationW
        return pose

    def checking_robot_pose_goal(self, msg):
        print(self.robot_pose_goal)
        print("실제로 받은거")
        print(msg)

    def open_path_file(self):
        with open('/home/dong/turtlebot4_project/turtlebot4-ws/src/turtlebot4_path_planning/path/path.json','r') as f:
            data = json.load(f)
            # index = self.data[0]['index']
        self.path_plan_data(data)
        print("경로 업로드")

    def path_plan_data(self, data):
        index = [i['index'] for i in data]
        x = [i['x'] for i in data]
        y = [i['y'] for i in data]
        z = [i['z'] for i in data]
        w = [i['w'] for i in data]
        self.goal_list = [index, x, y, z, w]

    def checking_robot_pose(self, msg): #데이터를 지속적으로 받아와서 현재 경로의 값에 근접한지 확인
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        self.robot_pose_list = [x, y, z, w]
        print("로봇의 현재 좌표")

    def going_path_plan(self):
        self.goal = self.getPoseStamped(self.goal_list[1][0],self.goal_list[2][0], self.goal_list[3][0],self.goal_list[4][0])
        self.pub.publish(self.goal)
        print("실행")
        print(self.goal)
        count = 0
        while 1:
            if np.round(self.robot_pose_list[0],2) <= np.round(self.goal_list[1][count],2) and np.round(self.robot_pose_list[1],2) <= np.round(self.goal_list[2][count],2):
                print("실행함?")
                self.goal = self.getPoseStamped(self.goal_list[1][count], self.goal_list[2][count], self.goal_list[3][count],self.goal_list[4][count])
                self.pub.publish(self.goal)
                count += 1
            elif count == 4:
                break
            else:
                pass


def main(args=None):
    rclpy.init(args=args)
    node = turtlebot4_pub_path()
    node.open_path_file()
    node.going_path_plan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()