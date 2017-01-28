#!/usr/bin/env python

#math stuff
#import scipy.io.wavfile as wav
#import librosa

#program stuff
#import argparse
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

#only debug
#import matplotlib.pyplot as plt

import ui

ui = ui.UI()

"""
Simple output of chords
may be moved sometime
"""
#def simple_text_output(chords, labels):
#    for i in range(chords.shape[0]):
#        print("{a:8.2f}: {b}".format(a=i*0.5*args.windowlength, b=labels[np.argmax(chords[i])]))

#parser = argparse.ArgumentParser()
#parser.add_argument("-o", "--output", help="Turns commando line output on", action="store_true")
#parser.add_argument("file", help="A WAV File, desireably containing some music")
#parser.add_argument("-N", "--windowlength", help="Windowlength to use for the STFT [seconds]", type=float, default=0.2)
#args = parser.parse_args()

#example of how to plot
#plt.subplot(4, 2, 5)
#librosa.display.specshow(chromas, y_axis='chroma')
#plt.colorbar()
#plt.title('Chromagram')
#plt.show()
