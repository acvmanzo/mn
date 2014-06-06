
from mn.imaging.gclib import *
import mn.cmn.cmn as cmn
import glob


KEYLIST = 'keylist'
    

FONTSIZE = 22 # Font size for tick labels, axis labels.
FIGW = 8 # Figure width in inches
FIGH = 4# Figure height in inches
FIGDPI = 300

BORDER = 'no'
YAXISTICKS = 5
TIME = 10
WINDOWSEC = 1

YLABEL = '%(' + r'$\Delta$' + 'F/F)'
YMIN = -1
YMAX = 2

PLOTFOLDER = 'plots'

def plotgctrace(figw, figh, figdpi, border, ymin, ymax):
    """Code for plotting various trace types."""
    #matplotlib.rc('axes', linewidth=1)
    
    movie = os.path.basename(os.path.abspath('.'))
    fd = load_params(PARAMSFILE)
    fps = float(fd['fps'])
    stimfr = STIMSEC*fps
    bgfr = (STIMSEC-BGSEC)*fps
    condition = fd['tastant']
    
    x, roi_cols = load_results(RESULTSFILE)
    dfft = dff(x[1], bgfr, stimfr)
    xvals = frametosec(x[0], fps)
    
    if movie == '2011-0413_112648_gc30_I_1_Wd_mc':
        dfft = dff(x[2], bgfr, stimfr)
    
    plt.figure()
    fig1 = plt.figure(figsize=(figw, figh), dpi=figdpi, facecolor='w', edgecolor='k')    
    
    plt.plot(xvals[0:40*fps], dfft[0:40*fps], color='k')
    plt.ylim( (ymin, ymax) )
    plt.title(condition, fontsize=FONTSIZE)
    
   
    ax = plt.gca()
    
    #Uncomment lines below to display without top, left and right borders.
    
    if border == 'no':
        for loc, spine in ax.spines.iteritems():
            if loc in ['right','top', 'left', 'bottom']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)
    
        #Uncomment lines below to display ticks only where there are borders.
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        
        ## Removes tick labels and ticks from xaxis.
        ax.axes.xaxis.set_major_locator(matplotlib.ticker.NullLocator())
        ax.axes.yaxis.set_major_locator(matplotlib.ticker.NullLocator())
        
        # Draws a horizontal line at the coordinates specified.
        plt.axhline(y=0, xmin=0, xmax=39, color='#858182')
    
    
   # Saves the figures in plots/plots.
    pardir = cmn.makepardir_data()
    plotfolder = os.path.join(pardir, 'plots')
    makenewdir(plotfolder)
    figname = os.path.join(plotfolder, movie + '_40sec')
    
    if border == 'no':
        plt.savefig(figname+'.svg', dpi=FIGDPI, format='svg')
        plt.savefig(figname+'.png', dpi=FIGDPI, format='png')
    
    if border == 'yes':
        plt.savefig(figname+'_border.svg', dpi=FIGDPI, format='svg')
        plt.savefig(figname+'_border.png', dpi=FIGDPI, format='png')
    plt.close()


def b_plotgctrace(figw, figh, figdpi, border, ymin, ymax):
    
    movies = glob.glob('*')
    for movie in movies:
        print(movie)
        os.chdir(movie)
        plotgctrace(figw, figh, figdpi, border, ymin, ymax)
        os.chdir('../')

b_plotgctrace(FIGW, FIGH, FIGDPI, BORDER, YMIN, YMAX)
