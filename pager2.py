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
parser.add_option("-c", "--number_of_columns", dest="number_of_columns", help = "number of columns", default=2)
parser.add_option("-k", "--caption_file", dest="caption_file",help="space separated list of <run><caption>", default='captions.txt')
parser.add_option("-z", "--zoom_sequence", action='store_true', dest="zoom_sequence",help="If this is a sequence of zooms, the names are parsed differently", default=False)
parser.add_option("-d", "--directory_trim", action='store_true',dest='directory_trim', help="If sims are in sub directories, and there's a one-to-one directory-sim relation, remove direcory names", default=False)
parser.add_option("-x", "--xtra", action='store_true',dest='xtra_skipped', help="Put links to extra files that dont match the ax19_0019_projectin.png format", default=True)
options, args = parser.parse_args()
#title=options.title
width = options.width

#this_fname_temp = 'p33_%s_%04d_2d-Profile_%s_%s_cell_mass.png'
#filename_template = r'([^_]*)_(\d\d\d\d)_([^_]*)_%s_(.*)_cell_mass.png'
#filename_template = r'([^_]*)_(\d\d\d\d)_(.*).png'
#filename_template = r'(.*)_(\d\d\d\d)_(.*).png' #pretty good version
if options.zoom_sequence:
    filename_template = r'(.*)_n{0,1}(\d\d\d\d)_(zoom\d+){0,1}_(.*).png' #with the zoom.
else:
    filename_template = r'(.*)_D{0,1}D{0,1}n{0,1}(\d\d\d\d)_(.*).png' #pretty good version
this_fname_temp = '%s_%04d_%s.png'
framelist = []
fieldlist = []
simlist = []
framere = re.compile(filename_template)
files_skipped = []

max_zoom = -1
name_dict={}
if len(args) > 0:
    fnames = args
else:
    fnames = glob.glob("*png")
for fname in fnames:
    mmm= framere.match(fname)
    if mmm:
        sim = mmm.group(1)
        if options.directory_trim:
            sim = sim.split("/")[-1]
        if sim not in simlist:
            simlist.append(sim)
            name_dict[sim]={}
        frame = int(mmm.group(2))
        field_or_zoom = mmm.group(3)
        if field_or_zoom.startswith('zoom'):
            field = mmm.group(4)
            zoom = int(mmm.group(3)[5:])
            max_zoom = max([max_zoom,zoom])
        else:
            field = mmm.group(3)
            zoom = -1
        if frame not in framelist:
            framelist.append(frame)
        if field not in fieldlist:
            fieldlist.append(field)

        if not name_dict[sim].has_key(frame):
            name_dict[sim][frame] = {}

        if not name_dict[sim][frame].has_key(field):
            name_dict[sim][frame][field] = {}

        #if not name_dict[sim][frame].has_key(zoom):
        #    name_dict[sim][frame][field][zoom] = {}

        if name_dict[sim][frame][field].has_key(zoom):
            print "ERROR name collision (keeping first) %s %s"%(
                    name_dict[sim][frame][field][zoom],
                    fname)
        else:
            name_dict[sim][frame][field][zoom] = fname

    else:
        files_skipped.append(fname)

fptr_skipped = open("skipped.txt","w")
for fname in files_skipped:
    fptr_skipped.write("%s\n"%fname)
fptr_skipped.close()

framelist = sorted(framelist)
simlist = sorted(simlist)
fieldlist = sorted(fieldlist)

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
print "zoom", max_zoom
title = "%s"*len(simlist)%tuple(simlist)
if options.title is not None:
    title = options.title
fptr = open(options.name,'w')
fptr.write('<html>\n')

if options.xtra_skipped:
    still_skipped=[]
    fptr.write('<table boerder="1">\n')
    fptr.write('<tr>')
    for nf, fname in enumerate(files_skipped):
        if fname.split('.')[-1] in ['png','jpg']:
            img_tag = '<td><a href="%s"><img src="%s" width='+width+'></a></td>'
            fptr.write(img_tag%(fname,fname))
        else:
            still_skipped.append(fname)
    fptr.write('</tr>')
    if len(still_skipped):
        #haha, this does nothing because we are only reading png in the first place.
        fptr.write('<tr>')
        for nf, fname in enumerate(still_skipped):
            fptr.write("<td><a href='%s'>%s</a></td>"%(fname,fname))

        fptr.write('</tr>')

    fptr.write('</table>\n')
        



fptr.write('<table border="1">\n')
for frame in [-1]+framelist:
    fptr.write('<tr>')
    fptr.write('<td class="td_frame_number"> %d </td>'%frame)
    for field in fieldlist:
        fptr.write('<td class="td_figure_table">')
        if frame < 0:
            fptr.write("%s"%(field))
        else:
            for zoom in range(-1,max_zoom+1):
                img_tag = '<a h<figure><a href="%s"><img src="%s" width='+width+'></a><figcaption>%s (%s)</figcaption></figure>'
                fptr.write("%s n%04d<br>"%(field,frame))

                fptr.write('<table border="2"><tr>\n')
                for n,run in enumerate(simlist):
                    
                    fptr.write('<td class="td_image">')
                    if name_dict[run].has_key(frame) and name_dict[run][frame].has_key(field) and name_dict[run][frame][field].has_key(zoom):
                        this_fname = name_dict[run][frame][field].pop(zoom)
                        fptr.write(img_tag%(this_fname,this_fname,run, caption.get(run,"---")))
                    else:
                        this_fname = this_fname_temp%(run,frame,field)
                        fptr.write("%s<br>"%this_fname)
                    fptr.write("</td>")
                    if (n+1)%int(options.number_of_columns) == 0:
                        fptr.write("</tr><tr>\n")
                
                fptr.write('</tr></table><br>\n')

        fptr.write('</td>\n')
    fptr.write('</tr>\n')

fptr.write('</table>\n')
fptr.write('</html>\n')
fptr.close()

#Make sure we got everyting.
for sim in name_dict.keys():
    for frame in name_dict[sim].keys():
        for field in name_dict[sim][frame].keys():
            if len(name_dict[sim][frame][field].keys()) > 0:
                print "PARSE ERROR: did not properly treat", name_dict[sim][frame]


#p33_ai01_0025_2d-Profile_density_HeI_Density_cell_mass.png 
#end
