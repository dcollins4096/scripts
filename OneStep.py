#!/usr/bin/env python

#
# Needs option parser.
#

import sys
def pull_step(filename,outfile,step=1):
    """Pulls out the text between the *step* occurance of "Start MainLoop ... End MainLoop" """
   
    file = open(filename,"r")

    first_line = file.readline()

    #We won't be matching regexp for the expense.
    ProcessorNumber = first_line.split()[0]

    #I don't what the start of the run to make the plot horrible.
    
    whatIwantFromTheFirstLine = ProcessorNumber+" TIME Start Main"
    outfile.write(first_line[0:len(whatIwantFromTheFirstLine)])

    #Set up the main loop strings
    StartString = "Start MainLoop"
    StopString = "End MainLoop"

    StartLine = ProcessorNumber + " TIME " + StartString
    StopLine = ProcessorNumber + " TIME " + StopString

    len_start = len(StartLine)
    len_stop = len(StopLine)
    len_proc = len(ProcessorNumber) + 6
    LoopCounter=1
    Reading = False
    for line in file:
        #if this line is a Start MainLoop
        #   LoopCounter++
        #   if LoopCounter == step, Reading=true
        #if Reading=True
        #   put the lotion in the basket.
        #   If end line break.
        if not Reading:
            if line[len_proc:len_start] == StartString:
                if LoopCounter == step:
                    Reading = True
                    time = line[len_start+1:]
                    outfile.write(" " + time)

                LoopCounter += 1
        #in a separate conditional to keep the start line.
        if Reading:
            outfile.write(line)
            if line[len_proc:len_stop] == StopString:
                break

    file.close()
#end

if len(sys.argv) > 1:
    output = 'all_times'
    step = 3
    output = open("all_files","w")
    for filename in sys.argv[1:]:
        pull_step(filename,output,step)
    output.close()
else:
    print "OneStep.py <options> <list of files>"
    print "Pulls out all code between the *stepth* iteration of MainLoop"
