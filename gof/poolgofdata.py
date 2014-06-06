

import os
import shutil
import mn.plot.genplotlib as gpl
import matplotlib.pyplot as plt
from mn.gof.gfplot import *
import mn.cmn.cmn as cmn

# Experiments that need to be pooled.
EXPTS = ['2011-0518_112648_dtrpa1', '2011-0527_112648_dtrpa1', '2011-0601_112648_plus_dtrpa1', 
'2011-0608_112648_plus_dtrpa1'] 

#EXPTS = ['2011-0601_423_dtrpa1', '2011-0617_423_dtrpa1', '2011-0620_423_dtrpa1', '2011-0622_423_dtrpa1', 
#'2011-0623_423_plus_dtrpa1', '2011-0624_423_plus_dtrpa1', '2011-0629_423_plus_dtrpa1']

#EXPTS = ['2011-0712_112204_dtrpa1_1copy', '2011-0714_112204_dtrpa1_1copy', 
#'2011-0715_112204_dtrpa1_1copy', '2011-0727_112204_dtrpa1_1copy', '2011-0801_112204_dtrpa1_1copy']

#EXPTS = ['pooled_112648_dtrpa1', 'pooled_112204_dtrpa1_1copy', 'pooled_423_dtrpa1']

def poolgenotypedata():
    #Pool cibdata and pumping results. Run from the folder where pooled data will be put.
    dtrpa1f = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1'
    p_cibpump = 'pooled_cibpump.txt'  
        
    if os.path.exists(p_cibpump) == True:
        os.remove(p_cibpump)
       
    for expt in EXPTS:
        cibpumpfile = dtrpa1f + '/{0}/cib_pumps.txt'.format(expt)
        with open(cibpumpfile) as f:
            f.next()
            
            if os.path.exists(p_cibpump)!=True:
                with open(p_cibpump, 'w') as g:
                    g.write('Movie,F1,F2,Condition,Cib open?,pumps,\n')
            
            with open(p_cibpump, 'a') as g:
                for l in f:
                    g.write(l)
    
    # Plot graphs.
    plotandsavegof(fname='pooled_cibpump.txt', ylimpump=100)


def poolalldata():
    # Run from gof/dtrpa1 folder.
    
    dtrpa1f = os.path.abspath('.')
    p_cibpump = os.path.join(dtrpa1f, 'pooled_all', 'pumps', 'pooled_all_cibpump.txt')
    
    if os.path.exists(p_cibpump) == True:
        os.remove(p_cibpump)
       
    for expt in EXPTS:
        cibpumpfile = os.path.join(dtrpa1f, expt, 'pooled_cibpump.txt')
        with open(cibpumpfile) as f:
            f.next()
            
            if os.path.exists(p_cibpump)!=True:
                with open(p_cibpump, 'w') as g:
                    g.write('Movie,F1,F2,Condition,Cib open?,pumps,\n')
            
            with open(p_cibpump, 'a') as g:
                for l in f:
                    g.write(l)


if True:
    poolgenotypedata()
