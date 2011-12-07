"""
Implements classes to represent the datatypes and elements found in run.xsd

http://cadac.sdcs.edu/schema/run.xsd
"""

from xml_base import XMLBase
from link import LinkType
from node import Node


short_list = ('id','Name','Computer','Program','User',
              'Successful','JobID','JobName','Nodes',
              'TasksPerNode','Queue','Account','SubmitTime',
              'StartTime','EndTime','Simulation')


class User(LinkType):

    def __init__(self,username, url=None):
        LinkType.__init__(self,'User',username, url)


class Computer(LinkType):

    def __init__(self,name, url=None):
        LinkType.__init__(self,'Computer',name, url)


class id(LinkType):

    def __init__(self,id, url=None):
        LinkType.__init__(self,'id',id, url)   


class Run(XMLBase):

    def __init__(self, name=None, comp=None, prog=None, user=None, id=None,
                 user_fields=None, tag_list=None, param_list=None,
                 **kwargs):
        
        self.attr = None
        self.name = 'Run'
        self.childnodes = []

        if name:
            if isinstance(name, str):
                name = Node('Name',name)
            elif isinstance(name,unicode):
                name = Node('Name',name)                
            self.childnodes.append(name)

        if comp:
            self.childnodes.append(comp) 
        if prog:
            self.childnodes.append(prog) 
        if user:
            self.childnodes.append(user) 

        if id:
            self.childnodes.append(id)

        for key in kwargs:
            n = Node(key, kwargs[key])
            self.childnodes.append(n)

        if user_fields:
            self.childnodes.append(user_fields)

        if tag_list:
            self.childnodes.append(tag_list)

        if param_list:
            self.childnodes.append(param_list)

    def totuple(self, attr=None, fmt='long'):

        if fmt=='short':
            outnodes = []
            for node in self.childnodes:
                if node.name in short_list:
                    outnodes.append(node.totuple())
        else:
            outnodes = []
            for node in self.childnodes:
                outnodes.append(node.totuple())
        
        if attr:
            t = (self.name,
                 outnodes,
                 attr)
        elif self.attr:
            t = (self.name,
                 outnodes,
                 self.attr)
        else:
            t = (self.name,
                 outnodes)

        return t

class RunList(XMLBase):
    
    def __init__(self, runs=[], fmt='long'):
        self.runs = runs
        self.name = 'RunList'
        self.attr = None
        self.fmt = fmt

    def totuple(self, attr=None):
        run_tuples = []
        for run in self.runs:
            run_tuples.append(run.totuple(fmt=self.fmt))

        if attr:
            t = (self.name,
                 run_tuples,
                 attr)
        elif self.attr:
            t = (self.name,
                 run_tuples,
                 self.attr)
        else:
            t = (self.name,
                 run_tuples)

        return t

    def toxml(self, fmt=None):

        my_fmt = None

        if fmt:
            my_fmt = self.fmt
            self.fmt = fmt

        my_xml = XMLBase.toxml(self)
        print my_xml
        if fmt:
            self.fmt = my_fmt

        return my_xml

def readXML(xmlstring):

    import xml.etree.ElementTree as ET

    elem = ET.fromstring(xmlstring)
    
    if elem.tag.endswith('RunList'):
        out = buildRunList(elem)
    else:
        out = buildRun(elem)

    return out

def buildRunList(et_node):
    runs = []

    for childnode in et_node:
        runs.append(buildRun(childnode))
    return RunList(runs)

def buildid(et_node):
    return id(et_node.text, et_node.attrib['url'])

def buildUser(et_node):
    return User(et_node.text, et_node.attrib['url'])

def buildComputer(et_node):
    return Computer(et_node.text, et_node.attrib['url'])

def buildRun(run_node):

    import node, parameter, program, tag, userfield

    node_map = {'id':buildid, 'Name':node.buildNode,
                'Description':node.buildNode,
                'Computer':buildComputer,
                'Program':program.buildProgram,
                'Simulation':program.buildNode,
                'User':buildUser,
                'Comments':node.buildNode,
                'ToDo':node.buildNode,
                'Successful':node.buildNode,
                'JobID':node.buildNode,
                'JobName':node.buildNode,
                'Nodes':node.buildNode,
                'TasksPerNode':node.buildNode,
                'Queue':node.buildNode,
                'QueueTime':node.buildNode,
                'Account':node.buildNode,
                'SubmitTime':node.buildNode,
                'StartTime':node.buildNode,
                'EndTime':node.buildNode,
                'UserFieldList':userfield.buildUserFieldList,
                'TagList':tag.buildTagList,
                'ParameterList':parameter.buildParameterList}

    new_run = Run()

    for node in run_node:
        tag_name = node.tag.lstrip('{http://cadac.sdsc.edu/schema}')
        new_run.childnodes.append(node_map[tag_name](node))

    return new_run
