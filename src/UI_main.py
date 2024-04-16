import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QThread, Qt, QRect, QPropertyAnimation, QParallelAnimationGroup, QSequentialAnimationGroup, QSize
from predicter import Predicter


class importThread(QThread):
    def __init__(self):
        super(importThread, self).__init__()

    def run(self):
        Predicter.importer()

class MainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("WhatGenre")
        self.setWindowIcon(QtGui.QIcon("./Resources/mike.png"))
        
        self.desktopWidth = QDesktopWidget().screenGeometry(-1).width()
        self.desktopHeight = QDesktopWidget().screenGeometry(-1).height()

        self.width = self.desktopWidth//2 - 240
        self.height = self.desktopHeight//2 + 350
        
        self.setGeometry(960-self.width//2, 100, self.width, self.height)

        self.setStyleSheet(open('src/style/style.css').read())
        self.UIComponents()

    def UIComponents(self):
        self.Title = QLabel("WhatGenre", self)
        self.Title.setFixedSize(500, 160)
        self.Title.move(((self.width - self.Title.width()) // 2), ((self.height - self.Title.height()) // 2))
        self.Title.setObjectName("Title")
        self.Title.setAlignment(Qt.AlignCenter)

        layoutMenu = QHBoxLayout()
        self.buttonUpload = QPushButton("Upload a song", self)
        self.buttonUpload.setFixedSize(370, 70)
        self.buttonUpload.clicked.connect(self.onUploadButtonClicked)
        self.buttonRecord = QPushButton("Record", self)
        self.buttonRecord.setFixedSize(200, 70)
        layoutMenu.addWidget(self.buttonUpload)
        layoutMenu.addWidget(self.buttonRecord, 1)

        self.menuFrame = QFrame(self)
        self.menuFrame.setFrameShape(QFrame.NoFrame)
        self.menuFrame.setLineWidth(0)
        self.menuFrame.setLayout(layoutMenu)
        self.menuFrame.setObjectName("Menu Frame")
        self.menuFrame.setVisible(False)
        self.setCentralWidget(self.menuFrame)

        layoutResult = QGridLayout(self)
        self.Rec1 = QLabel(self)
        self.Rec1.setFixedSize(300, 200)
        self.Rec1.setAlignment(Qt.AlignHCenter)
        self.Rec1.setWordWrap(True)
        self.Rec1.setOpenExternalLinks(True)
        self.Rec1.setObjectName("Rec")

        self.Rec2 = QLabel(self)
        self.Rec2.setFixedSize(300, 200)
        self.Rec2.setAlignment(Qt.AlignHCenter)
        self.Rec2.setWordWrap(True)
        self.Rec2.setOpenExternalLinks(True)
        self.Rec2.setObjectName("Rec")

        self.Rec3 = QLabel(self)
        self.Rec3.setFixedSize(300, 200)
        self.Rec3.setAlignment(Qt.AlignHCenter)
        self.Rec3.setWordWrap(True)
        self.Rec3.setOpenExternalLinks(True)
        self.Rec3.setObjectName("Rec")

        self.Rec4 = QLabel(self)
        self.Rec4.setFixedSize(300, 200)
        self.Rec4.setAlignment(Qt.AlignHCenter)
        self.Rec4.setWordWrap(True)
        self.Rec4.setOpenExternalLinks(True)
        self.Rec4.setObjectName("Rec")

        layoutResult.addWidget(self.Rec1, 0, 0)
        layoutResult.addWidget(self.Rec2, 0, 1)
        layoutResult.addWidget(self.Rec3, 1, 0)
        layoutResult.addWidget(self.Rec4, 1, 1)

        self.resultFrame = QFrame(self)
        self.resultFrame.setFrameShape(QFrame.NoFrame)
        self.resultFrame.setLineWidth(0)
        self.resultFrame.setObjectName("Result Frame")
        self.resultFrame.setFixedSize(614, 414)
        self.resultFrame.setVisible(False)
        self.resultFrame.setLayout(layoutResult)

        self.tryout = QLabel('Maybe try out:', self)
        self.tryout.setFixedSize(300, 60)
        self.tryout.setStyleSheet('font: 20pt "Poppins Medium"')
        self.tryout.setVisible(False)

        self.genreLabel = QLabel(self)
        self.genreLabel.setFixedSize(500, 100)
        self.genreLabel.setObjectName("genreLabel")
        self.genreLabel.setWordWrap(True)
        self.genreLabel.setAlignment(Qt.AlignCenter)
        self.genreLabel.setVisible(False)

        self.buttonReUpload = QPushButton(self)
        self.buttonReUpload.setFixedSize(100, 100)
        self.buttonReUpload.setIcon(QtGui.QIcon("./Resources/folder.jpg"))
        self.buttonReUpload.setIconSize(QSize(40, 40))
        self.buttonReUpload.setObjectName('Back')
        self.buttonReUpload.setVisible(False)
        self.buttonReUpload.clicked.connect(self.onUploadButtonClicked)

        self.buttonReRecord = QPushButton(self)
        self.buttonReRecord.setFixedSize(100, 100)
        self.buttonReRecord.setIcon(QtGui.QIcon("./Resources/mike.png"))
        self.buttonReRecord.setIconSize(QSize(40, 40))
        self.buttonReRecord.setObjectName('Back')
        self.buttonReRecord.setVisible(False)
     #   self.buttonReRecord.clicked.connect(self.onRecordButtonClicked)

        self.loadingCircle = QLabel(self)
        self.loadingMovie = QMovie("./Resources/Rolling-0.9s-230px.gif")
        self.loadingCircle.setMovie(self.loadingMovie)
        self.loadingCircle.setFixedSize(230, 230)
        self.loadingCircle.setMaximumWidth(50)

        self.importer = importThread()
        self.importer.start()
        self.predicterCreated = False

        self.show()

        unfadeTitle = self.unfade(self.Title, time = 1700, start = False)
        risingTitle = self.risingAnimation(widget = self.Title, rise_y = 0, time = 920, tk = 0.65, start = False)

        self.startUpAnimation = QSequentialAnimationGroup(self.effect)
        self.startUpAnimation.addAnimation(unfadeTitle)
        self.startUpAnimation.addAnimation(risingTitle)
        self.startUpAnimation.start()

        self.startUpAnimation.finished.connect(lambda: self.unfade(self.menuFrame, time = 800))
    

    def createPredicter(self):
        self.predictThread = QThread()
        self.predicter = Predicter()
        self.predicter.moveToThread(self.predictThread)
        self.predicter.start.connect(lambda: self.loading())
        self.importer.wait()
        self.predicter.finished.connect(lambda: (self.result(self.predicter), self.predicter.stop(), self.predictThread.quit(), self.predictThread.wait()))  
        self.predictThread.started.connect(self.predicter.predict)

    def fade(self, widget, time = 400):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(time)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)

        self.animation.start()
        return self.animation

    def unfade(self, widget, time, start = True):
        widget.setVisible(True)
        self.effect = QGraphicsOpacityEffect()

        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(time)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

        if start == True:
            self.animation.start()
        return self.animation

    def onUploadButtonClicked(self):
        filepath = QFileDialog.getOpenFileName(parent = self, 
                                        caption = "Select a file", 
                                        directory = os.getcwd(),
                                        filter = "Audio Files (*.mp3 *.mp4 *.flac *.wav *.m4a)")[0]
        if filepath != '':
            if(self.predicterCreated == False):
                self.createPredicter()
                self.predicterCreated = True
            self.genreLabel.setVisible(False)
            self.buttonReUpload.setVisible(False)
            self.buttonReRecord.setVisible(False)
            self.resultFrame.setVisible(False)
            self.tryout.setVisible(False)            
            self.buttonUpload.setEnabled(False)
            self.predicter.setFilepath(filepath)
            if(self.menuFrame.isVisible()):
                frameFade = self.fade(self.menuFrame)
                frameFade.finished.connect(lambda: (self.predictThread.start(), self.menuFrame.setVisible(False)))
            else:
                self.predictThread.start()

    def loading(self):
        self.loadingCircle.move(self.Title.x() + 125, self.Title.y() + 300)
        self.loadingMovie.start()
        self.loadingCircle.show()

    def risingAnimation(self, widget, rise_y, time, tk, start = True):
        self.rising = QPropertyAnimation(widget, b"geometry")
        self.rising.setDuration(time)
        self.rising.setKeyValueAt(tk, QRect(widget.x(), widget.y(), widget.width(), widget.height()))
        self.rising.setKeyValueAt(1, QRect(widget.x(), rise_y, widget.width(), widget.height()))

        if start:
            self.rising.start()

        return self.rising   

    def parallelUnfade(self, widgets_and_times):
        parallel = QParallelAnimationGroup(self.effect)
        for widget, time in widgets_and_times:
            parallel.addAnimation(self.unfade(widget, time, start = False))
        parallel.start()

    def result(self, predicter):
        self.loadingMovie.stop()
        self.loadingCircle.hide()

        self.genreLabel.setText("It's " + predicter.prediction + "!")
        print(self.genreLabel.text())
        self.genreLabel.move(((self.width - self.Title.width()) // 2), ((self.height+250 - self.Title.height()) // 3 + 60))

        recTemplate = '<a href="https://www.youtube.com/results?search_query={}">{} - {}</a>'

        self.Rec1.setText(recTemplate.format( (predicter.recs[0]['artistName'] + ' ' + predicter.recs[0]['trackName']).replace(' ', '+'), predicter.recs[0]['artistName'], predicter.recs[0]['trackName']))
        self.Rec2.setText(recTemplate.format( (predicter.recs[1]['artistName'] + ' ' + predicter.recs[1]['trackName']).replace(' ', '+'), predicter.recs[1]['artistName'], predicter.recs[1]['trackName']))
        self.Rec3.setText(recTemplate.format( (predicter.recs[2]['artistName'] + ' ' + predicter.recs[2]['trackName']).replace(' ', '+'), predicter.recs[2]['artistName'], predicter.recs[2]['trackName']))
        self.Rec4.setText(recTemplate.format( (predicter.recs[3]['artistName'] + ' ' + predicter.recs[3]['trackName']).replace(' ', '+'), predicter.recs[3]['artistName'], predicter.recs[3]['trackName']))

        self.buttonReUpload.move((self.width - self.buttonReUpload.width()) // 2 - 70, self.height - self.buttonReUpload.height() - 20)
        self.buttonReRecord.move((self.width - self.buttonReUpload.width()) // 2 + 70, self.height - self.buttonReUpload.height() - 20)

        self.parallelUnfade( [(self.genreLabel, 900), (self.buttonReUpload, 800), (self.buttonReRecord, 800)] )
        
        rising = self.risingAnimation(self.genreLabel, rise_y = 130, time = 1200, tk = 0.8)
        rising.finished.connect(lambda: (self.resultFrame.move((self.width - self.resultFrame.width()) // 2, self.genreLabel.y() + self.genreLabel.height() + 60), self.tryout.move(self.resultFrame.x() + 10, self.resultFrame.y() - 40), self.parallelUnfade( [(self.resultFrame, 900), (self.tryout, 900)])))

        
if __name__ == "__main__" :
    App = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("./Resources/Hiatus.otf")
    QtGui.QFontDatabase.addApplicationFont("./Resources/Poppins-SemiBold.ttf")
    QtGui.QFontDatabase.addApplicationFont("./Resources/Poppins-Medium.ttf")
  
    window = MainWindow()

    App.exec_()

    App.quit() 