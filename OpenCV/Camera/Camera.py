import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# cap1 = cv2.VideoCapture(1)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # ret, frame1 = cap1.read()


    # Display the resulting frame
    cv2.imshow('frame', frame)
    # cv2.imshow('frame2', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()