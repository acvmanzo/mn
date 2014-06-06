#! /usr/bin/env python

# This module defines functions used for generating 'params' files for use in the dftf module. 
# It extracts values from a summary text file and generates the 'params' file using those values. 
# It is referenced by the executable file 'genparams.py'.
#
# The summary text file should have this format (including the headings):
# Movie	Frame1	Frame_end	Condition	Comments
# movie name	#	#	string	string
#
# Missing values should be replaced with 'x'.
#
# The resulting params files will have this format:
# f1,xx
# f2,xx
# fps,xx
# f_end,xx
# sample_length,xx
# condition,xx
#
# f1 = first frame to use for the dft analysis
# f2 = last frame to use for the dft analysis
# fps = movie sampling rate
# f_end = last good frame for good view of proboscis (f1 to f_end defines a stretch of the movie 
# where proboscis can be easily observed)
# sample_length = # frames used for the dft analysis (should be the same for each movie)
# condition = specific parameter that is being varied in the experiment (ex., 24h or 48h, 100 mM 
# sucrose or 50 mM sucrose).


from mn.params.genparamslib import *
import sys

print('First arg is filename, second arg is fps, third arg is cutoff frame')

fname = sys.argv[1]
fps = int(sys.argv[2])
cutoff = int(sys.argv[3])
genplfc(fname, fps, cutoff)


