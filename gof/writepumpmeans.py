#! /usr/bin/env python

import mn.plot.genplotlib as gpl
from mn.cmn.cmn import *
import mn.gof.gfplot as gf
import sys

fname = sys.argv[1]
keyfile = sys.argv[2]
meansfname = sys.argv[3]



def writemeans(dict, meansfile):
    with open(meansfile, 'w') as f:
        f.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
        for k, v in dict.iteritems():
            f.write(k + ',')
            for x in v:
                f.write(str(x) + ',')
            f.write('\n')
        

k = load_keys(keyfile)
cib, pumps = gf.gendictgf(fname)
mpumps = gpl.genlist(pumps)
print(mpumps)
writemeans(mpumps, meansfname)


#plotbar(mpumps, k, plotname)

