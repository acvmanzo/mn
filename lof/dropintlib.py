# Plots two ROIs.

import sys
import os
import mn.dftf.dftf as dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt

RESULTS_FILE = 'results1.txt'


def load_results(results):
    """
    Returns a numpy array from 'results' file containing the mean ROI intensity for each frame 
    of an image sequence for 1+ ROIs. Function returns 
    a dictionary containing the ROI names and the indices of the columns they refer to. This 
    function is meant to be used with a file generated by the ImageJ function "multimeasure", 
    usually with the ImageJ custom macro "automeasure.txt".
    """
    
    # Makes a dictionary matching column names to column indices.
    with open(results) as f:
        roi_cols = dict(((roi, ind+1) for ind, roi in enumerate(f.readline().split())))
           
    # Creates a numpy array containing all the data.
    raw = np.loadtxt(results, skiprows=1)
    
    return np.transpose(raw), roi_cols


def genbubintparams(fname, datafol):
    """Make params file for calculating area."""
    
    d = open(fname)
    d.next()
        
    for l in d:
        newline = []
        
        for x in l.split(','):
            newline.append(x.rstrip('.fmf\n'))
        
              
        name, start, end, starts, ends, retracts, condition = newline[0:7]
        print(name)
        paramsfile = os.path.join('data_intensity', name, 'params')
        if os.path.exists(paramsfile) == True:
            print('Removing old params file')
            os.remove(paramsfile)
   
        #makenewdir(os.path.join(datafol, name))
        try:
            f = open(os.path.join(datafol, name, 'params'), 'w')
            f.write(var_str('name', name))
            f.write(var_str('start', start))
            f.write(var_str('end', end))
            f.write(var_str('startshort', starts))
            f.write(var_str('endshort', ends))
            f.write(var_str('retracts', retracts))
            f.write(var_str('condition', condition))
        except IOError:
            continue

def load_params():
    
    td = {}
    with open('params') as h:
        for l in h:
            td[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
    return(td)

def plotinttrace():
    
    td = load_params()
    x, roi_cols = load_results(RESULTS_FILE)
    start = int(td['startshort'])
    end = int(td['endshort'])
    #print(x, roi_cols)
    #xvals = x[0]
    #print(td['startshort'
    #print(xvals)
    plt.figure()
    plt.plot(x[0][start:end], x[roi_cols['Mean1']][start:end], label='cibarium')
    plt.plot(x[0][start:end], x[roi_cols['Mean2']][start:end], label='labellum')
    plt.xlim( (0, 40) )
    plt.title(td['condition'])
    plt.legend()

def saveinttrace(summpath, movie):
    plt.savefig(os.path.join(summpath, movie+'_intplot.png'))
    plt.close()


if __name__ == '__main__': 
    pardir = os.getcwd()
    summdir = makenewdir('summary_area_intensity')


    print('Generating params')
    genbubintparams('movies_dye_prob_end_int_notes.txt', 'data_intensity')
    os.chdir('data_intensity')
    print('Plotting traces')    


    files = dftf.batch_s('.')   

    # Generates traces and plots for each roi in each movie.
    for file in files:
        os.chdir(file)
        movie = os.path.basename(file)
        print(movie)
        plotinttrace()
        summpath = os.path.join(pardir, summdir)
        saveinttrace(summpath, movie)

        
    


        
