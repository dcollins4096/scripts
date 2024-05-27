#!/usr/bin/env python
import numpy as np
mach = 4.7
d=1
#alfspeed = B/np.sqrt(d)
#alfmach = mach/alfspeed = mach*np.sqrt(d)/B

alfmach = 1.5
B = mach*np.sqrt(d)/alfmach*np.sqrt(4*np.pi)
print("Mach",mach,"Alfmach",alfmach,"B",B, "Mach 1d", mach/np.sqrt(3))
print("tdyn", 0.5/mach)

alfmach = 3
B = mach*np.sqrt(d)/alfmach*np.sqrt(4*np.pi)
print("Mach",mach,"Alfmach",alfmach,"B",B, "Mach 1d", mach/np.sqrt(3))
print("tdyn", 0.5/mach)

alfmach = 0.75
B = mach*np.sqrt(d)/alfmach*np.sqrt(4*np.pi)
print("Mach",mach,"Alfmach",alfmach,"B",B, "Mach 1d", mach/np.sqrt(3))
print("tdyn", 0.5/mach)

#end
