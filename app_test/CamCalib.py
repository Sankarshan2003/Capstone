import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Function to get the pixel coordinates
def get_pixel_coords(event, x, y, flags, param):
    global pixel_coords
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_coords = (x, y)

# Initialize the pixel coordinates
pixel_coords = None

# Create a window and set the mouse callback
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', get_pixel_coords)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check if a point is selected
    if pixel_coords is not None:
        # Draw a circle at the selected point
        cv2.circle(frame, pixel_coords, 5, (0, 0, 255), -1)

        # Display the pixel coordinates
        print(f"Pixel Coordinates: {pixel_coords}")

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()