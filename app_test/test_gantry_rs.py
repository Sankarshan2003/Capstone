import robotInterfaces as rb
import time
import objDetInterface as objDet
import cv2 as cv
import cameraModules.realsense.camera_rs as cam
import numpy as np

rs = cam.RSCamera([640,480],30)


obj = objDet.ObjDet('yolo',folder_path=r'E:\University\RAIS\scripts\yolo_img_p\yolov5', model_path=r"E:\University\RAIS\scripts\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.85)
# obj = objDet.ObjDet('BG',bg='bg.png')
robot = rb.Robot('gantry', 'COM9')

robot.home()
print("asdfe")
robot.move_to(0,400,0)
robot.move_to(250,400,0)


# time.sleep(4)
_, color = rs.get_frames()
imgg = color
center_coords = obj.get_center_coord(imgg)
print(center_coords)


for i, center in enumerate(center_coords):
	cam_obj_coord = rs.deproject(center[0],center[1])
	print("deproject",cam_obj_coord)
	cam_obj_coord.append(center[2])
	robot_pose = robot.transformation(cam_obj_coord)
	# print(robot_pose)
	# robot_pose.append(center[2])
	print(robot_pose)

	robot.move_to(robot_pose[0],robot_pose[1],0,gripper_state=0,rHead=robot_pose[3])
	robot.move_to(robot_pose[0],robot_pose[1],robot_pose[2]-5,gripper_state=0,rHead=robot_pose[3])
	robot.move_to(robot_pose[0],robot_pose[1],robot_pose[2]+15,gripper_state=1,rHead=robot_pose[3])
	robot.move_to(robot_pose[0],robot_pose[1],robot_pose[2],gripper_state=1,rHead=robot_pose[3])
	robot.move_to(robot_pose[0]+100,robot_pose[1]+100,robot_pose[2],gripper_state=0,rHead=robot_pose[3])

