#! /usr/bin/env python

import sys
import mn.fmfp.fmfplib as fmfplib
import mn.cap.pcapm as pcapm
import os


#~ Run from the folder with fmf movies.

print('1-r, 2-g, 3-b')

r = sys.argv[1]
g = sys.argv[2]
b = sys.argv[3]

params = fmfplib.WBalRParams(0, r, g, b, 'bmp', 'jpg')
fmfplib.b_fmfconv(params)
bmpdir = fmfplib.bdir(params)

fmfplib.b_wbalr_fly(bmpdir, params)
