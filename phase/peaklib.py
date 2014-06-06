from __future__ import print_function

import os
import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mn.plot.genplotlib as genplotlib
import math
import shutil
import pickle
import sys
from mn.cmn.cmn import *
from mn.phase.findphaseargs import *

matplotlib.rc('savefig', dpi=300)

DROI = {'Mean1': [6, 1, 0, 6, 1, 0]}
ROIS = ['Mean1']
COLS = ['Mean1']


# Below are global variables that can be modified depending on the parameters I want to analyze.

# These are parameters that must be modified while finding the max/min points in graphs.
# [maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift]
# Positive trshift numbers bring the threshold closer to the max or min value
#DROI = {'Mean1': [6, 1, 0, 6, 1, 0], 'Mean2': [6, 1, 0, 6, 1, 0]}
#~ 
# Which points to compare and summary folder.
#COMPARE = ['Mean1_dmin', 'Mean2_dmax'] 
#PHASEPARFOLD = 'summary_ph_1min_2max/'

# The dictionary keys in the order of plotting.
#K = ['0% MC', '1.5% MC', '2% MC', '2.5% MC', '3% MC']
K = ['112648-GAL4', 'UAS-TNT', '112648 x TNT']


#---------------------------------------------------------------------------------------------------
#Below are global variables indicating dictionary keys and other values.
FS = 60 # sampling frequency
F1 = 'f1' # dictionary key for the first valid frame
F_END = 'f_end' # dictionary key for the last valid frame
CONDITION = 'condition' # dictionary key for the condition being tested
#ROIS = ['Mean1', 'Mean2']
#COLS= ['Mean1', 'Mean2']


# Below are global variables for plotting the raw movies.
WINDOW_LEN = 50 # window length for each section of the raw movie plot

#Below are global variables indicating filenames and folders.
FRAMES = 'pdframes'
RESULTS = 'results1.txt'
PEAKF = 'peakf_roi1.txt'
PICKLEFNAME = 'pickle_minmax'
#SUMMFOLD = PHASEPARFOLD+'summ/'
#SUMMFOLDFRAME = SUMMFOLD+'frame'
#SUMMFOLDTIME = SUMMFOLD+'time'
#SUMMFOLDPHASE = SUMMFOLD+'phase'
#PICKLEFOLD = SUMMFOLD+'picklefiles/'
ANALYSISFOLDPNG = 'phase_analysis/plots'
ANALYSISFOLDTXT = 'phase_analysis/ifiles'
TRACEFOLDER = 'phase_analysis/raw_movies'
MINMAXFOLDER = 'phase_analysis/minmax_movies'
ALTEREDPICKLEFOLD = 'phase_analysis/changed_picklefiles'
SUMMFILE = 'delta_summ'
MASTERSUMMFILE = 'mastersumm'
KEYLIST = 'keylist'

# Creates/relies on the following file structure:
#experiment/
    #data/
        #movie1/
            #pdframes
            #output from ImageJ scripts
            #params files from other scripts
    
    #phase_analysis/
        #changed_picklefiles/
            #movie/
                #~ picklefiles that have been manually changed
        #ifiles/
            #movie/
        #m11_inactive/
            #movie/ (contains ifiles)
        #m11_m12_inactive/
            #movie/ (contains ifiles)
        #minmax_movies/
            #~ traces for each movie showing min/max points as delta functions; both rois are 
            #~ plotted on the same graph for easy comparison
        #plots/ (contains raw traces of movies with min/max points plotted)
            #bad/ (contains plots where the initially determined min/max points are incorrect)
    #~ summary_ph_1min_2max/ (or whatever roi parameters were compared)
        #~ summ/
            #~ frame/
                #~ summary text files for each movie containing the deltaframe data.
            #~ time/
                #~ summary text files for each movie containing the deltaftime data.
            #~ phase/    
                #~ summary text files for each movie containing the phase data
        #~ delta_summ (summary text file with all calculated values)
        #~ deltaframe_summ.png (scatterplot of deltaframe)
        #~ deltaframe_summ_bar.png (bar graph of deltaframe)
        #~ deltatime_summ.png (scatterplot of deltatime)
        #~ deltatime_summ_bar.png (bar graph of deltatime)
        #~ deltaphase_r1.png (polar plot of phases)
        #~ deltaphasevsfreq.png (polar plot of phases where the radius is the pump frequency)
        #~ deltaphasevsfreq_avg.png (polar plot of average phase with the radius as avg frequency 
        #~ for each condition

        

# Below are functions for making directories and saving files.

    
def makepardir_ifiles():
    """Returns the experiment/ folder path if you are in a phase_analysis/ifiles/movie folder."""
    return(os.path.dirname(os.path.abspath('../../')))

def makepardir():
    """Returns the experiment/ folder path if you are in a phase_analysis/ folder."""
    return(os.path.dirname(os.path.abspath('.')))

def makesubdir(pardir, folder):
    """Generates a path for /experiment/folder/ and makes the resulting directory."""
    resdir = os.path.join(pardir, folder)
    makenewdir(resdir)
    return(resdir)

def makefilepath(pardir, folder, filen):
    """Generates a path for the file pardir/folder/filen and makes the pardir/folder directory."""
    
    resdir = os.path.join(pardir, folder)
    makenewdir(resdir)
    #filepath = '{0}/{1}'.format(resdir, filen)
    filepath = os.path.join(resdir, filen)
    #print(filepath)
    return(filepath)


def delfile(pardir, folder, filen):
    """Deletes the file pardir/folder/filen."""
    
    fn = makefilepath(pardir, folder, filen)
    #print(fn)
    if os.path.exists(fn) == True:
        os.remove(fn)

def delfilepath(path):
    if os.path.exists(path) == True:
        os.remove(path)

def savefigname(pardir, folder, suffix):
    """Saves the current figure into the folder 'pardir/folder' with the filename 'movie_suffix'. 
    """
    
    figname = makefigname(suffix)
    fullfold = os.path.join(pardir, folder)
    makenewdir(fullfold)
    figpath = os.path.join(fullfold, figname)
    plt.savefig(figpath)


def makefigname(suffix, dpath='.'):
    """Returns the string "movie_suffix' where 'movie' is the basename of the folder 'dpath' 
    and 'suffix' is the first argument. Should be run from inside a movie folder.
    
    For instance, if dpath is 'mov_20100817_172325' then genfigname('DFT') would 
    return the string 'mov_20100817_172325_DFT'.
    """ 
    
    moviename = (os.path.basename(os.path.abspath(dpath)))
    fullname = '{0}_{1}'.format(moviename, suffix)
    return(fullname)


def savesummgraph(fname, graphname):
    """Saves a summary graph with the name 'graphname' using the path of the summary file (fname) 
    the graph's info was taken from."""
    
    dir = os.path.dirname(fname)
    graph_path = os.path.join(dir, graphname)
    plt.savefig(graph_path)
    plt.close()



# Below are functions for loading data from files.

def load_frames(frames):
    """Loads the parameters from the file 'frames'; returns a dictionary."""

    fd={}
    with open(frames) as g:
        for l in g:
            fd[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
    for k in iter(fd):
        try:
            fd[k] = int(fd[k])
        except ValueError:
            pass
    return(fd)


def load_data(results, fd):
    """Loads the intensity data from the file 'results' (a mean intensity over frames file 
    generated by ImageJ) and returns a dictionary with the rois as keys."""
    
    data, index = load_results(results, fd)
    
    # Creates an 2D array where each row is the valid data for a specific ROI.
    traces = [data[:, index[col_name]] for col_name in COLS]
    
    dictdata = {}
    for col_name in COLS:
        dictdata[col_name] = []
        dictdata[col_name] = data[:, index[col_name]]
    
    return(dictdata)


def load_results(results, fd):
    """
    Returns a numpy array from 'results' file containing the mean ROI intensity for each frame 
    of an image sequence for 1+ ROIs. 'fd' is a dictionary containing the valid frames. Function returns 
    a dictionary containing the ROI names and the indices of the columns they refer to. This 
    function is meant to be used with a file generated by the ImageJ function "multimeasure", 
    usually with the ImageJ custom macro "automeasure.txt".
    """
    
    # Makes a dictionary matching column names to column indices.
    with open(results) as f:
        roi_cols = dict(((roi, ind) for ind, roi in enumerate(f.readline().split())))
           
    
    # Creates a numpy array containing all the data.
    raw = np.loadtxt(results, skiprows=1)
    
    # Creates a numpy array containing only the frames valid for analysis.
    start = fd[F1]
    end = fd[F_END]
    data = raw[start:end, 1:]
    
    return data, roi_cols
    #print(data, roi_cols)


def loadpicklefile(picklefname):
    
    with open(picklefname, 'r') as f:
        unpicklefile = pickle.Unpickler(f)
        d = unpicklefile.load()
    return(d)


def sl():
    """Works from inside phase_analysis/ifiles folder"""
    
    os.chdir(os.path.join(makepardir_data(), 'summary'))
    sl = glob.glob('sample_length_*')
    sl = int(sl[0].split('_')[2])
    return(sl)

# Below are functions for plotting and writing the traces and data for use in phase analysis.
def partition(x, n):
    """General function for splitting a 1D data set 'x' into lists with 'n' elements. The 
    output is an array of lists."""
    
    # Truncates the data set if it is not a multiple of n.
    trunc = x[:n*(x.shape[0]//n)]
    
    # Divides data set into multiple parts. (-1) means python calculates the requisite number of rows.  
    parts = trunc.reshape((-1, n))
    
    return(parts)

def pd_raw(raw):
    return(locals())
    
def pd_movie_raw(traces):
    """Finds the dft, cross-correlation spectrum, cross-correlation spectrum peak, and the phase  
    differences for all the time bins in one movie."""

    #data, index = load_results(results, fd)
    
    # Creates an 2D array where each row is the valid data for a specific ROI.
    #traces = [data[:, index[col_name]] for col_name in ('Mean1', 'Mean2')]
    
    # Creates a 3D array where the 3 dimensions refer to the ROI, # parts, and # elements in each part.
    parts = [partition(trace, WINDOW_LEN) for trace in traces]

    # Creates a list of tuples where each tuple contains a part of the trace from each ROI at 
    #the same time window.
    pairs = zip(*parts)
    
    # Runs the function pd (which does all the calculations) on each tuple.
    phase_diff_dict = [pd_raw(pair) for pair in pairs]
    
    return(phase_diff_dict)
    

def plot_raw_movie(pd_dict, fd, fdir='.'):
    """Plots the data in time bins for one movie. Run in the /data/movie/ folder."""
    
    movie = os.path.basename(os.path.abspath(fdir))
    
    if len(pd_dict) > 30:
        plt.figure(figsize=(8,20))
    else:
        plt.figure(figsize=(8,16))

    condition = fd[CONDITION]
    plt.suptitle('Raw traces for {0} \n {1}'.format(movie, condition), fontsize=18)
    
    
    for i, pdd in enumerate(pd_dict):       
        i_plotsize = (np.floor(len(pd_dict)/3)+1, 3, i+1)
        #print(i_plotsize)
        ax = plt.subplot(*i_plotsize)
        # Deletes axis labels and ticks.
        ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
        ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
        plt.plot(pdd['raw'][0])
        plt.plot(pdd['raw'][1])
        ymin, ymax = plt.ylim()
        plt.ylim(ymin-0.3*ymin, ymax+0.3*ymax)
        plt.draw()


def plotandsaverawmovie(tracefolder, fdir='.'):
    """Plots raw traces and saves the traces in the folder 'tracefolder'."""
    os.chdir(fdir)
    pardir = makepardir_data()
    movie = os.path.basename(os.path.abspath('.'))
    
    fd = load_frames(FRAMES)
    dict = load_data(RESULTS, fd)
    traces = np.array([dict['Mean1'], dict['Mean2']])
        
    pd_dict = pd_movie_raw(traces)
    
    plt.figure()
    plot_raw_movie(pd_dict, fd)
    rawn = makefilepath(pardir, tracefolder, movie+'_0raw')
    plt.savefig(rawn)
    plt.close()


def b_plotandsaverawmovies():
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        os.chdir(name)
        print(os.path.basename(name))
        try:
            plotandsaverawmovie(TRACEFOLDER)
        except IOError:
            continue

# Below are functions for generating plots for finding max/min points.


def findmaxormin(raw, surr, winlen, maxormin, trshift):
    """Raw is the raw trace.  Surr is the number of points to the right and left of the trace that will be compared with the central point. Winlen is the window length for convolution; set to 1 for no convolution. Max or min specifies whether the max or min points are identified. Trshift specifies the number of standard deviations to add/subtract to the mean when defining a threshold. Positive trshift values bring the thresshold closer to the max/min value. Default values are specified as global variables."""
    
    d = {}
    d['winlen'] = winlen
    d['surr'] = surr
    d['trshift'] = trshift
    
    
    # Sets the window length for the convolution.
    winlen = np.float(winlen)
    offset = int(np.floor(winlen/2))
    a = np.ones(winlen, dtype=np.float64)/winlen
    
    # Convolves the trace.
    convtr = np.convolve(raw, a, 'valid')
    #print(len(convtr))
    
    # Length of the region of the trace for comparison.           
    tracelen = len(convtr)-surr*2
    #print(tracelen)
    
    # Number of traces to compare + 1.
    col = 2*surr+1
    # Creates a triangle matrix of shape col x col.
    tri1 = np.tri(col)
    
    # Creates a transposed triangle matrix of shape col x col.
    tri2 = np.transpose(np.tri(col))
    
    # Creates a ones matrix.
    ones = np.ones((len(convtr)-2*col, col))
    
    # Creates a matrix composed of the two triangle matrices + ones matrix.
    tri12ones = np.vstack((tri1, ones, tri2))
    #print(np.shape(tri12ones))
    
    # Makes a matrix whose rows are the convolved trace.
    convmat = np.tile(convtr, col)
    convmat = convmat.reshape(col, len(convtr))
    convmat = np.transpose(convmat)
    #print(np.shape(convmat))
    
    # Multplies the convolved trace matrix with the transposed triangle matrix. Result is a matrix 
    #~ whose columns are the shifted traces, padded with zeros.
    ts_zeros = np.transpose(convmat*tri12ones)
    
    # Returns the coordinates of the elements which are non-zero.
    i_zeros = np.nonzero(ts_zeros)
    #print(np.shape(ts_zeros[i_zeros]))
    #print(col, tracelen)
    
    # Makes a matrix whose columns are the shifted traces without zeros.
    ts_full = np.reshape(ts_zeros[i_zeros], (col, tracelen))
    ts = np.delete(ts_full, np.floor(float(col)/2),0)
    
    # Makes a matrix whose columns are the region of the convolved trace to be used for comparison.
    trace = ts_full[np.floor(col/2)]
    tm = np.reshape(np.tile(trace, col-1), (col-1, tracelen))
    
    # Compares the values of the shifted and main traces.
    
    if maxormin == 'min':
        tt = ts > tm
    
    if maxormin == 'max':
        tt = ts < tm
        
    # Returns a 1_D array where it's 'True' only if every comparison is 'True'.
    tt_test = np.all(tt, 0)
      
    
    # Finds the indices of the nonzero values.
    i_tt = np.nonzero(tt_test)[0]
    # Finds the indices of the nonzero values with reference to the raw trace.
    i = i_tt + offset + surr
               
    # Finds the values.
    vals = raw[i]
    #print(vals)
    
    if maxormin == 'min':
    # Entry is 'True' if the values are less than the mean.
        z_vals = vals < np.mean(raw) - trshift*np.std(raw)
    
    if maxormin == 'max':
    # Entry is 'True' if the values are greater than the mean.
        z_vals = vals > np.mean(raw) + trshift*np.std(raw)
    
    # Finds the indices of the values where the amplitude is less (greater) than the mean.
    z_i = np.nonzero(z_vals)
    #print(z_i)
    
    # Selects only the indices where the values are less (greater) than the mean.
    i_meantr = i[z_i]
    
    d['i'] = i_meantr
    d['raw'] = raw
    d['ival'] = raw[i_meantr]
         
    return(d)
    


def maxminanalysis(rawdata, maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift):

    dmax = findmaxormin(rawdata, maxsurr, maxwinlen, 'max', maxtrshift)
    dmin = findmaxormin(rawdata, minsurr, minwinlen, 'min', mintrshift)
    return(dmax, dmin)


def plotminmax(dictmax, dictmin, color, scale, vshift):
    
    #raw = (dictmin['raw'])       
    raw = (dictmin['raw']-np.mean(dictmin['raw']))/scale + vshift
    imax = dictmax['i']
    imin = dictmin['i']
    maxwinlen = dictmax['winlen']
    maxsurr = dictmax['surr']
    minwinlen = dictmin['winlen']
    minsurr = dictmin['surr']
    
    maxlabel = 's{0}_w{1}_t{2}'.format(dictmax['surr'], dictmax['winlen'], dictmax['trshift'])
    minlabel = 's{0}_w{1}_t{2}'.format(dictmin['surr'], dictmin['winlen'], dictmin['trshift'])
    
    plt.plot(raw, color, label='raw')
    plt.scatter(imax, raw[imax], c='r', edgecolor='r', marker='o', s=8, label=maxlabel)
    plt.scatter(imin, raw[imin], c='m', edgecolor='m', marker='o', s=8, label=minlabel)
    xmin, xmax = plt.xlim()
    plt.xlim(-10, xmax)
    plt.legend(loc='best')
    

def writei(minmaxdict, fd, fold):
    # Run from a data/movie folder.
    #print(minmaxdict)
    
    pdframesfile = fold + 'pdframes'
    picklefile = fold + 'pickle_minmax'
    
    with open(pdframesfile, 'w') as f:
        for key, val in fd.iteritems():
            f.write(var_str(key, str(val)))
    
    for roi_minmax, dict in minmaxdict.iteritems():
        #print(dict)
        
        for key, val in dict.iteritems():
            
            fname = fold + roi_minmax + '_' + key
            
            with open(fname, 'w') as g:
                g.write(str(val))
    
    with open(picklefile, 'w') as h:
        picklefile = pickle.Pickler(h)
        picklefile.dump(minmaxdict)
    
    

def checkmaxmin(droi):
    
    """For a results file in a /data/movie/ folder, finds the min and max points for both rois, 
    plots the traces with the max/min points, and saves the plots along with the maxmin data in 
    the folder /experiment/ANALYSISFOLDPNG and /experiment/ANALYSISFOLDTXT.
    
    DROI refers to parameters for findmaxmin(). droi = [maxsurr, maxwinlen, maxtrshift, minsurr, 
    minwinlen, mintrshift]; positive trshift numbers bring the threshold closer to the max or min 
    value."""
   
    # Loads data.
    fd = load_frames(FRAMES)
    dictdata = load_data(RESULTS, fd)
    
    pardir = makepardir_data()
    movie = os.path.basename(os.path.abspath('.'))
    
    d = {}
    rois = droi.keys()
    
    # Finds the max and min points using the parameters specified in the list droi.
    for roi in rois:
        rawdata = dictdata[roi]
        maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift = droi[roi]
        
        dmax, dmin = maxminanalysis(rawdata, maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift)
        
        d[roi+'_dmax'] = dmax
        d[roi+'_dmin'] = dmin

    # Plots the raw traces with the max and min points indicated.
    for roi in rois:
        plt.figure(figsize=(14,10))
        plotminmax(d[roi+'_dmax'], d[roi+'_dmin'], 'b', 1, 0)
        
        figname = movie+'_'+roi
        plt.title('{0} \n {1} \n frames = {2}-{3} ({4} total)'.format(figname, fd['condition'], 
        fd['f1'], fd['f_end'], fd['f_end']-fd['f1']))
        
        figpath = makefilepath(pardir, ANALYSISFOLDPNG, figname)
        plt.savefig(figpath)
        plt.close()
    
    # Writes the min/max data into a file with the function writei.
    
    ifilefold = ANALYSISFOLDTXT + '/' + movie + '/'
    ipath = makesubdir(pardir, ifilefold)
    writei(d, fd, ipath)


def b_checkmaxmin(droi):
    
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        os.chdir(name)
        print(os.path.basename(name))
        try:
            checkmaxmin(droi)
        except IOError:
            continue       


# Below are functions for correcting the max/min values found automatically.

def checkmaxmin_manual(droi):
    """ Runs checkmaxmin, then saves the revised picklefile into the ALTEREDPICKLEFOLD. For use in 
    manual correction of the max/min values, with specific droi values. DROI refers to parameters for
    findmaxmin(). droi = [maxsurr, maxwinlen, maxtrshift, minsurr, 
    minwinlen, mintrshift]; positive trshift numbers bring the threshold closer to the max or min 
    value."""
    
    checkmaxmin(droi)
    
    pardir = makepardir_data()
    movie = os.path.basename(os.path.abspath('.'))
    
    oldpath = os.path.join(pardir, ANALYSISFOLDTXT, movie, PICKLEFNAME)
    print(oldpath)
    newfname = PICKLEFNAME
    newpath = makefilepath(pardir, ALTEREDPICKLEFOLD+'/'+movie, newfname)
    print(newpath)
    shutil.copy(oldpath, newpath)
    

def removepoints(picklefname, roi_minormax, iremove, printonly='yes'):
    """Removes points from the list of times at which max/min points occur in a trace. Used for 
    manual correction of max/min points.
    
    'picklefname' is the picklefile with the original list of max/min times
    'roi_minormax' specifies which roi to remove points from and is a key for the dictionary saved 
    in the picklefile (ex., Mean2_dmax)
    'iremove' is a list of numbers to be removed from the original list
    'printonly' = 'yes' or 'no'; if 'no', generates a dictionary with the new max/min points and 
    values; if 'yes', just prints out the max/min points without generating a new dictionary.
    """
    
    iremove.sort
    iremove.reverse
    
    d = loadpicklefile(picklefname)

    a = list(d[roi_minormax]['i'])
    b = list(d[roi_minormax]['ival'])
    bmean = np.mean(b)
    bdisp1 = ['{0:.2f}'.format(y) for y in b]
    
    # Prints out lists of the original peak times and values.
    print(a)
    print(bdisp1)
    print(len(a), len(b))
    
    if printonly == 'yes':
        print('Print only')
   
    if printonly == 'no':
        
        a_i = []
        for i in iremove:
            a_i.append(a.index(i))
        
        #print(a_i)
        a_i.sort()
        a_i.reverse()
        
        # Removes the numbers specified in i_remove and displays them and their values.
        for aii in a_i:
            m = [x.pop(aii) for x in [a, b]]
            print(m)
        # Prints the new list with the specified points removed.
        print(a)
        bdisp = ['{0:.2f}'.format(y) for y in b]
        print(bdisp)
        
        d[roi_minormax]['i'] = a
        d[roi_minormax]['ival'] = b
        
        return(d)

def removepoints_dict(picklefname, dictremove, printonly):
    """Similar to 'removepoints()' but instead of removing only one set of points from one trace, 
    it removes multiple sets of points from multiple traces. Used for manual correction of min/max 
    points.
    
    'picklefname' is the picklefile with the original list of max/min times
    'dictremove' is a dictionary where the keys are the rois_trace and the values are the points 
    to be removed (ex., 'Mean2_dmin': [125, 141, 154])
    'printonly' = 'yes' or 'no'; if 'no', generates a dictionary with the new max/min points and 
    values; if 'yes', just prints out the max/min points without generating a new dictionary.
    """
    
    with open(picklefname, 'r') as f:
        unpicklefile = pickle.Unpickler(f)
        d = unpicklefile.load()

    for roikey, vals in dictremove.iteritems():
        
        a = list(d[roikey]['i'])
        b = list(d[roikey]['ival'])
        print(roikey + '-before')
        print(a)
        print(b)
    
    if printonly == 'printonly':
        print('Print only')
        return()
   
    if printonly == 'save':
        
        for roikey, vals in dictremove.iteritems():
            
            a = list(d[roikey]['i'])
            b = list(d[roikey]['ival'])
            
            a_i = []
            for i in vals:
                a_i.append(a.index(i))
            
            #print(a_i)
            a_i.sort()
            a_i.reverse()
            print(roikey + '-after')
            print('Points to be deleted')
            for aii in a_i:
                m = [x.pop(aii) for x in [a, b]]
                print(m)
                
            
            print(a)
            print(b)
            d[roikey]['i'] = a
            d[roikey]['ival'] = b
            
        return(d)

def savepicklefile(dict, framesfile, oldpicklefilename, newpicklefilename):    
    #Rewrites new picklefile into /phase_analysis/ifiles/movie folder, saves old picklefile as 
    #picklefile.auto and copies new picklefile into picklefile.man. Also rewrite the ifiles with 
    #new picklefile data.
    
    fd = load_frames(FRAMES)
    fold = os.path.abspath('.') + '/'
    writei(dict, fd, fold)
    
    shutil.move(oldpicklefilename, oldpicklefilename+'.auto')
    
    with open(newpicklefilename, 'w') as h:
        picklefile = pickle.Pickler(h)
        picklefile.dump(dict)
    
    shutil.copy(newpicklefilename, newpicklefilename+'.manual')

def loadmaxmintimes(picklefname):
    """Run from /experiment/phase_analysis/ifiles/movie folder."""
    
    # Opens a pickle file to extract the dictionary data (dictionary is output of 'findmaxormin'.
    with open(picklefname, 'r') as f:
        unpicklefile = pickle.Unpickler(f)
        dict = unpicklefile.load()
        #print(dict)
    
    # The dictionary contains a list of times that each max or min occured for each roi. This generates lists of 1's and 0's where each 1 occurs during the frame that a max or min occurred in the raw data. COMPARE is a list of dictionary keys of the two lists of times being compared.
    
    a_i, b_i = [dict[x]['i'] for x in COMPARE] #Lists of frames that a max or min occured.
    #print(a, b)
    a = list(np.zeros(a_i[-1]))
    b = list(np.zeros(b_i[-1]))

    for x in a_i:
        x = int(x)
        a.insert(x, 1) #List of 1's and 0's.

    for x in b_i:
        x = int(x)
        b.insert(x, 1) #List of 1's and 0's.
    
    a.reverse()
    alast1 = len(a)-a.index(1)-1
    a.reverse()
    #plt.plot(a)
    #plt.scatter(alast1, a[alast1], c='r', marker='o')
    #plt.plot(a[:alast1+1])
    
    b.reverse()
    blast1 = len(a)-b.index(1)-1
    b.reverse()
    
    a = a[0:alast1]
    b = b[0:blast1]
    
    # Makes sure that the lists of 1's and 0's are the same length. If not, adds extra zeros to the end of the shorter trace to match the longer trace.
    try:
        assert len(a) == len(b)
        
    except AssertionError:
        if len(a) - len(b) > 0:
            #print('a larger')
            extra = np.zeros(len(a)-len(b))
            b.extend(extra)
            #print(b)
        
        if len(a) - len(b) < 0:
            #print('b larger')
            extra = np.zeros(len(b)-len(a))
            a.extend(extra)
            #print(a)
            
    traces = np.array([a, b])    
     
    return(traces)


def checkmaxmin_pickle(picklefname):
    """Use the parameters in the pickle file from a previous checkmaxmin occurrence to replot the 
    raw data with the max/min points highlighted. Run from a phase_analysis/ifiles/movie/ 
    folder. Also rewrites the ifile data. Used so that manual updates to the max/min points are 
    saved."""
   
    # Opens the pickle file to extract the dictionary data (dictionary is output of 'findmaxormin').
    with open(picklefname, 'r') as f:
        unpicklefile = pickle.Unpickler(f)
        d = unpicklefile.load()
    
    fd = load_frames(FRAMES)    
    pardir = makepardir_ifiles()
    movie = os.path.basename(os.path.abspath('.'))
    writei(d, fd, '.')
    
    # Plots the raw traces with the max and min points indicated.
    for roi in ROIS:
        plt.figure(figsize=(14,10))
        plotminmax(d[roi+'_dmax'], d[roi+'_dmin'], 'b', 1, 0)
        rawdata = d[roi+'_dmax']['raw']
        
        figname = movie+'_'+roi
        plt.title('{0} \n {1} \n frames = {2}-{3} ({4} total)'.format(figname, fd['condition'], 
        fd['f1'], fd['f_end'], fd['f_end']-fd['f1']))
        
        figpath = makefilepath(pardir, ANALYSISFOLDPNG, figname)
        plt.savefig(figpath)
        plt.close()


def b_checkmaxmin_pickle(picklefname):
    """Run from the phase_analysis/ifiles/ folder. Replots traces and resaves ifile data to 
    reflect updated picklefiles."""
    
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        os.chdir(name)
        print(os.path.basename(name))
        try:
            checkmaxmin_pickle(picklefname)
        except IOError:
            continue
            


#Below are functions for generating average frame delays, time delays, and phase differences for 
#~ each movie from the max/min data in the 
#phase_analysis/ifiles folder. 

def gendeltaframe(picklefname, compare):
    """ Run from an analysis/ifiles/movie folder with file picklefname. Returns list of times 
    between an event in the first entry in compare, and an event in the second entry in compare. 
    Computes for every event. Ex., compare = ['Mean1_dmin', 'Mean2_dmax'] 
    """

    dict = loadpicklefile(picklefname)
    
    a, b = [dict[x]['i'] for x in compare]
    
    delta = []
    for num in a:
        delta.extend(np.array(b)-num)
        
    return(delta)



def gdf_adj(picklefname, compare):
    """For each peak in trace 1, calculates the occurence of the peak in trace 2 that is next in 
    time. Generates a list of these numbers. Only finds delta frames for times in which both 
    muscles are pumping.
    """
    
    dict = loadpicklefile(picklefname)
    a, b = [dict[x]['i'] for x in compare]
    #~ print(a, b)
    
    adjfr = []
    for num in b:
        #~ For each number in b, generates a list of that number of the same length as a; compares 
        #~ this new list to a to find the first instance in a where the number > a, then subtracts 
        #~ the previous number from the number in b. If the number is bigger than 0, it is 
        #~ appended to the output list.
        
        
        c = np.tile(num, len(a))
        #~ print(c)
        #less = list(c < a)
        more = list(c > a)
        #~ print(more)
        try:
            aind = more.index(False)
            #~ print(aind)
            dfadj = num - a[aind-1]
            if dfadj >= 0:
                adjfr.append(num - a[aind-1])
        except ValueError:
            continue
            
    #~ print(np.mean(adjfr))
    return(adjfr)


def truncate_peaks(framelist, sample_length):
    
    sl_list = np.tile(sample_length, len(framelist))
    ttable = framelist < sl_list
    try:
        last_index = list(ttable).index(False)
        trunc_framelist = framelist[:last_index]
    
    except ValueError:
        print(ValueError)
        trunc_framelist = framelist
    
    return(list(trunc_framelist))


def gdf_adj_f2(picklefname, compare, sample_length):
    """For each peak in trace 1, calculates the occurence of the peak in trace 2 that is next in 
    time. Generates a list of these numbers. Only finds delta frames for times in which both 
    muscles are pumping.
    """
    
    dict = loadpicklefile(picklefname)
    afull, bfull = [dict[x]['i'] for x in compare]
    #print('afull', afull)
    #print('bfull', bfull)
    
    a = truncate_peaks(afull, sample_length)
    #print('a', a)
    b = truncate_peaks(bfull, sample_length)
    #print('b', b)
    
      
    adjfr = []
    for num in b:
        #~ For each number in b, generates a list of that number of the same length as a; compares 
        #~ this new list to a to find the first instance in a where the number > a, then subtracts 
        #~ the previous number from the number in b. If the number is bigger than 0, it is 
        #~ appended to the output list.
        
        
        c = np.tile(num, len(a))
        #~ print(c)
        #less = list(c < a)
        more = list(c > a)
        #~ print(more)
        try:
            aind = more.index(False)
            #~ print(aind)
            dfadj = num - a[aind-1]
            if dfadj >= 0:
                adjfr.append(num - a[aind-1])
        except ValueError:
            continue
            
    #~ print(np.mean(adjfr))
    return(adjfr)    
    
    
def gendeltatime(deltaframe):

    delta_time = [float(d)/FS for d in deltaframe]
    return(delta_time)

def findphase(time, freq):
    
    frac2pi = time * freq * 2 * np.pi
    phase = frac2pi%(2*np.pi)
    return(phase)

def gendeltaphase(deltaframe, freq):
    
    deltatime = gendeltatime(deltaframe)
    #~ frac2pi = [t*freq*2*np.pi for t in deltatime]
    #~ deltaphase = [x%(2*np.pi) for x in frac2pi]
    
    deltaphase = [findphase(t, freq) for t in deltatime]
    
    return(deltaphase)

def writedelta(deltaframe, freq, phaseparfold):
    """From phase_analysis/ifiles/movie folder."""
    
    deltatime = gendeltatime(deltaframe)
    deltaphase = gendeltaphase(deltaframe, freq)
    
    dt = ['{0:.3f}'.format(x) for x in deltatime]
    dp = ['{0:.3f}'.format(x) for x in deltaphase]
   
    
    movie = os.path.basename(os.path.abspath('.'))
    
    nameframe = movie+'_'+'frame'
    nametime = movie+'_'+'time'
    namephase = movie+'_'+'phase'
    
    pardir = makepardir_ifiles()
    
    summfold = phaseparfold+'summ/'
    summfoldframe = summfold+'frame'
    summfoldtime = summfold+'time'
    summfoldphase = summfold+'phase'

    
    framepath = makefilepath(pardir, summfoldframe, nameframe)
    timepath = makefilepath(pardir, summfoldtime, nametime)
    phasepath = makefilepath(pardir, summfoldphase, namephase)

    with open(framepath,'w') as f:
        f.write(str(deltaframe))

    with open(timepath, 'w') as f:
        f.write(str(dt))

    with open(phasepath, 'w') as f:
        f.write(str(dp))

   
def writeavgs(deltaframe, freq, cond, outfile):
    
    avgdf = np.mean(deltaframe)
    std_avgdf = np.std(deltaframe)
    avgdt = np.mean(gendeltatime(deltaframe))
    std_avgdt = np.std(gendeltatime(deltaframe))
    #~ avgdp = findphase(avgdt, freq)
    avgdp = pd_avg(gendeltaphase(deltaframe, freq))[0]
    
    movie = os.path.basename(os.path.abspath('.'))
    
    if os.path.isfile(outfile) != True:
        with open(outfile, 'w') as h:
            h.write('Movie,AvgDF,StDev(AvgDF),AvgDT,StdDev(AvgDT),AvgDP,PeakF,Condition\n')
    
    # Writes the average phase difference to a summary file.
    with open(outfile, 'a') as h:
        h.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(movie, avgdf, std_avgdf, avgdt,std_avgdt, avgdp, freq, cond))
  


def b_writedeltaavgs():
    """Run from phase_analysis/ifiles folder."""
    
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = sorted([os.path.abspath(name) for name in names])
    
    #~ Deletes old summary file.
    summfile = SUMMFILE
    pardir1 = makepardir_data()
    delfile(pardir1, PHASEPARFOLD, summfile)
       
    for name in names:
        os.chdir(name)
        print(name)
        try:
            fd = load_frames(PEAKF) 
        except IOError:
            print('IOError-no peakf file?')
            continue
        
        freq = float(fd['freq'])
        cond = fd['condition']
        try:
            deltaframe = gdf_adj(PICKLEFNAME, COMPARE)
            
            movie = os.path.basename(os.path.abspath('.'))
            pardir = makepardir_ifiles()
            
            #~ Writes average deltaframes, deltatimes, and deltaphases to the summfile.
            
            y = makefilepath(pardir, PHASEPARFOLD, summfile)
            writeavgs(deltaframe, freq, cond, y)
            
            #~ Writes the deltaframes, deltatimes, and deltaphses to files in the summary/summary 
            #~ folder.
            
            writedelta(deltaframe, freq)
        except IOError as e:
            if e.errno == 2:
                continue


def b_writedeltaavgs_f2(phaseparfold, compare):
    """Run from phase_analysis/ifiles folder."""
    
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = sorted([os.path.abspath(name) for name in names])
    
    #~ Deletes old summary file.
    summfile = SUMMFILE
    pardir1 = makepardir_data()
    delfile(pardir1, phaseparfold, summfile)
    
    #Defines sample length from file in summary folder.
    sample_length = sl() 
       
    for name in names:
        os.chdir(name)
        print(name)
        try:
            fd = load_frames(PEAKF) 
        except IOError:
            print('IOError-no peakf file?')
            continue
        
        freq = float(fd['freq'])
        cond = fd['condition']
        
        
        try:
            deltaframe = gdf_adj_f2(PICKLEFNAME, compare, sample_length)
            
            movie = os.path.basename(os.path.abspath('.'))
            pardir = makepardir_ifiles()
            
            #~ Writes average deltaframes, deltatimes, and deltaphases to the summfile.
            
            y = makefilepath(pardir, phaseparfold, summfile)
            writeavgs(deltaframe, freq, cond, y)
            
            #~ Writes the deltaframes, deltatimes, and deltaphses to files in the summary/summary 
            #~ folder.
            
            writedelta(deltaframe, freq, phaseparfold)
        
        except IOError as e:
            if e.errno == 2:
                continue
   
                
# Below are functions for producing plots of the data .

def plotdeltaframe(fname, k):
    d = genplotlib.gendict_phase(fname, 'deltaframe')
    md = genplotlib.genlist(d)
    
    n = []
    for i, v in d.iteritems():
        n.append(max(v))
    print(n)
    
    plt.figure()
    genplotlib.plotdata(d, md, k, 's', 'Delay (frames)', 'Frame delay', ymin=0, ylim=max(n)+5)
    plt.savefig('deltaframe_summ')
    
    plt.figure()
    genplotlib.plotdata(d, md, k, 'b', 'Delay (frames)', 'Frame delay', ymin=0, ylim=max(n)+5)
    plt.savefig('deltaframe_summ_bar')


def plotdeltatime(fname, k):
    d = genplotlib.gendict_phase(fname, 'deltatime')
    md = genplotlib.genlist(d)
    
    n = []
    for i, v in d.iteritems():
        n.append(max(v))
    print(n)
    
    plt.figure()
    genplotlib.plotdata(d, md, k, 's', 'Delay (seconds)', 'Time delay', ymin=0.05, ylim=(max(n)+0.1*max(n)))
    plt.savefig('deltatime_summ')
    
    plt.figure()
    genplotlib.plotdata(d, md, k, 'b', 'Delay (seconds)', 'Time delay', ymin=0.05, ylim=(max(n)+0.1*max(n)))
    plt.savefig('deltatime_summ_bar')
    

def plotdeltaphase(fname, k):
    d = genplotlib.gendict_phase(fname, 'deltaphase')
    print(d)
    
    plt.figure()
    genplotlib.plot_phaseplot(d, k, 'no', 'Phase')
    plt.savefig('deltaphase_r1')


def genavgphasefreqdict(phasefreqdict):
 
    ad = {}
    for cond, val in phasefreqdict.iteritems():
        phase, freq = zip(*val)
        avgphase = pd_avg(phase)[0]
        avgfreq = np.mean(freq)
        ad[cond] = (avgphase, avgfreq)
    return(ad)


def genavgphaselendict(phasefreqdict):
 
    ad = {}
    for cond, val in phasefreqdict.iteritems():
        phase, freq = zip(*val)
        avgphase = pd_avg(phase)[0]
        avglen = pd_avg(phase)[1]
        ad[cond] = (avgphase, avglen)
    return(ad)

def plotphasefreq(fname, K):
    """Plots and saves the phase vs. frequency plots; run from the 'summary' folder."""
    
    d = genplotlib.gendict_phase(fname, 'dp_freq')
    
    plt.figure()
    genplotlib.plot_phaseplot_lpf(d, K, 'no', 'Phase vs. freq')
    pname = 'deltaphasevsfreq'
    plt.savefig(pname)
    
    plt.figure()
    ad = genavgphasefreqdict(d)
    print(ad)
    genplotlib.plot_phaseplot_lpf(ad, K, 'no', 'Average phase vs. average freq', withn='no')
    aname = 'deltaphasevsfreq_avg'
    plt.savefig(aname)


def plotphaselen(fname, K):
    """Plots and saves the phase vs. length of phase vector; run from the 'summary' folder."""
    
    d = genplotlib.gendict_phase(fname, 'dp_freq')
    
    
    plt.figure()
    ad = genavgphaselendict(d)
    print(ad)
    genplotlib.plot_phaseplot_l(ad, K, 'no', 'Average phase', withn='no')
    aname = 'deltaphasevsphaselen_avg'
    plt.savefig(aname)


def plotphasenlpersec(fname, K):
    """Plots and saves the phase vs. nlpersec plots; run from the 'summary' folder."""
    
    d = genplotlib.gendict_phase(fname, 'dp_freq')
    
    plt.figure()
    genplotlib.plot_phaseplot_lpf(d, K, 'no', 'Phase vs. volume drunk')
    pname = 'deltaphasevsvol'
    plt.savefig(pname)
    
    plt.figure()
    ad = genavgphasefreqdict(d)
    print(ad)
    genplotlib.plot_phaseplot_lpf(ad, K, 'no', 'Average phase vs. average volume', withn='no')
    aname = 'deltaphasevsfreq_avg'
    plt.savefig(aname)


def plotallplots(fname, k):
    
    plotdeltaframe(fname, k)
    plotdeltatime(fname, k)
    plotdeltaphase(fname, k)
    plotphasefreq(fname, k)
    plotphaselen(fname, k)


# Below are functions for recopying picklefile and frequency data, and plotting the max/min times 
#~ for each movie.

def copyfreqdata(peakfname):
    """Run from summary folder."""
    
    with open(peakfname, 'r') as f:
        f.next()
        for l in f:
            movie, f, cond = map(str.strip, l.split(','))
            pardir = os.path.dirname(os.path.abspath('.'))
            pfile = makefilepath(pardir, ANALYSISFOLDTXT+'/'+movie, peakfname)
                        
            with open(pfile, 'w') as g:
                g.write(var_str('condition', cond))
                g.write(var_str('freq', str(f)))
            
def copypickledata(picklefname):
    """Run from the phase_analysis/ifiles folder."""
    
    pardir = makepardir_data()
    fold = PICKLEFOLD 
    
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        movie = os.path.basename(name)
        print(movie)
        pfile = name + '/' + picklefname
        newpfile = makefilepath(pardir, fold, movie+'_pickle_minmax')
        shutil.copy(pfile, newpfile)


def plotbothrois(picklefname):
    
    d = loadpicklefile(picklefname)
    rois = ['Mean1_dmax', 'Mean2_dmax']
    
    plt.figure()
    
    rawdata = d[rois[0]]['raw']
    plt.plot((rawdata/np.mean(rawdata))[400:460])
    
    rawdata2 = d[rois[1]]['raw'] 
    plt.plot((rawdata2/np.mean(rawdata2)-0.05)[400:460])
    

def plotminmaxtimes(minmaxfolder):
    
    traces = loadmaxmintimes(PICKLEFNAME)
    fd = load_frames(FRAMES)
    pd_dict = pd_movie_raw(traces)
    
    plot_raw_movie(pd_dict, fd)
    pardir = makepardir_ifiles()
    movie = os.path.basename(os.path.abspath('.'))
    
    plt.figure()
    plot_raw_movie(pd_dict, fd)
    rawn = makefilepath(pardir, minmaxfolder, movie+'_minmax')
    plt.savefig(rawn)
    plt.close()
   

def b_plotminmaxtimes():
    
    names = glob.iglob('*')
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        os.chdir(name)
        print(os.path.basename(name))
        try:
            plotminmaxtimes(MINMAXFOLDER)
        except IOError:
            continue

def copypicklefiles(picklefolder):
    # Start from folder containing the experiment folders.
    exptdir = os.getcwd()
    LIST = ['2010-1130_tnt', '2010-1213_tnt']

    for expt in LIST:

        os.chdir(expt)
        os.chdir('phase_analysis/ifiles')
                
        names = glob.iglob('*')
        # Absolute path rather than relative path allows changing of directories in fn_name.
        names = sorted([os.path.abspath(name) for name in names])
        pardir = os.path.dirname(os.path.abspath('../'))
        
        for name in names:
            movie = os.path.basename(name)
            os.chdir(name)
            fname = movie+'_pickle_minmax'
            fpath = picklefolder
            
            try:
                shutil.copy('pickle_minmax', fpath+fname)
            except IOError as e:
                if e.errno == 2:
                    continue
        
        os.chdir(exptdir)

# Below are functions for pooling data from several experiments (relies on making a master 
#~ summfile).

def makemastersumm(experiments, summfile):
    
    #~ Deletes old summary file.
    if os.path.exists(summfile) == True:
        os.remove(summfile)
    
    #~ Generates summfile paths.
    filelist = []
    for expt in experiments:
        f = makefilepath(expt, PHASEPARFOLD, SUMMFILE)
        filelist.append(f)
    
    #~ Defines new mastersumm file.
    with open('mastersumm', 'w') as f:
        f.write('Movie,AvgDF,StDev(AvgDF),AvgDT,StdDev(AvgDT),AvgDP,PeakF,Condition\n')
    
        for file in filelist:
            with open(file) as g:
                g.next()
                for l in g:
                    f.write(l)
    



def inactiveflies(experiments):
    
    
    for expt in experiments:
        os.chdir(expt)
        os.chdir('phase_analysis/')
        for folder in ['m11_inactive', 'm12_inactive', 'm11_m12_inactive']:
            try:
                os.chdir(folder)
                fs = os.listdir('.')
                n = len(fs)/3
            except OSError as e:
                if e.errno == 2:
                    continue
            

    
    


    



