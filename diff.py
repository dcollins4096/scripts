#!/usr/bin/env python

import sys



def deriv(filename, normalize = False, unit = 1.0, percent = False):
    file = open(filename,"r")
    Start = True
    for f in file:

        number = float(f)/unit

        if Start:
            Start = False
            FirstElement = number
            LastElement = number
        else:
            if normalize:
                print number - FirstElement
            elif percent:
                print (number - LastElement)/LastElement
                LastElement = number
            else:
                print number - LastElement
                LastElement = number
        


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-n", "--norm", dest="normalize",
                  help="subtract the first element (instead of differencing)",
                  action = "store_true", default = False)

parser.add_option("-p", "--percent", dest="percent",
                  help="Print the percent change (this-last)/last (use this option only)",
                  action = "store_true", default = False)

parser.add_option("-u", "--unit", dest="unit",
                  help="divide by unit",
                  action = "store", type = "float", default = "1.0")
(options, args) = parser.parse_args()

if len( sys.argv ) < 2:
    print "diff.py file"
    print "differentiates a list of numbers."
else:
    filename = sys.argv[1]

    norm = False
    if len( sys.argv ) > 2:
        norm = sys.argv[2]

    deriv(filename,normalize=options.normalize, unit = options.unit, percent = options.percent)

#end
