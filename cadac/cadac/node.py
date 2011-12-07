from xml_base import XMLBase

class Node(XMLBase):
    """
    Class used for simple XML nodes, without attributes
    or child nodes, like
      <Foo>Bar</Foo>
    """

    def __init__(self, name, val, attr=None):
        self.name = name
        self.val = val
        self.attr = attr

def buildNode(et_node):

    tag_name = et_node.tag.lstrip('{http://cadac.sdsc.edu/schema}')
    return Node(tag_name, et_node.text, et_node.attrib)
