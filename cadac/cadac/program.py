"""
Implements classes to represent the datatypes and elements found in program.xsd

http://cadac.sdcs.edu/schema/parameter.xsd

Example:
>>> import program
>>> p = program.Program('Enzo',1.0,'http://lca.ucsd.edu/enzo')
>>> print p.toxml()
<?xml version="1.0" encoding="utf-8"?>
<Program url="http://lca.ucsd.edu/enzo" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd" version="1.0">Enzo</Program>
>>> 
"""

from xml_base import XMLBase
from link import LinkType


class Program(LinkType):

    def __init__(self, name, version=None, url=None):
        LinkType.__init__(self, 'Program',name,url)
        
        if version:
            d = {'version':version}
            if self.attr:
                self.attr.update(d)
            else:
                self.attr = d

def buildProgram(et_node):
    return Program(et_node.text, et_node.attrib['version'], et_node.attrib['url'])
