import mn.dftf.dftf as dftf
import os
import matplotlib.pyplot as plt
import numpy as np
import operator
from mn.cmn.cmn import *
import matplotlib
import pickle

# Plots raw traces on one graph from the movies specified below.
# Run from the 'data' folder; in the 'data' folder are individual movie folders (similar to the experiment/data folders).

# Same values as in dftf.py, but only plotting roi1.
DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'
COLS= ['Mean1']
ROIS = ['roi1']

TYPE = 'raw' # Choose 'dft' or 'raw'

if TYPE == 'dft':
    PLOTNAME = 'dfttraces.png'
    YLABEL = 'Amplitude'
    XLABEL = 'Hz'
    YMIN = 0
    YLIM = 4
    
if TYPE == 'raw':
    #PLOTNAME = 'rawtraces.svg'
    PLOTNAME = 'rawtraces.png'
    YLABEL = 'Arbitrary Intensity'
    XLABEL = 'Seconds'    
    YMIN = -50
    #YLIM = 45
    YLIM = 220
    

FONTSIZE = 'x-small' # Font size for tick labels, axis labels.
FIGW = 5.5 # Figure width in inches
FIGH = 3.5 # Figure height in inches
FIGDPI = 300 # Figure dpi

BORDER = 'no'

YAXISTICKS = 2
TIME = 30 # Length of time the traces show.
XLIMHZ = 10



# Dictionary where the keys are the movie names and the values are the condition, the y offset of the trace (so that they aren't on top of each other), and the color the of the trace.

#MOVIES = {'mov_20101130_200135': ['112648-GAL4', 32.5+1, 'k'], 'mov_20110803_190537': ['UAS-TNT', 14+1, 'b'], 'mov_20101213_193258': ['112648 x TNT', 0, 'r']}

DFT_MOVIES = {'mov_20101130_200135': ['112648-GAL4', 3.1-0.25, 'k'], 'mov_20110803_190537': ['UAS-TNT', 1.8-0.25, 'b'], 'mov_20101213_193258': ['112648 x TNT', 0.25, 'r']}

MOVIES = {'mov_20110518_184507': ['184507', 150, 'k'], 'mov_20110518_185105': ['185105', 50, 'r'], 'mov_20110518_184217': ['184217', 100, 'y'], 'mov_20110518_184849': ['184849', 0, 'b']}


def oneplot(moviedict, toplotdict, figw, figh, figdpi, fontsz, border, ylabel, ylim, time, ymin):
    
    """Moviedict is the above dictionary of movies, toplotdict is a dictionary produced by toplot(), and other values are what's specified as global variables."""
    
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    #Plots data on one graph with parameters specified in the moviedict directory.
    for k, v in moviedict.iteritems():
        cond1, offset, color = v
        xvals = toplotdict[k][0]
        data = toplotdict[k][1] + offset
        condition = toplotdict[k][2]

        plt.plot(xvals, data, color, label=cond1)

    ax = plt.gca()

    ## Plots legend.
    plt.legend()
    ## Manipulates order of the legend entries.
    #handles, labels = ax.get_legend_handles_labels()
    #handles2 = handles[0], handles[2], handles[1], handles[3]
    #labels2 = labels[0], labels[2], labels[1], labels[3]
    #legend = ax.legend(handles2, labels2, bbox_to_anchor=(0, 0, 1, 1), transform=plt.gcf().transFigure)
    ## Changes legend font to fontsz.
    #ltext  = legend.get_texts()
    #plt.setp(ltext, fontsize=fontsz)
    ## Removes border around the legend.
    #legend.draw_frame(False)
    
  
    #Uncomment lines below to display without top and right borders.
    if border == 'no':
        for loc, spine in ax.spines.iteritems():
            if loc in ['left','bottom']:
                pass
            elif loc in ['right','top']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)
    
    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ## Removes tick labels and ticks from yaxis.
    ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies axis labels and axis tick label sizes.
    plt.xlabel(XLABEL, fontsize=fontsz)
    plt.ylabel(ylabel, fontsize=fontsz, labelpad=12)
    plt.xticks(fontsize=fontsz)
    plt.yticks(fontsize=fontsz)
    
    # Specifies axis limits.
    plt.axis( [0, time, ymin, ylim])
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    #fig1.subplots_adjust(top=0.8)
    #fig1.subplots_adjust(left=0.15)
    #fig1.subplots_adjust(right=0.95)
    

def gentoplot(time):
    """Generates a dictionary where the keys are movie names and the values are the raw trace for plotting. Time specifies the length of time in seconds of the plots shown."""
    
    toplot = {}

    # Generates a list of movie paths in the data folder.
    files = dftf.batch_s('.')   

    # Generates dft traces and plots for each roi in each movie.
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))

        for col in COLS:
             
            if os.path.exists('params') == True:
                rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
                corrparamsfile=CORRPARAMS_FILE, colname=col)
                td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)

                # Selects the area of the raw trace to plot.
                frames = time * td['fps']
                #print(frames)
                plottime = td['seltrace'][:frames]
                #print(len(plottime))
                ms = plottime-np.mean(plottime)
                xsec = np.linspace(0, len(plottime)/td['fps'], len(plottime))
                #print(xsec)
                condition = td['condition']
                toplot[td['moviename']] = [xsec, ms, condition]
                print(np.max(ms), np.min(ms))
                
    return(toplot)


def gentoplot_dft(xlimhz):
    
    toplot = {}

    # Generates a list of movie paths in the data folder.
    files = dftf.batch_s('.')   

    # Generates dft traces and plots for each roi in each movie.
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))

        for col in COLS:
             
            if os.path.exists('params') == True:
                rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
                corrparamsfile=CORRPARAMS_FILE, colname=col)
                td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)

                condition = td['condition']
                m = td['peakf']
                                
                xpoints = np.linspace(0, td['fps']/2, td['dftsize']/2)
                prop = xlimhz/(td['fps']/2)
                tracelen = np.rint(prop*len(td['dftnormtrunctrace']))
                
                toplot[td['moviename']] = [xpoints[:tracelen], td['dftnormtrunctrace'][:tracelen], condition]
    
    return(toplot)


if TYPE == 'dft':
    toplot = gentoplot_dft(XLIMHZ)
    #oneplot(MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, TIME)
    oneplot(DFT_MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, XLIMHZ, YMIN)

    # Saves the figures in plots/plots.
    plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, PLOTNAME)
    plt.savefig(figname, dpi=FIGDPI)

    # Saves a file showing the movies I used for the plot.
    fname = os.path.join(plotfolder, 'movies_used_for_dfttraces.txt')
    with open(fname, 'w') as f:
        for k, v in MOVIES.iteritems():
            f.write(k + ' ' + v[0] + '\n')

if TYPE == 'raw':
    toplot = gentoplot(TIME)
    oneplot(MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, TIME, YMIN)

    # Saves the figures in plots/plots.
    plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, PLOTNAME)
    plt.savefig(figname, dpi=FIGDPI)

    # Saves a file showing the movies I used for the plot and a pickle file with all the variables.
    fname = os.path.join(plotfolder, 'movies_used_for_rawtraces.txt')
    with open(fname, 'w') as f:
        for k, v in MOVIES.iteritems():
            f.write(k + ' ' + v[0] + '\n')
    
    picklename = os.path.join(plotfolder, 'picklefile')
    with open(picklename, 'w') as h:
        d = {}
        d['FONTSIZE'] = FONTSIZE
        d['FIGW'] = FIGW
        d['FIGH'] = FIGH
        d['FIGDPI'] = FIGDPI
        d['YAXISTICKS'] = YAXISTICKS
        d['TIME'] = TIME
        d['XLIMHZ'] = XLIMHZ
        d['PLOTNAME'] = PLOTNAME
        d['YLABEL'] = YLABEL
        d['XLABEL'] = XLABEL
        d['YMIN'] = YMIN
        d['YLIM'] = YLIM
        print(d)
        picklefile = pickle.Pickler(h)
        picklefile.dump(d)


