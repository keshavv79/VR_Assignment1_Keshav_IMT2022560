import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('Question1Images/img5.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (15, 15), 7)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.show()

_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

# Edge detection
edges = cv2.Canny(binary, 120, 250)
plt.imshow(edges, cmap='gray')
plt.title("Edge detection of coins")
plt.show()
cv2.imwrite("Question1Outputs/EdgeImg5.jpg", edges) 
cv2.waitKey(0)
cv2.destroyAllWindows()

# Segmentation
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
segmented = np.zeros_like(gray)
cv2.drawContours(segmented, contours, -1, 255, thickness=cv2.FILLED)

plt.imshow(segmented, cmap='gray')
plt.title("Segmentation of coins")
plt.show()
cv2.imwrite("Question1Outputs/segmentationOutputImg5.jpg", segmented) 
cv2.waitKey(0)
cv2.destroyAllWindows()

# Counting the coins
count, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contourAreaMin = 475  
filteredCount = [c for c in count if cv2.contourArea(c) > contourAreaMin]
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, filteredCount, -1, (0, 255, 0), thickness=2) 

plt.imshow(rgb)
plt.show()
cv2.imwrite("Question1Outputs/coinCountOutputImg5.jpg", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))  
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Number of coins in the image:", len(filteredCount))
