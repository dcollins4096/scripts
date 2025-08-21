#!/usr/bin/env python
import numpy as np
mach = 2
d=1
#alfspeed = B/np.sqrt(d)
#alfmach = mach/alfspeed = mach*np.sqrt(d)/B

for alfmach in [3, 4]:
    B = mach*np.sqrt(d)/alfmach*np.sqrt(4*np.pi)
    print("Mach",mach,"Alfmach",alfmach,"B",B, "Mach 1d", mach/np.sqrt(3))
    tdyn = 0.5/mach
    print("tdyn", tdyn, "tstop", 5*tdyn, "dt", 0.05*tdyn)

