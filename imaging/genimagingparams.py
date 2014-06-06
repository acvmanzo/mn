import glob
import os
import numpy as np
import mn.imaging.gclib as gclib

# Run from the data folder.

BGSEC = 3
STIMSEC = 8

movies = glob.glob('*')
for movie in movies:
    os.chdir(movie)
    a = gclib.TraceData('results1.txt', 'params')
    td = a.Processrawtrace()
    maxf = td['Mean1']['dff']['peaki']+ 1
    
    d={}
    with open('params', 'r') as g:
        for l in g:
            d[l.split(',')[0]] = l.split(',')[1]
    
    fps = float(d['fps'])
    stimfr = np.rint(STIMSEC * fps)
    bgfr = np.rint((STIMSEC-BGSEC) * fps)
    
    with open('imaging_params.m', 'w') as f:
        f.write('stim_frame = ' + str(stimfr) + '\n')
        f.write('bg_frame = ' + str(bgfr)+'\n')
        f.write('max_frame = ' + str(maxf))
        
    os.chdir('../')
