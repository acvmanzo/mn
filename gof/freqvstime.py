#This module contains functions used to generate a frequency versus time plot. First, run findphase1 and findphase2 to generate picklefiles in the phase_analysis/ifiles folder containing the list of times when a minimum occured (Mean1_dmin_i; a minimum is the same as the time when the cibarium is at its fullest, right before emptying). From this list, a series of points is generated in which there is a 1 for every frame when a minimum occurs and 0 otherwise. This list is then convolved with a window function (a list of ones of the length WINDOWSEC, specified below). What arises is a list of pump frequency per frame, which can then be plotted.

import glob
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import mn.dftf.dftf as dftf

#MOVIES = {'mov_20101130_200533': ['control', 45, 'k'], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 30, 'b'], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 15, 'r'], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -5, 'r'], 'mov_20110518_184849': ['112648 x dtrpa1 - 32', 0, 'r']}

DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'

MOVIES = {'mov_20110517_181356': ['control', 67, 'k', '(i) '], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 45, 'k', '(ii) '], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 20, '#B52634', '(iii) '], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -7, '#B52634', '(iv) ']}

#TIME = 14
WINDOWSEC = 1
IFILEFOL = '/home/andrea//Documents/lab/motor_neurons/gof/dtrpa1/pooled_112648_dtrpa1/sample_traces/phase_analysis/ifiles'
DATAFOL = '/home/andrea//Documents/lab/motor_neurons/gof/dtrpa1/pooled_112648_dtrpa1/sample_traces/data'

def loadpicklefile(picklefname):
    
    with open(picklefname, 'r') as f:
        unpicklefile = pickle.Unpickler(f)
        d = unpicklefile.load()
    return(d)


def min_idict():
    """Loads picklefile and returns a dictionary of this format: {movie: [list of values of times when pumps occur, fps], etc.}"""
    os.chdir(IFILEFOL)
    t = {}
    for movie in MOVIES.iterkeys():
        os.chdir(movie)
        print('Generating min_idict', movie)
        d = loadpicklefile('pickle_minmax')
        if movie == 'mov_20110518_195501':
            t[movie] = [[], 30]
        elif movie == 'mov_20110517_181356':
            t[movie] = [d['Mean1_dmin']['i'].tolist(), 60]
        else:
            t[movie] = [d['Mean1_dmin']['i'], 30]
        os.chdir('../')
    return(t)


def min_frames(dict, time):
    """'Dict' is a dictionary generated by min_idict() and time is the length of time to plot. f1dict is a dictionary listing each movie and the first frame used to plot the raw traces. Returns a dictionary of this format: {movie: [list of frames with a 1 if a minimum occured (and therefore a pump) and 0 if a pump did not occur, fps], etc.}"""
    
    cfdict = checkframes() # Loads dictionary of the start frames from the params and pdframes files.
    
    d = {}
    for k, val in dict.iteritems():
        
        diff = int(cfdict[k][0] - cfdict[k][1]) # Finds the difference between the two start frames.
        print(diff)
                
        v, fps = val
        print(k, v)
        framelen = time*fps
        vframes = np.zeros(2*framelen).tolist()
        for n in v:
            vframes.insert(n, 1)
       
        vkeep = vframes[diff:framelen+diff] # Takes the frames from the start of the plotted raw trace to the end of the time limit.
        d[k] = [vkeep, fps]
        print(k, 'diff', diff, 'vkeep', len(vkeep), 'vframes', len(vframes))
    return(d)


def checkframes():
    """Generates a dictionary with the f1 from the params file and the pdframes file for each movie."""
    
    d = {}
    for movie in MOVIES.iterkeys():
        os.chdir(DATAFOL)
        os.chdir(movie)
        rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
        corrparamsfile=CORRPARAMS_FILE, colname='Mean1')
        td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)
        
        os.chdir(IFILEFOL)
        os.chdir(movie)
        pd = {}
        with open('pdframes') as f:
             for l in f:
                pd[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
        
        d[movie] = (td['f1'], float(pd['f1']))
    print(d)    
    return(d)


def pumpsovertime(dict, windowsec):
    """'Dict' is a dictionary generated by min_frames() and windowsec is the length of the window (in sec) used for convolving. Returns a dictionary of this format: {movie: [xvalues, convolved values, condition, fps], etc.}"""
    

    
    d = {}
    for k, val in dict.iteritems():
        print('Calculating pumps over time', k)
        v, fps = val
        winlen = windowsec*fps
        wind = list(np.ones(winlen))
        
        # Convolves the list of frames with the window function; only reports frames for which there is complete overlap.
        v_conv = np.convolve(v, wind, 'valid')/windowsec
        #print(k, len(v), len(v_conv))
        # Returns x values for the convolved trace. Xmin is at half of the window length (in seconds), xmax is at xmin + the length of the convolved trace (in seconds) and the number of points is the same as the length of the convolved trace.
        xvals = np.linspace((float(winlen/2))/fps, float((winlen/2)+len(v_conv))/fps, len(v_conv))
        #print(winlen/2, len(xvals), xvals)
        #print(zip(xvals, v_conv)[:60])
        cond = MOVIES[k][0]
        d[k] = [xvals, v_conv, cond, fps]
    return(d)
    
        
        


