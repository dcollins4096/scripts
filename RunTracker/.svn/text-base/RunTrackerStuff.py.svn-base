
import os
import string
import glob
import sys
import re

def rematch(filename, regexp, default=None,debug = None):
    """Finds the line in *filename* that matches *regexp*, returns group(1)
    """
    file = open(filename,'r')
    lines = file.readlines()
    file.close()
    nodeCount_re = re.compile(regexp)
    for line in lines:
        match = nodeCount_re.match(line)
        if match != None:
            return match.group(1)
    return default

def DictionaryFromParameterFile(filename):
    """Opens *filename* containing list of
    parameter = value
    pairs, returns a dictionary of
    dict[parameter] = value"""
    if glob.glob(filename) == []:
        print "DictionaryFromParameterFile: Can't make dictionary from missing file:", filename
    param_match = re.compile(r'\s*(\S*)\s*=\s*(\S*)\s*')
    param_file = open(filename, "r")
    params = param_file.readlines()
    paramDic = {}
    for p in params:
        match = param_match.match(p)
        if match != None:
            name = match.group(1)
            if name[0] == "#":
                continue
            value = match.group(2)
            paramDic[ name ] = value
    param_file.close()
    return paramDic

class sysInfo:

    resourceFileName = "~/.RunTracker"
    pendingFileName = "~/.RunTrackerPending"

    cadacInstall = "~/Research/CodeGames/RunTracker"
    runTrackerXMLname = "./RunTracker.xml"
    runTrackerOutputName = "./RunTracker.out"
    runTrackerXMLAlternateName = "./RunTrackerBackup.xml"
    submitCommand  = "ls"
    computerName   = "AnalyticalEngine"
    computerLink   = "http://en.wikipedia.org/wiki/Analytical_engine"
    programName    = "helloWorld"
    programVersion = "0.1"
    programLink    = "www.google.com"
    userName       = "aLovelace"
    userLink       = "http://en.wikipedia.org/wiki/Ada_Lovelace"
    machineProcPerNode = "1"
    batchSystemName = None
    jobName        = "science!"
    jobName_reg    = jobName
    jobID_reg      = ""
    nodeCount_reg  = "node"
    taskCount_reg  = "task"
    queueName_reg  = "name"
    queueTime_reg  = "time"

    jobID_var = None
    stderr_var = None
    stdout_var = None

    debug = 0

    def __init__(self):
        """Initializes the sysInfo object by populating sysInfo.__dict__ with the contents of ~/.RunTracker"""
        filename = os.path.expanduser(self.resourceFileName)

        if glob.glob(filename) == []:
            print "Gsubmit: Requires a", self.resourceFileName, "file.  See documentation for details."
            sys.exit(1)
        
        #Convert parameters in file to members in object

        self.__dict__.update( DictionaryFromParameterFile(filename) )

        self.cadacInstall = os.path.expanduser(self.cadacInstall)
        if not hasattr(self,'submitCommand'):
            print "Undefined Submit Script.  Please add the line"
            print "   submitCommand = qsub"
            print "to",self.resourceFileName," with qsub replaced by your schedulers submit script"
            self = None

    def returnJobName(self,scriptFile):
        """Parses Job Name from *scriptFile* using sysInfo.jobName_reg.
        Most machines have some sort of sensible default, this is currently unaware."""
        output = rematch(scriptFile,self.jobName_reg,debug=self.debug)
        if self.debug > 2:
            print "jobName_reg =", self.jobName_reg, "matched", output
        return output

    def returnNodeCount(self,scriptFile):
        output= rematch(scriptFile,self.nodeCount_reg)
        if self.debug > 2:
            print "nodeCount_reg", self.nodeCount_reg, "matched", output
        return output
    def returnTaskCount(self,scriptFile):
        output = rematch(scriptFile,self.taskCount_reg)
        if self.debug > 2:
            print "taskCount_reg", self.taskCount_reg, "matched",output
        return output
    def returnTaskPerNode(self,scriptFile):
        output = rematch(scriptFile,self.taskPerNode_reg)
        if self.debug>2:
            print "taskPerNode_reg", self.taskPerNode_reg, "matched", output
        return output
    def returnQueueName(self,scriptFile):
        output = rematch(scriptFile,self.queueName_reg)
        if self.debug > 2:
            print "queueName_reg",self.queueName_reg, "matched", output
        return output

    def returnQueueTime(self,scriptFile):
        output = rematch(scriptFile,self.queueTime_reg)
        return output

    def returnJobID(self,myout):
        match = re.match(self.jobID_reg,myout)
        if match != None:
            return match.group(1)
        else:
            return None
        
    def deriveOutputNames(self,jobID=None, stdout=None, stderr=None, debug=0 ):
        if self.batchSystemName == "LoadLeveler":
            if jobID == None:
                jobID = os.getenv('LOADL_STEP_ID')
                if debug > 0:
                    print "jobID1", jobID
                if jobID != None:
                    jobID = jobID[0:-2] #cuts off the trailing .0
                if debug > 0:
                    print "jobID", jobID
            if stdout == None:
                stdout = os.getenv('LOADL_STEP_OUT')
            if stderr == None:
                stderr = os.getenv('LOADL_STEP_ERR')
            if debug > 0:
                print "stderr", stderr
                print "stdout", stdout
        elif self.batchSystemName == "PBS":
            jobID_env = os.getenv('PBS_JOBID')
            if debug > 0:
                print "jobID_env =",jobID_env
            jobName = os.getenv('PBS_JOBNAME')
            if debug > 0:
                print "jobName =",jobName
            if jobID == None:
                jobID = jobID_env
            if jobName != None and jobID_env != None:
                jobID_num = jobID_env[0: jobID.find('.')]
                if debug > 0:
                    print "jobID_env 2 =",jobID_env
                    print "stdout = ", stdout
                    print "stderr = ", stderr
                if stdout == None:
                    stdout = jobName + ".o" + jobID_num
                if stderr == None:
                    stderr = jobName + ".e" + jobID_num
                if debug > 0:
                    print "jobID_env 2 =",jobID_env
                    print "stdout = ", stdout
                    print "stderr = ", stderr                    
        else:
            print "No way to derive outputfile names for batch system",self.batchSystemName
        return [jobID,stdout,stderr]
    
    def setPending(self,jobId, uuid):
        filename = os.path.expanduser(self.pendingFileName)
        cwd = os.getcwd()
        stringToWrite = cwd + " , " + jobId + " , " + uuid + "\n"
        #print stringToWrite
        file = open(filename,'a')
        file.write(stringToWrite)
        file.close
    def returnPending(self):
        filename = os.path.expanduser(self.pendingFileName)
        output = []
        if glob.glob(filename) != []:
            file = open(filename,'r')
            allPending = file.readlines()
            file.close
            for line in allPending:
                list = line.split(",")
                output.append({"directory":string.strip(list[0]),\
                               "jobID":string.strip(list[1]),\
                               "uuid":string.strip(list[2])})
        return output
