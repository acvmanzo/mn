import mn.dftf.dftf as dftf
import os
import matplotlib.pyplot as plt
import numpy as np
import operator
from mn.cmn.cmn import *
import matplotlib
import pickle
import mn.gof.freqvstime as ft


# Plots raw traces on one graph from the movies specified below.
# Run from the 'data' folder; in the 'data' folder are individual movie folders (similar to the 
# experiment/data folders).

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

if TYPE == 'fvt':
    PLOTNAME = 'fvt'
    YLABEL = 'Hz'
    XLABEL = 'Time'
    YMIN = -1
    YLIM = 7
    WINDOWSEC = 1
    TIMEOFFSET = 0
    
    
if TYPE == 'dft':
    PLOTNAME = 'dfttraces.png'
    YLABEL = 'Amplitude'
    XLABEL = 'Hz'
    YMIN = 0
    YLIM = 4
    
    
if TYPE == 'raw':
    PLOTNAME = 'rawtraces'
    YLABEL = 'Arbitrary Intensity'
    XLABEL = 'Time (s)'    
    YMIN = -18
    YLIM = 75
    

FONTSIZE = 6.7 # Font size for tick labels, axis labels.
FIGW = 2.33# Figure width in inches
FIGH = 2 # Figure height in inches
FIGDPI = 600 # Figure dpi

BORDER = 'no'

YAXISTICKS = 2
XAXISTICKS = 4
TIME = 8 # Length of time the traces show.
TIMEOFFSET = 0 # Amount of time to offset the trace by (perhaps useful when plotting freq vs. 
#time graphs).
WITHLEG = 'no' # Change to yes if you want a legend plotted.
XLIMHZ = 10




# Dictionary where the keys are the movie names and the values are the condition, the y offset of
# the trace (so that they aren't on top of each other), and the color the of the trace.

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_191243': ['423 x dTRPA1 - 24', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dTRPA1 - 32', 15, 'r'], 
#'mov_20110518_192012': ['423 x dTRPA1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_191243': ['423 x dTRPA1 - 24', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dTRPA1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dTRPA1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dTRPA1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dTRPA1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_201605': ['wild type',45, 'k'], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 30, 'b'], 
#'mov_20110527_163607_part2' :['423 x dTRPA1 - 32', 15, 'r'], 
#'mov_20110527_150743': ['423 x dTRPA1 - 32', -5, 'r']}

#MOVIES = {'mov_20101130_200533': ['control',67, 'k'], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 45, 'b'], 
#'mov_20110527_163607_part2' :['112648 x dTRPA1 - 32', 20, '#FF6A00'], 
#'mov_20110518_192012': ['112648 x dTRPA1 - 32', -7, 'r']}

# USED IN THE CURRENT GRAPH
#MOVIES = {'mov_20101130_200533': ['control', 67, 'k'], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 45, 'b'], 
#'mov_20110527_163607_part2' :['112648 x dTRPA1 - 32', 20, '#FF6A00'], 
#'mov_20110518_184849': ['112648 x dTRPA1 - 32', -7, 'r']}

# WITH DTRPA DRINKING AT 32
#MOVIES = {'mov_20110517_174209': ['control', 67, 'k', '(i) '], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 45, 'k', '(ii) '], 
#'mov_20110527_163607_part2' :['112648 x dTRPA1 - 32', 20, '#B52634', '(iii) '], 
#'mov_20110518_192012': ['112648 x dTRPA1 - 32', -7, '#B52634', '(iv) ']}

#MOVIES = {'mov_20110517_181356': ['UAS-dTRPA1 - drinking - 32'+u'\u00b0'+'C', 67, 'k', '(i) '], 
#'mov_20110518_195501': ['UAS-dTRPA1 - 32', 45, 'k', '(ii) '], 
#'mov_20110527_163607_part2' :['MN11+12 x dTRPA1 - 32', 20, '#B52634', '(iii) '], 
#'mov_20110518_192012': ['MN11+12 x dTRPA1 - 32', -7, '#B52634', '(iv) ']}

MOVIES = {'mov_20110517_181356': ['UAS-dTRPA1 - drinking', 67, 'k', '(i) '], 
'mov_20110518_195501': ['UAS-dTRPA1', 45, 'k', '(ii) '], 
'mov_20110527_163607_part2' :['MN11+12 x dTRPA1 - fly 1', 20, '#B52634', '(iii) '], 
'mov_20110518_192012': ['MN11+12 x dTRPA1 - fly 2', -7, '#B52634', '(iv) ']}


def oneplot(moviedict, toplotdict, figw, figh, figdpi, fontsz, border, ylabel, ylim, time, ymin, 
        xaxisticks, withleg='no'):
    
    """Moviedict is the above dictionary of movies, toplotdict is a dictionary produced by 
    toplot(), and other values are what's specified as global variables."""
    fontv = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    fonti = matplotlib.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/ariali.ttf')
    fonti.set_size(fontsz)
    
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    #Plots data on one graph with parameters specified in the moviedict directory.
    for k, v in moviedict.iteritems():
        cond1, offset, color, inum = v
        xvals = toplotdict[k][0]
        data = toplotdict[k][1] + offset
        condition = cond1
        #condition = toplotdict[k][2]
        print(condition)
        plt.plot(xvals, data, color, linewidth = 0.5, label=cond1)


        if k == 'mov_20110517_181356':
            plt.text(0.2, offset+9, inum, horizontalalignment='left', fontproperties=fontv)
            plt.text(0.65, offset+9.8, condition, horizontalalignment='left', 
                    fontproperties=fonti)
            #plt.text(3.05, offset+9, '- drinking', horizontalalignment='left', 
            #fontproperties=fontv)            
        if k == 'mov_20110518_195501':
            plt.text(0.2, offset+4, inum, horizontalalignment='left', fontproperties=fontv)
            plt.text(0.72, offset+4.8, condition, horizontalalignment='left', 
                    fontproperties=fonti)
        if k == 'mov_20110527_163607_part2':
            plt.text(0.2, offset+5, inum, horizontalalignment='left', fontproperties=fontv)
            plt.text(0.8, offset+5.8, condition, horizontalalignment='left', 
                    fontproperties=fonti)
        if k == 'mov_20110518_192012':
            plt.text(0.2, offset+9, inum, horizontalalignment='left', fontproperties=fontv)
            plt.text(0.8, offset+9.8, condition, horizontalalignment='left', 
                    fontproperties=fonti)



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
        plt.setp(ltext, fontsize=fontsz)
         #Removes border around the legend.
        legend.draw_frame(False)
    
  
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
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(xaxisticks)) 
    
    # Specifies axis labels and axis tick label sizes.
    plt.xlabel(XLABEL, fontproperties=fontv, labelpad=4)
    plt.ylabel(ylabel, fontproperties=fontv, labelpad=4)
    plt.xticks(fontproperties=fontv)
    plt.yticks(fontproperties=fontv)
    
    # Specifies axis limits.
    plt.axis( [0, time-TIMEOFFSET, ymin, ylim])
    
    # Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand
    #corner of the figure.
    #fig1.subplots_adjust(top=0.8)
    fig1.subplots_adjust(left=0.1)
    #fig1.subplots_adjust(right=0.95)
    
    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    #for line in ax.get_xticklines():
        #line.set_visible(False)

def gentoplot(time):
    """Generates a dictionary where the keys are movie names and the values are the raw trace for
    plotting. Time specifies the length of time in seconds of the plots shown."""
    
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
                frameoffset = TIMEOFFSET * td['fps']
                #print(frames)
                if os.path.basename(file) == 'mov_20101130_200533' \ 
                or os.path.basename(file) == 'mov_20110517_181356' \ 
                or os.path.basename(file) == 'mov_20110517_174209':
                    plottime = td['seltrace'][frameoffset:frames]/8
                elif os.path.basename(file) == 'mov_20110518_192012':
                    plottime = td['seltrace'][frameoffset:frames]/1.5
                elif os.path.basename(file) == 'mov_20110518_184849':
                    plottime = td['seltrace'][frameoffset:frames]/3
                #elif os.path.basename(file) == 'mov_20110527_163607_part2':
                    #plottime = td['seltrace'][50:frames+50]
                else:
                    plottime = td['seltrace'][frameoffset:frames]
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
                
                toplot[td['moviename']] = [xpoints[:tracelen], 
                        td['dftnormtrunctrace'][:tracelen], condition]
    
    return(toplot)





def saveplotpickle(type, withleg = 'no'):
    
    if type == 'raw':
         # Saves the figures in plots/plots.
        plotfolder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'plots')
        makenewdir(plotfolder)
        figname = os.path.join(plotfolder, PLOTNAME)
        
        if withleg == 'yes':
            plt.savefig(figname+'_leg.svg', dpi=FIGDPI)
            plt.savefig(figname+'_leg.png', dpi=FIGDPI)
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
    
    
    

if __name__ == "__main__":
    
    

    
    if TYPE == 'fvt':
        # Run from plotfolder.
        d = ft.min_idict()
        e = ft.min_frames(d, TIME)
        toplot = ft.pumpsovertime(e, WINDOWSEC)
        
        oneplot(ft.MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, XLIMHZ, 
                YMIN)
        # Saves the figures in plots/plots.
        
        
        
    if TYPE == 'dft':
        toplot = gentoplot_dft(XLIMHZ)
        #oneplot(MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, TIME)
        oneplot(DFT_MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, XLIMHZ, 
                YMIN)

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
        # Run from the data folder.
        #pdframes_from_params(TIME)
        matplotlib.rc('axes', linewidth=0.75)
        
        toplot = gentoplot(TIME)
        oneplot(MOVIES, toplot, FIGW, FIGH, FIGDPI, FONTSIZE, BORDER, YLABEL, YLIM, TIME, YMIN, 
                XAXISTICKS)
        saveplotpickle(TYPE, WITHLEG)
       


