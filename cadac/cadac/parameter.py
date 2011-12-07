"""
Implements classes to represent the datatypes and elements found in parameter.xsd

http://cadac.sdcs.edu/schema/parameter.xsd

Example:
>>> import parameter
>>> p = parameter.Parameter('cosmo',1.0,'http://lca.ucsd.edu')
>>> print p.toxml()
<?xml version="1.0" encoding="utf-8"?>
<Parameter url="http://lca.ucsd.edu" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd" name="cosmo">1.0</Parameter>
>>> q = parameter.Parameter('gosmo',2.0,'http://ppcluster.ucsd.edu')
>>> pl = parameter.ParameterList([p,q])
>>> print pl.toxml()
<?xml version="1.0" encoding="utf-8"?>
<ParameterList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd">
  <Parameter url="http://lca.ucsd.edu" name="cosmo">1.0</Parameter>
  <Parameter url="http://ppcluster.ucsd.edu" name="gosmo">2.0</Parameter>
</ParameterList>
>>> 


"""

from xml_base import XMLBase
from link import LinkType


class Parameter(LinkType):

    def __init__(self, name, val, url=None):
        LinkType.__init__(self, 'Parameter',val,url)
        d = {'name':name}
        if self.attr:
            self.attr.update(d)
        else:
            self.attr = d

class ParameterList(XMLBase):
    
    def __init__(self, params=[]):
        self.params = params
        self.name = 'ParameterList'
        self.attr = None

    def totuple(self, attr=None):
        param_tuples = []
        for param in self.params:
            param_tuples.append(param.totuple())

        if attr:
            t = (self.name,
                 param_tuples,
                 attr)
        elif self.attr:
            t = (self.name,
                 param_tuples,
                 self.attr)
        else:
            t = (self.name,
                 param_tuples)

        return t


def buildParameter(et_node):
    return Parameter( et_node.attrib['name'], 
                      et_node.text, et_node.attrib['url'])    

def buildParameterList(et_node):

    parameters = []
    for childnode in et_node:
        parameters.append(buildParameter(childnode))

    return ParameterList(parameters)
