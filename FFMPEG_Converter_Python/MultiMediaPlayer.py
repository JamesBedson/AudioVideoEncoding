from PyQt6 import QtCore, QtWidgets, QtMultimedia, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from SettingsManager import SettingsManager, SignalManager
from PyQt6.QtMultimediaWidgets import QVideoWidget

class MultiMediaPlayer(QWidget):
    def __init__(self, parent: QWidget, fileManager: SettingsManager, signalManager: SignalManager):
        super().__init__(parent)

        # Create a QMediaPlayer instance
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        self.fileManager = fileManager
        self.signalManager = signalManager

        self.signalManager.fileDropped.connect(self.initialiseMediaPath)

        self.slowDownButton = QtWidgets.QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/rewind.png"))
        self.slowDownButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.slowDownButton.clicked.connect(self.slowSpeed)

        self.playButton = QtWidgets.QPushButton(self)
        self.playButton.setIcon(QtGui.QIcon("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/play.png"))
        self.playButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.playButton.clicked.connect(self.playMedia)

        self.pauseButton = QtWidgets.QPushButton(self)
        self.pauseButton.setIcon(QtGui.QIcon("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/pause.png"))
        self.pauseButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pauseButton.clicked.connect(self.pauseMedia)

        self.stopButton = QtWidgets.QPushButton(self)
        self.stopButton.setIcon(QtGui.QIcon("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/stop.png"))
        self.stopButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stopButton.clicked.connect(self.stopMedia)

        self.fastforwardButton = QtWidgets.QPushButton(self)
        self.fastforwardButton.setIcon(QtGui.QIcon("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/fastForward.png"))
        self.fastforwardButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fastforwardButton.clicked.connect(self.fastForward)

        self.seekSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.seekSlider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.seekSlider.setRange(0, 10)
        self.seekSlider.setDisabled(True)

        buttonLayout = QHBoxLayout()
        buttonLayout.addSpacing(20)
        buttonLayout.addWidget(self.slowDownButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.fastforwardButton)
        buttonLayout.addSpacing(20)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.videoWidget, 8)
        mainLayout.addWidget(self.seekSlider, 1)
        mainLayout.addLayout(buttonLayout)
        
        self.seekSlider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.updateSliderPosition)
        self.mediaPlayer.errorOccurred.connect(self.handleError)

    def initialiseMediaPath(self):
        mediaPath = self.fileManager.getCurrentInputFilePath()
        self.mediaPlayer.setSource(QtCore.QUrl.fromLocalFile(mediaPath))

        # Update the seek slider range based on the media's duration
        duration = self.mediaPlayer.duration()
        self.seekSlider.setRange(0, duration)
        self.seekSlider.setEnabled(True)

    def playMedia(self):
        self.mediaPlayer.play()

    def pauseMedia(self):
        self.mediaPlayer.pause()

    def stopMedia(self):
        self.mediaPlayer.stop()

    def fastForward(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() * 2)

    def slowSpeed(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate() // 2)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def updateSliderPosition(self, position):
        self.seekSlider.setValue(position)

    def handleError(self, error):
        print(error)