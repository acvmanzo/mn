from mn.gof.gfplot import *
from mn.gof.ciblib import *



def reanalyze(exptlist):
    # Run from anywhere.

    dtrpfold = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1'
    os.chdir(dtrpfold)

    for expt in exptlist:
        os.chdir(expt)
        print(expt)
        b_comparea_plot()
        os.chdir(dtrpfold)
    
        

def poolcibdata(exptlist, keyfilemean, keyfilediff):
    # Run from pooled_expt/cibarea folder.
    dtrpfold = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1'
    p_cibarea = 'pooled_diff_cibarea.txt'
    
    if os.path.exists(p_cibarea) == True:
        os.remove(p_cibarea)

    for expt in exptlist:
        cibfile = os.path.join(dtrpfold, expt, 'summary', 'diff_cibarea.txt')
        
        with open(cibfile) as f:
            f.next()
            
            if os.path.exists(p_cibarea)!=True:
                with open(p_cibarea, 'w') as g:
                    g.write('Fly,Movie-24,Movie-32,MeanArea-24,MeanArea-32,DiffArea,Condition\n')
            
            with open(p_cibarea, 'a') as g:
                for l in f:
                    g.write(l)
    
    k1 = cmn.load_keys(keyfilemean)
    k2 = cmn.load_keys(keyfilediff)
    
    # Plot graphs.
    plotcibarea(p_cibarea, k1, k2)


def poolallcibdata(folderlist):
    #Can run from anywhere
    dtrpa1f = '/home/andrea/Documents/lab/motor_neurons/gof/dtrpa1'
    p_cibarea = os.path.join(dtrpa1f, 'pooled_all', 'cibarea', 'pooled_all_cibarea.txt')
    
    if os.path.exists(p_cibarea) == True:
        os.remove(p_cibarea)
       
    for fold in folderlist:
        cibareafile = os.path.join(dtrpa1f, fold, 'cibarea', 'pooled_diff_cibarea.txt')
        with open(cibareafile) as f:
            f.next()
            
            if os.path.exists(p_cibarea)!=True:
                with open(p_cibarea, 'w') as g:
                    g.write('Fly,Movie-24,Movie-32,MeanArea-24,MeanArea-32,DiffArea,Condition\n')
                    
            
            with open(p_cibarea, 'a') as g:
                for l in f:
                    g.write(l)
    


    
