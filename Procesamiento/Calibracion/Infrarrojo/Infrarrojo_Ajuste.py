import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

def main():
    directory = 'Sensor_Data_NoMotor'
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
    poly = np.polyfit(Distance_matrix, Voltage_matrix, 3)
    p = np.poly1d(poly)

    #Graficas
    figure
    plt.subplot(2,1, 1)
    plt.scatter(Distance_matrix, Voltage_matrix)
    plt.subplot(2,1,2)

    p(Distance_matrix)
    plt.show()



#files = glob.glob('*.out')


if __name__ == "__main__": main()