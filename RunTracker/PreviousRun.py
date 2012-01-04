



import sys
import os
import glob
from xml.dom import minidom
import datetime

import RunTrackerStuff

class PreviousRun:

    sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
    sys.path.append(sysInfo.cadacInstall)
    import cadac

    Name = minidom.parseString('<Name>name</Name>').firstChild
    Description = minidom.parseString('<Description>what it is</Description>').firstChild
    Comments = minidom.parseString('<Comments>What It Was</Comments>').firstChild
    ToDo = minidom.parseString('<ToDo>what it shall be.</ToDo>').firstChild

    
    TagList = minidom.parseString( cadac.TagList( [cadac.Tag('NoTags',sysInfo.userName)] ).toxml() ).firstChild
    UserList = None
    ParameterList = None
    defaultListOfFields = ['TagList','ToDo','Comments','Description','Name']
    scavengedFields = []
    #These I will want as defaults.  Stick them in the dictionary.
    prevRun = {'Name':Name,'Description':Description,'Comments':Comments,'ToDo':ToDo,'TagList':TagList}
    def __init__(self,listOfFields=defaultListOfFields):
        prevDic={}

        #get the xml, make a dictionary.
        PreviousDirectoryName = 'PreviousRunTracker'
        previousList = sorted(glob.glob(PreviousDirectoryName + "/*"))
        last_file = previousList[-1]
        xmldoc = minidom.parse(last_file)
        for node in xmldoc.firstChild.childNodes:
            prevDic[ node.nodeName ] = node
        self.prevRun.update( prevDic )
        for name in listOfFields:
            if self.prevRun.has_key(name):
                self.scavengedFields.append( self.prevRun[name] )

        

