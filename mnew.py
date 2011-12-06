#!/usr/bin/env python
import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-r", "--restart", dest="restart",
                  help="Makes the output a restart", action = "store_true", default = False)
parser.add_option("-s", "--src", dest="src",
                  help="source directory",action = "store",default = "$src")
parser.add_option("-o", "--output", dest = "silent", default = None,
                  help="Output options: yes/no/direct for silent output (yes) with tee (no) without tee (direct)")

ug, there's a bunch of options here.  
#end
