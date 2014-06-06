# This module defines functions used for generating 'params' files for use in the dftf module. 
# It extracts values from a summary text file and generates the 'params' file using those values. 
# It is referenced by the executable file 'genparams.py'.
#
# The summary text file should have this format (including the headings):
# Movie Frame1  Frame_end   Condition   Comments
# movie name    #   #   string  string
#
# Missing values should be replaced with 'x'.
#
# The resulting params files will have this format:
# f1 = xx
# f2 = xx
# fps = xx
# f_end = xx
# sample_length = xx
# condition = xx
#
# f1 = first frame to use for the dft analysis
# f2 = last frame to use for the dft analysis
# fps = movie sampling rate
# f_end = last good frame for good view of proboscis (f1 to f_end defines a stretch of the movie 
# where proboscis can be easily observed)
# sample_length = # frames used for the dft analysis (should be the same for each movie)
# condition = specific parameter that is being varied in the experiment (ex., 24h or 48h, 100 mM 
# sucrose or 50 mM sucrose)



import os
import sys
import numpy as np

def var_str(name, value):
    return name + ',' + value + '\n'


#def paramspatth(movie, fdir='.'):
    #fname = 'r180_r_AviTest' + movie + '-0000'
    #fpath = os.path.join(os.path.dirname(os.path.abspath('.')), 'data', fname)
    #return(fpath)

def testf(fname):
    """ Extracts Frame1 and Frame2 from the summary text file and prints out the number of good 
    frames. """
    
    for l in open(fname):
        
        name = l.split()[0]
        f1 = (l.split()[1])
        fend = (l.split()[2])
        
        if f1 != 'x' and f1 != 'Frame1':
            f1 = int(f1)
            fend = int(fend)
            print(name, fend-f1)


def tfp(fname):
    """ Extracts Frame1 and Frame2 from the summary text file and prints out the number of good 
    frames. Returns a list of the frame lengths."""
    
    a = []
    for l in open(fname):
        
        name = l.split(',')[0]
        f1 = (l.split(',')[1])
        fend = (l.split(',')[2])
        
        if f1 != 'x' and f1 != 'Frame1':
            f1 = int(f1)
            fend = int(fend)
            print(name, fend-f1)
            a.append(fend-f1)
    return(a)


def genp(fname, fps, cutoff):
    """ Generates params files. Reads values from a summary text file and writes them to the 
    params file. Missing values should be replaced with 'x'.  
    
    fname = name of the summary file
    fps = frames per second for each movie
    cutoff = number of good frames to use for dft analysis
    """
    
    d = open(fname)
    d.next()
    
    for l in d:
        
        name = l.split(',')[0].replace('.fmf', '')
        f1 = l.split(',')[1]
        fend = l.split(',')[2]
        condition = l.split(',')[3].rstrip('\n')
        fps = str(fps)
        cutoff = str(cutoff)
        hzshift = str(hzshift)
        
                        
        if f1 != 'x' and f1 != '' and f1 != 'Frame1':
            print(name, int(fend)-int(f1))
            
            if int(fend)-int(f1) >= int(cutoff):
                f2 = str(int(f1)+int(cutoff))
                print('Saved')
                f = open(os.path.join('data', name, 'params'), 'w')
                f.write(var_str('f1', f1))
                f.write(var_str('f2', f2))
                f.write(var_str('fps', fps))
                f.write(var_str('condition', condition))
                f.write(var_str('f_end', fend))
                f.write(var_str('sample_length', cutoff))
                

def genpgf(fname, fps):
    """ Generates params files. Reads values from the summary text file 'fname' and writes them to the 
    params file. Missing values should be replaced with 'x'.  
    
    fps = sample rate of the movies
    
    Note that this function is for generating parameters for use in analyzing and plotting data 
    from gain of function experiments.
    
    """
    
    d = open(fname)
    d.next()
    
    for l in d:
        
        name = l.split(',')[0].rstrip('.fmf')
        f1 = l.split(',')[1]
        fend = l.split(',')[2]
        condition = l.split(',')[3].rstrip('\n')
        cib = l.split(',')[4]
        
        fps = str(fps)
                
        if f1 != 'x':
            print name, int(fend)-int(f1)
                
            f = open(os.path.join('data', name, 'params'), 'w')
            f.write(var_str('f1', f1))
            f.write(var_str('f2', fend))
            f.write(var_str('f_end', fend))
            f.write(var_str('fps', fps))
            f.write(var_str('condition', condition))
            f.write(var_str('cib open?', cib))


def makenewdir(newdir):
    """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""
    
    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.errno == 17:
            pass  
        
        
def genplfc(fname, fps, cutoff):
    """Generates params files for loss of function experiments where information about the 
    capmovie is written in the info file.  Order of columns should be moviename, frame1, 
    frame_end, duration, capillary movie 1, capillary  movie 2, condition"""
    
    d = open(fname)
    d.next()
        
    for l in d:
        newline = []
        
        for x in l.split(','):
            newline.append(x.rstrip('.fmf\n'))
        
              
        name, f1, fend, duration, capmovie1, capmovie2, condition = newline[0:7]
        print(name)
        paramsfile = os.path.join('data', name, 'params')
        if os.path.exists(paramsfile) == True:
            print('Removing old params file')
            os.remove(paramsfile)
        if f1 != 'x' and f1 != '':
            print name, int(fend)-int(f1)
            
            if int(fend)-int(f1) >= int(cutoff):
                f2 = str(int(f1)+int(cutoff))
                fps = str(fps)
                cutoff = str(cutoff)
                print('Saved')
        
                makenewdir(os.path.join('data', name))
                f = open(os.path.join('data', name, 'params'), 'w')
                f.write(var_str('f1', f1))
                f.write(var_str('f2', f2))
                f.write(var_str('fps', fps))
                f.write(var_str('condition', condition))
                f.write(var_str('f_end', fend))
                f.write(var_str('sample_length', cutoff))
                f.write(var_str('capmovie1', capmovie1))
                f.write(var_str('capmovie2', capmovie2))
                f.write(var_str('duration', duration))
        
            
            
def gencapparams(fname):
    """Fname is the name of a text file containing the capparams data for each movie."""
    d = open(fname)
    d.next()
    
    for l in d:
        newline = []
        
        for x in l.split(','):
            newline.append(x.rstrip('.fmf'))
        
              
        name, f1, fend, duration, capmovie1, capmovie2, condition = newline[0:7]
        print name
        
        capparamsfile = os.path.join('data', name, 'capparams')
        if os.path.exists(capparamsfile) == True:
            print('Removing old params file')
            os.remove(capparamsfile)
                
        if capmovie1 != 'x' and capmovie1 !='' and capmovie2 != 'x' and capmovie2 != '' and duration != 'x' and duration != '':

            makenewdir(os.path.join('data', name))
            f = open(capparamsfile, 'w')
            
            f.write(var_str('name', name))
            f.write(var_str('capmovie1', capmovie1))
            f.write(var_str('capmovie2', capmovie2))
            f.write(var_str('duration', duration))
            f.write(var_str('condition', condition))
            print('Saved')

def genplfcapctrl(fname):
    d = open(fname)
    d.next()
    
    for l in d:
        newline = []
        
        for x in l.split(','):
            newline.append(x.rstrip('.fmf'))
        
              
        name, condition = newline 
            
        print name
        print('Saved')
        makenewdir(os.path.join('data_cap_ctrl', name))
        f = open(os.path.join('data_cap_ctrl', name, 'capparams'), 'w')
        
        f.write(var_str('name', name))
        f.write(var_str('condition', condition))


def genpdframes(fname, fps):
    """Generates files that contain the frame numbers for phaselib.py."""
    
    with open(fname) as d:
        d.next()
        for l in d:
            
            
            name = l.split(',')[0].replace('.fmf', '')
            print(name)
            f1 = l.split(',')[1]
            fend = l.split(',')[2]
            condition = l.split(',')[6].rstrip('\n')
            fps = str(fps)            
                          
            pdframesfile = os.path.join('data', name, 'pdframes')
            if os.path.exists(pdframesfile) == True:
                print('Removing old pdframes file')
                os.remove(pdframesfile)
                                
            if f1 != 'x' and f1 != 'Frame1':
                try:
                    f = open(os.path.join(pdframesfile), 'w')
                    f.write(var_str('f1', f1))
                    f.write(var_str('f_end', fend))
                    f.write(var_str('fps', fps))
                    f.write(var_str('condition', condition))
                except IOError as e:
                    if e.errno == 2:
                        continue

def genpdframes2(fname, fps, sample_length):
    """Generates files that contain the frame numbers for phaselib.py."""
    
    with open(fname) as d:
        d.next()
        for l in d:
            
            
            name = l.split(',')[0].replace('.fmf', '')
            print(name)
            f1 = l.split(',')[1]
            fend = l.split(',')[2]
            condition = l.split(',')[6].rstrip('\n')
            fps = str(fps)            
                          
            pdframesfile = os.path.join('data', name, 'pdframes')
            if os.path.exists(pdframesfile) == True:
                print('Removing old pdframes file')
                os.remove(pdframesfile)
                                
            if f1 != 'x' and f1 != '' and f1 != 'Frame1':
                f2 = str(int(f1) + sample_length)
                try:
                    f = open(os.path.join(pdframesfile), 'w')
                    f.write(var_str('f1', f1))
                    f.write(var_str('f_end', f2))
                    f.write(var_str('fps', fps))
                    f.write(var_str('condition', condition))
                except IOError as e:
                    if e.errno == 2:
                        continue

def gencibareaframes(fname, fps):
    """Generates files that contain the frame numbers for phaselib.py."""
    
    with open(fname) as d:
        d.next()
        for l in d:
            name = l.split(',')[0].replace('.fmf', '')
            duration = l.split(',')[1]
            condition = l.split(',')[2].rstrip('\n')
            fps = str(fps)            
                            
            makenewdir(os.path.join('data', name))
            f = open(os.path.join('data', name, 'cibareaparams'), 'w')
            f.write(var_str('duration', duration))
            f.write(var_str('fps', fps))
            f.write(var_str('condition', condition))


def gengcampparams(fname):
    
    tastes = {'Sd': '1 M sucrose', '100Sd': '100 mM sucrose', 'Cd': '100 mM caffeine', 'Wd': 
    'Water', 'Wdt': 'Water - deprived', '2Sd': '2 M sucrose'}
    
    with open(fname) as d:
        d.next()
        for l in d:
            name = l.split(',')[0]
            t = name.split('_')[5]
            print(t)
            tastant = tastes[t]
            
            fps = l.split(',')[1]
            n = l.split(',')[2]
            z = l.split(',')[3]           
                        
            makenewdir(os.path.join('data', name))
            print(os.path.join('data', name, 'params'))
            f = open(os.path.join('data', name, 'params'), 'w')
            f.write(var_str('name', name))
            f.write(var_str('tastant', tastant))
            f.write(var_str('fps', fps))
            f.write(var_str('neurons', n))
            f.write(var_str('zmotion', z))


def gengcampparamswater(fname):
    
    tastes = {'Wd': 'not deprived', 'Wdt':'water deprived'}
    
    with open(fname) as d:
        d.next()
        for l in d:
            name = l.split(',')[0]
            t = name.split('_')[5]
            print(t)
            tastant = tastes[t]
            
            fps = l.split(',')[1]
            n = l.split(',')[2]
            z = l.split(',')[3]           
                        
            makenewdir(os.path.join('data', name))
            print(os.path.join('data', name, 'params'))
            f = open(os.path.join('data', name, 'params'), 'w')
            f.write(var_str('name', name))
            f.write(var_str('tastant', tastant))
            f.write(var_str('fps', fps))
            f.write(var_str('neurons', n))
            f.write(var_str('zmotion', z))


           
def gengc_freqparams(fname):
    tastes = {'Sd': '1 M sucrose', '100Sd': '100 mM sucrose', 'Cd': '100 mM caffeine', 'Wd': 
    'Water', '2Sd': '2 M sucrose'}
    
    with open(fname) as d:
        d.next()
        for l in d:
            name = l.split(',')[0]
            t = name.split('_')[5]
            condition = tastes[t]
            fps = float(l.split(',')[1])
            f1 = str(int(np.floor(8*fps)))
            f2 = str(int(np.floor(39*fps)))
            fend = str(int(np.ceil(40*fps)))
            cutoff = str(int(np.floor(39*fps)))
            capmovie1 = 'x'
            capmovie2 = 'x'
            duration = str(int(np.floor(40*fps)))
            fps = str(fps)
                        
            makenewdir(os.path.join('data', name))
            print(os.path.join('data', name, 'params'))
            f = open(os.path.join('data', name, 'params'), 'w')
            f.write(var_str('f1', f1))
            f.write(var_str('f2', f2))
            f.write(var_str('fps', fps))
            f.write(var_str('condition', condition))
            f.write(var_str('f_end', fend))
            f.write(var_str('sample_length', cutoff))
            f.write(var_str('capmovie1', capmovie1))
            f.write(var_str('capmovie2', capmovie2))
            f.write(var_str('duration', duration))


                
#if True:
    #fname='2010-1201_113990_tnt_frames.txt'
    #fps=60
    #genpdframes(fname, fps)


#if True:
    #import glob
    #import shutil
    
    #names=glob.glob('*')
    #names = sorted([os.path.abspath(name) for name in names])

    #newpath='/home/andrea/Documents/lab/motor_neurons/lof/2010-1130_tnt/old-frames/frames'
    
    #for i, name in enumerate(names):
        #os.chdir(name)
        
        #newname = newpath + str(i)
        #print(name)
        #print(newname)
        #try:
            #shutil.move('frames', newname)
        #except IOError as e:
            #if e.errno == 17:
                #pass
