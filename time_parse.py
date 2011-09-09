#!/usr/bin/env python

# Parses output from the wall_time(string) function in enzo.
# Looks for output in the form:
# ProcessorNumber "TIME" Start/End "Function"
# i.e. 
# 0 TIME Start Main
# Groups 

import re
import sys
import glob
import copy
import math
import string
import types
import copy

class Event:
    #start time and end time.
    start = -1.0
    end = -1.0
    #numerical id for each object.  (Dumb?)
    #and processor number
    id = -1
    proc_num = -1
    level = -1
    #type of event. (EvolveLevel, Main, whatever)
    name = "no_name"
    
    #ids of calls nested in this routine, for extraction.
    nests = []
    original_text = ""
    original_line = 0

    def dt(self):
        if self.end < 0:
            return -1
        else:
            return self.end - self.start
    def talk_about_yourself(self, norm = 0.0, note = ""):
        out = "xxx "
        #out += " %d "%(self.id)
        out += "proc  %d "%(self.proc_num)
        out += "name  %10s "%(self.name)
        out += "start %10f "%(self.start-norm)
        out += "end   %10f "%(self.end-norm)
        out += "lapse %5f "%(self.dt() )
        print out
    def __cmp__(self,other):
        return cmp(self.start, other.start)

def parse(filename,dbg=0):
    
    #       error check.
    if glob.glob(filename) == []:
        print "File not found ", filename
        sys.exit(-1)
	
    #the file open, read, close
    file = open(filename, "r")


    #variable initialization	
    id = -1
    event_array = []
    norm_time = {}
    NormalizeProcessorTime = True
    first_start = -1
    last_end = -1
    for line in file:
        if dbg > 1:
            print "line: ",line[0:-1]
        
        match = re.match(r"([\d\s]{4}:){0,1}(\s{0,1}\d+)\s*TIME\s+(\S+)\s+(\S+)\s+(\S+)",line)
        #match = re.match(r"(\d+)\s*TIME\s+(\S+)\s+(\S+)\s+(\S+)",line)
			
        if match != None:
            proc_num = int(match.group(2)) #This is the proc num from wall_time
            #proc_num = match.group(1)
            #proc_num = int(string.strip(proc_num[0:proc_num.find(":")]))
            start_or_end = match.group(3)
            type = match.group(4)
            time = float(match.group(5))

            if dbg > 1:
                print "mmm", proc_num
                print "sss", start_or_end
                print "www", type
                print "ttt", time

            if start_or_end == "Start" or start_or_end == "start":


                if NormalizeProcessorTime:
                    if type == 'Main':
                        norm_time[proc_num] = time
                        print "norm_time[%d] = %f"%(proc_num,time)
                else:
                    norm_time[proc_num] = 0.0
                time = time - norm_time[proc_num]
                

                if first_start < 0:
                    first_start = time
                else:
                    first_start = min(time,first_start)
                if dbg > 1:
                    print "start"
                id += 1

                while proc_num > len(event_array) - 1:
                    if dbg > 2:
                        print "proc_num", proc_num,"len", len(event_array)
                    event_array.append({})
                    event_array[-1]['LEVEL'] = -1
                if not event_array[proc_num].has_key(type):
                    event_array[proc_num][type] = {'pend':[],'done':[]}

                event_array[proc_num][type]['pend'].append(Event())
                event_array[proc_num][type]['pend'][-1].proc_num = proc_num
                event_array[proc_num][type]['pend'][-1].start = time
                event_array[proc_num][type]['pend'][-1].name = type

                if type == 'EvolveLevel':
                    event_array[proc_num]['LEVEL'] += 1

                event_array[proc_num][type]['pend'][-1].level = event_array[proc_num]['LEVEL']
                                                              
                if dbg > 0:
                    event_array[proc_num][type]['pend'][-1].talk_about_yourself(note = "start")
            elif start_or_end == "End":

                time = time - norm_time[proc_num]

                if last_end < 0:
                    last_end = time
                else:
                    last_end = max(time,last_end)
                if type == 'EvolveLevel':
                    event_array[proc_num]['LEVEL'] -= 1

                if event_array[proc_num].has_key(type):
                    event_array[proc_num][type]['done'].append(
                        event_array[proc_num][type]['pend'].pop() )

                    event_array[proc_num][type]['done'][-1].end = time
                
                    if dbg > 0:
                        event_array[proc_num][type]['done'][-1].talk_about_yourself(note = "end")
                else:
                    print "Start not found for End:", type
            else:
                print "Unknown start/end status:"
                print "   ", line
                    
    file.close()
    duplicate = [] #because I changed the data model, and don't want to rewrite 
    for pn, proc in enumerate(event_array):
        duplicate.append({})
        for event_name in proc.keys():
            event = proc[event_name]
            if not isinstance(event, types.DictType):
                continue
            while len(event['pend']) > 0:
                event['done'].append(event['pend'].pop())
                event['done'][-1].end = last_end
            
            duplicate[pn][event_name] = event['done']

        
    return duplicate

def give_dictionary(event_array):
    event_dict = {}
    for processor in event_array:
        for event_name in processor.keys():
            name = processor[event_name][0].name
            if event_dict.has_key( name ):
                event_dict[ name ].extend( processor[event_name] )
            else:
                event_dict[ name ] = processor[event_name] 
    return event_dict

def verbose_report(event_dict,stat_dict,eventName):
    #first get the start time, for easier reading.
    norm = 0.0
    lmin = 1e10
    
    if event_dict.has_key("Main"):
        first = 1
        for event in event_dict["Main"]:
            if first == 1:
                lmin = event.start
                first = 0
            else:
                lmin = min(lmin, event.start)
        norm = 0
    if event_dict.has_key(eventName):
        for event in event_dict[eventName]:
            event.talk_about_yourself(norm = norm)
    else:
        print "verbose_report: name ", eventName, "not found"
class stat:
    avg = 0
    std = 0
    min = 1e10
    max = -1e10
    n = 0
    total_in = 0
    total_only = 0
    MaxProc = -1
    MinProc = -1
    def report(self):
        print "Avg:    %f +- %f"%(self.avg, self.std)
        print "span:   [%f, %f]  Min/Max Procs: %d %d"%( self.min,self.max, self.MinProc, self.MaxProc)
        print "Total:  ", self.total_in
        print "N calls:", self.n


def avg_for_events(event_dict):
    stat_dict={}
    for key in event_dict.keys():
        stat_dict[key] = stat()
        #compute average, count
        total = 0
        for event in event_dict[key]:
            dt = event.dt()
            if dt < 0:
                continue
            stat_dict[key].n += 1
            stat_dict[key].avg += event.dt()
            if stat_dict[key].min >  event.dt():
                stat_dict[key].min = event.dt()
                stat_dict[key].MinProc = event.proc_num
            if stat_dict[key].max < event.dt():
                stat_dict[key].max = event.dt()
                stat_dict[key].MaxProc = event.proc_num
            stat_dict[key].total_in += event.dt()
        if stat_dict[key].n == 0:
            continue
        stat_dict[key].avg /= stat_dict[key].n
        #compute std. deviation.
        for event in event_dict[key]:
            stat_dict[key].std = (stat_dict[key].avg - event.dt())**2
        stat_dict[key].std = math.sqrt( stat_dict[key].std/stat_dict[key].n )
    return stat_dict
def print_all(event_array):
    for event in event_array:
        event.talk_about_yourself()

def stat_report(stat_dict,stats_to_report=None):
    if not stats_to_report:
        stats_to_report = stat_dict.keys()
    for stat in stats_to_report:
        if stat_dict.has_key(stat):
            print "========", stat, "========"
            stat_dict[stat].report()



import numpy as na
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt

class DrawParams:
    start_time = -1
    stop_time = -1
    
    hor_offset = 10
    column_width = 20
    column_sep = 30
    level_offset = 3
    level_un_offset = 0
    
    vert_offset=10
    vert_scale = 1
    vert_right_margin = 10
    vert_total = 800

    dpi = 100

    def __init__(self,event_array = None):
        is_first = True
        if event_array != None:
            for proc in event_array:
                for name in proc.keys():
                    event_list = proc[name]
                    if is_first:
                        start_time = event_list[0].start
                        stop_time = event_list[0].start
                        is_first = False
                    for event in event_list:
                        start_time = min(start_time, event.start)
                        stop_time = max(stop_time,event.end)
            self.start_time = start_time
            self.stop_time = stop_time
        self.vert_scale = (self.vert_total - self.vert_right_margin - self.vert_offset)/ \
                          (self.stop_time - self.start_time)
class box:
    x_left =  0
    x_right = 0
    y_left = 0
    y_right = 0
    def __init__(self,dp,event):
        """dp is a DrawParams object, event is and Event object"""
        self.x_left = dp.hor_offset + ((dp.column_width +
                                        dp.column_sep)*
                                       event.proc_num +
                                       dp.level_offset * event.level )
        self.x_right = self.x_left + dp.column_width - dp.level_un_offset*event.level
        self.y_left = dp.vert_offset + (event.start - dp.start_time)*dp.vert_scale
        self.y_right =self.y_left + max((event.end - event.start)*dp.vert_scale,1)

        self.x_left = int( self.x_left)
        self.y_left = int( self.y_left)

        self.x_left = max([self.x_left,0])
        self.y_left = max([self.y_left,0])

        self.x_right = int(self.x_right)
        self.y_right = int(self.y_right)
        self.x_right = max([self.x_right, self.x_left + 1])
        self.y_right = max([self.y_right, self.y_left + 1])


    def talk(self):
        return "[%f:%f][%f:%f]"%(
            self.x_left, self.x_right, self.y_left, self.y_right)
            
                                       


def img_array(event_array,filename):
    dp = DrawParams(event_array)

    dbg = 0
    counter = 1
    event_colors = {}
    max_levels = 12
    complete_event_list = []
    for proc in event_array:
        for event_name in proc.keys():            
            if event_name not in complete_event_list:
                complete_event_list.append(event_name)
            if not event_colors.has_key(event_name):
                if event_name == 'SMHD':
                    event_colors[event_name] = na.arange(max_levels+1) +max_levels +1
                elif event_name == 'EvolveLevel':
                    event_colors[event_name] = na.arange(max_levels+1) +1
                else: 
                    event_colors[event_name] = na.arange(max_levels+1)+1


    pixel_width = len(event_array) * (dp.column_width + dp.column_sep ) + 2*dp.hor_offset
    pixel_height = dp.vert_total + dp.vert_offset + dp.vert_right_margin


    complete_event_list.append('all')
    big_array = {}
    for event_name in complete_event_list:
        big_array[event_name] = na.zeros( [pixel_height,pixel_width] )
    fig_width = pixel_width/(1.0*dp.dpi)
    fig_height =pixel_height/(1.0*dp.dpi)

    fig = plt.figure(frameon=False, figsize=[fig_height,fig_width], dpi=dp.dpi)	


    sorted_by_time = []
    for proc in event_array:
        for event_name in proc.keys():
            for event in proc[event_name]:
                sorted_by_time.append(event)
    sorted_by_time.sort()
    first = True
    for event in sorted_by_time:
        tb = box(dp,event)
        #counter += 1
        #print tb.talk()

        if dbg > 0:
            event.talk_about_yourself()
            print 'relative (start,end) (%.3e,%.3e) name %s levvel %d color %d'%(
                (event.start - dp.start_time)/(dp.stop_time - dp.start_time),
                (event.end - dp.start_time)/(dp.stop_time - dp.start_time),
                event.name,event.level, event_colors[event.name][event.level])
            print '    position [%d:%d, %d:%d] total (%d,%d)'%(tb.y_left,tb.y_right,
                                                    tb.x_left,tb.x_right,
                                                    big_array[event.name].shape[0],
                                                    big_array[event.name].shape[1])
        for en in [event.name,'all']:
            big_array[en][tb.y_left:tb.y_right,tb.x_left:tb.x_right] =event_colors[event.name][event.level]

            if tb.y_right - tb.y_left  > 1:
                big_array[en][tb.y_right,tb.x_left:tb.x_right]=0
            #big_array[en][tb.y_left,tb.x_left:tb.x_right]=0
            #big_array[en][tb.y_left:tb.y_right,tb.x_left]=0
            #big_array[en][tb.y_left:tb.y_right,tb.x_right]=0

    print "Total Time: %f"%(dp.stop_time - dp.start_time)
    for en in complete_event_list:
        big_array[en] = big_array[en].transpose()

        img = plt.figimage(big_array[en],xo=0,yo=0,cmap=cm.jet)

        #im1 = plt.figimage(Z, xo=50, yo=0, cmap=cm.jet)
        #im2 = plt.figimage(Z, xo=100, yo=100, alpha=.8, cmap=cm.jet)

        this_name = "%s_%s.%s"%(filename.split('.')[0],en,filename.split('.')[1])
        print "k done", this_name
        plt.savefig(this_name)

if __name__ == '__main__':	
    if len(sys.argv) == 1:

        print """
        %> time_parse filename

        Finds lines in filename that match
        ProcNumber "TIME" "Start/End" word

        scrubs the data, reports the result.
        """

    else:
        from optparse import OptionParser
        parser = OptionParser()
        parser.add_option("-d", "--dbg", dest="dbg",action="store",
                          help = "dbg level (0 is off, 100 is very verbose)",
                          default=0, type = "int")
        parser.add_option("-i", "--img", dest="img",action="store",
                          help = "make an image of the use history, stored to IMG",
                          default='NOFILE', type = "string")
        parser.add_option("-s", "--stat", dest="stat", help = "make statistics",
                          default = False, action='store_true')
        parser.add_option("-r", "--report",dest="report", help="Space separated, quoted list of routines to report",
                          default = None, type = 'string')
        (options, args) = parser.parse_args()

        event_array = parse( args[0] , options)	
        if options.stat:
            event_dict = give_dictionary(event_array)
            stat_dict = avg_for_events(event_dict)
            if options.report:
                options_list= options.report.split(" ")
            else:
                options_list = None
                
            stat_report(stat_dict,options_list)
        if options.img != 'NOFILE':
            img_array(event_array,options.img)

