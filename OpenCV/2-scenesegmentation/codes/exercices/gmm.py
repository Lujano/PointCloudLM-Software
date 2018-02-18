import cv2
import numpy as np
from sklearn import mixture
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal


imBGR = cv2.imread("../ressources/landscape_hdr.jpg")

# Segment that image in N different cluster using a Gaussian mixture model (e.g. N=17)
# 1. Create the gaussian mixture
N = 3
#g = mixture.GaussianMixture(n_components=N, max_iter=100)

newdata = imBGR.reshape(imBGR.shape(0)*imBGR.shape(1), 4)
gmm = GaussianMixture(n_components=3, covariance_type="tied")
gmm = gmm.fit(newdata)

cluster = gmm.predict(newdata)
cluster = cluster.reshape(800, 800)
imshow(cluster)
plt.waitforbuttonpress()
# 2. Fit the image observed to the GMM:
#obs = np.array(imBGR).reshape(-1,1)

#g.fit(obs)
#y = g.score_samples(obs)

plt.plot(y)
plt.show()
plt.waitforbuttonpress()

# means and cov of the gmm are stored in:
# g.means_
# g.covariances_

# Use the Probability Distribution Function (PDF) to compute which pixel belong to which Gaussian
#  and assign the mean of the gaussian to the pixels
plt.figure()
plt.imshow(imBGR[..., ::-1])
plt.show()