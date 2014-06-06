
import os
import glob
from mn.imaging.gclib import *

TSTART = 100
TEND = 200

summfolder = summdir()
makenewdir(summfolder)
#print(summfolder)

os.chdir('data')
names = glob.glob('*')
# Absolute path rather than relative path allows changing of directories in fn_name.
names = [os.path.abspath(name) for name in names]
names = sorted(names)

d = {}
for name in names:
    print(name)
    os.chdir(name)
    movie = os.path.basename(name)
    tstart=0
    tend=772
       
    
    if movie == '2011-0329_112648_gc30_B_1_Sd_mc':
        pass
        #tstart = 175
        #tend = 275
    
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        pass
        #tstart = 220
        #tend = 320
        
    if movie == '2011-0429_112648_gc30_C_1_Sd_mc':
        pass
        #tstart = 150
        #tend = 250
    
    
    a = TraceData(RESULTSFILE, PARAMSFILE)
    td = a.Processrawtrace()
    trace1 = td['Mean1']['dff']['trace'][tstart:tend]
    trace2 = td['Mean2']['dff']['trace'][tstart:tend]
    
    if movie == '2011-0330_112648_gc30_F_2_Cd_mc':
        trace2 = td['Mean2']['dff']['trace'][tstart:tend] * 1.4
    
    z = np.zeros(3)
    trace3 = np.concatenate((z, trace2))
    
    #print(movie)
    
    xcorr = np.correlate(trace1, trace2, mode='full')
    plt.figure()
    plt.plot(trace1)
    plt.plot(trace2)
    ax = plt.gca()
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(40)) 
    plt.xticks(fontsize=5)
    figname = os.path.join(summfolder, movie+'_plot.png')
    plt.savefig(figname)
    
    #plt.show()
    #plt.plot(np.linspace(400, 400+len(trace2), len(trace2)), trace2)
    plt.figure()
    
    #xvals = []
    #xvals = np.linspace(-772/19.8, 772/19.8, len(xcorr))
    #plt.plot(xvals, xcorr)
    #maxxcorr = np.max(xcorr)
    #maxi = list(xcorr).index(maxxcorr)
    #print(maxi)
    #print(xvals[maxi])
    #plt.xlim( (-50, 772*2) )
    
    
    xvals = []
    xvals = np.linspace(-len(trace1), len(trace1), len(trace1)*2)
    plt.plot(xcorr)
    maxxcorr = np.max(xcorr)
    maxi = list(xcorr).index(maxxcorr)
    print(maxi)
    print(xvals[maxi])
    
    figname = os.path.join(summfolder, movie+'_xcorr.png')
    plt.savefig(figname)
    plt.close()
    
    d[movie] = {}
    d[movie]['max'] = maxxcorr
    d[movie]['maxi'] = xvals[maxi]
    
    summfile = os.path.join(summfolder, 'lim_xcorr_results.txt'.format(tstart,tend))
    with open(summfile, 'a') as f:
        f.write('{0},{1},{2},{3},{4}\n'.format(movie, maxxcorr, xvals[maxi], tstart, tend))
    
    
    #plt.figure()
    #xcorrtest = np.correlate(trace1, trace3, mode='full')
    #plt.plot(xcorrtest)
    #plt.xlim( (0, 2000) )
    #figname = os.path.join(summfolder, movie+'_xcorr+3.png')
    #plt.savefig(figname)

    #plt.show()
#print(d)
#summfile = os.path.join(summfolder, '{0}-{1}_xcorr_results.txt'.format(tstart,tend))
#summfile = os.path.join(summfolder, '{0}-{1}_xcorr_results.txt'.format(tstart,tend))
#with open(summfile, 'w') as f:
    #f.write('Movie,Maxval,Maxindex')
    #for movie, vals in d.iteritems():
        #f.write('{0},{1},{2}\n'.format(movie, vals['max'], vals['maxi']))
