#! /usr/bin/env python

import sys
import re

def times_and_files(filename, near = -1.0):

    #Matches the grid structure.  Only for the simple kind of write.
    grid = re.compile(r"data(....).grid0001")
    TopGrid = re.compile(r"TopGrid.*time =(.*)")
    Step = re.compile(r"STEP.* T = (.*)")

    #Open the file, print it, read from it.
    file = open(filename, "r")
    AllLines = file.readlines()

    #Initialize; SaveLine saves the time line.
    #OutputStyle saves the output style: options are 1 for the Old (TopGrid)
    #search, 2 is for the New (STEP_INFO) search.
    #0 is for Unknown, do both.
    #Nearness monitors the current distance from the targt number.
    #Saves the current Nearness and DumpNumber
    SaveLine = "Startup"
    OutputStyle = 0
    Nearness = -1
    SaveTime = -1
    DumpNumber = 0
    for line in AllLines:

        #This is kind of dirty. 
        if OutputStyle == 0 or OutputStyle == 1:
            match = TopGrid.search(line)
            if match != None:
                SaveLine = match.group(1)
                OutputStyle = 1
        if OutputStyle == 0 or OutputStyle == 2:
            match = Step.search(line)
            if match != None:
                SaveLine = match.group(1)
                OutputStyle = 2
        match = grid.search(line)
        if match != None:
            if near > 0:
                if Nearness > 0:
                    if Nearness > abs( near - float(SaveLine) ) :
                        Nearness = abs( near - float(SaveLine) )
                        DumpNumber = match.group(1)
                        SaveTime = SaveLine
                else:
                    if SaveLine != "Startup":
                        Nearness = abs( near - float(SaveLine) )
                    DumpNumber = match.group(1) 
                    SaveTime = SaveLine
            else:
                DumpNumber = match.group(1)
                print DumpNumber , SaveLine
                
#    if near > 0 :
#        print "nearest exit:", DumpNumber, SaveTime, Nearness
    return [DumpNumber,SaveTime,Nearness]

#forall lines;
#If the line contains "TopGrid" save it.
#if th line contains "grid0001" print it and the previously saved line.

    file.close()


if len( sys.argv ) == 1:
    print "timefind <list of file names>"
    print "   gets times and file numbers."
    print "   might get more options later."
    print "   -near <time> for the first number returns only the number closest to <time>"
else:
    filenamestart = 1 #might change if other options appear.
    near = -1

    SaveThisOne = [0,-1,-1]
    if sys.argv[1] == "-near":
        filenamestart = 3
        near = float(sys.argv[2])
    for filename in sys.argv[filenamestart:]:
        Output = times_and_files( filename,near )
        if near < 0 :
            print "==== filename === "
        else:
            if SaveThisOne[2] < 0:
                SaveThisOne = Output
            else:
                if SaveThisOne[2] > Output[2]:
                    SaveThisOne = Output
            print "==== ", filename," === ", Output, SaveThisOne
    if near > 0 :
        print "File you want: ", SaveThisOne
#end
