import numpy as np
import matplotlib.pyplot as plt

plt.axis('auto')
plt.ion()

for i in range(1000):
    y = 2
    plt.scatter(i, y)
    plt.pause(0.55)

