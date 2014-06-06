#! /usr/bin/env python

import mn.params.genparamslib as genparamslib
import sys

print('First arg is filename, second arg is fps')

FRAMES_FILE = sys.argv[1]
FPS = int(sys.argv[2])

genparamslib.genpdframes(FRAMES_FILE, FPS)
