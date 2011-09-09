#
# dcc: 
# setenv HDF5_INSTALL <something useful>
# setenv HDF4_INSTALL <something useful>

#=======================================================================
#  MAKEFILE FOR HDF5 UNIGRID "GLUE" TOOLS
#  Robert Harkness, April 2003
#=======================================================================
#
# ENZO_PPR is one of p4 (single), p8 (double) or p16 (quad) for
#          precision of position
# ENZO_XPR is r4 (32 bits) or r8 (64 bits) for float and real and
#          MUST be <= precision of position
# FORTPR   defines how Fortran real precision is specified to the
#          compiler e.g. SGI -r8; IBM -qrealsize=8
#
# The process of building ENZO executables can be controlled by setting
# the following environment variables:
#
# name       default     allowed values
# ENZO_PPR   p8          p4, p8, p16
# ENZO_XPR   r8          r4, r8
# ENZO_HDF   hdf5        hdf4, hdf5
# ENZO_END   HDF5_BE     HDF5_BE, HDF4_LE (not recommended)
#
# The makefile will attempt to determine the operating system and
# its default message-passing library (in most cases MPI), but by
# setting the following environment variables one can easily
# experiment with new systems. All that is required is consistency
# in the naming convention, and machine-specific include files
# for HDF4 or HDF5.  It may also be necessary to specify FORTPR.
#
# ENZO_ARCH  auto        anything you like (e.g. cray_x1)
# ENZO_MESS  auto        mpi, vmi, mpich etc.
# ENZO_MESS  nompi       none of these tools use MPI (12 April 03)

null :=
hdf4 := hdf4
hdf5 := hdf5

ifeq ($(ENZO_PPR),$(null))
  ENZO_PPR := p8
endif
ifeq ($(ENZO_XPR),$(null))
  ENZO_XPR := r8
endif

SYSTEM := $(shell uname -s)
UNAMEM := $(shell uname -m)
<<<<<<< Makefile
ENZO_ARCH = ranger
ENZO_MESS = nompi
=======

ENZO_ARCH = kraken
ENZO_MESS = nompi
>>>>>>> 1.4
ifeq ($(ENZO_ARCH),$(null))

ifeq ($(SYSTEM),IRIX64)
  ENZO_ARCH = irix64
  ENZO_MESS = nompi
  ifeq ($(ENZO_XPR),r8)
    FORTPR = -r8 -r8const -d8
  endif
endif

ifeq ($(SYSTEM),OSF1)
  ENZO_ARCH = osf64
  ENZO_MESS = nompi
  ifeq ($(ENZO_XPR),r8)
    FORTPR = -real_size 64 -double_size 64 -fpconstant
  endif
endif

ifeq ($(SYSTEM),AIX)
  ifeq ($(OBJECT_MODE),$(null))
    ENZO_ARCH = aix32
    ENZO_MESS = nompi
  endif
  ifeq ($(OBJECT_MODE),64)
    ENZO_ARCH = aix64
    ENZO_MESS = nompi
  endif
  ifeq ($(ENZO_XPR),r8)
    FORTPR = -qrealsize=8 -qdpc=e
  endif
endif

ifeq ($(SYSTEM),SunOS)
  ENZO_ARCH = sun64
  ENZO_MESS = nompi
  ifeq ($(ENZO_XPR),r8)
    FORTPR = -xtypemap=real:64,double:64
  endif
endif

ifeq ($(SYSTEM),Linux)
  ifeq ($(UNAMEM),ia64)
    ENZO_ARCH = tg64
    ENZO_MESS = nompi
  endif
  ifeq ($(UNAMEM),i686)
    ENZO_ARCH = i686
    ENZO_MESS = nompi
  endif
  ifeq ($(UNAMEM),x86_64)
    ENZO_ARCH = x86_64
    ENZO_MESS = nompi
  endif
  ifeq ($(ENZO_XPR),r8)
    FORTPR = -r8
  endif
endif

endif

ifeq ($(ENZO_HDF),$(null))
  ENZO_HDF := hdf5
endif

ifeq ($(ENZO_END),$(null))
  ENZO_END := HDF5_BE
endif

ifeq ($(SYSTEM),Linux)
  CPP_FLAG := -traditional
endif


#-------------------  object files  ------------------------------------

ifeq ($(ENZO_HDF),$(hdf5))
  HDV := HDF5
endif

ifeq ($(ENZO_HDF),$(hdf4))
  HDV := HDF4
endif

MGLUE_OBJ := mglue.o crack_b.o
XGLUE_OBJ := xglue.o crack.o
DGLUE_OBJ := dark_glue.o crack.o
PMERG_OBJ := pmerge.o crack.o

#-------------------  macro definitions -------------------------------

.SUFFIXES:
.SUFFIXES: .src .c .f .o .C

EXEDIR  =

SHELL   = csh

#------------------ include machine-dependent macros -----------------

INCLUDE_MAKEFILE = MakeMacros/${ENZO_HDF}/Make.${ENZO_ARCH}.${ENZO_MESS}
include ${INCLUDE_MAKEFILE}

#--------------------  implicit rules ---------------------------------
dbg:
	echo ${INCLUDE_MAKEFILE}
.src.o:
	${CPP} ${DEFINES} -P ${CPP_FLAG} $< > $*.f
	${FC} ${FC_OPT} ${DEBUG} ${OPTS} $*.f
.C.o:
	${CCxx} ${CCxx_OPT} -D ${ENZO_XPR} -D ${ENZO_END} ${DEBUG} ${OPTS} $*.C
.c.o:
	${CC} ${CC_OPT} -D ${ENZO_XPR} -D ${ENZO_END} ${DEBUG} ${OPTS} -c $<

#-------------------------  main targets  -------------------------------

mglue: ${MGLUE_OBJ}
	${LDR} ${LDR_OPT} ${DEBUG} -o ${EXEDIR}mglue ${MGLUE_OBJ} ${LIB}

xglue: ${XGLUE_OBJ}
	${LDR} ${LDR_OPT} ${DEBUG} -o ${EXEDIR}xglue ${XGLUE_OBJ} ${LIB}

dglue: ${DGLUE_OBJ}
	${LDR} ${LDR_OPT} ${DEBUG} -o ${EXEDIR}dglue ${DGLUE_OBJ} ${LIB}

pmerge: ${PMERG_OBJ}
	${LDR} ${LDR_OPT} ${DEBUG} -o ${EXEDIR}pmerge ${PMERG_OBJ} ${LIB}

#---------------------  special compilation rules ---------------------


#----------------------------- help ------------------------------------

help:
	@echo Type 'make' to generate executable
	@echo Type 'make clean' to remove object files, etc

#----------------------------- clean ------------------------------------

clean:
	rm -f *.o mglue xglue dglue pmerge

#-----------------------------------------------------------------------

${OBJ}: ${HEADER}
