import cv2
import numpy as np
from math import sqrt

# Load image and get dimensions
image = cv2.imread("test.jpg")
height, width = image.shape[:2]

# Calculate half dimensions
half_width = width // 2
half_height = height // 2

# Find white pixels
white_pixels = []
for x in range(height):
    for y in range(width):
        b, g, r = image[x, y]
        if b > 200 and g > 200 and r > 200:
            white_pixels.append((x, y))

# Create a blank image and mark white pixels
binary_img = np.zeros((height, width), np.uint8)
for x, y in white_pixels:
    binary_img[x, y] = 255

# Define kernel and apply morphological operations
kernel = np.ones((5, 5), np.uint8)
binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

# Split image into left and right halves
right_half = binary_img[half_height:, half_width:]
left_half = binary_img[half_height:, :half_width]

# Threshold for minimum width of bounding boxes
min_width_threshold = width * 0.04

# Find contours in the right half
contours, _ = cv2.findContours(right_half, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
possible_right_lines = []
shortest_distance = None
lane_lines_right = None

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > min_width_threshold:
        possible_right_lines.append((x, y, w, h))
        distance = sqrt((x - 0) ** 2 + (y - right_half.shape[0]) ** 2)
        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
            lane_lines_right = (x, y, w, h)

# Calculate the scaling factor for the right side
if lane_lines_right:
    x1, y1, w1, h1 = lane_lines_right
    right_slope = h1 / w1
    right_intercept = right_half.shape[0] - y1
    right_weight = right_intercept / right_slope

# Find contours in the left half
contours, _ = cv2.findContours(left_half, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
possible_left_lines = []
shortest_distance = None
lane_lines_left = None

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > min_width_threshold:
        possible_left_lines.append((x, y, w, h))
        distance = sqrt((left_half.shape[1] - x) ** 2 + (left_half.shape[0] - y) ** 2)
        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
            lane_lines_left = (x, y, w, h)

# Calculate the scaling factor for the left side
if lane_lines_left:
    x2, y2, w2, h2 = lane_lines_left
    left_slope = h2 / w2
    left_intercept = left_half.shape[0] - y2
    left_weight = left_intercept / left_slope

    # Draw the lanes on the original image
    points = np.array([
        [x2 - int(left_weight), half_height + left_half.shape[0]],
        [x2, half_height + y2],
        [half_width + x1, half_height + y1],
        [half_width + int(right_weight) + x1, half_height + right_half.shape[0]]
    ], np.int32)

    points = points.reshape((-1, 1, 2))
    cv2.polylines(image, [points], True, (140, 130, 17), thickness=3)

# Display the result
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
