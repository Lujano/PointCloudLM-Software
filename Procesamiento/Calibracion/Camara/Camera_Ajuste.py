import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

def main():
    Data = np.loadtxt('Sensor_Data_Fix.out') # Distance, pixelx, pixely
    distance_cm = np.array([])
    pixelx= np.array([])
    pixely = np.array([])
    for element in Data:
        distance_cm = np.append(distance_cm, [element[0]])
        pixelx = np.append(pixelx, [element[1]])
        pixely = np.append(pixely, [element[2]])

    # Ajuste polinomial a data
    order =8 # Orden del polinomio
    poly_x = np.polyfit(distance_cm, pixelx, order)
    px = np.poly1d(poly_x)
    np.savetxt('Px.out', poly_x, fmt='%1.12e')

    poly_y = np.polyfit(distance_cm, pixely, order)
    py = np.poly1d(poly_y)
    np.savetxt('Py.out', poly_y, fmt='%1.12e')

    # Graficas
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.scatter(distance_cm, pixelx)
    plt.title("Datos del sensor")
    plt.subplot(2, 2, 2)
    plt.scatter(distance_cm, px(distance_cm))
    plt.title("Polinomio orden {} ajustado a la data".format(order))
    plt.subplot(2, 2, 3)
    time_cont = np.arange(2, 25, 0.01)
    plt.plot(time_cont, px(time_cont))
    plt.title("Polinomio orden {} ajustado continuo".format(order))
    plt.subplot(2, 2, 4)
    plt.scatter(distance_cm, pixelx, c = 'g')
    plt.subplot(2, 2, 4)
    plt.scatter(distance_cm, px(distance_cm), c = 'r')
    plt.title("Datos del sensor vs Polinomio")

    plt.figure()
    plt.subplot(2, 2, 1)
    plt.scatter(distance_cm, pixely)
    plt.title("Datos del sensor")
    plt.subplot(2, 2, 2)
    plt.scatter(distance_cm, py(distance_cm))
    plt.title("Polinomio orden {} ajustado a la data".format(order))
    plt.subplot(2, 2, 3)
    time_cont = np.arange(2, 25, 0.01)
    plt.plot(time_cont, py(time_cont))
    plt.title("Polinomio orden {} ajustado continuo".format(order))
    plt.subplot(2, 2, 4)
    plt.scatter(distance_cm, pixely, c='g')
    plt.subplot(2, 2, 4)
    plt.scatter(distance_cm, py(distance_cm), c='r')
    plt.title("Datos del sensor vs Polinomio")

    plt.show()



#files = glob.glob('*.out')


if __name__ == "__main__": main()