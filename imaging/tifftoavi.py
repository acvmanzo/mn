#! /usr/bin/env python

import os
import glob
import mn.cmn.cmn as cmn
import shutil

# Script for batch converting multipage tiff files to avi files using ImageJ.

wdir = os.path.abspath('.')
print(wdir)
names = glob.glob('*.tiff')
# List of input files in the directory.
inputs = [os.path.abspath(name) for name in names]
roots, exts = zip(*[os.path.splitext(name) for name in names])
# Creates a list of output files with .avi as extension.
outputs = [os.path.join(wdir, root+'.avi') for root in roots]
ios = zip(inputs, outputs)
# List of arguments to feed into ImageJ macro, where each item is inputfile_outputfile.
args = [io[0]+'%'+io[1] for io in ios]

for arg in args:
    cmd = 'java -jar /home/andrea/software/ImageJ/ij.jar -batch /home/andrea/software/ImageJ/macros/tifftoavi.txt {0}'.format(arg)
    os.system(cmd)


