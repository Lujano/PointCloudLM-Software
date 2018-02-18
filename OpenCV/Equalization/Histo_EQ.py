import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
while(1):
    ret, frame = cap.read()
    clahe = cv2.createCLAHE(clipLimit= 2.0, tileGridSize = (8,8))
    frame= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cl1 = clahe.apply(frame)
    cv2.imshow('frame',cl1)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()