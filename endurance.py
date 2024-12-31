import app_test.robotInterfaces as rb
import time
gantry = rb.Robot('gantry','COM3')
print(gantry.robot)
gantry.home()
pos = [[200,100,0],[200,100,140],[200,100,0],[400,100,0],[400,100,140],[400,100,0]]
if __name__ =="__main__":
    while(True):
        for i in pos:
            gantry.move_to(*i)
        gantry.move_to(0,0,0)
2
