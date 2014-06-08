#! /usr/bin/env python

from mn.cmn.pool_results import *
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


homefol = os.path.abspath('.')
probendfol = cmn.makenewdir('probend')
probendpath = os.path.join(homefol, probendfol)

print(os.path.basename(os.getcwd()))
name = (os.path.basename(os.getcwd())).split('_')[1]

if name == '112648':
    expts = ['2010-1130_112648_tnt_probend', '2010-1201_113990_tnt_probend',
            '2010-1210_113990_tnt_probend', '2010-1213_112648_tnt_probend']
    POINTS = 2

if name == '423':
    expts = ['2011-0329_423_tnt_probend', '2011-0331_423_tnt_probend',
            '2011-0406_423_tnt_probend']
    POINTS = 3

if name == '112204':
    expts = ['2011-0313_112204_tnt_probend', '2011-0316_112204_tnt_probend']
    POINTS = 4


# Values for formatting graph.
FONTSIZE = 6.7 # Font size for tick labels, axis labels.
FIGW = 1.5/5 * POINTS # Figure width in inches
FIGH = 1.25# Figure height in inches
FIGDPI = 600
XLIM = POINTS+0.5
YLIM = 0.012
YMIN = -1
YAXISTICKS = 3
#XAXISTICKS = POINTS
LW = 0.75
NLIM = 3




def plotmeanspaper(meanpointsdict, withyticks):  
    
    
    matplotlib.rc('axes', linewidth=LW)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    fontv = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(FONTSIZE)
    
    fonti = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/ariali.ttf')
    fonti.set_size(FONTSIZE)
    
    fig1 = plt.figure(figsize=(FIGW, FIGH), dpi=FIGDPI, facecolor='w', edgecolor='k')
    
    for condition, val in meanpointsdict.iteritems():
        print(condition)
        if 'x TNT' in condition:
            color = '#B52634'
            condleg = 'GAL4 x\nTNT'
        elif 'GAL4' in condition:
            color='#2338C2'
            condleg = 'GAL4'
        elif 'UAS' in condition:
            color = 'k'
            condleg = 'TNT'
    
        #if len(val['mean']) < 5:
            #y = val['mean']
        #else:
            #y = val['mean'][0:5]
        n = val['n']
        lims = np.tile(NLIM, len(n))
        
        ntruth = n >= lims
        
        try:
            fa = list(ntruth).index(False)
            if fa < POINTS:
                y = val['mean'][:fa]
                stderr = val['stderr'][:fa]
            else:
                y = val['mean'][:POINTS]
                stderr = val['stderr'][:POINTS]
        
        except ValueError:
            y = val['mean'][:POINTS]
            stderr = val['stderr'][:POINTS]
        
        print(y)
        
        x = np.linspace(1, len(y), len(y))
        
        
        
        plt.errorbar(x, y, yerr=stderr, xerr=None, elinewidth=0.75, mfc=color, mec=color,
                ecolor=color, barsabove='True', capsize=2, fmt='o', ms=2.5, label=condleg)
        
    plt.xticks(np.arange(POINTS+1), fontproperties=fontv)
    
    if withyticks == 'yes':    
    
        plt.yticks(fontproperties=fontv)
        plt.xlabel('Pump number', fontproperties=fontv)
        plt.ylabel('Area ('r'mm$^2$)', fontproperties=fontv)
        
        legend = plt.legend(loc='upper right', bbox_to_anchor = (1.5, 1.6), markerscale=0.1,
                numpoints=1, labelspacing=0.1)
        ltext  = legend.get_texts()
        plt.setp(ltext, fontproperties=fonti)
        # Removes border around the legend.
        legend.draw_frame(False)
        
    
    plt.xlim( (0, XLIM) )
    plt.ylim( (0, YLIM) )
    
    ax = plt.gca()        
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(YAXISTICKS)) 
    #ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(XAXISTICKS)) 
    
    ## Removes tick labels and ticks from xaxis.
    #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    if withyticks == 'no':
        ax.yaxis.set_ticklabels([''])
    
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower
    #lefthand corner of the figure.
    fig1.subplots_adjust(bottom=0.23)
    fig1.subplots_adjust(left=0.17)
    fig1.subplots_adjust(right=0.95)
    

ad, pd, pdd, md, sd, asd = pool_probendarea_results('data_area_liquid', expts)
os.chdir(probendpath)
dal.savemeans(md, probendpath, 'means_area_liquid.txt')
dal.savestats(asd, probendpath, 'stats_area_liquid.txt')
plotmeanspaper(md, 'yes')
dal.savemeanplot(probendpath, 'means_area_liquid_paper', 'png', FIGDPI)
dal.savemeanplot(probendpath, 'means_area_liquid_paper', 'svg', FIGDPI)

plotmeanspaper(md, 'no')

dal.savemeanplot(probendpath, 'means_area_liquid_paper_noyticks', 'png', FIGDPI)
dal.savemeanplot(probendpath, 'means_area_liquid_paper_noyticks', 'svg', FIGDPI)

#dal.for_mc_conds(sd, probendpath
