#!/usr/bin/env python

import sys
import os
import glob
import RunTrackerStuff

sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.


pending = sysInfo.returnPending()

for p in pending:
    dir = p['directory']
    print "Working dir",dir
    os.chdir(dir)
    
