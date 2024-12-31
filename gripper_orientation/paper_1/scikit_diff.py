from skimage.metrics import structural_similarity
import cv2
import numpy as np

before = cv2.imread('images\\img0.png',cv2.COLOR_BGR2GRAY)
after = cv2.imread('images\\img1.png',cv2.COLOR_BGR2GRAY)


before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

(score, diff) = structural_similarity(before_gray, after_gray, full=True)
print("Image Similarity: {:.4f}%".format(score * 100))

diff = (diff * 255).astype("uint8")
diff_box = cv2.merge([diff, diff, diff])

thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        # x,y,w,h = cv2.boundingRect(c)
        # cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
        # cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
        # cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.drawContours(mask, [c], 0, (255,255,255), -1)
        # cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

# cv2.imshow('before', before)
# cv2.imshow('after', after)
# cv2.imshow('diff', diff)
# cv2.imshow('diff_box', diff_box)
cv2.imshow('mask', mask)
# cv2.imshow('filled after', filled_after)
# cv2.waitKey()

mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

binary_mask=mask
binary_image=mask
# _, binary_image = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
# ret, binary_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
# binary_image=binary_mask
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
        print(f"center of the object: {cx},{cy}")
        image_with_line = cv2.line(after.copy(), (cx, cy), (x2, y2), (255, 0, 0), 2)
        # image_with_line = cv2.line(image_with_line, (cx, cy), (x2_i, y2_i), (255, 0, 0), 2)
        cv2.imshow(f'Image with orientation line {label}', image_with_line)

cv2.waitKey(0)
cv2.destroyAllWindows()