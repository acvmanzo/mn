#! /usr/bin/env python

# 
#Run from the 'data_intensity' folder; in this folder are individual movie folders (similar to 
#the experiment/data folders).

import sys
import os
import mn.dftf.dftf as dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt
import matplotlib 
import mn.lof.dropintlib as dil


# Same values as in dftf.py
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'

# Values for formatting graph.
FONTSIZE = 6.7 # Font size for tick labels, axis labels.
FIGW = 1.5 # Figure width in inches
FIGH = 1.5 # Figure height in inches
FIGDPI = 600

#XLIM = 0.65
BORDER = 'no'
YLABEL = 'Arbitrary intensity'
XLABEL = 'Time (s)'
YAXISTICKS = 1
XAXISTICKS = 4
LINEWIDTH = 0.75
LABELS = 'yes'
FS = 60

print('Plotting traces')    


MOVIES = {'mov_20110313_181051': ['MN11 x TNT', 0.6, 'k', '(i) '], 
'mov_20110313_192534': ['MN11-GAL4', 0.4, 'k', '(ii) '], 
'mov_20110313_195959': ['UAS-TNT', 0.4, 'k', '(iii) '], 
'mov_20110316_195256': ['UAS-TNT', 0.4, 'k', '(iii) ']}


def plottrace_paper(moviedict, figw, figh, figdpi, fontsz, border, xlabel, ylabel, yaxisticks, 
        xaxisticks, labels, lw, fs):
    """Plots the first half of the normalized and truncated dft trace; td is a dictionary 
    generated using method TraceData.Processrawtrace."""
    
    for movie, val in moviedict.iteritems():
        os.chdir(movie)
        condition, xlim, color, inum = val
        
        fontv = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
        fontv.set_size(fontsz)
        
        print(movie)
        td = dil.load_params()
        x, roi_cols = dil.load_results(RESULTS_FILE)
        start = int(td['startshort'])
        end = int(td['endshort'])
        
        
        fig1 = plt.figure(figsize=(figw*xlim/0.6, figh), dpi=figdpi, facecolor='w', edgecolor='k')
        
        xlen = len(x[roi_cols['Mean1']][start:end])
        #print(xlen)
        xvals = np.arange(0, float(xlen)/fs, 1/float(fs))
        #print(xvals)
        
        
        ycib = x[roi_cols['Mean1']][start:end]
        ycib = [v - np.mean(ycib) for v in ycib]
        #print(ycib)
        
        ylab = x[roi_cols['Mean2']][start:end]
        ylab = [v - np.mean(ylab) for v in ylab]
        ylab = [v + 70 for v in ylab]
        
        # Plots the traces
        
        plt.plot(xvals, ylab, label='proboscis tip', linewidth=lw, color='k')
        plt.plot(xvals, ycib, label='cibarium', linewidth=lw, color='b')
        
        
        
        
        
        
         
        if labels == 'yes':
            plt.title(td['condition'], fontproperties=fontv, horizontalalignment='left')
            
            #Plots legend and removes the border around it.
            legend=plt.legend()
            #legend = plt.legend(bbox_to_anchor = (1.5, 1.6))
            legend.draw_frame(False)
            ltext  = legend.get_texts() 
            plt.setp(ltext, fontproperties=fontv) 
        
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
        
        # Specifies the number of tickmarks/labels on the yaxis.
        #ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 
        ## Removes tick labels and ticks from xaxis.
        ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
        
        if labels == 'yes':
            plt.ylabel(ylabel, fontsize=fontsz, labelpad=12)
            fig1.figsize = (6, 3)
            
        # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower 
        #lefthand corner of the figure.
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(left=0.05)
        fig1.subplots_adjust(right=0.95)
        fig1.subplots_adjust(top=0.95)
        
        #ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(XAXISTICKS)) 
        
         #Specifies axis labels and axis tick label sizes.
        plt.xlabel(xlabel, fontproperties=fontv)
        plt.ylabel(ylabel, fontproperties=fontv)
        plt.xticks([0, 0.2, 0.4, 0.6], fontproperties=fontv)
        plt.xlim( (0, xlim+0.05) )
        #plt.yticks(fontproperties=fontv)
        
       
        
        # Saves the figures in plots/plots.
        if labels == 'no':
            plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))),
                    'plots')
            makenewdir(plotfolder)
            figname = os.path.join(plotfolder, movie + '_trace_nolab')
            plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
            plt.savefig(figname+'.png', dpi=FIGDPI, format='png')
            os.chdir('../')

        if labels == 'yes':
            plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))),
                    'plots')
            makenewdir(plotfolder)
            figname = os.path.join(plotfolder, movie + '_trace')
            plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
            plt.savefig(figname+'.png', dpi=FIGDPI, format='png')
            os.chdir('../')




matplotlib.rc('axes', linewidth=LINEWIDTH)
# Generates a list of movie paths in the data folder.
files = dftf.batch_s('.')   


# Generates dft traces and plots for each roi in each movie.

plottrace_paper(MOVIES, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, XLABEL, YLABEL, YAXISTICKS,
        XAXISTICKS, LABELS, LINEWIDTH, FS)
    
os.chdir('../')

        

