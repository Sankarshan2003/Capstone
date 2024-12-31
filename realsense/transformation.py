import cv2
import numpy as np

# Define the corresponding points in the two coordinate systems
pts1 = np.array([[-50, -80], [0, -80], [50, -80], [-50, 40], [0, 40], [50, 40]], dtype=np.float32)
pts2 = np.array([[120, 30], [120, -20], [120, -70], [0, 30], [0, -20], [0, -70]], dtype=np.float32)

# Add a fixed z-coordinate for each point
z_coord = 60
pts1_3d = np.hstack((pts1, np.full((pts1.shape[0], 1), z_coord))).reshape(-1, 3)
pts2_3d = np.hstack((pts2, np.full((pts2.shape[0], 1), z_coord))).reshape(-1, 3)

# Find the perspective transformation matrix
transformation_matrix, _ = cv2.findHomography(pts1_3d[:, :2], pts2_3d[:, :2])

print("Transformation Matrix:")
print(transformation_matrix)
