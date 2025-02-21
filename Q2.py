import numpy as np
import cv2
import imutils
import os
import matplotlib.pyplot as plt

path = "Question2Images"
files = sorted([f for f in os.listdir(path) if f.endswith(('.png', '.jpg', '.jpeg'))])
images = []
for file in files:
    pathToImage = os.path.join(path, file)
    img = cv2.imread(pathToImage)
    images.append(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.title(f"Image: {file}")
    plt.axis("off") 
    plt.show()
 
orb = cv2.ORB_create()

for i, img in enumerate(images):
    keypoints = orb.detect(img, None)
    keypointsImage = cv2.drawKeypoints(img, keypoints, None, color=(0, 0, 255))

    img_rgb = cv2.cvtColor(keypointsImage, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.title(f"Keypoints in Image {i+1}")
    plt.axis("off")
    plt.show()


imageStitcher = cv2.Stitcher_create()
error, stitchedImage = imageStitcher.stitch(images)
if not error:
    stitchedResized = cv2.resize(stitchedImage, (800, 600))
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(stitchedResized, cv2.COLOR_BGR2RGB))
    plt.title("Stitched Resized Image")
    plt.axis("off")
    plt.show()


    stitchedImage = cv2.copyMakeBorder(stitchedImage, 5, 5, 5, 5, cv2.BORDER_CONSTANT, (0, 0, 0))

    gray = cv2.cvtColor(stitchedImage, cv2.COLOR_BGR2GRAY)
    threshImage = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    threshCopy = threshImage.copy()
  

    contours = cv2.findContours(threshCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv2.contourArea)

    mask = np.zeros(threshImage.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(areaOI)
    cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    minRectangle = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, threshImage)


    contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv2.contourArea)

    # cv2.imshow("minRectangle Image", cv2.resize(minRectangle, (800, 600)))
    # cv2.waitKey(0)

    x, y, w, h = cv2.boundingRect(areaOI)

    stitchedImage = stitchedImage[y:y + h, x:x + w]

    cv2.imwrite("stitchedOutputProcessed.png", stitchedImage)
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(stitchedImage, cv2.COLOR_BGR2RGB))
    plt.title("Final Stitched Image")
    plt.axis("off")
    plt.show()
    cv2.waitKey(0)
