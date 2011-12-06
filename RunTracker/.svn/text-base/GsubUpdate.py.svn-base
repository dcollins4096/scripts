#!/usr/bin/env python

import sys
import os
import glob
import datetime
from optparse import OptionParser
from xml.dom import minidom

import RunTrackerStuff
sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.

sys.path.append(sysInfo.cadacInstall)

import cadac
from cadac import client

filename   = sysInfo.runTrackerXMLname

if len(sys.argv) > 1:
    filename = sys.argv[1]

BackupFile = sysInfo.runTrackerXMLAlternateName

parser = OptionParser(usage = "%prog <filename>\nReposts <filename>")
#parser.add_option("-o","--stdout", dest="stdout", action="store",default=None,type="string",
#                  help="name of the stdout file written by this job. Default: guessed based on queue system.")

if glob.glob(filename) != []:
    xmldoc = minidom.parse(filename)    

    uuid = xmldoc.getElementsByTagName('id')
    if len(uuid) == 0:
        print "No UUID for run found: Must post before updating."
    elif len(uuid) > 1:
        print "Too Many UUIDs for run found.  Writing to Alternate file."            
    elif len(uuid) == 1:
        run_id = uuid[0].firstChild.data
        
        update_loc = '/xml/runs/%s' % (run_id)
        post_status = client.post(sysInfo.userName,'amrrox',update_loc,xmldoc.toxml())
else:
    print "Missing file ", filename
