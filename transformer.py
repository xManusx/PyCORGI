import scipy
import numpy as np
import math
import matplotlib.pyplot as plt

class Transformer:
    def __init__(self, frameSize, hopSize, samplingRate, tuning=440):
        self.frameSize = frameSize
        self.hopSize = hopSize
        self.samplingRate = samplingRate
        # A4 frequency in Hz
        self.tuning = tuning

    # Calculates STFT using a Hann window
    # frameSize and hopSize must be specified in samples
    # Last frame gets dropped, if its sa
    def stft(self, x):
        trans = []
        window = np.hanning(self.frameSize)
        for i in range(0, len(x), self.hopSize):
            # Last frame to short
            if i+self.frameSize > len(x):
                break 
            trans.append(np.fft.rfft(window*x[i:i+self.frameSize]))
        return np.array(trans)

    # Calculates spectrogram of STFT
    def spectrogram(self, x):
        spec = []
        for i in x:
            spec.append(np.power(np.abs(i), 2))
        return np.array(spec)

    # Calculates log-frequency spectrogram out of spectrogram
    def logFrequencySpectrogram(self, x):
        logFreq = np.empty((len(x), 128))
        freqs = np.arange(0.0, len(x[0]), 1.0) * self.samplingRate/self.frameSize
        f_pitch = lambda p: math.pow(2, (p-69)/12)*self.tuning
        for p in range(0, 128):
            p_min = f_pitch(p-0.5)
            p_max = f_pitch(p+0.5)
            mask = np.logical_and(p_min <= freqs, freqs < p_max)
            logFreq[:,p] = np.sum(x[:,mask], axis=1)
        return logFreq

    # Calculates chroma features out of log-frequency spectrogram
    def chroma(self, x):
        chromas = np.empty((len(x), 12))
        for i in range(0, 12):
            chromas[:,i] = np.sum(x[:, i::12], axis=1)
        return chromas

    # Plots spectrogram
    def plotSpectrogram(self, x, compRate=10):
        t_max = (len(x)-1)*self.hopSize/self.samplingRate
        freq_max = (len(x[0])-1)*self.samplingRate/self.frameSize
        plt.imshow(np.transpose(np.log(1+compRate*x)), cmap=plt.cm.Reds, extent=[0.0, t_max, 0, freq_max], aspect='auto', origin='lower')
        plt.colorbar()
        plt.show()
