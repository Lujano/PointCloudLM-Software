import numpy as np
import cv2
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output3.avi',fourcc, 20.0, (640,480))
# cap1 = cv2.VideoCapture(1)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    out.write(frame)
    w, h = frame.shape[1], frame.shape[0]


    # ret, frame1 = cap1.read()

    # Display the resulting frame
    red = (0, 0, 255)
   # print(h)
   # print(w)
    cv2.line(frame, (w-140, 0), (w-140, h-1), red, 3)
    cv2.line(frame, (140, 0), (140, h - 1), red, 3)
    cv2.putText(frame, "camera0", (10, 10 ), cv2.LINE_AA, 1, 1)
    cv2.imshow('frame', frame)

    # cv2.imshow('frame2', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()