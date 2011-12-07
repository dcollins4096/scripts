"""
Implements classes to represent the datatypes and elements found in userfield.xsd

http://cadac.sdcs.edu/schema/parameter.xsd

Example:
>>> import userfield
>>> u = userfield.UserField('mach',2.0)
>>> print u.toxml()
<?xml version="1.0" encoding="utf-8"?>
<UserField xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd" name="mach">2.0</UserField>
>>> v = userfield.UserField('clfd',0.125)
>>> ul = userfield.UserFieldList([u,v])
>>> print ul.toxml()
<?xml version="1.0" encoding="utf-8"?>
<UserFieldList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd">
  <UserField name="mach">2.0</UserField>
  <UserField name="clfd">0.125</UserField>
</UserFieldList>
>>>  

"""

from xml_base import XMLBase

class UserField(XMLBase):

    def __init__(self, name, val):
        self.name = 'UserField'
        self.val = val
        self.attr = {'name':name}


class UserFieldList(XMLBase):
    
    def __init__(self, userfields=[]):
        self.userfields = userfields
        self.name = 'UserFieldList'
        self.attr = None

    def totuple(self, attr=None):
        userfield_tuples = []
        for userfield in self.userfields:
            userfield_tuples.append(userfield.totuple())

        if attr:
            t = (self.name,
                 userfield_tuples,
                 attr)
        elif self.attr:
            t = (self.name,
                 userfield_tuples,
                 self.attr)
        else:
            t = (self.name,
                 userfield_tuples)

        return t


def buildUserField(et_node):

    return UserField(et_node.attrib['name'],
                     et_node.text)

def buildUserFieldList(et_node):


    userfields = []

    for childnode in et_node:
        userfields.append(buildUserField(childnode))
    return UserFieldList(userfields)
