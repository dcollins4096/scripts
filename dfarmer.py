#!/usr/bin/env python

import os, sys
import re
import datetime

def scrub_output(options):

    verbose = not (options.finished + options.running +options.queue + options.blocked + options.monitor)

    actions = []
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
    trigger_lines = [r'^active jobs',r'^eligible jobs', r'^blocked jobs',r'^Total']
    trigger_bool = [False, options.running, options.queue, options.blocked]
    monitor_bool = [False, options.monitor, False,False]
    running_list = []

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
                print_this = trigger_bool.pop(nr)
                monitor = monitor_bool.pop(nr)
                break
        if match is not None:
            for j in JobIDs:
                if qhash.has_key(j):
                    if verbose or print_this:
                        print qhash[j]
                    this_job = qhash.pop(j)
                    if monitor:
                        running_list.append(this_job)
            JobIDs = []
            if debug > 2:
                print "==== Remaining QUEUED ===="
                for q in qhash.keys():
                    print q, qhash[q]

        if verbose:
            print sl,
    if verbose:
        print "finished jobs ----------"

    def output_from_job_string(job_string):
        subtime, machine, id, path = job_string.split(" ")
        return "%s/slurm-%s.out"%(path,id)
    def id_from_job_string(job_string):
        subtime, machine, id, path = job_string.split(" ")
        return id
    machine_kill = "mjobctl -c"

    if options.monitor:
        for job in running_list:
            filename = output_from_job_string(job)
            id = id_from_job_string(job)
            if os.path.exists(filename):
                time = os.path.getmtime(filename)
                now = datetime.datetime.now()
                stamp = datetime.datetime.fromtimestamp(time)
                seconds = (now-stamp).seconds
                #print filename, "\n\t",stamp, "\n\t",now, "\n\t",stamp-now,"\n\t",seconds
                if seconds > options.monitor_minutes*60:
                    if options.kill:
                        fptr = open(filename,"a")
                        fptr.write('\n\ndfarmer: killing due to inactivity,%d> %d minutes\n\n\n'%(seconds/60.,options.monitor_minutes))
                        fptr.close()
                        print '%s %s'%(machine_kill,id)
                    else:
                        print filename
        
    for q in qhash.keys():
        queue_machine = qhash[q].split(" ")[1]
        if machine == queue_machine:
            if options.finished or verbose:
                print qhash[q]
            qhash.pop(q)

    if not options.local and verbose:
        print "\n\n=========== other machines ===========\n"
        for q in qhash.keys():
            print qhash[q]





from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l","--local",dest="local",action="store_true",default=False,
                      help="ignore other machines in queue file")
parser.add_option("-f","--finished",dest="finished",action="store_true",default=False,
                      help="Only show finished jobs")
parser.add_option("-r","--running",dest="running",action="store_true",default=False,
                      help="Only show currently running jobs")
parser.add_option("-q","--queue",dest="queue",action="store_true",default=False,
                      help="Only show currently queued jobs")
parser.add_option("-b","--blocked",dest="blocked",action="store_true",default=False,
                      help="Only show currently blocked jobs")
parser.add_option("-m","--monitor", dest="monitor", action ="store_true",default=False,
                  help="Monitor reports all jobs whos output file is more than dt minuts old.")
parser.add_option("-k","--kill", dest="kill", action ="store_true",default=False,
                  help="Kills jobs older than t minutes old")
parser.add_option("-t","--monitor_minutes", dest="monitor_minutes", default=20,
                  help="Time window in minutes for monitor response")

(options,args)=parser.parse_args()
if options.kill:
    options.monitor=True
if __name__ == "__main__":
    scrub_output(options)



#end
