from ProjectUtil import *
from Izhikevich import *
from Constants import *
import numpy as np

# ------------------------layer 1 dynamics-------------------------#

data, labels = data_load_mnist(DIGITS)
data = (data.T / (data.T).sum(axis=0)).T

inarr = []
tarr = []

start = data.shape[0] - 50
for index in range(start, start + NumOfDigitsTest):
    print "Label : {0}".format(labels[index - start])
    ret = np.array(np.nonzero(data[index - start].reshape(28, 28))).T
    indicesArray = np.array(ret[:, 0])
    timeArray = np.array(ret[:, 1]) + ((index - start) * DIGIT_DURATION / ms)
    inarr.extend(indicesArray)
    tarr.extend(timeArray)

P1st = SpikeGeneratorGroup(M, inarr, tarr * ms)

# ------------------------layer 2 dynamics-------------------------#

P2nd = NeuronGroup(N/ K_VALUE, IzhikevichEquations, threshold=threshold, reset=reset)

# --------------------connecting layer 1 and layer 2-------------------#
syn12 = Synapses(P1st, P2nd, on_pre=Syn12Condition)
syn12.connect("i/K_VALUE == j")


# ------------------------layer 3/op dynamics-------------------------#


P3rd = NeuronGroup(NUM_OUTPUT_CLASSES, IzhikevichEquations, threshold=threshold, reset=reset)

syn23 = Synapses(P2nd, P3rd, '''w : 1
                        ''',
               on_pre='''I += 100 * w * volt/second
                        ''')


syn23.connect()

# syn23.w = [0.008, 0.008, 0.041, 0.028, 0.033, 0.070, 0.109, 0.137, 0.158, 0.155, 0.132, 0.105, 0.008, 0.008,
# 0.009, 0.010, 0.062, 0.147, 0.100, 0.034, 0.026, 0.051, 0.147, 0.190, 0.142, 0.063, 0.009, 0.009,
# 0.009, 0.009, 0.130, 0.190, 0.083, 0.045, 0.076, 0.062, 0.018, 0.026, 0.122, 0.186, 0.033, 0.010,
# 0.010, 0.010, 0.010, 0.028, 0.082, 0.138, 0.187, 0.208, 0.159, 0.055, 0.036, 0.038, 0.029, 0.010,
# 0.008, 0.008, 0.020, 0.065, 0.092, 0.117, 0.137, 0.152, 0.051, 0.105, 0.144, 0.088, 0.008, 0.008,
# 0.009, 0.033, 0.051, 0.043, 0.051, 0.071, 0.132, 0.165, 0.171, 0.151, 0.097, 0.011, 0.009, 0.009,
# 0.010, 0.010, 0.010, 0.079, 0.199, 0.114, 0.069, 0.045, 0.051, 0.044, 0.066, 0.091, 0.151, 0.063,
# 0.006, 0.006, 0.032, 0.084, 0.114, 0.127, 0.113, 0.055, 0.089, 0.113, 0.113, 0.112, 0.029, 0.006,
# 0.008, 0.008, 0.008, 0.059, 0.133, 0.154, 0.152, 0.155, 0.052, 0.027, 0.041, 0.072, 0.124, 0.008,
# 0.008, 0.008, 0.021, 0.047, 0.083, 0.092, 0.122, 0.126, 0.114, 0.146, 0.156, 0.061, 0.008, 0.008]

#syn23.w = [ 1.83606481, 1.03416515, 1.03180659, 1.03180002, 1.0318 , 1.0318 , 1.0318 , 1.0318 , 1.0318 , 1.0318 , 1.83276481, 1.03086515, 1.02850659, 1.04851821, 1.02855582, 1.02850016, 1.0285 , 1.06453128, 1.02860046, 1.02850028, 11.05633573, 1.10235201, 1.03613349, 1.09192227, 1.07798331, 1.00217427, 1.05076276, 1.09897228, 0.99728432, 1.07991354, 30.48572451, 1.18457116, 1.00412685, 1.17807888, 1.21994492, 1.05840517, 1.10503875, 1.01924334, 0.97211134, 1.19473062, 35.40088633, 1.2043063 , 0.98635986, 1.14620578, 1.14870716, 1.05230279, 1.14276333, 0.97208014, 1.15793419, 1.10130679, 31.11176877, 1.21226209, 1.00254198, 1.08092322, 1.04660394, 1.10258587, 1.05666484, 1.01884142, 1.19564282, 1.12289721, 25.25828602, 1.15916159, 0.99491419, 1.02606572, 1.11088126, 1.14388117, 1.02984138, 1.14496822, 1.09925877, 1.07760178, 22.32505366, 1.09565317, 0.97984497, 1.06643701, 1.11709559, 1.23214951, 1.05841272, 1.20109542, 1.02874465, 1.04340446, 21.45871203, 1.13613469, 0.99324185, 1.22055032, 1.0275903 , 1.18991297, 1.03626299, 1.18199802, 1.02374178, 1.06955113, 28.26973621, 1.13819713, 1.03782343, 1.27037951, 1.02289464, 1.04798382, 1.08366752, 1.19726139, 1.01782779, 1.0801844 , 41.32614477, 1.21945787, 0.9961476 , 1.18075172, 1.14753377, 0.96929198, 1.15514486, 1.13397995, 0.99750125, 1.07825459, 33.31947167, 1.20140452, 1.00933844, 1.0435108 , 1.18366155, 0.99633338, 1.06482975, 1.00640524, 1.01570052, 1.13554925, 6.24580223, 1.0377291 , 1.01296923, 1.02330612, 1.07047605, 1.01821702, 1.03253768, 1.01295475, 1.07197716, 1.06172787, 1.83546492, 1.03356516, 1.03120659, 1.03120002, 1.0312 , 1.0312 , 1.0312 , 1.0312 , 1.0400122 , 1.03122457]
# syn23.w = [ 2.4610545 ,  0.96442392,  0.96001233,  0.96000003,  0.96      ,
#         0.96      ,  0.96      ,  0.96      ,  0.96      ,  0.96      ,
#         2.45775451,  0.96112392,  0.95671233,  0.99420462,  0.9568045 ,
#         0.95670029,  0.9567    ,  1.02413535,  0.95688802,  0.95670052,
#         2.44341623,  1.12246671,  0.99849158,  1.10300731,  1.07683607,
#         0.93486663,  1.02586613,  1.11615422,  0.92573239,  1.08045927,
#         2.4809336 ,  1.3311174 ,  3.97964624,  5.25173671,  1.3973382 ,
#         1.09488645,  1.18216769,  1.0215924 ,  0.93328756,  1.35015112,
#         2.7231405 ,  1.38666027,  2.94390174,  3.22377851,  2.2594661 ,
#         1.10202284,  1.27144115,  3.95245409,  1.29981493,  1.1937833 ,
#         3.73397034,  1.39161621,  0.99894626,  1.14581161,  2.05830801,
#         1.18624263,  1.10030708,  4.0421651 ,  1.36049324,  1.22426876,
#         4.80715612,  1.29347321,  0.98599231,  1.04434383,  1.20309156,
#         1.26485523,  1.05131863,  5.23345938,  1.18130356,  2.16472346,
#         2.68854265,  1.17378566,  0.95697472,  1.11912971,  5.24772498,
#         1.42931735,  1.10401718,  1.3712783 ,  1.048433  ,  1.07594452,
#         3.56880205,  1.24485268,  4.05525279,  1.40314157,  4.07475582,
#         1.3455351 ,  1.05783601,  1.33079363,  1.03435028,  1.1201868 ,
#         4.47806055,  1.24531128,  7.17721659,  1.49309435,  1.02943089,
#         3.10635318,  1.14324162,  1.35598199,  1.01992329,  1.13670194,
#         5.44977541,  1.40061064,  4.02749465,  5.23993916,  1.26598077,
#         2.95621124,  1.28019658,  1.24064324,  0.98504621,  1.13622267,
#         5.52641604,  1.33992832,  1.99223299,  9.94557466,  1.30664225,
#         1.96192318,  1.08415693,  0.97477368,  1.99821249,  1.21654328,
#         2.5533615 ,  0.98761049,  0.94122968,  1.96665522,  1.04892279,
#         0.95106141,  0.97786763,  0.94120252,  1.05173981,  1.03255458,
#         2.46045463,  0.96382392,  0.95941233,  0.95940003,  0.9594    ,
#         0.9594    ,  0.9594    ,  0.9594    ,  0.97590988,  0.95944603]

syn23.w = [  2.3590545 ,   0.86242392,   0.85801233,   0.85800003,
         0.858     ,   0.858     ,   0.858     ,   0.858     ,
         0.858     ,   0.858     ,   2.34855451,   0.85192392,
         0.84751233,   0.97199505,   0.84784687,   0.84750097,
         0.85897657,   1.05601722,   0.84808135,   0.84750162,
         2.27657817,   1.25846391,   2.95109125,   1.48536013,
         1.29302677,   0.77861003,   1.05191355,   1.171587  ,
         0.75895362,   1.13314884,   2.51810387,   1.68634058,
         3.92092454,   8.48821864,   1.74388096,   0.98743969,
         1.45542745,   0.95904076,   0.86136412,   1.62548383,
         2.88674624,   1.79308112,   2.86174565,   5.1423984 ,
         2.37945214,   1.0783751 ,   1.42771059,   6.79961397,
         1.77300472,   1.37427103,   3.84593117,   1.70727956,
         0.94924034,   1.0876337 ,   2.12264929,   1.27821825,
         1.13128685,   9.01069496,   3.71886935,   2.47165207,
         6.02502386,   1.45118942,   0.93356543,   1.04053878,
         2.32977553,   1.42764288,   1.13921388,   6.48251384,
         2.25340416,   3.43250366,   3.92741139,   1.28372826,
         1.85957734,   1.33827486,   8.38892685,   1.77944384,
         1.19813151,   1.73485293,   1.00791661,   1.20574003,
         4.56054759,   1.3751164 ,   9.01150191,   1.81735154,
         8.13475667,   1.68148862,   1.01570562,   1.77508256,
         0.99947882,   1.27622541,   7.37299685,   1.56115102,
        17.02847388,   2.02177506,   1.06658234,   5.08700584,
         1.22701823,   1.7615557 ,   0.94893688,   1.29439361,
         8.30917888,   1.93094733,  19.76833681,  16.68119294,
         1.61553728,   4.8197953 ,   1.4827765 ,   1.36433598,
         0.87210374,   1.32773818,   6.4220258 ,   1.68398038,
         1.93545981,  21.99965491,   1.67787597,   3.82417704,
         1.18740793,   0.81051692,   1.93093031,   1.46842653,
         2.54116736,   0.90567353,   0.82432751,   1.84965549,
         0.98140112,   0.84262966,   0.87736268,   0.82424851,
         1.11921664,   0.93312784,   2.35815472,   0.86152392,
         0.85711233,   0.85710003,   0.8571    ,   0.8571    ,
         0.8571    ,   0.8571    ,   0.88452672,   0.85717647]

v_mon = getStateMonitor(P3rd)['voltage']
isyn_mon = getStateMonitor(P3rd)['current']
s_mon = getSpikeMonitor(P3rd)

run(DIGIT_DURATION*NumOfDigitsTest)

print "Test Error  : {0}".format(getError(s_mon, labels, 1))
figure(figsize=(6,4))
plot(s_mon.t/ms, s_mon.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
ylim([-1,len(P1st)+1])
tight_layout()

figure(figsize=(9, 9))
ax = axes()

ax2 = ax.twinx()
ax2.plot(isyn_mon.t / ms, isyn_mon.I[0], 'b', linewidth=3, alpha=.4)
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Synaptic Current')
tight_layout()
show()