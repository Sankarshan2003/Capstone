import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

def find_transformation(points1, points2):

    centroid1 = np.mean(points1, axis=0)
    centroid2 = np.mean(points2, axis=0)

    # Subtract the centroids from the point coordinates
    points1_centered = points1 - centroid1
    points2_centered = points2 - centroid2

    # Compute the SVD of the centered point coordinates
    H = np.matmul(points2_centered.T, points1_centered)
    U, S, VT = np.linalg.svd(H)

    # Compute the rotation matrix
    R = np.matmul(U, VT)

    # Handle the case where the determinant of R is -1
    if np.linalg.det(R) < 0:
        VT[-1,:] *= -1
        R = np.matmul(U, VT)

    # Compute the translation vector
    t = centroid2 - np.matmul(R, centroid1)

    return R, t

# camera_points=[[322.9195556640625, 188.25277709960938, 663.0], [-249.14190673828125, 197.48037719726562, 665.0], [-247.26866149902344, -196.13320922851562, 660.0], [319.8998718261719, -205.49032592773438, 659.0]]
camera_points=[[-100,50,-50],[-50,50,-50],[50,50,-50],[100,50,-50],[-100,-50,-50],[-50,-50,-50],[50,-50,-50],[100,-50,-50]]
object_points=[[-100,50,0],[-50,50,0],[50,50,0],[100,50,0],[-100,-50,0],[-50,-50,0],[50,-50,0],[100,-50,0]]
# camera_points=[[322.9195556640625, 188.25277709960938, 663.0], [-249.14190673828125, 197.48037719726562, 665.0], [-247.26866149902344, -196.13320922851562, 660.0], [319.8998718261719, -205.49032592773438, 659.0],[37.69513702392578, -6.774129390716553, 634.0]]
# object_points=[[-191, -278, 0], [-191, 278, 0], [191, 278, 0], [191, -278, 0],[0,0,0]]

points1 = np.array(camera_points)
points2 = np.array(object_points)

# rotation_matrix, translation_vector = find_transformation(points1, points2)
# R, t = find_transformation(points1, points2)

from scipy.spatial.transform import Rotation

# points1 and points2 are the corresponding sets of 3D points
centroid1 = np.mean(points1, axis=0)
centroid2 = np.mean(points2, axis=0)
points1_centered = points1 - centroid1
points2_centered = points2 - centroid2

R, _ = Rotation.align_vectors(points1_centered, points2_centered)
t = centroid2 - R.apply(centroid1)


R = R.as_matrix()

print("Rotation matrix:")
print(R)
print("Translation vector:")
print(t)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the original points (points1)
ax.scatter(points1[:, 0], points1[:, 1], points1[:, 2], color='r', label='Original Points')

# Apply the transformation to points1 and plot the transformed points
# points1.append([37.69513702392578, -6.774129390716553, 634.0])
# points1 = np.append(points1,[37.69513702392578, -6.774129390716553, 634.0])

# camera_points=[[322.9195556640625, 188.25277709960938, 663.0], [-249.14190673828125, 197.48037719726562, 665.0], [-247.26866149902344, -196.13320922851562, 660.0], [319.8998718261719, -205.49032592773438, 659.0],[37.69513702392578, -6.774129390716553, 634.0]]
# points1 = np.array(camera_points)
# print(points1)
points1_transformed = np.dot(R, points1.T).T + t
ax.scatter(points1_transformed[:, 0], points1_transformed[:, 1], points1_transformed[:, 2], color='g', label='Transformed Points')

# Plot the target points (points2) for reference
ax.scatter(points2[:, 0], points2[:, 1], points2[:, 2], color='b', label='Target Points')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Transformation Visualization')

# Add a legend
ax.legend()

# Adjust the view angle
ax.view_init(azim=-60, elev=30)

# # Show the plot
plt.show()

print("transformed:",points1_transformed)
print("original:",points2)
# test = np.array([37.69513702392578, -6.774129390716553, 634.0])
# test_transformed = np.dot(R, test.T).T + t
# print(test_transformed)
# #  [37.69513702392578, -6.774129390716553, 634.0]



