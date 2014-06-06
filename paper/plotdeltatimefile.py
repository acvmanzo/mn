#! /usr/bin/env python

import mn.plot.genplotlib as genplotlib
from mn.cmn.cmn import *
from mn.cmn.writefiles import *
import sys
import matplotlib.pyplot as plt
import os

fname = sys.argv[1]
keyfile = sys.argv[2]
plotname = sys.argv[3]
meansfname = sys.argv[4]


def plotbar(dictdata, keylist, plotname, fdir='.', ylim=10):
    """Plots bar graph from data in 'peakf.txt' and saves it in the summary directory. Run from a 
    data/ or summary/ folder."""
    
    dictmeans = genplotlib.genlist(dictdata)
    n = []
    for i, v in dictdata.iteritems():
        n.append(max(v))
    
    plt.figure()
    genplotlib.plotdata(d, md, k, 'b', 'Delay (seconds)', 'Time delay', ymin=0.05, ylim=(max(n)))
    plt.savefig(plotname)

print(os.path.abspath(os.getcwd()))
k = load_keys(keyfile)
d = genplotlib.gendict_phase(fname, 'deltatime')
print(d)
md = genplotlib.genlist(d)
print(md)

writemeans(md, meansfname)

plotbar(d, k, plotname)

