#
# 変換処理(時間がなかったためstftを使っていない(=サイズが大きいデータは扱えないはず))
# a_pathとb_pathとresult_pathを指定してください。
#

from lib import wavefile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
def add_subplot():
    global pcount
    global fig
    pcount += 1
    return fig.add_subplot(3,2,pcount)

def fft2ccep(w):
    global nfft
    return ifft(np.log(w),n=nfft)
def ccep2fft(ccep):
    return np.exp(fft(ccep,n=nfft))
a_path = "D:/Waves/e.wav"
b_path = "D:/Waves/e.wav"
result_path = "D:/Waves/result.wav"
fname = "a"
nfft=1024 *2*2
pcount = 0

fig = plt.figure()
fs, a = wavefile.read_wav(a_path)
_ , b = wavefile.read_wav(b_path)
aspec = fft(a,n=nfft)
bspec = fft(b,n=nfft)

# Cep
fx = add_subplot()
que = np.linspace(0, len(a) / fs, len(a)) * 1000
m = fft2ccep(aspec)
    #m = np.concatenate([m ,m[::-1]])
plt.plot(que[1:int(nfft/2)],m[1:int(nfft/2)],label='linear')
plt.title("a-cep")

result = ifft(ccep2fft(m),n=nfft)
fx = add_subplot()
plt.plot(result,label='linear')
plt.title("re")
fig.tight_layout()
plt.show()

wavefile.write_wav(result_path,fs,result)
