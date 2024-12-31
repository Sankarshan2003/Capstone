import cv2
import numpy as np

# Load your image
image = cv2.imread('images\\objects.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to get a binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over all contours
for contour in contours:
    # Calculate the moments of the contour
    M = cv2.moments(contour)
    # Calculate the centroid coordinates
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # Draw a circle at the centroid
    cv2.circle(image, (cX, cY), 5, (255, 0, 0), -1)

# Display the image with the centroid marked
cv2.imshow('Image with Centroid', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
