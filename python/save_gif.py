# -*- coding: utf-8 -*-
"""
Plot Voltage data coming from Arduino and save to gif
"""
import serial
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import time

ser = serial.Serial('COM3', 9600)
time.sleep(2)
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x_len = 200         # Number of points to display
y_range = [0, 5] 
plt.style.use('ggplot')

xs = []
ys = []
ax.set_ylim(y_range)

line = ax.plot(xs, ys)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    data = ser.readline() # read data from serial
    
    # Add x and y to lists
    try:
        print(data.decode())
        ys.append(float(data.decode()))
        xs.append(i)

    except ValueError:
        print("error reading float")

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
animate.save('example_graph.gif', writer='imagemagick', fps=30)
plt.show()
