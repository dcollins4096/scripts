#!/usr/bin/env python
import h5py
import sys
setname = sys.argv[1]
fptr = h5py.File(setname,'r')
print setname, fptr[setname].shape, fptr[setname].attrs['Dimensions']
fptr.close()
#end
