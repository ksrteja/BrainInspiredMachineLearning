<<<<<<< 40554d4b39f49f8d2ddf16a4a60c77c7818d6926:Project_InFComptetiveLearning/InF.py
from brian2 import *

Cm = 50*pF; gl = 1e-9*siemens; taus = 20*ms
Vt = 50*mV; Vr = 0*mV; 


InFEquations = '''
dv/dt  = -gl*v/Cm + isyn/Cm: volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
'''

threshold='v>Vt'
reset='v = Vr'
refractory=4*ms
method='euler'
=======
from brian2 import *

Cm = 50*pF; gl = 1e-9*siemens; taus = 20*ms
Vt = 50*mV; Vr = 0*mV; 


CLEquations = '''
dv/dt  = -gl*v/Cm + isyn/Cm: volt (unless refractory)
disyn/dt  = -isyn/taus : amp 
'''

threshold='v>Vt'
reset='v = Vr'
refractory=4*ms
method='euler'
>>>>>>> Bug in test_model fixed. Clean up:Project_ComptetiveLearning/CompetetiveLearning.py
