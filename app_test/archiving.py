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
VTReader = barReader.BarcodeReader("COM9")
# DestPalletReader = barReader.BarcodeReader("COM4")
obj = objDet.ObjDet('yolo',folder_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5', model_path=r"C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.80,mode='src')
#destmodel = objDet.ObjDet('','',model_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\train2\weights\best.pt',conf=0.35,type='dest')
robot = rb.Robot('gantry', 'COM7')
conn = func.connect_to_db()
robot.home()
print("LOL")
max_height = 10
height_offset = 2
x_offset = 18
y_offset = 0
dest = [400,150,max_height]
capture_pos = [355.5, 273, 0, 1, 60]
def robot_pick(pose,dest):	 
    pose = [int(num) for num in pose]
    print("Robot Pose:",pose)
    
    x,y,z,rHead = pose
    x = x + x_offset
    y = y + y_offset
    z = z + height_offset
    rHead = 60
    robot.move_to(x,y,max_height,rHead,0)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,z,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)


def robot_place(pose,dest):	 
    dest = [int(num) for num in dest]
    print("Robot Dest:",dest)
  
    x,y,z,rHead = pose
    rHead = 60
    x,y,_ = dest
 
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,rHead,0)


def dest_coord(barcode):

    print("barcode",barcode)
    if barcode != None:
        dest_pallet_id = func.search_csv_by_tt_id("",barcode)
        #print(dest_pallet_id)
        #dest_pallet_id = func.search_db(conn,barcode)
        print(dest_pallet_id)
    else:
        dest_pallet_id = "0"
        
    # dest_pallet_id = "2"
    pallet_coord = pPos.dest_pallet_coord[int(dest_pallet_id)]
    pallet_empty_slot = func.get_emp_slot(pPos.dest_pallet[int(dest_pallet_id)])
    print(dest_pallet_id,pPos.dest_pallet[int(dest_pallet_id)])
    pallet_empty_slot = func.tray_id_to_xy(pallet_coord,pallet_empty_slot[0],pallet_empty_slot[1],"dest")
    dest = [pallet_empty_slot[0], pallet_empty_slot[1], max_height]
    return dest
# while True:
def main():
    dest = [400,150,max_height]
    robot.move_to(*capture_pos)
    time.sleep(1)
    print("Moved to capture position")
    depth, color = rs.get_frames()
    center_coords = obj.get_center_coord(color) #center x, center y, orientation
    print(type(center_coords[0][1]))
    center_coords.sort(key=lambda x: x[1], reverse=True)
    print(center_coords)
    k=0

    for i, center in enumerate(center_coords):
        cam_obj_coord = rs.deproject(center[0],center[1],depth)
        print("deproject",cam_obj_coord)
        cam_obj_coord.append(center[2])
        robot_pose = robot.transformation(cam_obj_coord,'src')
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
                    if(True):
                        robot.rotate_gripper(robot.get_pose()[3]+60)
                        print("rotate gripper:",robot.get_pose()[3]+60)
                    # time.sleep(0.25)
                    try:
                        ret,barcode = VTReader.readBarcode(0.5)
                    except Exception as e:
                        print(e)
                        barcode = 0
                    # print(ret)
                        if not ret or robot.get_pose()[3] >= 180:
                        # barcode = None
                            break    
                # ret,barcode = VTReader.readBarcode(0.75)
                # print(ret)
            
            robot.rotate_gripper(5)
            # if ret:
            print(barcode)
            dest = dest_coord(barcode)
            print(dest)
            robot_place(robot_pose,dest)
    robot.move_to(*capture_pos)
        
if __name__ == "__main__":
    while True:
        print("1. Archive \n2. Exit")
        opt = input()
        if opt == "1":
            main()
        if opt == "2":
            func.disconnect_from_db(conn)
            break
        else:
            pass