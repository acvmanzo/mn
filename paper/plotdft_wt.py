#! /usr/bin/env python

# This script plots sample dft plots, one for each movie.
# Run from the 'data' folder; in the 'data' folder are individual movie folders (similar to the experiment/data folders).

import sys
import os
import mn.dftf.dftf as dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt
import matplotlib as mpl

# Same values as in dftf.py
DFTSIZE=10000
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
CORRPARAMS_FILE = 'corrparams'
HZ_BOUND1 = 0.5
HZ_BOUND2 = 'end'
KEYLIST = 'keylist'

# Values for formatting graph.
FONTSIZE = 6.7 # Font size for tick labels, axis labels.
FIGW = 1.5 # Figure width in inches
FIGH = 0.38 # Figure height in inches
FIGDPI = 600
YLIM = 1.05
BORDER = 'no'
YLABEL = 'Normalized magnitude'
XAXISTICKS = 5
YAXISTICKS = 1
XLIMHZ = 10

TIMEOFFSET = 4
LINEWIDTH = 0.75

print('Plotting traces')    


# Specifies name of the columns from the imageJ results file and the names of the rois.
COLS= ['Mean1']
ROIS = ['roi1']


DFT_MOVIES = {'mov_20110830_152007': ['24 h/100 mM suc', 70, 'k'], 'mov_20110830_192926': ['10 h/100 mM suc', 45, 'k'], 'mov_20110901_182709' :['24 h/500 mM suc', 20, 'k'], 'mov_20110113_180524': ['500 mM suc + 2.5% MC', -1, 'k']}


def plottrace_paper(td, figw, figh, figdpi, fontsz, ylim, border, ylabel, xaxisticks, yaxisticks, xlimhz, color):
    """Plots the first half of the normalized and truncated dft trace; td is a dictionary generated using method TraceData.Processrawtrace."""
    
    m = td['peakf']
    
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    # Plots the dft.
    xpoints = np.linspace(0, td['fps']/2, td['dftsize']/2)
    print(len(xpoints))
    
    prop = xlimhz/(td['fps']/2)
    print(prop)
    tracelen = np.rint(prop*len(td['dftnormtrunctrace']))
    print(tracelen)
    
    plt.plot(xpoints[:tracelen], td['dftnormtrunctrace'][:tracelen], color, label='peak frequency = {0} Hz'.format(m), linewidth=1)
    
     #Plots legend and removes the border around it.
    #legend = plt.legend(numpoints = 1, loc='best')
    #legend.draw_frame(False)
    #ltext  = legend.get_texts() 
    #plt.setp(ltext, fontsize='small') 
    
    ax = plt.gca()
    
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
    #ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks)) 
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(xaxisticks)) 
    ## Removes tick labels and ticks from xaxis.
    #ax.axes.xaxis.set_major_locator(mpl.ticker.NullLocator())
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    fig1.subplots_adjust(bottom=0.3)
    fig1.subplots_adjust(left=0.05)
    fig1.subplots_adjust(right=0.95)
    fig1.subplots_adjust(top=0.95)
    
    
    
     #Specifies axis labels and axis tick label sizes.
    plt.xlabel('Hz', fontsize=fontsz)
    #plt.ylabel(ylabel, fontsize=fontsz, labelpad=12)
    plt.xticks(fontsize=fontsz)
    plt.yticks( [1], fontsize=fontsz)
    
    # Sets the limits.
    plt.axis( [0, xlimhz, 0, ylim])
    
    # Saves the figures in plots/plots.
    plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, td['moviename'] + '_dft_ticks_labels')
    plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
    plt.savefig(figname+'.png', dpi=FIGDPI, format='png')



mpl.rc('axes', linewidth=LINEWIDTH)
# Generates a list of movie paths in the data folder.
files = dftf.batch_s('.')   


def plotdft_paper(td, figw, figh, figdpi, fontsz, ylim, border, ylabel, xaxisticks, yaxisticks, xlimhz, color, lw):
    """Plots the first half of the normalized and truncated dft trace; td is a dictionary generated using method TraceData.Processrawtrace."""
    
    m = td['peakf']
    
    
    #fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    
    # Plots the dft.
    xpoints = np.linspace(0, td['fps']/2, td['dftsize']/2)
    print(len(xpoints))
    
    prop = xlimhz/(td['fps']/2)
    print(prop)
    tracelen = np.rint(prop*len(td['dftnormtrunctrace']))
    print(tracelen)
    
    plt.plot(xpoints[:tracelen], td['dftnormtrunctrace'][:tracelen], color, label='peak frequency = {0} Hz'.format(m), linewidth=lw)
    
     #Plots legend and removes the border around it.
    #legend = plt.legend(numpoints = 1, loc='best')
    #legend.draw_frame(False)
    #ltext  = legend.get_texts() 
    #plt.setp(ltext, fontsize='small') 
    
    ax = plt.gca()
    
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
    
    ## Removes tick marks from both x axes:
    #for tick in ax.xaxis.get_major_ticks():
        #tick.tick1On = False
        #tick.tick2On = False
    
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(yaxisticks)) 
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(xaxisticks)) 
    ## Removes tick labels and ticks from xaxis.
    #ax.axes.xaxis.set_major_locator(mpl.ticker.NullLocator())
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    fig1.subplots_adjust(bottom=0.38)
    fig1.subplots_adjust(left=0.07)
    fig1.subplots_adjust(right=0.95)
    fig1.subplots_adjust(top=0.9)
    
    
    
     #Specifies axis labels and axis tick label sizes.
    #plt.xlabel('Pump frequency (Hz)', fontproperties=fontv, labelpad=2)
    #plt.ylabel(ylabel, fontproperties=fontv, labelpad=4)
    plt.xticks(fontproperties=fontv)
    plt.yticks( [1], fontproperties=fontv)
    
    # Sets the limits.
    plt.axis( [0, xlimhz, 0, ylim])
    
    # Saves the figures in plots/plots.
    plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, td['moviename'] + '_dft_ticks_labels')
    plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
    plt.savefig(figname+'.png', dpi=FIGDPI, format='png')



mpl.rc('axes', linewidth=LINEWIDTH)
# Generates a list of movie paths in the data folder.
files = dftf.batch_s('.')   


# Generates dft traces and plots for each roi in each movie.
for movie, val in DFT_MOVIES.iteritems():
    os.chdir(movie)
    print(os.path.basename(movie))

    for col in COLS:
         
        if os.path.exists('params') == True:
            rawtracedata = dftf.TraceData(fname=RESULTS_FILE, paramsfile=PARAMS_FILE, 
            corrparamsfile=CORRPARAMS_FILE, colname=col)
            td = rawtracedata.Processrawtrace(DFTSIZE, HZ_BOUND1, HZ_BOUND2)
            
            condition, offset, color = val

            plotdft_paper(td, FIGW, FIGH, FIGDPI, FONTSIZE, YLIM, BORDER, YLABEL, XAXISTICKS, YAXISTICKS, XLIMHZ, color, LINEWIDTH)
    
    os.chdir('../')

        

