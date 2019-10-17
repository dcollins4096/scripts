#! /bin/tcsh 
#

# m 
# To compile, copy, run, report.  For the extremely lazy.  And vim users.
# Usage:
#     1.) Setup m.local by copying it to the run directory, editing the files.
#     2.) m
#     This will then:
#     1.) change to $src
#     2.) compile $exec
#     3.) change back
#     4.) Copy the exec
#     5.) Run the test 
#     6.) Save str, std out from the run in a file 'dump'
#     
#     If any error is thrown, the system stops.
#
# Options:
#     r: restart (uses $RestartDump)
#     m: multiple processors (set by $nprocRun)
#     nc: no compile (can also be set statically with $Compile == no)
#     t: launch totalview
#     o: only compile
#     c: make clean first
#     s: silent.  Don't tee output to screen.  (setenv silent yes/no/direct in m.local for default. direct does no tee.)
#     v: vim. Launch "vim dump" when finished.
#
# Changes:
#     Removed the -p on the copy step, as dcwan was having troubles with it.
#
#
# User Defined Variables
#

#
# internal flags
#
set linkforf = yes
set Success = yes 
set Parallel = no
set RestartJob = no
set GrepAfter = no
set RunJob = yes
set CleanSrc = no
set HPMcount = no
set RunDebugger = no
set Extract = no
set RunDir = $PWD
set CompileOnly = no
set new_local = no
set make = make
if( -e m.local ) then
    source m.local
    if ( $?Problem == 0 ) then
    echo Please define Problem in m.local
    exit
    endif

else
    if( $1 != 'new' ) then
        echo "No job file-- compile only."
        set RunJob = no
        set Problem = none
        set nprocRun = 0
    else
        set Problem = ""
    endif
endif

if( $?Compile == 0 ) set Compile = yes

if( $?exec == 0 ) set exec = enzo.exe
if( $?RestartClean == 0 ) set RestartClean = no
if( $?RestartDebugging == 0 ) set RestartDebugging = no
if( $?KillExec == 0 ) set KillExec = no
if( $?KillEnzo != 0 ) then
 set KillExec = $KillEnzo
endif
if( $?ExtractionLevel == 0 ) then 
    set ExtractionLevel = 1
endif
if( $?KillDataOnStartup == 0 ) set KillDataOnStartup = "no"
if ( $?dbg == 0 ) set dbg =
#yes, I meant for this to be blank.

echo $Problem

#set tv = "/usr/local/apps/totalview/tv7.0/totalview.7.0.1-0/toolworks/totalview.7.0.1-0/bin//totalview"
set tv = valgrind

#for datastar, "poe" runs on 8 way nodes, "poe32" runs on, you guessed it, a TI-89

if( $?poe == 0 ) then
 set poe = poe
endif

set poeargs = "-rmpool 1 -euilib us -euidevice sn_all"

set vim_when_done = no
if( $?silent == 0 ) set silent = no
#
# Parse Args
#
while( $#argv )
    switch( $1 )
    case "0":
    set nProcCompile = ""
    shift
    breaksw

    case "m":
    set Parallel = "yes"
    shift
    breaksw
    case "clean":
    set Compile = no
    set RunJob = no
    shift
    breaksw

    case "o":
    set RunJob = no
    set CompileOnly = yes
    shift
    breaksw

    case "c":
    set CleanSrc = yes
    shift
    breaksw

    case "h":
    set HPMcount = yes
    shift
    breaksw

    case "t":
    set RunDebugger = yes
    shift
    breaksw

    case "dump":
    set GrepAfter = "yes"
    shift
    set ToGrepFor = $1
    shift
    breaksw

    case "x":
    set Extract = yes
    set Problem = " -x -l $ExtractionLevel -b 0 0 0 -f 1 1 1  $ExtractDump"
    set KillDataOnStartup = "no"
    shift
    breaksw

    case "r":
    set RestartJob = "yes"
    set Problem = "-r  $RestartDump"
    shift
    breaksw

    case "nc":
    set Compile = "no"
    shift
    breaksw

    case "new":
        echo $argv
    set new_local = "yes"
    shift
        echo $argv
    set Problem = $1
    shift
        echo $argv
    if ( $#argv > 0 ) then
        set src = $1
        shift
    endif
        echo $argv
    breaksw

    case "s":
        set silent = yes
        shift
        breaksw

    case "v":
        set vim_when_done = yes
        shift
        breaksw

    default:
        echo "Unrecognized argument" $1
        exit
    breaksw
endsw
end

if( "$silent" == "direct" && $GrepAfter == "yes" ) then
  echo "silent == direct cannot be used with the dump grep option"
  exit
endif
#
# Check consistency
#
if( $silent == direct && $GrepAfter == "yes" ) then
  echo "Cannot grep dump after run, silent == direct "
  exit
endif
#
# New local file.  Only sets the paramert name.
#
if( $new_local == 'yes' ) then
    sed -e 's,setenv\ *Problem.*,setenv Problem '$Problem',' $ScriptDir/m.local > ./m.local
    if ( $?src ) then
        echo "setenv src $src" >> m.local
    endif
    vim m.local
    exit
endif
#
#interdependant parameters:
#

#restart debugging: no fresh runs.
if(  $RestartDebugging == yes ) then
 if(  $CompileOnly != yes && $RestartJob != "yes") then
    echo "RestartDebugging = yes, so you can't do anything that isn't a restart"
    exit
 endif
endif

#no data delete on restart:
if( $RestartJob == "yes" && $KillDataOnStartup == "only_new" ) set KillDataOnStartup = "no"
if( $RestartJob != "yes" && $KillDataOnStartup == "only_new" ) set KillDataOnStartup = "yes"


#
# Set machine dependant crap
#

#
# determine machine name.
#

if( $?machine == 0 ) then
  set machine =  `uname -a | awk '{print $2}'` 
endif

#if( `uname` == Darwin ) then
#        set machine = "MAC"
#endif

#triton?
if( $machine == 'login-4-0.local') then
 set machine = "triton"
endif
if( $machine == 'login-4-40.local') then
 set machine = "triton"
endif
if( $machine == 'login-4-40') then
 set machine = "triton"
endif
if( $machine == 'login-4-41.local') then
 set machine = "triton"
endif

if( `echo $machine | cut -c 1-3` == tcc ) then
 echo "No compiling on the compute nodes on triton"
 if( $Compile == yes) then
    echo $src
    cp $src/$exec .    
 endif    
 set Compile = no
 set machine = "triton"
endif

#Is it verne?
if( `echo $machine |cut -c 1-5` == "verne" ) then
    set machine = "verne"
endif

#determine which tg-login this is:
if( `echo $machine |cut -c 1-6` == "kraken") then
    set machine = "kraken"
endif
if( `uname -a | awk '{print $2}' | cut -f2 -d .` == "ranger") then
    set machine = "ranger"
endif

if ( `echo $machine |cut -c 1-8` == "tg-login" ) then
   if( `hostname -f |cut -d . -f 2` == sdsc ) then
        set machine = "tg-sdsc"
   endif
   if( `hostname -f |cut -d . -f 2` == ncsa ) then
         set machine = "tg-ncsa"
   endif

endif

if( `uname` == Linux ) then
    if( `hostname | cut -c 1-8` == tg-login ) then 
    if( `hostname -f | cut -d . -f 2` == sdsc ) then
        set machine = "tg-sdsc"
    endif
    
    if( `hostname -f | cut -d . -f 2` == ncsa ) then
        set machine = "tg-ncsa"
    endif
    endif
    #Abe login
    if( `hostname | cut -c 1-6 ` == honest ) then
    set machine = "abe_login"
    endif
    if( `hostname |cut -c 1-3` == abe ) then
    set machine = "abe"
    endif
endif

if( `echo $machine | cut -c 1-8` == co-login ) then
    set machine = "cobalt"
endif

echo "machine: " $machine
switch ( $machine )
    case generic_machine:
      set nProcCompile = -j2
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      breaksw
    case mullaghmore:
    case shipsterns:
      set nProcCompile = -j4
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      breaksw
    case picoalto:
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      breaksw
 
    case BW:
      set nProcCompile = -j8
      set srcdir = $src
      #set exeSer = "$exec $dbg $Problem"
      if ( $#nprocNode == 0 ) then
          set nprocNode = 16
      endif
      set exeMPI = "aprun -n $nprocRun -N $nprocNode -cc 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30 -ss $exec $dbg $Problem"
      set exeSer = "aprun -n 1 -N 1 -cc 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30 -ss $exec $dbg $Problem"
      breaksw

    case stampede2:
      set nProcCompile = -j16
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      #set exeSer = "ibrun -o 0  -n 1 $exec $dbg $Problem"
      #set exeMPI = "ibrun -o 0  -n $nprocRun $exec $dbg $Problem"
      set exeSer = "ibrun  -o 0 -n 1 $exec $dbg $Problem"
      set exeMPI = "ibrun $exec $dbg $Problem"
      breaksw

    case stampede:
      set nProcCompile = -j16
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      #set exeSer = "ibrun -o 0  -n 1 $exec $dbg $Problem"
      #set exeMPI = "ibrun -o 0  -n $nprocRun $exec $dbg $Problem"
      set exeSer = "ibrun  -o 0 -n 1 $exec $dbg $Problem"
      set exeMPI = "ibrun -o 0 -n $nprocRun $exec $dbg $Problem"
      #set exeMPI = "ibrun $exec $dbg $Problem"
      breaksw
    case mapache:
      case Nazare:
    case conejo:
    case lobo:
      set nProcCompile = -j16
      set srcdir = $src
      set exeSer = "mpirun  -n 1 $exec $dbg $Problem"
      set exeMPI = "mpirun  -n $nprocRun $exec $dbg $Problem"
    set exeTS = "$tv $exec $dbg $Problem"
    set exeTM = "mpirun  -n $nprocRun $tv $exec $dbg $Problem"
      breaksw
    case mustang:
      set nProcCompile = -j20
      set srcdir = $src
      set exeSer = "$exec $dbg $Problem"
      set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
      breaksw


    case David-Collinss-MacBook-Pro.local:
    case fnord.ucsd.edu:
        case MAC:
        if( `uname -a | awk '{print $2}'` == 1283355 ) then
            if( $?nProcCompile == 0 ) set nProcCompile = -j8
        endif

        set srcdir = $src
        if( $?nProcCompile == 0 ) set nProcCompile = -j2
        #set exeSer = "mpiexec -n 1 $exec $dbg $Problem"
        set exeSer = "$exec $dbg $Problem"
        set exeMPI = "mpirun -n $nprocRun $exec $dbg $Problem"
    breaksw

    case nautilus:
    case harpoon3:
    set srcdir = $src
    if( $?nProcCompile == 0 ) set nProcCompile = 
    if(  $?PBS_NODEFILE  == 0 ) then
        echo "no running without interactive shell. try:"
        echo " qsub -I -V -l walltime=00:30:00,nodes=2:ppn=2"
        set RunJob = no
    else
    if( $?hostfile == 0 ) set hostfile = $PBS_NODEFILE
    set mpirun =  mpiexec 
    set exeSer = "$mpirun -machinefile $hostfile -np 1 $exec $dbg $Problem"
    set exeMPI = "$mpirun -machinefile $hostfile -np $nprocRun $exec $dbg $Problem"
    set exeTS = "$tv aprun -a -n 1 $exec $dbg $Problem"
    set exeTM = "$tv aprun -a -n $nprocRun $exec $dbg $Problem"
    endif
    breaksw

    case triton:
    set srcdir = $src
    if( $?nProcCompile == 0 ) set nProcCompile = -j4
    if(  $?PBS_NODEFILE  == 0 ) then
        echo "no running without interactive shell. try:"
        echo " qsub -I -V -l walltime=00:30:00,nodes=2:ppn=2"
        set RunJob = no
    else
    if( $?hostfile == 0 ) set hostfile = $PBS_NODEFILE
  set mpirun =  /opt/mpich/intel/mx/bin/mpirun
  #set mpirun =  /opt/openmpi/bin/mpirun
    set exeSer = "$mpirun -machinefile $hostfile -np 1 $exec $dbg $Problem"
    set exeMPI = "$mpirun -machinefile $hostfile -np $nprocRun $exec $dbg $Problem"
    set exeTS = "$tv aprun -a -n 1 $exec $dbg $Problem"
    set exeTM = "$tv aprun -a -n $nprocRun $exec $dbg $Problem"
    endif
    breaksw


    case ranger:
    set srcdir = $src
    if( $?nProcCompile == 0 ) set nProcCompile = -j4
    set exeSer = "$exec $dbg $Problem"
    set exeMPI = DONT KNOW
    
    breaksw

    case verne:
    set srcdir = $src
    if( $?nProcCompile == 0 ) set nProcCompile = -j4
    #set exeSer = "mpiexec -n 1 $exec $dbg $Problem"
    set exeSer = "$exec $dbg $Problem"
    set exeMPI = "mpiexec -n $nprocRun $exec $dbg $Problem"
    set exeTS = "$tv mpiexec -a -n 1 $exec $dbg $Problem"
    set exeTM = "$tv mpiexec -a -n $nprocRun $exec $dbg $Problem"
    breaksw

    case kraken:
    echo "yo"
    set srcdir = $src
    if( $?nProcCompile == 0 ) set nProcCompile = -j4
    set exeSer = "aprun -n 1 $exec $dbg $Problem"
    set exeMPI = "aprun -n $nprocRun $exec $dbg $Problem"
    set exeTS = "$tv aprun -a -n 1 $exec $dbg $Problem"
    set exeTM = "$tv aprun -a -n $nprocRun $exec $dbg $Problem"
    breaksw
    
    case cosmos:
    if( $?src == 0 ) set src = "~/enzo-code/amr_mpi/src"

    set srcdir = $src
    
    if( $?nProcCompile == 0 ) set nProcCompile = -j3
    set exeMPI = "mpirun -np $nprocRun  $exec $dbg $Problem"
    set exeSer = "$exec $dbg $Problem"
    breaksw

    

    case ppcluster.ucsd.edu:
        
    if( $?hostfile == 0 ) set hostfile = ~/machinefile

    if( $?nProcCompile == 0 ) set nProcCompile = -j2
    if( $?src == 0 ) then
        set srcdir = "/home/dcollins/enzo-code/amr_mpi/src"
    else
        set srcdir = "$src"
    endif
    set LaunchCommand = "ssh `head -1 $hostfile |cut -f 1 -d ":"` cd `pwd`;"
    set exeMPI = "$LaunchCommand /opt/mpich/gnu/bin/mpirun -np $nprocRun -machinefile $hostfile   $exec  $dbg  $Problem"

    set exeSer = "$exec  $dbg $Problem"
    breaksw


    case ds004:
    case ds011:
    if( $?nProcCompile == 0 ) set nProcCompile = -j8
    set srcdir = "$src"
    set poeargs2 =  "-resd no -hfile ~/NodeFile "
    set exeMPI = "$poe $exec $dbg  $Problem -nodes 1 -tasks_per_node $nprocRun $poeargs2"
    set exeSer = "$poe $exec $dbg  $Problem -nodes 1 -tasks_per_node 1 $poeargs2"
    set exeTS = "$tv $poe -a $exec  $dbg $Problem -nodes 1 -tasks_per_node 1 $poeargs2"
        set exeTM0 = "$tv $poe -a $exec $dbg  $Problem"
    set exeTM = "$exeTM0 -nodes 1 -tasks_per_node $nprocRun $poeargs2"


    breaksw
    case ds100:
    if( $?nProcCompile == 0 ) set nProcCompile = -j8

    set nodes = 0
    set ppn_mach = 8
    set ppn_run = 0
    set total = $nprocRun
    
    if( $total > $ppn_mach ) then
    @ nodes = $total / $ppn_mach
    set ppn_run = $ppn_mach
    else
    set nodes = 1
    set ppn_run = $total
    endif
    echo nodes $nodes ppn $ppn_run

    set srcdir = "$src"

    if( $HPMcount == 'yes') then
       set exeMPI = "$poe hpmcount -o data_hpm $exec $dbg  $Problem -nodes $nodes -tasks_per_node $ppn_run $poeargs"
      set exeSer = "$poe hpmcount -o data_hpm $exec $dbg  $Problem -nodes 1 -tasks_per_node 1 $poeargs"
    else      
       set exeMPI = "$poe $exec $dbg  $Problem -nodes $nodes -tasks_per_node $ppn_run $poeargs"
      set exeSer = "$poe $exec $dbg  $Problem -nodes 1 -tasks_per_node 1 $poeargs"
    endif
    set exeTS = "$tv $poe -a $exec  $dbg $Problem -nodes 1 -tasks_per_node 1 $poeargs"
        set exeTM0 = "$tv $poe -a $exec $dbg  $Problem"
    set exeTM = "$exeTM0 -nodes $nodes -tasks_per_node $ppn_run $poeargs"

    if( $machine == 'ds100' && $poe == 'poe32' ) then
        echo "Can't use poe32 on ds100"
        set RunJob = 'no'
    endif

    breaksw

    case tg-ncsa:

    if( $?nProcCompile == 0 ) set nProcCompile = -j4
    if( $?src == 0 ) then
        set srcdir = "/home/ac/dcollins/enzo-code/amr_mpi/src"
    else
        set srcdir = "$src"
    endif

    #test for the existance of "PBS_NODEFILE"
    if(  $?PBS_NODEFILE  == 0 ) then
        echo "no running without interactive shell. try:"
        echo " qsub -I -V -l walltime=00:30:00,nodes=2:ppn=2"
        set RunJob = no
    else
    set exeMPI = "mpirun -machinefile $PBS_NODEFILE -np $nprocRun $exec $dbg  $Problem"
    set exeSer = "mpirun -machinefile $PBS_NODEFILE -np 1 $exec $dbg  $Problem"
    set exeTM  = "mpirun -machinefile $PBS_NODEFILE -np $nprocRun -tv $exec $Problem"
    set exeTS  = "mpirun -machinefile $PBS_NODEFILE -np 1 -tv $exec $Problem"

    endif

    breaksw

    case tg-c227:
    case tg-sdsc:
    #this machine provides two modes of interactive work.
    #A batch type session or 4 interactive nodes.

    if( $?nProcCompile == 0 ) set nProcCompile = -j4

    if( $?src == 0 ) then
        set srcdir = "/users/ux454321/jb-cvs/amr_mpi/mhd/"
    else
        set srcdir = "$src"
    endif
    #set hostfile = dummy

    #PBS_NODEFILE is given by the batch system.
    #If it exists, run 
    #if not, check if user is on an interactive node.
    #If not on interactive node, issue instruction.  Otherwise, set up the run file
    if( $?PBS_NODEFILE == 0 ) then


        #if there's node 
        set OnInteractiveNode = 0

        foreach node ( tg-c127 tg-c128 tg-c129 tg-c130 )
        if( `hostname` == $node ) then
            set OnInteractiveNode = 1
        endif
        end

        if( $OnInteractiveNode == 1 ) then
        if( $?hostfile == 0 ) set hostfile = /users/ux454321/InteractiveNodes
        else        
        echo "Either:"
        echo " login to tg-c127 tg-c128 tg-c129 tg-c130"
        echo "    or run"
        echo " qsub -I -V -l walltime=00:30:00,nodes=2:ppn=2 "
        echo " NOT GOING TO RUN JOB"
        set RunJob = no
        endif        

    else 
        set hostfile = $PBS_NODEFILE
    endif        

    set exeMPI = "mpirun -machinefile $hostfile -np $nprocRun $exec $dbg  $Problem"
    set exeSer = "mpirun -machinefile $hostfile -np 1 $exec $dbg  $Problem"
    set exeTM  = "mpirun -machinefile $hostfile -np $nprocRun -tv $exec $Problem"
    set exeTS  = "mpirun -machinefile $hostfile -np 1 -tv $exec $Problem"


    breaksw
    case cobalt:
    if( $?nProcCompile == 0 ) set nProcCompile = -j4

    if( $?src == 0 ) then
        set srcdir = "/u/ac/dcollins/enzo-code/amr_mpi/src"
    else
        set srcdir = "$src"
    endif


    set exeMPI = "mpirun -np $nprocRun $exec  $dbg $Problem"
    set exeSer = "mpirun -np 1 $exec  $dbg $Problem"

    endif
    
    breaksw

    #ncsa's ABE
    case abe_login:

    if( $?nProcCompile == 0 ) set nProcCompile = -j8

    if( $?src == 0 ) then
            set srcdir = /u/ac/dcollins/Enzo/MHD/Enzo/amr_mpi/src
        else
            set srcdir = "$src"
        endif

    if( $exec == "enzo.exe" || "$Parallel" == "yes"  ) then
        echo "---- login node only.  No run.----"
        set RunJob = no
        set Compile = yes
    else
        echo "---- login node only.  No run.----"
        set exeSer = "$exec $dbg  $Problem"
        set RunJob = yes
        set Compile = yes
        set exeTM = "echo NoParallel."
        set exeTS = "$tv $exec -a $Problem"
    endif
    breaksw
    case abe:

    if( $?nProcCompile == 0 ) set nProcCompile = -j8

    if( $?src == 0 ) then
            set srcdir = /u/ac/dcollins/Enzo/MHD/Enzo/amr_mpi/src
        else
            set srcdir = "$src"
        endif

    #test for the existance of "PBS_NODEFILE"
    if(  $?PBS_NODEFILE  == 0 ) then
        echo "no running without interactive shell. try:"
        echo " qsub -I -V -l walltime=00:30:00,nodes=2:ppn=2"
        set RunJob = no
    else 

    #old set abe_mpirun = "/opt/mpich-vmi-2.2.0-1-intel/bin/mpirun"
#    set abe_mpirun = "/usr/local/ofed-1.2/mpi/intel/openmpi-1.2.2-1/bin/mpirun"
    set abe_mpirun = mpirun 
    set exeMPI = "$abe_mpirun -machinefile $PBS_NODEFILE -np $nprocRun $exec $dbg  $Problem"
#    set exeSer = "$abe_mpirun -machinefile $PBS_NODEFILE -np 1 $exec $dbg  $Problem"
    set exeSer = "$exec $dbg  $Problem"
    set exeTM  = "$abe_mpirun -tv -machinefile $PBS_NODEFILE -np $nprocRun  $exec $Problem"
    set exeTS  = "$abe_mpirun -tv -machinefile $PBS_NODEFILE -np 1 $exec $Problem"



    echo "------ abe interactive: no compile. ----"
    echo "------ Please compile the code on a different node. ----"
    set Compile = no
    set RunJob = yes
    endif

    breaksw

    
    default:
    echo "Machine Not defined: " $machine
    set Compile = no
    set RunJob = no
    breaksw

endsw
#dbg
#echo $exeMPI
#echo REFORMAT
#exit
#/dbg

if( $Compile == "yes" ) then
set Success = 'no'

    if( $KillExec == yes ) if( -e $exec ) rm $exec

    cd $srcdir
    echo "cd $srcdir"

    if( -e $exec && $KillExec == yes) then 
        rm $exec
    endif
    foreach i ( EvolveLevel.o EvolveHierarchy.o enzo.o )
      if ( -e $i ) rm $i
    end

#
#       clean
#
    if( $linkforf == "yes" && $RunDebugger == yes ) then
           rm *.f
    endif

    if( $CleanSrc == "yes" ) then
        echo Making Clean
        $make clean
    endif


#
#       compile
#

    $make $nProcCompile $exec && set Success = "yes"

#
#       move exec.exe if the recently compiled copy is newer
#

    if( -e $exec ) then
        set t1 = `ls -l $exec | awk '{print($5 $6 $7 $8)}'`
    else
        set t1 = 'moops'
    endif
    if( -e $RunDir/$exec ) then
        set t2 = `ls -l $RunDir/$exec | awk '{print($5 $6 $7 $8)}'`
    else
        set t2 = "monkeys"
    endif

    if( ($t1 != $t2) && ($Success == "yes") ) then
        unalias cp
        echo copying exec


        #cp -p $exec $RunDir || set Success = "NO"
        cp  $exec $RunDir || set Success = "NO"

        #On ncsa teragrid, when copying to gpfs-wan, something gets screwed up with permissions.
        #So an extra check is needed here

        if( $machine == "tg-ncsa" ) then
        if( -e $RunDir/$exec ) then
            set Success = "yes"
        endif

        endif
    else
        if( $Success == "yes" ) then
        echo No exec change.
        else
        echo Sompins Wrong
        endif
    endif

    cd $RunDir

endif


#
# Clean up this directory, to ensure data seen is relevant to what I'm doing.
#

    if( ($RestartJob == no || $RestartClean == "yes") && $RunJob == "yes" ) then

    if( $Success == "yes" && $KillDataOnStartup == "yes") then
      touch data666 file666
      foreach i (OutputLog randomForcing.out Enzo_Build Enzo_Build_Diff performance.out )
          if( -e $i ) rm $i
      end

      set KILL = ""
      foreach start (data cycle time Extra TD DD CD ED)
          set KILL = `find . -maxdepth 1 -name "$start*"`
          if( $?SaveList != 0 ) then
              foreach i ($KILL)
                set saveThis = 0
                foreach save ($SaveList)    
                    if( "$i" =~ *"$save"* ) then
                      echo "save " $i
                      set saveThis = 1
                    endif
                end
                if( $saveThis == 0 ) then
                    rm -rf $i
                    echo "kill " $i
                endif
              end
          else #save list not defined.

             foreach i ($KILL)
               echo rm -rf $i
               rm -rf $i
             end
          endif #savelist
      end

    endif

#    foreach ff (`ls *file* data* *~ *\# .\#* amr.out SRBlog OutputLevelInformation.out core perfdata_* Density *velocity* MagneticField_* Total-Energy amr* dump pie >& pie`)
#        if( -e $ff ) rm $ff
#    end
#
    endif

#
#
# If the compile was successful AND a run is desired,
#
if( -e $exec && $Success == "yes" && $RunJob == "yes") then

#    Moved this to be a part of $exeSer and $exeMPI
#    if( $HPMcount == yes ) then 
#    poe hpmcount $exec -d $Problem |& tee dump
#    endif

    if( $GrepAfter == yes ) then
    echo Will Grep For $ToGrepFor
    endif

    if( $RunDebugger == yes ) then
    
    # This is needed for totalview, 'cause I can't figure out how to get 
    # it to look for .src files instead of .f files.  Makes soft links.

    if( $linkforf == "yes" ) then
        cd $srcdir
        echo linking "*.src" to "*.f"
        Linker.dcc
        cd $RunDir
    endif

    set exeMPI = "$exeTM"
    set exeSer = "$exeTS"
    endif


    if( $Parallel == yes ) then
    echo "parallel " $exeMPI
    if( "$exeMPI" != "no" ) then
        if( $silent == yes ) then
            echo "running silently"
            $exeMPI >& dump
        else if ( $silent == no ) then
            $exeMPI |& tee dump
        else if ( $silent == direct ) then
            $exeMPI
        endif
     endif

    else
        echo "Serial " $exeSer 
        echo "silent" $silent
    if( "$exeSer" != "no" ) then 
        if( $silent == yes ) then
            echo "running silently"
            $exeSer >& dump    
        else if ( $silent == no ) then
            $exeSer |& tee dump
        else if ( $silent == direct ) then
            $exeSer
        endif
    endif
    endif


    if( 1 ) then
        grep -i CLOWN dump
        grep -i kludge dump
    endif
    if( $GrepAfter == yes ) then
    grep $ToGrepFor dump
    endif

    if( $vim_when_done == yes ) then
        $EDITOR dump
    endif
endif # runjob

#
# If extraction, rename the file
# 
    if(  -e $exec && $Success == "yes" && $Extract == yes ) then

    foreach i (9999 9998 9997 9996 9995 9994 9993 9992 9991 9990)
    set DestName = $ExtractDump.grid$i
        if( -e amr_extract0000 && !( -e $DestName ) ) then
        mv -f amr_extract0000 $DestName
        echo "Moved to " $DestName
        endif
    end

    endif
#
# This is the old extraction part.  Now taken care of by renameing the problem
# This bit is kept becaues I may some day want the "extract all" functionality.
#

    if(  -e $exec && $Success == "yes" && $Extract == yes && $?FinishAllExtractionLater == 1 ) then
    if( ! ( -e dump ) ) then
        touch dump
    endif
    if( $ExtractDump != "all" ) then
        echo =============
        echo ============= extract
        echo =============
        #$exec -x -l 1 -b 0 0 0.375 -f 1 1 0.75  $ExtractDump
        #    mv -f amr_extract0000 $Extract.grid9998

        set ExtCmd = "$exec -x -l $ExtractionLevel -b 0 0 0 -f 1 1 1  $ExtractDump"
        if( $RunDebugger == 'yes' ) then
        $tv $poe -a $ExtCmd -nodes 1 -tasks_per_node 1 $poeargs2
        else
        $ExtCmd
        endif

        if( -e amr_extract0000 ) then
        mv -f amr_extract0000 $ExtractDump.grid9999
        endif
    else
        foreach i (*.hierarchy )
        set ExtractName = `basename $i .hierarchy`
        if( ! ( -e $ExtractName.grid9999 ) ) then
            echo $ExtractName
            $exec -x -l $ExtractionLevel -b 0 0 0 -f 1 1 1  $ExtractName >>& dump
            mv -f amr_extract0000 $ExtractName.grid9999
        endif
        end
        endif        
    endif


#        set exeTS = "$tv $poe -a $exec  $dbg $Problem -nodes 1 -tasks_per_node 1 $poeargs"
#        set exeTM0 = "$tv $poe -a $exec $dbg  $Problem"
#        set exeTM = "$exeTM0 -nodes 1 -tasks_per_node $nprocRun $poeargs"
