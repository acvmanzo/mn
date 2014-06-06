#! /usr/bin/env python

import mn.fmfp.fmfplib as fmfplib

params = fmfplib.WBalRParams(0, 1, 1, 1, 'jpg', 'jpg')
fmfplib.b_fmfconv(params)

