# Script for opening a series of jpg files.

import os
import glob
import mn.cmn.cmn as cmn
import shutil
import sys

movie = sys.argv[1]

os.chdir(movie)
num = len(os.listdir('.'))
files = sorted([os.path.abspath(x) for x in os.listdir('.')])
first = files[0]

arg = str(num) + '%' + first

cmd = 'java -jar /home/andrea/software/ImageJ/ij.jar'+
' -macro /home/andrea/software/ImageJ/macros/openser.txt {0}&'.format(arg)

os.system(cmd)
