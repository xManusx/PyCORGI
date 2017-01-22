#!/usr/bin/env python

import math
import librosa
import numpy as np

def synthesize_chord(chordIndex, samplerate, numberOfFrames):
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
      BITRATE = FREQUENCY1+100

  #RESTFRAMES = NUMBEROFFRAMES % BITRATE
  WAVEDATA = []

  for x in range(numberOfFrames):
      WAVEDATA.append(int(math.sin(x/((samplerate/FREQUENCY1)/math.pi))*127+128)+int(math.sin(x/((samplerate/FREQUENCY2)/math.pi))*127+128) + int(math.sin(x/((samplerate/FREQUENCY3)/math.pi))*127+128))    

  #for x in range(RESTFRAMES): 
      #WAVEDATA.append(128)
      
  return np.array(WAVEDATA)