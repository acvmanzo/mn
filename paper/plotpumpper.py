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



ERRORS = 'stderr' # Determines whether error bars delineate standard error (stderr) or standard deviation (stdev)
SAVEFIG = 'yes'
FIGDPI = 600
YAXISTICKS = 5

FIGNAME = 'pump_per'
YLABEL = 'Pump frequency \n(Hz)' # Label for y-axis.
YLABELPER = 'PER (%)'
YLIM = 8 # Max y-value.
YMIN = 0

FIGW = 2.3# Figure width in inches
FIGH = 1 # Figure height in inches
BARWIDTH = 2
ADJBOTTOM = 0.3
ADJRIGHT = 0.8
ADJLEFT = 0.15
LINEWIDTH = 0.75
LABELPADY = 2
LABELPADX = 4

PERCOLOR = '#555659'
PERTEXTCOLOR = '#3D3E40'
FONTSIZE = 6.7
   

KEYFILES = ['keyfile_c', 'keyfile_s']

CONDPER = ['g24 h/500 mM suc', 'g24 h/50 mM suc', 'g48 h/100 mM suc', 'g24 h/100 mM suc', 'g10 h/100 mM suc']
CONDPUMP = ['24 hours/500 mM sucrose', '24 hours/50 mM sucrose', '48 hours/100 mM sucrose', '24 hours/100 mM sucrose', '10 hours/100 mM sucrose']


PUMPFOL = '/home/andrea/Documents/lab/motor_neurons/wildtype/pooled/pumpfreq_pooled/'
PUMPFILE = 'means_cs_pumpfreq.txt'

PERFOL = '/home/andrea/Documents/lab/motor_neurons/wildtype/pooled/per_check/'
PERFILE = '/home/andrea/Documents/lab/motor_neurons/wildtype/pooled/per-check/per-check_cibdata_m_alpha0.05.txt'


def multiplot_visc(pumpfname, keyfile, errors, savefig, figname, ylim, ylabel, figw, figh, figdpi, yaxisticks, ymin, barwidth, lw, fontsz, lpx, lpy):
    
    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    #Creates a figure of the indicated size and dpi.
    figw = 1.1*figw
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    origconds = []
    conds = []
    means = []
    stdevs = []
    stderrs = []
    ns = []
    
    # With this data, all the condition names are different.
    # Loads keys in order of plotting from keyfile.
    keylist = cmn.load_keys(keyfile)
    
    ### PLOTS PUMP FREQUENCY DATA ###
    # Loads data from pumpfname into a dictionary and generates lists from that data.
    
    dictmeans = mp.loadmeans(pumpfname)
    for condition in keylist:
        mean, stdev, sterr, n = dictmeans[condition]
        means.append(mean)
        stdevs.append(stdev)
        stderrs.append(sterr)
        conds.append(condition)
        origconds.append(condition)
    
    if keyfile == 'keyfile_v':
        conds = [cond.replace('MC', '\nMC') for cond in conds]
            
    barnum = len(keylist)
    # Defines coordinates for each bar.
    
    lastbar = (2*barnum*barwidth)-barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 

    colors = np.tile('k', barnum).tolist()
      
    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + 0.5*truebarw for x in x_list]

    # Defines limit of x axis.
    xlim = x_list[-1]+1.5*barwidth
    print(xlim)
    

    #Plots the bar plot.
    plt.bar(x_list, means, width=truebarw, color=colors, ecolor='k')
    # Plots error bars.
    zeros = np.tile(0, len(x_list)).tolist()
    x_errbar = xlabel_list
    if errors == 'stderr':
        plt.errorbar(x_errbar, means, yerr=[zeros,stderrs], fmt=None, ecolor='k', lw=lw, capsize=2)
    if errors == 'stdev':
        plt.errorbar(x_errbar, means, yerr=[zeros,stdevs], fmt=None, ecolor='k', lw=lw, capsize=2)
    
    # Defines the axes.
    ax1 = plt.gca()
    
    # Writes the label for 500 mM sucrose.    
    line = mpl.lines.Line2D([x_list[0],x_list[2]+barwidth], [-3.65, -3.65], lw=lw, color='k')
    line.set_clip_on(False)
    l = ax1.add_line(line)
   
    plt.text(xlabel_list[1], -4.05, '500 mM sucrose', fontproperties=fontv, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)
    
    # Writes the label for sucrose.
    plt.text(xlabel_list[3]+barwidth, -2.15, 'sucrose', fontproperties=fontv, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)
    
    # Formats the yticks.
    plt.yticks(fontproperties=fontv)
    
    # Plots the xticks.
    plt.xticks(xlabel_list, conds, multialignment = 'center', fontproperties=fontv)
    
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

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)
    
    #Uncomment the line below to remove all tick marks/labels.
    #ax1.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax1.get_xticklines():
        line.set_visible(False)

    plt.ylim(ymax = YLIM)
    plt.xlim(xmax = xlim)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=lpy, fontproperties=fontv, multialignment='center')
    
   
    
     #plt.text(xlabel_list[1], -2, '[Sucrose]', fontproperties=fontv, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)
    
    
    #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    fig1.subplots_adjust(bottom=ADJBOTTOM)
    fig1.subplots_adjust(right=ADJRIGHT)
    fig1.subplots_adjust(left=ADJLEFT)
    
    # Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig('pump_per_'+keyfile+'.png', dpi=300)
        plt.savefig('pump_per_'+keyfile+'.svg', dpi=300)

def multiplot_visc2(pumpfname, keyfile, errors, savefig, figname, ylim, ylabel, figw, figh, figdpi, yaxisticks, ymin, barwidth, lw, fontsz, lpx, lpy):
    
    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    #Creates a figure of the indicated size and dpi.
    figw = 1.1*figw
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    origconds = []
    conds = []
    means = []
    stdevs = []
    stderrs = []
    ns = []
    
    # With this data, all the condition names are different.
    # Loads keys in order of plotting from keyfile.
    keylist = cmn.load_keys(keyfile)
    
    ### PLOTS PUMP FREQUENCY DATA ###
    # Loads data from pumpfname into a dictionary and generates lists from that data.
    
    dictmeans = mp.loadmeans(pumpfname)
    for condition in keylist:
        mean, stdev, sterr, n = dictmeans[condition]
        means.append(mean)
        stdevs.append(stdev)
        stderrs.append(sterr)
        conds.append(condition)
        origconds.append(condition)
    
    if keyfile == 'keyfile_v':
        conds = [cond.replace('% MC', '') for cond in conds]
        conds = [cond.replace(' M', '') for cond in conds]
        
        
            
    barnum = 3
    # Defines coordinates for each bar.
    
    lastbar = (1.3*barnum*barwidth)-(0.5*barwidth) # X-coordinate of last bar
    x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
    x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
    x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
    x_list = x_gen1
    x_list.extend(x_gen2)
    print(x_list)
    

    colors = np.tile('k', barnum).tolist()
      
    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + 0.5*truebarw for x in x_list]
    print(xlabel_list)
    
    # Defines limit of x axis.
    xlim = x_list[-1]+1.5*barwidth
   
    print(means)

    #Plots the bar plot.
    plt.bar(x_list, means, width=truebarw, bottom=0, color=colors, ecolor='k', capsize=0.5, lw=lw)
    # Plots error bars.
    zeros = np.tile(0, len(x_list)).tolist()
    x_errbar = xlabel_list
    if errors == 'stderr':
        plt.errorbar(x_errbar, means, yerr=[zeros,stderrs], fmt=None, ecolor='k', lw=lw, capsize=2)
    if errors == 'stdev':
        plt.errorbar(x_errbar, means, yerr=[zeros,stdevs], fmt=None, ecolor='k', lw=lw, capsize=2)
    
    # Defines the axes.
    ax1 = plt.gca()
    
    # Writes the label for 500 mM sucrose.    
    line = mpl.lines.Line2D([x_list[0],x_list[2]+barwidth], [-2.15, -2.15], lw=lw, color='k')
    line.set_clip_on(False)
    l = ax1.add_line(line)
    
    plt.text(xlabel_list[1], -2.8, '% MC', fontproperties=fontv, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)    
    # Writes the label for sucrose.
    line = mpl.lines.Line2D([x_list[3],x_list[5]+barwidth], [-2.15, -2.15], lw=lw, color='k')
    line.set_clip_on(False)
    l = ax1.add_line(line)
    
    plt.text(xlabel_list[4], -2.8, 'sucrose (M)', fontproperties=fontv, horizontalalignment='center', verticalalignment='top', rotation=0)
    
    # Formats the yticks.
    plt.yticks(fontproperties=fontv)
    
    # Plots the xticks.
    plt.xticks(xlabel_list, conds, multialignment = 'center', fontproperties=fontv)
    
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

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)
    
    #Uncomment the line below to remove all tick marks/labels.
    #ax1.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax1.get_xticklines():
        line.set_visible(False)

    plt.ylim(ymax = YLIM)
    plt.xlim(xmax = xlim)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=lpy, fontproperties=fontv, multialignment='center')
    
   
    
     #plt.text(xlabel_list[1], -2, '[Sucrose]', fontproperties=fontv, horizontalalignment='center', verticalalignment='top',multialignment='center',rotation=0)
    
    
    #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    fig1.subplots_adjust(bottom=ADJBOTTOM)
    fig1.subplots_adjust(right=ADJRIGHT)
    fig1.subplots_adjust(left=ADJLEFT)
    
    # Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig('pump_per_'+keyfile+'.png', dpi=300)
        plt.savefig('pump_per_'+keyfile+'.svg', dpi=300)



def multiplot_pumpper(pumpfname, perfname, keyfile, errors, savefig, figname, ylim, ylabel, ylabelper, figw, figh, figdpi, yaxisticks, ymin, barwidth, lw, fontsz, lpx, lpy):
    
    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    #Creates a figure of the indicated size and dpi.
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
    
    origconds = []
    conds = []
    means = []
    stdevs = []
    stderrs = []
    ns = []
    
    # With this data, all the condition names are different.
    # Loads keys in order of plotting from keyfile.
    keylist = cmn.load_keys(keyfile)
    
    
    ### PLOTS PUMP FREQUENCY DATA ###
    # Loads data from pumpfname into a dictionary and generates lists from that data.
    
    dictmeans = mp.loadmeans(pumpfname)
    for condition in keylist:
        mean, stdev, sterr, n = dictmeans[condition]
        means.append(mean)
        stdevs.append(stdev)
        stderrs.append(sterr)
        conds.append(condition)
        origconds.append(condition)
    
    if keyfile == 'keyfile_s':
        conds = [cond.replace('/100 mM sucrose', '') for cond in conds]
            
    if keyfile == 'keyfile_c':
        conds = [cond.replace('24 hours/', '') for cond in conds]
        conds = [cond.replace(' sucrose', '') for cond in conds]
            

    # Defines coordinates and colors for each bar.
    barnum = len(keylist)
    lastbar = (3*barnum*barwidth)-2*barwidth # X-coordinate of last bar
    x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
    x_list = x_gen1 

    colors = np.tile('k', barnum).tolist()
      
    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + truebarw for x in x_list]


    #Plots the bar plot.
    plt.bar(x_list, means, width=truebarw, color=colors, ecolor='k', linewidth=lw)
    # Plots error bars.
    zeros = np.tile(0, len(x_list)).tolist()
    x_errbar = [x - 0.5*barwidth for x in xlabel_list]
    if errors == 'stderr':
        plt.errorbar(x_errbar, means, yerr=[zeros,stderrs], fmt=None, ecolor='k', lw=lw, capsize=2)
    if errors == 'stdev':
        plt.errorbar(x_errbar, means, yerr=[zeros,stdevs], fmt=None, ecolor='k', lw=lw, capsize=2)
    
    # Defines the axes.
    ax1 = plt.gca()
        
    # Formats the yticks.
    plt.yticks(fontproperties=fontv)
    
    # Formats the xticks.
    plt.xticks(multialignment = 'center')
    
    #Uncomment lines below to display without top and right borders.
    for loc, spine in ax1.spines.iteritems():
        if loc in ['left','bottom', 'right']:
            pass
        elif loc in ['top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
     
   
    #Uncomment lines below to display ticks only where there are borders.
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)
    
    #Uncomment the line below to remove all tick marks/labels.
    #ax1.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax1.get_xticklines():
        line.set_visible(False)

    plt.ylim(ymax=YLIM)

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=lpy, fontproperties=fontv, multialignment='center')
    
    # Labels the xaxis.
    if keyfile == 'keyfile_c':
        plt.xlabel('[Sucrose]', labelpad=lpx, fontproperties=fontv, multialignment='center')
            
    if keyfile == 'keyfile_s':
        plt.xlabel('Starvation time', labelpad=lpx, fontproperties=fontv, multialignment='center')
    
    
    ### PLOTS PER DATA ###
    ax2 = ax1.twinx()
    
    props = []
    lcis = []
    ucis = []
    nsuccesses = []
    ntotals = []
    
    
    perdictprop = mp.loadpropci(perfname)
    for condition in keylist:
        
        cind = CONDPUMP.index(condition)
        condition = CONDPER[cind]
        prop, lci, uci, nsuccess, ntotal = perdictprop[condition]
        props.append(prop*100)
        lcis.append((prop-lci)*100)
        ucis.append((uci-prop)*100)
        nsuccesses.append(nsuccess)
        ntotals.append(ntotal)
    
    lastbarper = (3*barnum*barwidth-barwidth) # X-coordinate of last bar
    x_gen1per = np.linspace(1.5*barwidth, lastbarper, barnum).tolist()
    x_listper = x_gen1per 
    print(x_listper)
    print(x_list)
    colors = np.tile(PERCOLOR, barnum).tolist()
      
    
    #Plots the bar plot and error bars.
    x_errbar_per = [x + 0.5*barwidth for x in x_listper]
    plt.bar(x_listper, props, width=truebarw, color=colors, linewidth=lw)
    plt.errorbar(x_errbar_per, props, yerr=[lcis,ucis], fmt=None, ecolor='k', lw=lw, capsize=2)
    for loc, spine in ax2.spines.iteritems():
        if loc in ['right']:
            pass
        elif loc in ['left', 'top', 'bottom']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    
    # Plots the yticks and ylabel for the PER scale.
    plt.yticks(fontproperties=fontv, color=PERTEXTCOLOR)
    plt.ylim(ymax=100)
    plt.ylabel(ylabelper, labelpad=lpy, fontproperties=fontv, multialignment='center', rotation=-90, color=PERTEXTCOLOR)
    

    ### ADJUSTS FIGURE PROPERTIES ####
    
    # Plots the xticks and labels for both scales.
    ax1.xaxis.set_ticks(xlabel_list)
    ax1.xaxis.set_ticklabels(conds, fontproperties=fontv)
    xlim = x_list[-1]+2.5*barwidth
    
    # Sets the x limits.
    plt.xlim( [0, xlim] )
    print(xlim)
    
    #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower lefthand corner of the figure.
    fig1.subplots_adjust(bottom=ADJBOTTOM)
    fig1.subplots_adjust(right=ADJRIGHT)
    fig1.subplots_adjust(left=ADJLEFT)
    
    # Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig('pump_per_'+keyfile+'.png', dpi=300)
        plt.savefig('pump_per_'+keyfile+'.svg', dpi=300)




if __name__ == '__main__':
    pumpfile = os.path.join(PUMPFOL, PUMPFILE)
    #perfile = os.path.join(PERFOL, PERFILE)
    perfile = PERFILE
    
    for keyfile in KEYFILES:
        multiplot_pumpper(pumpfile, perfile, keyfile, ERRORS, SAVEFIG, FIGNAME, YLIM, YLABEL, YLABELPER, FIGW, FIGH, FIGDPI, YAXISTICKS, YMIN, BARWIDTH, LINEWIDTH, FONTSIZE, LABELPADX, LABELPADY)

    multiplot_visc2(pumpfile, 'keyfile_v', ERRORS, SAVEFIG, FIGNAME, YLIM, YLABEL, FIGW, FIGH, FIGDPI, YAXISTICKS, YMIN, BARWIDTH, LINEWIDTH, FONTSIZE, LABELPADX, LABELPADY)

