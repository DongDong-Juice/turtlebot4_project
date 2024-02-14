from setuptools import find_packages, setup
from setuptools import setup
import os
from glob import glob
package_name = 'turtlebot4_cmd_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dong',
    maintainer_email='dong@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            #첫번째 입력된 값이 executable 즉 "ros2 run 패키지명 test " 처럼 됨
            'Turtlebot4Ctl = turtlebot4_cmd_py.turtlebot4_ctl:main',
            'test = turtlebot4_cmd_py.pross:main',
            'test1 = turtlebot4_cmd_py.pross1:main',
            'test2 = turtlebot4_cmd_py.pross2:main',
            'pub = turtlebot4_cmd_py.pub:main',
            'sub = turtlebot4_cmd_py.sub:main',

        ],
    },
)
