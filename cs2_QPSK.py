import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
N = 1000000
b = np.random.randint(0, 2, N)
grouped_bits = [b[i:i+2] for i in range(0, len(b), 2)]
s = np.array([(2*i[0]-1) + 1j*(2*i[1]-1) for i in grouped_bits])
EbN0_dB = np.arange(-4, 9, 2)
BER = []
BER_th = []
for x in EbN0_dB:
    EbN0 = 10**(x/10)
    N0 = 1/EbN0
    n_r = (np.random.randn(len(s)) + 1j*np.random.randn(len(s))) * np.sqrt(N0/2)
    r = s + n_r
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
    b_hat = np.array(S, dtype=int).flatten()
    b_orig = np.array(b, dtype=int).flatten()
    errors = np.sum(b_hat != b_orig)
    ber = errors / N
    BER.append(ber)
    BER_th.append(0.5 * erfc(np.sqrt(EbN0)))
plt.semilogy(EbN0_dB, BER, 'o-', label='Simulated')
plt.semilogy(EbN0_dB, BER_th, '--', label='Theoretical')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('QPSK BER vs Eb/N0')
plt.grid(True, which='both')
plt.legend()
plt.show()
