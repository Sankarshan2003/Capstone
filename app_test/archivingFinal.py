from flask import Flask
from flask_cors import CORS
import socketio
import time
import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import robotInterfaces as rb
import objDetInterface as objDet
import barcodeReader as barReader
import time
import archiving_funcs as func
import pallet_pos as pPos
max_height = 15
height_offset = 12
x_offset = 10
y_offset = -3
capture_pos = [355.5, 273, 0, 3, 0]
# Create a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
def robot_pick(robot,pose,dest):	 
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


def robot_place(robot,pose,dest):	 
    dest = [int(num) for num in dest]
    print("Robot Dest:",dest)
  
    x,y,z,rHead = pose

    x,y,_ = dest
 
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,max_height,rHead,1)
    robot.move_to(x,y,z,rHead,0)
    robot.move_to(x,y,max_height,0,0)


def dest_coord(barcode):

    print("barcode",barcode)
    if barcode != None:
        #dest_pallet_id = func.search_csv_by_tt_id("",barcode)
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
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)  
    #sio.emit('cmdStatus', {'status': 'connected'}, to=sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def robotCmd(sid, data):
    print('Received command:', data)
    try:
        rs = cam.RSCamera([640,480],30) #init camera
        VTReader = barReader.BarcodeReader("COM3")
# DestPalletReader = barReader.BarcodeReader("COM4")
        obj = objDet.ObjDet('yolo',folder_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5', model_path=r"C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\yolo_img_p\yolov5\runs\train\exp\weights\last.pt", conf=0.80,mode='src')
#destmodel = objDet.ObjDet('','',model_path=r'C:\Users\sanka\OneDrive\Desktop\capstone\oldGantryRobot\train2\weights\best.pt',conf=0.35,type='dest')
        robot = rb.Robot('gantry', 'COM3')
        sio.emit('cmdStatus', {'status': 'connected'}, to=sid)
        time.sleep(2)
        sio.emit('cmdStatus',{'status':'homing'})
        robot.home()
        sio.emit('cmdStatus',{'status':'capture'}, to=sid)
        robot.move_to(*capture_pos)
        print("Moved to capture position")
        depth, color = rs.get_frames()
        center_coords = obj.get_center_coord(color)
        l = {'S3':['A12']}
        sio.emit('cmdStatus',{'status':'render','payload':l})
        for i, center in enumerate(center_coords):
         cam_obj_coord = rs.deproject(center[0],center[1],depth)
         print("deproject",cam_obj_coord)
         cam_obj_coord.append(center[2])
         robot_pose = robot.transformation(cam_obj_coord,'src')
         print(robot_pose)
         if robot_pose is not None:
            robot_pick(robot,robot_pose,dest)
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
                # ret,barcode = VTReader.readBarcode(0.75)
                # print(ret)
            
            robot.rotate_gripper(5)
            # if ret:
            print(barcode)
            dest = dest_coord(barcode)
            print(dest)
            robot_place(robot,robot_pose,dest)
        
        robot.move_to(*capture_pos)

       
        time.sleep(2) ##Place the test tubes
        p = {'S1':'A1','D1':'A1'}
        sio.emit('cmdStatus',{'status':'place','payload':p})
        print("Sent")

    except Exception as e:
        print(e)
        sio.emit('cmdStatus',{'status':'error','emsg':str(e)})
    
if __name__ == '__main__':
    app.run(port=8080)


