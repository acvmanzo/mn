#! /usr/bin/env python

from mn.imaging.dyearea import *
from mn.imaging.gclib import *
import sys

#~ Start from the gal4/summary folder.

fname = sys.argv[1]

kfile = os.path.join(os.path.dirname(os.path.abspath('.')), 'keylist')
K = load_keys(kfile)

plotdyearea(fname, K)
#plotdyearea_3d2(fname, K)
