#! /usr/bin/env python

import sys
import os
import mn.params.genparamslib as genparamslib

#Run from /experiment/ folder.

print('parameters file')

CAPPARAMSFILE = sys.argv[1] #Text file containing capillary movie parameters.

#Makes capparams files.
genparamslib.gencapparams(CAPPARAMSFILE)



