

import os
import shutil
import mn.plot.genplotlib as gpl
import matplotlib.pyplot as plt
from mn.plot.gfplot import *


d = gendictgf('pooled_cibpump.txt')[0]
md = genpercent_m(d)
writedata_matlab(md)
