"""
Aqui se implemento tomar 16 mediciones para tener un promedio del infrarrojo
"""

import serial
import matplotlib.pyplot as plt
import numpy as np
import time

def open_port():
    ser = serial.Serial('COM8', 115200)

    return ser

def close_port(port):
    port.close()

def detect_data(port):
    #port.reset_input_buffer()
    flag = True

    while flag:
        anuncio = port.read(1)
        anuncio = ord(anuncio[0]) # convertir en entero

        if (anuncio & 0xf0)  == 0xf0:# Se detecta el byte de anuncio de trama
                n_canales = anuncio & 0x0f # Numero de canales a leer
                return  n_canales

def main():
    port = open_port()
    i = 0.00
    y = 0.00
    print("Inicio")
    Amplitud_matrix = np.array([])
    #Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio

    while(Dif < 20):




        n_canales = detect_data(port)
        data1_in = port.read(2*n_canales)
        canal_n1 = (2 ** 15) * ord(data1_in[0]) + (2 ** 8) * ord(data1_in[1]) + (2 ** 7) * ord(data1_in[2]) + ord(data1_in[3])
        y = canal_n1*3.1/(2**12-1) # Escalamiento, el voltaje de ref de adc es 3.1
        y = y/16
        print(y)
        Amplitud_matrix = np.append(Amplitud_matrix, [y])
        T_Final = time.time()
        Dif = T_Final - T_Inicio
    #Amplitud_matrix = np.append(Amplitud_matrix, [y])

    close_port(port)
    # np.savetxt('InfraDC.out', Amplitud_matrix, fmt='%1.8e')
    print("Media = {}, Dev = {}, Nmediciones = {} ".format(np.mean(Amplitud_matrix), np.std(Amplitud_matrix, ddof=1),
                                                            Amplitud_matrix.shape[0]))
    plt.hist(Amplitud_matrix, bins='auto')
    plt.title("Histogramas de Infrarrojo Calibracion 2")
    plt.show()


if __name__ == "__main__": main()