#! /usr/bin/env python

from mn.params.genparamslib import *
import sys

fname = sys.argv[1]
fps = sys.argv[2]

genpgf(fname, fps)
