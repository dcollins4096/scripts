#!/usr/bin/env python

import sys
import os
import glob
import RunTrackerStuff
import datetime
from xml.dom import minidom


sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
sys.path.append(sysInfo.cadacInstall)

import cadac
from cadac import client


from optparse import OptionParser
parser = OptionParser(usage = "%prog [options] RunList")
parser.add_option("-t","--deltags", dest="deltags", action="store_true",default=False,
                  help='delete tags from runs')
parser.add_option("-p","--post", dest="post", action="store_true",default=False,
                  help='Post')
parser.add_option("-d","--debug", dest="debug", action="store",default=0,
                  help='debug level.')
parser.add_option("-k","--kill", dest="kill", action="store_true",default=False,
                  help='Remove list.')

(options, args) = parser.parse_args()
if options.debug > 0:
    print "options", options
    print "args", args

if len(args) != 1 or glob.glob(args[0]) == []:
    print "MultiPost file"
    print "Posts all runs from file"
else:
    all_runs = minidom.parse(args[0])
    
    runs = all_runs.getElementsByTagName('Run');
    for run in runs:
        uuid_list = run.getElementsByTagName('id')
        if len(uuid_list) == 0:
            uuid = None
        else:
            uuid = run.getElementsByTagName('id')[0]
        if uuid != None:
            run_id = uuid.firstChild.data
        if options.kill:
            update_loc = '/xml/runs/%s' % (run_id)
            print "kill: ", update_loc
            post_status = client.delete(sysInfo.userName,'amrrox',update_loc)

        if options.deltags:
            del_loc = '/xml/runs/%s/tags' % (run_id)
            # 0 is good, otherwise -HTTP response code.
            post_status = client.delete(sysInfo.userName,'amrrox', del_loc)
            print del_loc, post_status
        if options.post:
            if uuid != None:
                update_loc = '/xml/runs/%s' % (run_id)
            else:
                update_loc = '/xml/runs'
            print update_loc
            post_status = client.post(sysInfo.userName,'amrrox',update_loc,run.toxml())

                    

#end
