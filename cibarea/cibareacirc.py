import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import mn.plot.genplotlib as genplotlib


class CibData:
    
    def __init__(self, paramsfile, resultsfile):
        self.paramsfile = paramsfile
        self.resultsfile = resultsfile
    
    def Gendata(self):
        d = {}           
        
        d['moviename'] = os.path.basename(os.path.abspath('.'))
        if os.path.exists(self.paramsfile) == True:
            for l in open(self.paramsfile):
                d[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
            
            d['fps'] = int(d['fps'])

        
        if os.path.exists(self.resultsfile) == True:
            d['frac'] = findfraction(self.resultsfile)
        
        return(d)
    
    

def loadresultsfile(fname):
    """Returns a numpy array from data in the ImageJ-generated file 'fname', which is a text file 
    containing the Mean ROI intensity for each frame of an image sequence.
    
    This function is meant to be used with a file generated by the ImageJ function "multimeasure", 
    usually with the ImageJ custom macro "automeasure.txt".
    """
    
    return(np.loadtxt(fname, skiprows=1, usecols=(1,3,4)))
    
    #for x in a:
        #return(np.loadtxt(fname, skiprows=1, usecols=(1,)))

def findfraction(resultsfile):

    data = loadresultsfile(resultsfile)

    d={}
    
    
    for datum in data:
        area, slice, len = datum
        print area, slice, len
        slicestr = str(slice)
        
        if slicestr not in d:
            d[slicestr] = []
        
            a ={}
            a['area'] = []
            a['length'] = []
            
        if len == 0:
            a['area'].append(area)
        if len != 0:
            a['length'].append(len)

        d[slicestr] = a

        print(d)
        
    fraction = []
    for slice, value in d.iteritems():
        f = value['area'][0]/value['length'][0]
        fraction.append(f)

    return(np.mean(fraction))


def batchfiles(fdir='.'):
    """Carries out the function 'fn_name' recursively on all files in the directory 'fdir'.
    """
    
    os.chdir(fdir)
    names = glob.iglob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = sorted([os.path.abspath(name) for name in names])
    return(names)

def makenewdir(newdir):
    """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""
    
    try:
        os.makedirs(newdir)
    except OSError as e:
        if e.errno == 17:
            pass  

def genresfile_moviefolder():
    resdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'summary')
    makenewdir(resdir)
    resfile = os.path.join(resdir, 'cibresults.txt')
    return(resfile)
    
def genresfile_datafolder():
    resdir = os.path.join(os.path.dirname(os.path.abspath('.')), 'summary')
    makenewdir(resdir)
    resfile = os.path.join(resdir, 'cibresults.txt')
    return(resfile)


def writeresults(dict):
            
    resfile = genresfile_moviefolder()
    
    if os.path.isfile(resfile) != True:
        f = open(resfile, 'w')
        f.write('Movie' + ',' + 'NormCibArea,Condition' + '\n')
        f.close()
    
    f = open(resfile, 'a')
    try:
        fracstr = str(dict['frac'])
        f.write(dict['moviename'] + ',' + fracstr + ',' + dict['condition'] + '\n')
     
    except KeyError:
        pass
    
    f.close()    

    



#PARAMS_FILE = 'cibareaparams'
PARAMS_FILE = 'params'
RESULTS_FILE = 'results1.txt'


x = genresfile_datafolder()
if os.path.exists(x) == True:
    os.remove(x)

names = batchfiles('.')
for name in names:
    print os.path.basename(name)
    os.chdir(name)
    params = CibData(PARAMS_FILE, RESULTS_FILE)
    cibdict = params.Gendata()
    writeresults(cibdict)

os.chdir('../../summary')
d = genplotlib.gendict_cibarea_circ('cibresults.txt')
md = genplotlib.genlist(d)
k = d.keys()
genplotlib.plotdata(d, md, k, 'b', 'NormCibArea', 'Fraction of cibarium open', ymin=0, ylim=100)
plt.savefig('cibareacirc')

#plt.figure()
#e = genplotlib.gendict_cibarea_dur('cibresults.txt')
#me = genplotlib.genlist(e)
#genplotlib.plotdata(e, me, k, 'b', 'Duration', 'Duration of Drinking', ymin=0, ylim=200)
#plt.savefig('duration')


    #try:
        #a = 
        #f = findfraction()
        #list.append(f)
    #except IOError as e:
        #if e.errno == 2:
            #continue

#print(list)