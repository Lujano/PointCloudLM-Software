# -*- encoding: utf-8 -*-
# USAGE

# python skindetector.py
# python skindetector.py --video video/skin_example.mov

# import the necessary packages
import numpy as np
import cv2

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([100, 50, 50], dtype = "uint8")
upper = np.array([120, 255, 255], dtype = "uint8")

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)
bgSubThreshold = 50
bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
last_paso_theta , last_paso_phi = 145, 192
call = 0

def adjust_coord(handx, handy, w1, y1, n_pasos):
	global last_paso_theta
	global last_paso_phi

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


def removeBG(frame):
    fgmask = bgModel.apply(frame)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


while True:

	grabbed, frame = cap.read()
	grabbed, frame2 = cap2.read()
	frame = cv2.flip(frame, 1)
	w , h = frame.shape[1], frame.shape[0]
	centerx = int(round(w/2))
	centery = int(round(h/2))

	#print("W= {}, H={}".format(w, h))

	res = removeBG(frame)

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
		if np.abs(paso_phi-last_paso_phi)>4:
			paso_phi = last_paso_phi

		last_paso_theta, last_paso_phi = paso_theta, paso_phi

		print("theta {}, phi {}".format(paso_theta, paso_phi))

	# show the skin in the image along with the mask0
	cv2.imshow("Draw", drawing)
	cv2.imshow("Image", frame)
	cv2.imshow("MOG2", skinMask)
	cv2.imshow("CAM2", frame2)
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
