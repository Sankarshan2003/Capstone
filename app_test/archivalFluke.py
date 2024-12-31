import robotInterfaces as rb
import time
max_height = 140
height_offset = 0
x_offset = 0
y_offset = 0

robot = rb.Robot('dobot', 'COM14')
robot.gripper(0)
time.sleep(3)
robot.gripper(1)
#robot.move_to(0,255,0,0,0)
time.sleep(3)
while(True):
    robot.move_to(100,255,0,0,1)
    robot.move_to(85,255,0,0,1)
    time.sleep(0.1)

