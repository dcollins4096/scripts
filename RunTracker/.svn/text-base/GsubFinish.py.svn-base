#!/usr/bin/env python

from optparse import OptionParser
from xml.dom import minidom
import subprocess
import glob
import sys
import datetime
import TimeFromString
import RunTrackerStuff
import mergeXML

sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
sys.path.append(sysInfo.cadacInstall)

from PreviousRun import PreviousRun
import cadac
from cadac import client



parser = OptionParser()
parser.add_option("-o","--stdout", dest="stdout", action="store",default=None,type="string",
                  help="name of the stdout file written by this job. Default: guessed based on queue system, if not found in the file.")
parser.add_option("-e","--stderr", dest="stderr", action="store",default=None,type="string",
                  help="name of the stderr file written by this job. Default: guessed based on queue system, if not found in the file")
parser.add_option("-j","--jobID", dest="jobID", action="store",default=None,type="string",
                  help="name of the job ID. Default: guessed based on queue system.")
parser.add_option("-x","--executable", dest="executable", action="store",default="DaveParse.py",type="string",
                  help="Name of executable to parse output.")
parser.add_option("-b","--begin", dest="start", action="store",default=None,
                  help='Begin time. format: -t "2008 8 14 3:45" "8 14 3:45"')
parser.add_option("-f","--finish", dest="end", action="store",default=None,
                  help='Finish time. format: -t "2008 8 14 3:45" "8 14 3:45"')
parser.add_option("-d","--debug", dest="debug", action="store",default=0,
                  help="debug > 0: Debug info.")

(options, args) = parser.parse_args()

jobID = None
stderr = None
stdout = None
debug = options.debug
[jobID, stdout,stderr] = sysInfo.deriveOutputNames(jobID, stderr, stdout,debug)
if options.jobID != None:
    jobID = options.jobID
if options.stderr != None:
    stderr = options.stderr
if options.stdout != None:
    stdout = options.stdout

if debug > 0:
    print "jobID", jobID
    print "stder", stderr
    print "stdou", stdout
    
filename   = sysInfo.runTrackerXMLname

if glob.glob(filename) == []:
    extant_xml = minidom.parseString("<Run></Run>")
else:
    extant_xml = minidom.parse(filename)

runToUpdate = None
uuid = []
jobs = extant_xml.getElementsByTagName('JobID')
if len(jobs) > 1:
    for job in jobs:
        if job.firstChild.data == jobID:
            runToUpdate = job.parentNode
            break
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

#Find stderr and stdout from the run.
fields=runToUpdate.getElementsByTagName('UserField')
for f in fields:
    for k in f.attributes.keys():
        if f.attributes[k].value == 'stderr':
            stderr = f.firstChild.data
        if f.attributes[k].value == 'stdout':
            stdout = f.firstChild.data


if options.start != None:
    starttime = TimeFromString.TimeFromString(options.start)
    endXML = minidom.parseString('<StartTime>'+starttime+'</StartTime>').firstChild
    extant_xml.firstChild.appendChild( extant_xml.createTextNode('  ') )
    extant_xml.firstChild.appendChild(endXML)
    extant_xml.firstChild.appendChild( extant_xml.createTextNode('\n') )
    
if options.end != None:
    endtime = TimeFromString.TimeFromString(options.end)
    endXML = minidom.parseString('<EndTime>'+endtime+'</EndTime>').firstChild
    extant_xml.firstChild.appendChild( extant_xml.createTextNode('  ') )
    extant_xml.firstChild.appendChild(endXML)
    extant_xml.firstChild.appendChild( extant_xml.createTextNode('\n') )



#If not found, lookup stderr and stdout.

if options.executable != None and options.stderr != None:
    
    command = [options.executable]
    if jobID != None:
        command.extend(["-j",str(jobID)])
    if stderr != None:
        command.extend(["-e", stderr])
    if stdout != None:
        command.extend(["-o", stdout])

    [myout, myerr]=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()    
    
    if len(myerr) == 0:
        newXML = minidom.parseString(str(myout))
        extant_xml = mergeXML.mergeXML(extant_xml, newXML)
    else:
        print "GsubFinish: scrub script failed"
        print command
        print "=== stdout ===", myout
        print "=== stderr ===", myerr
update_loc = '/xml/runs/%s' % (run_id)
##print update_loc
if debug > 1:
    print "Not posting run"
else:
    post_status = client.post(sysInfo.userName,'amrrox',update_loc,extant_xml.toxml())
#print post_status
#print extant_xml.toxml()
if debug > 1:
    print "=== new xml ==="
    print extant_xml.toxml()
else:
    file = open(filename,'w')
    file.write(extant_xml.toxml())
    file.write('\n') #to shut emacs up.
    file.close
    
