#! /usr/bin/env python

import mn.dftf.dftf as dftf
import os
import matplotlib.pyplot as plt
from mn.cmn.cmn import *
import numpy as np
import scipy.stats as stats


CONV = 482677.0 # number of pixel^2 in 1 mm^2; calculated using images in 
#~/Documents/lab/motor_neurons/camera/ruler_calib/2011-0812/ and the file in the summary 
#folder '5x_mean.txt'



def genbubparams(fname, datafol):
    """Make params file for calculating area."""
    
    d = open(fname)
    d.next()
        
    for l in d:
        newline = []
        
        for x in l.split(','):
            newline.append(x.rstrip('.fmf\n'))
        
              
        name, drop_rem, end, retracts, condition = newline[0:5]
        print(name)
        paramsfile = os.path.join('data_area', name, 'params')
        if os.path.exists(paramsfile) == True:
            print('Removing old params file')
            os.remove(paramsfile)
   
        #makenewdir(os.path.join(datafol, name))
        try:
            f = open(os.path.join(datafol, name, 'params'), 'w')
            f.write(var_str('name', name))
            f.write(var_str('frame_drop_gone', drop_rem))
            f.write(var_str('frame_pump_end', end))
            f.write(var_str('retracts', retracts))
            f.write(var_str('condition', condition))
        except IOError:
            continue
        
def genmoviedict(moviefol='.'):
    """Loads data from results file and params files into a dictionary. Converts into um^2"""
    
    os.chdir(moviefol)
    td = {}
    with open('params') as h:
        for l in h:
            td[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
    #print(td['condition'])
            
    try:
        with open('results1.txt', 'r') as f:
            numl = []
            areal = []
            slicel = []
            
            f.next()
            for l in f:
                x = l.strip('\n').split('\t')
                num, area, slice = [int(y) for y in x]
                mmarea = area/CONV 
                
                numl.append(num)
                areal.append(mmarea)
                slicel.append(slice)
                
        moviedict = {}                       
        moviedict['num'] = numl
        moviedict['area'] = areal
        moviedict['slice'] = slicel
        moviedict['condition'] = td['condition']
        moviedict['retracts'] = td['retracts']
        moviedict['moviename'] = os.path.basename(os.path.abspath(moviefol))
        print(moviedict['moviename'])
        return(moviedict)
    
    except IOError:
        pass


def loadhwidth(movie, data_hwidth_fold):
    
        resfile = os.path.join(data_hwidth_fold, movie, 'results1.txt')
        with open(resfile) as f:
            f.next()
            for l in f:
                length = l.strip('\n').split('\t')[4]
        return(float(length))


def normbywidth(moviefol, data_hwidth_fol):
    
    os.chdir(moviefol)
    moviedict = genmoviedict()
    moviedict['hwidth'] = loadhwidth(moviedict['moviename'], data_hwidth_fol)
    moviedict['normarea'] = [x/moviedict['hwidth'] for x in moviedict['area']]
    return(moviedict)
    
    


def plotpoints(moviedict, summfold):
    #For each movie, plots the points.
    
    plt.plot(moviedict['num'], moviedict['area'], '-', color='k')
    plt.plot(moviedict['num'], moviedict['area'], 'o', color='k', label=moviedict['moviename'])
    plt.legend()
    plt.title(moviedict['moviename'] + '    ' + moviedict['condition'])
    plt.xlim( (0, 16) )
    plt.ylim( (0, 0.030) )
    plotpath = os.path.join(summfold, moviedict['moviename']+'_plot.png')
    plt.savefig(plotpath)
    plt.close()


def b_plotpoints(files, summfold):
    
    for file in files:
        os.chdir(file)
        #print(file)
        md = genmoviedict()
        plotpoints(md, summfold)


def areadict_multpts(files):
    """Makes a dictionary where the keys are conditions and the values is a list of lists; each list is the area measurements for one movie."""
    
    # Run from data folder.
    
    conddict = {}
     
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))
        movie = os.path.basename(file)
        moviedict = genmoviedict()
        cond = moviedict['condition']
        if cond not in conddict:
            conddict[cond] = []
        
        if len(moviedict['area']) > 1:
             conddict[cond].append(moviedict['area'])
    
    return(conddict)


def areadict(files):
    """Makes a dictionary where the keys are conditions and the values is a list of lists; each list is the area measurements for one movie. Only includes movies with at least two pumps."""
    
    conddict = {}
     
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))
        movie = os.path.basename(file)
        moviedict = genmoviedict()
        cond = moviedict['condition']
        if cond not in conddict:
            conddict[cond] = []
        
        conddict[cond].append(moviedict['area'])
    
    return(conddict)
  

def areadict_norm(files, data_hwidth_fol):
    """Makes a dictionary where the keys are conditions and the values is a list of lists; each list is the area measurements for one movie."""
    
    # Run from data folder.
    
    conddict = {}
     
    for file in files:
        os.chdir(file)
        print(os.path.basename(file))
        movie = os.path.basename(file)
        moviedict = normbywidth(file, data_hwidth_fol)
        cond = moviedict['condition']
        if cond not in conddict:
            conddict[cond] = []
        
        conddict[cond].append(moviedict['normarea'])
    
    return(conddict)
    
def areapoints_dict(areadict):   
    """Generates a dictionary of dictionaries. The highest keys are the conditions. The next set of keys is the pump number. The values are the areas at that pump number."""
      
    pointsdict = {}
        
    for cond, arealists in areadict.iteritems():
               
        pointsdict[cond] = {}
        
        areans = []
        for area in arealists:
            areal = len(area)
            areans.append(areal)
        nums = np.linspace(1, max(areans), max(areans))
        
        point = {}
        for x in nums:
            point[x] = []
            
            for item in areadict[cond]:
                try:    
                    point[x].append(item[int(x)-1])
                except IndexError:    
                    continue
        
        pointsdict[cond] = point
    
    return(pointsdict)

        
def areapoints(areadict):   
    """Generates a dictionary of dictionaries. The keys are the conditions. The values are lists of lists; each list is the area measured at that pump number. For example, the first list is the dye areas at the first pump."""
      
    pointsdict = {}
        
    for cond, arealists in areadict.iteritems():
               
        pointsdict[cond] = []
        
        areans = []
        for area in arealists:
            areal = len(area)
            areans.append(areal)
        try:
            nums = np.linspace(1, max(areans), max(areans))
        except ValueError:
            pass
        
        point = []
        for x in nums:                       
            pointlist = []
            for item in areadict[cond]:
                try:    
                    pointlist.append(item[int(x)-1])
                    
                except IndexError:    
                    continue
            point.append(pointlist)
        
        pointsdict[cond] = point
    
    return(pointsdict)

            
def meanpoints(pointsdict):
    
    meandict = {}
    for cond, lists in pointsdict.iteritems():
        
        meandict[cond] = {}
        
        avgs = []
        stderrs = []
        ns = []
        
        for l in lists:
            ptsmean = np.mean(l)
            avgs.append(ptsmean)
            
            n = len(l)
            ns.append(n)
            
            stdev = np.std(l)
            stderr = stdev/np.sqrt(n)
            stderrs.append(stderr)
        
        meandict[cond]['mean'] = avgs
        meandict[cond]['stderr'] = stderrs
        meandict[cond]['n'] = ns

    return(meandict)   


def meanpoints_multi(pointsdict, limit):
    
    meandict = {}
    for cond, lists in pointsdict.iteritems():
        
        meandict[cond] = {}
        
        avgs = []
        stderrs = []
        ns = []
        
        for l in lists:
            if len(l) > 2: 
                ptsmean = np.mean(l)
                avgs.append(ptsmean)
            
                n = len(l)
                ns.append(n)
            
                stdev = np.std(l)
                stderr = stdev/np.sqrt(n)
                stderrs.append(stderr)
            
            else:
                pass
        
        meandict[cond]['mean'] = avgs
        meandict[cond]['stderr'] = stderrs
        meandict[cond]['n'] = ns

    return(meandict)  

def statdict(areapoints):
    
    areans = []
    for cond, arealists in areapoints.iteritems():
        areans.append(len(arealists))
    print(areans)   
    nums = np.linspace(0, max(areans), max(areans)+1)
    #nums = np.linspace(0, 1, 2)
    
    
    statdict = {}
    for x in nums:
        statdict[x] = {}
        
        for cond, arealists in areapoints.iteritems():
            statdict[x][cond] = []
            try:
                statdict[x][cond].append(arealists[int(x)])
            except IndexError:
                continue
    
    return(statdict)
    
def areastats(statdict):
    
    areastats = {}
    for num, data in statdict.iteritems():
        areastats[num] = {}
        conds = data.keys()
        
        
        for cond in conds:
            
            if 'x TNT' in cond:
                tnt = data[cond]
            if '-GAL4' in cond:
                gal4 = data[cond]
            if 'UAS-' in cond:
                uas = data[cond]
        
        print(tnt)
        print(gal4)
        print(uas)
        
        try: 
            t_tg, pval_tg = stats.ttest_ind(tnt[0], gal4[0], axis=0)
            t_tu, pval_tu = stats.ttest_ind(tnt[0], uas[0], axis=0)
            t_gu, pval_gu = stats.ttest_ind(gal4[0], uas[0], axis=0)
        
               
            areastats[num]['tnt vs gal4'] = {}
            areastats[num]['tnt vs gal4']['tstat'] = t_tg
            areastats[num]['tnt vs gal4']['pval'] = pval_tg
            areastats[num]['tnt vs uas'] = {}
            areastats[num]['tnt vs uas']['tstat'] = t_tu
            areastats[num]['tnt vs uas']['pval'] = pval_tu
            areastats[num]['gal4 vs uas'] = {}
            areastats[num]['gal4 vs uas']['tstat'] = t_gu
            areastats[num]['gal4 vs uas']['pval'] = pval_gu
        
        except IndexError:
            continue

    return(areastats)
        

def for_mc_conds(statdict, summfold, name):
    
    for num, data in statdict.iteritems():
        mcfile = os.path.join(summfold, '{0}_{1}_droparea_mc.txt'.format(name, num+1))
        with open(mcfile, 'w') as f:
            for cond, vals in data.iteritems():
                print(cond, num)
                try:
                    for val in vals[0]:
                        f.write(cond + '\t' + str(val) + '\n')
                except IndexError:
                    continue

        
def for_mc_points(areapoints_dict, summfold):
    print('areapoints_dict', areapoints_dict)
    for cond, data in areapoints_dict.iteritems():
        mcfile = os.path.join(summfold, '{0}_droparea_points_mc.txt'.format(cond))
        with open(mcfile, 'w') as f:
            for num, vals in data.iteritems():
                if num > 2:
                    continue
                else:
                    if num == 1.0:
                        snum = 'one'
                    if num == 2.0:
                        snum = 'two'
                    for val in vals:
                        f.write(str(snum) + '\t' + str(val) + '\n')
                #except IndexError:
                    #continue
        

def savemeans(meanpointsdict, summfold, meansname):    
    
    summfile = os.path.join(summfold, meansname)
    with open(summfile, 'w') as f:
        f.write('Condition,Mean,Stderr,N\n')
        
        for condition, val in meanpointsdict.iteritems():
            
            f.write('{0},{1},{2},{3}\n'.format(condition, val['mean'], val['stderr'], val['n']))

def savestats(areastatsdict, summfold, statsname):
    print(areastatsdict)
    statsfile = os.path.join(summfold, statsname)
    
    with open(statsfile, 'w') as f:
        f.write('Point,Comparison,pval,tstat\n')
    
    for point, data in areastatsdict.iteritems():
        for comp in data.iterkeys():
            with open(statsfile, 'a') as f:
                f.write('{0},{1},{2},{3}\n'.format(point, comp, data[comp]['pval'], data[comp]['tstat']))


def plotmeans(meanpointsdict):
    
    for condition, val in meanpointsdict.iteritems():
        print(condition)
        if 'x TNT' in condition:
            color = 'r'
        elif 'GAL4' in condition:
            color='b'
        elif 'UAS' in condition:
            color = 'k'
    
        y = val['mean']
        x = np.linspace(1, len(y), len(y))
        stderr = val['stderr']
        
        plt.plot(x, y, 'o', color=color, label=condition)
        plt.errorbar(x, y, stderr, elinewidth=1, mfc=color, mec=color, ecolor=color, barsabove='True', capsize=4, fmt='o')
        plt.legend()
        plt.xlabel('Pump number')
        plt.ylabel('Area')
        plt.xlim( (0, 12) )
        plt.ylim( (0, 0.012) )


def gensummfol_data(summfoldname):
    #Run from movie/data folder.
    
    pd = makepardir_data()
    summfol = os.path.join(pd, summfoldname)
    makenewdir(summfol)
    return(summfol)


def savemeanplot(summfold, plotname, format, figdpi=600):
    
    plt.savefig(os.path.join(summfold, plotname+'.'+str(format)), format=format, dpi=figdpi)
    
    
if __name__ == '__main__':        
    
    homefol = os.path.abspath(os.getcwd())
    genbubparams('movies_dye_prob_end_notes.txt', 'data_area_liquid')
    os.chdir('data_area_liquid')
    #os.chdir('data_area_wholelab')
    files = dftf.batch_s('.')  
    ad = areadict(files)
    pd = areapoints(ad)
    md = meanpoints(pd)
    
    print('Area dictionary')
    print(ad)
    
    print('Area points')
    print(pd)
    
    #ad = areadict_norm(files, os.path.join(homefol, 'data_hwidth'))
    
    sf = gensummfol_data('summary_area_liquid')
    #b_plotpoints(files, sf)
    savemeans(md, sf, 'means_area_liquid')
    
    plotmeans(md)
    savemeanplot(sf, 'means_area_liquid', 'png')
    
    sd = statdict(pd)
    print('Statdict')
    print(sd)
    
    asd = areastats(sd)
    savestats(asd, sf, 'stats_area_liquid.txt')
    print('Areastats')
    print(asd)
#plt.show()


#genbubparams('movies_dye_prob_end_notes.txt', 'data_area_wholelab')
#pardir = os.getcwd()
#summdir = makenewdir('summary_area_wholelab')
#os.chdir('data_area')
#os.chdir('data_area_wholelab')

#d = {}

 #Generates a list of movie paths in the data folder.
#files = dftf.batch_s('.')   

 #Generates dft traces and plots for each roi in each movie.
#condd = {}

#for file in files:
    #os.chdir(file)
    #movie = os.path.basename(file)
    #print(movie)

    
    
    #td = {}
    #with open('params') as h:
        #for l in h:
            #td[l.split(',')[0]] = (l.split(',')[1].strip('\n'))
    #print(td['condition'])
            
    #if td['condition'] not in condd:
        #condd[td['condition']] = []
        
       
    #try:
        #with open('results1.txt', 'r') as f:
            #numl = []
            #areal = []
            #slicel = []
            
            #f.next()
            #for l in f:
                #x = l.strip('\n').split('\t')
                #num, area, slice = [int(y) for y in x]
                
                #numl.append(num)
                #areal.append(area)
                #slicel.append(slice)
                
                #if movie not in d:
                    #d[movie] = {}
                
            #d[movie]['num'] = numl
            #d[movie]['area'] = areal
            #d[movie]['slice'] = slicel
            #d[movie]['condition'] = td['condition']
            #d[movie]['retracts'] = td['retracts']
            
            #condd[td['condition']].append(areal)
            #print(condd)
            
            
             #For each movie, plots the points.
            #plt.plot(d[movie]['num'], d[movie]['area'], '-', label=movie)
            #plt.plot(d[movie]['num'], d[movie]['area'], 'o', label=movie)
            #plt.legend()
            #plt.xlim( (0, 14) )
            #plt.savefig(os.path.join(pardir, summdir, movie+'_plot.png'))
            #plt.close()
            
    #except IOError:
            #continue

#print(condd)

#condd_pts = {}

#for key, value in condd.iteritems():
    #print(key)
    
    #condd_pts[key] = {}
    #cdd = {}
    #nums = np.linspace(0, 15, 16)
    #for x in nums:
        
        #cdd[x] = []
        #for item in condd[key]:      
            #try:
                #cdd[x].append(item[int(x)])
            #except IndexError:
                #continue
    #condd_pts[key] = cdd
    
#print(condd_pts)

#condd_avg = {}
#for cond, points in condd_pts.iteritems():
    #print(key)
    #print(value)
    
    #condd_avg[cond] = {}
    #cddavg = {}
    #for k, v in points.iteritems():
        
        #ptsmean = np.mean(v)
        
        #cddavg[key] = ptsmean
        #condd_avg[cond][k] = ptsmean

#print(condd_avg)

#condd_stderr = {}
#for cond, points in condd_pts.iteritems():
    #print(key)
    #print(value)
    
    #condd_stderr[cond] = {}
    #cddstderr = {}
    #for k, v in points.iteritems():
        
        #stdev = np.std(v)
        #n = len(v)
        #sterr = stdev/np.sqrt(n)
        
                
        #cddstderr[key] = sterr
        #condd_stderr[cond][k] = sterr

#print(condd_avg)

#for condition, points in condd_avg.iteritems():
    
    #if condition == '112204 x TNT':
        #color = 'r'
    #elif condition == '112204-GAL4':
        #color='b'
    #else:
        #color = 'k'
    
    #for x, y in points.iteritems():
        #print(x, y)
        #plt.plot(x, y, 's', color=color)
        
#plt.xlim( (-1, 10) )
#plt.legend()
#plt.show()
#for condition, points in condd_stderr.iteritems():
    
    #if condition == '112204 x TNT':
        #color = 'r'
    #elif condition == '112204-GAL4':
        #color='b'
    #else:
        #color = 'k'
    
    #for x, y in points.iteritems():
        
        #plt.errorbar(x_list, meanyvals, meansterr, mfc=meanc, mec=meanc, ecolor=meanc, ms=7, elinewidth=2, barsabove='True', capsize=8, fmt='o')
        
#plt.xlim( (-1, 10) )
#plt.legend()


#keys = sorted(d.keys())

#for key in d.iterkeys():
        
    #val = d[key]
    ##print(val)
    
    ##if val['retracts'] == 'yes':
    
    #if val['condition'] == '112204 x TNT':
        #color = 'r'
    #elif val['condition'] == '112204-GAL4':
        #color='b'
    #else:
        #color = 'k'
    
    #x = [a-1 for a in val['num']]
    #print(x)
    
    ##plt.plot(val['num'], val['area'], '-', color = color, label=key)
    #plt.plot(x, val['area'], 'o', mfc = color, ms=5)
    #plt.xlim( (-1, 15) )
    ##plt.legend() 





#plt.figure()
#for key in d.iterkeys():
    #val = d[key]

    
    ##if val['retracts'] == 'yes':
    
    #if val['condition'] == '112204 x TNT':
        #color = 'r'
    #elif val['condition'] == '112204-GAL4':
        #color='b'
    #else:
        #color = 'k'
    
    #x = [a-1 for a in val['num']]
    #print(x)
    
    #plt.plot(x, val['area'], '-', color='k')
    #plt.plot(x, val['area'], 'o', label=key)
    
    
#plt.xlim( (-1, 15) )
#plt.legend()
#plt.show()
            
        

