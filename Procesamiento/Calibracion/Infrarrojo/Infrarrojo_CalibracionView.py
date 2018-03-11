import serial
import matplotlib.pyplot as plt
import numpy as np
import time


def main():
    #Amplitud_matrix = np.loadtxt('Sensor_Data/Infra30cm.out')
    Amplitud_matrix = np.loadtxt('InfraLowpassNoMotor.out')
    print("Media = {}, Dev = {}, Nmediciones = {} ".format(np.mean(Amplitud_matrix), np.std(Amplitud_matrix, ddof=1),
                                                           Amplitud_matrix.shape[0]))
    plt.figure()
    plt.subplot(2,1,1)
    plt.hist(Amplitud_matrix, bins='auto')
    plt.title("Histogramas de Infrarrojo 20 cm")
    plt.subplot(2,1,2)
    plt.plot(Amplitud_matrix)
    plt.title("Histogramas de Infrarrojo 20 cm")
    plt.show()


if __name__ == "__main__": main()