#!/usr/bin/env python
"""Convert parameter files from old-style to new-style MHD"""

import sys
def conv(filename):
    infile = open(filename,'r')
    oufile = open(filename+'.new','w')

    for line in infile:
        args = line.split('=')
        newline = None
        if args[0].startswith('MHD_DivBparam'):
            #argument switch taken from the two typedefs.  ugly, yes.
            newline = 'CT_AthenaDissipation = '+args[1]
        elif args[0].startswith("MHD_DivB "):
            newline = 'MHD_CT_Method = %d'%[3,0,-1,-1,-1,2,1,0][int(args[1])]
        elif args[0].startswith("WriteInThis"):
            newline = 'SingleGridDump = '
            for i in args[1:]:
                newline += i + " "
        elif args[0].startswith("MHD_Used "):
            newline = 'useMHDCT = '+args[1]

        if newline:
            if newline[-1] != '\n':
                print newline
                newline += "\n"
            else:
                print newline[:-1]

            oufile.write(newline)
        else:
            oufile.write(line)

    print "HEY!!! making it 5 ghost zones"
    oufile.write("DEFAULT_GHOST_ZONES = 5");
    infile.close()
    oufile.close()
if len(sys.argv) != 2:
    print "pconv.py filename"
    print " converts *filename* to filename.new, for the new mhdct"
else:
    conv(sys.argv[1])
    
#end
