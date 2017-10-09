#!/usr/bin/env python

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


def delta(d1, d2, nchecks=None):
    """changes the *delta* value in d2 to reflect changes
    Files the disappear from d1 are maybe not obvious how to deal with..."""
    if nchecks is None:
        nchecks = max(len(d1.lines),len(d2.lines))
    n1=0; n2=0
    longest = max([d1.longest_line,d2.longest_line])
    template = "%"+str(longest)+"s |%s|  %"+str(longest)+"s"
    verb = -1
    for n_counter in range(nchecks):  #n1 + n2 < len(d1.files)+ len(d2.files):
        n_counter+=1
        if n1 == len(d1.files): 
            for i in range(n2,len(d2.files)):
                d2.new_lines.append([d2.sizes_bytes[i],d2.files[i]])
                print template%("","n",d2.lines[i])
            break
                
        if n2 == len(d2.files): 
            for i in range(n1,len(d1.files)):
                d2.removed_lines.append([d1.sizes_bytes[i],d1.files[i]])
                print template%(d1.lines[i],"n","")
            break
                                    
        if d1.files[n1] == d2.files[n2]:
            this_delta = d2.sizes_bytes[n2]-d1.sizes_bytes[n1]
            d2.delta[n2] = this_delta
            if this_delta > 1 and verb > 2:
                print "- ",d1.lines[n1]
                print "+ ",d2.lines[n2]
            if verb == -1:
                if this_delta > 1:
                    print template%(d1.lines[n1],'D',d2.lines[n2])
                else:
                    print template%(d1.lines[n1],'s',d2.lines[n2])
            n1+=1
            n2+=1

        else:
            new_d2_line= False
            kill_d1_line=False
            if d1.files[n1] in d2.files[n2+1:]:
                new_d2_lines=np.where(np.array(d1.files[n1]) == np.array(d2.files[n2+1:]))[0][0] + n2+1

                for i in range(n2,new_d2_lines+1):
                    if verb > 2:
                        print "+", d2.lines[i]
                    if verb == -1:
                        print template%("","+",d2.lines[i])
                    d2.new_lines.append([d2.sizes_bytes[i],d2.files[i]])
                n1+=1
                n2=new_d2_lines+1
            else:
                if verb > 2:
                    print "-", d1.lines[n1]
                d2.removed_lines.append([d1.sizes_bytes[n1], d1.files[n1]])
                if verb == -1:
                    print template%(d1.lines[n1],"-","")
                n1+=1
                if  d2.files[n2] not in d1.files[n1+1:]:
                    d2.new_lines.append([d2.sizes_bytes[n2], d2.files[n2]])
                    n2+=1




            #new_line=True
            #new_n2 
            #for n_tmp in range(1,3):
            #    if d1.files[n1] == d2.files[n1+n_tmp]:
            #        new_n2 = 



duud_list = []
for filename in args:
    the_duud= duud(filename)
    the_duud.ingest(slice(30)) 
    #print the_duud.sizes_bytes
    duud_list.append(the_duud)

for n_duud, the_duud in enumerate(duud_list):
    if n_duud == 0:
        last_duud = the_duud
    else:
        delta(last_duud, the_duud, nchecks=15)
        last_duud=the_duud
d1 = duud_list[0]
d2 = duud_list[1]
#end
