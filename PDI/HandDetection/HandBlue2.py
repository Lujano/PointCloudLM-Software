# USAGE
# python skindetector.py
# python skindetector.py --video video/skin_example.mov

# import the necessary packages
import numpy as np
import cv2

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([100, 100, 50], dtype = "uint8")
upper = np.array([130, 255, 250], dtype = "uint8")

cap = cv2.VideoCapture(0)

while True:
	# grab the current frame
	grabbed, frame = cap.read()
	# kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
	# im = cv2.filter2D(frame, -1, kernel)
	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video

	# resize the frame, convert it to the HSV color space,
	# and determine the HSV pixel intensities that fall into
	# the speicifed upper and lower boundaries
	#frame = imutils.resize(frame, width = 400)
	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	skinMask = cv2.inRange(converted, lower, upper)
	kernel = np.ones((3, 3), np.uint8)
	#skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_OPEN, kernel)
	skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)

	# apply a series of erosions and dilations to the mask
	# using an elliptical kernel
	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	# skinMask = cv2.erode(skinMask, kernel, iterations = 2)
	# skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	# # skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)
	# skinMask = cv2.dilate(skinMask, kernel, iterations=2)
	# blur the mask to help remove noise, then apply the
	# mask to the frame
	skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
	skin = cv2.bitwise_and(frame, frame, mask = skinMask)

	# show the skin in the image along with the mask
	cv2.imshow("images", np.hstack([frame, skin]))
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
