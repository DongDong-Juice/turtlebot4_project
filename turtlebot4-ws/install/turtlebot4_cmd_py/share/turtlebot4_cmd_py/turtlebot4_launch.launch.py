#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription(
        [
            # Node(
            #     package='turtlebot4_cmd_py',
            #     #namespace='turtlebot4_cmd_py',
            #     executable='Turtlebot4Ctl',
            #     name='sim',
            #     output='screen'
            #
            # ),
            Node(
                package='turtlebot4_cmd_py',
                executable='test',
                name='turtlebot_control',
                output='screen',
            ),
            Node(
                package='turtlebot4_cmd_py',
                executable='test1',
                name='turtlebot_control',
                output='screen',
            ),
            Node(
                package='turtlebot4_cmd_py',
                executable='test2',
                name='turtlebot_control',
                output='screen',
            ),
        ]
    )
