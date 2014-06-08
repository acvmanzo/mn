#! /usr/bin/env python

import os
import shutil
import glob
import mn.cmn.cmn as cmn
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.axes_grid.axislines import Subplot
import matplotlib as mpl
import matplotlib
import mn.gof.gfplot as gfplot
import mn.plot.genplotlib as gpl
import mn.paper.multiplot as mp
import sys


ERRORS = 'stderr' # Determines whether error bars delineate standard error (stderr) or standard deviation (stdev)
SAVEFIG = 'yes'
YAXISTICKS = 4
FIGNAME = 'deltatime'
YLABEL = 'Time (s)' # Label for y-axis.
YLIM = 0.4 # Max y-value.
YMIN = 0

FIGDPI = 600
#FIGW = 3.3 # Figure width in inches
FIGW = 4 # Figure width in inches
FIGH = 1 # Figure height in inches
BARWIDTH = 2
BARNUM = 3
ADJBOTTOM = 0.3
ADJRIGHT = 0.8
ADJLEFT = 0.15
FONTSIZE = 6.7
LINEWIDTH = 0.75
CAPSIZE = 2
LABELPADY = 4

OTHERCOLOR = '#555659'





def multiplot_deltatime(fname1max1min, fname1min1max, errors, savefig, figname, ylim, ylabel,
        figw, figh, figdpi, yaxisticks, ymin, barwidth, barnum, othercolor, fontsz, lw, capsize,
        lpy):
    
    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very
    # similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    fonti = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/ariali.ttf')
    fonti.set_size(fontsz)
    
    #Creates a figure of the indicated size and dpi.
    figw = figw
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    conds_1max1min = []
    means_1max1min = []
    stdevs_1max1min = []
    stderrs_1max1min = []
    ns_1max1min = []
    
    conds_1min1max = []
    means_1min1max = []
    stdevs_1min1max = []
    stderrs_1min1max = []
    ns_1min1max = []
    
    # Some of the condition names are the same; load conditions from the summary file.
    with open(fname1max1min) as f:
        f.next()
        for l in f:
            condition, mean, stdev, stderr, n = l.split(',')[0:5]
            conds_1max1min.append(condition)
            means_1max1min.append(float(mean))
            stdevs_1max1min.append(float(stdev))
            stderrs_1max1min.append(float(stderr))
            ns_1max1min.append(float(n))
            
    with open(fname1min1max) as g:
        g.next()
        for l in g:
            condition, mean, stdev, stderr, n = l.split(',')[0:5]
            conds_1min1max.append(condition)
            means_1min1max.append(float(mean))
            stdevs_1min1max.append(float(stdev))
            stderrs_1min1max.append(float(stderr))
            ns_1min1max.append(float(n))
    
    assert conds_1max1min == conds_1min1max, (conds1max1min, conds_1min1max)

    #barnum = len(conds_1min1max)
    
    #### Plots deltatime 1max1min #####
    # Defines coordinates for each bar.
    
    lastbar_1max1min = (2*barnum*barwidth) # X-coordinate of last bar
    print(lastbar_1max1min)
    x_gen1_1max1min = np.linspace(barwidth, lastbar_1max1min, barnum).tolist()
    print(x_gen1_1max1min)
    x_gen2_1max1min = [x + (lastbar_1max1min + 3*barwidth) for x in x_gen1_1max1min]
    print(x_gen2_1max1min)
    x_gen3_1max1min = [x + (lastbar_1max1min + 3*barwidth) for x in x_gen2_1max1min]
    print(x_gen3_1max1min)
    x_list_1max1min = []
    x_list_1max1min.extend(x_gen1_1max1min)
    x_list_1max1min.extend(x_gen2_1max1min)
    x_list_1max1min.extend(x_gen3_1max1min)
    print(x_list_1max1min)

    colors_1max1min = np.tile('k', barnum).tolist()
      
    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + truebarw for x in x_list_1max1min]

    # Defines limit of x axis.
    xlim = x_list_1max1min[-1]+3*barwidth

    #Plots the bar plot.
    plt.bar(x_list_1max1min, means_1max1min, width=truebarw, color=colors_1max1min, ecolor='k', 
            label='Filling', linewidth=lw)
    # Plots error bars.
    zeros = np.tile(0, len(x_list_1max1min)).tolist()
    x_errbar = [x + 0.5*truebarw for x in x_list_1max1min]
    if errors == 'stderr':
        plt.errorbar(x_errbar, means_1max1min, yerr=[zeros,stderrs_1max1min], fmt=None,
                ecolor='k', lw=lw, capsize=capsize)
    if errors == 'stdev':
        plt.errorbar(x_errbar, means_1max1min, yerr=[zeros,stdevs_1max1min], fmt=None,
                ecolor='k', lw=lw, capsize=capsize)
    
    
    #### Plots deltatime 1min1max #####
    # Defines coordinates for each bar.
    
    lastbar_1min1max = (lastbar_1max1min+barwidth) # X-coordinate of last bar
    print(lastbar_1min1max)
    x_list_1min1max = [x + barwidth for x in x_list_1max1min]
    colors_1min1max = np.tile(othercolor, barnum).tolist()
      
   
    #Plots the bar plot.
    plt.bar(x_list_1min1max, means_1min1max, width=truebarw, color=colors_1min1max, ecolor='k',
            label='Emptying', linewidth=lw)
    # Plots error bars.
    zeros = np.tile(0, len(x_list_1min1max)).tolist()
    x_errbar_1min1max = [x + 0.5*truebarw for x in x_list_1min1max]
    if errors == 'stderr':
        plt.errorbar(x_errbar_1min1max, means_1min1max, yerr=[zeros,stderrs_1min1max], fmt=None,
                ecolor='k', lw=lw, capsize=capsize)
    if errors == 'stdev':
        plt.errorbar(x_errbar_1min1max, means_1min1max, yerr=[zeros,stdevs_1min1max], fmt=None,
                ecolor='k', lw=lw, capsize=capsize)

    
    # Defines the axes.
    ax1 = plt.gca()
        # Formats the yticks.
    plt.yticks(fontproperties=fontv)
    
    # Plots the xticks.
    plt.xticks(xlabel_list, conds_1max1min, rotation=90, multialignment = 'center',
            fontproperties=fonti)
    
    #Uncomment lines below to display without top and right borders.
    for loc, spine in ax1.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['top', 'right']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
     
   
    #Uncomment lines below to display ticks only where there are borders.
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')

    ## Uncomment the line below to remove all of the plot axis lines.
    ##plt.setp(ax, frame_on=False)
    
    ##Uncomment the line below to remove all tick marks/labels.
    ##ax1.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax1.get_xticklines():
        line.set_visible(False)

    plt.ylim(ymax = YLIM)
    plt.xlim(xmax = xlim)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=lpy, fontproperties=fontv, multialignment='center')
    
    # Plots legend
    legend = plt.legend(loc='upper right', bbox_to_anchor = (1.05, 1.5), markerscale=0.1, 
            numpoints=1, labelspacing=0.2)
    # Changes legend font to fontsz.
    ltext  = legend.get_texts()
    plt.setp(ltext, fontproperties=fontv)
    # Removes border around the legend.
    legend.draw_frame(False)

    #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand
    #corner of the figure.
    fig1.subplots_adjust(bottom=ADJBOTTOM)
    fig1.subplots_adjust(right=ADJRIGHT)
    fig1.subplots_adjust(left=ADJLEFT)
    
    ## Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig('deltatime.png', dpi=FIGDPI)
        plt.savefig('deltatime.svg', dpi=FIGDPI)


#genotype = sys.argv[1]
fname1max1min = 'all_ph_1max_1min_means.txt'
fname1min1max = 'all_ph_1min_1max_means.txt'
multiplot_deltatime(fname1max1min, fname1min1max, ERRORS, SAVEFIG, FIGNAME, YLIM, YLABEL, FIGW,
        FIGH, FIGDPI, YAXISTICKS, YMIN, BARWIDTH, BARNUM, OTHERCOLOR, FONTSIZE, LINEWIDTH,
        CAPSIZE, LABELPADY)
