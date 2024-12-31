import cameraModules.realsense.camera_rs as cam
import cv2
import numpy as np
import cv2.aruco as aruco

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)


object_coords = [[191,278,0],[191,-278,0],[-191,-278,0],[-191,278,0]]
object_coords_sorted = []
depth_coords=[]

rs = cam.RSCamera([640,480],30)
depth, frame = rs.get_frames()
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# frame = cv.imread(...)

markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(depth.get_data()), alpha=0.03), cv2.COLORMAP_JET)
# print(marker)

for i,Corners in enumerate(markerCorners):
# Corners = markerCorners[1]
    coord = Corners[0][0]
    cam_obj_coord = rs.deproject(int(coord[0]),int(coord[1]),depth)
    depth_coords.append(cam_obj_coord)
    object_coords_sorted.append(object_coords[markerIds[i][0]])
    print("id:",markerIds[i])
    print(int(coord[0]),int(coord[1]))
    cv2.circle(frame, (int(coord[0]),int(coord[1])), 5, (0, 255, 0), 2)
    cv2.circle(frame, (343,245), 5, (0, 255, 0), 2)

print(depth_coords)
print(object_coords_sorted)

cv2.imshow("sadsad",frame)
cv2.waitKey()

    
print("center_cam_coord:",rs.deproject(343,245,depth))
# while True:
#     # Capture a frame from the video
#     # ret, frame = cap.read()
    
# 	# cv2.imshow("Color Image", color)
#     parameters =  cv2.aruco.DetectorParameters()
#     detector = cv2.aruco.ArucoDetector(dictionary, parameters)

#     # frame = cv.imread(...)

#     markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
#     # Detect ArUco markers in the frame
#     # corners, ids, rejected_img_points = aruco.detectMarkers(frame, dictionary, parameters=parameters,)

#     # Draw the detected markers on the frame
#     aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

#     # Display the frame
#     cv2.imshow('ArUco Marker Detection', frame)

#     # Exit the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# Release the video capture object and close all windows
# cap.release()
# cv2.destroyAllWindows()