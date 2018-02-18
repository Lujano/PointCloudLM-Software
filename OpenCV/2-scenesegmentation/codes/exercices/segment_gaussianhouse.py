import numpy as np
import cv2
import matplotlib.pyplot as plt


imBGR = cv2.imread("../ressources/house.jpg")
# Convert to BGR to HSV
imHSV = cv2.cvtColor(imBGR, cv2.COLOR_BGR2HSV)

# Segment brick
# Select a sub part of the image:
y1 = 309
y2 = 330
x1 = 300
x2 = 320
patch_bricks = imHSV[y1:y2, x1:x2]

h, s, v = cv2.split(patch_bricks)
muh = np.mean(h[0])
sigmah = np.std(h)
mus = np.mean(s)
sigmas = np.std(s)

muv = np.mean(v)
sigmav = np.std(v)


h2 = np.random.normal(muh, sigmah, h.size)
s2 = np.random.normal(mus, sigmas, h.size)
v2 = np.random.normal(muv, sigmav, h.size)

imgGauss = cv2.merge((h,s,v))
print(hb)
print("jaja")
print(h)


# Build a histogram:
hist_bricks = cv2.calcHist([patch_bricks], channels = [0], mask=None, histSize=[180], ranges=[0, 179])

hist_bricks2 = cv2.calcHist([imgGauss], channels = [0], mask=None, histSize=[180], ranges=[0, 179])

plt.figure("Gr2")
plt.subplot(3, 1, 1)
plt.plot(hist_bricks)
plt.subplot(3, 1, 2)
plt.plot(hist_bricks2)
plt.show()


""""
# Don't forget to plot a BGR image

plt.figure("Grass")
plt.imshow(lhMap_grass[..., : : -1])
plt.figure("Path")
plt.imshow(lhMap_path[..., : : -1])

plt.figure("Bricks")
plt.imshow(lhMap_bricks[..., : : -1])
plt.figure("Roof")
plt.imshow(lhMap_roof[..., : : -1])

plt.figure("Original")
plt.imshow(imBGR[..., : : -1])
plt.show()

"""

#segLabels
