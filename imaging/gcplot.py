#! /usr/bin/env python


from mn.imaging.gclib import *

#~ Start from data folder.

names = glob.iglob('*')
# Absolute path rather than relative path allows changing of directories in fn_name.
names = [os.path.abspath(name) for name in names]
names = sorted(names)
for name in names:
    t = time.strftime('%H:%M:%S')
    print os.path.basename(name), t
    os.chdir(name)
    try:
        plotandsaveplot('raw', RAWFOLDER)
        plotandsaveplot('dff', DFFFOLDER)
        plotandsaveplot('dff_sec', DFFSECFOLDER)
        plotandsaveplot('dffc', DFFCFOLDER)
        plotandsaveplot('dffc_sec', DFFCSECFOLDER)
        plotandsaveplot('dffc_40sec', DFFC40SECFOLDER)
        plotandsaveplot('dff_40sec', DFF40SECFOLDER)

        
    except IOError as e:
        if e.errno == 2:
            continue

