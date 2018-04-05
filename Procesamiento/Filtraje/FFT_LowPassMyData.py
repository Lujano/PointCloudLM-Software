#!/usr/bin/env python
# -*- coding: utf-8 -*-



import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 2
cutoff = 7.1535 # desired cutoff frequency of the filter, Hz
fs = 2000
# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 65)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

# Demonstrate the use of the filter.
# First make some data to be filtered.
Fs = 2000.0  # tasa de muestreo
Ts = 1.0 / Fs  # intervalo de tiempo
signal_vector = np.loadtxt('InfraNoLowpass.out')
t_size = signal_vector.size
t_vector = np.arange(0, Ts * t_size, Ts)

data = signal_vector

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, Fs, order)

plt.subplot(2, 1, 2)
plt.plot(t_vector, data, 'b-', label='data')
plt.plot(t_vector, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()