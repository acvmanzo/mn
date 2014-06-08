import os
import shutil
import glob
import numpy as np
import matplotlib.pyplot as plt
import mn.plot.genplotlib as gp
from mn.cmn.cmn import *

def capmovielist(fname):
    """Generates a list of the movies that have pictures of the capillary 
    tube during feeding experiments.
    
    First, take the column marked "Capillary" from the notes file and save it
    as a comma-separated text file. Then run the function on that file.
    """
    
    f = open(fname)
    #f.next()
    
    capnames1 = []
    for l in f:
        capnames1.extend(l.split(','))
    
    capnames2 = []
    for l in capnames1:
        capnames2.append(l.strip(' \n'))
    
    capnames2 = filter(None, capnames2)
    capnames2 = list(set(capnames2))
    
    return(capnames2)


def mvcapmovies(capmovlist, capdirname='capfmfs', fdir='.'):
    """Moves movies in capmovielist to a new directory. If run from the
    directory experiment/fmfs, will put in the directory experiment/capfmfs."""
    
    capmovlistl = []
    for i in capmovlist:
        #Converts names to lowercase in case of typos.
        capmovlistl.append(i.lower())
    
    dirlist = os.listdir(fdir)

    capmovdir = os.path.join(os.path.dirname(os.path.abspath(fdir)), capdirname)
    makenewdir(capmovdir)
    
    for i in capmovlistl:
        print(i)
        try:
            shutil.move(i, capmovdir)
        except shutil.Error:
            pass
        except IOError:
            pass
        
        #try: 
            #shutil.move(i, capmovdir)
        #except: 
            #continue
        

    return(sorted(capmovlist) == sorted(os.listdir(capmovdir)))
    


def batchfiles(fdir='.'):
    """Generates a list of the absolute paths of all files in directory fdir.
    """
    
    os.chdir(fdir)
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories 
    # in fn_name.
    names = sorted([os.path.abspath(name) for name in names])
    return(names)


class CapMovieData:
    def __init__(self, capparamsfile):
        self.capparamsfile = capparamsfile
    
    def Readdata(self):
        """Returns a dictionary containing the info in the capparams file."""
        
        d = {}
        f = open(self.capparamsfile)
        
        for l in open(self.capparamsfile):
            try: 
                d[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
                
            except IndexError:
                pass
        try:        
            d['duration'] = int(d['duration'])
        except ValueError:
            pass
        return(d)
        
        
            
    
def deltalength(dict, fname='results1.txt', fdir='.'):
    """Finds the difference in length in the capillary liquid between two
    capillary images.  Returns the results in a dictionary.
    
    'dict' is a dictionary containing the info in the capparams file
    'fname' is the name of the results file generated in ImageJ.
    'fdir' should be the directory containing the capparams file (data/movie)
    """
    
    l = [1, 2]
    
    for n in l:
        #The results files for the length of the capillary liquid are in 
        #movie folders in the 
        #experiment/data_cap folder. For each capmovie (capmovie1 and 
        #capmovie2), this line specifies the path to the appropriate 
        #data_cap/movie/results1.txt file.
        moviepath = os.path.join(os.path.dirname(os.path.abspath(fdir)) + '_cap', dict['capmovie'+str(n)])
        movieres = os.path.join(moviepath, fname)
        
        #Opens the results file and loads data into two lists, label and data.
        f = open(movieres)
        label = f.next().split()
        data = f.next().split()
        f.close()
        
        # Finds the column with the Length measurement and adds that to the dictionary.
        i = label.index('Length')
        key = 'length{0}'.format(n)
        dict[key] = data[i+1]

    # Finds the difference in length between the two capillary measurements.
    dict['difflength'] = float(dict['length1']) - float(dict['length2'])
    
    return(dict)


def pixpersec(dict):
    """Converts pixels per frame to pixels per second."""
    
    pixperframe = dict['difflength']/dict['duration']
    pixpersec = pixperframe*60
    
    dict['pixpersec'] = pixpersec
    return(dict)
    

def nlpersec(dict, r=0.247, c=93.67):
    """Converts pixels per second to nL per second.
    
    r = radius of the capillary tube.
    c = pixels/mm?
    """
    
    nlpersec = np.pi * np.square(r) * dict['pixpersec'] * 1000 / c
    
    dict['nlpersec'] = nlpersec
    return(dict)
      
    
    

#~ def makenewdir(newdir):
    #~ """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""
    #~ 
    #~ try:
        #~ os.makedirs(newdir)
    #~ except OSError as e:
        #~ if e.errno == 17:
            #~ pass  


def deloldsummfile(summfile, fdir):
    """Deletes an old summary file; fdir should be the 'data' folder"""
    
    summfilename = os.path.join(os.path.dirname(os.path.abspath(fdir)), 'summary', summfile)

    if os.path.exists(summfilename) == True:
        os.remove(summfilename)


def writedata(dict, capdatafile, fdir='.'):
    """Writes the difference in capillary liquid length to the summary file 'capdata.txt' 
    located in the summary folder. 
    
    Dict is dictionary with length differences included.
    'fdir' is the data/movie folder.
    """
    
    exptpath = os.path.dirname(os.path.dirname(os.path.abspath(fdir)))
    summfold = os.path.join(exptpath, 'summary')
    makenewdir(summfold)
    
    outfile = os.path.join(summfold, capdatafile)
    
    
    if os.path.isfile(outfile) != True:
        f = open(outfile, 'w')
        f.write('Movie' + ',' + 'Delta cap length' + ',' + 'Duration' + ',' + 'Pixpersec' + ',' +
        'nLpersec' + ',' + 'Condition' + '\n')
        f.close()
    
    
    f = open(outfile, 'a')
    f.write(dict['name'] + ',' + str(dict['difflength']) + ',' + str(dict['duration']) + ',' + 
    str(dict['pixpersec']) + ',' + str(dict['nlpersec']) + ',' + dict['condition'] + '\n')
    f.close() 



def gencapdata(capdatafile, fdir):
    """Writes the caplength data into the summary file if certain conditions exist."""
    
    os.chdir(fdir)
    if os.path.exists('capparams') != True:
        print('No capparams file')
    if os.path.exists('results1.txt') != True:
        print('No results file')

    if os.path.exists('capparams') == True and os.path.exists('results1.txt') == True:
        lobj = CapMovieData('capparams')
        d = lobj.Readdata()
    
        d_length = deltalength(d)
        d_pixpersec = pixpersec(d_length)
        d_nlpersec = nlpersec(d_pixpersec)
        if d_nlpersec < 0:
            raise('Negative consumption')
        writedata(d_nlpersec, capdatafile)
    


def capctrl(fdir='.'):
    
    os.chdir(fdir)
    if os.path.exists('results1.txt') == True:
        f = open('results1.txt')
        f.next()
        l = f.next().split()
        length = l[4]
        f.close()
        
        g = open('capparams')
        l = g.next().split(',')
        name = l[1].strip('\n')
        j = g.next().split(',')
        condition=j[1].strip('\n')
       
        g.close()
        
        exptpath = os.path.dirname(os.path.dirname(os.path.abspath(fdir)))
        summfold = os.path.join(exptpath, 'summary_cap_ctrl')
        makenewdir(summfold)
        outfile = os.path.join(summfold, 'capctrllengths.txt')
        
        if os.path.isfile(outfile) != True:
            m = open(outfile, 'w')
            m.write('Movie' + ',' + 'Condition' + ',' + 'Length' + '\n')
            m.close()       
        n = open(outfile, 'a')
        n.write('{0},{1},{2},\n'.format(name, condition, length))
        n.close() 


def gendictpps(fname):
    """Generates a dictionary with the pixelpersec values from the capdata file."""
        
    data_dict = {}
    f = open(fname)
    f.next()
    
    for l in f:
        name, deltalstr, durationstr, pixpersecstr, nlpersecstr, condition = map(str.strip, l.split(','))
        
        pixpersec = float(pixpersecstr)
                
        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(pixpersec)
    
    return(data_dict)


def gendictnps(fname='capdata.txt'):
    """Generates a dictionary with the nlpersecond values from the capdata file.
    """ 
    
    data_dict = {}
    f = open(fname)
    f.next()
    
    for l in f:
        name, deltalstr, durationstr, pixpersecstr, nlpersecstr, condition = map(str.strip, l.split(','))
        
        nlpersec = float(nlpersecstr)
                

        if condition not in data_dict:
            data_dict[condition] = []

        data_dict[condition].append(nlpersec)
    
    return(data_dict)




def genlist(dict, label='data'):
    """Generates a new dictionary in which the keywords are conditions and the values are lists of 
    the mean flowrate, standard deviation, standard error, and n for that condition.
    """
    
    mean_dict = {}
    
    for condition, value in dict.iteritems():
        meanval = np.mean(value)
        stdev = np.std(value)
        n = len(value)
        sterr = stdev/np.sqrt(n)
        
        if condition not in mean_dict:
            mean_dict[condition] = []
        
        mean_dict[condition].append(meanval)
        mean_dict[condition].append(stdev)
        mean_dict[condition].append(sterr)
        mean_dict[condition].append(n)
        mean_dict[condition].append('{0}'.format(label))
    
    return(mean_dict)


def genalldict(fname='capdata.txt'):
    d = gendictpps()
    md = genlist(d)
    return(d, md)

def plotpixpersec(capfile, k):
    """capfile is the summary file, k is the keylist"""
    
    p = gendictpps(capfile)
    mp = genlist(p)
    gp.plotdata(p, mp, k, 's', 'pix/sec', 'Amount consumed \n pixels/sec', 
            ylim=10, titlesize='x-large', xlabelsize='medium', xstart=0.25)
    plt.savefig('cap_pixpersec')
    plt.close()

def plotnlpersec(capfile, l):
    """capfile is the summary file, l is the keylist"""
    
    n = gendictnps(capfile)
    mn = genlist(n)
    
    o = []
    for i, v in n.iteritems():
        o.append(max(v))

    print(max(o))
    
    gp.plotdata(n, mn, l, 's', 'nL/sec', 'Amount consumed', 
            ylim=max(o)+0.3*max(o), titlesize='x-large', xlabelsize='medium',
            xstart=0.25)
    plt.savefig('cap_nlpersec')
    
    plt.figure()
    gp.plotdata(n, mn, l, 'b', 'nL/sec', 'Amount consumed', 
            ylim=max(o)+0.3*max(o), titlesize='x-large', xlabelsize='medium',
            xstart=0.25)
    plt.savefig('cap_nlpersec_bar')
    
    #plt.show()


def checkcapmovies(fname, gname):
    """Fname is the frames text file and gname is the output file of the list of movies with incorrect capmovies."""

    with open(gname, 'w') as f:
        f.write('Movies whose capmovies have incorrect time stamps\n')

    with open(fname) as d:
        d.next()
            
        for l in d:
            newline = []
            
            for x in l.split(','):
                newline.append(x.rstrip('.fmf'))
            
                  
            name, f1, fend, duration, capmovie1, capmovie2, condition = newline[0:7]
            
            print(name)
            
            if capmovie1 != 'x' and capmovie1 != '' and capmovie2 != 'x' and capmovie2 !='':
                timemov = float(name.split('_')[2])
                timecap1 = float(capmovie1.split('_')[2])
                timecap2 = float(capmovie2.split('_')[2])
                
                if timecap1 > timemov or timecap2 < timemov:
                    
                    with open(gname, 'a') as f:
                        f.write(name + '\n')
                


def checkcapmovies2(fname, gname):
    """Fname is the frames text file and gname is the output file of the list of movies with incorrect capmovies."""

    times = []
    
    with open(gname, 'w') as f:
        f.write('Movies whose capmovies have incorrect time stamps\n')

    with open(fname) as d:
        d.next()
            
        for l in d:
            newline = []
            
            for x in l.split(','):
                newline.append(x.rstrip('.fmf'))
            
                  
            name, f1, fend, duration, capmovie1, capmovie2, condition = newline[0:7]
            
            print(name)
            if capmovie1 != 'x' and capmovie1 != '' and capmovie2 != 'x' and capmovie2 !='':
                timemov = float(name.split('_')[2])
                timecap1 = float(capmovie1.split('_')[2])
                timecap2 = float(capmovie2.split('_')[2])
                
                times.append(timecap1)
                times.append(timemov)
                times.append(timecap2)
        
        stimes = sorted(times)
        print(stimes == times)
