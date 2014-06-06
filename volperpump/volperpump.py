#! /usr/bin/env python


#~ Start from expt/summary folder.

import mn.plot.genplotlib as gpl
import matplotlib.pyplot as plt
from mn.cmn.cmn import *

import sys

print('arg1 = capfile, arg2 = peakffile, arg3 = writefile, write default 1 1 for defaults')

CAPFILE = sys.argv[1]
PEAKFFILE = sys.argv[2]
CAP_PEAKFFILE = sys.argv[3]

KEYLIST = 'keylist'
if CAPFILE == 'default':
    CAPFILE = 'capdata.txt'
    PEAKFFILE = 'peakf_roi1.txt'
    CAP_PEAKFFILE = 'cap_peakf_roi1_summ.txt'



d = {}

with open(CAPFILE) as f:
    f.next()
    for l in f:
        name, deltalstr, durationstr, pixpersecstr, nlpersecstr, condition = map(str.strip, l.split(','))
        
        nlpersec = float(nlpersecstr)
               
        if name not in d:
            d[name] = {}

        print(name)
        d[name]['cap'] = nlpersec
        d[name]['cond'] = condition


with open(PEAKFFILE) as g:
    g.next()
        
    for l in g:
        name, valuestr, condition = map(str.strip, l.split(','))
        value = float(valuestr)
        
        print(name)
        try:
            d[name]['freq'] = value
        except KeyError:
            continue

with open(CAP_PEAKFFILE, 'w') as h:
    h.write('Movie,nlpersec,peakf_roi1,volperpump,condition\n')
    
    for key, value in sorted(d.iteritems()):        
        try:
            volperpump = value['cap']/value['freq']
            h.write(key + ',{0},{1},{2},{3}\n'.format(value['cap'], value['freq'], volperpump, value['cond']))

        except KeyError:
            continue
        except ZeroDivisionError:
            continue
            

keyfile = os.path.join(makepardir_subexpt(), KEYLIST)
K = load_keys(keyfile)

dd = gpl.gendict_volperpump(CAP_PEAKFFILE)
md = gpl.genlist(dd)

n = []
for i, v in dd.iteritems():
    n.append(max(v))

print(max(n))

plt.figure()
gpl.plotdata(dd, md, K, 's', 'nL', 'Volume per pump', ymin=0, ylim=max(n)+0.1*max(n))
plt.savefig('volperpump_sc')

plt.figure()
#gpl.plotdata(dd, md, K, 'b', 'nL', 'Volume per pump', ymin=0, ylim=max(n)+0.1*max(n))
gpl.plotdata(dd, md, K, 'b', 'nL', 'Volume per pump', ymin=0, ylim=4)

plt.savefig('volperpump_bar')

