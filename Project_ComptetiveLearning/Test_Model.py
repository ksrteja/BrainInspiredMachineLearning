from ProjectUtil import *
from CompetetiveLearning import *
from Constants import *
import numpy as np

# ------------------------layer 1 dynamics-------------------------#

data, labels = data_load_mnist(DIGITS)
data = (data.T / (data.T).sum(axis=0)).T

inarr = []
tarr = []

start = 0#data.shape[0] - 50
for index in range(start, start + NumOfDigitsTest):
    print "Label : {0}".format(labels[index - start])
    ret = np.array(np.nonzero(data[index - start].reshape(28, 28))).T
    indicesArray = np.array(ret[:, 0])
    timeArray = np.array(ret[:, 1]) + ((index - start) * DIGIT_DURATION / ms)
    inarr.extend(indicesArray)
    tarr.extend(timeArray)

P1st = SpikeGeneratorGroup(M, inarr, tarr * ms)

# ------------------------layer 2 dynamics-------------------------#

P2nd = NeuronGroup(N/ K_VALUE, CLEquations, threshold=threshold, reset=reset, refractory = refractory,
                   method = method)

# --------------------connecting layer 1 and layer 2-------------------#
syn12 = Synapses(P1st, P2nd, on_pre=Syn12Condition)
syn12.connect("i/K_VALUE == j")


# ------------------------layer 3/op dynamics-------------------------#


P3rd = NeuronGroup(NUM_OUTPUT_CLASSES, CLEquations, threshold=threshold, reset=reset, refractory = refractory,
                   method = method)

#turning off stdp - as it is test phase
apre = 0
apost=0

syn23 = Synapses(P2nd, P3rd, '''w : 1
                        dx/dt = -x / taupre  : 1 (event-driven)
                        dy/dt = -y / taupost : 1 (event-driven)''',
             on_pre='''isyn += w*amp
                        x += apre
                        w += y''',
             on_post='''y += apost
                        w += x-alpha*w''')


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
syn23.w =[ -5.83622827e-15,   1.52009121e-13,  -9.18692946e-15,
        -2.31497506e-13,  -1.01497544e-14,   3.19358454e-12,
         1.29945619e-10,   8.67888190e-13,  -4.16959120e-14,
         1.60964451e-13,   3.68630887e-11,   6.65672485e-12,
         3.93962186e-10,   2.48935763e-12,   1.13986861e-12,
         5.53393740e-11,   6.28129674e-10,   3.59436434e-12,
        -3.42338998e-14,   2.56671479e-13,   6.69855046e-10,
         6.77704122e-10,   7.34801150e-10,   5.34248918e-10,
         6.49049205e-10,   3.96171051e-10,   6.96637317e-10,
         2.60850781e-11,   6.97678023e-10,   1.74071945e-11,
         7.76201228e-10,   7.34906938e-10,   7.92218566e-10,
         7.93583529e-10,   7.30664450e-10,   7.84725966e-10,
         7.07946971e-10,   6.53994492e-10,   7.79460450e-10,
         7.51253627e-10,   7.92260716e-10,   7.40922855e-10,
         7.20064773e-10,   7.62727532e-10,   7.65912930e-10,
         7.31430126e-10,   7.08584262e-10,   8.23118059e-10,
         7.67453107e-10,   8.01905416e-10,   7.67823722e-10,
         7.26074418e-10,   7.06630557e-10,   7.52748329e-10,
         7.87771614e-10,   7.60162255e-10,   7.25394857e-10,
         8.08469193e-10,   7.84831730e-10,   7.80993414e-10,
         7.66247656e-10,   7.38541398e-10,   7.40424222e-10,
         7.51146156e-10,   7.87637739e-10,   8.00221676e-10,
         7.87349120e-10,   7.62955797e-10,   7.71501051e-10,
         7.92477768e-10,   7.57873099e-10,   7.36108605e-10,
         7.77643280e-10,   7.74184379e-10,   8.08794886e-10,
         7.56456855e-10,   7.93470975e-10,   7.45963655e-10,
         7.51910119e-10,   7.87194107e-10,   7.48375922e-10,
         7.37678187e-10,   7.97685795e-10,   7.42139562e-10,
         8.16715224e-10,   7.34273264e-10,   7.91279358e-10,
         7.28082222e-10,   7.54987898e-10,   7.13996542e-10,
         7.58334608e-10,   7.41081193e-10,   8.20355284e-10,
         7.48062951e-10,   7.43849705e-10,   7.55638298e-10,
         7.95149309e-10,   7.29783875e-10,   7.58372363e-10,
         6.89434308e-10,   7.79134915e-10,   7.37929265e-10,
         8.10008522e-10,   7.85118277e-10,   7.08599159e-10,
         7.74057388e-10,   7.62251499e-10,   7.25859740e-10,
         7.55823492e-10,   6.98652772e-10,   7.78223897e-10,
         7.33700180e-10,   4.61219643e-10,   7.73311495e-10,
         7.07423002e-10,   6.55005802e-10,   4.00455426e-10,
         7.10893315e-10,   7.60860420e-10,   6.95614517e-10,
         4.60848750e-10,   3.66132161e-10,   1.06791966e-11,
         3.35670882e-10,   1.79099574e-10,   3.08156475e-10,
         1.76067192e-11,   6.95697345e-10,   3.82687500e-10,
         6.81725234e-10,   1.88352335e-12,  -1.39284700e-13,
         3.26373084e-14,   3.07201297e-13,   1.13381804e-13,
         1.12426824e-14,   1.19325595e-11,   4.86424410e-10,
         8.20005986e-12,   2.93483458e-10]

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
ax2.plot(isyn_mon.t / ms, isyn_mon.isyn[0], 'b', linewidth=3, alpha=.4)
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Synaptic Current')
tight_layout()
show()