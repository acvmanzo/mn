#! /usr/bin/env python

import matplotlib.pyplot as plt
import mn.plot.genplotlib as gpl
from mn.cmn.cmn import *
import sys

print('arg1 = volperpump file, arg2 = keyfile, arg3 = plotname, arg4 = meansfname')

fname = sys.argv[1]
keyfile = sys.argv[2]
plotname = sys.argv[3]
meansfname = sys.argv[4]

def plotbar(dd, md, k):
    
    k = load_keys(keyfile)

    n = []
    for i, v in dd.iteritems():
        n.append(max(v))
    plt.figure()
    #gpl.plotdata(dd, md, K, 'b', 'nL', 'Volume per pump', ymin=0, ylim=max(n)+0.1*max(n))
    gpl.plotdata(dd, md, k, 'b', 'nL', 'Volume per pump', ymin=0, ylim=4)

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

dd = gpl.gendict_volperpump(fname)
md = gpl.genlist(dd)

writemeans(md, meansfname)

plotbar(dd, md, k)

