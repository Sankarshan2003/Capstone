import cv2
import numpy as np

bg_image = cv2.imread('images\\bg.png')
new_image = cv2.imread('images\\objects.png')

bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

diff = cv2.absdiff(bg_gray, new_gray)
_, binary_image = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

ret, binary_mask = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

for label in range(1, num_labels):
    mask = np.uint8(labels == label) * 255
    isolated_object = cv2.bitwise_and(binary_image, binary_image, mask=mask)

    contours, _ = cv2.findContours(isolated_object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if circularity > 0.8:
            orientation = 0
        else:
            contour_points = largest_contour.reshape(-1, 2).astype(np.float32)
            mean, eigenvectors = cv2.PCACompute(contour_points, mean=None)
            principal_axis = eigenvectors[0]
            orientation = np.arctan2(principal_axis[1], principal_axis[0])
            orientation = orientation + np.pi / 2
            
        angle_degrees = np.degrees(orientation)
        print(f"Object {label} orientation: {angle_degrees:.2f} degrees")

        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        line_length = 30
        x2 = int(cx + line_length * np.cos(orientation))
        x2_i = int(cx - line_length * np.cos(orientation))
        y2 = int(cy + line_length * np.sin(orientation))
        y2_i = int(cy - line_length * np.sin(orientation))

        image_with_line = cv2.line(new_image.copy(), (cx, cy), (x2, y2), (255, 0, 0), 2)
        # image_with_line = cv2.line(image_with_line, (cx, cy), (x2_i, y2_i), (255, 0, 0), 2)
        cv2.imshow(f'Image with orientation line {label}', image_with_line)

cv2.waitKey(0)
cv2.destroyAllWindows()