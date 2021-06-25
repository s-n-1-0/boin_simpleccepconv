import wave
import numpy as np

def load_wav(path):
    print("ファイルチェックはしません。読み込めるファイルについてはReadme.mdを参照してください。")
    w = wave.open(path, "r" )
    buf = w.readframes(w.getnframes())
    return np.frombuffer(buf, dtype="int16")