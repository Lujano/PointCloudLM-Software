import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

def main():
    directory = 'Temporal_Si_motor'
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
    order = 10# Orden del polinomio
    poly = np.polyfit(Voltage_matrix, Distance_matrix, order)
    p = np.poly1d(poly)

    # Graficas
    plt.figure()
    plt.scatter(Distance_matrix, Voltage_matrix)
    plt.title("Datos del sensor")
    plt.xlabel("Distancia (cm)")
    plt.ylabel("Voltage(Volts)")
    plt.show()



#files = glob.glob('*.out')


if __name__ == "__main__": main()