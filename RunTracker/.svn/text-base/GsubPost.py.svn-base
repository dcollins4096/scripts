#!/usr/bin/env python

import subprocess

import sys
import os
import glob
import RunTrackerStuff
import TimeFromString
import datetime
from xml.dom import minidom


sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
sys.path.append(sysInfo.cadacInstall)

import cadac
from cadac import client

if len(sys.argv) == 1:
    print "GsubPost.py [options] SubmitScript [submit args]"
    print "    Submit job to batch queue, and submit XML to simcat."
    print "    For simCat submission, run GsubAssembleXML.py first."
    print "GsubPost.py -h for more help"
    sys.exit(0)
    

from optparse import OptionParser
parser = OptionParser(usage = "%prog [options] SubmitScript [submit args]")
parser.add_option("-r","--run", dest="postRun", action="store_true",default=False, 
                  help="Submit to the job scheduler. (default doesn't submit)")
parser.add_option("-x","--xml", dest="postXML", action="store_true",default=False,
                  help="Submit to the simCat. (default doesn't submit)")

parser.add_option("-d","--debug", dest="debug", action="store",default=0,
                  help="debug > 0: Debug info.")
parser.add_option("-s","--submitScript", dest="submitScript", action="store",default=None,
                  help="Name of script to submit to scheduler. Required if -r is present.")
parser.add_option("-t","--time", dest="time", action="store",default=None,
                  help='time of submit. format: -t "2008 8 14 3:45" or        \n -t "8 14 3:45"')

(options, args) = parser.parse_args()

postRun    = options.postRun
postXML    = options.postXML
debug      = options.debug
SubmitTime = options.time
jobID      = None

if debug > 0:
    print "postRun =",postRun
    print "postXML =", postXML
    print "opts    =",options
    print "args    =",args

if postRun:
    if debug > 0:
        print "posting Run."
    filename = options.submitScript

    if glob.glob(filename) == []:
        print "GsubPost.py: no file called", filename
        sys.exit(0)
        
    #Parse arguments: systems submit method, this jobs submit script, and any additional arguments.
    command = [sysInfo.submitCommand,filename]
    command.extend(args)
    if debug > 0:
        print "command = " , command

    [myout, myerr]=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    if myout == "":
        print "GsubPost.py: Error.  No stdout from submit."
        print myerr
        sys.exit(1)

    jobID = sysInfo.returnJobID(myout)

    print "=== stdout from", sysInfo.submitCommand,"==="
    print myout
    if len(myerr) > 0:
        print "=== stderr from", sysInfo.submitCommand,"==="
    if debug > 0:
        print "Job id", jobID

if postXML:

    if glob.glob(sysInfo.runTrackerXMLname) == []:
        print "GsubPost.py: Error, Missing XML to submit."
        sys.exit(1)

    xmldoc = minidom.parse(sysInfo.runTrackerXMLname)    

    if postRun or SubmitTime != None:
        if postRun:
            SubmitTime = datetime.datetime.utcnow().isoformat()
        else:
            SubmitTime = TimeFromString.TimeFromString(SubmitTime)

        timeXML = minidom.parseString('<SubmitTime>'+SubmitTime+'</SubmitTime>').firstChild
        space = xmldoc.createTextNode('  ')
        cr = xmldoc.createTextNode('\n')    
        xmldoc.firstChild.appendChild(space)
        xmldoc.firstChild.appendChild(timeXML)
        xmldoc.firstChild.appendChild(cr)

    if postRun and jobID != None:
        jobXML = minidom.parseString('<JobID>'+jobID+'</JobID>').firstChild
        space = xmldoc.createTextNode('  ')
        cr = xmldoc.createTextNode('\n')    
        xmldoc.firstChild.appendChild(space)
        xmldoc.firstChild.appendChild(jobXML)
        xmldoc.firstChild.appendChild(cr)
        
    output= client.post(sysInfo.userName,'amrrox','/xml/runs',xmldoc.toxml())

    if output[0] != 0:
        print "Bad send.  Run not posted!"
    else:

        moreXML = minidom.parseString( output[1] )
        uuid = moreXML.getElementsByTagName('id')[0]

        if len(xmldoc.getElementsByTagName('id')) != 0:
            print "Run cached in RunTracker.xml already has id tag. I'm not a friggin mind reader,"
            print "you deal with it:  the new uuid is"
            print uuid.firstChild.data
        else:
            xmldoc.firstChild.insertBefore(uuid,xmldoc.firstChild.firstChild)
            cr = xmldoc.createTextNode('\n  ')
            xmldoc.firstChild.insertBefore( cr, xmldoc.firstChild.firstChild)
            if debug > 0:
                print "==== new xml ==== "
                print xmldoc.toxml()
            file = open(sysInfo.runTrackerXMLname,'w')
            file.write( xmldoc.toxml() )
            file.write('\n') #to shut emacs up.
            file.close

            #
            # set pending directory, jobId.
            #

            jobId = xmldoc.getElementsByTagName('JobID')
            if len(jobId) != 1 :
                print "Odd number of job IDs for this run:", len(jobId)
            else:
                sysInfo.setPending(str(jobId[0].firstChild.data),str(uuid.firstChild.data))
