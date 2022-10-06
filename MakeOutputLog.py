#!/usr/bin/env python

#
#  Make's OutputLog file from enzo files in the directory tree.
#

import fnmatch
import os
import shutil
import glob
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H","--Hierarchy",dest="hierarchy",action="store_true",default=False,
                      help="takes list of hierarchy files")
parser.add_option("-b","--backup",dest="backup",action="store_true",default=False,
                      help="Backup old outputlog in OldOutputLog")
parser.add_option("-o","--output",dest="output",action="store",default="OutputLog",
                      help="Name of output log file")
(options,args)=parser.parse_args()
OutputLog = options.output

if glob.glob(OutputLog) != [] and not options.backup:
    print("OutputLog written.  Please remove existing file before running.")
    sys.exit(0)
if glob.glob(OutputLog) != [] and options.backup:
    n_backup = len(glob.glob('*%s*'%(OutputLog)))
    shutil.move(OutputLog,'%s.backup%s'%(OutputLog,n_backup))

if 1:
    #Hunt for *.hierarchy files (easier to search than parameter files)
    matches = []
    output_list=[]
    if len(args) == 0:
        for root, dirnames, filenames in os.walk('.'):
          for filename in fnmatch.filter(filenames, '*.hierarchy'):
              print("filename",filename)
              matches.append(os.path.join(root, filename.split('.')[0]))


    else:
        if options.hierarchy:
            for hierarchy in args:
                matches.append(hierarchy.split('.')[0])
                print(hierarchy.split('.'))
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
                #fptr.write( "DATASET WRITTEN %s %8d %18.16e\n"%(PF, cycle, time))
                output_list.append([PF,cycle,time])
                break
        inptr.close()
        if nSuccess != 2:
            print("Error parsing", PF)

    #write output sorted by sim time
    fptr= open(OutputLog,'w')
    for p in sorted(output_list, key=lambda item:item[2]):
        fptr.write( "DATASET WRITTEN %s %8d %18.16e\n"%(p[0], p[1],p[2]))
    fptr.close()



#end
