#! /usr/bin/env python

import mn.fmfp.fmfplib as fmfplib
import sys

print('type r, g, b')

r = sys.argv[1]
g = sys.argv[2]
b = sys.argv[3]


params = fmfplib.WBalRParams(0, r, g, b, 'bmp', 'jpg')
fmfplib.b_movie_fmfconvwb(params)
