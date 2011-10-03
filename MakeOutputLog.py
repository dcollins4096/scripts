#!/usr/bin/env python

#
#  Make's OutputLog file from enzo files in the directory tree.
#

import fnmatch
import os
import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H","--Hierarchy",dest="hierarchy",action="store_true",default=False,
                      help="takes list of hierarchy files")
(options,args)=parser.parse_args()
if glob.glob('OutputLog') != []:
    print "OutputLog written.  Please remove existing file before running."
else:

    #Hunt for *.hierarchy files (easier to search than parameter files)
    matches = []
    if len(args) == 0:
        for root, dirnames, filenames in os.walk('.'):
          for filename in fnmatch.filter(filenames, '*.hierarchy'):
              matches.append(os.path.join(root, filename.split('.')[0]))


    else:
        if options.hierarchy:
            for hierarchy in args:
                matches.append(hierarchy.split('.')[0])
                print hierarchy.split('.')
    fptr= open('OutputLog','w')
    for PF in matches:
        inptr = open(PF,'r')
        nSuccess = 0
        for line in inptr:
            if line.startswith('InitialCycleNumber'):
                nSuccess += 1
                cycle = int(line.split("=")[1].strip())
            if line.startswith('InitialTime'):
                nSuccess += 1
                time = float(line.split("=")[1].strip())
            if nSuccess == 2:
                fptr.write( "DATASET WRITTEN %s %8d %18.16e\n"%(PF, cycle, time))
                break
        inptr.close()
        if nSuccess != 2:
            print "Error parsing", PF
    fptr.close()



#end
