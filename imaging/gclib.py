import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import glob
import mn.plot.genplotlib as genplotlib
from mn.cmn.cmn import *



PARAMSFILE = 'params'
RESULTSFILE = 'results1.txt'
RAWFOLDER = 'plots_raw'
DFFFOLDER = 'plots_dff'
DFFCFOLDER = 'plots_dffc'
DFFSECFOLDER = 'plots_dff_sec'
DFFCSECFOLDER = 'plots_dffc_sec'
DFFC40SECFOLDER = 'plots_dffc_40sec'
DFF40SECFOLDER = 'plots_dff_40sec'
STIMSEC = 8
BGSEC = 3 # Number of seconds before STIMSEC used to calculate the basal fluorescence (if BGSEC = 
# 3, then seconds STIMSEC-BGSEC to STIMSEC will be used to calculate the basal fluorescence.
STIMDUR = 39 # how long the movie lasts in seconds
WINLENSEC = 1
DFTHRESHOLD = 0.15


YMINRAW = 0
YMAXRAW = 250
YMINDFF = -1
YMAXDFF = 2



def load_params(paramsfile):
    """Loads the parameters from the file 'paramfiles'; returns a dictionary."""

    fd={}
    with open(paramsfile) as g:
        for l in g:
            fd[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
    for k in iter(fd):
        try:
            fd[k] = int(fd[k])
        except ValueError:
            pass
    return(fd)


def load_results(results):
    """
    Returns a numpy array from 'results' file containing the mean ROI intensity for each frame 
    of an image sequence for 1+ ROIs. Function returns 
    a dictionary containing the ROI names and the indices of the columns they refer to. This 
    function is meant to be used with a file generated by the ImageJ function "multimeasure", 
    usually with the ImageJ custom macro "automeasure.txt".
    """
    
    # Makes a dictionary matching column names to column indices.
    with open(results) as f:
        roi_cols = dict(((roi, ind+1) for ind, roi in enumerate(f.readline().split())))
           
    # Creates a numpy array containing all the data.
    raw = np.loadtxt(results, skiprows=1)
    
    return np.transpose(raw), roi_cols

# Not used.
def loadtrace(fname):
    frame = np.loadtxt(fname, skiprows=1, usecols=(0,))
    roi1 = np.loadtxt(fname, skiprows=1, usecols=(1,))
    try:
        roi2 = np.loadtxt(fname, skiprows=1, usecols=(2,))
        return(np.array([frame, roi1, roi2]))
    except IndexError:
        return(np.array([frame, roi1]))


def dff(trace, x1, x2):
    """Returns the deltaf/f trace"""
    dfft = trace/np.mean(trace[x1:x2])-1
    return(dfft)

def window(winlen):
    
    wind = list(np.ones(winlen)/winlen)
    return(wind)

def frametosec(trace, fps):
    """Converts a list of frames to seconds but maintaining length"""
    
    len_trace = len(trace)
    sec_trace = float(len_trace)/fps
    newtrace = np.linspace(1/fps, sec_trace, len_trace)
    return(newtrace)

def plottrace(type):
    """Code for plotting various trace types."""
    
    fd = load_params(PARAMSFILE)
    fps = float(fd['fps'])
    stimfr = STIMSEC*fps
    bgfr = (STIMSEC-BGSEC)*fps
    winlen_fr = WINLENSEC*fps
    wind = window(winlen_fr)
        
    x, roi_cols = load_results(RESULTSFILE)
    
    plt.figure()
    plt.title(fd['name'] + '\n' + 'stim =' + str(stimfr))
    for col in roi_cols.itervalues():
        dfft = dff(x[col], bgfr, stimfr)
    
        if type == 'raw':
            plt.plot(x[0], x[col])
            plt.ylim( (YMINRAW, YMAXRAW) )
        
        if type == 'dff':
            plt.plot(x[0], dfft)
            plt.ylim( (YMINDFF, YMAXDFF) )
            plt.title(fd['name'] + '\n' + 'stim =' + str(stimfr))
        
        if type == 'dffc':
            plt.plot(x[0], np.convolve(dfft, wind, 'same'))
            plt.ylim( (YMINDFF, YMAXDFF) )
            plt.title(fd['name'] + '\n' + 'stim =' + str(stimfr) + ' winlen (s) =' + str(WINLENSEC))
        
        if type == 'dff_sec':
            xvals = frametosec(x[0], fps)
            plt.plot(xvals, dfft)
            plt.ylim( (YMINDFF, YMAXDFF) )
        
        if type == 'dffc_sec':
            xvals = frametosec(x[0], fps)
            plt.plot(xvals, np.convolve(dfft, wind, 'same'))
            plt.ylim( (YMINDFF, YMAXDFF) )
            plt.title(fd['name'] + '\n' + 'stim =' + str(STIMSEC) + ' winlen (s) =' + str(WINLENSEC))
        
        if type == 'dffc_40sec':
            xvals = frametosec(x[0], fps)
            plt.plot(xvals[0:40*fps], np.convolve(dfft, wind, 'same')[0:40*fps])
            plt.ylim( (YMINDFF, YMAXDFF) )
            plt.title(fd['name'] + '\n' + 'stim =' + str(STIMSEC) + ' winlen (s) =' + str(WINLENSEC))
        
        if type == 'dff_40sec':
            xvals = frametosec(x[0], fps)
            plt.plot(xvals[0:40*fps], dfft[0:40*fps])
            plt.ylim( (YMINDFF, YMAXDFF) )
            plt.title(fd['name'] + '\n' + 'stim =' + str(STIMSEC) + ' winlen (s) =' + str(WINLENSEC))
        


def plotandsaveplot(type, plotfolder):
    plt.figure()
    plottrace(type)
    cur = os.getcwd()
    name = os.path.basename(cur)
    new = cur.replace('data/'+name, plotfolder)
    
    makenewdir(new)
    plt.savefig(os.path.join(new, name))
    plt.close()




def downsample(trace, startfps, endfps):
    assert startfps > endfps
    
    ratio = startfps/endfps
    points_tilenum = len(trace)*(1-endfps/startfps)
    points = np.tile([1,1,1,0], np.ceil(points_tilenum))
    points = points[0:len(trace)]
    downsampled_trace = trace * points

def peak(trace, stimfr, fps):
    """Finds the peak deltaf/f"""
    end = fps*STIMDUR
    x = np.max(trace[stimfr:end])
    return(x)

#~ This function normalizes area by downsampling the trace.
#~ def area(trace, stimfr, fps, threshold):
    #~ """Finds area of trace above threshold and after stimulation frame. Because there are different 
    #~ frame rates, I have to downsample the fastest frame rate (~20) to the lower frame rate, ~13.3. 
    #~ Will instruct it to remove every 4th frame in this case"""
    #~ compmat = trace > np.ones(len(trace)) * threshold
    #~ newtrace = compmat * trace
    #~ print('Newtrace', newtrace)
    #~ end = fps*STIMDUR
    #~ 
    #~ if fps == 19.8:
        #~ 
        #~ # Create a list of the same length as the original trace but with every 4th point set to 0.
        #~ downsample(newtrace, fps, 13.3)
        #~ x = np.sum(downsampled_trace[stimfr:end])
    #~ 
    #~ if fps == 13.3:
        #~ x = np.sum(newtrace[stimfr:end])
    #~ 
    #~ print(x)
    #~ return(x)

#~ This function normalizes area by dividing by the sampling frequency when calculating area, as 
#~ the area of each point is value * 1/sampling frequency.

def area(trace, stimfr, fps, threshold):
    """Finds area of trace above threshold and after stimulation frame. Because there are different 
    frame rates, I have to downsample the fastest frame rate (~20) to the lower frame rate, ~13.3. 
    Will instruct it to remove every 4th frame in this case"""
    compmat = trace > np.ones(len(trace)) * threshold
    newtrace = compmat * trace
    end = fps*STIMDUR
    
    #~ Divide each point by the fps to normalize them, so now each point is intensity-seconds 
    #~ rather than just intensity. Area is intensity-seconds anyway, because area is intensity/ 
    #~ sample frequency.
    norm_newtrace = newtrace/fps
    x = np.sum(norm_newtrace[stimfr:end])
    #print(x)
    return(x)



#def area(trace, stimfr, fps):
    #"""Finds area of trace after stimulation frame."""
    
    #end = fps*STIMDUR
    #x = np.sum(newtrace[stimfr:end])
    #return(x)


def duration(trace, stimfr, fps, threshold):
    """Finds the duration of response above threshold and after stimulation frame."""
    
    compmat = trace > np.ones(len(trace)) * threshold
    newtrace = compmat * trace
    end = fps*STIMDUR
    
    indices = (np.nonzero(newtrace[stimfr:end]))
    
    return(np.shape(indices)[1]/fps)
    

class TraceData:
    
    def __init__(self, fname, paramsfile):
        self.fname = fname
        self.paramsfile = paramsfile
       
    def Processrawtrace(self):
        """Structure of dictionary: 
        ROI1 (dictionary): fps, neurons, zmotion, stimframe, raw trace, dff (dictionary), dffc (dictionary)
            dff: trace, peak, area, duration
            dffc: trace, peak, area, duration
        ROI2 (dictionary): fps, neurons, zmotion, stimframe, raw trace, dff (dictionary), dffc (dictionary)
            dff: trace, peak, area, duration
            dffc: trace, peak, area, duration
        """
            
        
        tracedict = {}
        
        x, roi_cols = load_results(self.fname)
        for roi, col in roi_cols.iteritems():
            
            coldict = {}
            
            for l in open(self.paramsfile):
                coldict[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
            
            coldict['fps'], coldict['neurons'], coldict['zmotion'] = map(float, [coldict['fps'],coldict['neurons'], coldict['zmotion']])
            coldict['stimfr'] = STIMSEC*coldict['fps']
            coldict['bgfr'] = (STIMSEC-BGSEC)*coldict['fps']
            fps = coldict['fps']

            coldict['raw'] = x[col]
            
            #~ Define x values in seconds.
            l_raw = len(coldict['raw'])
            l_sec = len(coldict['raw'])/coldict['fps']
            coldict['time_values'] = np.linspace(1/fps, l_raw/fps, l_raw/fps)
            
            
            winlen_frames = WINLENSEC * coldict['fps']
            
            
            # Dictionary containing deltaf/f trace, deltaf/f peak value, deltaf/f area, and deltaf/f duration.
            coldict['dff'] = {}
            coldict['dff']['trace'] = dff(x[col], coldict['bgfr'], coldict['stimfr'])
            
            coldict['dff']['peak'] = peak(coldict['dff']['trace'], coldict['stimfr'], coldict['fps'])

            coldict['dff']['peaki'] = list(coldict['dff']['trace']).index(coldict['dff']['peak'])
            coldict['dff']['peakisec'] = coldict['dff']['peaki']/coldict['fps']
            
            coldict['dff']['area'] = area(coldict['dff']['trace'], coldict['stimfr'], coldict['fps'], DFTHRESHOLD)
            
            coldict['dff']['duration'] = duration(coldict['dff']['trace'], coldict['stimfr'], coldict['fps'], DFTHRESHOLD)
            
            # Dictionary containing trace, peak value, area, and duration for convolved deltaf/f trace.
            coldict['dffc'] = {}
            
            coldict['dffc']['trace'] = np.convolve(coldict['dff']['trace'], window(winlen_frames), 'same')
            
            coldict['dffc']['peak'] = peak(coldict['dffc']['trace'], coldict['stimfr'], coldict['fps'])
            
            coldict['dffc']['area'] = area(coldict['dffc']['trace'], coldict['stimfr'], coldict['fps'], DFTHRESHOLD)
            
            coldict['dffc']['duration'] = duration(coldict['dffc']['trace'], coldict['stimfr'], coldict['fps'], DFTHRESHOLD)
            
            tracedict[roi] = coldict
        
        return(tracedict)


def summdir():
    """Run from any folder in the line (ex., 112648) folder."""
    
    temp = os.path.abspath('.').split('/')
        #summdir = os.path.join('/', temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], 'summary')
    summdir = os.path.join('/', temp[1], temp[2], temp[3], temp[4], 'summary')
    
    return(summdir)
    

def summfile(tracetype):
    """Run from  any folder in the line (ex., 112648) folder."""
    
    summfold = summdir()
    
    if tracetype == 'dff':
        summpath = os.path.join(summfold, 'summ_dff.txt')
    if tracetype == 'dffc':
        summpath = os.path.join(summfold, 'summ_dffc_w{0}.txt'.format(WINLENSEC))
    
    return(summpath)


def writemetrics(dict):
    """Writes metrics to summary file."""
    xs = ['dff', 'dffc']
    
    for roi in dict.iterkeys():
        for x in xs:
            makenewdir(summdir())
            summpath = summfile(x)
                        
            if os.path.isfile(summpath) != True:
                with open(summpath, 'w') as f:
                    f.write('Movie,Tastant,FPS,Zmotion,Neurons,Peak,Area,Dur,DFThreshold\n')
            
            fps, zmotion, neurons, peakn, arean, durationn, dfthreshold = map(str, [dict[roi]['fps'], dict[roi]['zmotion'], dict[roi]['neurons'], dict[roi][x]['peak'], dict[roi][x]['area'], dict[roi][x]['duration'], DFTHRESHOLD])
            
            with open(summpath, 'a') as f:
                f.write(dict[roi]['name'] + ',' + dict[roi]['tastant'] + ',' + fps + ',' + zmotion + ',' + neurons + ',' + peakn + ',' + arean + ',' + durationn + ',' + dfthreshold + '\n')

def batch_writemetrics():
    
    if os.path.exists(summfile('dff')) == True:
        os.remove(summfile('dff'))
    
    if os.path.exists(summfile('dffc')) == True:
        os.remove(summfile('dffc'))
        
    names = glob.glob('*')
    # Absolute path rather than relative path allows changing of directories in fn_name.
    names = [os.path.abspath(name) for name in names]
    names = sorted(names)
    
    for name in names:
        t = time.strftime('%H:%M:%S')
        print os.path.basename(name), t
        os.chdir(name)
        if os.path.exists(RESULTSFILE) == True:
            a = TraceData(RESULTSFILE, PARAMSFILE)
            td = a.Processrawtrace()
            writemetrics(td)
        else:
            print('No results file')
            continue


def plotpeak(k, fname, type = 's', ymax=1.0):
    plt.figure()
    d = genplotlib.gendictgc(fname)[0]
    md = genplotlib.genlist(d)
    print('Peak')
    for tastant, values in d.iteritems():
        print(tastant, np.max(values))
    if type == 'b':
        genplotlib.plotdata(d, md, k, 'b', '%', 'Peak deltaF/F', 0, ymax, xlabelsize='medium')
    if type == 's':
        genplotlib.plotdata(d, md, k, 's', 'Peak deltaF/F', 'Peak deltaF/F', -0.4, ymax+0.6, 
        xlabelsize='medium')
    
def plotarea(k, fname, type='s', ymax=10):
    plt.figure()
    d = genplotlib.gendictgc(fname)[1]
    md = genplotlib.genlist(d)
    print('Area')
    for tastant, values in d.iteritems():
        print(tastant, np.max(values))
    if type == 'b':
        genplotlib.plotdata(d, md, k, 'b', 'intensity-seconds', 'Area under curve', 0, ymax, xlabelsize='medium')
    if type == 's':
        genplotlib.plotdata(d, md, k, 's', 'Area under curve', 'Area under curve', 0, ymax+15, xlabelsize='medium')

def plotdur(k, fname, type='s', ymax=30):
    plt.figure()
    d = genplotlib.gendictgc(fname)[2]
    md = genplotlib.genlist(d)
    print('Duration')
    for tastant, values in d.iteritems():
        print(tastant, np.max(values))
    
    if type == 'b':
        genplotlib.plotdata(d, md, k, 'b', 'seconds', 'Duration', 0, ymax, xlabelsize='medium')
    if type == 's':
        genplotlib.plotdata(d, md, k, 's', 'seconds', 'Duration', -5, ymax+10, xlabelsize='medium')


def plotdyearea(fname, k):
    plt.figure()
    d = genplotlib.gendictgc2(fname)[3]
    #~ print(d)
    md = genplotlib.genlist(d)
    print(md)
    #~ print('Dye Area Max Values')
    #~ for tastant, values in d.iteritems():
        #~ print(tastant, np.max(values))
    genplotlib.plotdata(d, md, k, 'b', 'Normalized Area', 'Dye Area', -0.001, 0.1, xlabelsize='medium')
    plt.savefig('dyearea_b')
    genplotlib.plotdata(d, md, k, 's', 'Normalized Area', 'Dye Area', -.01, 0.3, xlabelsize='medium')
    plt.savefig('dyearea_s')


def plotdyearea_3d2(fname, k):
    plt.figure()
    d = genplotlib.gendictgc2(fname)[3]
    #~ print(d)
    md = genplotlib.genlist(d)
    print(md)
    #~ print('Dye Area Max Values')
    #~ for tastant, values in d.iteritems():
        #~ print(tastant, np.max(values))
    genplotlib.plotdata(d, md, k, 'b', 'Normalized Area', 'Dye Area', -0.001, 0.05, xlabelsize='medium')
    plt.savefig('dyearea_b')
    genplotlib.plotdata(d, md, k, 's', 'Normalized Area', 'Dye Area', -.01, 0.12, xlabelsize='medium')
    plt.savefig('dyearea_s')

def plotgraphs(fname, k, peakmax=1.5):
    
    summfolder = summdir()
    makenewdir(summfolder)
    print(fname)
    trace = fname.split('_')[1].rstrip('.txt')
    
    plotpeak(k, fname, 's', peakmax)
    plt.savefig(os.path.join(summfolder, trace + 'peak_s'))
    plotpeak(k, fname, 'b', peakmax)
    plt.savefig(os.path.join(summfolder, trace + 'peak_b'))
    plotarea(k, fname, 's')
    plt.savefig(os.path.join(summfolder, trace + 'area_s'))
    plotarea(k, fname, 'b')
    plt.savefig(os.path.join(summfolder, trace + 'area_b'))
    plotdur(k, fname, 's')
    plt.savefig(os.path.join(summfolder, trace + 'dur_s'))
    plotdur(k, fname, 'b')
    plt.savefig(os.path.join(summfolder, trace + 'dur_b'))

    



