#!/usr/bin/env python

import sys, glob,datetime, subprocess
import sys
import os
import glob
import datetime
from optparse import OptionParser
from xml.dom import minidom
sys.path.append('/nics/b/home/collins/Research/RunTracker')
import RunTrackerStuff, mergeXML
import TimeFromString
sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
sys.path.append(sysInfo.cadacInstall)
from PreviousRun import PreviousRun
import cadac
from cadac import client


def defaults(dictionary,item,default_value=None):
    if not dictionary.has_key(item):
        return default_value
    else:
        return dictionary[item]

def no_space_split(line, token=" "):
    line_all = line.split(token)
    line_out = []
    for x in line_all:
        if x != "":
            line_out.append(x)
    return line_out

def parse_qhist_ranger(id,filename):
    """Opens the output of qhist, as supplied by Ranger."""

    def parse_time(time):
        month_lookup = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
                        'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        day = int(time[3])
        month = month_lookup[time[2]]
        year = int(time[5])
        hour = int( time[4][0:2])
        minute = int( time[4][3:5])
        return datetime.datetime(year,month,day,hour,minute)
    file = open(filename,'r')
    for line in file:
        spaces = []
        if line.startswith('start_time'):
            l2=no_space_split(line)
            start_dt= parse_time(l2)
        if line.startswith('end_time'):
            l2=no_space_split(line)
            end_dt= parse_time(l2)

    file.close()

    return {'StartTime':start_dt.isoformat(),'EndTime':end_dt.isoformat()}
            

def parse_glsjob_kraken(id,filename):
    """Opens kraken glsjob -u `whoami` file, makes a datetime object for start, end time.
    Format expected should be a dictionary with the things it can find."""
    file = open(filename,'r')
    for line in file:
        if line.find(str(id)) == 0:
            break
    file.close()
    spaces_all = line.split(" ")
    spaces = []
    for x in spaces_all:
        if x != "":
            spaces.append(x)
    queueName = spaces[3]
    processors = int( spaces[5] )
    start_date = [int(x) for x in spaces[7].split("-")]
    start_time = [int(x) for x in spaces[8].split(":")]
    end_date =   [int(x) for x in spaces[9].split("-")]
    end_time =   [int(x) for x in spaces[10].split(":")]
    start_dt = datetime.datetime(start_date[0],start_date[1],start_date[2],start_time[0],start_time[1],start_time[2])
    end_dt = datetime.datetime(end_date[0],end_date[1],end_date[2],end_time[0],end_time[1],end_time[2])
    return {'totalTasks':processors,'StartTime':start_dt.isoformat(),
            'EndTime':end_dt.isoformat(),'queueName':queueName}

def parse_lobo(id,filename):
    """I think this 'qhist parser' doesn't work."""
    pass
def grab_and_post(filename,qhist_filename,style='cvs'):
    """Scrub *filename* for job info.  Timing info comes from *qhist_filename*, if provided.
    """

    command = ['DaveParse.py',filename]
    #This gets actually used later....

    computer = cadac.Computer(sysInfo.computerName, sysInfo.computerLink)
    program  = cadac.Program(sysInfo.programName, sysInfo.programVersion, sysInfo.programLink)
    user     = cadac.User(sysInfo.userName,  sysInfo.userLink)

    if sysInfo.computerName == "Kraken":
        parse_function = parse_glsjob_kraken
    elif sysInfo.computerName == "Ranger":
        parse_function = parse_qhist_ranger
    elif sysInfo.computerName == "Lobo":
        parse_function = parse_lobo
    else:
        print "Computer",sysInfo.computerName,"not recognized"
        return None

    #get job id from filename
    jobID = filename.split(".")[-1]
    if jobID[0] == "e" or jobID[0] == "o":
        jobID = jobID[1:]

    qhist_info = {}
    if qhist_filename != None:
        qhist_info = parse_function(jobID,qhist_filename)

    nodeCount    = defaults(qhist_info,'nodeCount',None)
    totalTasks   = defaults(qhist_info,'totalTasks',None)
    tasksPerNode = defaults(qhist_info,'tasksPerNode',sysInfo.machineProcPerNode)
    jobName      = defaults(qhist_info,'jobName','NoName')
    queueTime    = defaults(qhist_info,'queueTime','None')
    queueName    = defaults(qhist_info,'queueName','queueName')
    SubmitTime   = defaults(qhist_info,'SubmitTime',datetime.datetime(1900,1,1).isoformat())
    StartTime    = defaults(qhist_info,'StartTime',datetime.datetime(1900,1,1).isoformat())
    EndTime      = defaults(qhist_info,'EndTime',datetime.datetime(1900,1,1).isoformat())
    

    if nodeCount == None:
        if totalTasks != None:
            nodeCount = str( int( float(totalTasks)/float(sysInfo.machineProcPerNode) + 0.5))


    baseRunObj = cadac.Run(comp=computer, prog=program, user=user,
                           JobName = jobName, Nodes = nodeCount, TasksPerNode = tasksPerNode,\
                           Queue = queueName, QueueTime = queueTime)

    runXML = minidom.parseString(baseRunObj.toxml())

    Previous   = PreviousRun(sysInfo.runTrackerXMLname)

    for i in PreviousRun.scavengedFields:
        runXML.firstChild.insertBefore(i,runXML.firstChild.firstChild)
        cr = runXML.createTextNode('\n  ')
        runXML.firstChild.insertBefore( cr, runXML.firstChild.firstChild)


    if jobID != None:
        jobXML = minidom.parseString('<JobID>'+str(jobID)+'</JobID>').firstChild
        space = runXML.createTextNode('  ')
        cr = runXML.createTextNode('\n')
        runXML.firstChild.appendChild(space)
        runXML.firstChild.appendChild(jobXML)
        runXML.firstChild.appendChild(cr)
    if SubmitTime != None:
        #SubmitTime = TimeFromString.TimeFromString(SubmitTime)
        timeXML = minidom.parseString('<SubmitTime>'+SubmitTime+'</SubmitTime>').firstChild
        space = runXML.createTextNode('  ')
        cr = runXML.createTextNode('\n')
        runXML.firstChild.appendChild(space)
        runXML.firstChild.appendChild(timeXML)
        runXML.firstChild.appendChild(cr)
    if StartTime != None:
        timeXML = minidom.parseString('<StartTime>'+StartTime+'</StartTime>').firstChild
        space = runXML.createTextNode('  ')
        cr = runXML.createTextNode('\n')
        runXML.firstChild.appendChild(space)
        runXML.firstChild.appendChild(timeXML)
        runXML.firstChild.appendChild(cr)
    if EndTime != None:
        timeXML = minidom.parseString('<EndTime>'+EndTime+'</EndTime>').firstChild
        space = runXML.createTextNode('  ')
        cr = runXML.createTextNode('\n')
        runXML.firstChild.appendChild(space)
        runXML.firstChild.appendChild(timeXML)
        runXML.firstChild.appendChild(cr)

    [myout, myerr]=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(myerr) == 0:
        newXML = minidom.parseString(str(myout))
        runXML = mergeXML.mergeXML(runXML, newXML)
    else:
        print "error with parser:"
        print myerr
        sys.exit(-1)

    return runXML
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "post.py job_output_filename qhist_file <options>" 
    else:
        parser = OptionParser("post.py job_id qhist_file <options>")
        parser.add_option("-p","--post", dest="postRun", action="store_true",default=False,
                          help="Submit xml to simcat")
        parser.add_option("-x","--xml", dest="printXML", action="store_true",default=False,
                          help="print xml to screen")

        (options, args) = parser.parse_args()
        if options.printXML == False and options.postRun == False:
            print "If you select neither -x or -p, all you do is heat the room up by a microkelvin."

        job_output_file = args[0]
        qhist_file = None
        if len(args) > 1:
            qhist_file = args[1]
        xml=grab_and_post(job_output_file,qhist_file)

        if xml == None:
            print "an error was had"
        if options.postRun:
            output= client.post(sysInfo.userName,'amrrox','/xml/runs',xml.toxml())
        if options.printXML:
            print xml.toxml()
#end
