#! /usr/bin/env python

import sys
import mn.cap.pcapm as pcapm
import mn.fmfp.fmfplib as fmfplib
import os

#Run from /experiment/ folder.

print('1-valid movie list, 2-fmf folder')

VALIDFMFFILE = sys.argv[1] #Text file containing a list of movies where the fly extends and drinks 
#(rather than not responding at all).
FMFFOLDER = sys.argv[2] #Folder the fmfs are in.

#Moves valid movies to the folder 'validfmfs'.
l = pcapm.capmovielist(VALIDFMFFILE)
print(l)
os.chdir(FMFFOLDER)
pcapm.mvcapmovies(l, capdirname='validfmfs')
