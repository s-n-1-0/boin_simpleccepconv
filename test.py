from lib import wavefile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
def add_subplot():
    global pcount
    global fig
    pcount += 1
    return fig.add_subplot(2,2,pcount)

path = "D:/Waves/a.wav"
fname = "a"
fs = 22050
nfft=1024
pcount = 0

fig = plt.figure()
fx = add_subplot()
#波形表示
a = wavefile.load_wav(path)
fx.plot(a)
plt.title("Source : " + fname)

#短時間フーリエ変換(スペクトログラム)表示
f, t, aspec = signal.stft(a, fs,window=('hamming'),nfft=nfft) 
fx = add_subplot()
m = fx.pcolormesh(t, f, np.log(np.abs(aspec)) * 10)
plt.ylabel('Hz')
plt.xlabel('s')
cbar = plt.colorbar(m)
cbar.ax.set_ylabel("dB")
plt.title("Spec")

# index50番目のパワースペクトル
pidx = 50
fx = add_subplot()
plt.plot(f,np.log(np.abs(aspec[:,pidx])),label='linear')
plt.title("time" + "{:.2f}".format(t[pidx]) + "(i:" + str(pidx) +")")

# 再生成(元に戻してるだけ:テスト)
x = fft(np.log(aspec[:,pidx])) #複素数のまま流す
ans = np.exp(ifft(x))
fx = add_subplot()
fx.plot(f,np.log(np.abs(ans))*10,label='linear')
plt.title("UNC")
fig.tight_layout()
plt.show()


