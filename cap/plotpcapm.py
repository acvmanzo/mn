#! /usr/bin/env python

import pcapm
import os
import matplotlib.pyplot as plt
import mn.plot.genplotlib as gp
from mn.cmn.cmn import *
import sys

capdatafile = sys.argv[1]


#Run from the data/ folder.
KEYLIST = 'keylist'

# Loads the keyfile (order of conditions for plotting).
keyfile = os.path.join(makepardir(), KEYLIST)
K = load_keys(keyfile)


pcapm.plotpixpersec(capdatafile, K)
pcapm.plotnlpersec(capdatafile, K)



