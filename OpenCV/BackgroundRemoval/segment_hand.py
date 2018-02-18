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


cap = cv2.VideoCapture(0)
imBGR = cv2.imread("hand1.jpg")
# Convert to BGR to HSV
imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)
while(1):
    ret, frame = cap.read()
    # Convert to BGR to HSV
    imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Segment hand
    # Select a sub part of the image:
    y1 = 202
    y2 = 259
    x1 = 580
    x2 = 647
    patch_bricks = imHSV[y1:y2, x1:x2]



    # Build a histogram:
    hist_bricks = cv2.calcHist([patch_bricks], channels = [0, 1], mask=None, histSize=[180, 256], ranges=[0, 179, 0, 255])

    hist_bricks /=hist_bricks.max()
    # Compute the histogram back projection:
    lhMap_bricks = cv2.calcBackProject([frameHSV], channels=[0, 1], hist=hist_bricks, ranges = [0, 179, 0, 255], scale=255)



    # fun = np.zeros_like(lhMap_grass )
    # gr = np.dstack((fun+0.1*255, lhMap_roof, lhMap_bricks, lhMap_grass, lhMap_path))
    # gf = np.argmax(gr, 2)
    # #
    # plt.figure("Gr2")
    # plt.imshow(gf)
    # plt.show()


    # # Don't forget to plot a BGR image
    # #
    # plt.figure("Grass")
    # plt.imshow(lhMap_grass[..., : : -1])
    # plt.figure("Path")
    # plt.imshow(lhMap_path[..., : : -1])
    #
    cv2.imshow("hand", lhMap_bricks)
    # plt.figure("Roof")
    # plt.imshow(lhMap_roof[..., : : -1])


    cv2.imshow("input", frame)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

    #segLabels
