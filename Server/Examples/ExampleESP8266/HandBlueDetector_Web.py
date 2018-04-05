# -*- encoding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2
import urllib2
import urllib
import time
ip_server = "192.168.1.101"
#ip_server = "127.1.1.1"
port_server = "8000"



def delay_s(tiempo):
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final - T_Inicio
    while(Dif < tiempo ):
        T_Final = time.time()
        Dif = T_Final - T_Inicio
    return

def open_port():
    url_request = "http://"+ip_server+":"+port_server+"/HandTracking?param1=WHERE_IS_ESP8266"
    response =  "Negative"
    ip_ESP8266 = "0.0.0.0"

    while response == "Negative" or response == "ESP8266_Is_No_Connected" :
        try :
            print("Connecting to Server")
            req = urllib2.Request(url_request)
            res= urllib2.urlopen(req)
            response = res.read()
            res.close()
            if response == "ESP8266_Is_No_Connected" or response == "Negative" :
                print(response)
                delay_s(10.0)
                print("Retrying")
            else:
                ip_ESP8266 = response
                print("HandTracking Started")
        except:
            print("Error connecting to Server")
            delay_s(5.0)
            print("Retrying")

    return ip_ESP8266


def close_port():
    url_request = "http://"+ ip_server + ":" + port_server + "/HandTracking?param1=PROCESS_END"
    response = "Negative"

    while response == "Negative":
        try:
            print("Finishing the connection")
            req = urllib2.Request(url_request)
            res = urllib2.urlopen(req)
            response = res.read()
            res.close()
            if response == "Negative":
                print(response)
                delay_s(10.0)
                print("Retrying")
            else:
                print("Connection Has Finished")
        except:
            print("Error Finishing the connection")
            delay_s(5.0)
            print("Retrying")


    return

def ESP8266_send(ip, step1, step2): # el servo que controla phi (plano xy)
    url_FREERUN = "http://"+ip+"/Server" + '?step1=' + str(step1) \
                  + '&step2=' + str(step2) + '&commad=OK'

    try:
        req = urllib2.Request(url_FREERUN)
        res = urllib2.urlopen(req)
        response = res.read()
        res.close()
        if response != "OK":
            print("Bad response ")
    except:
        print("Error Sending Data")

def adjust_coord(handx, handy, w1, y1, n_pasos):


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

    paso_theta = int(handy/(n_pasos*2))*n_pasos
    paso_phi = int(handx/(n_pasos*2))*n_pasos

    return paso_theta, paso_phi


# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([100, 50, 50], dtype = "uint8")
upper = np.array([120, 255, 255], dtype = "uint8")


bgSubThreshold = 50
bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
last_paso_theta , last_paso_phi = 145, 192 #centro
call = 0




# Datos de motores calibrados
phi_0 =228
phi_180 = 36
phi_resol = (-phi_180+phi_0+1)/180.0

theta_0 = 245
theta_90 = 131
theta_max = 100  # minimo angulo sin que el motor choque con la base
theta_resol = (-theta_90+theta_0 +1)/90.0

ip_ESP8266 = open_port()
step1 = phi_180
step2 = theta_90
ESP8266_send(ip_ESP8266, step1, step2)

cap = cv2.VideoCapture(1)
while True:



    grabbed, frame = cap.read()
    frame = cv2.flip(frame, 1)
    w , h = frame.shape[1], frame.shape[0]
    centerx = int(round(w/2))
    centery = int(round(h/2))

    #print("W= {}, H={}".format(w, h))


    # if we are viewing a video and we did not grab a
    # frame, then we have reached the end of the video

    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    #frame = imutils.resize(frame, width = 400)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    # skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    # skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    kernel = np.ones((5,5), np.uint8)

    # skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_OPEN, kernel)
    #skinMask = cv2.erode(skinMask, kernel, iterations=1)
    # blur the mask to help remove noise, then apply the
    # mask to the frame
    #skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
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
            last_paso_theta, last_paso_phi = paso_theta, last_paso_phi

        if np.abs(paso_theta-last_paso_theta)>4:
            paso_theta = last_paso_theta
        else:
            step2 =  -paso_theta+theta_0
            ESP8266_send(ip_ESP8266, step1, step2)
            print("theta {0:0.2f}, phi {0:0.2f}".format(paso_theta/theta_resol, paso_phi/phi_resol))

        if np.abs(paso_phi-last_paso_phi)>4:
            paso_phi = last_paso_phi
        else:

            step1 = -paso_phi+phi_0
            ESP8266_send(ip_ESP8266, step1, step2)
            print("theta {0:0.2f}, phi {0:0.2f}".format(paso_theta/theta_resol, paso_phi/phi_resol))

        last_paso_theta, last_paso_phi = paso_theta, paso_phi



    # show the skin in the image along with the mask0
    #cv2.imshow("Draw", drawing)
    cv2.imshow("Image", frame)
    #cv2.imshow("MOG2", skinMask)
    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        close_port()
        break
