import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import numpy as np

rs = cam.RSCamera([640,480],30)

while True:
    depth, color = rs.get_frames()
    
    # Get the dimensions of the color image
    height, width, _ = color.shape
    
    # Calculate the center of the image
    center_x, center_y = width // 2, height // 2
    
    # Draw a circle at the center of the image
    cv.circle(color, (center_x, center_y), 5, (0, 255, 0), 2)
    
    # Display the color image with the circle
    cv.imshow("Color Image", color)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()