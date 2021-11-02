
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

import numpy as np
import matplotlib.pyplot as plt
 
filesize = 10615705

plt.figure(figsize=(20, 10))
x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
y1 = [66.235, 105.564, 177.241, 198.462, 234.572, 301.134, 377.306, 462.941, 553.350, 639.462, 749.213]
plt.xlabel("Corruption Percentage")
plt.ylabel("Time in seconds")
plt.plot(x, y1)
plt.show()
 
 
plt.figure(figsize=(20, 10))
x = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
y2 = [66.235, 69.2313, 93.137, 128.571, 170.532, 179.420, 196.167, 228.451, 261.628, 294.373, 310.907]
plt.xlabel("Delay in ms")
plt.ylabel("Time in seconds")
plt.plot(x, y2)
plt.show()
 
 
plt.figure(figsize=(20, 10))
x = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80]
y3 = [50.768, 51.0588, 52.516, 57.212, 88.568, 106.338, 169.662, 272.732, 461.918, 1211.521]
plt.xlabel("Packet Loss Percentage")
plt.ylabel("Time in seconds")
plt.plot(x, y3)
plt.show()

# Throughput graphs

plt.figure(figsize=(20, 10))
x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
newY = [filesize/i for i in y1]
plt.xlabel("Corruption Percentage")
plt.ylabel("Throughput in bytes/sec")
plt.plot(x, newY)
plt.show()
 
 
plt.figure(figsize=(20, 10))
x = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
newY = [filesize/i for i in y2]
plt.xlabel("Delay in ms")
plt.ylabel("Throughput in bytes/sec")
plt.plot(x, newY)
plt.show()
 
 
plt.figure(figsize=(20, 10))
x = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80]
newY = [filesize/i for i in y3]
plt.xlabel("Packet Loss Percentage")
plt.ylabel("Throughput in bytes/sec")
plt.plot(x, newY)
plt.show()