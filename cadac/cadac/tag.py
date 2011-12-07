"""
Implements classes to represent the datatypes and elements found in tag.xsd

http://cadac.sdcs.edu/schema/tag.xsd

Example:
>>> import tag
>>> t = tag.Tag('grad','rpwagner')
>>> print t.toxml()
<?xml version="1.0" encoding="utf-8"?>
<Tag xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd" user="rpwagner">grad</Tag>
>>> u = tag.Tag('grad2','dcollins')
>>> tl = tag.TagList([t,u])
>>> print tl.toxml()
<?xml version="1.0" encoding="utf-8"?>
<TagList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://cadac.sdsc.edu/schema" xsi:schemaLocation="http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd">
  <Tag user="rpwagner">grad</Tag>
  <Tag user="dcollins">grad2</Tag>
</TagList>
"""

from xml_base import XMLBase

class Tag(XMLBase):

    def __init__(self, tag, user):
        self.val = tag
        self.name = 'Tag'
        self.attr = {'user':user}

class TagList(XMLBase):
    
    def __init__(self, tags=[]):
        self.tags = tags
        self.name = 'TagList'
        self.attr = None

    def totuple(self, attr=None):
        tag_tuples = []
        for tag in self.tags:
            tag_tuples.append(tag.totuple())

        if attr:
            t = (self.name,
                 tag_tuples,
                 attr)
        elif self.attr:
            t = (self.name,
                 tag_tuples,
                 self.attr)
        else:
            t = (self.name,
                 tag_tuples)

        return t


def buildTag(et_node):
    return Tag(str(et_node.text), str(et_node.attrib['user']))    

def buildTagList(et_node):

    tags = []

    for childnode in et_node:
        tags.append(buildTag(childnode))

    return TagList(tags)
