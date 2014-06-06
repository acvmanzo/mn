import mn.gof.gfplot as gf
import mn.plot.genplotlib as gpl
import mn.cmn.cmn as cmn
import os
import shutil
import glob
import numpy as np
import matplotlib.pyplot as plt

CONV = 0.482677 # number of pixel^2 in 1 um^2; calculated using images in 
#~/Documents/lab/motor_neurons/camera/ruler_calib/2011-0812/ and the file in the summary 
#folder '5x_mean.txt'


#def copyjpgs():
    ## Start from wbr directory.
    
    #wbrd = os.path.abspath('.')
    #exptdir = os.path.dirname(wbrd)
    #jpgdir = os.path.join(exptdir, 'cibjpg_bymovie')
    #cmn.makenewdir(jpgdir)
    
    
    #names = sorted(glob.glob('*'))
    #for name in names:
        #dfold = os.path.join(jpgdir, name)
        #cmn.makenewdir(dfold)
        
        #os.chdir(name)
        
        #for frame in ['699', '799', '899']:
            #jpgfile = name + '_00000' + frame + '.jpg'
            #shutil.copy(jpgfile, dfold)
        
        #os.chdir(wbrd)
        
    
def copyjpgs(fname):
    # Start experiment directory. Fname has the list of matching movies.
    
    exptdir = os.path.abspath('.')
    expt = os.path.basename(exptdir)
    wbr = expt + '_wbr'
    wbrdir = os.path.join(exptdir, wbr)
    
    jpgdir = os.path.join(exptdir, expt + '_cibjpgs')
    cmn.makenewdir(jpgdir)
    
    
    with open(fname, 'r') as f:
        f.next()
        for l in f:
            fly, m24, m32, cond = l.split(',')
            m24, m32 = [m.rstrip('.fmf') for m in [m24, m32]]
            fly = int(fly)
            fly = '{0:03d}'.format(fly)
            
            
            flyfold = os.path.join(jpgdir, 'fly_'+fly)
            cmn.makenewdir(flyfold)
            
            with open(os.path.join(flyfold, 'params.txt'), 'w') as g:
                g.write(cmn.var_str('movie at 24', m24))
                g.write(cmn.var_str('movie at 32', m32))
                g.write(cmn.var_str('condition', cond))
            
            for movie in [m24, m32]:
                dfold = os.path.join(flyfold, movie)
                cmn.makenewdir(dfold)
                for frame in ['698', '798', '898']:
                    jpgfile = movie + '_00000' + frame + '.jpg'
                    jpgpath = os.path.join(wbrdir, movie, jpgfile)
                    shutil.copy(jpgpath, dfold)
        


def comp_intensity_norm():
    # Start from fly folder.
    
    meannormint = {}
    movies = []
    
    flyfold = os.path.abspath('.')
    names = glob.glob('mov_*')
    for name in sorted(names):
        os.chdir(name)
        print(name)
        if os.path.exists('results1.txt') == True:
            data = np.loadtxt('results1.txt', skiprows=1, usecols=(1,2))
        else:
            break
        
        normint = []
        for datum in data:
            x = datum[0]/datum[1]
            normint.append(x)
        
        #print(np.mean(normint))
        meannormint[name] = np.mean(normint)
        
        os.chdir(flyfold)
       
    s_means = sorted(meannormint.items())
    frac = (s_means[1][1])/(s_means[0][1])
    return(frac)
      
      
def comp_intensity():
    # Start from fly folder.
    
    meanint = {}
    movies = []
    
    flyfold = os.path.abspath('.')
    names = glob.glob('mov_*')
    for name in sorted(names):
        os.chdir(name)
        print(name)
        #os.path.exists('results1.txt') == True:
        data = np.loadtxt('results1.txt', skiprows=1, usecols=(1,2))
        
        #else:
            #break
        intensity = []
        intensity.append(data[0])
        #for datum in data:
            #print(datum)
            #x = datum[0]
            #intensity.append(x)
        
        #print(np.mean(normint))
        meanint[name] = np.mean(intensity)
        
        os.chdir(flyfold)
       
    s_means = sorted(meanint.items())
    frac = (s_means[0][1])-(s_means[1][1])
    return(frac)  


def batch_comp_intensity():
    
    cibjpgdir = os.path.abspath('.')
    exptdir = os.path.dirname(cibjpgdir)
    
    fracfile = os.path.join(exptdir,'fracs_notnorm.txt')
    with open(fracfile, 'w') as f:
        f.write('Fly,M24,M32,Condition,Frac\n')
    
    
    flies = glob.glob('*')
    for fly in sorted(flies):
        os.chdir(fly)
        
        #try:
        frac = comp_intensity()
        strfrac = str(frac)
        #except IndexError:
            #continue
        
        
        with open('params.txt') as g:
            params = []
            for l in g:
                try:
                    x = l.split(',')[1]
                    x = x.rstrip('\n')
                    params.append(x)
                except IndexError:
                    continue
                
            m24, m32, cond = params
        
        with open(fracfile, 'a') as f:
            f.write('{0},{1},{2},{3},{4}\n'.format(fly,m24,m32,cond,strfrac))
        
        os.chdir(cibjpgdir)
        

def loadareas(fname):
    areadata = np.loadtxt(fname, skiprows=1, usecols=(1,))
    
    return(areadata.tolist())



def comp_areadiff(moviematchfile, difffile):
    exptdir = os.path.abspath('.')
    expt = os.path.basename(exptdir)
    wbr = expt + '_wbr'
    wbrdir = os.path.join(exptdir, wbr)
    summdir = os.path.join(exptdir, 'summary')
    cmn.makenewdir(summdir)
    difffpath = os.path.join(summdir, difffile)
    
    with open(difffpath, 'w') as g:
        g.write('Fly,Movie-24,Movie-32,MeanArea-24(um),MeanArea-32(um),DiffArea(um^2),Condition\n')

    with open(moviematchfile, 'r') as f:
        f.next()
        for l in f:
            fly, m24, m32, cond = l.split(',')[0:4]
            m24, m32 = [m.rstrip('.fmf') for m in [m24, m32]]
            cond = cond.rstrip('\n')
            
            cibdatadir = os.path.join(exptdir, 'data_cibarea')
            try:
                results = [loadareas(os.path.join(cibdatadir, m, 'results1.txt')) for m in [m24, m32]]
            except IOError as e:
                if e.errno == 2:
                    continue
            pixmeans = [np.mean(result) for result in results]
            mm_means = [x/CONV for x in pixmeans]
            
            pixmean24, pixmean32 = pixmeans
            mm_mean24, mm_mean32 = mm_means
            
            pixdiff = pixmean32 - pixmean24
            mmdiff = mm_mean32 - mm_mean24
            
            
            with open(os.path.join(summdir, difffpath), 'a') as g:
                g.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(fly, m24, m32, mm_mean24, mm_mean32, mmdiff, cond))


def writecibmeans(fname, gname):
    dicts = gpl.gendict_cibgf(fname)
    dmean, ddiffa = dicts
    
    for k, val in dmean.iteritems():
        for v in val:
            with open(gname, 'a') as g:
                g.write(k + '\t' + v + '\n')


def plotcibarea(fname, k1, k2):
    
    dicts = gpl.gendict_cibgf(fname)
    dmean, ddiffa = dicts
    mdicts = map(gpl.genlist, dicts)
    mdmean, mddiffa = mdicts
    zd = zip(dicts, mdicts)
    

    #k1 = sorted(dmean.keys())
    #k2 = sorted(ddiffa.keys())
    
    for type in ['b', 's']:
        gpl.plotdata(dmean, mdmean, k1, type, r'$\mu$m$^2$', 'Mean areas', ylim=10000, ymin=0)
        plt.savefig('areameans_' + type)
        
        if type == 'b':
            gpl.plotdata(ddiffa, mddiffa, k2, type, r'$\mu$m$^2$', 'Difference in area', 
            ylim=6000, ymin=-1000)
            plt.savefig('areadiffs_' + type)
        if type == 's':
            gpl.plotdata(ddiffa, mddiffa, k2, type, r'$\mu$m$^2$', 'Difference in area', 
            ylim=6000, ymin=-2000)
            plt.savefig('areadiffs_' + type)
    
    
def autokeys(fname):
    dicts = gpl.gendict_cibgf(fname)
    dmean, ddiffa = dicts
    k1 = sorted(dmean.keys())
    k2 = sorted(ddiffa.keys())
    return(k1, k2)


def b_comparea_plot():
    # Run from experiment folder.
    comp_areadiff('moviematch.txt', 'diff_cibarea.txt')
    os.chdir('summary')
    k1, k2 = autokeys('diff_cibarea.txt')
    #k1 = cmn.loadkeys('keylistmean')
    #k2 = cmn.loadkeys('keylistdiff')
    plotcibarea('diff_cibarea.txt', k1, k2)


#
