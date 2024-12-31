import cv2
import numpy as np
import matplotlib.pyplot as plt
# Load the background image and the new image
bg_image = cv2.imread('images\\img0.png')
new_image = cv2.imread('images\\img1.png')


fgbg1 = cv2.createBackgroundSubtractorMOG2();  

bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)



diff = cv2.absdiff(bg_gray, new_gray)
_, binary_image = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

fgmask1 = fgbg1.apply(new_image);
erosion_size = 1
erosion_shape = 0

element = cv2.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
 (erosion_size, erosion_size))
 
erosion_dst = cv2.erode(binary_image, element)


cv2.imshow('Difference Image', erosion_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


# contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# image_with_contours = np.copy(binary_image)
# image_with_contours = cv2.cvtColor(image_with_contours, cv2.COLOR_GRAY2BGR)

# cv2.drawContours(bg_image, contours, -1, (0, 0, 0), 1)
# # print(contours)
# for contour in contours:
#     print(len(contour))
#     for points in contour:
#         plt.scatter(points[0][0], points[0][1])
#         # print((points[0]))

# plt.show()
# cv2.imshow('Contours', bg_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
