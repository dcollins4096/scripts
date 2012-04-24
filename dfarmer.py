#!/usr/bin/env python

import os, sys
import re

def scrub_output():

    if 'USER' in os.environ:
        user = os.environ['USER']
    else:
        print "No user in environment.  Rework script"
        return -1

    machine = None
    if 'machine' in os.environ:
        machine = os.environ['machine']

    if 'StatFile' in os.environ:
        sptr = open(os.environ['StatFile'])
        slines = sptr.readlines()
        sptr.close()
    else:
        print "No StatFile in environ.  Rework script"
        return -1
    if 'QueuedRuns' in os.environ:
        qptr = open(os.environ['QueuedRuns'])
        qlines = qptr.readlines()
        qptr.close()
    else:
        print "No QueuedRuns in environ.  Rework script"
        return -1

    JobIDs = []
    qhash = {}
    """build has of jobs in queue file."""
    debug = 0
    if debug > 0:
        print "==== ALL QUEUED ===="
    for q in qlines:
        jobid = q.split(" ")[2]
        qhash[jobid] = q[:-1]
        if debug > 0:
            print jobid, qhash[jobid]


    """this can be generalized by machine. Setup for the moab system."""
    trigger_lines = [r'^active jobs',r'^eligible jobs', r'^blocked jobs']

    trigger_reg = [re.compile(lll) for lll in trigger_lines]

    for sl in slines:
        match = None
        sl_split = sl.split(" ")
        if user in sl_split:
            JobIDs.append( sl_split[0])
        for nr, reg in enumerate(trigger_reg):
            match = reg.match(sl)
            if match is not None:
                trigger_reg.pop(nr)
                break
        if match is not None:
            for j in JobIDs:
                if qhash.has_key(j):
                    print qhash[j]
                    qhash.pop(j)
            JobIDs = []
            if debug > 2:
                print "==== Remaining QUEUED ===="
                for q in qhash.keys():
                    print q, qhash[q]

        print sl,
    print "finished jobs ----------"
    for q in qhash.keys():
        queue_machine = qhash[q].split(" ")[1]
        if machine == queue_machine:
            print qhash[q]
            qhash.pop(q)

    print "\n\nother machines ----------"
    for q in qhash.keys():
        print qhash[q]







if __name__ == "__main__":
    scrub_output()



#end
