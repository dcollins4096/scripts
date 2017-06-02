#!/usr/bin/env python

#notes: annoyed by alignment, esp. with one column.
#style sheets may help.  Made the td tags, but not further.

import sys
import glob
import re
import pdb
import numpy as np

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-w", "--width", dest="width",action="store",help = "width", default="300")
parser.add_option("-t", "--title", dest="title",action="store",help = "title", default=None)
parser.add_option("-n", "--name", dest="name",action="store",help = "fame", default="oot.html")
parser.add_option("-f", "--fieldlist", dest="fieldlist",action="store",help = "fame", default=None)
parser.add_option("-c", "--number_of_columns", dest="number_of_columns", help = "number of columns", default=2)
parser.add_option("-k", "--caption_file", dest="caption_file",help="space separated list of <run><caption>", default='captions.txt')
options, args = parser.parse_args()
#title=options.title
width = options.width

#this_fname_temp = 'p33_%s_%04d_2d-Profile_%s_%s_cell_mass.png'
#filename_template = r'([^_]*)_(\d\d\d\d)_([^_]*)_%s_(.*)_cell_mass.png'
#filename_template = r'([^_]*)_(\d\d\d\d)_(.*).png'
#filename_template = r'(.*)_(\d\d\d\d)_(.*).png' #pretty good version
filename_template = r'(.*)_n{0,1}(\d\d\d\d)_(.*).png' #pretty good version
this_fname_temp = '%s_%04d_%s.png'
framelist = []
fieldlist = []
simlist = []
framere = re.compile(filename_template)
files_skipped = []

name_dict={}
for fname in (glob.glob('*png')):
    mmm= framere.match(fname)
    if mmm:
        sim = mmm.group(1)
        if sim not in simlist:
            simlist.append(sim)
            name_dict[sim]={}
        frame = int(mmm.group(2))
        field = mmm.group(3)
        if frame not in framelist:
            framelist.append(frame)
        if field not in fieldlist:
            fieldlist.append(field)
        if not name_dict[sim].has_key(frame):
            name_dict[sim][frame] = {}
        name_dict[sim][frame][field] = fname
    else:
        files_skipped.append(fname)

fptr_skipped = open("skipped.txt","w")
for fname in files_skipped:
    fptr_skipped.write("%s\n"%fname)
fptr_skipped.close()

if options.fieldlist is not None:
    fieldlist = options.fieldlist.split(" ")
framelist = sorted(framelist)
simlist = sorted(simlist)


caption = {}
if len(glob.glob( options.caption_file ) ):
    fptr = open(options.caption_file,'r')
    for line in fptr:
        spl = line.split(" ")
        if len(spl) > 1:
            caption[spl[0]] = line[ line.index(" "):].strip()
    fptr.close()
else:
    fptr = open(options.caption_file,'w')
    for sim in simlist:
        fptr.write("%s ---\n"%sim)
    print "wrote a caption file", options.caption_file
    fptr.close()




print simlist
print framelist
print fieldlist
title = "%s"*len(simlist)%tuple(simlist)
if options.title is not None:
    title = options.title
fptr = open(options.name,'w')
fptr.write('<html>\n')
fptr.write('<head><title>'+title+'</title><link rel="stylesheet" href="oot.css" typ="text/css" media=screen></head>\n')
        
fptr.write('<table border="1">\n')
for frame in [-1]+framelist:
    fptr.write('<tr>')
    fptr.write('<td class="td_frame_number"> %d </td>'%frame)
    for field in fieldlist:
        fptr.write('<td class="td_figure_table">')
        if frame < 0:
            fptr.write("%s"%(field))
        else:
            img_tag = '<a h<figure><a href="%s"><img src="%s" width='+width+'></a><figcaption>%s (%s)</figcaption></figure>'
            fptr.write("%s n%04d<br>"%(field,frame))

            fptr.write('<table border="2"><tr>\n')
            for n,run in enumerate(simlist):
                
                fptr.write('<td class="td_image">')
                if name_dict[run].has_key(frame) and name_dict[run][frame].has_key(field):
                    this_fname = name_dict[run][frame].pop(field)
                    fptr.write(img_tag%(this_fname,this_fname,run, caption.get(run,"---")))
                else:
                    this_fname = this_fname_temp%(run,frame,field)
                    fptr.write("%s<br>"%this_fname)
                fptr.write("</td>")
                if (n+1)%int(options.number_of_columns) == 0:
                    fptr.write("</tr><tr>\n")
            
            fptr.write('</tr></table>\n')

        fptr.write('</td>\n')
    fptr.write('</tr>\n')

fptr.write('</table>\n')
fptr.write('</html>\n')
fptr.close()

#Make sure we got everyting.
for sim in name_dict.keys():
    for frame in name_dict[sim].keys():
        if len(name_dict[sim][frame].keys()) > 0:
            print "PARSE ERROR: did not properly treat", name_dict[sim][frame]


#p33_ai01_0025_2d-Profile_density_HeI_Density_cell_mass.png 
#end
