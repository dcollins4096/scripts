#!/usr/bin/env python


import re
import sys
import glob
#import numpy as np
#nar = np.array
ctid_re = re.compile("CurrentTimeIdentifier =(.*)")
def hmd(seconds):
    hours = int(seconds/3600)
    minutes = int( (seconds - hours*3600)/60)
    seconds_only = seconds - int( seconds/60)*60
    return "%02d:%02d:%02d"%(hours,minutes,seconds_only)

if len(sys.argv) == 1:
    print "job_time.py <list of enzo PFs>"
    print "pulls out CurrentTimeIdentifier and prints the time difference in HH:MM:SS"
else:
    pf_list = sys.argv[2:]

    ctid  = []
    for file in pf_list:
        for line in open(file, 'r'):
            match = ctid_re.match(line)
            if match is not None:
                ctid.append( int(match.group(1)))
                total = hmd( ctid[-1] - ctid[0])
                rel = ""
                if len(ctid) > 1:
                    rel = hmd(ctid[-1]-ctid[-2])
                print "total %s delta %s"%(total, rel)




#end
