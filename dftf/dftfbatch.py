#! /usr/bin/env python

# Run from the 'data' folder.

import sys
import os
import dftf
from mn.cmn.cmn import *

DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'

keyfile = os.path.join(makepardir(), KEYLIST)
K = load_keys(keyfile)

print('Plotting traces')    


# Specifies name of the columns from the imageJ results file and the names of the rois.
#COLS= ['Mean1', 'Mean2']
#ROIS = ['roi1', 'roi2']

COLS= ['Mean1']
ROIS = ['roi1']


for roi in ROIS:
# Deletes any summary files that are present.
    dftf.deloldsummfile(roi, '.')
  
# Generates a list of movie paths in the data folder.
files = dftf.batch_s('.')   

# Generates dft traces and plots for each roi in each movie.
for file in files:
    os.chdir(file)
    print(os.path.basename(file))

    for col in COLS:
        if os.path.exists('params') != True:
            print('No params file')
            
        if os.path.exists('params') == True:
            rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
            corrparamsfile=CORRPARAMS_FILE, colname=col)
            try:
                td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)
            except IOError:
                print('No results1.txt file?')
                continue

            dftf.plotandsavealltraces(td, fdir=file)
            dftf.writepeakf_d(td, fdir=file)


 #Generates a file listing the number of frames used.
for file in files:
    os.chdir(file)
    if os.path.exists('params') == True:
        dl = {}
        for l in open('params'):
            name, val = l.split(',')
            dl[name] = val
        psumm = os.path.join(os.path.dirname(os.path.abspath('../')), 'summary', 'sample_length_'+dl['sample_length'].rstrip('\n'))
        with open(psumm, 'w') as g:
            pass
        break
        
print(os.getcwd())
os.chdir('..')

# Generates bar and scatter plots for each roi.
for roi in ROIS:
    dftf.plotandsavebargraph(roi, K, fdir='.')
    dftf.plotandsavescatterplot(roi, K, fdir='.')
        

