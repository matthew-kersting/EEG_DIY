# -*- coding: utf-8 -*-
"""
Plot Voltage data coming from Arduino
"""
import serial
import matplotlib.animation as animation
from matplotlib import pyplot as plt

ser = serial.Serial('COM3', 9600)
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x_len = 200         # Number of points to display
y_range = [0, 5] 

xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

line = ax.plot(xs, ys)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    data = ser.readline() # read data from serial
    print(data.decode())
    
    # Add x and y to lists
    xs.append(i)
    ys.append(data.decode())

    # Limit x and y lists to 20 items
    xs = xs[-x_len:]
    ys = ys[-x_len:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)
    
    # Format plot
    plt.ylabel('Voltage')


# Set up plot to call animate() function periodically
animate = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
plt.show()
