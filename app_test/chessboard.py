import cv2
import numpy as np

import cameraModules.realsense.camera_rs as cam
import cv2 as cv
import numpy as np

rs = cam.RSCamera([640,480],30)

# while True:
# cv.imshow("Depth Image", depth)
depth, img = rs.get_frames()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Define the chessboard dimensions
pattern_size = (11, 8)  # Number of corners (width, height)

# Find chessboard corners
ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

# If corners are found
if ret:
	# Refine the corner coordinates
	corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

	# Draw and display the corners
	img_corners = cv2.drawChessboardCorners(img.copy(), pattern_size, corners, ret)

	# Print the pixel coordinates of the corners
	print("Pixel coordinates of the corners:")
	for i,corner in enumerate(corners):
		if i <= 10:
			x, y = corner[0]
			# print(f"({int(x)}, {int(y)})")
	print(len(corners))

	# Display the image with corners
	# cv2.imshow('Chessboard Corners', img_corners)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

else:
	print("No chessboard pattern found.")
# cv.imshow("Color Image", color)
# cv.waitKey(1)
 
# cv.destroyAllWindows()


# x0, y0 = (333,150)
x0, y0 = (120,150)

corner_coords = []

for col in range(8):
	x = x0 + col * -30
	for row in range(11):
		y = y0 + row * -30
		corner_coords.append((x, y, 0))

coords = np.array(corner_coords)

print(coords)
# center_cam_coord = rs.deproject(337,264,depth)
# print("Asdasdasdasdasdasd",center_cam_coord)
corner_camera_points = []

for i in range(0,88):
    # print(i,corners[i][0])
    coord=corners[i][0]
    # print(coord[0])
    cv2.circle(img, (int(coord[0]),int(coord[1])), 5, (0, 255, 0), 2)
    # temp = rs.deproject(int(coord[0]),int(coord[1]),depth)[0:2]
    # temp.append(535)
    corner_camera_points.append(rs.deproject(int(coord[0]),int(coord[1]),depth))
    # corner_camera_points.append(temp)
    cv2.imshow("asdasd",img)
    cv2.waitKey(10)
print(corner_camera_points)

# corner_camera_points=[[-109.5826416015625, -117.35076141357422, 658.0], [-78.43852996826172, -118.24186706542969, 657.0], [-48.45527648925781, -118.0618896484375, 656.0], [-18.53473472595215, -118.7665023803711, 654.0], [12.263772010803223, -119.46460723876953, 652.0], [41.752532958984375, -118.91492462158203, 649.0], [71.40758514404297, -120.15619659423828, 650.0], [102.21211242675781, -121.4007339477539, 651.0], [133.51927185058594, -123.02473449707031, 654.0], [163.29208374023438, -124.08930206298828, 654.0], [194.42503356933594, -125.34522247314453, 655.0], [-108.677734375, -87.49357604980469, 659.0], [-77.37033081054688, -87.22804260253906, 657.0], [-47.388710021972656, -88.1630859375, 656.0], [-17.444705963134766, -87.75989532470703, 653.0], [13.262528419494629, -88.27873992919922, 649.0], [42.74176025390625, -89.197509765625, 648.0], [72.24142456054688, -89.197509765625, 648.0], [103.11192321777344, -90.5308609008789, 650.0], [133.11094665527344, -91.87071228027344, 652.0], [164.60670471191406, -93.35962677001953, 655.0], [195.19151306152344, -94.28164672851562, 654.0], [-107.60629272460938, -56.38534164428711, 659.0], [-77.6058578491211, -56.38534164428711, 659.0], [-46.3221435546875, -57.19647216796875, 656.0], [-16.433195114135742, -58.17546844482422, 655.0], [14.31771469116211, -58.69898223876953, 649.0], [43.79532241821289, -58.60853576660156, 648.0], [73.40809631347656, -59.755401611328125, 649.0], [103.27055358886719, -59.93954849243164, 651.0], [134.7883758544922, -61.374027252197266, 655.0], [164.60670471191406, -62.44021224975586, 655.0], [197.15509033203125, -63.700313568115234, 657.0], [-106.69650268554688, -25.315465927124023, 660.0], [-76.41827392578125, -26.30982208251953, 658.0], [-46.392757415771484, -27.339279174804688, 657.0], [-16.357927322387695, -27.13121795654297, 652.0], [14.31771469116211, -28.062801361083984, 649.0], [43.79532241821289, -29.074352264404297, 648.0], [73.18187713623047, -30.08264923095703, 647.0], [104.00847625732422, -30.175640106201172, 649.0], [134.7883758544922, -31.520801544189453, 655.0], [165.67164611816406, -31.520801544189453, 655.0], [197.15509033203125, -32.68648910522461, 657.0], [-106.69650268554688, 4.765646934509277, 660.0], [-75.34846496582031, 3.680135726928711, 658.0], [-45.32456588745117, 3.6745429039001465, 657.0], [-15.321329116821289, 2.589240312576294, 653.0], [15.372899055480957, 1.516959547996521, 649.0], [44.848876953125, 1.5146220922470093, 648.0], [74.4632797241211, 0.4605395495891571, 649.0], [105.54931640625, -0.5986348986625671, 652.0], [135.85330200195312, -0.6013893485069275, 655.0], [167.24569702148438, -1.6726677417755127, 657.0], [198.52499389648438, -2.746283769607544, 658.0], [-105.46340942382812, 34.79396057128906, 659.0], [-74.27864074707031, 34.74116134643555, 658.0], [-44.18901062011719, 33.567752838134766, 656.0], [-14.303314208984375, 32.45039367675781, 655.0], [16.453397750854492, 32.20268249511719, 650.0], [45.97327423095703, 31.09671974182129, 649.0], [75.63482666015625, 30.086585998535156, 650.0], [105.3874282836914, 30.13287353515625, 651.0], [137.1272735595703, 29.29649543762207, 656.0], [167.24569702148438, 28.271711349487305, 657.0], [198.52499389648438, 28.314743041992188, 658.0], [-104.23355102539062, 65.80219268798828, 658.0], [-74.16575622558594, 64.63274383544922, 657.0], [-43.05671310424805, 63.36980438232422, 655.0], [-13.238373756408691, 63.36980438232422, 655.0], [16.453397750854492, 61.82801818847656, 650.0], [46.88353729248047, 61.542659759521484, 647.0], [76.69163513183594, 60.76996994018555, 650.0], [106.93639373779297, 60.07938003540039, 654.0], [137.98318481445312, 60.17124557495117, 655.0], [168.05770874023438, 59.19529724121094, 656.0], [199.5948028564453, 58.3046989440918, 658.0], [-104.39196014404297, 95.93772888183594, 659.0], [-72.9863052368164, 95.50098419189453, 656.0], [-43.18818283081055, 94.5771255493164, 657.0], [-13.238373756408691, 93.22303009033203, 655.0], [17.537147521972656, 92.65373229980469, 651.0], [47.10092544555664, 91.45336151123047, 650.0], [77.98767852783203, 90.67344665527344, 652.0], [107.99971008300781, 90.95159149169922, 654.0], [138.19384765625, 90.16191864013672, 656.0], [169.38209533691406, 90.29936218261719, 657.0], [200.3596649169922, 89.22991180419922, 657.0]]


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

points1 = np.array(corner_camera_points)
points2 = np.array(coords)

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


ax.scatter(points1[:, 0], points1[:, 1], points1[:, 2], color='r', label='Original Points')

# points1_transformed = np.dot(R, points1.T).T + t
# ax.scatter(points1_transformed[:, 0], points1_transformed[:, 1], points1_transformed[:, 2], color='g', label='Transformed Points')

# Plot the target points (points2) for reference
# ax.scatter(points2[:, 0], points2[:, 1], points2[:, 2], color='b', label='Target Points')

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



#  [37.69513702392578, -6.774129390716553, 634.0]

element = np.array([243,0,-155])
index = np.where((coords == element).all(axis=1))[0]
print(index)
center = corners[index[0]][0]
print("center", center)
x = int(center[0])
y = int(center[1])
cv2.circle(img, (x,y), 5, (0, 0, 255), 2)
center_cam_coord = rs.deproject(x,y,depth)

# test = np.array([32.35,13.18,651])
print("center_cam_coord",center_cam_coord)
test = np.array(center_cam_coord)
test_transformed = np.dot(R, test.T).T + t
print(test_transformed)


cv2.imshow("center", img)
cv2.waitKey(0)




