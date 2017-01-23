import math
import librosa
import numpy as np

def synthesize_chord(chordIndex, samplerate, samples):
    #print(samplerate)
    #print(samples)
    #chordIndex 0: CMajor, chordIndex 12: CMinor
    chord = 73 + (chordIndex % 12)
  
    FREQUENCY1 = math.pow(2, ((chord-69)/12.0))*440;
    FREQUENCY2 = 0.0
    FREQUENCY3 = math.pow(2, ((chord+7-69)/12.0))*440;
  
    ##major chord
    if chordIndex < 12:
        FREQUENCY2 = math.pow(2, ((chord+4-69)/12.0))*440;
    ##minor chord
    else:
        FREQUENCY2 = math.pow(2, ((chord+3-69)/12.0))*440;

    if FREQUENCY1 > samplerate:
        samplerate = FREQUENCY1+100

    # samplerate = samples -> 1 sekunde
    # samplerate = 0.5 samples -> 2 sekunden
    #print(samples/samplerate)
    t = np.linspace(0.0, samples/samplerate, num=samples)
    #print(t)
    wave1 = np.sin(2*np.pi*t*FREQUENCY1)
    wave2 = np.sin(2*np.pi*t*FREQUENCY2)
    wave3 = np.sin(2*np.pi*t*FREQUENCY3)
    return wave1+wave2+wave3
