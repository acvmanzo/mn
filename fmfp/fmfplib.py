# This module defines functions useful for processing and converting .fmf files generated by fview.

# It produces a directory structure like the following:

# dirname/
	# dirname_fmf/
	# dirname_bmp/
		# moviexxxx/
            # moviexxxx_xxx0.bmp
            # moviexxxx_xxx1.bmp
		# moviexxxx/
	# dirname_wbr/
		# moviexxxx/
            # moviexxxx_xxx0.jpg
            # moviexxxx_xxx1.jpg
		# moviexxxx/

# Fmf files should be placed in the dirname_fmf folder.


import os
import os.path
import glob
import shutil
import time
import sys
from mn.cmn.cmn import *


class WBalRParams:
    """Class defining the parameters for rotating and white balancing images using ImageMagick command line functions.
        
    rot: Specifies the amount of rotation in degrees that is applied to the images. 
    r, g, b: Specifies the scaling factors for each color channel that are used to white balance each image using the 'convert -recolor' function of ImageMagick. 
    itype: Specifies the format of the image sequences generated from fmf files. Allowed values are 'bmp, 'jpg' and 'png'.
    otype: Specifies the output format of the images being white-balanced and rotated. Allowed values include 'bmp' and 'jpg'.
    """
    
    def __init__(self, rot=0, r=1, g=1, b=1, itype='bmp', otype='jpg'):
        self.rot = rot
        self.r = r
        self.g = g
        self.b = b
        self.itype = itype
        self.otype = otype
    def apply(self, image):
        """Method that white balances and rotates images using the -rotate and -recolor functions of ImageMagick."""
        
        recmat = '{0} 0 0 0 {1} 0 0 0 {2}'.format(self.r, self.g, self.b)
        root, ext = os.path.splitext(image)
        cmdwbr = r'convert -rotate {0} -recolor "{1}" {2}.{4} {3}.{5}'.format(self.rot, recmat, root, root, self.itype, self.otype)
        exitcode = os.system(cmdwbr)
        if exitcode != 0:
            sys.exit(0)

def apply(image, params):
	"""Method that white balances and rotates images using the -rotate and -recolor functions of ImageMagick."""
	
	recmat = '{0} 0 0 0 {1} 0 0 0 {2}'.format(params.r, params.g, params.b)
	root, ext = os.path.splitext(image)
	cmdwbr = r'convert -rotate {0} -recolor "{1}" {2}.{4} {3}.{5}'.format(params.rot, recmat, root, root, params.itype, params.otype)
	os.system(cmdwbr)

    
# Creates an instance of the class WBalRParams with values for rotating and white-balancing. 
# To white balance a single image, use the command 'params.apply('filename').
#params = WBalRParams(rot, r, g, b, itype, otype)


#~ def batch(fn_name, ftype, params, fdir='.'):
    #~ """Carries out the function 'fn_name' recursively on files with extension 'itype' (e.g., 'jpg' or '*') in directory 'fdir'.
    #~ """
    
  
    #~ os.chdir(fdir)
    #~ names = glob.iglob('*{0}'.format(ftype))
    #~ # Absolute path rather than relative path allows changing of directories in fn_name.
    #~ names = [os.path.abspath(name) for name in names]
    #~ names = sorted(names)
    #~ for name in names:
        #~ if ftype != params.itype:
            #~ t = time.strftime('%H:%M:%S')
            #~ print os.path.basename(name), t
        
        #~ fn_name(name, params)
        


def movefiles(source, dest, itype):
    """Moves all files with the extension 'itype' from 'source' to 'dest'. All arguments are strings.
    """
    
    os.chdir(source)
    files = glob.iglob('*{0}'.format(itype))
    for afile in files:
        shutil.move(afile, dest)
    

#~ def makenewdir(newdir):
    #~ """Makes the new directory 'newdir' without raising an exception if 'newdir' already exists."""
    
    #~ try:
        #~ os.makedirs(newdir)
    #~ except OSError as e:
        #~ if e.errno == 17:
            #~ pass
    

def defpardir (dpath, suffix):
    """ Returns a string of the form 'dirname_suffix'. For instance, if dpath = 
    '/home/andrea/pytest' then the returned string is '/home/andrea/pytest_suffix'.
    """
    
    mainname = os.path.basename(dpath)
    fullname = '{0}_{1}'.format(mainname, suffix)
    pardir = os.path.join(dpath, fullname)
    return(os.path.abspath(pardir))


def defbmpdir(fmf, params):
    name = os.path.basename(fmf)
    root, ext = os.path.splitext(name)
    
    pardir = defpardir(os.path.abspath('..'), params.itype)
    newdir = os.path.join(pardir, root)
    return(newdir)


def fmfconv(fmf, params):
    """Converts a single fmf file to an image sequence of type 'itype'. Image files are placed in a 
    directory such as 'dirname_bmp/moviexxxx" in the above file structure.
    """
    
    #name = os.path.basename(fmf)
    #root, ext = os.path.splitext(name)
    
    #pardir = defpardir(os.path.abspath('..'), params.itype)
    #newdir = os.path.join(pardir, root)
    newdir = defbmpdir(fmf, params)
    makenewdir(newdir)
    
    cmd = 'fmf2bmps "{0}" --extension={1} --outdir="{2}"'.format(fmf, params.itype, newdir)
    exitcode = os.system(cmd)
    if exitcode != 0:
        sys.exit(0)
    return(newdir)
    # Can also do os.chdir(pardir) here (for use in the long batch version).
    
    

def b_fmfconv(params, fdir='.'):
    """Converts multiple fmf files in the directory 'fdir' into image sequences of type 'itype'. 
    Image files are placed in directories like 'dirname_bmp/moviexxxx" in the above file structure. 
    """
    
    batch(fmfconv, 'fmf', params)


def bdir(params):
    dirname = '{0}_{1}'.format(os.path.basename(os.path.abspath('.')), params.itype)
    pardir = defpardir(os.path.abspath('..'), dirname)
    makenewdir(pardir)
    return(pardir)


def fmfconvimg(fmf, params, fdir='.'):
    """Converts a single fmf file to a single image of type 'itype' (like for capfmfs). Image files are placed in a 
    directory such as 'dirname_bmp/moviexxxx" in the above file structure.
    """
    name = os.path.basename(fmf)
    root, ext = os.path.splitext(name)
    #dirname = '{0}_{1}'.format(os.path.basename(os.path.abspath(fdir)), params.itype)
    #pardir = defpardir(os.path.abspath('..'), dirname)
    #makenewdir(pardir)
    #newdir = os.path.join(pardir, root)
    #makenewdir(newdir)
    
    pardir = bdir(params)
    makenewdir(pardir)
    
    cmd = 'fmf2bmps "{0}" --start=1 --stop=1 --extension={1} --outdir="{2}"'.format(fmf, params.itype, pardir)
    os.system(cmd)
    return(pardir)
    


def b_fmfconvimg(params, fdir='.'):
    batch(fmfconvimg, 'fmf', params)
    


def b_wbalr(bdir, params):
    """White balances and rotates images using the -rotate and -recolor functions of ImageMagick 
    using parameters specified in the object 'params'. This batch version is for batch processing 
    the folder 'bdir' which contains multiple image files."""
    
     # Changes into the directory containing the bmp files (a requirement of ImageMagick).
    os.chdir(bdir)
       
    # Batch white balance.
    batch(apply, params.itype, params)
    
    # Makes a directory for the new files. In the above file structure, makes the directory 
    # 'dirname_wbr/moviexxxx'.
    
    pardir = defpardir(os.path.abspath('../..'), 'wbr')
    newdir = os.path.join(pardir, os.path.basename(os.path.abspath('.')))
    makenewdir(newdir)
    
    # Moves files to 'dirname_wbr/moviexxxx'.
    movefiles('.', newdir, params.otype)
    os.chdir(os.path.dirname(os.path.abspath((bdir))))
    

def b_wbalr_fly(bdir, params):
    """White balances and rotates images using the -rotate and -recolor functions of ImageMagick 
    using parameters specified in the object 'params'. This batch version is for batch processing 
    the folder 'bdir' which contains multiple image files."""
    
     # Changes into the directory containing the bmp files (a requirement of ImageMagick).
    os.chdir(bdir)
       
    # Batch white balance.
    batch(apply, params.itype, params)
    
    # Makes a directory for the new files.     
    newdir = defpardir(os.path.abspath('..'), 'wbr')
    makenewdir(newdir)
    
    # Moves files to 'dirname_wbr/moviexxxx'.
    movefiles('.', newdir, params.otype)
    os.chdir(os.path.dirname(os.path.abspath((bdir))))
    


   
def sb_wbalr(params, fdir='.'):
    """Super batch version: white balances and rotates images using the rotate and -recolor 
    functions of ImageMagick using the parameters specified in the object 'params'. This batch 
    version is for batch processing multiple folders in the directory 'fdir', with each 
    folder containing multiple image files.
    """
    
    batch(b_wbalr, '*', params)


def fullbatch(params, fdir='.'):
    """Converts all fmf files located in the directory 'fdir' into image sequences, then white 
    balances and rotates the new images.
    """
    
    b_fmfconv(params)
    
    os.chdir(defpardir(os.path.abspath('..'), params.itype))
    
    # Can also put the change directory function in fmfconv (see comment); ok because batch uses the absolute path.
    sb_wbalr(params, '.')


def movie_fmfconvwb(fmf, params):
    """Converts an fmf file to bmps, white-balances each bmp, and then deletes the bmps. Use this 
    to minimize space usage."""
    
    fmfdir=os.path.dirname(fmf)
    os.chdir(fmfdir)
    fmfconv(fmf, params)
    
    bmpdir = defbmpdir(fmf, params)
    os.chdir(bmpdir)
    
    b_wbalr(bmpdir, params)
    shutil.rmtree(bmpdir)
    
    

def b_movie_fmfconvwb(params, fdir='.'):
    """Converts multiple fmf files to white-balanced jpegs. Uses script that processes each movie 
    in one batch, and then deletes the bmps."""
    
    batch(movie_fmfconvwb, '*', params)
    
    
    
#if __name__ == '__main__':
	# Creates an instance of the class WBalRParams with values for rotating and white-balancing. 
	# To white balance a single image, use the command 'params.apply('filename').
	#params = WBalRParams(rot, r, g, b, itype, otype)
    #params = WBalRParams(0, 1, 1.47, 1.75, 'bmp', 'jpg')
    #b_movie_fmfconvwb(params)
    