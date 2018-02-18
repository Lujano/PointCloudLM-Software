""""
///////////////////////////////////////////////////////////////////////
//                                                                   //
//                       Segment House v1                            //
//                        Luis  Lujano, 13-10775                     //
//                       Jaime Villegas, 13-11493                    //
///////////////////////////////////////////////////////////////////////
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt


imBGR = cv2.imread("../ressources/house.jpg")
# Convert to BGR to HSV
imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)

# Segment brick
# Select a sub part of the image:
y1 = 309
y2 = 330
x1 = 300
x2 = 320
patch_bricks = imHSV[y1:y2, x1:x2]

# Grass
# Select a sub part of the image:
y1 = 900
y2 = 930
x1 = 400
x2 = 450
patch_grass = imHSV[y1:y2, x1:x2]

# Path
# Select a sub part of the image:
y1 = 828
y2 = 850
x1 = 500
x2 = 520
patch_path = imHSV[y1:y2, x1:x2]

#Roof
# Select a sub part of the image:
y1 = 164
y2 = 200
x1 = 856
x2 = 900
patch_roof = imHSV[y1:y2, x1:x2]

# Build a histogram:
hist_bricks = cv2.calcHist([patch_bricks], channels = [0, 1], mask=None, histSize=[180, 256], ranges=[0, 179, 0, 255])

hist_bricks /=hist_bricks.max()
# Compute the histogram back projection:
lhMap_bricks = cv2.calcBackProject([imHSV], channels=[0, 1], hist=hist_bricks, ranges = [0, 179, 0, 255], scale=255)


hist_grass = cv2.calcHist([patch_grass], channels = [0, 1], mask =None, histSize=[180, 256], ranges = [0, 179, 0, 255])
hist_grass /=hist_grass.max()

# Compute the histogram back projection:
lhMap_grass = cv2.calcBackProject([imHSV], channels=[0, 1], hist=hist_grass, ranges = [0, 179, 0, 255], scale=255)

hist_path = cv2.calcHist([patch_path], channels = [0, 1], mask =None, histSize=[180, 256], ranges = [0, 179, 0, 255])
hist_path /=hist_path.max()
# Compute the histogram back projection:
lhMap_path = cv2.calcBackProject([imHSV], channels=[0, 1], hist=hist_path, ranges = [0, 179, 0, 255], scale=255)

hist_roof = cv2.calcHist([patch_roof], channels = [0, 1], mask =None, histSize=[180, 256], ranges = [0, 179, 0, 255])
hist_roof /=hist_roof.max()


# Compute the histogram back projection:
lhMap_roof = cv2.calcBackProject([imHSV], channels=[0, 1], hist=hist_roof, ranges = [0, 179, 0, 255], scale=255)

fun = np.zeros_like(lhMap_grass )
gr = np.dstack((fun+0.1*255, lhMap_roof, lhMap_bricks, lhMap_grass, lhMap_path))
gf = np.argmax(gr, 2)

plt.figure("Gr2")
plt.imshow(gf)
plt.show()

""""
# Don't forget to plot a BGR image

plt.figure("Grass")
plt.imshow(lhMap_grass[..., : : -1])
plt.figure("Path")
plt.imshow(lhMap_path[..., : : -1])

plt.figure("Bricks")
plt.imshow(lhMap_bricks[..., : : -1])
plt.figure("Roof")
plt.imshow(lhMap_roof[..., : : -1])

plt.figure("Original")
plt.imshow(imBGR[..., : : -1])
plt.show()

"""

#segLabels
