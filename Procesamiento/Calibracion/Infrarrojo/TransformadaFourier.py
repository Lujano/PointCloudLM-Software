#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from scipy.fftpack import fft, fftfreq
from scipy import signal, arange

def plotSpectrum(y, Fs):
    """

    grafica la amplitud del espectro de y(t)

    """

    n = len(y)  # longitud de la señal
    k = arange(n)
    T = n / Fs
    frq = k / T  # 2 lados del rango de frecuancia
    print(type(frq))
    frq = frq[range(int(n / 2))]  # Un lado del rango de frecuencia
    Y_ = fft(y) / n  # fft calcula la normalizacion
    Y_ = Y_[range(int(n / 2))]
    plt.plot(frq, abs(Y_), 'r')  # grafica el espectro de frecuencia
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('|Y(f)|')

def main():
    Fs = 10000.0 # tasa de muestreo
    Ts = 1.0/Fs # intervalo de tiempo

#ARCHIVO------------------------------------------------------------

    Y = np.zeros((0, 1), dtype=np.float)
    try:
        with open("SenalSensorSerial.txt", "r") as out_file:
            lines = out_file.readlines()
            for line in lines:
                Lectura = np.fromstring(line, dtype=float, sep=' ')
                Y = np.vstack([Y, Lectura[1]])
    except:
        print("Error al abrir el archivo")
        out_file.close()
#--------------------------------------------------------------------
    
    signal_vector = np.loadtxt('InfraPRUEBA2.out')
    t_size = len(Y)#signal_vector.size
    t_vector = np.arange(0, Ts*t_size, Ts )
    #y = signal_vector
    print(type(signal_vector))
    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(Y, bins='auto')
    plt.title("Histogramas de Infrarrojo 20 cm")
    plt.subplot(2,2,2)
    plt.plot(t_vector, Y)
    plt.title("Se#al en tiempo")

    plt.subplot(2,2,3)
    plotSpectrum(Y, Fs)
    plt.title("Se#al en frecuencia")
    plt.show()

main()