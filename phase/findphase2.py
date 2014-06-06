#! /usr/bin/env python

from mn.phase.peaklib import *

def gotodatamovie(movie):
    path = os.path.join(EXPT, 'data', movie)
    os.chdir(path)

def gotoifilesmovie(movie):
    path = os.path.join(EXPT, 'phase_analysis/ifiles', movie)
    os.chdir(path)

EXPT = '/home/andrea/Documents/lab/motor_neurons/lof/2011-0313_112204_tnt_180f/'
#EXPT = '/home/andrea/Documents/lab/motor_neurons/lof/2011-0329_423_tnt/'

# maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift
# positive trshift numbers bring the threshold closer to the max or min value; a mulitiple of the sd
# default DROI = {'Mean1': [6, 1, 0, 6, 1, 0], 'Mean2': [6, 1, 0, 6, 1, 0]}

MOVIE = 'mov_20110313_181240'
LOCAL = {'Mean1': [6, 1, 0, 6, 1, -1]}
DICTREMOVE = {'Mean1_dmin': [188]}

printorsave = sys.argv[1]


gotodatamovie(MOVIE)
checkmaxmin_manual(LOCAL) # Run from data/movie folder.
print(LOCAL)
#If it looks ok, everything is fine, no need to proceed.


#Run from the ifiles/movie folder. Specifies the points to remove.
#Doesn't actually remove anything from the file.
#Enter 'yes' to print traces, 'no' to generate dictionary.

gotoifilesmovie(MOVIE)
d = removepoints_dict(PICKLEFNAME, DICTREMOVE, printorsave)

###Once satisfied with the trace, uncomment line below to permanently change file.

if printorsave == 'save':
    print('Saving pickle file')
    savepicklefile(d, FRAMES, PICKLEFNAME, PICKLEFNAME)
    checkmaxmin_pickle(PICKLEFNAME)
    


