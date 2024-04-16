#%%
from joblib import load
import os.path
from pydub import AudioSegment
from pathlib import PurePath
from PyQt5 import QtCore
import random
import recommender
from numpy import argmax


#%%
class Predicter(QtCore.QObject):
    start = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def importer():
        global keras, librosa, input_preproc
        keras = __import__('keras', fromlist = ('models'))
        librosa = __import__('librosa', fromlist = ('load'))
        input_preproc = __import__('input_preprocessing', fromlist = ('extract_info'))
        
    
    def __init__(self, filepath = None):
        super(Predicter, self).__init__()
        self.filepath = filepath
        self.genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()

        self._isRunning = True

    def load_model(self):
        self.model = keras.models.load_model('./model/')
        self.fit = load('./model/std_scaler.bin')

    def setFilepath(self, filepath):
        self.filepath = filepath
        
    @QtCore.pyqtSlot()
    def predict(self):
        self.start.emit()
        
        self.load_model()
        wavless = False
        filepath = PurePath(self.filepath)
        filepath_full, extension = os.path.splitext(filepath)
        sound = AudioSegment.from_file(filepath)
        if (len(sound) >= 30000):
            sample_start = random.randint(0, len(sound)-30000)/1000
            sound = sound[sample_start*1000:(sample_start + 30)*1000]
        print(filepath.name)
        if(extension != '.wav'):
            sound.export(filepath_full + ".wav", format="wav")
            wavless = True
        print("Gata pana la librosa load")

        song, sr = librosa.load(filepath_full + ".wav")
        self.prediction = self.model(input_preproc.extract_info(song, sr, self.fit))
        self.prediction = self.genres[argmax(self.prediction)]

        if(wavless == True):
            os.remove(filepath_full + ".wav")

        self.recs = recommender.lastfm_getTopTracks(self.prediction)

        self.finished.emit()

    def stop(self):
        self._isRunning = False