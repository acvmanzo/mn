import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import glob
import mn.plot.genplotlib as genplotlib
from mn.cmn.cmn import *
import math


def loadint(fname):
    data = np.loadtxt(fname, skiprows=1, usecols=(1,))
    
    ratio = data[0]/areadata[1]
    return(ratio)


def writeint(fname, summpath, summnotes):
    
    int = loadint(fname)
    
    pwd = os.getcwd()
    name = os.path.basename(pwd)
    
    if os.path.isfile(summpath) != True:
            with open(summpath, 'w') as f:
                f.write('Movie,IntRatio\n')
    
    with open(summpath, 'a') as f:
        f.write(name + ',' + str(area) + '\n')
    

def batch_writeint():
    #~ Start from data folder.
    
    pardir = makepardir_subexpt()
    makenewdir(os.path.join(pardir, 'summary'))
    summpath = os.path.join(pardir, 'summary', 'summ_int.txt')
    summnotes = os.path.join(pardir, 'summary_notes.txt')
    
    if os.path.exists(summpath) == True:
        os.remove(summpath)
    
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    for name in names:
        t = time.strftime('%H:%M:%S')
        print os.path.basename(name), t
        os.chdir(name)
        if os.path.exists('results1.txt') == False:
            continue
        writearea(RESULTSFILE, summpath, summnotes)
        
    with open(summpath, 'a') as f:
        with open(summnotes,'r') as g:
            g.next()
            for l in g:
                f.write(l)

def batch_writearea_3d2():
    #~ Start from data folder.
    
    pardir = makepardir_subexpt()
    makenewdir(os.path.join(pardir, 'summary'))
    summpath = os.path.join(pardir, 'summary', 'summ_area.txt')
    summnotes = os.path.join(pardir, 'summary_notes.txt')
    
    if os.path.exists(summpath) == True:
        os.remove(summpath)
    
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    for name in names:
        t = time.strftime('%H:%M:%S')
        print os.path.basename(name), t
        os.chdir(name)
        writearea_3d2(RESULTSFILE, summpath, summnotes)
        
    with open(summpath, 'a') as f:
        with open(summnotes,'r') as g:
            g.next()
            for l in g:
                f.write(l)

        
def combine_data():
    
    #with open(summdff) as f:
        #f.next()
        #for l in f:
            #name = l.split(',')[0]
            #date = name.split('_')[0]
            #fly = name.split(',')[3]
            #tastant = l.split(',')[1]
            
            #date = date.replace('-','')
            #flypicname = 'fly' + fly + '_' + date
    pardir = makepardir_subexpt()
    summareapath = os.path.join(pardir, 'summary', 'summ_area.txt')
    newsumm = os.path.join(pardir, 'summary', 'summ_area_reformatted.txt')

    if os.path.exists(newsumm) == True:
        os.remove(newsumm)
    

    with open(summareapath) as f:
        f.next()
        for l in f:
            name, area = l.split(',')
            print(name)
            if len(name.split('_')) == 3:
                fly, date, time = name.split('_')
            if len(name.split('_')) == 4:            
                genotype, fly, date, time = name.split('_')
            if len(name.split('_')) == 5:
                genotype, fly, dye, date, time = name.split('_')
            
            date = date.replace('2011', '2011-')
            fly = fly.replace('fly', '')
            
            with open(newsumm, 'a') as g:
                g.write(date + '_' + fly + ',' + str(area))
            




SUMMAREAPATH = '/home/andrea/Documents/lab/motor_neurons/imaging/112648/flypics/summary/summ_area.txt'
SUMMAREAPATH_3D2 = '/home/andrea/Documents/lab/motor_neurons/imaging/112648/flypics/summary/summ_area_3d2.txt'
RESULTSFILE = 'results1.txt'
SUMMAREANOTES = '/home/andrea/Documents/lab/motor_neurons/imaging/112648/flypics/summary_notes.txt'
DFF_SUMMFILE = '/home/andrea/Documents/lab/motor_neurons/imaging/112648/summary/summ_dff.txt'
NEWSUMMAREAPATH = '/home/andrea/Documents/lab/motor_neurons/imaging/112648/flypics/summary/summ_area_new.txt'

#~ with open(NEWSUMMAREAPATH) as f:
    #~ list = []
    #~ for l in f:
        #~ list =
