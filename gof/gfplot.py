#! /usr/bin/env python

# Contains functions useful for plotting data from gain of function experiments.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import glob
import mn.plot.genplotlib as genplotlib
import mn.dftf.dftf as dftf
import mn.cmn.cmn as cmn
import mn.phase.peaklib as peaklib


matplotlib.rc('savefig', dpi=150)
matplotlib.rc('figure.subplot', left=0.1, right=0.95, hspace=0.4, wspace=0.25)
matplotlib.rc('figure', figsize=(12,8))

ANALYSISFOLDPNG = 'phase_analysis/plots'
ANALYSISFOLDTXT = 'phase_analysis/ifiles'
PARAMSFILE = 'gofparams'

def msub(trace):
    """Returns a mean subtracted trace."""
    
    return(trace - np.mean(trace))
    

class GFTraceData:
    """This class provides functions for processing a numpy array generated by ImageJ's custom 
    automeasure macro.
    
    The numpy array is a list of numbers representing the mean intensity of an ROI; this data is 
    saved in the file 'fname'. 'Paramsfile' is the file containing parameters needed for further 
    analyzing the data, and is generated by the python code 'genparamslib.genpgf'. The first column of 
    'paramsfile' contains the variable names and the second column contains the values.'Paramsfile' 
    requires the following parameters to be specified:
        f1: start frame (used to select the frames for plotting the trace)
        f2 = f_end: f1 to f_end specifies frames that are valid for plotting traces (i.e., little movement)
        fps: sampling frequency of the movie being analyzed
    """
    
    def __init__(self, fname, paramsfile, f2):
        self.fname = fname
        self.paramsfile = paramsfile
        self.f2 = f2
        
 
    def Processrawtrace(self):
        """This method returns a dictionary containing the raw mean intensity trace as well as 
        processed traces.
        
        'rawtrace' refers to the trace that is loaded from the ImageJ results file.
        'msubtrace' refers to the 'trace' after it has been mean-subtracted.
        """
        
        tracedict = {}
        
        for l in open(self.paramsfile):
            tracedict[l.split(',')[0]] = (l.split(',')[1])
        
        tracedict['f1'] = int(tracedict['f1'])
        tracedict['f2'] = self.f2
        tracedict['fps'] = int(tracedict['fps'])
        tracedict['f_end'] = int(tracedict['f_end'])
        tracedict['flypic'] = dftf.getflypic('roi')  
        tracedict['rawtrace'] = dftf.loadresultsfile(self.fname, 'Mean1')
        tracedict['msubtrace'] = msub(tracedict['rawtrace'][0:tracedict['f2']])
                     
        return tracedict


def plotmsubtrace(td, subplotn=111):
    """Plots the mean-subtracted trace."""
    
    ax = plt.subplot(subplotn)
    plt.plot(td['msubtrace'])
    plt.ylim(-20, 20)
    movie = dftf.genfigname('')
    plt.title('{0}'.format(movie))
    ### Changes tick interval to be 250.
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(18))


#def plotflypic(td, subplotn=111):
    #ax = plt.subplot(subplotn)
    #### Removes tick marks and labels.
    #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    #ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
    #plt.imshow(np.rot90(np.rot90(td['flypic'])))
    #movie = dftf.genfigname('')
    #plt.title('{0}'.format(movie))

    

def plotalltraces(td):
    """Plots the mean subtracted trace as well as the picture of the fly."""
    
    plotmsubtrace(td, 211)
    dftf.plotflypic(td, 212)


def makenewdir(newdir):
    """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""
    
    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.errno == 17:
            pass  


def plotandsavealltraces(fdir='.'):
    os.chdir(fdir)
    if os.path.exists('gofparams') == True:
        gftracedata = GFTraceData(fname='results1.txt', paramsfile='gofparams', f2=900)
        td = gftracedata.Processrawtrace()
        if os.path.isfile('gofparams') == True:
            plotalltraces(td)
            dftf.savetracesumm('plot', moviefold='/summary/rawtraces/')
            plt.close()
        
        
def batch(f, fdir='.'):
    """Carries out the function 'fn_name' recursively on all files in the directory 'fdir'.
    """
    
    os.chdir(fdir)
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = sorted([os.path.abspath(name) for name in names])
    for name in names:
        print os.path.basename(name)
        f(name)


def b_plotandsavealltraces():
    batch(plotandsavealltraces)


# The following functions are used for analyzing the data.


def gendictgf(fname):
    """Generates two dictionaries from the data in fname, with the conditions as keywords.
    
    fname is of the following format:
    Movie, F1, Fend, Condition, cib open, pumps over first 900 frames, comments
    
    F1 and Fend are the frames that are valid for pumping analysis (in this case, all of them)
    
    Generates one dictionary with the cibarium state data and another dictionary with the pump 
    number data.
    """
    
    cibopen = {}
    npumps = {}
    
    f = open(fname)
    f.next()
    
    for l in f:
        movie, f1, f2, cond, cib, npump = l.split(',')[0:6]
        condition = cond
        #condition = c.strip('')
        
        if condition not in cibopen:
            cibopen[condition] = []
        
        if condition not in npumps:
            npumps[condition] = []
        
        if npump != 'x' and npump != '':
            try:
                npumps[condition].append(float(npump))
            except ValueError:
                continue
               
        if cib != 'x' and cib != '':
            try:
                cibopen[condition].append(float(cib))
            except ValueError:
                continue
       
    return(cibopen, npumps)


#The following functions are for analyzing the percent of flies with open cibariums.

   

def genpercent_noci(dict, label='data'):
    """For use with binary data: generates a new dictionary in which the keywords are conditions 
    and the values are lists with the percent, the sample number, and the label 'label'. Use with 
    genplotlib.plotdata()
    """
    
    percent_dict = {}
    
    for condition, value in dict.iteritems():
        sum = np.sum(value)
        percent = (np.sum(value)/len(value))*100
        
        #stdev = np.std(value)
        n = len(value)
        #sterr = stdev/np.sqrt(n)
        
        if condition not in percent_dict:
            percent_dict[condition] = []
        
        percent_dict[condition].append(percent)
        percent_dict[condition].append(0)
        percent_dict[condition].append(0)
        percent_dict[condition].append(n)
        percent_dict[condition].append(label)
        
    return(percent_dict)


def genpercent_ci(fname):
    """Here, fname is the file generated by the matlab script binomial_ci.m; contains the limits 
    of the confidence interval. Use the output of the matlab script."""
    
    d = {}
    
    with open(fname) as f:
        f.next()
        for l in f:
            condition, prop, lb, ub, nsuccess, n = l.strip('\n').split(',')
            prop, lb, ub = map(float, [prop, lb, ub])
            
            cond = condition.lstrip('g')
            cond = cond.replace('GAL4', '-GAL4 - ')
            cond = cond.replace('UAS', 'UAS-')
            cond = cond.replace('dtrpa1', 'dtrpa1 - ')
            
            lci = prop - lb
            uci = ub - prop
            
            prop, lci, uci = map(str, [prop, lci, uci])
                        
            d[cond] = []
            d[cond].extend([prop, lci, uci, nsuccess, n])
    
    return(d)


def genpercent_m(dict, label='data'):
    """For use with binary data: generates a new dictionary in which the keywords are conditions 
    and the values are lists with the number of successes and the total.
    
    Used primarily for data stating whether the cibarium is open. Use output as argument for 
    cwritedata_matlab function.
    """
    
    newdict = {}
    
    for condition, value in dict.iteritems():
        sum = np.sum(value)
        n = len(value)
        
        if condition not in newdict:
            newdict[condition] = []
        
        newdict[condition].append(sum)
        newdict[condition].append(n)
    
    return(newdict)
    

def writedata_matlab(cibpercentdictm):
    """Generates a file listing the values for whether the cibarium is open for use in 
    statistical analysis in matlab."""
    
    expt = os.path.basename(os.path.abspath('.'))
    with open(expt + '_cibdata_m.txt', 'w') as f:
        #f.write('Condition \t cibopen \t total \n')
        for condition, vals in cibpercentdictm.iteritems():
            condition = condition.replace(' - ', '')
            condition = condition.replace('-', '')
            sum, n = map(str, vals)
            #f.write('g' + condition + '_cibopen=' + sum + '\n')
            #f.write('g' + condition + '_total=' + n + '\n')
            #f.write(condition + '\t' + sum + '\t' + n + '\n')
            f.write('g' + condition + '\t' + sum + '\t' + n + '\n')
            

def plotcibdata_noci(keyfile='keylist', fname='cib_pumps.txt', type='b'):
    """Fname is the file with the original cibarium and pump count data."""
    
    cib, npumps = gendictgf(fname)
    cibdict = genpercent_noci(cib)
    #keylist = sorted(pcib.keys())
    keylist = cmn.load_keys(keyfile)

    fig1 = genplotlib.plotdata(cib, cibdict, keylist, type, ylabel='%', ftitle='Percentage of flies with open' + ' cibariums', ylim=100, ymin=-2)
    fig1.subplots_adjust(bottom=0.45)


def plotcibdata_ci(fname, gname, keyfile='keylist', type='b'):
    
    cibpoints, pumps = gendictgf(fname)
    cibpercent = genpercent_ci(gname)
    keylist = cmn.load_keys(keyfile)
    
    fig1 = genplotlib.plotdata_ci(cibpoints, cibpercent, keylist, type, '%', ftitle='Percentage of flies with open' + ' cibariums', ylim=100, ymin=-2)
    fig1.subplots_adjust(bottom=0.45)
    

    
def plotpumpdata(keyfile='keylist', fname='cib_pumps.txt', type='b', ylim=40):
    
    cib, pumps = gendictgf(fname)
    mpumps = genplotlib.genlist(pumps)
    #keylist = sorted(mpumps.keys())
    keylist = cmn.load_keys(keyfile)
    
    fig1 = genplotlib.plotdata(pumps, mpumps, keylist, type, ylabel='# of pumps', ftitle = 'Number of ' 
    + 'pumps over 30 seconds', ylim=ylim, ymin=-2)
    fig1.subplots_adjust(bottom=0.45)


def plotandsavegof(keyfile='keylist', fname='cib_pumps.txt', ylimpump=40):
    
    for type in ['b', 's']:

        plotcibdata_noci(keyfile, fname, type)
        plt.savefig('cibdata_' + type)
        plt.close()

        plotpumpdata(keyfile, fname, type, ylimpump)
        plt.savefig('pumpdata_' + type)
        plt.close()


def plotandsavegof_ci(fname, gname, keyfile='keylist'):
    
    for type in ['b', 's']:

        plotcibdata_ci(fname, gname, keyfile, type)
        plt.savefig('cibdata_ci_' + type)
        plt.close()

        plotpumpdata(keyfile, fname, type)
        plt.savefig('pumpdata_' + type)
        plt.close()


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


def loadresultsfile(fname, colname):
    """Returns a numpy array from data in the ImageJ-generated file 'fname', which is a text file 
    containing the Mean ROI intensity for each frame of an image sequence.
    
    This function is meant to be used with a file generated by the ImageJ function "multimeasure", 
    usually with the ImageJ custom macro "automeasure.txt".
    """
    
    f = open(fname)
    a = f.readline().split()
    f.close()
    b = []
    #Specifically imports the data under the "Mean1" column.
    for x in a: 
        b.append(x.find(colname))
    col = b.index(0) + 1
    return(np.loadtxt(fname, skiprows=1, usecols=(col,)))
    

def checkmaxmin(droi):
    
    """For a results file in a /data/movie/ folder, finds the min and max points for both rois, 
    plots the traces with the max/min points, and saves the plots along with the maxmin data in 
    the folder /experiment/ANALYSISFOLDPNG and /experiment/ANALYSISFOLDTXT.
    
    DROI refers to parameters for findmaxmin(). droi = [maxsurr, maxwinlen, maxtrshift, minsurr, 
    minwinlen, mintrshift]; positive trshift numbers bring the threshold closer to the max or min 
    value."""
   
    # Loads data.
    fd = load_frames('gofparams')
    rawdata = loadresultsfile('results1.txt', 'Mean1')
    
    pardir = cmn.makepardir_data()
    movie = os.path.basename(os.path.abspath('.'))
    
    d = {}
    rois = droi.keys()
    
    # Finds the max and min points using the parameters specified in the list droi.
    for roi in rois:

        maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift = droi[roi]
        
        dmax, dmin = peaklib.maxminanalysis(rawdata, maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift)
        
        d[roi+'_dmax'] = dmax
        d[roi+'_dmin'] = dmin

    # Plots the raw traces with the max and min points indicated.
    for roi in rois:
        plt.figure(figsize=(14,10))
        peaklib.plotminmax(d[roi+'_dmax'], d[roi+'_dmin'], 'b', 1, 0)
        
        figname = movie+'_'+roi
        plt.title('{0} \n {1} \n frames = {2}-{3} ({4} total)'.format(figname, fd['condition'], 
        fd['f1'], fd['f_end'], fd['f_end']-fd['f1']))
        
        figpath = peaklib.makefilepath(pardir, ANALYSISFOLDPNG, figname)
        plt.savefig(figpath)
        plt.close()
    
    # Writes the min/max data into a file with the function writei.
    
    ifilefold = ANALYSISFOLDTXT + '/' + movie + '/'
    ipath = peaklib.makesubdir(pardir, ifilefold)
    peaklib.writei(d, fd, ipath)


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
