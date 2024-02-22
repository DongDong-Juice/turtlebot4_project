# turtlebot4_project
터틀봇 경로 계획 테스트 

종속 및 필수 실행:
SLAM으로 생성된 지도
turtlebot4_navigation localization.launch map:=/{맵이 있는 경로}/맵이름.yaml
turtlebot4_navigation nav2.launch
turtlebot4_viz view_robot.launch (경로 생성 시 필요)

실행:
ros2 launch turtlebot4_path_planning turtlebot4_global_path (경로 생성) 
ros2 launch turtlebot4_path_planning turtlebot4_pub_path (경로 주행) 

부가 설명:
경로 생성의 경우 rviz를 통해 2d goal pose 토픽의 데이터를 저장하여 ctrl+c 입력으로 스크립트 종료시 최종 json 파일 포맷으로 저장 

경로 주행의 경우 사전에 map 디렉토리에 생성된 path.json 파일을 파싱해서 goal_pose 토픽을 발행하는 것으로 동작함
