import os
import glob
from mn.imaging.gclib import *
import matplotlib as mpl

FPS = 19.8
STIMSEC = 8
BGSEC = 3 # Number of seconds before STIMSEC used to calculate the basal fluorescence (if BGSEC = 
# 3, then seconds STIMSEC-BGSEC to STIMSEC will be used to calculate the basal fluorescence.
STIMDUR = 39 # how long the movie lasts in seconds
FONTSIZE =  6.7 # Font size for tick labels, axis labels.
FIGW = 4 # Figure width in inches
FIGH = 2 # Figure height in inches
FIGDPI = 1000 # Figure dpi
YAXISTICKS1 = 5
YAXISTICKS2 = 5
XAXISTICKS2 = 12

fontsz = FONTSIZE
figw = FIGW
figh = FIGH
figdpi = FIGDPI
lw = 0.75

fontv = mpl.font_manager.FontProperties(fname='/usr/share/matplotlib/mpl-data/fonts/ttf/arial.ttf')
fontv.set_size(fontsz)
matplotlib.rc('axes', linewidth=lw)

temp = os.path.abspath('.').split('/')
summfolder = os.path.join('/', temp[1], temp[2], temp[3], temp[4], 'paper')
makenewdir(summfolder)

os.chdir('data')
names = glob.glob('*')
# Absolute path rather than relative path allows changing of directories in fn_name.
names = [os.path.abspath(name) for name in names]
names = sorted(names)

d = {}
for name in names:
    print(name)
    os.chdir(name)
    movie = os.path.basename(name)

    fps = FPS
    stimfr = STIMSEC*fps
    bgfr = (STIMSEC-BGSEC)*fps
    
    a = TraceData(RESULTSFILE, PARAMSFILE)
    td = a.Processrawtrace()
    trace1 = (td['Mean1']['dff']['trace'])*100
    trace2 = (td['Mean2']['dff']['trace'])*100
    
    xvals = frametosec(list(np.arange(len(trace1))), fps)
        
# Plots trace
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')
    plt.plot(xvals[0:40*fps], trace1[0:40*fps], color='b', linewidth=0.5, label='neuron 1')
    plt.plot(xvals[0:40*fps], trace2[0:40*fps], color='r', linewidth=0.5, label='neuron 2')
    ax = plt.gca()
    
    legend = plt.legend(loc = 'upper right', markerscale = 1)
    ltext  = legend.get_texts()
    plt.setp(ltext, fontproperties=fontv)
         #Removes border around the legend.
    legend.draw_frame(False)
    
    
    
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    plt.xticks(fontproperties = fontv)
    plt.yticks(fontproperties = fontv)
    
    plt.xlabel('Time (s)', fontproperties=fontv)
    plt.ylabel('%(' + r'$\Delta$' + 'F/F)', fontproperties=fontv)
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        plt.ylim( (-50, 150) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5)) 
    
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        plt.ylim( (-25, 100) )
    
    figname = os.path.join(summfolder, movie+'_paper')
    plt.savefig(figname+'.svg', dpi=FIGDPI)
    plt.savefig(figname+'.png', dpi=FIGDPI)
    plt.close()

#Plots close-uptrace


# Zoom2
    fig2 = plt.figure(figsize=(1.5, 2), dpi=figdpi, facecolor='w', edgecolor='k')
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        tstart=32*fps
        tend = 36*fps
        
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        tstart=20.8*fps
        tend=24.8*fps
    
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        tstart=18*fps
        tend=22*fps
    
    plt.plot(xvals[tstart:tend], trace1[tstart:tend], color='b', linewidth=0.5, label='neuron 1')
    plt.plot(xvals[tstart:tend], trace2[tstart:tend], color='r', linewidth=0.5, label='neuron 2')
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
     
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(XAXISTICKS2)) 
    
    plt.xticks(fontproperties = fontv, rotation=90)
    plt.yticks(fontproperties = fontv)
    
    plt.xlabel('Time (s)', fontproperties=fontv)
    plt.ylabel('%(' + r'$\Delta$' + 'F/F)', fontproperties=fontv)
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        plt.ylim( (-30, 120) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        plt.ylim( (-20, 60) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    
    figname = os.path.join(summfolder, movie+'_zoom2_paper')
    plt.savefig(figname+'.svg', dpi=FIGDPI)
    plt.savefig(figname+'.png', dpi=FIGDPI)
    plt.close()


    

# Zoom1

    fig3 = plt.figure(figsize=(1.5, 2), dpi=figdpi, facecolor='w', edgecolor='k')
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        tstart=10*fps
        tend = 14*fps
    
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        tstart=11.6*fps
        tend=15.6*fps    
    
    
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        tstart=8*fps
        tend=12*fps
    
    plt.plot(xvals[tstart:tend], trace1[tstart:tend], color='b', linewidth=0.5, label='neuron 1')
    plt.plot(xvals[tstart:tend], trace2[tstart:tend], color='r', linewidth=0.5, label='neuron 2')
    ax = plt.gca()

    #ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(YAXISTICKS)) 
    
    
    
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(YAXISTICKS2)) 
    
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(12)) 
    else:
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(XAXISTICKS2)) 
    
    plt.xticks(fontproperties = fontv, rotation=90)
    plt.yticks(fontproperties = fontv)
    
    plt.xlabel('Time (s)', fontproperties=fontv)
    plt.ylabel('%(' + r'$\Delta$' + 'F/F)', fontproperties=fontv)
    
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        plt.ylim( (-30, 120) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        plt.ylim( (-25, 150) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(7))
    
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        plt.ylim( (-30, 90) )
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        
    figname = os.path.join(summfolder, movie+'_zoom_paper')
    plt.savefig(figname+'.svg', dpi=FIGDPI)
    plt.savefig(figname+'.png', dpi=FIGDPI)
    plt.close()
