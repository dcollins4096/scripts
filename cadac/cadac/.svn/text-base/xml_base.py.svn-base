import pyfo

class XMLBase:

    def __init__(self,name, val, attr=None):
        pass

    def totuple(self, attr=None):
        if attr:
            t = (self.name,
                 str(self.val),
                 attr)
        elif self.attr:
            t = (self.name,
                 str(self.val),
                 self.attr)
        else:
            t = (self.name,
                 str(self.val))

        return t
            
        
    def toxml(self):
        
        schema_attr = {"xmlns":"http://cadac.sdsc.edu/schema",
                       "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                       "xsi:schemaLocation":"http://cadac.sdsc.edu/schema http://cadac.sdsc.edu/schema/run.xsd"}

        if self.attr:
            schema_attr.update(self.attr)

        t = self.totuple(schema_attr)
        xml = pyfo.pyfo(t, pretty=True, prolog=True, encoding='utf-8')

        return xml


    def __str__(self):
        return self.toxml()

    def write(self, filename):

        fout = open(filename, 'w')
        fout.write(str(self))
        fout.close()
        
