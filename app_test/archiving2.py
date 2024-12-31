import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import objDetInterface as objDet
import barcodeReader as barReader
import time
import archiving_funcs as func
import pallet_pos as pPos
import multiprocessing
rs = cam.RSCamera([640,480],30) #init camera
VTReader = barReader.BarcodeReader("COM4")
# DestPalletReader = barReader.BarcodeReader("COM4")
obj = objDet.ObjDet('yolo',folder_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5', model_path=r"C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.90)
robot = rb.Robot('gantry', 'COM3')
robot.home()
print("LOL")
max_height = 20
height_offset = 0
x_offset = 16
y_offset = -1
dest = [400,150,max_height]
capture_pos = [340, 90, 0, 3, 0]

def main():
    dest = [400,150,max_height]
    robot.move_to(*capture_pos)
    time.sleep(1)
    print("Moved to capture position")
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
            robot_pick(robot_pose,dest)
            start_time = time.time()
            barcode = None
            print("Reading barcode")
            ret,barcode=0,0
            print(VTReader)
            #while barcode!=0 and VTReader != None:
               # ret,barcode = VTReader.readBarcode(0.75)
            #ret,barcode = VTReader.readBarcode(0.75)
            try:
                ret,barcode = VTReader.readBarcode(0.75)
            except Exception as e:
                print(e)
            #ret,barcode = VTReader.readBarcode(0.75)
            print("first attempt failed",ret)
            while not ret and (time.time() - start_time) <= 3:
                # curr_pose = robot.get_pose()
                # print("inside rotation")
                # print(curr_pose[3])
                while not ret and robot.get_pose()[3] < 180:
                    if(VTReader!=None):
                        robot.rotate_gripper(robot.get_pose()[3]+60)
                        print("rotate gripper:",robot.get_pose()[3]+60)
                    # time.sleep(0.25)
                    try:
                        ret,barcode = VTReader.readBarcode(0.5)
                    except Exception as e:
                        print(e)
                    # print(ret)
                        if not ret or robot.get_pose()[3] >= 180:
                        # barcode = None
                            break    
                # ret,barcode = VTReader.readBarcode(0.75
    robot.move_to(*capture_pos)
        
if __name__ == "__main__":
    while True:
        print("1. Archive \n2. Exit")
        opt = input()
        if opt == "1":
            main()
        if opt == "2":
            break
        else:
            pass