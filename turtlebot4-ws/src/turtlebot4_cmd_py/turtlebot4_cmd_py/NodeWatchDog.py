import os
import psutil
import subprocess
from multiprocessing import Process


#첫 실행 시 살아있는지 판별을 위한 핸들러
handle ={}
#실행할 노드들의 이름
node_list=['test','test1','test2','Turtlebot4Ctl']
#명령어 패키지까지 정의
fileName = "ros2 run turtlebot4_cmd_py "
#관리할 노드 일괄 실행
for i in range(0,len(node_list)):
    handle[i]=subprocess.Popen(fileName+repr(node_list[i]),shell=True)
#자식프로세스가 죽었을 경우 반환값 확인해서 재 실행 및 키보드 종료를 위한 try, except
try:
    while 1:
        for i in range(len(handle)):
            if handle[i].poll() == 1:#핸들러의 자식 프로세스가 죽었을 경우
                handle[i] = subprocess.Popen(fileName + repr(node_list[i]), shell=True)
except KeyboardInterrupt:
     print("종료")
     exit()










