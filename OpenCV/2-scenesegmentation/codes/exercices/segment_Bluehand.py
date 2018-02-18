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


imBGR = cv2.imread("../ressources/HandBlue.jpg")
# Convert to BGR to HSV
imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)

# Segment hand
# Select a sub part of the image:
y1 = 229
y2 = 401
x1 = 620
x2 = 704
patch_bricks = imHSV[y1:y2, x1:x2]



# Build a histogram:
hist_handh = cv2.calcHist([patch_bricks], channels = [0], mask=None, histSize=[180], ranges=[0, 179])
hist_hands = cv2.calcHist([patch_bricks], channels = [1], mask=None, histSize=[255], ranges=[0, 255])
hist_handv = cv2.calcHist([patch_bricks], channels = [2], mask=None, histSize=[255], ranges=[0, 255])

hist_handh /=hist_handh.max()
hist_hands /=hist_hands.max()
hist_handv /=hist_handv.max()
# Compute the histogram back projection:



# fun = np.zeros_like(lhMap_grass )
# gr = np.dstack((fun+0.1*255, lhMap_roof, lhMap_bricks, lhMap_grass, lhMap_path))
# gf = np.argmax(gr, 2)
# #
# plt.figure("Gr2")
# plt.imshow(gf)
# plt.show()

plt.figure("Input")
plt.imshow(imBGR[..., : : -1])
plt.figure("Canales")
plt.subplot(2,2,1)
plt.title("Canal H")
plt.plot(hist_handh)
plt.subplot(2,2,2)
plt.title("Canal S")
plt.plot(hist_hands)
plt.subplot(2,2,3)
plt.title("Canal V")
plt.plot(hist_handv)
plt.show()



#segLabels
