#!/usr/bin/env python

import scipy.io.wavfile as wav
import argparse
import transformer
import matplotlib.pyplot as plt
import numpy as np
import templates
import librosa

parser = argparse.ArgumentParser()
parser.add_argument("file", help="A WAV File, desireably containing some music")
parser.add_argument("-N", "--windowlength", help="Windowlength to use for the STFT [seconds]", type=float, default=0.2)
args = parser.parse_args()

samples, samplerate = librosa.core.load(args.file)
windowsize = args.windowlength*samplerate
hopsize = 0.5*windowsize

#trans = transformer.Transformer(4400, 2200, samplerate)
#stft = trans.stft(samples)
#gpec = trans.spectrogram(stft)

#trans.plotSpectrogram(spec)
#log = trans.logFrequencySpectrogram(spec)
#plt.imshow(np.transpose(log))
#plt.show()
#chromas = trans.chroma(log)
chromas = librosa.feature.chroma_stft(y=samples, sr=samplerate, n_fft=windowsize, hop_length=hopsize)
print(chromas.shape)
#plt.subplot(4, 2, 5)
librosa.display.specshow(chromas, y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')
plt.show()
#plt.imshow(chromas)
#plt.show()
