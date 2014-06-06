#! /usr/bin/env python

# Run from the 'data' folder.

import sys
import os
import dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt

DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'

#~ keyfile = os.path.join(makepardir(), KEYLIST)
#~ K = load_keys(keyfile)

K = ['Water', '100 mM sucrose', '1 M sucrose']

#~ 
#~ print('Plotting traces')    
#~ 
#~ 
#~ # Specifies name of the columns from the imageJ results file and the names of the rois.
#~ COLS= ['Mean1', 'Mean2']
#~ ROIS = ['roi1', 'roi2']
#~ 
#~ 
#~ for roi in ROIS:
#~ 
#~ # Deletes any summary files that are present.
    #~ dftf.deloldsummfile(roi, '.')
  
#~ # Generates a list of movie paths in the data folder.
#~ files = dftf.batch_s('.')   
#~ 
#~ # Generates dft traces and plots for each roi in each movie.
#~ for file in files:
    #~ os.chdir(file)
    #~ print(os.path.basename(file))
#~ 
    #~ for col in COLS:
        #~ print(col)
        #~ try:
            #~ if os.path.exists('params') and os.path.exists('results1.txt') == True:
                #~ rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
                #~ corrparamsfile=CORRPARAMS_FILE, colname=col)
                #~ td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)
#~ 
                #~ dftf.plotandsavealltraces(td, fdir=file)
                #~ dftf.writepeakf_d(td, fdir=file)
        #~ except ValueError:
            #~ pass
#~ 
#~ 
#~ os.chdir('..')
#~ 
#~ # Generates bar and scatter plots for each roi.

    
dftf.plotandsavebargraph_poolrois('peakf_pooled.txt', K, fdir='.', ylim=2)
plt.figure()
dftf.plotandsavescatterplot_poolrois('peakf_pooled.txt', K, fdir='.', ylim=2)


        

