import cv2
import matplotlib.pyplot as plt


im = cv2.imread('hand_grass.jpeg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
plt.figure("Hand on grass")
plt.subplot(2, 2, 1)
plt.imshow(im[..., ::-1])
plt.subplot(2, 2, 2)
plt.imshow(imgray[..., ::-1])
plt.subplot(2, 2, 3)
plt.imshow(im2[..., ::-1])
plt.subplot(2, 2, 4)
plt.waitforbuttonpress()