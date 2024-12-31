import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import time
import objDetInterface as objDet
import random

# cls_freq = 38
# opn_freq = 27

# pwr_pin = 13
# pwm_pin = 14
# Dobot raised by 69mm

def get_dest():
    temp = random.randint(0,5)
    if temp == 0:
        return [90,190,max_height]
    elif temp == 1:
        return [17,197,max_height]
    elif temp == 2:
        # return [-45,190,max_height]
        return [17,197,max_height]
    elif temp == 3:
        return [90,-190,max_height]
    elif temp == 4:
        return [17,-197,max_height]
    elif temp == 5:
        # return [-45,-190,max_height]
        return [17,-197,max_height]

robot = rb.Robot('dobot', 'COM10')
# robot = rb.Robot('gantry', 'COM9')
# obj = objDet.ObjDet('BG',bg='bg.png')
obj = objDet.ObjDet('yolo',folder_path=r'E:\University\RAIS\scripts\yolo_img_p\yolov5', model_path=r"E:\University\RAIS\scripts\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.85)
# robot.home()
rs = cam.RSCamera([640,480],30)

bg_captured = False
max_height = 120
height_offset = 0
x_offset = -10
y_offset = -5

robot.gripper(0)

def capture_bg():
    print("Prep the workspace for background capture...")
    for i in range(3,0):	
        print(i)
        time.sleep(1)
    _, color_image = rs.get_frames()
    cv.imshow("imageeeee", color_image)
    cv.waitKey()
    cv.imwrite("bg.png", color_image)


def robot_pick_place(pose,dest):	 
    print("Robot Pose:",pose)
    print("Robot Dest:",dest)
    x,y,z,rHead = pose
    x = x + x_offset
    y = y + y_offset
    z = z + height_offset
    # rHead = -rHead
    print(x,y,z,rHead)
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,z,rHead,1)
    time.sleep(0.5)
    robot.move_to(x,y,max_height,rHead,1)
 
    x,y,z = dest
 
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,30,rHead,0)
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,0,0)

def main():
    while True:
        print("1. Capture Background \n2. Pick and Place \n3. Exit")
        opt = int(input())
        if opt == 1:
            # pass
            robot.move_to(0, 255, 90, 0, 0)
            capture_bg()
            obj.update_bg('bg.png')
        if opt == 2:
            # dest = [-25,-275,max_height]
            robot.move_to(0, 255, 90, 0, 0)
            time.sleep(1)
            depth, color = rs.get_frames()
            center_coords = obj.get_center_coord(color)
            
            print(center_coords)
            for i, center in enumerate(center_coords):
                cam_obj_coord = rs.deproject(center[0],center[1],depth)
                cam_obj_coord.append(center[2])
                print("deproject",cam_obj_coord)
                robot_pose = robot.transformation(cam_obj_coord)
                # print(robot_pose)
                # robot_pose.append(center[2])
                dest = get_dest()
                # print(dest)
                robot_pick_place(robot_pose,dest)
        if opt == 3:
            break
  
if __name__ == "__main__":
    try:
        main()
        # robot.gripper(1)
        # time.sleep(1)
        # robot.gripper(0)
    finally:
        rs.stop_pipeline()
