import numpy as np
import matplotlib.pyplot as plt


def main():
    mu, sigma = 0, 0.1  # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)
    np.savetxt('test1.out', s, fmt='%1.6e')
    s = np.loadtxt('test1.out')
    plt.hist(s, bins='auto')
    plt.show()

if __name__ == "__main__": main()