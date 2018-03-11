#!/usr/bin/env python
# -*- coding: utf-8 -*-



# n = 2 ** 6  # Número de intervalos
# f = 400.0  # Hz
# dt = 1 / (f * 16)  # Espaciado, 16 puntos por período
# t = np.linspace(0, (n - 1) * dt, n)  # Intervalo de tiempo en segundos
# y= signal.square(2 * np.pi * f* t)
# plt.figure()
# plt.axis('auto')
# plt.plot(t, y)
# plt.plot(t, y, 'ko')
# plt.xlabel('Tiempo (s)')
# plt.ylabel('$y(t)$')
#
#
# plt.figure()
# Y = fft(y) / n  # Normalizada
# frq = fftfreq(n, dt)  # Recuperamos las frecuencias
# plt.plot(frq, np.abs(Y))  # Representamos la parte imaginaria
# plt.annotate(s=u'f = 400 Hz', xy=(400.0, -0.5), xytext=(400.0 + 1000.0, -0.5 - 0.35), arrowprops=dict(arrowstyle = "->"))
# plt.annotate(s=u'f = -400 Hz', xy=(-400.0, 0.5), xytext=(-400.0 - 2000.0, 0.5 + 0.15), arrowprops=dict(arrowstyle = "->"))
# plt.annotate(s=u'f = 800 Hz', xy=(800.0, 0.25), xytext=(800.0 + 600.0, 0.25 + 0.35), arrowprops=dict(arrowstyle = "->"))
# plt.annotate(s=u'f = -800 Hz', xy=(-800.0, -0.25), xytext=(-800.0 - 1000.0, -0.25 - 0.35), arrowprops=dict(arrowstyle = "->"))
# plt.ylim(-1, 1)
# plt.xlabel('Frecuencia (Hz)')
# plt.ylabel('Im($Y$)')
#
#
# plt.show()
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from scipy.fftpack import fft, fftfreq
from scipy import signal, arange

def plotSpectrum(y,Fs):
     """

     grafica la amplitud del espectro de y(t)

     """

     n = len(y) # longitud de la señal
     k = arange(n)
     T = n/Fs
     frq = k/T # 2 lados del rango de frecuancia
     frq = frq[range(n/2)] # Un lado del rango de frecuencia
     Y = fft(y)/n # fft calcula la normalizacion
     Y = Y[range(n/2)]
     plt.plot(frq,abs(Y),'r') # grafica el espectro de frecuencia
     plt.xlabel('Frecuencia (Hz)')
     plt.ylabel('|Y(f)|')

def main():
    Fs = 2000.0 # tasa de muestreo
    Ts = 1.0/Fs # intervalo de tiempo
    signal_vector = np.loadtxt('InfraPRUEBA2.out')
    t_size = signal_vector.size
    t_vector = np.arange(0, Ts*t_size, Ts )
    y = signal_vector

    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(signal_vector, bins='auto')
    plt.title("Histogramas de Infrarrojo 20 cm")
    plt.subplot(2,2,2)
    plt.plot(t_vector, signal_vector)
    plt.title("Se#al en tiempo")

    plt.subplot(2,2,3)
    plotSpectrum(y, Fs)
    plt.title("Se#al en frecuencia")
    plt.show()

if __name__ == "__main__": main()