#!/usr/bin/env python

# A tool to parse where the data went.
# Current status:  
#    Makes the diff correctly
#    Doesn't seem to get all the numbers right: totals at the end don't match.


from optparse import OptionParser
import re
import numpy as np
import pdb

parser = OptionParser()
parser.add_option("-H","--Hierarchy",dest="hierarchy",action="store_true",default=False,
                              help="takes list of hierarchy files")
parser.add_option("-b","--backup",dest="backup",action="store_true",default=False,
                              help="Backup old outputlog in OldOutputLog")
parser.add_option("-o","--output",dest="output",action="store",default="OutputLog",
                              help="Name of output log file")
(options,args)=parser.parse_args()

def tab_is_white(string):
    tablist=string.split("\t")
    out = ""
    for i in tablist:
        if len(i):
            out += i
        else:
            out += " "
    return out

re_num = re.compile(r'\s*([\d\.])+([KMGBT])\s*')
def sci_format(num, suffix=''):
    #units = ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']
    #the above is probably more accurate.  MUST be consistent with the other getnum function
    units = ['B','K','M','G','T','P','E','Z']
    for unit in units:
        if abs(num) < 1e3:
            return "%3.1f%s" % (num, unit)
            #return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1e3
    return "%.1f%s%s" % (num, 'Yi', suffix)

def getnum(line):
    match = re_num.match(line)
    if match is None:
        print "No byte match.  Chunk", "'%s'"%line
        return -1
    value= float(match.group(1))
    order = match.group(2)
    mult = {'K':1e3,'M':1e6,'G':1e9,'B':1,'T':1e12}[order]
    return value*mult
class duud():
    def __init__(self,fname):
        self.fname = fname
        self.lines=[]
        self.files=[]
        self.sizes_bytes=[]

        self.delta=[]
        self.changed_lines=[]
        self.new_lines=[]
        self.removed_lines=[]
        self.date=None
        self.longest_line=-1
    def ingest(self,ingest_slice=slice(None)):
        fptr = open(self.fname,'r')
        for line in fptr.readlines():
            self.lines.append(tab_is_white(line[:-1]))
        fptr.close()
        for line in self.lines[ingest_slice]:
            self.longest_line=max([len(line), self.longest_line])
            #print line
            try:
                line_start = line.index("/")
            except:
                print "error with finding the directory."
                print line[:-1]
                raise
            self.files.append(line[line_start:])
            byte_chunk = line[:line_start]
            self.sizes_bytes.append(getnum(byte_chunk))
        self.delta=np.zeros(len(self.sizes_bytes))


def report(d1, d2, n1, n2, message):
    #longest = max([d1.longest_line,d2.longest_line])
    delta = 0
    longest = 50
    nformat=6
    t2 = "%"+str(nformat)+"s"
    t1 = "%"+str(longest)+"s"
    if d1 is None:
        s1 = t1%"" + t2%" "
        n1p = "%2s"%" "

    else:
        #s1 = d1.lines[n1]
        s1 = t1%d1.files[n1] + t2%sci_format(d1.sizes_bytes[n1])
        n1p = "%2d"%n1
        delta -= d1.sizes_bytes[n1]
    if d2 is None:
        s2 = t1%""
        n2p = "%2s"%" "
    else:
        #s2 = d2.lines[n2]
        t1 = "%"+str(longest)+"s"
        s2 = t2%sci_format(d2.sizes_bytes[n2]) + t1%d2.files[n2] 
        n2p = "%2d"%n2
        delta += d2.sizes_bytes[n2]
    #nstring="(%s,%s)"%(n1p,n2p)
    nstring = " "+t2%sci_format(delta)

    template = "%s |%s"+nstring+"|  %"+str(longest)+"s"
    #template = "%"+str(longest)+"s |%s"+nstring+"|  %"+str(longest)+"s"
    #template = "%"+str(longest)+"s |%s|  %"+str(longest)+"s"
    if np.abs(delta) > 0:
        print template%(s1,message,s2)

def delta(d1, d2, nchecks=None):
    """changes the *delta* value in d2 to reflect changes
    Files the disappear from d1 are maybe not obvious how to deal with..."""
    if nchecks is None:
        nchecks = max(len(d1.lines),len(d2.lines))
    n1=0; n2=0
    verb = -1
    #longest = max([d1.longest_line,d2.longest_line])
    #template = "%"+str(longest)+"s |%s|  %"+str(longest)+"s"
    for n_counter in range(nchecks):  #n1 + n2 < len(d1.files)+ len(d2.files):
        n_counter+=1
        if n1 == len(d1.files): 
            for i in range(n2,len(d2.files)):
                d2.new_lines.append([d2.sizes_bytes[i],d2.files[i]])
                #print template%("","n",d2.lines[i])
                report(None, d2,None,i, "n")
            break
                
        if n2 == len(d2.files): 
            for i in range(n1,len(d1.files)):
                d2.removed_lines.append([d1.sizes_bytes[i],d1.files[i]])
                #print template%(d1.lines[i],"n","")
                report(d1,None,i,None,"n")
            break
                                    
        if d1.files[n1] == d2.files[n2]:
            this_delta = d2.sizes_bytes[n2]-d1.sizes_bytes[n1]
            abs_delta = np.abs(this_delta)
            #d2.delta[n2] = this_delta
            if abs_delta > 0:
                d2.changed_lines.append([this_delta,d2.files[n2]])
            if abs_delta > 1 and verb > 2:
                print "- ",d1.lines[n1]
                print "+ ",d2.lines[n2]
            if verb == -1:
                if abs_delta > 0:
                    #print template%(d1.lines[n1],'D',d2.lines[n2])
                    report(d1,d2,n1,n2,'D')
                else:
                    report(d1,d2,n1,n2,'s')
                    #print template%(d1.lines[n1],'s',d2.lines[n2])
            n1+=1
            n2+=1

        else:
            new_d2_line= False
            kill_d1_line=False
            if d1.files[n1] in d2.files[n2+1:]:
                new_d2_lines=np.where(np.array(d1.files[n1]) == np.array(d2.files[n2+1:]))[0][0] + n2
                new_range = range(n2,new_d2_lines+1) #plus one to make it LessEqual in range
                for i in new_range:
                    if verb > 2:
                        print "+", d2.lines[i]
                    if verb == -1:
                        #print template%("","+",d2.lines[i])
                        report(None,d2,None,i,"+")
                    d2.new_lines.append([d2.sizes_bytes[i],d2.files[i]])
                #n1+=1  Don't advance n1, you haven't eaten it yet.
                n2=new_d2_lines+1
            else:
                if verb > 2:
                    print "-", d1.lines[n1]
                d2.removed_lines.append([d1.sizes_bytes[n1], d1.files[n1]])
                if verb == -1:
                    #print template%(d1.lines[n1],"-","")
                    report(d1,None,n1,None,"-")
                n1+=1
                #if  d2.files[n2] not in d1.files[n1+1:]:
                #    d2.new_lines.append([d2.sizes_bytes[n2], d2.files[n2]])
                #    n2+=1




            #new_line=True
            #new_n2 
            #for n_tmp in range(1,3):
            #    if d1.files[n1] == d2.files[n1+n_tmp]:
            #        new_n2 = 



duud_list = []
for filename in args:
    the_duud= duud(filename)
    the_duud.ingest() #slice(30)) 
    #print the_duud.sizes_bytes
    duud_list.append(the_duud)

for n_duud, the_duud in enumerate(duud_list):
    if n_duud == 0:
        last_duud = the_duud
    else:
        delta(last_duud, the_duud) #, nchecks=4)
        last_duud=the_duud
d1 = duud_list[0]
d2 = duud_list[1]

all_delta=[]
all_files=[]
full_report=False
for delta, fname in d2.changed_lines:
    if full_report: print "changed", delta, fname
    all_delta.append(delta)
    all_files.append(fname)
for delta, fname in d2.new_lines:
    if full_report: print "new", delta, fname
    all_delta.append(delta)
    all_files.append(fname)
for delta, fname in d2.removed_lines:
    if full_report: print "gone", delta, fname
    all_delta.append(delta)
    all_files.append(fname)

print d1.lines[-1]
print d2.lines[-1]



#end
