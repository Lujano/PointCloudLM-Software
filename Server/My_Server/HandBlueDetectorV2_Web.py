# -*- encoding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2
import time
import requests
ip_server = "192.168.1.125"
#ip_server = "127.1.1.1"
port_server = "8000"


def ESP8266_send(ip, step1, step2): # el servo que controla phi (plano xy)
    url_FREERUN = "http://"+ ip +":"+ port_server+ "/HandTracking" + '?step1=' + str(step1) \
                  + '&step2=' + str(step2)

    try:
        T_Inicio = time.time()

        req = requests.get(url_FREERUN)
        response = req.content
        T_Final = time.time()
        Dif = T_Final - T_Inicio
        print(Dif)
        if response != "OK":
            print("Bad response ")
    except:
        print("Error Sending Data")

def adjust_coord(handx, handy, w1, h1, n_pasos):


    # Chequeo de fronteras de control
    if handx<0:
        handx = 0
    if handy<0:
        handy = 0
    if handx > 2*w1:
        handx = 2*w1
    if handy > 2*h1:
        handy = 2*h1
    # Conversion a pasos del motor

    paso_theta = int(handy/(n_pasos*2))*n_pasos # pasos por pixeles
    paso_phi = int(handx/(n_pasos*2))*n_pasos

    return paso_theta, paso_phi

# def draw_last_position (last_paso_theta, last_paso_phi, ref_x1, ref_y2, n_pasos):
#     pixel_theta = int(last_paso_theta/n_pasos)*n_pasos*2
#     pixel_phi =  int(last_paso_theta/n_pasos)*n_pasos*2
#     pixel_phi = last_paso_phi
#     center_cx = ref_x1-pixel_phi
#     center_cy = ref_y1+pixel_theta
#     center_last_position = (center_cx, center_cy)
#     cv2.circle(img, center_last_position, 5, [0, 255, 0], 2)


# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([95, 50, 50], dtype = "uint8")
upper = np.array([130, 255, 255], dtype = "uint8")



call = 0


# Datos de motores calibrados
phi_0 = 228
phi_180 = 36
phi_resol = (phi_0-phi_180+1)/180.0

theta_0 = 245
theta_90 = 131
theta_max = 100  # minimo angulo sin que el motor choque con la base
theta_resol = (theta_0-theta_90 +1)/90.0 # pasos por angulo

step1 = phi_0-97 # 45 grados
step2 = theta_90 +57 #

cap = cv2.VideoCapture(0)
ESP8266_send(ip_server, step1, step2)

last_paso_theta, last_paso_phi = 57,  97
cx, cy = 97*2, 57*2
last_cx, last_cy = 0, 0

while True:



    grabbed, frame = cap.read()
    frame = cv2.flip(frame, 1)
    w , h = frame.shape[1], frame.shape[0]
    centerx = int(round(w/2))
    centery = int(round(h/2))

    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)


    kernel = np.ones((5,5), np.uint8)
    skinMask= cv2.medianBlur(skinMask, 9)
    img = frame
    thresh1 = skinMask
    im3, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape, np.uint8)
    max_area = 0
    ci = 0

    if len(contours)>0:
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if (area > max_area):
                max_area = area
                ci = i
        cnt = contours[ci]
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
            cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00

        centr = (cx, cy)

        cv2.circle(img, centr, 5, [0, 0, 255], 2)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)

        cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        hull = cv2.convexHull(cnt, returnPoints=False)

        if (1):
            defects = cv2.convexityDefects(cnt, hull)
            mind = 0
            maxd = 0
            if type(defects)!= type(None):
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt, centr, True)
                    cv2.line(img, start, end, [0, 255, 0], 2)

                    cv2.circle(img, far, 5, [0, 0, 255], -1)
            #print(i)
            i = 0
        w1, h1 = 192, 145, #int(round(7/20*w)), int(round(7/20*h))
        cv2.rectangle(img, (centerx-w1, centery-h1), (centerx+w1, centery+h1), (255,0, 0), 3)
        handx = centerx+w1-cx
        handy = cy-(centery-h1)
        paso_theta, paso_phi = adjust_coord(handx, handy,w1, h1, 4)
        # No quemar los motores: permitir solo pasos pequeños en caso de fallo en deteccion de mano
        if call == 0:
            call = 1
            last_paso_theta, last_paso_phi = 73,  97
            last_cx, last_cy = centerx, centery
            cv2.circle(img, (last_cx, last_cy), 5, [0, 255, 0], 2)

        if np.abs(paso_theta-last_paso_theta)>4:
            paso_theta = last_paso_theta
            cv2.circle(img, (last_cx, last_cy), 5, [0, 255, 0], 2)

        else:
            step2 =  theta_0 - paso_theta
            last_cy =  cy
            ESP8266_send(ip_server, step1, step2)
            cv2.circle(img, (last_cx, cy), 5, [0, 255, 0], 2)
            print("theta {0:0.2f}, phi {1:0.2f}".format(paso_theta/theta_resol, paso_phi/phi_resol))

        if np.abs(paso_phi-last_paso_phi)>4:
            paso_phi = last_paso_phi
            cv2.circle(img, (last_cx, last_cy), 5, [0, 255, 0], 2)
        else:
            last_cx = cx
            step1 = phi_0-paso_phi
            ESP8266_send(ip_server, step1, step2)
            cv2.circle(img, (cx, last_cy), 5, [0, 255, 0], 2)
            print("theta {0:0.2f}, phi {1:0.2f}".format(paso_theta/theta_resol, paso_phi/phi_resol))

        last_paso_theta, last_paso_phi= paso_theta, paso_phi



    # show the skin in the image along with the mask0
    #cv2.imshow("Draw", drawing)
    cv2.imshow("Image", frame)
    #cv2.imshow("MOG2", skinMask)
    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
