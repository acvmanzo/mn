#! /usr/bin/env python

import sys
import os
import mn.params.genparamslib as genparamslib


#Run from experiment/ folder.

print('1- parameters file, 2-fps, 3-cutoff')

FRAMES_FILE = sys.argv[1] #Text file containing capillary movie parameters.
FPS = sys.argv[2]
CUTOFF = sys.argv[3]

#Makes pdframes file for phasebatch.
genparamslib.genpdframes(FRAMES_FILE, FPS)

#Makes params file for dftfbatch.
genparamslib.genplfc(FRAMES_FILE, FPS, CUTOFF)

#Makes capparams files.
genparamslib.gencapparams(FRAMES_FILE)



