import wave
import numpy as np
from scipy.io.wavfile import write
def normalize(w):
    w_max = np.max(w)
    w_min = np.min(w)
    return (w - w_min) / (w_max - w_min)

def read_wav(path):
    print("ファイルチェックはしません。読み込めるファイルについてはReadme.mdを参照してください。")
    w = wave.open(path, "r" )
    buf = w.readframes(w.getnframes())
    return w.getnframes(), np.frombuffer(buf, dtype="int16")

def write_wav(path,fs,wav):
    data  = normalize(wav)*2 - 1
    data = np.array([data * 32767.0],dtype = "int16")[0]
    write(path, fs, data)