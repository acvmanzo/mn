#! /usr/bin/env python

from mn.gof.poolcibarealib import *

#EXPTS = ['2011-0601_423_dtrpa1', '2011-0617_423_dtrpa1', '2011-0620_423_dtrpa1',
#'2011-0622_423_dtrpa1', '2011-0623_423_plus_dtrpa1', '2011-0624_423_plus_dtrpa1',
#'2011-0629_423_plus_dtrpa1']

#EXPTS = ['2011-0518_112648_dtrpa1', '2011-0527_112648_dtrpa1', '2011-0601_112648_plus_dtrpa1', '2011-0608_112648_plus_dtrpa1']

EXPTS = ['2011-0712_112204_dtrpa1_1copy', '2011-0714_112204_dtrpa1_1copy',
'2011-0715_112204_dtrpa1_1copy', '2011-0727_112204_dtrpa1_1copy']

KEYFILEMEAN = 'keylistmean'
KEYFILEDIFF = 'keylistdiff'
CIBAREAFOLD = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1/' +
'pooled_112204_dtrpa1_1copy/cibarea'



# Run from anywhere.
reanalyze(EXPTS)
makenewdir(CIBAREAFOLD)
os.chdir(CIBAREAFOLD)
poolcibdata(EXPTS, KEYFILEMEAN, KEYFILEDIFF)

    
