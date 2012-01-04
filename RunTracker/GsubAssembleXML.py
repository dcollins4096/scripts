#!/usr/bin/env python

import sys
import os
import glob
import datetime
from optparse import OptionParser
from xml.dom import minidom
import RunTrackerStuff
import TimeFromString
Message = """GsubAssembleXML (job script) (Args for native submit)
Assembles XML for simcat.
GsubAssembleXML -h for more help"""
if len(sys.argv) == 1:
    print Message
    sys.exit(0)


sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
sys.path.append(sysInfo.cadacInstall)


from PreviousRun import PreviousRun
import cadac
from cadac import client

parser = OptionParser(usage = "%prog [options] SubmitScript [args for submit script]:\n\tAssemble the XML for simcat from the job script and environment.")
parser.add_option("-d","--debug", dest="debug", action="store",default=0,
                  help="debug > 0: Write XML to std out instead of screen.\ndebug > 1: possibly more verbose output")
parser.add_option("-j","--jobID", dest="jobID", action="store",default=None,
                  help="job ID of existig run.")
parser.add_option("-t","--time", dest="time", action="store",default=None,
                  help='time of submit. format: -t "2008 8 14 3:45" or        \n -t "8 14 3:45"')
(options, args) = parser.parse_args()

if len(args) != 1:
    print Message
    sys.exit(0)


submitFile = args[0]

if glob.glob(submitFile) == []:
    print "Error: File not found" , submitFile
    print Message
    sys.exit(0)
    
debug = options.debug
jobID = options.jobID
SubmitTime = options.time
sysInfo.debug = debug
if debug > 1:
    print "options: ", options
    print "args: " , args

computer = cadac.Computer(sysInfo.computerName, sysInfo.computerLink)
program  = cadac.Program(sysInfo.programName, sysInfo.programVersion, sysInfo.programLink)
user     = cadac.User(sysInfo.userName,  sysInfo.userLink)
jobName      = sysInfo.returnJobName(submitFile)
nodeCount    = sysInfo.returnNodeCount(submitFile)
totalTasks   = sysInfo.returnTaskCount(submitFile)
tasksPerNode = sysInfo.returnTaskPerNode(submitFile)
queueName    = sysInfo.returnQueueName(submitFile)
queueTime    = sysInfo.returnQueueTime(submitFile)

#Run tracker stores Number of Nodes and Tasks Per Node.
#Some systems give Total Number and tasks per node.
#Fix.

if nodeCount == None:
    if totalTasks != None and tasksPerNode != None:
        nodeCount = str( float(totalTasks)/float(sysInfo.machineProcPerNode))
        
account = "acct"
if False:
    baseRunObj = cadac.Run(comp=computer, prog=program, user=user, 
                           JobName = jobName, Nodes = nodeCount, TasksPerNode = tasksPerNode,\
                           Queue = queueName, QueueTime = queueTime)

else:
    pa = []
    pa.append(cadac.Parameter('TopGridDimensions0',128,'google'))
    pa.append(cadac.Parameter('TopGridDimensions1',128,'google'))
    pa.append(cadac.Parameter('TopGridDimensions2',128,'google'))
    plist = cadac.ParameterList(pa)
    baseRunObj = cadac.Run(comp=computer, prog=program, user=user, 
                           JobName = jobName, Nodes = nodeCount, TasksPerNode = tasksPerNode,\
                           Queue = queueName, QueueTime = queueTime,param_list=plist)

runXML = minidom.parseString(baseRunObj.toxml())

if jobID != None:
    jobXML = minidom.parseString('<JobID>'+jobID+'</JobID>').firstChild
    space = runXML.createTextNode('  ')
    cr = runXML.createTextNode('\n')    
    runXML.firstChild.appendChild(space)
    runXML.firstChild.appendChild(jobXML)
    runXML.firstChild.appendChild(cr)

if SubmitTime != None:
    SubmitTime = TimeFromString.TimeFromString(SubmitTime)
    timeXML = minidom.parseString('<SubmitTime>'+SubmitTime+'</SubmitTime>').firstChild
    space = runXML.createTextNode('  ')
    cr = runXML.createTextNode('\n')    
    runXML.firstChild.appendChild(space)
    runXML.firstChild.appendChild(timeXML)
    runXML.firstChild.appendChild(cr)

#
# Info scrubbed from the previous run.  Gets stored in 'scavengedField' array
# in PreviousRun object.  Carriage Returns are for readability only.
# 

Previous   = PreviousRun(sysInfo.runTrackerXMLname)

for i in PreviousRun.scavengedFields:
    runXML.firstChild.insertBefore(i,runXML.firstChild.firstChild)
    cr = runXML.createTextNode('\n  ')
    runXML.firstChild.insertBefore( cr, runXML.firstChild.firstChild)
    
if debug > 0 :
    print runXML.toxml()
else:
    PreviousDirectoryName = 'PreviousRunTracker'
    if glob.glob(PreviousDirectoryName) == []:
        os.mkdir(PreviousDirectoryName)
    file = open("PreviousRunTracker/%s.%04d"%(sysInfo.runTrackerXMLname,1),"w")
    file.write(runXML.toxml())
    file.write('\n') #to shut emacs up.
    file.close
