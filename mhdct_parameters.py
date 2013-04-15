#!/usr/bin/env python

def no_white_array(something):
    """Removes any empty charachters"""
    out = []
    for s in something:
        if s != '':
            out.append(s)
    return out

def no_whites(something):
    """Removes any empty charachters"""
    out = ""
    for s in something:
        #print "."+s+".",
        if s not in  ['', ' ', '\n']:
            out += s
    #print "x"
    return out

import sys
fname = sys.argv[1]
new_name = fname + ".new"

fptr = open(fname,'r')
optr = open(new_name,'w')

#MHD_WriteElectric;
#tiny_pressure;
#useMHDCT;
#EquationOfState;
#*MHDLabel[3];
#*MHDcLabel[3];
#*MHDUnits[3];
#*MHDeLabel[3];
#*MHDeUnits[3];

ParametersToSkip = ['MHD_Equation', 'MHD_Used']

lines = fptr.readlines()

#first check for MHDCT.
useMHDCT = False
for line in lines[:]:
    both = line.split("=")
    parameter = both[0]
    parameter = no_whites(parameter)
    if parameter == 'HydroMethod':
        value = no_whites(both[1])
        if value == '6':
            useMHDCT = True

if useMHDCT:
    #the parameter array MHDLi overrides these values.
    ParametersToSkip += ['ReimannSolver', 'ReconstructionMethod']

for line in lines[:]:
    both = line.split("=")
    if len(both) != 2:
        optr.write(line)
        continue
    parameter = both[0]
    parameter = no_whites(parameter)
    value = both[1]
    if parameter == 'MHD_DivBparam':
        optr.write('CT_AthenaDissipation = %s'%value)
        continue
    if parameter == 'MHD_DivB':
        optr.write('MHD_CT_Method = %s\n'%{'0':'0','1':'1','5':'3','6':'2','7':'1'}[no_whites(value)])
        continue
    if parameter in ParametersToSkip:
        continue
    if parameter == 'MHDLi':
        all = no_white_array(value.split(" "))
        print line
        print all
        #Dual Energy method-- 0: off 1:Entropy 2: Internal Energy
        optr.write('MHDCTDualEnergyMethod = %s\n'%no_whites(all[0]))

        #Slope limiter-- 0: constant, primitive, 1: minmod, primitive, 2: vanLeer, primitive
        #                3: characteristic, conserved, 4: characteristic, primitive
        slope_limiter = no_whites(all[1])
        if slope_limiter < '9':
            optr.write('MHDCTSlopeLimiter = %s\n'%slope_limiter)
        elif slope_limiter == '11':
            optr.write('MHDCTSlopeLimiter = 4\n')
        else:
            optr.write('MHDCTSlopeLimiter = 3\n')
        #1: HLL, 2: HLLC w/ Bartens 3: HLLE 4: HLL + stuff 5: HLLC + stuff 6: HLLD
        optr.write('ReimannSolver = %s\n'%no_whites(all[2]))

        #Predictor: 0: PLM, 6: MUSCL-Hancock; 7: Piecewise Constant
        predictor_old = no_whites(all[3])
        predictor_map = {'1':'0', '2':'6', '3':'7'}
        predictor_new = predictor_map[predictor_old]
        optr.write('ReconstructionMethod = %s\n'%(predictor_new))

        #Powell type source terms.
        optr.write('MHDCTPowellSource = %s\n'%no_whites(all[4]))
                
        continue
    optr.write(line)
    

fptr.close()
optr.close()
print "Make a decision about MHDCTUseSpecificEnergy"


#end
