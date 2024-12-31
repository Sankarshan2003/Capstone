import robotInterfaces as rb
import time
import barcodeReader as barReader
robot = rb.Robot('gantry', 'COM15')
robot.home()
samples = 100
for i in range(0,samples):
    '''
    robot.move_to(600,0,150,0,1)
    time.sleep(1)
    robot.move_to(600,0,0,0,1)
    time.sleep(1)
    robot.move_to(600,50,150,0,1)
    time.sleep(1)
    robot.move_to(600,50,0,0,1)
    time.sleep(1)
    robot.move_to(640,0,0,0,1)
    time.sleep(1)
    robot.move_to(640,0,150,0,1)
    time.sleep(1)
    robot.move_to(640,0,0,0,1)
    time.sleep(1)
    robot.move_to(640,50,150,0,1)
    time.sleep(1)
    robot.move_to(640,50,0,0,1)
    time.sleep(1)
    robot.move_to(600,0,0,0,1)
    time.sleep(1)
    '''
    robot.move_to(300,0,150,0,1)
    time.sleep(1)
    robot.move_to(300,0,0,0,1)
    time.sleep(1)
    robot.move_to(640,0,150,0,1)
    time.sleep(1)
    robot.move_to(640,0,0,0,1)
    time.sleep(1)
