#!/usr/bin/env python
"""Scrubs the input file for parameter filename, and [initial,final]\times[time,cycle,dt]."""


execfile('/home1/00369/tg456484/yt3_scripts/go_lite')
from optparse import OptionParser
import glob
import sys
import re
from datetime import *
from xml.dom import minidom


try:
    import cadac
    import RunTrackerStuff
    sysInfo = RunTrackerStuff.sysInfo() #Get info about the system and user.
    sys.path.append(sysInfo.cadacInstall)
    RunTracker_on = True
except:
    RunTracker_on = False
    sysInfo = None

class stepInfo:
    dt = -1
    time = -1
    cycle = -1
    wall = None
    set = False
parser = OptionParser("DaveParse.py output")
parser.add_option("-o","--stdout", dest="stdout", action="store",default=None,type="string")
parser.add_option("-e","--stderr", dest="stderr", action="store",default=None,type="string")
parser.add_option("-j","--jobID", dest="jobID", action="store",default=None,type="string")
(options, args) = parser.parse_args()

#I started trying to discriminate between stderr and stdout,
#but I don't think it matters.
if options.stderr:
    if glob.glob(options.stderr) ==[]:
        sys.stderr.write("DaveParse.py: file "+options.stderr+" not found.\n")
        sys.exit(1)
    filename = options.stderr


def scrubParameterFile(string):
    """Matches each line in the file *string* (good name, eh?) to the regular expressions
    in re_list.
    This isn't presently used."""
    
    if string == None:
        return None
    print "Param File To Open: ", string
    if glob.glob(string) == []:
        return None

    file = open(string, 'r')
    pa = []
    re_list = []
    re_list.append(re.compile(r'\s*(TopGridDimensions)\s*=\s*(\d*)\s*(\d*)\s*(\d*)'))

    for line in file:
        if len(re_list) == 0:
            break
        for reg in re_list:
            match = reg.match(line)
            if match != None:
                re_list.remove(reg) #save us some effort.
                #This is where you should put the new parameters.
                if match.group(1) == 'TopGridDimensions':
                    pa.append(cadac.Parameter('TopGridDimensions0',match.group(2)))
                    if match.group(3) != '':
                        pa.append(cadac.Parameter('TopGridDimensions1',match.group(3)))
                    if match.group(4) != '':
                        pa.append(cadac.Parameter('TopGridDimensions3',match.group(4)))
        
                elif match.group(1) == "monkey":
                    monkey = "wtf?"
    plist = cadac.ParameterList(pa)
    file.close
    return plist

def scrub_log_file(filename):
    file = open(filename,'r')

    initialFile_start = re.compile(r'.*Successfully read in parameter file\s+(\S+)\.+')
    initialFile_restart = re.compile(r'.*Successfully read ParameterFile\s+(\S+).+')
    initialFileString = None

    oldTicker = re.compile(r'.*TopGrid\s*cycle\s*=\s*(\S+)\s*dt\s*=\s*(\S*)\s*time\s*=\s*(\S+)\s*(wall = (\S+))?')
    newTicker = re.compile(r'.*STEP_INFO\s*N\s*=\s*(\S+)\s*\s*DT\s*=\s*(\S+)\s*,?\s*T\s*=\s*(\S+)')
    weekOfCodeTicker_with_wall = re.compile(r'.*TopGrid\s*dt\s*=\s(\S+)\s*time\s*=\s*(\S+)\s*cycle\s*=\s*(\S+)\s*(wall = (\S+))?')
    #weekOfCodeTicker = re.compile(r'.*TopGrid\s*dt\s*=\s(\S+)\s*time\s*=\s*(\S+)\s*cycle\s*=\s*(\S+)')
    weekOfCodeTicker = re.compile(r'.*TopGrid\s*dt\s*=\s(\S+)\s*time\s*=\s*(\S+)\s*cycle\s*=\s*(\S+)\s*z\s*=\s*(\S+)')
#weekOfCodeTicker = re.compile(r'.*TopGrid\s*dt\s*=\s(\S+)\s*time\s*=\s*(\S+)\s*cycle\s*=\s*(\S+)\s*(wall = (\d*\.\d*))?C.*)?')
#TopGrid dt = 1.690168e-06     time = 0.025478588    cycle = 10500
    old_map = {'cycle':1,'dt':2,'time':3,'wall':5}
    woc_map_wall = {'cycle':3,'dt':1,'time':2,'wall':5}
    woc_map = {'cycle':3,'dt':1,'time':2,'wall':5}
    TickerList = [(woc_map,weekOfCodeTicker), (old_map,oldTicker), (old_map,newTicker),(woc_map_wall, weekOfCodeTicker_with_wall)]
    initialStepInfo = stepInfo()
    finalStepInfo = stepInfo()
    firstTime=True

    last_ten_lines = []
    all_steps = {'cycle':[], 'dt':[], 'time':[]}
    for line in file: 

        last_ten_lines.append(line)
        if len(last_ten_lines) == 11:
            last_ten_lines.pop(0)
        match = initialFile_start.match(line)
        if match != None:
            initialFileString = match.group(1)
            continue
        
        match = initialFile_restart.match(line)
        if match != None:
            initialFileString = match.group(1)
            continue
        
        for reg_map,ticker in TickerList:
            match = ticker.match(line)
            if match != None:
                if firstTime == True:
                    initialStepInfo.cycle = match.group(reg_map['cycle'])
                    initialStepInfo.dt = match.group(reg_map['dt'])
                    initialStepInfo.time = match.group(reg_map['time'])
                    initialStepInfo.set = True
                    firstTime = False
                    all_steps['cycle'].append(initialStepInfo.cycle)
                    all_steps['dt'].append(initialStepInfo.dt)
                    all_steps['time'].append(initialStepInfo.time)
                    try:
                        initialStepInfo.wall = match.group(reg_map['wall'])
                    except:
                        pass
                    TickerList = [(reg_map,ticker)]
                else:
                    finalStepInfo.cycle = match.group(reg_map['cycle'])
                    finalStepInfo.dt = match.group(reg_map['dt'])
                    finalStepInfo.time = match.group(reg_map['time'])
                    finalStepInfo.set = True
                    all_steps['cycle'].append(finalStepInfo.cycle)
                    all_steps['dt'].append(finalStepInfo.dt)
                    all_steps['time'].append(finalStepInfo.time)
                    try:
                        finalStepInfo.wall = match.group(reg_map['wall'])
                    except:
                        pass

    file.close()

    if 1:
        plt.clf()
        plt.plot(all_steps['cycle'], all_steps['dt'])
        plt.xlabel('cycle'); plt.ylabel('dt')
        plt.savefig(filename+'_cycle_dt.pdf')
        plt.yscale('log')
        plt.savefig(filename+'_cycle_dt_log.pdf')
        plt.clf()
        plt.plot(all_steps['time'], all_steps['dt'])
        plt.xlabel('time'); plt.ylabel('dt')
        plt.savefig(filename+'_time_dt.pdf')
        plt.yscale('log')
        plt.savefig(filename+'_time_dt_log.pdf')

    if RunTracker_on:
        ua=[]
        if initialFileString != None:
            ua.append(cadac.UserField('startFile',initialFileString))
        if initialStepInfo.set and not finalStepInfo.set:
            #then the first step wasn't finished.
            finalStepInfo = initialStepInfo
        ua.append(cadac.UserField('init_time',initialStepInfo.time ))
        ua.append(cadac.UserField('final_time',finalStepInfo.time ))

        ua.append(cadac.UserField('init_cycle',initialStepInfo.cycle))
        ua.append(cadac.UserField('final_cycle',finalStepInfo.cycle ))

        ua.append(cadac.UserField('init_dt',initialStepInfo.dt ))
        ua.append(cadac.UserField('final_dt',finalStepInfo.dt ))

        userlist = cadac.UserFieldList(ua)

        parameterList = None #scrubParameterFile(initialFileString)

        output_dom = minidom.parseString('<appendMe></appendMe>')

        list_dom= minidom.parseString(userlist.toxml()).firstChild
        output_dom.firstChild.appendChild(list_dom)

        if parameterList != None:
            param_dom = minidom.parseString(parameterList.toxml()).firstChild
            output_dom.firstChild.appendChild(param_dom)

        #Sanatize wall info. This should be in the regexp, but my regexp-fu is weak today.
        if 'C' in finalStepInfo.wall:
            finalStepInfo.wall = finalStepInfo.wall[ :finalStepInfo.wall.index('C') ]
        if 'C' in initialStepInfo.wall:
            initialStepInfo.wall = initialStepInfo.wall[ :initialStepInfo.wall.index('C') ]

        if initialStepInfo.wall != None:
            #This sure is a lot of work for one line of xml.
            #there has to be an easier way...
            round = int(float(initialStepInfo.wall))  #really don't care about microseconds.

            iso_string = datetime.fromtimestamp(round).isoformat()
            start_xml=minidom.parseString('<StartTime>'+iso_string+'</StartTime>').firstChild
            output_dom.firstChild.appendChild( output_dom.createTextNode('\n'))
            output_dom.firstChild.appendChild(start_xml)

        if finalStepInfo.wall != None:
            round = int(float(finalStepInfo.wall))  #really don't care about microseconds.
            iso_string = datetime.fromtimestamp(round).isoformat()
            end_xml=minidom.parseString('<EndTime>'+iso_string+'</EndTime>').firstChild
            output_dom.firstChild.appendChild( output_dom.createTextNode('\n'))
            output_dom.firstChild.appendChild(end_xml)

        if initialStepInfo.wall != None and finalStepInfo.wall != None:
            difference = int( float(finalStepInfo.wall) - float(initialStepInfo.wall) )
            hours = int( difference/3600 )
            minutes = int( (difference - hours*3600)/60 )
            runtime_xml = minidom.parseString('<RunTime>%d:%02d</RunTime>'%(hours,minutes)).firstChild
            output_dom.firstChild.appendChild( output_dom.createTextNode('\n'))
            output_dom.firstChild.appendChild(runtime_xml)
        sys.stdout.write( output_dom.toxml())
        sys.stdout.write("\n")

    else:
        outdict = {}
        outdict['dti'] = initialStepInfo.dt
        outdict['dtf'] = finalStepInfo.dt
        outdict['timei'] = initialStepInfo.time
        outdict['timef'] = finalStepInfo.time
        outdict['cyclei'] = initialStepInfo.cycle
        outdict['cyclef'] = finalStepInfo.cycle

        for line in last_ten_lines:
            print line[:-1]
        print "\n\n"

        #print "%(dti)s %(dtf)s %(timei)s %(timef)s %(cyclei)s %(cyclef)s"%outdict
    return {'initialStepInfo':initialStepInfo,'finalStepInfo':finalStepInfo}




def parse_perf(initialStepInfo,finalStepInfo,fname='performance.out'):
    fptr = open(fname,'r')
    ncore_re = re.compile(r'# Starting performance log. MPI processes:\s*(\d*)')
    cycle_re = re.compile(r'Cycle_Number\s*(\d*)')
    taking_data = False
    total_time = 0
    total_up = 0
    for line in fptr:
        match = ncore_re.match(line)
        if match != None:
            ncore=int( match.group(1))
            continue
        match = cycle_re.match(line)
        if match is not None:
            cycle = int(match.group(1))
            if cycle >= initialStepInfo.cycle:
                taking_data=True
            if cycle > finalStepInfo.cycle:
                taking_data=False
            continue
        if line.startswith('Total'):
            bits = []
            for bit in line.split(" "):
                if len(bit):
                    #get rid of extra spaces
                    bits.append(bit)
            # mean time(1), stddev time(2), Tmin (3), Tmax(4), Nupdates (5), Ngrids (6), mean cell updates/s/processor(7)
            # I believe that max time is the one to take, as it sets the performance
            # for the whole level.
            total_time += float(bits[4])
            total_up += float(bits[5])
    return {'proc':ncore,'coresec':ncore*total_time,'cellup':total_up, 'cspercu':(ncore*total_time/total_up)}

log_out=scrub_log_file(args[0])
#dumb_Initial=stepInfo
#dumb_Final = stepInfo
#dumb_Initial.cycle = 0
#dumb_Final.cycle = 5
#perf_out=parse_perf(dumb_Initial,dumb_Final)
perf_out = parse_perf(log_out['initialStepInfo'],log_out['finalStepInfo'])
outdict = {}
outdict['dti'] =   log_out['initialStepInfo'].dt
outdict['dtf'] =   log_out['finalStepInfo'].dt
outdict['timei'] = log_out['initialStepInfo'].time
outdict['timef'] = log_out['finalStepInfo'].time
outdict['cyclei'] =log_out['initialStepInfo'].cycle
outdict['cyclef'] =log_out['finalStepInfo'].cycle
outdict.update(perf_out)


print "%(dti)s %(dtf)s %(timei)s %(timef)s %(cyclei)s %(cyclef)s %(cellup)0.3e %(coresec)0.2e %(cspercu)0.3e"%outdict
print "then also", perf_out


#end
