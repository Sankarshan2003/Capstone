import robotInterfaces as rb
import time

# robot_1 = rb.Robot('dobot', 'COM10')
robot_1 = rb.Robot('gantry', 'COM9')
time.sleep(2)
robot_1.home()

print(robot_1.get_pose()) 


# robot_1.gripper(1)
# time.sleep(1)
robot_1.move_to(200,115,rHead=40,gripper_state=1)
# time.sleep(1)
print(robot_1.get_pose()) 
robot_1.move_to(500,315,rHead=40,gripper_state=0)
print(robot_1.get_pose()) 
# robot_1.move_to(200,115,rHead=40,gripper_state=1)
# time.sleep(1)
# robot_1.gripper(0)