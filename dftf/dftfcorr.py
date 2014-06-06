#! /usr/bin/env python

from mn.dftf.dftf import *

#This script is for implementing manual corrections to the dft results. Sometimes the program 
#picks out the wrong peak in the DFT, and this script lets me manually set the boundaries over which the 
#program finds the peak. 

# Vary these global variables to find the ones that work.
HZ_BOUND1 = 2
HZ_BOUND2 = 'end'
COLNAME = 'Mean2'

CORRPARAMS_FILE = 'corrparams'

rawtracedata = TraceData(fname='results1.txt', paramsfile='params', corrparamsfile=CORRPARAMS_FILE, 
colname=COLNAME)
td = rawtracedata.Processrawtrace(10000, HZ_BOUND1, HZ_BOUND2)
plotalltraces(td)


#Once sufficient values have been found, uncomment the next three lines.

makenewdir('../../summary/corrections')

#Writes a corrparams file, which is used to override the default values for HZ_BOUND1 and 2.
if os.path.exists(CORRPARAMS_FILE) == True:
    os.remove(CORRPARAMS_FILE)
    
writecorrparams(td)

# Plots and saves the traces to summaries/corrections as well as to the normal folders
plotandsaveallcorrtraces(td)

#Writes the corrected peakf to a file in summaries/corrections.
writecorrpeakf_d(td)


