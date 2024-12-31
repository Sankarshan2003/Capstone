import robotInterfaces as rb
import barcodeReader as barReader
robot = rb.Robot('gantry', 'COM15')

#VTReader = barReader.BarcodeReader("COM9")
robot.home()
#robot.move_to(155,112,110,1,120)
x_offset=0
y_offset=0
height_offset=0
rhead = 50
max_height=45

def robot_pick(pose):	 
    pose = [int(num) for num in pose]
    print("Robot Pose:",pose)
    
    x,y,z = pose
    x = x + x_offset
    y = y + y_offset
    z = z + height_offset
    rHead = 49
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,z,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)
def robot_place(pose):	 
    x,y,z = pose
    rHead = 49
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,rHead,0)

source = [(90,98,165)]
dest = [(397.5,100,160)]
tt_filled = [48]
row=0
for i,l in zip(source,dest):
    j = tt_filled[source.index(i)]

    while(j!=0):
            for k in range(0,4 if j>=4 else j):
                xs,ys,zs = i
                xs =xs + 22*row
                ys=ys+ 21*k
                robot_pick((xs,ys,zs))
                xd,yd,zd = l
                xd = xd + 22*row
                yd = yd+21*k
                robot_place((xd,yd,zd))
                j-=1
            row += 1
    row =0
            

             