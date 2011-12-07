import httplib
import sys
import os
from string import rfind
import base64
import datetime

import xml.etree.ElementTree as ET

def getconfig():
    hdir = os.getenv('HOME')
    conf = open(hdir +'/.cadac')
    lines = conf.readlines()
    conf.close()

    for i in range(0,len(lines)):
        lines[i] = lines[i].split()

    # file contents
    # name userurl
    # passwd
    # machinename machineurl

    # user name, passwd
    if len(lines[0]) == 2:
        user = User(lines[0][0], lines[1][0], lines[0][1])
    else:
        user = User(lines[0][0])
    
    if len(lines[2]) == 2:
        comp = User(lines[2][0], lines[2][1])
    else:
        comp = User(lines[2][0])

    return user, comp


def postSubmitTime(jobid):

    user, comp = getconfig()

    subtime = datetime.datetime.utcnow().isoformat()

    
    xq = u'declare namespace sim="http://cadac.sdsc.edu/simulation";\n'
    xq += u'for $run in //sim:Run[sim:JobID="%s"][sim:Computer="%s"]\n' % (jobid, comp.value)
    xq += u'let $sub := concat("<",$run/name(),">","%s","</",$run/name(),">")\n' % subtime
    xq += u'let $sub := util:eval(replace($sub,"Run","SubmitTime"))\n'
    xq += u'return\n'
    xq += u'  update insert $sub into $run\n'
   
    postQuery(xq, user.value, user.passwd)


def postStartTime(jobid):

    user, comp = getconfig()

    starttime = datetime.datetime.utcnow().isoformat()
    
    xq = u'declare namespace sim="http://cadac.sdsc.edu/simulation";\n'
    xq += u'for $run in //sim:Run[sim:JobID="%s"][sim:Computer="%s"]\n' % (jobid, comp.value)
    xq += u'let $start := concat("<",$run/name(),">","%s","</",$run/name(),">")\n' % starttime
    xq += u'let $start := util:eval(replace($start,"Run","StartTime"))\n'
    xq += u'return\n'
    xq += u'  update insert $start into $run\n'
   
    postQuery(xq, user.value, user.passwd)

def postEndTime(jobid):

    user, comp = getconfig()

    stoptime =  = datetime.datetime.utcnow().isoformat()

    xq = u'declare namespace sim="http://cadac.sdsc.edu/simulation";\n'
    xq += u'for $run in //sim:Run[sim:JobID="%s"][sim:Computer="%s"]\n' % (jobid, comp.value)
    xq += u'let $stop := concat("<",$run/name(),">","%s","</",$run/name(),">")\n' % stoptime
    xq += u'let $stop := util:eval(replace($stop,"Run","EndTime"))\n'
    xq += u'return\n'
    xq += u'  update insert $stop into $run\n'
   
    postQuery(xq, user.value, user.passwd)


def postQuery(xq_in, username=None, passwd=None):

    if username:
        userpass = username + u':' + passwd
        userpass = base64.encodestring(userpass).strip()
        authorization = u'Basic ' + userpass
    else:
        authorization = None

    xq = u'<?xml version="1.0" encoding="UTF-8"?>\n'
    xq += u'<query xmlns="http://exist.sourceforge.net/NS/exist">\n'
    xq += u'<text><![CDATA[\n'
    xq += xq_in
    xq +=u']]></text>\n'
    xq +=u'</query>\n'
   
    con = httplib.HTTP('lca.ucsd.edu')
    con.putrequest('POST', '/xmldb/devel/')
    con.putheader('Content-Type', 'text/xml')
    clen = len(xq)
    con.putheader('Content-Length', `clen`)
    if authorization:
        con.putheader('Authorization', authorization)
    con.endheaders()
    con.send(xq)

    errcode, errmsg, headers = con.getreply()
    
    #print con.file.read()


def deleteFromCADAC(self, filename, username='rpwagner',password='bin13nri'):
    collection = 'devel/simulations'
    
    userpass = username + ':' + password
    userpass = base64.encodestring(userpass).strip()
    authorization = 'Basic ' + userpass

    con = httplib.HTTP('lca.ucsd.edu')
    con.putrequest('DELETE', '/xmldb/%s/%s' % (collection, filename))
    con.putheader('Authorization', authorization)
    con.endheaders()

    errcode, errmsg, headers = con.getreply()

    if errcode != 200:
        f = con.getfile()
        print 'Error %d occurred: %s' % (errcode, errmsg)
        f.close()

def queryRun(jobid, computer):

    xq = u'     declare namespace sim="http://cadac.sdsc.edu/simulation";\n'
    xq += u'         for $run in //sim:Run[sim:JobID="%s"][sim:Computer="%s"]\n' % (jobid, computer)
    xq += u'         return $run'

    postQuery(xq)

class LinkType:
    
    def __init__(self,name,value,url=None):
        self.name = unicode(name)
        self.value = unicode(value)
        self.url = unicode(url)

    def addElement(self, parentEl):
        nameEl = ET.SubElement(parentEl, self.name)
        nameEl.text = self.value
        if self.url:
            nameEl.set("url",self.url)

        return nameEl

class User(LinkType):
    def __init__(self, name, passwd, url=None):
        LinkType.__init__(self, 'cadacUser', name, url)
        self.passwd = unicode(passwd)

class Computer(LinkType):
    def __init__(self, name, url=None):
        LinkType.__init__(self, 'Computer', name, url)

class Program(LinkType):
    def __init__(self, name, version=None, url=None):
        self.version = version
        LinkType.__init__(self, 'Program', name, url)

    def addElement(self, parentEl):
        nameEl = LinkType.addElement(self, parentEl)
        if self.version:
            nameEl.set("version",self.version)

class Parameter:
    def __init__(self, paramname, value, refurl=None):
        self.parameter = LinkType('Parameter', paraname, refurl)
        self.value = value


class Run:
    
    def __init__(self, computer, program, cadacuser, jobid,
                 jobname=None, nodes=None, tasksper=None,
                 queue=None, account=None):
        self.computer = computer
        self.program = program
        self.cadacuser = cadacuser
        self.jobid = jobid
        self.jobname = jobname
        self.nodes = nodes
        self.tasksper =tasksper
        self.queue = queue
        self.account = account

    def addElements(self, simEl):

        runEl = ET.SubElement(simEl, "Run")

        self.computer.addElement(runEl)
        self.program.addElement(runEl)
        self.cadacuser.addElement(runEl)

        jobidEl = ET.SubElement(runEl, "JobID")
        jobidEl.text = self.jobid

        if self.jobname:
            newEl = ET.SubElement(runEl, "JobName")
            newEl.text = self.jobname
        if self.nodes:
            newEl = ET.SubElement(runEl, "Nodes")
            newEl.text = self.nodes
        if self.tasksper:
            newEl = ET.SubElement(runEl, "TasksPerNode")
            newEl.text = self.tasksper
        if self.queue:
            newEl = ET.SubElement(runEl, "Queue")
            newEl.text = self.queue
        if self.account:
            newEl = ET.SubElement(runEl, "Account")
            newEl.text = self.account


class Simulation:

    def __init__(self, name, description=None, runs=[]):
        self.name = name
        self.description = description
        self.runs = runs
    
    def buildElement(self):
        simEl = ET.Element('Simulation')
        simEl.set('xmlns',"http://cadac.sdsc.edu/simulation")
        simEl.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        simEl.set('xsi:schemaLocation', "http://cadac.sdsc.edu/simulation http://cadac.sdsc.edu/schema/simulation.xsd")

        nameEl = ET.SubElement(simEl, "Name")
        nameEl.text = self.name

        if self.description:
            descEl = ET.SubElement(simEl, "Description")
            descEl.text = self.description
            
        for run in self.runs:
            run.addElements(simEl)
            
        return simEl

    def writeXML(self, filename):
        simEl = self.buildElement()
        tree = ET.ElementTree(simEl)
        decl = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        f = open(filename,'w')
        f.write(decl)
        tree.write(f, encoding="utf-8")
        f.close()

    def getXML(self):
        simEl = self.buildElement()
        decl = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        return decl + ET.tostring(simEl, encoding='utf-8')

    def postToCADAC(self, filename, username='rpwagner',password='bin13nri'):

        xml = self.getXML()
        
        collection = 'devel/simulations'

        userpass = username + ':' + password
        userpass = base64.encodestring(userpass).strip()
        authorization = 'Basic ' + userpass

        con = httplib.HTTP('lca.ucsd.edu')
        con.putrequest('PUT', '/xmldb/%s/%s' % (collection, filename))
        con.putheader('Content-Type', 'text/xml')
        clen = len(xml)
        con.putheader('Content-Length', `clen`)
        con.putheader('Authorization', authorization)

        con.endheaders()
        con.send(xml)

        errcode, errmsg, headers = con.getreply()

        if errcode != 200 and errcode != 201:
            f = con.getfile()
            print 'Error %d occurred: %s' % (errcode, errmsg)
            f.close()

