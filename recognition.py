import numpy as np
import librosa
import templates
import scipy

def openFile(filename):
    samples, samplerate = librosa.core.load(filename)
    #Drop empty start and end
    for i in range(0, len(samples)):
        if samples[i] > 0.1:
            dropBeginning = i
            break
    for i in range(len(samples)-1, -1, -1):
        if samples[i] > 0.1:
            dropEnd = i+1
            break
    return samples[dropBeginning:dropEnd], samplerate

def HPSS(samples):
    harm, perc = librosa.effects.hpss(samples)
    return harm, perc

def calculateChroma(samples, samplerate, windowsize, hopsize):
    chromas = librosa.feature.chroma_stft(y=samples, sr=samplerate, n_fft=windowsize, hop_length=hopsize, tuning=librosa.core.estimate_tuning(y=samples, sr=samplerate))
    return chromas

def calculateSimilarities(chromas, templates_to_use="bin"):
    if(templates_to_use=="bin"):
        temps, labels = templates.binary()
    elif(templates_to_use=="exp"):
        temps, labels = templates.harmonics()
    else:
        temps, labels = templates.triangle()

    chords = recognition(temps, np.transpose(chromas))
    return chords, temps, labels
    #simple_text_output(chords,labels)

#windowsize and hopsize in seconds
def identifyMostProbableChordSequence(chords, labels, windowsize, hopsize):
    seq = []
    print(len(chords))
    for i in chords:
        seq.append(np.argmax(i))
    print(len(seq))
    seq = np.array(seq)
    print(len(seq)*hopsize)
    chordSequence = fusedChordSequence(seq, labels, windowsize, hopsize)
    return chordSequence


def similarity(vec1, vec2):
    return np.inner(vec1, vec2)/(np.linalg.norm(vec1) *  np.linalg.norm(vec2))

def recognition(templates, features):
    ret = np.zeros((features.shape[0], templates.shape[0]))
    for i in range(features.shape[0]):
        for j in range(templates.shape[0]):
            test = similarity(features[i], templates[j])
            ret[i][j]  = test
            #print(similarity(features[i], templates[j]))
    return ret

# Convert framewise chord sequence into sequence of chord labels (with start and endtime) where same sucessive chords get fused into one
def fusedChordSequence(chords, chordNames, windowlength, hopsizeInSeconds):
    ret = []
    startTime = 0.0
    duration = hopsizeInSeconds
    currentChord = chords[0]
    for i in range(1, len(chords)):
        if chords[i] != currentChord:
            ret.append((chordNames[currentChord%24], startTime, startTime+duration))
            startTime = startTime + duration
            duration = hopsizeInSeconds
            currentChord = chords[i]
        else:
            duration += hopsizeInSeconds
    # Append last chord
    ret.append((chordNames[currentChord%24], startTime, startTime+duration+(windowlength-hopsizeInSeconds)))
    return ret
