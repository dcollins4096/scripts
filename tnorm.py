#!/usr/bin/env python
import sys

class time:
    
    def __init__(self,line):
        self.string = line
        array = line.split(" ")
        #make it look like this:['0:0', 'TIME', 'Start', 'Main', '1205838178.504223', '\n']
        while array[0] == '':
            array = array[1:len(array)]
        self.array = array
        
        self.process = array[0][0:array[0].find(":")]
        self.startOrEnd = array[2]
        self.position = array[3]
        self.time = float(array[4])
def tnorm(filename, option, args, t0):

    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    moments = [time(lines[0])]

    #print 
    time0 = moments[0].time*1.0

    for line in lines[1:]:
        moments.append( time(line) )

    #options:
    #1. normalize.
    #2. Show difference between the End of ComputeGlobalStats and the Start of SMHD.
    if option == 1:
        for i in range(0,len(moments)):
            mom = moments[i]
            if mom.startOrEnd == "Start" and mom.position == "Main":
                continue
            Delta = 0.0
            if i > 0:
                Delta = mom.time - moments[i-1].time
            print '%6s %25s %15.7f (%15.7f)' % (mom.startOrEnd, mom.position, mom.time-time0, Delta)
    elif option == 2:
        e_cgs = 0
        s_smhd = 0
        for mom in moments:
            if mom.startOrEnd == "End" and mom.position == "ComputeGlobalStats":
                e_cgs = mom.time
            if mom.startOrEnd == "Start" and mom.position == "SMHD":
                s_smhd = mom.time
        print filename, s_smhd , "-", e_cgs, "=", s_smhd - e_cgs
    elif option == 3:
        #Time from the root processor
        for mom in moments:
            if mom.startOrEnd == args[0] and mom.position == args[1]:
                print "%10s %15.7f " %(mom.process, mom.time-t0)
    else:
        print "Option not defined:", option
if len(sys.argv) == 1:
    print "Tnorm.  Does stuff."
    sys.exit(0)
else:
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",action="store",help = "File name", default="none")
    parser.add_option("-a","--all", dest = "opt_all", action = "store_true", default = "false",\
                      help = "Print all found, normalized to -t (if given)")
    parser.add_option("-s","--single", dest = "opt_sing", action = "store_true", default = "false",\
                      help = "-s <start/end> <position> prints all instances of given field.  Normalizes to -t")
    parser.add_option("-t", dest = "t0", action = "store", default = "0", type = "float",\
                      help = "Initial time.  If given, all times are normalized to this time.")

    (options, args) = parser.parse_args()


    opt = 1
    if options.opt_all != "false":
        opt = 1
    elif options.opt_sing != "false":
        opt = 3
    if options.opt_sing != "false" and len(args) != 2:
        print "option -s requires <start/end> and <position> arguments.  For instance:"
        print "   tnorm.py TIME -s End InitializeNew"
        sys.exit(0)

    if options.filename == 'none':
        print "tnorm.py -f filename"
    tnorm(options.filename, opt, args, options.t0)



#end
