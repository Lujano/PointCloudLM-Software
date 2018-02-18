import cv2
import numpy as np  # importing libraries

cap = cv2.VideoCapture(0)  # creating camera object
while (cap.isOpened()):
    ret, img = cap.read()  # reading the frames
    cv2.imshow('input', img)  # displaying the frames
    k = cv2.waitKey(10)
    if k == 27:
        break