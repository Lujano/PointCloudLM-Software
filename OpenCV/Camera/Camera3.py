import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)


T_Inicio = time.time()
T_Final = time.time()
Dif = T_Final - T_Inicio
i = 0
while (Dif<10):
    # Capture frame-by-frame
    ret, frame = cap.read()
    w, h = frame.shape[1], frame.shape[0]

    # ret, frame1 = cap1.read()

    # Display the resulting frame
    red = (0, 0, 255)
   # print(h)
   # print(w)
    cv2.line(frame, (w-140, 0), (w-140, h-1), red, 3)
    cv2.line(frame, (140, 0), (140, h - 1), red, 3)
    cv2.imshow('frame', frame)

    # cv2.imshow('frame2', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imwrite("Data/Image_" + str(i)+".jpg", frame)
    i += 1
    T1 = time.time()
    T2= time.time()
    Dif2 = T2-T1
    while (Dif2 < 0.25):
        T2 = time.time()
        Dif2 = T2 - T1


    T_Final = time.time()
    Dif = T_Final - T_Inicio

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()