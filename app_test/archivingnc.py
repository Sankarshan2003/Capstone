import robotInterfaces as rb
import barcodeReader as barReader
import cameraModules.realsense.camera_rs as cam
import objDetInterface as objDet
rs = cam.RSCamera([640,480],30)
robot = rb.Robot('gantry', 'COM15')
import time
#VTReader = barReader.BarcodeReader("COM9")
obj = objDet.ObjDet('yolo',folder_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5', model_path=r"C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.80,mode='src')
robot.home()
#robot.move_to(155,112,110,1,120)
x_offset=-18
y_offset=-9
height_offset=0
rhead = 50
max_height=45

def robot_pick(pose):	 
    pose = [int(num) for num in pose]
    print("Robot Pose:",pose)
    
    x,y,z = pose
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
def transform(Cam):
    #print(Cam)
    xr = 226-Cam[1]+x_offset
    yr = 262+Cam[0]+y_offset
    print(yr)
    z = 165
    return (xr,yr,z)
dest = [(397.5,100,160)]

def main(): 
    l= 0
    j=0
    depth, color = rs.get_frames()
    center_coords = obj.get_center_coord(color) #center x, center y, orientation
    print(type(center_coords[0][1]))
    center_coords.sort(key=lambda x: x[1], reverse=True)
    print(center_coords)
    for i in center_coords:
        if(i[1]>106):
            cam_obj_coord = rs.deproject(i[0],i[1],depth)
            print("deproject",cam_obj_coord)
            robot_coord = transform(cam_obj_coord)
            print(robot_coord)
            robot_pick(robot_coord)
            x = dest[0][0] + 22* l
            y = dest[0][1] + 22*j
            robot_place([x,y,160])
            if(j==3):
                j=0
                l+=1
            else:
                j+=1

            
source = [(90,98,165)]

tt_filled = [48]
row=0
'''
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
'''     
if __name__ == '__main__':
    l= 0
    j=0
    while(True):
        ch = input("1)Archiving 2)Exit(e) ?")
        if ch == 'e':
            break
        else:
            main()
    

             