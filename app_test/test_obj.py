import objDetInterface as objDet
import cv2 as cv
import cameraModules.realsense.camera_rs as cam
import numpy as np

rs = cam.RSCamera([640,480],30)
_, color = rs.get_frames()
_, color = rs.get_frames()

obj = objDet.ObjDet('yolo',folder_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5', model_path=r"C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.80)

# obj = objDet.ObjDet('BG',bg='bg.jpg')


imgg = color
# imgg = cv.imread('img6.jpg')
# imgg2 = cv.imread('bg.jpg')
# print(type(imgg2))
# cv.imshow('asdasd',imgg)
# cv.waitKey()
center_coords = obj.get_center_coord(np.array(color))
# orientation = obj.get_orientation(imgg)
for center in center_coords:
    print(center)
    imgg = cv.circle(imgg, (int(center[0]),int(center[1])), radius=0, color=(0, 0, 255), thickness=5) 
# print(orientation)
print(center_coords)
cv.imshow('asdasd',imgg)
cv.waitKey()