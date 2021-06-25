from lib import wavefile

import matplotlib.pyplot as plt

#%%
# -*- coding: utf-8 -*-
fs = 22050
nfft=1024
a = wavefile.load_wav("D:/Waves/a.wav" )
plt.plot(a)
plt.grid()
plt.show()
exit()
