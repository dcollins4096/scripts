#!/usr/bin/env python

import sys
import os
import glob
import datetime
from optparse import OptionParser
from xml.dom import minidom

import RunTrackerStuff
import TimeFromString
sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.

sys.path.append(sysInfo.cadacInstall)

import cadac
from cadac import client

filename   = sysInfo.runTrackerXMLname
BackupFile = sysInfo.runTrackerXMLAlternateName

parser = OptionParser(usage = "%prog [options]: \nAlerts simCat to the beginning of the job." )
parser.add_option("-o","--stdout", dest="stdout", action="store",default=None,type="string",
                  help="name of the stdout file written by this job. Default: guessed based on queue system.")
parser.add_option("-e","--stderr", dest="stderr", action="store",default=None,type="string",
                  help="name of the stderr file written by this job. Default: guessed based on queue system.")
parser.add_option("-j","--jobID", dest="jobID", action="store",default=None,type="string",
                  help="name of the job ID. Default: guessed based on queue system.")
parser.add_option("-t","--time", dest="time", action="store",default=None,
                  help='time of submit. format: -t "2008 8 14 3:45" or        \n -t "8 14 3:45"')
parser.add_option("-d","--debug", dest="debug", action="store",default=0,
                  help="debug > 0: Debug info.")

(options, args) = parser.parse_args()

jobID = options.jobID
stderr = options.stderr
stdout = options.stdout
debug  = options.debug

if debug > 0:
    print "jobID", jobID
    print "stder", stderr
    print "stdou", stdout

if stderr == None or stdout == None or jobID == None:
    [jobID,stdout,stderr] = sysInfo.deriveOutputNames(jobID, stdout, stderr, debug)

if debug > 0:
    print "Updating job " , jobID
if glob.glob(filename) != []:
    xmldoc = minidom.parse(filename)    
    jobs = xmldoc.getElementsByTagName('JobID')
    runToUpdate = None
    uuid = []
    if len(jobs) > 1:
        for job in jobs:
            if jobID == None:
                print "GsubStart.py: multiple jobs found, but no jobID specified.  Please specify jobID."
            if debug > 0:
                print  "GsubPostStart checing xml .%s. vs .%s."%(job.firstChild.data,jobID)
            if job.firstChild.data == jobID:
                runToUpdate = job.parentNode
                break
            else:
                print "jobs  don't match!: %s %s"%(job.firstChild.data,jobID)
    else:
        runToUpdate = jobs[0].parentNode
    if runToUpdate != None:
        uuid = runToUpdate.getElementsByTagName('id')
    if len(uuid) == 0:
        print "No UUID for run found.  Writing to Alternate file."
        print "really, you should write the backup code."
    elif len(uuid) > 1:
        print "Too Many UUIDs for run found.  Writing to Alternate file."            
    elif len(uuid) == 1:
        run_id = uuid[0].firstChild.data
        
        #Append start time
        if options.time != None:
            starttime = TimeFromString.TimeFromString(options.time)
        else:
            starttime = datetime.datetime.utcnow().isoformat()

        startXML = minidom.parseString('<StartTime>'+starttime+'</StartTime>').firstChild
        xmldoc.firstChild.appendChild( xmldoc.createTextNode('  ') )
        xmldoc.firstChild.appendChild(startXML)
        xmldoc.firstChild.appendChild( xmldoc.createTextNode('\n') )
        
        #If they exist, make user fields for stderr and stdout
        userFieldArray = []
        if stdout != None:
            userFieldArray.append(cadac.UserField('stdout',stdout))
        if stderr != None:
            userFieldArray.append(cadac.UserField('stderr',stderr))
            
        #print cadac.UserFieldList(userFieldArray).toxml()
        list = xmldoc.getElementsByTagName('UserFieldList')
        if len( userFieldArray ) != 0:
            if len( list ) == 0:
                userList = cadac.UserFieldList(userFieldArray)
                userXML = minidom.parseString(userList.toxml()).firstChild
                xmldoc.firstChild.appendChild( xmldoc.createTextNode('  ') )
                xmldoc.firstChild.appendChild(userXML)
                xmldoc.firstChild.appendChild( xmldoc.createTextNode('\n') )
            elif len(list) == 1:
                for out in userFieldArray:
                    list[0].appendChild( xmldoc.createTextNode('  ') )
                    userXML = minidom.parseString( out.toxml() ).firstChild
                    list[0].appendChild( userXML)
                    list[0].appendChild( xmldoc.createTextNode('\n') )
                    
        #We'll need to update this with a function call in the future.
        update_loc = '/xml/runs/%s' % (run_id)
        #print update_loc
        post_status = client.post(sysInfo.userName,'amrrox',update_loc,xmldoc.toxml())
        if debug > 0:
            print post_status
            
        file = open(filename,'w')
        file.write(xmldoc.toxml())
        file.write('\n') #to shut emacs up.
        file.close
else:
    print "RunTracker File", filename,"not found."
    print "storing start time and job id in Alternate"
    print "Actually, this isn't done yet: you should write code to do this."
    """
    Notes on the backup file:
    1.) make a cadac object with JobID and StartTime
    2.) Open the backup file in read/write mode (make sure it cats the to the end)
    3.) Cat this run to the end.
    """
    
