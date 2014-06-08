#! /usr/bin/env python

# Run from the 'data' folder.

import sys
import os
import mn.dftf.dftf as dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import glob

DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'



print('Plotting traces')    


# Specifies name of the columns from the imageJ results file and the names of the rois.
#COLS= ['Mean1', 'Mean2']
#ROIS = ['roi1', 'roi2']

COLS= ['Mean1']
ROIS = ['roi1']

#NFFT = 128
XLIM = 12
YLIM = 10
PADMULTIPLE=4
TIME = 12
TIMEOFFSET = 2
#EXPTS = [
#'/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1/2011-0527_112648_dtrpa1/data/'+
#'mov_20110527_151224', 
#'/home/andrea/Documents/lab/motor_neurons/lof/2010-1130_tnt/data/mov_20101130_201605',
#'/media/Data/gof/dtrpa1/2011-0518_112648_dtrpa1/data/mov_20110518_192012',
#'/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1/2011-0527_112648_dtrpa1/data/'+
#'mov_20110527_150743']

LABMTGFOLD = '/home/andrea/Documents/lab/labmtg/2011-0815_labmtg_files/specs'
FONTSIZE = 'x-large'

def plotcustomspec(td, nfft, time, xlim=30, ylim=10, padmultiple=1):
    frames = time * td['fps']
    frameoffset = TIMEOFFSET * td['fps']
    trace = td['seltrace'][frameoffset:]
    

    (Pxx, freqs, bins, im) = plt.specgram(trace, NFFT=nfft, Fs=td['fps'],
            detrend=mlab.detrend_mean, noverlap=nfft/2, pad_to=nfft*padmultiple,
            scale_by_freq=False)
    
    #plt.axvline(x=td['f1']/td['fps'], c='k')
    #plt.axvline(x=td['f2']/td['fps'], c='k')
    #plt.axvline(x=td['f_end']/td['fps'], c='k', ls='--')
    plt.title(td['condition'], fontsize=FONTSIZE)
    plt.xlabel('Time', fontsize=FONTSIZE)
    plt.ylabel('Hz', fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.xticks(fontsize=FONTSIZE)
    plt.axis( [0, xlim-TIMEOFFSET, 0, ylim])
    #plt.colorbar()
    plt.clim(vmin=-50, vmax=50)

def plotspecmovie(nfft, padmultiple):
    
    rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
    corrparamsfile=CORRPARAMS_FILE, colname='Mean1')
    td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)
    
    plotcustomspec(td, nfft=nfft, time=TIME, xlim=XLIM, ylim=YLIM, padmultiple=padmultiple)




def batch_plotspecmovie(nfft, padmultiple):

    # Generates a list of movie paths in the data folder.
    files = dftf.batch_s('.')   

    # Generates dft traces and plots for each roi in each movie.
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))

        if os.path.exists('params') == True and os.path.exists('results1.txt') == True:
            plotspecmovie(nfft, padmultiple)
            dftf.savetracesumm(str(nfft), moviefold = 'summary/spec_pad_' + str(nfft))
            plt.close()



def savetracefold(suffix, fold):
    """Saves the current figure into the summary folder with the filename 'movie_suffix'. 
    
    For instance, if you run savetracesumm(summ) in the folder
    '/home/andrea/Documents/lab/test2/data/mov_20100819_174601', then the figure is saved with
    the filename 'mov_20100819_174601_summ.png' in the folder
    '/home/andrea/Documents/lab/test2/summary'.
    """
    
    figname = dftf.genfigname(suffix)
    makenewdir(fold)
    respath = os.path.join(fold, figname)
    plt.savefig(respath)

def testspec():
    expts = glob.glob('*')
    for expt in expts:
        os.chdir(expt)
        print(expt)
        for pad in [1, 2, 4]:
            for nfft in [128, 256]:
                plotspecmovie(nfft, pad)
                dftf.savetracesumm(str(NFFT), moviefold = 'summary/spec_pad_' + str(NFFT))
                #savetracefold(str(nfft)+'pad'+str(pad), LABMTGFOLD)
                plt.close()
        os.chdir('../')

dataf = os.path.abspath('.')
for nfft in [128, 256]:
    batch_plotspecmovie(nfft, PADMULTIPLE)
    os.chdir(dataf)

