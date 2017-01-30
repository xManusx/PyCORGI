import sys
import os
from PyQt4.QtGui import *
from PyQt4 import QtCore
import math
import matplotlib.pyplot as plt
import random
import recognition
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import transformer
import synthesizer
import csv

class UI:
    def __init__(self):
        self.width = 700
        self.height = 500
        self.label1height = math.ceil(self.height/4)
        self.label2height = math.ceil(self.height/8)
        self.label1width = self.width
        self.label2width = self.width

        # Init basic window
        self.app = QApplication(sys.argv)
        self.w = QWidget()
        self.w.resize(self.width, self.height)
        self.w.setFixedSize(self.width, self.height)
        self.w.setWindowTitle("PyCorgi")

        # Recognize button
        self.recognize_button = QPushButton("Recognize", self.w)
        self.recognize_button.resize(self.recognize_button.sizeHint())
        self.recognize_button.move(self.width-100, self.height-50)
        self.recognize_button.clicked.connect(self.recognize)

        #Info text field
        self.infobox = QLabel(" ", self.w)
        self.infobox.setFixedWidth(280)
        self.infobox.move(self.width-400, self.height - 45)
        self.infobox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.infobox.repaint()
        self.infobox.repaint()

        # Picture printer
        self.label1 = QLabel(self.w)
        self.label1.setFixedWidth(self.width)
        self.label1.setFixedHeight(self.label1height)
        self.label2 = QLabel(self.w)
        self.label2.setFixedWidth(self.width)
        self.label2.setFixedHeight(self.label2height)
        self.label2.move(0, self.label1height+2)
        self.label3 = QLabel(self.w)
        self.label3.setFixedWidth(self.width)
        self.label3.setFixedHeight(self.label2height)
        self.label3.move(0, self.label1height+self.label2height+4)

        ## Textboxes
        # filepath
        self.filepath = QLineEdit("audio/Dm_DI.wav",self.w)
        self.filepath.move(10, self.height-48)
        # groundTruth path
        self.groundTruth = QLineEdit("groundTruths/Dm_DI.csv", self.w)
        self.groundTruth.move(150, self.height-48)
       
        # windowsize
        self.windowsize = QLineEdit("0.2", self.w)
        self.windowsize.move(10, self.height-170)
        self.windowsize.setFixedWidth(50)
        #hopsize
        self.hopsize = QLineEdit("0.5", self.w)
        self.hopsize.move(10, self.height-150)
        self.hopsize.setFixedWidth(50)
        # compressionRate
        self.comprate = QLineEdit("10", self.w)
        self.comprate.move(650, self.height - 170)
        self.comprate.setFixedWidth(40)
        # prefilter length
        self.filterL = QLineEdit("10", self.w)
        self.filterL.move(650, self.height - 150)
        self.filterL.setFixedWidth(40)

        
        ## Labels for Textboxes
        self.windowsizeLabel = QLabel("Window Size (seconds)", self.w)
        self.windowsizeLabel.move(self.windowsize.x()+ self.windowsize.width() + 5, self.windowsize.y())
        self.hopsizeLabel = QLabel("Hop Size (fractions of Window Size)", self.w)
        self.hopsizeLabel.move(self.hopsize.x()+ self.hopsize.width() + 5, self.hopsize.y())

        #Checkbox
        #Use hpss
        self.hpss = QCheckBox("Use HPSS", self.w)
        self.hpss.setChecked(True)
        self.hpss.move(300, self.height - 170)
        #Print output
        self.output = QCheckBox("Console output", self.w)
        self.output.setChecked(False)
        self.output.move(300, self.height - 150)
        #Synthesize chords
        self.synth = QCheckBox("Synthesize Chords", self.w)
        self.synth.setChecked(False)
        self.synth.move(300, self.height - 130)       
        #Use own chromas
        self.chromas = QCheckBox("Use libRosa", self.w)
        self.chromas.setChecked(True)
        self.chromas.move(300, self.height - 110)
        #Use log compression
        self.logComp = QCheckBox("Use log compression", self.w)
        self.logComp.setChecked(True)
        self.logComp.move(500, self.height - 170)
        #Use prefiltering
        self.prefiltering = QCheckBox("Use prefiltering", self.w)
        self.prefiltering.setChecked(True)
        self.prefiltering.move(500, self.height - 150)


        # Radio Buttons  
        self.binary = QRadioButton("Binary Templates", self.w)
        self.binary.move(10, self.height-120)
        self.binary.setChecked(True)
        self.binary.clicked.connect(self.clickedBinary)

        self.harmonic = QRadioButton("Harmonic Templates (exp)", self.w)
        self.harmonic.move(10, self.height-100)
        self.harmonic.clicked.connect(self.clickedHarmonic)

        self.triangle = QRadioButton("Harmonic Templates (tri)", self.w)
        self.triangle.move(10, self.height-80)
        self.triangle.clicked.connect(self.clickedTriangle)


        self.colorDic = None
        self.w.show()
        sys.exit(self.app.exec_())
    
    def clickedBinary(self):
        self.harmonic.setChecked(False)
        self.triangle.setChecked(False)

    def clickedHarmonic(self):
        self.binary.setChecked(False)
        self.triangle.setChecked(False)

    def clickedTriangle(self):
        self.binary.setChecked(False)
        self.harmonic.setChecked(False)

    def recognize(self):
        filename = self.filepath.text()
        groundTruth = self.groundTruth.text()
        windowSize = float(self.windowsize.text())
        hopSize = float(self.hopsize.text()) * windowSize
        if(self.binary.isChecked()):
            template_to_use = "bin"
        elif(self.harmonic.isChecked()):
            template_to_use = "exp"
        else:
            template_to_use = "tri"

        if self.hpss.isChecked():
            hpss = True
        else:
            hpss = False
        if self.synth.isChecked():
            synth = True
        else:
            synth = False
        if self.output.isChecked():
            output = True
        else:
            output = False

        if(self.chromas.isChecked()):
            ownChromas = False
        else:
            ownchromas = True

        
        infotext = "Opening '" + filename + "'..."
        self.infobox.setText(infotext)
        self.infobox.repaint()
        self.infobox.repaint()

        samples, samplerate = recognition.openFile(filename)
        orig_samples = samples
        duration = len(samples)/samplerate

        if hpss:
            self.infobox.setText("Doing HPSS...")
            self.infobox.repaint()
            self.infobox.repaint()
            samples, _ = recognition.HPSS(samples)
        windowSizeInSamples = windowSize*samplerate
        hopSizeInSamples = int(float(self.hopsize.text())*windowSizeInSamples)

        self.infobox.setText("Calculating chromas...")
        self.infobox.repaint()
        self.infobox.repaint()
        ownChromas= True
        chromas = None
        if(ownChromas):
            trans = transformer.Transformer(windowSizeInSamples, hopSizeInSamples, samplerate)
            chromas = np.transpose(trans.chroma(trans.logFrequencySpectrogram(trans.spectrogram(trans.stft(samples)))))
        else:
            chromas = recognition.calculateChroma(samples, samplerate, windowSizeInSamples, hopSizeInSamples)

        # Logarithmic compression
        if(self.logComp.isChecked()):
            chromas = np.log(1+float(self.comprate.text())*chromas)
        
        # Prefiltering
        if(self.prefiltering.isChecked()):
            L = float(self.filterL.text())
            chromasFiltered = np.empty(chromas.shape)
            zeroPadsLeft = int(math.floor((L-1)/2))
            zeroPadsRight = int(L-1 - math.floor((L-1)/2))
            chromas = np.concatenate((np.zeros((12, zeroPadsLeft)), chromas), axis=1)
            chromas = np.concatenate((chromas, np.zeros((12, zeroPadsRight))), axis =1)
            for i in range(zeroPadsLeft, chromas.shape[1]-zeroPadsRight):
                left = i - math.floor((L-1)/2)
                right = i + L - 1 - math.floor((L-1)/2)
                chromasFiltered[:, i-zeroPadsLeft]= np.sum(chromas[:,left:right+1], axis=1)
            chromas = chromasFiltered
            chromas = chromas/L

        self.infobox.setText("Identifying chords...")
        self.infobox.repaint()
        self.infobox.repaint()
        chords, temps, labels = recognition.calculateSimilarities(chromas, template_to_use)
        chordSequence = recognition.identifyMostProbableChordSequence(chords, labels, windowSize, hopSize)

        #color dictionary
        if self.colorDic == None:
            self.colorDic = self.chordColorDict(labels)

        if output:
            for i in chordSequence:
                print("Chord " + i[0] + " from " + str(i[1]) + "s to " + str(i[2]) + "s.")

        if synth:
            self.infobox.setText("Synthesizing output...")
            self.infobox.repaint()
            self.infobox.repaint()
            synthesizer.synthChords(chordSequence, labels, orig_samples, samplerate)

        # Waveform
        self.wavToImg(samples, samplerate, windowSize)
        pixmap = QPixmap(os.getcwd() + '/plot.png')
        self.label1.setPixmap(pixmap)
       
        # Recognized Chords
        self.drawChords(chordSequence, labels, duration)
        pixmap2 = QPixmap(os.getcwd() + '/chords.png')
        self.label2.setPixmap(pixmap2)

        # Ground Truth
        if groundTruth != "":
            gtChords = []
            with open(groundTruth, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                for row in reader:
                    gtChords.append((row[0], float(row[1]), float(row[2])))
            self.drawChords(gtChords, labels, duration, 'gtChords.png')
            pixmap3 = QPixmap(os.getcwd() + '/gtChords.png')
            self.label3.setPixmap(pixmap3)
        else:
            self.label3.clear()
        self.infobox.setText("Finished!")
        return None

    def wavToImg(self, samples, samplerate, windowsize):
        x = np.linspace(0, len(samples)/samplerate, len(samples))
        fig = plt.figure()
        fig.set_size_inches(self.label1width/100, self.label1height/100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        ax.set_xlim([0, x[-1]])
        fig.add_axes(ax)
        ax.plot(x,samples)
        
        numberOfLines = 10 
        ts = x[::math.ceil(len(x)/numberOfLines)]
        for t in ts:
            ax.plot((t, t),(-1,1), color='black')
            ax.text(t, 0.0, "%.1f" % t + 's')
            #Only 10 vertical lines
            t += windowsize*numberOfLines/10

        # drop borders of figure
        #fig.subplots_adjust(bottom=0)
        #fig.subplots_adjust(top=1)
        #fig.subplots_adjust(right=1)
        #fig.subplots_adjust(left=0)

        fig.savefig('plot.png', dpi=100, bbox_inchex = 'tight')
        return None
    
    def chordColorDict(self, labels):
        dic = {}
        labels.append("None")
        part = 255/len(labels)
        for i in range(0,len(labels)):
            dic[labels[i]] = (math.ceil(i*part), 255 - math.ceil(i*part), random.randrange(0,256,1))
        return dic

    # Chords should be list of tuples with (chordlabel, starttime, endtime)
    def drawChords(self, chordSequence, labels, duration, filename='chords.png'):
        # Endtime of last chord
        pixelsPerSecond = self.label2width/duration

        img = Image.new("RGB", (self.label2width, self.label2height), (255, 255, 255))
        font = ImageFont.truetype('./arial.ttf', 10)
        draw = ImageDraw.Draw(img)
        # Draw chord colors
        for i in range(0,len(chordSequence)):
            leftCoord = math.ceil(pixelsPerSecond*chordSequence[i][1])
            rightCoord = math.ceil(pixelsPerSecond*chordSequence[i][2])
            color = self.colorDic[chordSequence[i][0]]
            draw.rectangle([(leftCoord,0), (rightCoord, self.label2height)], color)


        # Draw the chord names
        for i in range(0,len(chordSequence)):
            leftCoord = math.ceil(pixelsPerSecond*chordSequence[i][1])
            rightCoord = math.ceil(pixelsPerSecond*chordSequence[i][2])
            ranOffset = random.randrange(0,self.label2height-10,1)
            draw.text((leftCoord,ranOffset), chordSequence[i][0],(0,0,0),font=font)
        img.save(filename)
        return None
