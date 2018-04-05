# -*- encoding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while True:



    grabbed, frame = cap.read()
    frame = cv2.flip(frame, 1)
    w , h = frame.shape[1], frame.shape[0]
    centerx = int(round(w/2))
    centery = int(round(h/2))
    img = frame
    canvas = np.zeros((h, w, 3), dtype = 'uint8')
    w1, h1 = 192, 145, #int(round(7/20*w)), int(round(7/20*h))
    cv2.rectangle(canvas, (centerx-w1, centery-h1), (centerx+w1, centery+h1), (255,255, 255), -1)
    #cv2.rectangle(img, (centerx-w1, centery-h1), (centerx+w1, centery+h1), (255,255, 255), -1)
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)  # Cambiar a escala de grises la mascara de puntos
    img2 = cv2.bitwise_and(img, img, mask= gray_canvas)
    mean_color = cv2.mean(img2, mask = gray_canvas)
    print(mean_color)




    # show the skin in the image along with the mask0
    cv2.imshow("Draw", img)
    cv2.imshow("Draw2", img2)
    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        close_port(port)
        break
