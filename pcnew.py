#! /usr/bin/env python

### Author: David Collins <dcollins@physics.ucsd.edu>
### Affiliation: University of California, San Diego
### Homepage: http://barn.enzotools.org/

### License:
###   Copyright (C) 2007-2009 David Collins.  All Rights Reserved.
### 
###   paramdiff is free software; you can redistribute it and/or modify
###   it under the terms of the GNU General Public License as published by
###   the Free Software Foundation; either version 3 of the License, or
###   (at your option) any later version.
### 
###   This program is distributed in the hope that it will be useful,
###   but WITHOUT ANY WARRANTY; without even the implied warranty of
###   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###   GNU General Public License for more details.
### 
###   You should have received a copy of the GNU General Public License
###   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Compares two enzo parameter files.
# Looks for the first 'word' on each line, 
# compares the things after the '='

import sys
import glob
import re
import os
import numpy as np
nar=np.array
blank = re.compile(r'\S')

def multi_compare(list_of_pfs):
    """
    = get all the keys, make a unique list.
    = Look for a file that contains the prefred order of parameters.
    = Look for a file that contains the prefred order of files.
    = Get the max number of elements for each parameter.  Make a dict.
    = header.
    = for each file
        for each parameter
           print the value

    """
    full_pf_list = [ parse_file(fname) for fname in list_of_pfs]
    unique_list = []
    multiples = {}
    for pf in full_pf_list:
        for key in pf.keys():
            if key not in unique_list:
                n_components = len(pf[key])
                if n_components > 1:
                    multiples[key] = max([multiples.get(key,0),n_components])
                unique_list.append(key)
    
    template = "%s\t"*(len(unique_list) + 1)
    fptr = open("stuff.tsv","w")
    fptr.write(template%tuple([" "]+list(nar( unique_list))))
    for n,pf in enumerate(list_of_pfs):
        fptr.write("%s\t"%pf)
        for key in nar(unique_list):
            fptr.write( "%s\t"%full_pf_list[n].get(key,""))
        fptr.write("\n")
    fptr.close()

    

def parse_file(filename, dbgOut=0):
    file1ob = open(filename,"r")
    lines1 = file1ob.readlines()
    file1ob.close()    
    ParameterList = {}
    if dbgOut > 0:
        print filename
    for line in lines1:
        if dbgOut > 0:
            print "--", line
        if line[0] == "#":
            continue
        if line[0:2] == "//":
            continue
        #skip blank lines. (blank lines don't match
        #non-whitespace.)
        if blank.match(line) == None:
            continue

        name = line[0:line.find("=")]

        #Pull off argument from line
        TrailingComment = max(line.find("//"),line.find("#"))

        if TrailingComment == -1 :
            args = line[line.find("=")+1: -1]
        else:
            args = line[line.find("=")+1: TrailingComment]        

        
        #Number strings must start with a number
        FirstElement = re.findall(r"(\s*)(.)", args)[0][1]
        
        if dbgOut > 0:
            print "---- args", args, "trailing comment", TrailingComment
        
        arglist = args.split(" ")
        newargs = []
        for arg1 in arglist:
            arg = arg1.strip()
            if arg == "":
                continue
            try:
                newargs.append( int( arg ) )
                continue
            except:
                pass
            try:
                newargs.append( float(arg))
                continue
            except:
                pass
            newargs.append(arg)
        #to account for array parameters
        #with spaces in the brackets:

        if name.find("\t") != -1:
            FirstWhiteIndex = min( name.find(" "), name.find("\t"))
        else:
            FirstWhiteIndex = name.find(" ")
        LastIndex = max( FirstWhiteIndex, name.find("]")+1)
        name = name[0:LastIndex]
        
        if ParameterList.has_key(name):
            print "File", filename, "has multiple instances of",name
            print "       Using the last"
        ParameterList[name] = newargs
    return ParameterList
def compare(FileName1,FileName2):

    dbgOut = 0
    for filename in [FileName1,FileName2]:
        if glob.glob(filename) == []:
            print "No file named " , filename
            return 1

    print "Comparing", FileName1, FileName2
    #open both files
    #Make a dictionary of the parameters in file1. Match if
    # [1] != #
    # all before =
    # cut up to ']'
    # for now, I'm not going to worry about spaces within [].
    # Exact matches only.

    ParameterList = [] #[{},{}]
    spacer = "        "
    #oft used regular expresions.  
    #matches non-whitespace.

    parameter_file = -1
#
#       Parse both files for parameters.
#    Make dictionaries of all the words.
#

    for filename in [FileName1,FileName2]:
        parameter_file = parameter_file +1
        ParameterList.append( parse_file(filename,dbgOut=dbgOut) )

    IvePrintedHeadder = 0
    #compare list 1 aganst list2
    #remove the missing ones from list1
    Keyz = ParameterList[0].keys()
    Keyz.sort()
    for key1 in Keyz:
        if ParameterList[1].has_key(key1) == 0:
            if IvePrintedHeadder == 0:
                print "Parameters missing from", FileName2
                IvePrintedHeadder = 1
            print spacer, key1,"(",ParameterList[0].pop(key1),")"
    IvePrintedHeadder = 0
    #compare list 1 aganst list2
    #remove them from list1
    Keyz =ParameterList[1].keys() 
    Keyz.sort()
    for key2 in Keyz:
        if ParameterList[0].has_key(key2) == 0:
            if IvePrintedHeadder == 0:
                print "Parameters missing from", FileName1
                IvePrintedHeadder = 1
            print spacer, key2, "(",ParameterList[1].pop(key2),")"

        
#now compare the parameters
    IvePrintedHeadder = 0
    SortedList = ParameterList[0].keys()
    SortedList.sort()
    for key1 in SortedList:
        different=False
        length = len(ParameterList[0][key1])
        if length != len(ParameterList[1][key1]):
            different=True
        for n in range(length):
            if ParameterList[0][key1] != ParameterList[1][key1]:
                different=True
        if different:
            if IvePrintedHeadder == 0:
                IvePrintedHeadder = 1
                print "Parameters that are different: ", FileName1, FileName2
            print1 = ParameterList[0][key1]
            print2 = ParameterList[1][key1]
            #The string cast is to avoid quering the type, which I don't know
            #how to do right now.
            if str(print1)[-1] == "\n":
                print1 =  print1[0:-1]
            if str(print2)[-1] == "\n":
                print2 =  print2[0:-1]
            print spacer, key1, "(", print1, ",", print2,")"
    return 0
#end compare

if len( sys.argv ) < 3 :
    print """ pc.py file1 file2 """
    print """ compares two enzo parameter files."""
elif len(sys.argv) ==3:
    run = 1
    FileName1 = sys.argv[1]
    FileName2 = sys.argv[2]
    if glob.glob(FileName1) == []:
        print FileName1,"doesn't exist."
        run = 0
    if os.path.isdir(FileName2) == 1:
        FileName2 = FileName2 + "/" + FileName1
    if glob.glob(FileName2) == []:
        print FileName2,"doesn't exist."        
        run = 0
    if run != 0:
        out = compare(FileName1,FileName2)
else:
    multi_compare(sys.argv[1:])


#end
