#! /usr/bin/env python

from mn.cap.pcapm import *
from mn.plot.genplotlib import *
from mn.cmn.cmn import *
import sys

fname = sys.argv[1] #File containing capdata
keyfile = sys.argv[2] #Name of file containing keylist
plotname = sys.argv[3] #Name of output plot.
meansfname = sys.argv[4] #Name of output means file.


def plotbar(dictdata, keylist, plotname, fdir='.', ylim=25):
    """Plots bar graph from data in 'peakf.txt' and saves it in the summary directory. Run from a 
    data/ or summary/ folder."""
    
    dictmeans = genlist(dictdata)
    #~ keylist = genplotlib.genkeylist(dictdata)
    plotdata(dictdata, dictmeans, keylist, 'b', ylabel='nL/sec', ftitle='Amount drunk/time ', ylim=ylim)
    plt.savefig(plotname)


def writemeans(dict, meansfile):
    with open(meansfile, 'w') as f:
        f.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
        for k, v in dict.iteritems():
            f.write(k + ',')
            for x in v:
                f.write(str(x) + ',')
            f.write('\n')
        

k = load_keys(keyfile)
d = gendictnps(fname)
md = genlist(d)
print(md)
writemeans(md, meansfname)

plotbar(d, k, plotname)

