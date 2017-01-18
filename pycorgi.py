#!/usr/bin/env python3.6

import scipy.io.wavfile as wav
import argparse
import templates

parser = argparse.ArgumentParser()
parser.add_argument("file", help="A WAV File, desireably containing some music")
parser.add_argument("-N", "--windowlength", help="Windowlength to use for the STFT [seconds]", type=float, default=0.2)
args = parser.parse_args()

samplerate,samples = wav.read(args.file)
windowsize = args.windowlength*samplerate
hopsize = 0.5*windowsize

print(samples.size)
print(samplerate)
print(samples.size/samplerate)
