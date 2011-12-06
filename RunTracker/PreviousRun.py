



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
    def __init__(self,filename,listOfFields=defaultListOfFields):
        prevDic={}

        #get the xml, make a dictionary.
        PreviousDirectoryName = 'PreviousRunTracker'
        if glob.glob(filename) != []:
            xmldoc = minidom.parse(filename)
            for node in xmldoc.firstChild.childNodes:
                prevDic[ node.nodeName ] = node
            self.prevRun.update( prevDic )
            if glob.glob(PreviousDirectoryName) == []:
                os.mkdir(PreviousDirectoryName)
            previousList = glob.glob(PreviousDirectoryName + "/*")
            number = len(previousList) + 1
            save_file = open("%s/%s.%04d"%(PreviousDirectoryName, filename, number),'w')
            save_file.write(xmldoc.toxml())
            save_file.write('\n')
            save_file.close()
        for name in listOfFields:
            if self.prevRun.has_key(name):
                self.scavengedFields.append( self.prevRun[name] )

        

