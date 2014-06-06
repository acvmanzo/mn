#! /usr/bin/env python

from mn.phase.peaklib import *
print('first argument replot ifiles')
replot = sys.argv[1]



try:
    
    #~ #From ifiles folder:
    keyfile = os.path.join(makepardir_data(), KEYLIST)
    #~ keyfile = os.path.join(makepardir_subexpt(), KEYLIST)
    K = load_keys(keyfile)
    
    print('Copying frequency data')
    ifiles = os.getcwd()
    os.chdir('../../summary')
    copyfreqdata(PEAKF)
    os.chdir(ifiles)
    
    if replot == 'replot':
        print('Rewriting ifiles and replotting ifile plots')
        b_checkmaxmin_pickle(PICKLEFNAME)
        os.chdir('../')
        #print('Plotting min/max traces')
        #b_plotminmaxtimes()
        
        
    
    print('Generating summary files')
    b_writedeltaavgs()
    os.chdir('../../../'+PHASEPARFOLD)
    print('Generating plots')
    print(K)
    plotallplots(SUMMFILE, K)


except OSError:
    raise
