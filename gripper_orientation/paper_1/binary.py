import cv2

# Load the image
image = cv2.imread('images\\img1.png', cv2.IMREAD_GRAYSCALE)

# Convert the image to a binary image
_, binary_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

# Display the binary image
cv2.imshow('Binary Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2 
# import numpy as np

# # Load the background image and the image with objects
# background = cv2.imread('images\\bg.jpg')
# image_with_objects = cv2.imread('images\\object.jpg')

# # Convert the images to grayscale
# background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
# image_with_objects_gray = cv2.cvtColor(image_with_objects, cv2.COLOR_BGR2GRAY)

# # Calculate the absolute difference between the two images
# diff = cv2.absdiff(background_gray, image_with_objects_gray)

# # Apply a threshold to create a binary mask
# _, mask = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)

# # Invert the mask
# mask = cv2.bitwise_not(mask)

# # Apply the mask to the image with objects
# result = cv2.bitwise_and(image_with_objects, image_with_objects, mask=mask)

# # Display the result
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()