#!/usr/bin/env python

#math stuff
import scipy.io.wavfile as wav
import numpy as np
import librosa

#program stuff
import argparse
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

#only debug
import matplotlib.pyplot as plt

#local imports
import transformer
import templates
import recognition
import synthesizer


"""
Simple output of chords
may be moved sometime
"""
def simple_text_output(chords, labels):
    for i in range(chords.shape[0]):
        print("{a:8.2f}: {b}".format(a=i*0.5*args.windowlength, b=labels[np.argmax(chords[i])]))


parser = argparse.ArgumentParser()
parser.add_argument("file", help="A WAV File, desireably containing some music")
parser.add_argument("-N", "--windowlength", help="Windowlength to use for the STFT [seconds]", type=float, default=0.2)
args = parser.parse_args()

samples, samplerate = librosa.core.load(args.file)
windowsize = args.windowlength*samplerate
hopsize = 0.5*windowsize

chromas = 0 #initialise variable
use_HPSS = False
if(use_HPSS):
    """
    Not ideal => does hpss then transforms back into audio time series
    """
    harm, perc = librosa.effects.hpss(samples)
    chromas = librosa.feature.chroma_stft(y=harm, sr=samplerate, n_fft=windowsize, hop_length=hopsize, tuning=librosa.core.estimate_tuning(y=samples, sr=samplerate))

else:
    chromas = librosa.feature.chroma_stft(y=samples, sr=samplerate, n_fft=windowsize, hop_length=hopsize, tuning=librosa.core.estimate_tuning(y=samples, sr=samplerate))


temps = 0
labels = 0
use_harmonics = False
if(use_harmonics):
    temps, labels = templates.harmonics_norm()
else:
    temps, labels = templates.binary()

chords = recognition.recognition(temps, np.transpose(chromas))

simple_text_output(chords,labels)

"""
Get the recognized chord and synthesize it
"""

synthwav = None
for c in chords:
    chord = np.argmax(c)
    synth = synthesizer.synthesize_chord(chord, samplerate/2, int((samplerate/2)*args.windowlength))
    
    if synthwav is None:
      synthwav = synth
    else:
      synthwav = np.concatenate((synthwav, synth))

synthwav = np.delete(synthwav, np.s_[len(samples)::], axis=0)

##Write to output.wav
m = np.matrix([synthwav / np.linalg.norm(synthwav), samples])

librosa.output.write_wav(path='output.wav', y=m, sr=samplerate, norm=False)

#example of how to plot
#plt.subplot(4, 2, 5)
#librosa.display.specshow(chromas, y_axis='chroma')
#plt.colorbar()
#plt.title('Chromagram')
#plt.show()
