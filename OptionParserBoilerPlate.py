
from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] quiz_name.csv")
parser.add_option("-g","--gradebook",action="store",default="gradebook.csv", help="Main grade book for student list")
parser.add_option("-v","--verbose",action="store_true",default=False, help="Verbose.  Say which names are altered by the script")
(options,args)=parser.parse_args()
