#! /usr/bin/env python

# This script plots frequency vs. time plots, one for each movie, using scripts in mn/gof/freqvstime.py
# Run from the 'phase_analysis/ifiles' folder.

import sys
import os
import mn.dftf.dftf as dftf
from mn.cmn.cmn import *
import matplotlib.pyplot as plt
import matplotlib
import mn.gof.freqvstime as ft

KEYLIST = 'keylist'

# Values for formatting graph.
FONTSIZE = 6.7 # Font size for tick labels, axis labels.
FIGW = 1 # Figure width in inches
FIGH = 1# Figure height in inches
FIGDPI = 600
YLIM = 7.5
YMIN = -1
BORDER = 'no'
YLABEL = 'Pump frequency (Hz)'
YAXISTICKS = 5
XAXISTICKS = 4
TIME = 8
WINDOWSEC = 1
PLOTFOLDER = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1/pooled_112648_dtrpa1/sample_traces/conv_plots'



print('Plotting traces')    


# Specifies name of the columns from the imageJ results file and the names of the rois.
COLS= ['Mean1']
ROIS = ['roi1']

#MOVIES = {'mov_20101130_200533': ['control',45, 'k'], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 30, 'b'], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 15, '#FF6A00'], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_200533': ['control', 45, 'k'], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 30, 'b'], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 15, '#FF6A00'], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -5, 'r'], 'mov_20110518_184849': ['112648 x dtrpa1 - 32', 0, 'r']}


MOVIES = {'mov_20110517_181356': ['control', 67, 'k', '(i) '], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 45, 'k', '(ii) '], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 20, '#B52634', '(iii) '], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -7, '#B52634', '(iv) ']}



def plotfvt_paper(moviedict, figw, figh, figdpi, fontsz, ylim, border, ylabel, yaxisticks, xaxisticks, ymin):
    
    os.chdir('/home/andrea//Documents/lab/motor_neurons/gof/dtrpa1/pooled_112648_dtrpa1/sample_traces/phase_analysis/ifiles')
    
    d = ft.min_idict()
    e = ft.min_frames(d, TIME)
    toplot = ft.pumpsovertime(e, WINDOWSEC)
    
    # Plots the dft.
    for movie, v in toplot.iteritems():
        
        fontv = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
        fontv.set_size(fontsz)
        
        fonti = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/ariali.ttf')
        fonti.set_size(fontsz)
        
        
        fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
           
        xvals, v_conv, cond, fps = v
        cond1, yval, color, inum = moviedict[movie] 
        
        plt.plot(xvals, v_conv, color, linewidth = 0.5, label=cond1)
    
        # Plots the (i), etc.
        plt.text(-0.25, 8, inum, horizontalalignment='left', fontproperties=fontv)
    
        
        ## Plots legend and removes the border around it.
        #legend = plt.legend(numpoints = 1, loc='upper right', bbox_to_anchor=(1, 0.98))
        #legend.draw_frame(False)
        #ltext  = legend.get_texts() 
        #plt.setp(ltext, fontsize=FONTSIZE) 
        
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
        
        #Removes the tickmarks on the x-axis but leaves the labels and the spline.
        for line in ax.get_xticklines():
            line.set_visible(False)
        for line in ax.get_yticklines():
            line.set_visible(False)
        
        # Specifies the number of tickmarks/labels on the yaxis.
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(xaxisticks)) 
        ## Removes tick labels and ticks from xaxis.
        #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
        
        # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
        fig1.subplots_adjust(bottom=0.23)
        fig1.subplots_adjust(left=0.17)
        fig1.subplots_adjust(right=0.95)
        
         #Specifies axis labels and axis tick label sizes.
        
        #plt.xlabel('Time (s)', fontproperties=fontv, labelpad=4)
        #plt.ylabel(ylabel, fontproperties=fontv, labelpad=4, multialignment='center')
        plt.xticks(fontproperties=fontv)
        plt.yticks(fontproperties=fontv)
        
        # Sets the limits.
        plt.axis( [0, len(xvals)/fps+WINDOWSEC, ymin, ylim])
        #plt.ylim( ymin, ylim )
        
        # Saves the figures in plots/plots.
        plotfolder = PLOTFOLDER
        makenewdir(plotfolder)
        figname = os.path.join(plotfolder, movie + '_convplot')
        plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
        plt.savefig(figname+'.png', dpi=FIGDPI, format='png')
        plt.close()



#Run from the 'phase_analysis/ifiles' folder; in the 'data' folder are individual movie folders (similar to the experiment/data folders).

matplotlib.rc('axes', linewidth=0.75)

# Generates dft traces and plots for each roi in each movie.
plotfvt_paper(MOVIES, FIGW, FIGH, FIGDPI, FONTSIZE, YLIM, BORDER, YLABEL, YAXISTICKS, XAXISTICKS, YMIN)

#ft.genf1dict()

