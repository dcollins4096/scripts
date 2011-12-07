"""
Implements classes to represent the datatypes and elements found in link.xsd

http://cadac.sdcs.edu/schema/link.xsd

Example:
>>> import link
>>> l = link.LinkType('Computer','Cobalt','http://ncsa.uiuc.edu')
>>> print l.toxml()
<?xml version="1.0" encoding="utf-8"?>
<Computer url="http://ncsa.uiuc.edu" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd">Cobalt</Computer>

"""

from xml_base import XMLBase

class LinkType(XMLBase):

    def __init__(self, name, val, url=None):
        self.val = val
        self.name = name
        if url:
            self.attr = {'url':url}
        else:
            self.attr = None

