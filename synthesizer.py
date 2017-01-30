import math
import librosa
import numpy as np
import scipy.io.wavfile

def synthChord(chordSequenceEntry,labels,samplerate):
    
    chordIndex = labels.index(chordSequenceEntry[0])

    chord = 72 + (chordIndex % 12)
  
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

    #print(samples/samplerate)
    duration = chordSequenceEntry[2]-chordSequenceEntry[1]
    t = np.linspace(0.0, duration, num=duration*samplerate)
    wave1 = np.sin(2*np.pi*t*FREQUENCY1)
    wave2 = np.sin(2*np.pi*t*FREQUENCY2)
    wave3 = np.sin(2*np.pi*t*FREQUENCY3)
    return np.array(wave1+wave2+wave3, dtype='f')


def synthChords(chordSequence, labels, samples, samplerate):
    """
    #Get the recognized chord and synthesize it
    #"""
    synthwav = None
    for c in chordSequence:
        synth = synthChord(c, labels, samplerate)
        if synthwav is None:
          synthwav = synth
        else:
          synthwav = np.concatenate((synthwav, synth))

    if len(synthwav) > len(samples):
      synthwav = np.delete(synthwav, np.s_[len(samples)::], axis=0)
    else:
      samples = np.delete(samples, np.s_[len(synthwav)::], axis=0)
    
    ###Write to output.wav
    m = np.matrix([100*synthwav / np.linalg.norm(synthwav), samples])
    librosa.output.write_wav(path='output.wav', y=m, sr=samplerate, norm=False)
