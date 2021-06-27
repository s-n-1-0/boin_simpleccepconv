#
# 変換処理(時間がなかったためstftを使っていない(=サイズが大きい波形を生成できない))
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

def fft2ccep(sp):
    def _ang2unang(ang):#アンラップ処理
        n = ang.shape[-1]
        ren = np.arange(n)
        unang = np.unwrap(ang)
        fsize = (n + 1) // 2
        d = np.array(np.round(unang[..., fsize] / np.pi)) #ずれ特定
        unang -= np.pi * d[..., None] * ren / fsize
        return unang, d
    global nfft
    unang, d = _ang2unang(np.angle(sp))
    sp = np.log(np.abs(sp)) + 1j * unang #j=虚数単位
    return ifft(sp).real, d
def ccep2fft(ccep,d):
    def _unang2ang(unang, d):
        n = unang.shape[-1]
        ren = np.arange(n)
        fsize = (n + 1) // 2
        return unang + np.pi * d[..., None] * ren / fsize 
    global nfft
    sp = fft(ccep,n=nfft)
    return np.exp(sp.real + 1j * _unang2ang(sp.imag, d))
def cutplot(ccep,name):
    global fs
    global nfft
    global plot_qi
    fx = add_subplot()
    ax = np.copy(ccep)
    ax[plot_qi:-plot_qi] = 0
    ax = np.abs(ccep2fft(ax,d))
    plt.plot(np.linspace(0, fs, nfft)[:int(nfft/2)],ax[:int(nfft/2)],label='linear')
    plt.title(name + "-cep2fft-cut")
    plt.xlim([0,2500])

a_path = "D:/Waves/a.wav"
b_path = "D:/Waves/e.wav"
result_path = "D:/Waves/result.wav"
fname = "a"
nfft=1024 *2 * 2
pcount = 0

fig = plt.figure()
fs, a = wavefile.read_wav(a_path)
_ , b = wavefile.read_wav(b_path)
a = a[:nfft]
b = b[:nfft]
a = np.hamming(nfft) * a
b = np.hamming(nfft) * b
aspec = fft(a,n=nfft)
bspec = fft(b,n=nfft)

# Cep
que = np.linspace(0, len(a) / fs, len(a)) * 1000
qi = 40
plot_qi = min((i for i in range(len(que)) if que[i] > 10.0), default=-1)
ac, _ = fft2ccep(aspec)
bc, d = fft2ccep(bspec)
fx = add_subplot()
plt.plot(que[1:plot_qi],ac[1:plot_qi],label='linear')
plt.title("a-cep")
cutplot(ac,"a")
fx = add_subplot()
plt.plot(que[1:plot_qi],bc[1:plot_qi],label='linear')
plt.title("b-cep")
cutplot(bc,"b")
result = ac[0:qi]
result = np.concatenate([result,bc[qi:-qi],ac[-qi:]])

fx = add_subplot()
plt.plot(que[:len(result)],result,label='linear')
plt.title("merge-cep")
result = ifft(ccep2fft(result,d),n = nfft)

result *=  1/np.hamming(nfft)

fx = add_subplot()
plt.plot(result,label='linear')
plt.title("re")
fig.tight_layout()
plt.show()

wavefile.write_wav(result_path,fs,result)
