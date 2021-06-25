#
# 波形を読み込んでまた元に戻すテスト
#pathとresult_pathを指定してください。
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

path = "D:/Waves/a.wav"
result_path = "D:/Waves/result.wav"
fname = "a"
nfft=1024
pcount = 0

fig = plt.figure()
fx = add_subplot()
#波形表示
fs, a = wavefile.read_wav(path)
fx.plot(a)
plt.title("Source : " + fname)

#短時間フーリエ変換(スペクトログラム)表示
f, t, aspec = signal.stft(a, fs,window=('hamming'),nperseg=nfft,padded=False) 
print(aspec.shape)
fx = add_subplot()
m = fx.pcolormesh(t, f, np.log(np.abs(aspec)) * 10)
plt.ylabel('Hz')
plt.xlabel('s')
cbar = plt.colorbar(m)
cbar.ax.set_ylabel("dB")
plt.title("Spec")

# 平均のパワースペクトル
fx = add_subplot()
plt.plot(f,np.log(np.abs(np.mean(aspec,axis=1)))*10,label='linear')
plt.title("mean-power")

# 平均のCep
fx = add_subplot()
plt.plot(f,ifft(np.log(np.mean(aspec,axis=1))),label='linear')
plt.title("mean-cep")

# 再生成(元に戻してるだけ:テスト)
x = fft(np.log(np.mean(aspec,axis=1))) #複素数のまま流す
ans = np.exp(ifft(x))
fx = add_subplot()
fx.plot(f,np.log(np.abs(ans))*10,label='linear')
print((ans).size)
anspec = np.repeat(ans[:, None], aspec.shape[1], axis=1)
print(anspec.shape)
plt.title("mean-UNC")
fx = add_subplot()
m = fx.pcolormesh(t, f, np.log(np.abs(anspec)) * 10)
plt.ylabel('Hz')
plt.xlabel('s')
cbar = plt.colorbar(m)
cbar.ax.set_ylabel("dB")
plt.title("Spec")
#fx = add_subplot() 何日か後に見直した時誤解しそうなのであえて非表示

#fx.plot(result)
#plt.title("Result(Source->sftf): " + fname)

fig.tight_layout()
plt.show()

t,result = signal.istft(aspec, fs,window=('hamming'),nperseg=nfft)
wavefile.write_wav(result_path,fs,result)
