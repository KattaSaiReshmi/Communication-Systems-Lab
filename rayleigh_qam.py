import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
N = 10**6
EbN0_dB = np.arange(4, 14, 2)
SER_sim = []
SER_theory = []
BER_sim=[]
BER_theory=[]
E0 = 1 / (2 * 5)
sqrt_E0 = np.sqrt(E0) 
bits = np.random.randint(0, 2, N)
bit_groups = bits.reshape(-1, 4)
gray_map = {
    (0, 0): -3,
    (0, 1): -1,
    (1, 1):  1,
    (1, 0):  3
}
inverse_gray_map = {
    0: (0, 0),
    1: (0, 1),
    2: (1, 0),
    3: (1, 1)
}
def bits_to_symbol(bits4):
    I_bits = tuple(bits4[:2])
    Q_bits = tuple(bits4[2:])
    I = gray_map[I_bits]
    Q = gray_map[Q_bits]
    return (I + 1j * Q) * sqrt_E0
def detect_symbol(y):
    y = y * np.sqrt(10)
    I_real = np.real(y)
    if I_real < -2:
        I_hat = 0
    elif I_real < 0:
        I_hat = 1
    elif I_real < 2:
        I_hat = 3
    else:
        I_hat = 2

    Q_imag = np.imag(y)
    if Q_imag < -2:
        Q_hat = 0
    elif Q_imag < 0:
        Q_hat = 1
    elif Q_imag < 2:
        Q_hat = 3
    else:
        Q_hat = 2
    
    return I_hat, Q_hat

symbols = np.array([bits_to_symbol(b) for b in bit_groups])

for EbN0 in EbN0_dB:
    EbN0_linear = 10**(EbN0 / 10)
    EsN0_linear = EbN0_linear * 4 
    noise_std = np.sqrt(1 / (2 * EsN0_linear))
    n = noise_std * (np.random.randn(len(symbols)) + 1j * np.random.randn(len(symbols)))
    h=(1/np.sqrt(2))*((np.random.randn(len(bit_groups)))+(1j*np.random.randn(len(bit_groups))))
    abs_h=np.abs(h)
    y = (abs_h*symbols) + n

    detected_bits = []
    for s in y:
        I_hat, Q_hat = detect_symbol(s)
        I_bits = inverse_gray_map[I_hat]
        Q_bits = inverse_gray_map[Q_hat]
        detected_bits.extend(I_bits + Q_bits)
        
    detected_bits = np.array(detected_bits)
    symbol_errors = np.any(bit_groups != detected_bits.reshape(-1, 4), axis=1)
    SER = np.sum(symbol_errors) / len(symbol_errors)
    SER_sim.append(SER)
    SER_theory.append(1.5*(1-(np.sqrt((0.2*EsN0_linear)/((0.2*EsN0_linear)+2)))))
BER_sim = np.array(SER_sim) / 4
BER_theory = np.array(SER_theory)/4
plt.figure(figsize=(8, 6))
plt.semilogy(EbN0_dB, BER_sim, 'o-', label='Simulated BER')
plt.semilogy(EbN0_dB, BER_theory, 's--', label='Theoretical BER')
plt.grid(True, which='both')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Symbol Error Rate (BER)')
plt.title(' RAYLEIGH 16-QAM BER vs Eb/N0')
plt.legend()
plt.tight_layout()
plt.show()
