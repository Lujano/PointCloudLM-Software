import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
time_ini = time.time()
time_fini = time.time()
delta = time_fini-time_ini
while(delta < 4.0):

ret, frame1 = cap.read()
mask1 = fgbg.apply(frame)
while(1):
    ret, frame = cap.read()
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()