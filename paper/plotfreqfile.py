#! /usr/bin/env python

from mn.plot.genplotlib import *
from mn.cmn.cmn import *
import sys

fname = sys.argv[1]
keyfile = sys.argv[2]
plotname = sys.argv[3]
meansfname = sys.argv[4]


def plotbar(dictdata, keylist, plotname, fdir='.', ylim=10):
    """Plots bar graph from data in 'peakf.txt' and saves it in the summary directory. Run from a 
    data/ or summary/ folder."""
    
    dictmeans = genlist(dictdata)
    #~ keylist = genplotlib.genkeylist(dictdata)
    plotdata(dictdata, dictmeans, keylist, 'b', ylabel='Hz', ftitle='Mean pumping ' + 
    'frequency ', ylim=ylim)
    plt.savefig(plotname)


def writemeans(dictmeans, meansfile):
    with open(meansfile, 'w') as f:
        f.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
        for k, v in dictmeans.iteritems():
            f.write(k + ',')
            for x in v:
                f.write(str(x) + ',')
            f.write('\n')
        

k = load_keys(keyfile)
d = gendict(fname)
md = genlist(d)
print(md)
writemeans(md, meansfname)

plotbar(d, k, plotname)

