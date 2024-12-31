import robotInterfaces as rb
import time

robot_1 = rb.Robot('dobot', 'COM10')
robot_2 = rb.Robot('gantry', 'COM9')
time.sleep(2)
robot_2.home()

print(robot_1.get_pose()) 


# robot_1.gripper(1)
# time.sleep(1)
robot_1.move_to(200,15,rHead=40,gripper_state=1)
robot_2.move_to(200,15,rHead=40,gripper_state=1)
time.sleep(1)
robot_1.move_to(250,200,rHead=40,gripper_state=0)
robot_2.move_to(500,215,rHead=40,gripper_state=0)
# robot_1.move_to(200,115,rHead=40,gripper_state=1)
# time.sleep(1)
# robot_1.gripper(0)