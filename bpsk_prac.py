import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
N=1_000_000
b=np.random.randint(0,2,N)
s=2*b-1
EbN0_dB=np.arange(-4,9,2)
BER=[];BER_th=[]
for x in EbN0_dB:
    EbN0=10**(x/10)
    N0=1/EbN0
    n=np.sqrt(N0/2)
    noise=n*np.random.randn(N)
    r=s+noise
    rx=(r>0).astype(int)
    error=np.sum(rx!=b)
    ber=error/N
    BER.append(ber)
    #theoritical
    BER_th.append(0.5*erfc(np.sqrt(EbN0)))
plt.semilogy(EbN0_dB,BER,'o-',label='Simulated')
plt.semilogy(EbN0_dB,BER_th,'--',label='Theoretical')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.title('BPSK BER vs Eb/N0')
plt.grid(True,which='both')
plt.legend()
plt.show()
