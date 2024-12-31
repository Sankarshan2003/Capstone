import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import objDetInterface as objDet
import barcodeReader as barReader
import time
import archiving_funcs as func
import pallet_pos as pPos
rs = cam.RSCamera([640,480],30)
robot = rb.Robot('gantry', 'COM3')
robot.home()
mod = objDet.ObjDet(model_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\train2\weights\best.pt',conf=0.35,mode='dest')
capturePos = [608,334,0,1,0]
max_height = 20
x_offset=0
y_offset=0
height_offset=0
def robot_pick(pose,dest):	 
    pose = [int(num) for num in pose]
    print("Robot Pose:",pose)

    x,y,z,rHead = pose
    x = x + x_offset
    y = y + y_offset
    z = z + height_offset
    
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    # while True:
        # pass
    robot.move_to(x,y,z,rHead,1)
    # time.sleep(0.5)
    robot.move_to(x,y,max_height,rHead,1)


def robot_place(pose):	 
    #dest = [int(num) for num in dest]
    #print("Robot Dest:",dest)
  
    x= pose[0]
    y=pose[1]
    z=pose[2]
    rHead = 0

    #x,y,_ = dest
 
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,0,0)

def main():
    robot.move_to(*capturePos)
    depth, color = rs.get_frames()
    try:
        center_coords = mod.getd_center_coord(color) #center x, center y, orientation
        print(center_coords)
        center = center_coords[0]
        print(center)
        print(depth)
        cam_obj_coord = rs.deproject(center[0],center[1],depth)
        cam_obj_coord.append(0)
        print("deproject",cam_obj_coord)
        robot_pose = robot.transformation(cam_obj_coord,'dest')
        print(robot_pose)
        robot_place(robot_pose)
    except Exception as e:
        print(e)
if __name__ =="__main__":
    while(True):
        opt = int(input("1. Capture Background \n3. Exit"))
        if opt == 1:
            main()
        if opt == 2:
            break
        else:
            pass



