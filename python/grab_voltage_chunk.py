# -*- coding: utf-8 -*-
"""
Grabs 5 second chunks of voltage data being sampled at
100 Hz
"""
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from scipy import fftpack
from scipy import signal


ser = serial.Serial('COM3', 9600)
time.sleep(2)
ser.readline()
ser.readline()

xs = []
ys = []
time = 0 #time in ms

#Sampling at 10 ms, end at 5 s
while time < 5000:
    
    time += 10
    data = ser.readline() # read data from serial    
    try:
        print(data.decode())
        ys.append(float(data.decode()))
        xs.append(time)
    
    except ValueError:
        print("error reading float")

plt.subplot(311)
plt.plot(xs, ys)
plt.xlabel('time (ms)')
plt.ylabel('Voltage (V)')

y = np.asarray(ys)
x = np.asarray(xs)
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
filename = "5s_voltagechunk_" + dt_string
np.savez_compressed(os.path.join("data", filename), y)

sos = signal.butter(3, 3, 'hp', fs=10, output='sos')
filtered = signal.sosfilt(sos, y)

filename = "5s_filteredvoltagechunk_" + dt_string
np.savez_compressed(os.path.join("data", filename), sos)
plt.subplot(312)
plt.plot(x, filtered)
plt.grid()
plt.xlabel('time (ms)')
plt.ylabel('Filtered Voltage (V)')
plt.show()

fy = fftpack.rfft(filtered)
dt = 0.01 #10 ms
n = x.size
freqs = fftpack.fftfreq(n, d=dt) # Frequencies associated with each samples
new_freqs = fftpack.fftshift(freqs)
new_freqs = np.around(new_freqs, decimals=2)
freq_shift = fftpack.fftshift(abs(fy))

filename = "5s_fft_" + dt_string
np.savez_compressed(os.path.join("data", filename), freq_shift)

plt.subplot(313)
plt.plot(new_freqs, freq_shift)
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel(r'Spectral Amplitude')
plt.show()

