#!/usr/bin/env python

import librosa
import matplotlib.pyplot as plt

samples, samplerate = librosa.core.load('output.wav', mono=False)
print(samples.shape)
chromas1 = librosa.feature.chroma_stft(y=samples[0,:], sr=samplerate)
chromas2 = librosa.feature.chroma_stft(y=samples[1,:], sr=samplerate)

#example of how to plot
plt.subplot(2, 1, 1)
librosa.display.specshow(chromas2, y_axis='chroma')
plt.colorbar()
plt.title('Chromagram (Input)')


plt.subplot(2, 1, 2)
librosa.display.specshow(chromas1, y_axis='chroma')
plt.colorbar()
plt.title('Chromagram (Synth)')
plt.show()
