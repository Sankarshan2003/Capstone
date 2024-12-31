import cv2
import cv2.aruco as aruco

# Load the dictionary for 5x5 markers
# dictionary = aruco.Dictionary_get(aruco.DICT_5X5_250)


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)


# Load the camera parameters
camera_matrix = ...  # Replace with your camera matrix
distortion_coefficients = ...  # Replace with your distortion coefficients

# Initialize the detector parameters
# parameters = aruco.DetectorParameters_create()

# Create a video capture object
cap = cv2.VideoCapture(1)  # Use 0 for the default camera, or provide a video file path

while True:
    # Capture a frame from the video
    ret, frame = cap.read()
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    # frame = cv.imread(...)

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    # Detect ArUco markers in the frame
    # corners, ids, rejected_img_points = aruco.detectMarkers(frame, dictionary, parameters=parameters,)

    # Draw the detected markers on the frame
    aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

    # Display the frame
    cv2.imshow('ArUco Marker Detection', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()