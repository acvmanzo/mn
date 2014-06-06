# For use with peaklib; contains the global variables that must be modified before using the 
#~ 'findphase' functions.

# These are parameters that must be modified while finding the max/min points in graphs.
# [maxsurr, maxwinlen, maxtrshift, minsurr, minwinlen, mintrshift]
# Positive trshift numbers bring the threshold closer to the max or min value



DROI = {'Mean1': [6, 1, 0, 6, 1, 0], 'Mean2': [6, 1, 0, 6, 1, 0]}



# Which points to compare and summary folder.

# Uncomment this part to calculate filling time.
#COMPARE = ['Mean1_dmax', 'Mean1_dmin'] 

#summfname = []
#for c in COMPARE:
    #comp = c.replace('Mean', '')
    #comp = comp.replace('_d', '')
    #summfname.append(comp)

#PHASEPARFOLD = 'summary_ph_{0}_{1}/'.format(summfname[0], summfname[1])
#PHASEPARFOLD_SL = 'summary_ph_{0}_{1}_sl/'.format(summfname[0], summfname[1])
#print(PHASEPARFOLD)

 #Uncomment this part to calculate emptying time.
#COMPARE = ['Mean1_dmin', 'Mean1_dmax'] 
#summfname = []
#for c in COMPARE:
    #comp = c.replace('Mean', '')
    #comp = comp.replace('_d', '')
    #summfname.append(comp)

#PHASEPARFOLD = 'summary_ph_{0}_{1}/'.format(summfname[0], summfname[1])
#PHASEPARFOLD_SL = 'summary_ph_{0}_{1}_sl/'.format(summfname[0], summfname[1])
#print(PHASEPARFOLD)


# The dictionary keys in the order of plotting.
#K = ['0% MC', '1.5% MC', '2% MC', '2.5% MC', '3% MC']
#~ K = ['423-GAL4', 'UAS-TNT', '423-GAL4 x UAS-TNT']

# Experiments to be pooled.
 
#EXPTS = ['/home/andrea/Documents/lab/motor_neurons/lof/2010-1130_tnt', '/home/andrea/Documents/lab/motor_neurons/lof/2010-1213_tnt']
 

