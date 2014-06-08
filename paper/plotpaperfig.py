#! /usr/bin/env python


from mn.paper.multiplot import *
import sys

DATA = sys.argv[1]

KEYFILE = 'keylist'
#DATA = 'freq' # Choose 'capdata', 'freq'
ERRORS = 'stderr' # Determines whether error bars delineate standard error (stderr) or
#standard deviation (stdev)
SAVEFIG = 'yes'
BORDER = 'no' # Whether the top and right splines (borders) are drawn.
FIGDPI = 600
FONTSIZE = 6.7
LINEWIDTH = 0.75




if DATA == 'capdata':
    FNAME = 'all_capdata_means.txt' # Name of the file with the data.
    FIGNAME = 'all_capdata_norm'
    YLABEL = 'Ingestion rate\n (nL/sec)' # Label for y-axis.
    YLIM = 16 # Max y-value.
    XLIM = 12.5
    YMIN = 0
    
    FIGW = 3.3 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 3
    YAXISTICKS = 5

if DATA == 'freq':
    FNAME = 'all_freq_means.txt'
    FIGNAME = 'pumpfreq_lof'
    YLABEL = 'Pump frequency\n (Hz)' # Label for y-axis.
    YLIM = 8 # Max y-value.
    YMIN = 0
    
    FIGW = 3.3 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 3
    YAXISTICKS = 5

if DATA == 'volperpump':
    FNAME = 'all_volperpump_means.txt'
    FIGNAME = 'volperpump_lof'
    YLABEL = 'Volume per pump\n (nL)' # Label for y-axis.
    YLIM = 3 # Max y-value.
    YMIN = 0
    
    FIGW = 3.3 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 3
    YAXISTICKS = 3

if DATA == 'cibdiffa':
    FNAME = 'all_diffa_means.txt'
    KEYFILE = 'keylist' # not used
    FIGNAME = 'all_cibdiffa_dtrpa1'
    #YLABEL = r'$\Delta$' + 'cibarial area\n('r'$\mu$m$^2$)'
    YLABEL = r'$\Delta$' + 'cibarial area ('r'$\mu$m$^2$)'
    YLIM = 4000
    YMIN = -2000
    YAXISTICKS = 4

    #FIGW = 3.25 # Figure width in inches
    FIGW = 2.75 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 3 # Number of bars to plot per gal4 line.



if DATA == 'pumps':
    FNAME = 'all_pumps_means.txt'
    FIGNAME = 'all_pumps_dtrpa1'
    YLABEL = 'Number of pumps'
    YLIM = 35
    YMIN = -2
    YAXISTICKS = 4

    FIGW = 6 # Figure width in inches
    FIGH = 1 # Figure height in inches
    #FIGH = 3 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 6 # Number of bars to plot per gal4 line.

if DATA == 'cibarea':
    FNAME = 'all_cibareas_means.txt'
    KEYFILE = 'keylistmean'
    FIGNAME = 'all_cibareas_dtrpa1'
    YLABEL = r'$\mu$m$^2$'
    YLIM = 4000
    YMIN = 0
    YAXISTICKS = 5

    FIGW = 3 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 6 # Number of bars to plot per gal4 line.
    

if DATA == '721_lof':
    FNAME = 'peakf_means.txt'
    KEYFILE = 'keylist'
    FIGNAME = '721_peakf'
    YLABEL = 'Pump frequency\n (Hz)' # Label for y-axis.
    YLIM = 8 # Max y-value.
    YMIN = 0
    
    FIGW = 0.8 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 2
    YAXISTICKS = 5
    
if DATA == '721_gof':
    FNAME = '721_pumps_means.txt'
    KEYFILE = 'keylist'
    FIGNAME = '721_pumps'
    YLABEL = 'Number of pumps' # Label for y-axis.
    YLIM = 35 # Max y-value.
    YMIN = -2
    
    FIGW = 1.5 # Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 4
    YAXISTICKS = 5

if DATA == 'cibareacirc':
    FNAME = 'means_pooled_cibareacirc_um.txt'
    FIGNAME = 'paper_cibareacirc'
    YLABEL = 'Area / prob width \n(' + r'$\mu$m$)$' # Label for y-axis.
    YLIM = 110 # Max y-value.
    YMIN = 0
    
    FIGW = 3.3# Figure width in inches
    FIGH = 1 # Figure height in inches
    BARWIDTH = 2
    BARNUM = 3
    YAXISTICKS = 5



if True:
    multiplot(DATA, FNAME, KEYFILE, ERRORS, SAVEFIG, FIGNAME, YLIM, BORDER, YLABEL, FONTSIZE,
            FIGW, FIGH, FIGDPI, YAXISTICKS, YMIN, BARWIDTH, BARNUM, LINEWIDTH)
