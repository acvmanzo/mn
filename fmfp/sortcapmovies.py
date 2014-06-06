#! /usr/bin/env python

import sys
import fmfplib
import mn.cap.pcapm as pcapm
import os

#Run from /experiment/ folder.

print('1-capfmf movielist, 2-fmf folder')

CAPFMFFILE = sys.argv[1] #Text file containing a list of capfmf movies.
FMFFOLDER = sys.argv[2] #Folder the fmfs are in.

#Moves capillary movies to the folder 'capfmfs'.
l = pcapm.capmovielist(CAPFMFFILE)

os.chdir(FMFFOLDER)
pcapm.mvcapmovies(l, capdirname='capfmfs')

#Converts fmfs to a jpg.
os.chdir('../capfmfs')
params = fmfplib.WBalRParams(0, 1, 1, 1, 'jpg', 'jpg')
fmfplib.b_fmfconvimg(params)

#Makes some directories that are needed for future scripts.
os.chdir('../')
os.mkdir('data')
os.mkdir('data_cap')
os.mkdir('roi_jpegs')
