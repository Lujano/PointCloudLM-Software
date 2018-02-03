import numpy as np
import matplotlib.pyplot as plt

matrix = np.zeros((0, 1))
time = np.zeros((0, 1))
for i in range(0, 100):
    matrix = np.append(matrix, [2*i], )
    time = np.append(time, [i], )
plt.plot(matrix, time)
plt.show()