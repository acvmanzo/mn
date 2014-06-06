import os
import glob

#EXPTS = ['2011-0329_423_tnt_180f', '2011-0331_423_tnt_180f', '2011-0406_423_tnt_180f']
#EXPTS = ['2011-0331_423_tnt_180f', '2011-0406_423_tnt_180f']
EXPTS = ['2011-0313_112204_tnt_180f', '2011-0316_112204_tnt_180f']
EXPTS = ['2011-0316_112204_tnt_180f']
FRAMES = 180

for expt in EXPTS:
    os.chdir(expt)

    framesfile = glob.glob('*frames.txt')
    os.system('genparams {0} 60 {1}'.format(framesfile[0], FRAMES))
    os.system('gencapparams {0} 60'.format(framesfile[0]))


    os.chdir('data')
    os.system('dftfbatch')
    os.system('pcapmbatch')

    #os.chdir('{0}/summary'.format(expt))
    os.chdir('../summary'.format(expt))
    os.system('volperpump default 1 1')
    os.chdir('../')
