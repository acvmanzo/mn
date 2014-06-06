#! /usr/bin/env python

import os
import mn.cmn.cmn as cmn
import numpy as np

# Script for automatically opening roi.zip files and running multi-measure in ImageJ. Used when I 
#have previously specified the rois using the 'automeasure-roi only' script in imagej.

def measure(dname, wbrdir, dpardir):
    
    # Makes a list of the jpg files for one movie.
    jpgfiles = os.listdir(wbrdir)
    # Finds the number of jpg files for one movie.
    num = len(jpgfiles)
    files = sorted(jpgfiles)
    # Finds the first jpg file in one movie for use in opening with ImageJ. (CHANGED IN NEW 
    #IMAGEJ VERSION.
    #first = os.path.join(wbrdir, os.path.basename(files[0]))
    first = wbrdir + '/'
    #Specifies the roi path and the results file path.
    roifile = os.path.join(dpardir, dname, 'roi1.zip')
    resfile = os.path.join(dpardir, dname, 'ijresults1.txt')
    # Creates an argument for the above values which will be parsed by the imagej macro 
    #'roi_mm.txt'
    arg = str(num) + '%' + first + '%' + roifile + '%' + resfile
    
    cmd = 'java -jar /home/andrea/software/ImageJ/ij.jar -batch /home/andrea/software/ImageJ/macros/roi_mm.txt {0}'.format(arg)
    os.system(cmd)
    
    return(resfile)


def reformat(infile, outfile):
    
    mean1vals = []
    mean2vals = []

    with open(infile) as f:
        for l in f:
            val = l.strip('\n').split('\t')[1]
            mean1vals.append(val)
            f.next()
    
    with open(infile, 'r') as f:   
        f.next()
        for l in f:
            val = l.strip('\n').split('\t')[1]
            mean2vals.append(val)
            try:
                f.next()
            except(StopIteration):
                pass
            
    
    with open(outfile, 'w') as g:
        g.write(' \tMean1\tMean2\n')
        
        x = len(mean1vals)
        slices = np.linspace(1, x, x)
        slices = [int(x) for x in slices]
        #print(slices)
        
        for x in slices:
            g.write(str(x) + '\t' + mean1vals[x-1] + '\t' + mean2vals[x-1] + '\n')


def batch_measure():
        
    # Start from data folder.

    # Creates a list of movie directories in the data folder.
    dnames = sorted((os.listdir('.')))
    dpardir = os.path.abspath('.')

    # Creates a list of movie directories in the wbr folder.
    pardir = cmn.makepardir_subexpt()
    wbrpardir = pardir+'/'+os.path.basename(pardir)+'_wbr/'

    for dname in dnames:
        print(dname)
        
        wbrdir = os.path.join(wbrpardir, dname)
        resfile = measure(dname, wbrdir, dpardir)
                
        formresfile = os.path.join(dpardir, dname, 'results1.txt')
        reformat(resfile, formresfile)

if True:
    batch_measure()
