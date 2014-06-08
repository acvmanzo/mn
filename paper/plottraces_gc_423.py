import mn.dftf.dftf as dftf
import os
import matplotlib.pyplot as plt
import numpy as np
from mn.cmn.cmn import *
import matplotlib as mpl
import pickle
from mn.imaging.gclib import *


# Plots raw traces on one graph from the movies specified below.
# Run from the 'data' folder; in the 'data' folder are individual movie folders (similar to the 
# experiment/data folders).

# Same values as in dftf.py, but only plotting roi1.
RESULTS_FILE = 'results1.txt'
PARAMS_FILE = 'params'
KEYLIST = 'keylist'
COLS= ['Mean1']
ROIS = ['roi1'] 
    
PLOTNAME = 'gctraces'
YLABEL =  '%(' + r'$\Delta$' + 'F/F)'
XLABEL = 'Seconds'    
YMIN = 0.5
YLIM = 5

FONTSIZE =  6.7 # Font size for tick labels, axis labels.
FIGW = 2.25 # Figure width in inches
FIGH = 2.5 # Figure height in inches
FIGDPI = 600 # Figure dpi

BORDER = 'no'
WITHLEG = 'no' # Change to yes if you want a legend plotted.

TIME = 40
YAXISTICKS = 4


# Dictionary where the keys are the movie names and the values are the condition, the y offset of
# the trace (so that they aren't on top of each other), and the color the of the trace.

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_191243': ['423 x dtrpa1 - 24', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dtrpa1 - 32', 15, 'r'], 
#'mov_20110518_192012': ['423 x dtrpa1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_191243': ['423 x dtrpa1 - 24', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dtrpa1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dtrpa1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_195501': ['UAS-dtrpa1 - 32', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dtrpa1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dtrpa1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_195501': ['UAS-dtrpa1 - 32', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dtrpa1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dtrpa1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_200533': ['control',67, 'k'], 'mov_20110518_195501': ['UAS-dtrpa1 - 32', 45, 'b'], 'mov_20110527_163607_part2' :['112648 x dtrpa1 - 32', 20, '#FF6A00'], 'mov_20110518_192012': ['112648 x dtrpa1 - 32', -7, 'r']}

#OFFSETS = [1+1.75+1.75+1.75, 1+1.75+1.75, 1+1.75, 1]
##OFFSETS = [3.6, 2.8, 1.8, 1]
OFFSETS = [4.5, 3.6, 2.8, 1.8, 1]
W, V, X, Y, Z = OFFSETS

#MOVIES = {'2011-1107_423_gc30_C_1_Wd_mc': ['Water', W, 'k'], 
#'2011-0718_423_gc30_A_1_Sd_mc': ['1 M sucrose', X, 'b'], 
#'2011-0722_423_gc30_D_1_2Sd_mc' :['2 M sucrose', Y, 'k'], 
#'2011-1112_423_gc30_C_1_Cd_mc': ['100 mM caffeine', Z, 'k']}

MOVIES = {
'2011-1107_423_gc30_C_1_Wd_mc': ['Water', W, 'k'], 
'2012-0201_423_gc30_B_2_Wdt_mc': ['Water (wd)', V, 'k'],
'2011-0718_423_gc30_A_1_Sd_mc': ['1 M sucrose', X, 'b'], 
'2011-0722_423_gc30_D_1_2Sd_mc' :['2 M sucrose', Y, 'k'], 
'2011-1112_423_gc30_C_1_Cd_mc': ['100 mM caffeine', Z, 'k']}



matplotlib.rc('axes', linewidth=1)

def oneplot(moviedict, figw, figh, figdpi, fontsz, border, ylabel, ymax, ymin, 
withleg='no'):
    
    """Moviedict is the above dictionary of movies, toplotdict is a dictionary produced by 
    toplot(), and other values are what's specified as global variables."""
    
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    yconds = []
    #Plots data on one graph with parameters specified in the moviedict directory.
    for k, v in moviedict.iteritems():
        print(k)
        cond1, offset, color = v
        os.chdir(k)
        movie = os.path.basename(os.path.abspath('.'))
        
        fd = load_params(PARAMSFILE)
        fps = float(fd['fps'])
        stimfr = STIMSEC*fps
        bgfr = (STIMSEC-BGSEC)*fps
        #condition = fd['tastant']
        condition = cond1
        condition = condition.replace('M ', 'M\n')
        condition = condition.replace(' (wd)','\n(wd)')
        #ylab = (condition, offset)
        yconds.append((condition, offset))
        
        x, roi_cols = load_results(RESULTSFILE)
        dfft = dff(x[1], bgfr, stimfr) + offset
        if border == 'yes':
             dfft = (dff(x[1], bgfr, stimfr) + offset)*100
             offset = offset*100
        xvals = frametosec(x[0], fps)
    
        if movie == '2011-0413_112648_gc30_I_1_Wd_mc':
            dfft = dff(x[2], bgfr, stimfr) + offset
        
            
    # Plots trace
        plt.plot(xvals[0:40*fps], dfft[0:40*fps], color='k', linewidth=0.5, label='condition')
        plt.axhline(y=offset, xmin=0, xmax=TIME, color='#858182', linewidth=0.5)

        # Draws a horizontal line at the coordinates specified.
        
        print(os.getcwd())
        os.chdir('../')
    
    print(yconds)
    ax = plt.gca()
    
    
    if withleg == 'yes':
         #Plots legend.
        a1 = plt.legend(loc='best', bbox_to_anchor=(0.7, 0.9))
        
        # Manipulates order of the legend entries.
        handles, labels = ax.get_legend_handles_labels()
        print(labels)
        handles2 = handles[3], handles[0], handles[1], handles[2]
        labels2 = labels[3], labels[0], labels[1], labels[2]
        legend = ax.legend(handles2, labels2, bbox_to_anchor=(0.5, 0.98), loc='best')
        # Changes legend font to fontsz.
        ltext  = legend.get_texts()
        plt.setp(ltext, fontproperties=fontv)
         #Removes border around the legend.
        legend.draw_frame(False)
    
  
    #Uncomment lines below to display without top and right borders.
    if border == 'no':
        for loc, spine in ax.spines.iteritems():
            if loc in ['right','top', 'left', 'bottom']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)
        # Removes ticks and labels from the specified axis.
        ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
        #ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
        
        # Plots yticks.
        ylab, off = zip(*yconds)
        plt.yticks(off, ylab, fontproperties=fontv, multialignment='center')
    
    
    #Uncomment lines below to display ticks only where there are borders.
    #ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Specifies axis limits.
    plt.axis( [0, TIME, ymin, ymax])
    
    if border == 'yes':
        # Specifies axis labels and axis tick label sizes.
        #plt.xlabel(XLABEL, fontsize=fontsz)
        plt.ylabel(ylabel, fontproperties=fontv, labelpad=4)
        plt.xticks(fontsize=fontsz)
        plt.yticks(fontsize=fontsz)
        plt.axis( [0, TIME, ymin*100, ymax*100])
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(10))
    
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower 
    #lefthand corner of the figure.
    #fig1.subplots_adjust(top=0.8)
    fig1.subplots_adjust(left=0.2)
    fig1.subplots_adjust(right=0.8)
    
    ## Code for putting the legend on right.
    #xv = [42,47]
    #yv = [1,1]
    #line1 = mpl.lines.Line2D(xv, yv, lw=2., color='k')
    #line1.set_clip_on(False)
    #l = ax.add_line(line1)
    
    #xv = [47,47]
    #yv = [1,2]
    #line2 = mpl.lines.Line2D(xv, yv, lw=2., color='k')
    #line2.set_clip_on(False)
    #l = ax.add_line(line2)
    
    #plt.text(44.5, 0.8, '5 sec', fontsize=FONTSIZE, horizontalalignment='center', 
    #verticalalignment='top',multialignment='center',rotation=0)
    
    #plt.text(50.25, 2, '100%\n' + r'$\Delta$' + 'F/F''', fontsize=FONTSIZE, 
    #horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)
    
    #Code for putting the legend on left
    linex = -19
    liney = 1
    
    plt.text(linex+1.5, liney-0.1, ' 3s', fontproperties=fontv, horizontalalignment='center', 
            verticalalignment='top',multialignment='center',rotation=0)
    
    plt.text(linex-6, liney+0.2, '20%\n(' + r'$\Delta$' + 'F/F)''', fontproperties=fontv, 
            horizontalalignment='center', verticalalignment='top',multialignment='center', 
            rotation=0)
    
    xv = [linex, linex+3]
    yv = [liney, liney]
    line1 = mpl.lines.Line2D(xv, yv, lw=1., color='k')
    line1.set_clip_on(False)
    l = ax.add_line(line1)
    
    xv = [linex, linex]
    yv = [liney, liney+0.2]
    line2 = mpl.lines.Line2D(xv, yv, lw=1., color='k')
    line2.set_clip_on(False)
    l = ax.add_line(line2)
    
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand
    #corner of the figure.
    #fig1.subplots_adjust(top=0.8)
    fig1.subplots_adjust(left=0.42)
    #fig1.subplots_adjust(left=0.5)
    fig1.subplots_adjust(right=0.95)
        
    

def saveplotpickle(withleg = 'no', border='no'):

     # Saves the figures in plots/plots.
    plotfolder = os.path.join(os.path.dirname(os.path.abspath('.')), 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, PLOTNAME)
    if withleg == 'yes':
        plt.savefig(figname+'_leg.svg', dpi=FIGDPI)
        plt.savefig(figname+'_leg.png', dpi=FIGDPI)
    elif border == 'yes':
        plt.savefig(figname+'_bor.svg', dpi=FIGDPI)
        plt.savefig(figname+'_bor.png', dpi=FIGDPI)
    
    else:
        plt.savefig(figname+'.svg', dpi=FIGDPI)
        plt.savefig(figname+'.png', dpi=FIGDPI)
    # Saves a file showing the movies I used for the plot and a pickle file with all the 
    #variables.
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
        d['TIME'] = TIME
        d['PLOTNAME'] = PLOTNAME
        d['YLABEL'] = YLABEL
        d['XLABEL'] = XLABEL
        d['YMIN'] = YMIN
        d['YLIM'] = YLIM
        print(d)
        picklefile = pickle.Pickler(h)
        picklefile.dump(d)
    
    
    

if __name__ == "__main__":

        # Run from the data folder.
        #pdframes_from_params(TIME)
        
    oneplot(MOVIES, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, YMIN, WITHLEG)
    saveplotpickle(WITHLEG, BORDER)
       


