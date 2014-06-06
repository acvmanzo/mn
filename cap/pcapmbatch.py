#! /usr/bin/env python

import pcapm
import os
import matplotlib.pyplot as plt
import mn.plot.genplotlib as gp
from mn.cmn.cmn import *


#Run from the data/ folder.
CAPDATAFILE = 'capdata.txt'
KEYLIST = 'keylist'

# Loads the keyfile (order of conditions for plotting).
keyfile = os.path.join(makepardir(), KEYLIST)
K = load_keys(keyfile)

# Deletes an older summary file if present.
pcapm.deloldsummfile(CAPDATAFILE, '.')

# Finds the pixels per second and nL per second of liquid consumed per movie and saves to a text file.
names = pcapm.batchfiles('.')
for name in names:
    print os.path.basename(name)
    pcapm.gencapdata(CAPDATAFILE, name)

# Generates summary plots.
makenewdir('../../summary')
os.chdir('../../summary')

pcapm.plotpixpersec(CAPDATAFILE, K)
pcapm.plotnlpersec(CAPDATAFILE, K)


#p = pcapm.gendictpps(CAPDATAFILE)
#mp = pcapm.genlist(p)
#k = p.keys()
#gp.plotdata(p, mp, k, 's', 'pix/sec', 'Amount consumed \n pixels/sec', ylim=10, titlesize='x-large', xlabelsize='medium', xstart=0.25)
#plt.savefig('pixpersec')
#plt.close()


#n = pcapm.gendictnps(CAPDATAFILE)
#mn = pcapm.genlist(n)
#l = n.keys()
#gp.plotdata(n, mn, l, 's', 'nL/sec', 'Amount consumed \n nL/sec', ylim=10, titlesize='x-large', xlabelsize='medium', xstart=0.25)
#plt.savefig('nlpersec')
##plt.show()
