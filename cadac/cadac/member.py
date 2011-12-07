from xml_base import XMLBase
from node import Node


class Member(XMLBase):

    def __init__(self, username, name=None, url=None):
        self.val = None
        self.name = 'Member'
        self.childnodes = [Node('UserName', username)]
        self.attr = None

        if name:
            self.childnodes.append(Node('Name',name))

        if url:
            self.childnodes.append(Node('PersonalSite',url))

    def get_values(self):

        username = name = url = ""
        for node in self.childnodes:
            tag_name = node.name
            if tag_name == 'UserName':
                username = node.val
            elif tag_name == 'Name':
                name = node.val
            elif tag_name == 'PersonalSite':
                url = node.val

        return username, name, url
        

    def totuple(self, attr=None):

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


class MemberList(XMLBase):
    
    def __init__(self, members=[]):
        self.members = members
        self.name = 'MemberList'
        self.attr = None

    def totuple(self, attr=None):
        member_tuples = []
        for member in self.members:
            member_tuples.append(member.totuple())

        if attr:
            t = (self.name,
                 member_tuples,
                 attr)
        elif self.attr:
            t = (self.name,
                 member_tuples,
                 self.attr)
        else:
            t = (self.name,
                 member_tuples)

        return t


def buildMember(et_node):

    username = name = url = None
    for node in et_node:
        tag_name = node.tag.lstrip('{http://cadac.sdsc.edu/schema}')
        if tag_name == 'UserName':
            username = node.text
        elif tag_name == 'Name':
            name = node.text
        elif tag_name == 'PersonalSite':
            url = node.text

    return Member(username, name, url)

def buildMemberList(et_node):

    members = []

    for childnode in et_node:
        members.append(buildMember(childnode))

    return MemberList(members)

def readXML(xmlstring):

    import xml.etree.ElementTree as ET

    elem = ET.fromstring(xmlstring)
    
    if elem.tag.endswith('MemberList'):
        out = buildMemberList(elem)
    else:
        out = buildMember(elem)

    return out
