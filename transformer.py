import scipy
import numpy as np
import math
import matplotlib.pyplot as plt

class Transformer:
    def __init__(self, frameSize, hopSize, samplingRate):
        self.frameSize = frameSize
        self.hopSize = hopSize
        self.samplingRate = samplingRate

    # Calculates STFT using a Hann window
    # frameSize and hopSize must be specified in samples
    # Last frame gets dropped, if its sa
    def stft(self, x):
        trans = []
        window = np.hanning(self.frameSize)
        for i in range(0, len(x), self.hopSize):
            # Last frame to short
            if i+self.framSize > len(x):
                break 
            trans.append(np.fft.rfft(window*x[i:i+self.frameSize]))
        return np.array(trans)

    # Calculates spectrogram of STFT
    def spectrogram(self, x):
        spec = []
        for i in x:
            spec.append(np.power(np.abs(i), 2))
        return np.array(spec)

    # Plots spectrogram
    def plotSpectrogram(self, x, compRate=10):
        t_max = (len(x)-1)*self.hopSize/self.samplingRate
        freq_max = (len(x[0])-1)*self.samplingRate/self.frameSize
        plt.imshow(np.transpose(np.log(1+compRate*x)), cmap=plt.cm.Reds, extent=[0.0, t_max, 0, freq_max], aspect='auto', origin='lower')
        plt.colorbar()
        plt.show()
