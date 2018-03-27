import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

def main():
    directory = 'Sensor_Data2'
    a= os.listdir(directory)
    Distance_matrix = np.array([])
    Voltage_matrix = np.array([])
    for element in a:
        distance_cm = float(element.replace('Infra_','').replace('cm.out', ''))

        Data = np.loadtxt(directory+'/'+element)
        media = np.mean(Data)
        desv =  np.std(Data, ddof=1)
        print("Media = {}, Dev = {}, Nmediciones = {}, distancia = {} ".format(media,desv,
                                                         Data.shape[0], distance_cm))
        Distance_matrix = np.append(Distance_matrix, [distance_cm])
        Voltage_matrix = np.append(Voltage_matrix, [media])

    # Ajuste polinomial a data
    order =12 # Orden del polinomio
    poly = np.polyfit(Voltage_matrix, Distance_matrix, order)
    p = np.poly1d(poly)
    np.savetxt('Polinomio_Ajuste_Infra2.out', poly, fmt='%1.12e')

    # Graficas
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.scatter(Voltage_matrix, Distance_matrix)
    plt.title("Datos del sensor")
    plt.subplot(2, 2, 2)
    plt.scatter(Voltage_matrix, p(Voltage_matrix))
    plt.title("Polinomio orden {} ajustado a la data".format(order))
    plt.subplot(2, 2, 3)
    time_cont = np.arange(0.8, 3, 0.01)
    plt.plot(time_cont, p(time_cont))
    plt.title("Polinomio orden {} ajustado continuo".format(order))
    plt.subplot(2, 2, 4)
    plt.scatter(Voltage_matrix, Distance_matrix, c = 'g')
    plt.subplot(2, 2, 4)
    plt.scatter(Voltage_matrix, p(Voltage_matrix), c = 'r')
    plt.title("Datos del sensor vs Polinomio")

    plt.show()



#files = glob.glob('*.out')


if __name__ == "__main__": main()