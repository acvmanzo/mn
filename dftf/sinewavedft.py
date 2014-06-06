import numpy as np
import matplotlib.pyplot as plt
from mn.dftf.dftf import *


x = np.linspace(0, 6*np.pi, 100).tolist()
print(len(x))
x1 = [3*num for num in x]
print(len(x1))
y1 = np.sin(x).tolist()
y2 = np.sin(x1).tolist()
y2 = [num * 2 for num in y2]
z = np.zeros(100)

y = []
y.extend(y1)
y.extend(z)
y.extend(y2)
y.extend(y2)
plt.subplot(121)
plt.plot(y)
print(len(y))

x1 = np.linspace(0, 300, 300)

#yh = hmsub(y)
dft = dft(y, 1200)
print(len(dft))
plt.subplot(122)
plt.plot(dft[0:len(dft)/2])
plt.show()
