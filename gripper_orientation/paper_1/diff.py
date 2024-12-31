import cv2
import numpy as np


# bg_image = cv2.imread('images\\bg.png')
bg_image = cv2.imread('images\\bg.jpg')
new_image = cv2.imread('images\\object.jpg')
# new_image = cv2.imread('images\\objects.png')

bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

# diff = cv2.absdiff(bg_gray, new_gray)
_, binary_image = cv2.threshold(new_image, 155, 255, cv2.THRESH_BINARY)

cv2.imshow('Difference Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

ret, binary_mask = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)


# num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

# isolated_objects = []


# for label in range(1, num_labels):
#     mask = np.uint8(labels == label) * 255
    
#     isolated_object = cv2.bitwise_and(binary_image, binary_image, mask=mask)
    
#     isolated_objects.append(isolated_object)

# for i, isolated_object in enumerate(isolated_objects):
#     cv2.imshow(f'Isolated Object {i}', isolated_object)
#     # cv2.imwrite(f'Isolated Object {i}.png', isolated_object)
    
#     contours, _ = cv2.findContours(isolated_object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     image_with_contours = np.copy(bg_gray)
#     image_with_contours = cv2.cvtColor(image_with_contours, cv2.COLOR_GRAY2BGR)

#     cv2.drawContours(image_with_contours, contours, -1, (0, 0, 0), 1)
#     # print(contours[0])
#     # for line in contours[0]:
#         # with open("contours.txt","ab") as f:
#             # np.savetxt(f, line,fmt='%4.6f',delimiter=' ')
#     M = cv2.moments(contours[0],True)

#     if M["m00"] != 0:
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#     else:
#         cX, cY = 0, 0

#     cv2.circle(image_with_contours, (cX, cY), 5, (255, 0, 0), -1)

#     cv2.imshow(f'Object {i} Center', image_with_contours)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()

#     # image = cv2.imread('binary_image.png', cv2.IMREAD_GRAYSCALE)

#     # Find contours of the object
#     contours, _ = cv2.findContours(isolated_object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Get the largest contour (assuming it's the object of interest)
#     if len(contours) > 0:
#         largest_contour = max(contours, key=cv2.contourArea)

#         contour_points = largest_contour.reshape(-1, 2).astype(np.float32)
#         mean, eigenvectors = cv2.PCACompute(contour_points, mean=None)

#         # The eigenvector with the largest eigenvalue corresponds to the principal axis
#         principal_axis = eigenvectors[0]

#         # Calculate the orientation angle from the principal axis
#         orientation = np.arctan2(principal_axis[1], principal_axis[0])
        
#         # Convert orientation to degrees
#         angle_degrees = np.degrees(orientation)
#         print("Object orientation:", angle_degrees)
        
#         # Get centroid of the object
#         M = cv2.moments(largest_contour)
#         cx = int(M['m10'] / M['m00'])
#         cy = int(M['m01'] / M['m00'])
        
#         # Calculate endpoint of the line
#         line_length = 50
#         x2 = int(cx + line_length * np.cos(orientation))
#         y2 = int(cy + line_length * np.sin(orientation))
        
#         # Draw line on the image
#         image_with_line = cv2.line(new_image.copy(), (cx, cy), (x2, y2), (255, 0, 0), 2)
        
#         # Display the image
#         cv2.imshow(f'Image with orientation line {i}', image_with_line)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#     else:
#         print("No object found in the image.")

cv2.waitKey(0)
cv2.destroyAllWindows()
