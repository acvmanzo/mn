#! /usr/bin/env python

# Plots bar graphs of data contained in a 'means' file. Sample 'means' file and format:

#Condition,Mean,StdDev,StdError,N,Label
#112648-GAL4,4.82415384615,0.402989949513,0.111769302036,13,data,
#UAS-TNT,5.013125,0.475266750757,0.118816687689,16,data,
#112648 x TNT,2.52156521739,1.0220889022,0.213120268557,23,data,
#112204-GAL4,5.7695,0.516128617691,0.105354312916,24,data,
#UAS-TNT,5.36495652174,0.477205951188,0.0995043192964,23,data,
#112204 x TNT,5.098,0.816750546094,0.142178020565,33,data,
#423-GAL4,6.34676923077,0.761411457941,0.149325072381,26,data,
#UAS-TNT,5.28546153846,0.521647554962,0.102303502383,26,data,
#423 x TNT,3.86392307692,0.903741365448,0.177238263756,26,data,


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





def loadmeans(fname):
    
    dictmeans = {}
    
    with open(fname) as f:
        f.next()
        for l in f:
            condition, mean, stdev, stderror, n = l.strip('\n').split(',')[0:5]
            dictmeans[condition] = map(float, [mean, stdev, stderror, n])
    return(dictmeans)
        


def loadpropci(fname):
    
    dictprops = {}
    with open(fname) as f:
        f.next()
        for l in f:
            condition, prop, lci, uci, nsucc, n = l.strip('\n').split(',')[0:6]
            dictprops[condition] = map(float, [prop, lci, uci, nsucc, n])
    return(dictprops)

def multiplot(type, fname, keyfile, errors, savefig, figname, ylim, border, ylabel, fontsz, figw,
        figh, figdpi, yaxisticks, ymin, barwidth, barnum, lw):
    
    matplotlib.rc('axes', linewidth=lw)
    matplotlib.rc('axes.formatter', limits = [-6, 6])
    
    # Sets font properties.
    fontv = mpl.font_manager.FontProperties()
    # Uncomment line below to set the font to verdana; the default matplotlib font is very
    # similar (just slightly narrower).
    fontv = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/arial.ttf')
    #~ fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
    fontv.set_size(fontsz)
    
    fonti = mpl.font_manager.FontProperties(fname='/home/andrea/.matplotlib/ariali.ttf')
    fonti.set_size(fontsz)
    
    conds = []
    means = []
    stdevs = []
    stderrs = []
    ns = []
    
    # With this data, all the condition names are different.
    if type == 'pumps' or type == 'cibarea' or type == 'gcpeakf' or type == 'gcpeakwater' \ 
    or type == 'gcarea' or type == 'gcdur' or type == 'gcdurwater' or type == 'dyearea' \ 
    or type == 'gcpeakfpool' or type == 'gcareapool' or type == 'gcdurpool' \ 
    or type == 'dyeareapool'  or type == '721_lof' or type == '721_gof':
        # Loads keys in order of plotting from keyfile.
        keylist = cmn.load_keys(keyfile)
        
        # Loads data from fname into a dictionary and generates lists from that data.
        
        dictmeans = loadmeans(fname)
        for condition in keylist:
            mean, stdev, sterr, n = dictmeans[condition]
            means.append(mean)
            stdevs.append(stdev)
            stderrs.append(sterr)
            conds.append(condition)
    
    else:
        # Loads values from the file containing data to be plotted. Used for experiments where
        #some of the conditions are the same (ex., UAS-dTRPA1)
        with open(fname) as f:
            f.next()
            for l in f:
                condition, mean, stdev, stderr, n = l.split(',')[0:5]
                conds.append(condition)
                means.append(float(mean))
                stdevs.append(float(stdev))
                stderrs.append(float(stderr))
                ns.append(float(n))
            print(conds)
    
    #if type == 'gcpeakf' or type == 'gcarea' or type == 'gcdur' or type == 'dyearea':
        #conds = [cond.replace('M ', 'M\n') for cond in conds]
    
    if type == 'gcpeakfpool' or type == 'gcareapool' or type == 'gcdurpool' \ 
    or type == 'dyeareapool':
        g1 = [cond.split('_')[0] for cond in conds]
        genotypes = [g1[0], g1[2]]
        genotypes = [gen.replace('112204', 'MN11') for gen in genotypes]
        genotypes = [gen.replace('423', 'MN12') for gen in genotypes]
        
        
        print(genotypes)
        cond1 = [cond.split('_')[1] for cond in conds]
        print(cond1)
        conds = [cond.replace('M sucrose', 'M') for cond in cond1]
    
          
    # Defines coordinates for each bar.
    if type == 'gcpeakf' or type == 'gcpeakwater' or type == 'gcpeakfpool' \ 
    or type == 'gcarea' or type == 'gcdur' or type == 'gcdurwater' or type == 'dyearea' \ 
    or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool' \ 
    or type == '721_lof' or type == '721_gof':
        lastbar = (1.5*barnum*barwidth)-barwidth # X-coordinate of last bar
        x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
        x_list = x_gen1 # Coordinates for the temperature labels.
        
    else:
        lastbar = (barnum*barwidth)-(0.5*barwidth) # X-coordinate of last bar
        x_gen1 = np.linspace(0.5*barwidth, lastbar, barnum).tolist()
        x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
        x_gen2 = [x + (lastbar + 2*barwidth) for x in x_gen1]
        x_gen3 = [x + (lastbar + 2*barwidth) for x in x_gen2]
        x_list = x_gen1
        x_list.extend(x_gen2)
        x_list.extend(x_gen3)
        print(x_list)
    
    
    if type == 'gcpeakf' or type == 'gcpeakwater' or type == 'gcpeakfpool' \ 
    or type == 'gcarea' or type == 'gcdur' or type == 'gcdurwater' or type == 'dyearea' \ 
    or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        colors = np.tile('k', barnum).tolist()
       
        
    else:
        # Defines the colors for each bar.
        #color1 = np.tile('#3856A6', barnum-1).tolist()
        color1 = np.tile('k', barnum-1).tolist()
        #color1 = np.tile('#555659', barnum-1).tolist() # gray color for controls
        redcol = '#B52634'
        color1.append(redcol)
        colors = np.tile(color1, 3).tolist()  
       
    
  
    
    #Coordinates where the xlabels will be listed.
    truebarw = barwidth-(0.05*barwidth)
    xlabel_list = [x + truebarw/2 for x in x_list]
    
    
    # Defines limit of x axis.
    xlim = x_list[-1]+1.5*barwidth
    
    #Creates a figure of the indicated size and dpi.
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    
        
    #Plots the bar plot.
    plt.bar(x_list, means, width=truebarw, bottom=0, color=colors, ecolor='k', capsize=0.5,
            linewidth=lw)

    #Uncomment the line below and comment the line above to plot both positive and negative error
    #bars.
    #plt.bar(x_list, means, width=0.9, bottom=0, color=colors, ecolor='k')
    
    # The following code plots only the negative error bars for negative data points and positive
    #error bars for positive data points.
    ts = zip(means, stderrs)
    negerr = []
    poserr = []
    if type == 'cibdiffa':
        for t in ts:
            if t[0] < 0:
                negerr.append(t[1])
                poserr.append(0)
            if t[0] >= 0:
                negerr.append(0)
                poserr.append(t[1])
         
        if errors == 'stderr':
            plt.errorbar(xlabel_list, means, yerr=[negerr,poserr], fmt=None, ecolor='k', lw=lw,
                    capsize=2)
            print(means)
            print(poserr)
        else:
            raise
    
    else:
    #Uncomment the lines below to plot only the positive error bars.
    
    #Values for negative error bars (all zeros).
        zeros = np.tile(0, len(x_list)).tolist()
        if errors == 'stderr':
            plt.errorbar(xlabel_list, means, yerr=[zeros,stderrs], fmt=None, ecolor='k', lw=lw,
                    capsize=2)
        if errors == 'stdev':
            plt.errorbar(xlabel_list, means, yerr=[zeros,stdevs], fmt=None, ecolor='k' ,lw=lw,
                    capsize=2)
    
    # Defines the axes.
    ax = plt.gca()


    if type == 'cibdiffa':
        conds2 = []
        for cond in conds:
            print(cond)
            cond = cond.replace('dtrpa1', 'dTRPA1')
            conds2.append(cond)
        conds = conds2


    # Adds labels to the x-axis at the x-coordinates specified in xlabel_list; labels are
    #specified in the conds list.
    if type == 'gcpeakf' or type == 'gcarea' or type == 'gcdur' or type == 'dyearea':
        plt.xticks(xlabel_list, conds, fontproperties=fontv, rotation=90)
    
    if type == 'capdata' or type == 'freq' or type == 'volperpump' or type == 'cibdiffa' \ 
    or type == '721_lof' or type == '721_gof' or type == 'cibareacirc':
        plt.xticks(xlabel_list, conds, rotation=90, fontproperties=fonti)
    
    if type == 'gcareapool' or type == 'gcpeakfpool' or type == 'gcdurpool' \ 
    or type == 'dyeareapool':
        plt.xticks(xlabel_list, conds, fontproperties=fontv)
    
    if type == 'gcdurwater' or type == 'gcpeakwater':
        plt.xticks([])
    
    
    # 'genlabely' and 'genline' sets the y coordinates for where the secondary genotype labels
    #and the horizontal line above them appear.
    
        
    if type == 'cibarea':
        genlabely = -1250
        genline = -950
    
    if type == 'gcpeakfpool' or 'gcpeakf':
        genlabely = 100
        genline = 85
    
    if type == 'dyeareapool':
        #genlabely = -0.085
        genlabely = 0.3
        genline = 0.3
    
    if type == 'dyearea':
        #genlabely = -0.0378
        genlabely = 0.15
        genline = -0.0345
    
    if type == 'gcareapool' or type == 'gcarea':
        genlabely = -325
        genline = -275
    
    if type == 'gcdurpool':
        genlabely = 29
        genline = 29
    
    if type == 'gcdur':
        genlabely = 25
        genline = -5.5
    
    if type == 'pumps':
        genlabely = -14
        genline = -11.5

    if type == 'gcdurwater':
        labelline = -5
        #genline = -11.5
    
    
    #if type == 'gcdurwater':
        #plt.text((x_list[0]+truebarw)/2, labelline, '+', fontproperties=fontv)
        #plt.text((x_list[1]+truebarw)/2, labelline+1, '_', fontproperties=fontv)
    
    
    
    if type == 'pumps' or type == 'cibarea':
        temps = []
        for cond in conds:
            if cond.endswith('24') == True:
                temps.append('24')
            if cond.endswith('32') == True:
                temps.append('32')
        print(conds)
        
        # Xlabels corresponding to the temperatures are added.
        plt.xticks(xlabel_list, temps, rotation=0, fontproperties=fontv)
        
        # List of genotypes are generated.
        genotypes = []
        for cond in conds:
            if '32' in cond:
                pass
            elif 'MN11+12' in cond:
                #cond = cond.replace('+12-GAL4', '\n+12-\nGAL4\n')
                cond = cond.replace('+12-GAL4', '+12-\nGAL4')
                #cond = cond.replace('+12 x', '\n+12 x\n')
                cond = cond.replace('+12 x', '+12 x\n')
                cond = cond.replace(' - 24', '')
                cond = cond.replace('-GAL4','GAL4')
                #cond = cond.replace('-','-\n')
                #cond = cond.replace('x ','x\n')
                cond = cond.replace('dtrpa1', 'dTRPA1')
                genotypes.append(cond)
                          
            else:
                cond = cond.replace(' - 24', '')
                cond = cond.replace('-','-\n')
                cond = cond.replace('dtrpa1', 'dTRPA1')
                cond = cond.replace('x ','x\n')
                
                genotypes.append(cond)
        print('genotypes', genotypes)
        
        # Genotypes are plotted below the temperature labels.
        # Selects every even number from the x coordinate list.
        x_genotypes1 =  map(lambda i: x_list[i],filter(lambda i: i%2 == 0,range(len(x_list))))
        # Adds an extra barwidth for each x coordinate.
        x_genotypes = [x+barwidth for x in x_genotypes1]
        genotypes_x = zip(genotypes, x_genotypes)
        for item in genotypes_x:
            # Plots the genotypes at the specified coordinates (x coordinate, y coordinate,
            #string)
            print('genlabely', genlabely)
            plt.text(item[1], genlabely, item[0], fontproperties=fonti,
                    horizontalalignment='center', verticalalignment='top',
                    multialignment='center',rotation=90)
        
        # Uncomment the lines below to draw vertical lines between the genotype names.
        #xlines1 = [x+ 2*barwidth for x in x_genotypes1]
        #xlines2 = [x_list[0], x_gen2[0], x_gen3[0]]
        #for q in [xlines1, xlines2]:
            #for x in q:
                #xv = np.tile(x, 2).tolist()
                #yv = [-16, ymin]
                 ##plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
                #line = mpl.lines.Line2D(xv, yv, lw=1., color='k')
                #line.set_clip_on(False)
                #l = ax.add_line(line)
            
        # Uncomment the lines below to draw horizontal lines above the genotype names.
        for x in x_genotypes1:
            xv = [x+0.5, x + (2*barwidth-0.5)]
            yv = np.tile(genline, 2).tolist()
            #yv = [-16, ymin]
             #plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
            line = mpl.lines.Line2D(xv, yv, lw=lw, color='k')
            line.set_clip_on(False)
            l = ax.add_line(line)
    
    if type == 'gcpeakfpool' or type == 'gcareapool' or type == 'gcdurpool' \ 
    or type == 'dyeareapool':
        x_genotypes1 =  map(lambda i: x_list[i],filter(lambda i: i%2 == 0,range(len(x_list))))
        # Adds an extra barwidth for each x coordinate.
        x_genotypes = [x+1.25*barwidth for x in x_genotypes1]
        genotypes_x = zip(genotypes, x_genotypes)
        for item in genotypes_x:
            # Plots the genotypes at the specified coordinates (x coordinate, y coordinate,
            #string)
            plt.text(item[1], genlabely, item[0], fontproperties=fonti,
                    horizontalalignment='center', verticalalignment='top', 
                    multialignment='center',rotation=0)
        
         # Uncomment the lines below to draw horizontal lines above the genotype names.
        for x in x_genotypes1:
            print(x)
            #xv = [x-0.6, x + (2.5*barwidth)+0.3]
            xv = [x, x + (2.25*barwidth)]
            yv = np.tile(genline, 2).tolist()
            #yv = [-16, ymin]
             #plt.axvline(x, 0, 1, lw=1, c='k', clip_on='False')
            line = mpl.lines.Line2D(xv, yv, lw=lw, color='k')
            line.set_clip_on(False)
            l = ax.add_line(line)
        
        # Writes xlabel.
        plt.xlabel('[Sucrose]', fontproperties=fontv, labelpad=4)
    
    if type == 'gcpeakf648' or type == 'gcdur648' or type == 'gcarea648' or type == 'dyearea648':
        plt.text(lastbar/2 + 0.75*barwidth, genlabely, 'MN11+12', fontproperties=fonti,
                horizontalalignment='center', verticalalignment='top',multialignment='center', 
                rotation=0)
        
        #line = mpl.lines.Line2D([x_list[0], lastbar+barwidth], [genline, genline], lw=1.,
        #color='k')
        #line.set_clip_on(False)
        #l = ax.add_line(line)
        
    
    # Formats the yticks.
    plt.yticks(fontproperties=fontv)
    
    # Formats the xticks.
    if type == 'gcpeakf' or type == 'gcpeakfpool' or type == 'gcarea' or type == 'gcdur' \ 
    or type == 'dyearea' or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        plt.xticks(multialignment = 'center', fontproperties=fontv)
    
    #Uncomment lines below to display without top and right borders.
    if border == 'no':
        for loc, spine in ax.spines.iteritems():
            if loc in ['left','bottom']:
                pass
            elif loc in ['right','top']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)
    
    
    if border == 'no' and type == 'cibdiffa':
        for loc, spine in ax.spines.iteritems():
            if loc in ['left']:
                pass
            elif loc in ['right','top', 'bottom']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)
        
        
        plt.axhline(y=0, xmin=0, xmax=xlim, color='k', linewidth=1)
   
   
    #Uncomment lines below to display ticks only where there are borders.
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Uncomment the line below to remove all of the plot axis lines.
    #plt.setp(ax, frame_on=False)
    
    #Uncomment the line below to remove all tick marks/labels.
    #ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    
    # Specifies the number of tickmarks/labels on the yaxis.
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(yaxisticks)) 
    

    #Removes the tickmarks on the x-axis but leaves the labels and the spline.
    for line in ax.get_xticklines():
        line.set_visible(False)

     #Adjusts the space between the plot and the edges of the figure; (0,0) is the lower
     #lefthand corner of the figure.
    if type == 'freq' or type == 'volperpump' or type == 'capdata' or type == 'cibareacirc':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)
        #fig1.subplots_adjust(top=0.8)
    
    if type == 'gcpeakf' or type == 'gcpeakfpool' or type == 'gcarea' or type == 'gcdur' \ 
    or type == 'dyearea' or type == 'gcareapool' or type == 'gcdurpool' or type == 'dyeareapool':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)      
        fig1.subplots_adjust(top=0.9)      
        #fig1.subplots_adjust(top=0.75)      
        
    
    if type == 'cibdiffa':
        fig1.subplots_adjust(left = 0.15)
        fig1.subplots_adjust(bottom=0.45)
    
    if type == 'pumps':
        fig1.subplots_adjust(bottom=0.3)
        fig1.subplots_adjust(right=0.8)
        fig1.subplots_adjust(left=0.15)
    
     #Might be best to keep it all uniform.
    #fig1.subplots_adjust(left = 0.15)
    #fig1.subplots_adjust(bottom=0.4)
    #fig1.subplots_adjust(right=0.95)
    

    # Sets the x- and y-axis limits.
    plt.axis( [0, xlim, ymin, ylim])

    # Labels the yaxis; labelpad is the space between the ticklabels and y-axis label.
    plt.ylabel(ylabel, labelpad=4, fontproperties=fontv, multialignment='center')

    #plt.title('# Pumps over 30 seconds', fontsize=20)
    
    # Saves the figure with the name 'figname'.
    if savefig == 'yes':
        plt.savefig(figname+'.svg', dpi=300)
        plt.savefig(figname+'.png', dpi=300)


def makeallsumm(data):
    # From lof folder. Takes all mean summary files from the folders listed below and combines 
    #the info into one master file. 'Data' is the type of data (ex., pump, dtrpa, etc.). Start
    #from experiment directory.
    
    startpath = os.path.abspath('.')
    
    p648 = 'pooled_112648_dtrpa1'
    p204 = 'pooled_112204_dtrpa1_1copy'
    p423 = 'pooled_423_dtrpa1'
    
    ps = [p648, p204, p423]
    ps = [os.path.join(startpath,p) for p in ps]
    
    nd = os.path.join(startpath, 'pooled_all/{0}/'.format(data))
    cmn.makenewdir(nd)
    nf = nd + 'all_{0}_means.txt'.format(data)
    

    if os.path.exists(nf) == True:
        os.remove(nf)
    
    for p in ps:
        mdir = p + '/' + data
        
        if os.path.exists(mdir) == True:
            os.chdir(mdir)
        else:
            os.chdir(p)

        meansfile = glob.glob('*{0}_means.txt'.format(data))[0]
        shutil.copy(meansfile, nd)
        nk = nd + 'keylist_{0}'.format(os.path.basename(p))
        shutil.copy('keylist', nk)
        

    os.chdir(nd)
    
    mfs = glob.glob('*means.txt')
    
    with open(nf , 'w') as g:
        g.write('Condition,Mean,StdDev,StdError,N,Label\n')
    
    for mf in mfs:
        with open(mf) as h:
            h.next()
            for l in h:
                with open(nf, 'a') as g:
                    g.write(l)


