import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
N = 1000000
b = np.random.randint(0, 2, N)
grouped_bits = []
for i in range(0, len(b), 2):
	grouped_bits.append(b[i:i+2] )
s = np.array([(2*i[0]-1)+ 1j*(2*i[1]-1) for i in grouped_bits])
EbN0_dB = np.arange(-4, 9, 2)
BER = []
BER_th = []
for x in EbN0_dB:
    EbN0 = 10**(x/10)
    h=(1/np.sqrt(2))*((np.random.randn(len(s)))+(1j*np.random.randn(len(s))))
    abs_h=np.abs(h)
    N0 = 1/EbN0
    n_r = (np.random.randn(len(s)) + 1j*np.random.randn(len(s))) * np.sqrt(N0/2)
    r = (abs_h*s) + n_r
    S = []
    for j in r:
        if np.real(j) > 0 and np.imag(j) > 0:
            S.append([1, 1])
        elif np.real(j) > 0 and np.imag(j) < 0:
            S.append([1, 0])
        elif np.real(j) < 0 and np.imag(j) > 0:
            S.append([0, 1])
        else:
            S.append([0, 0])
    b_r= np.array(S, dtype=int).flatten()
    b_o = np.array(b, dtype=int).flatten()
    errors = np.sum(b_r != b_o)
    ber = errors / N
    BER.append(ber)
    BER_th.append(0.5*(1-np.sqrt(EbN0/(1+EbN0))))
plt.semilogy(EbN0_dB, BER, 'o-', label='Simulated')
plt.semilogy(EbN0_dB, BER_th, '--', label='Theoretical')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('RAYLEIGH-QPSK BER vs Eb/N0')
plt.grid(True, which='both')
plt.legend()
plt.show()

