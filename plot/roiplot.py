#!/usr/bin/env python
     

import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import glob


matplotlib.rc('axes', titlesize='medium')
matplotlib.rc('xtick', labelsize='small')
matplotlib.rc('ytick', labelsize='small')
matplotlib.rc('legend', fontsize='x-small')
matplotlib.rc('savefig', dpi=150)
matplotlib.rc('figure.subplot', left=0.1, right=0.95, hspace=0.25, wspace=0.25)



def loadresultsfile(fname):
    f = open(fname)
    a = f.readline().split()
    f.close()
    b = []
    for x in a: 
        b.append(x.find('Mean1'))
    col = b.index(0) + 1
    return(np.loadtxt(fname, skiprows=1, usecols=(col,)))


if __name__ == '__main__':
    x = loadresultsfile('results1.txt')
    plt.plot(x)
    print(np.min(x))
    #plt.ylim(95 , 115)
    plt.draw()
    plt.show()
