import numpy as np

"""
All templates returned are 24x11 matrices
ret[0] corresponds to C,  ret[1] to C#
ret[12] corresponds to Cm,  ret[13] to C#m

ret[0][0] corresponds to the energy of the C band
in a C major chord
"""

def std_chords(flat=False):
    chords = 0
    if(flat):
        chords = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    else:
        chords = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    chordsm = [x + "m" for x in chords]
    chords.extend(chordsm)
    return chords


"""
Returns binary templates
"""
def binary(flat=False):
    ret = np.zeros((24, 12))
    ret[0][0] = 1
    ret[0][4] = 1
    ret[0][7] = 1
    ret[12][0] = 1
    ret[12][3] = 1
    ret[12][7] = 1

    for i in range(1,  12):
        ret[i] = np.roll(ret[0],  i)
        ret[i+12] = np.roll(ret[12],  i)

    return ret, std_chords(flat)


"""
Returns templates using some (whacky) assumptions about harmonics
"""
def harmonics(alpha = 0.8, flat=False):
    tone = np.zeros((12))
    tone[0] = 1+alpha+pow(alpha,  3)+pow(alpha, 7)
    tone[4] = pow(alpha, 4)
    tone[7] = pow(alpha, 2) + pow(alpha, 5)
    tone[10] = pow(alpha, 6)

    ret = np.zeros((24, 12))
    ret[0] = tone + np.roll(tone, 4) + np.roll(tone, 7)
    ret[12] = tone + np.roll(tone, 3) + np.roll(tone, 7)

    for i in range(1,  12):
        ret[i] = np.roll(ret[0],  i)
        ret[i+12] = np.roll(ret[12],  i)

    return ret, std_chords(flat)

"""
Returns templates using some (whacky) assumptions about harmonics
Entries for each chord are normalised to 1
"""
def harmonics_norm(alpha = 0.8, flat=False):
    tone = np.zeros((12))
    tone[0] = 1+alpha+pow(alpha, 3)+pow(alpha, 7)
    tone[4] = pow(alpha, 4)
    tone[7] = (pow(alpha, 2) + pow(alpha, 5))
    tone[10] = pow(alpha, 6)

    ret = np.zeros((24, 12))
    ret[0] = tone + np.roll(tone, 4) + np.roll(tone, 7)
    ret[0] /= np.amax(ret[0])

    ret[12] = tone + np.roll(tone, 3) + np.roll(tone, 7)
    ret[12] /= np.amax(ret[12])

    for i in range(1,  12):
        ret[i] = np.roll(ret[0],  i)
        ret[i+12] = np.roll(ret[12],  i)

    return ret, std_chords(flat)
