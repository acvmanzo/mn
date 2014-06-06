#! /usr/bin/env python

from mn.imaging.gclib import *

#~ Start from data folder.
kfile = os.path.join(os.path.dirname(os.path.abspath('.')), 'keylist')
K = load_keys(kfile)

batch_writemetrics()
print(summdir())
os.chdir(summdir())
plotgraphs(summfile('dff'), K)
plotgraphs(summfile('dffc'), K)
