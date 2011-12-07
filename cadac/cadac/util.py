def xml_value(xml_tag):
    "xml_valueGiven an xml tag of the form <head>\n<tagName attrs>value</tagNam\
e>, returns value"

    import re

    match = re.match(r"((.*)\n)?(<[^>]*>([^<]*))", xml_tag)
    if match != None:
        return match.group(4)
    else:
        print "No match"
    #print " "                                                                  
    #print xml_tag                                                              
    return ""


