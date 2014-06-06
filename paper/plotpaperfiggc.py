#! /usr/bin/env python


from mn.paper.multiplot import *
import sys

DATA = sys.argv[1]


KEYFILE = 'keylist'
#DATA = 'freq' # Choose 'capdata', 'freq'
ERRORS = 'stderr' # Determines whether error bars delineate standard error (stderr) or standard deviation (stdev)
SAVEFIG = 'yes'
BORDER = 'no' # Whether the top and right splines (borders) are drawn.
FONTSIZE = 6.7 # Font size for tick labels, axis labels; superceded by assignment in multiplot
FIGDPI = 600
YAXISTICKS = 5



if DATA == 'capdata':
    FNAME = 'all_capdata_means.txt' # Name of the file with the data.
    FIGNAME = 'all_capdata_norm'
    YLABEL = 'nL/sec' # Label for y-axis.
    YLIM = 16 # Max y-value.
    XLIM = 12.5
    YMIN = 0
    
    FIGW = 5.5 # Figure width in inches
    FIGH = 3 # Figure height in inches
    BARWIDTH = 6
    BARNUM = 3


if DATA == 'gcpeakf':
    FNAME = 'peakf_means.txt'
    FIGNAME = 'paper_peakf'
    YLABEL = 'Peak %(' + r'$\Delta$' + 'F/F)'
    YMIN = 0
    YLIM = 80
    #YLIM = 100
    BARNUM = 5

if DATA == 'gcpeakfpool':
    FNAME = 'peakf_means.txt'
    FIGNAME = 'paper_peakf'
    YLABEL = 'Peak %(' + r'$\Delta$' + 'F/F)'
    YMIN = 0
    YLIM = 80
    

if DATA == 'gcarea648' or DATA == 'gcareapool':
    FNAME = 'area_means.txt'
    FIGNAME = 'paper_areagc'
    YLABEL = '%(' + r'$\Delta$' + 'F/F)-seconds' 
    YMIN = 0
    YLIM = 1000

if DATA == 'gcarea' or DATA == 'gcareapool':
    FNAME = 'area_means.txt'
    FIGNAME = 'paper_areagc'
    YLABEL = '%(' + r'$\Delta$' + 'F/F)-seconds' 
    YMIN = 0
    #YLIM = 800
    YLIM = 1000
    #YLIM = 1200
    YAXISTICKS = 4

if DATA == 'gcdur':
    FNAME = 'dur_means.txt'
    FIGNAME = 'paper_durgc'
    YLABEL = 'Time (s)' 
    YMIN = 0
    #YLIM = 20
    YLIM = 25
    YAXISTICKS = 5
    BARNUM = 5

if DATA == 'gcdurpool':
    FNAME = 'dur_means.txt'
    FIGNAME = 'paper_durgc'
    YLABEL = 'Time (s)' 
    #YMIN = 0
    YLIM = 25
    #YAXISTICKS = 4
    YAXISTICKS = 5
    

if DATA == 'gcdurwater':
    FNAME = 'dur_means.txt'
    FIGNAME = 'paper_durgcwater'
    YLABEL = 'Time (s)' 
    YMIN = 0
    YLIM = 15
    #YAXISTICKS = 4
    YAXISTICKS = 3
    BARNUM = 2
    FIGW = 0.8
    FIGH = 1

if DATA == 'gcpeakwater':
    FNAME = 'peakf_means.txt'
    FIGNAME = 'paper_peakf_water'
    YLABEL = 'Peak %(' + r'$\Delta$' + 'F/F)'
    YMIN = 0
    YLIM = 50
    YAXISTICKS = 5
    #YLIM = 100
    BARNUM = 2
    FIGW = 0.75
    FIGH = 1
    
if DATA == 'dyearea648':
    FNAME = 'dyearea_means.txt'
    FIGNAME = 'paper_dyearea'
    YLABEL = 'Normalized volume'
    YMIN = -0.002
    YLIM = 0.05
    YAXISTICKS = 4

if DATA == 'dyearea':
    FNAME = 'dyearea_means.txt'
    FIGNAME = 'paper_dyearea'
    YLABEL = 'Normalized\nvolume'
    YMIN = 0
    YLIM = 0.03
    #YLIM = 0.15
    #YLIM = 0.04
    YAXISTICKS = 4

if DATA == 'dyeareapool':
    FNAME = 'dyearea_means.txt'
    FIGNAME = 'paper_dyearea'
    YLABEL = 'Normalized volume'
    YMIN = -0.005
    YLIM = 0.16
    YAXISTICKS = 4

#FIGW = 1.5
FIGW = 2
FIGH = 1
BARWIDTH = 2

LINEWIDTH = 0.75


if True:
    multiplot(DATA, FNAME, KEYFILE, ERRORS, SAVEFIG, FIGNAME, YLIM, BORDER, YLABEL, FONTSIZE, FIGW, FIGH, FIGDPI, YAXISTICKS, YMIN, BARWIDTH, BARNUM, LINEWIDTH)
