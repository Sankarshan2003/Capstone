import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import time
import objDetInterface as objDet

robotPort = {'type': 'gantry', 'port': 'COM4'}
# robotPort = {'type': 'dobot', 'port': 'COM10'}

robot = rb.Robot(robotPort['type'], robotPort['port'])

# obj = objDet.ObjDet('BG',bg='bg.png')
obj = objDet.ObjDet('yolo',folder_path=r'E:\University\RAIS\scripts\yolo_img_p\yolov5', model_path=r"E:\University\RAIS\scripts\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.85)

rs = cam.RSCamera([640,480],30)

bg_captured = False
if robotPort['type'] == 'dobot':
    max_height = 130
    height_offset = 0
    x_offset = 10
    y_offset = -6
    
    dest = [-25,-275,max_height]
    rest_pos = [0, 255, 90, 0, 0]
    
elif robotPort['type'] == 'gantry':
    robot.home()
    
    max_height = 20
    height_offset = 0
    x_offset = 9
    y_offset = -2
    
    dest = [400,150,max_height]
    rest_pos = [273, 400, 0, 3, 0]

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
    pose = [int(num) for num in pose]
    dest = [int(num) for num in dest]
    print("Robot Pose:",pose)
    print("Robot Dest:",dest)
    
    x,y,z,rHead = pose
    x = x + x_offset
    y = y + y_offset
    z = z + height_offset
    
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,z,rHead,1)
    time.sleep(0.5)
    robot.move_to(x,y,max_height,rHead,1)
 
    x,y,z = dest
 
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,0,0)

def main():
    while True:
        print("1. Capture Background \n2. Pick and Place \n4. Exit")
        opt = int(input())
        if opt == 1:
            robot.move_to(*rest_pos)
            capture_bg()
            obj.update_bg('bg.png')
        if opt == 2:
            robot.move_to(*rest_pos)
            time.sleep(1)
            
            depth, color = rs.get_frames()
            center_coords = obj.get_center_coord(color) #center x, center y, orientation
            print(center_coords)
            
            for i, center in enumerate(center_coords):
                cam_obj_coord = rs.deproject(center[0],center[1],depth)
                print("deproject",cam_obj_coord)
                cam_obj_coord.append(center[2])
                robot_pose = robot.transformation(cam_obj_coord)
                print(robot_pose)
                if robot_pose is not None:
                    robot_pick_place(robot_pose,dest)
        
        if opt == 3:
            robot.gripper(0)
            time.sleep(1)
            robot.gripper(1)
        if opt == 4:
            break
        
if __name__ == "__main__":
    try:
        main()
    finally:
        rs.stop_pipeline()
