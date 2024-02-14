
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import rclpy
from rclpy.qos import QoSProfile
from rclpy.node import Node

import sys, select, termios, tty

from std_msgs.msg import String
settings = termios.tcgetattr(sys.stdin)

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   q    w    e
   a    s    d
   z    x    c

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
aeasdfawefawe
"""
moveBindings = {
		'w':(1,0,0,0),
        'a':(0,0,0,1),
        's':(-1,0,0,0),
		'd':(0,0,0,-1),

        'e':(1,0,0,-1),
		'q':(1,0,0,1),
		'c':(-1,0,0,1),
		'z':(-1,0,0,-1),

        'W':(1,0,0,0),
        'A':(0,0,0,1),
        'S':(-1,0,0,0),
		'D':(0,0,0,-1),

        'E':(1,0,0,-1),
		'Q':(1,0,0,1),
		'C':(-1,0,0,1),
		'Z':(-1,0,0,-1),
	       }

speedBindings={
		'q':(1.1,1.1),
		'z':(.9,.9),
		'w':(1.1,1),
		'x':(.9,1),
		'e':(1,1.1),
		'c':(1,.9),
	      }


class Turtlebot4Ctl(Node):
    def __init__(self):
        super().__init__('Turtlebot4Ctl')
        self.speed = 0.5
        self.turn = 1.0
        self.x, self.y,self.z,self.th = 0, 0, 0, 0
        self.status = 0

        self.select = int(input())
        if self.select == 1:
            self.turtlebot4_keyboard_ctl_sub = self.create_subscription(
                Twist,
                '/cmd_vel',
                self.turtlecmd,
                10)
        elif self.select == 2:
            self.turtlebot4_joy_ctl_sub = self.create_subscription(
            Joy,
            '/joy',
            self.turtlejoy,
            10)

        self.Node_Management_pub = self.create_publisher(
            bool,
            'Node_Management',
            10)
        self.turtlebot4_ctl_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

    #키보드 입력값 들어오면 실행할 함수
    def turtlecmd(self,msg):
        while (1):
            key = self.getKey()
            if key in moveBindings.keys():
                self.x = moveBindings[key][0]
                self.y = moveBindings[key][1]
                self.z = moveBindings[key][2]
                self.th = moveBindings[key][3]
            elif key in speedBindings.keys():
                self.speed = self.speed * speedBindings[key][0]
                self.turn = self.turn * speedBindings[key][1]

                print(self.vels(self.speed, self.turn))
                if (self.status == 14):
                    print(msg)
                self.status = (self.status + 1) % 15
            else:
                self.x = 0
                self.y = 0
                self.z = 0
                self.th = 0
                break

            twist = Twist()
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = self.th * self.turn
            self.turtlebot4_ctl_pub.publish(twist)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def turtlejoy(self,msg):
        axes = msg.axes
        buttons = msg.buttons
        print("누름 ")
        print(axes[0])
        print("누름 2 ")
        print(axes[1])
        twist = Twist()
        twist.linear.x = axes[1]
        twist.angular.z = axes[0]
        self.turtlebot4_ctl_pub.publish(twist)

    #터미널에 입력한 키 값 가져오기
    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def vels(self, speed, turn):
        return "currently:\tspeed %s\tturn %s " % (speed, turn)


def main(args=None):
    if args is None:
        args = sys.argv
    print("모드를 선택하세요")
    print("1번 Keyboard")
    print("2번 JoyStick")
    rclpy.init(args=args)
    node = Turtlebot4Ctl()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:

        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

