#! /usr/bin/env python

import mn.plot.genplotlib as gpl
from mn.cmn.cmn import *
import mn.gof.gfplot as gf
import sys

print('fname, type, keyfile, outputfile; type = diffa or areameans')

fname = sys.argv[1]
type = sys.argv[2] #Choose diffa or areameans.
keyfile = sys.argv[3]
outputfile = sys.argv[4]




def writemeans(dict, meansfile):
    with open(meansfile, 'w') as f:
        f.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
        for k, v in dict.iteritems():
            f.write(k + ',')
            for x in v:
                f.write(str(x) + ',')
            f.write('\n')
        

k = load_keys(keyfile)    
darea, ddiffa = gpl.gendict_cibgf(fname)
mdarea, mddiffa = map(gpl.genlist, [darea, ddiffa])

if type == 'diffa':
    writemeans(mddiffa, outputfile)

if type == 'areameans':
    writemeans(mdarea, outputfile)
