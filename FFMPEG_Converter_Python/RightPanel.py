# Paths workaround

from Paths import *

import os

# Qt
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

# Custom Imports
from SettingsManager import SettingsManager, SignalManager, FileCategory
from SettingsManager import ConversionEvent
from FFMPEG_Functions import AudioOutputFormat, VideoOutputFormat, VideoResolution, SampleRate, Quality, Channels
from styles import *


class RightPanel(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager, signalManager: SignalManager) -> None:
        super().__init__(parent)

        self.settingsManager    = settingsManager
        self.signalManager  = signalManager

        self.signalManager.fileDropped.connect(self.settingsCallback)
        self.audioSettings  = AudioSettings(self, settingsManager)
        self.videoSettings  = VideoSettings(self, settingsManager)
        self.placeholder    = PlaceholderComponent(self)

        self.convertButton = QtWidgets.QPushButton("Convert", self)
        self.convertButton.setObjectName("convertButton")
        self.convertButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convertButton.setDisabled(True)
        self.convertButton.clicked.connect(self.showFileDialog)

        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.addWidget(self.placeholder)
        self.stackedWidget.addWidget(self.audioSettings)
        self.stackedWidget.addWidget(self.videoSettings)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.stackedWidget, 6)
        self.mainLayout.addWidget(self.convertButton, 1)
        self.settingsCallback()

    def settingsCallback(self) -> None:

        if self.settingsManager.fileInfo["category"] == FileCategory.AUDIO_FILE.value:
            self.stackedWidget.setCurrentIndex(1)
            self.mainLayout.setSpacing(150)
            self.convertButton.setDisabled(False)
            self.settingsManager.resetSettings()
            self.audioSettings.updateAllSettings()

        elif self.settingsManager.fileInfo["category"] == FileCategory.VIDEO_FILE.value:
            self.stackedWidget.setCurrentIndex(2)
            self.mainLayout.setSpacing(150)
            self.convertButton.setDisabled(False)
            self.settingsManager.resetSettings()
            self.videoSettings.updateAllSettings()

        else:
            self.stackedWidget.setCurrentIndex(0)
            self.mainLayout.setSpacing(0)
            self.convertButton.setDisabled(True)
            self.settingsManager.resetSettings()

    def showFileDialog(self):
        fileDialog      = QtWidgets.QFileDialog(self) 

        if self.stackedWidget.currentIndex() == 1:
            currentWidget = self.audioSettings
            currentEvent = ConversionEvent.AUDIO_CONVERSION
        
        elif self.stackedWidget.currentIndex() == 2:
            currentWidget = self.videoSettings
            currentEvent = ConversionEvent.VIDEO_CONVERSION

        else:
            print("Should not have gotten here, but oh well.. another bug")
            return

        filePath, _ = fileDialog.getSaveFileName(self, "Save File", "", f"All Files (*);;");
        
        if filePath:
            fileName = os.path.basename(filePath)
            _, fileExtension = os.path.splitext(fileName)

            if not fileExtension:
                extension   = currentWidget.outputFormatCBox.currentText().split(" ")[0]
                fileName = fileName + "." + extension
                filePath = os.path.join(os.path.dirname(filePath), fileName)

            self.settingsManager.setNewOutputFilePath(filePath)
            self.settingsManager.sendConversionEvent(currentEvent)


        

# Audio and Video Settings are kept separate, in case of additional and exclusive features in the future
class AudioSettings(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager) -> None:
        super().__init__(parent)
        self.fileManager = settingsManager
        self.outputLabel = QLabel("Output Format", self)
        self.outputLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.outputFormatCBox = QtWidgets.QComboBox(self)
        self.outputFormatCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for out in AudioOutputFormat:
            self.outputFormatCBox.addItem(out.value)

        self.rateLabel = QLabel("Sample Rate", self)
        self.rateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rateCBox = QtWidgets.QComboBox(self)
        self.rateCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for sr in SampleRate:
            self.rateCBox.addItem(sr.value)

        self.channelLabel = QLabel("Channels", self)
        self.channelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channelsCBox = QtWidgets.QComboBox(self)
        self.channelsCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for ch in Channels:
            self.channelsCBox.addItem(ch.value)

        self.qualityLabel = QLabel("Quality", self)
        self.qualityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qualityCBox = QtWidgets.QComboBox(self)
        self.qualityCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for q in Quality:
            self.qualityCBox.addItem(q.value)

        self.mainLayout = QVBoxLayout(self)
        spacers         = [QtWidgets.QSpacerItem(20, 20) for i in range(4)]
        
        self.mainLayout.addWidget(self.outputLabel)
        self.mainLayout.addWidget(self.outputFormatCBox)
        self.mainLayout.addSpacerItem(spacers[0])

        self.mainLayout.addWidget(self.rateLabel)
        self.mainLayout.addWidget(self.rateCBox)
        self.mainLayout.addSpacerItem(spacers[1])

        self.mainLayout.addWidget(self.channelLabel)
        self.mainLayout.addWidget(self.channelsCBox)
        self.mainLayout.addSpacerItem(spacers[2])

        self.mainLayout.addWidget(self.qualityLabel)
        self.mainLayout.addWidget(self.qualityCBox)
        self.mainLayout.addSpacerItem(spacers[3])

        self.outputFormatCBox.currentIndexChanged.connect(self.updateOutputFormat)
        self.rateCBox.currentIndexChanged.connect(self.updateSampleRate)
        self.channelsCBox.currentIndexChanged.connect(self.updateChannels)
        self.qualityCBox.currentIndexChanged.connect(self.updateQuality)

        self.updateAllSettings()

    def updateOutputFormat(self) -> None:
        self.fileManager.currentAudioSettings[AudioOutputFormat]    = self.outputFormatCBox.currentText()
        if self.fileManager.currentAudioSettings[AudioOutputFormat] == AudioOutputFormat.AIFF.value or self.fileManager.currentAudioSettings[AudioOutputFormat] == AudioOutputFormat.WAV.value:
            self.qualityCBox.setVisible(False)
            self.qualityLabel.setVisible(False)
        else:
            self.qualityCBox.setVisible(True)
            self.qualityLabel.setVisible(True)

    def updateSampleRate(self) -> None:
        self.fileManager.currentAudioSettings[SampleRate]           = self.rateCBox.currentText()

    def updateChannels(self) -> None:
        self.fileManager.currentAudioSettings[Channels]             = self.channelsCBox.currentText()

    def updateQuality(self) -> None:
        self.fileManager.currentAudioSettings[Quality]              = self.qualityCBox.currentText()

    def updateAllSettings(self) -> None:
        self.updateOutputFormat()
        self.updateSampleRate()
        self.updateChannels()
        self.updateQuality()
    

class VideoSettings(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager) -> None:
        super().__init__(parent)
        self.fileManager = settingsManager

        '''videoExtensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".ogv", ".3gp"]'''
        self.outputLabel = QLabel("Output Format", self)
        self.outputLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.outputFormatCBox = QtWidgets.QComboBox(self)
        self.outputFormatCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for outputFormat in VideoOutputFormat:
            self.outputFormatCBox.addItem(outputFormat.value)

        self.resolutionLabel = QLabel("Resolution", self)
        self.resolutionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resolutionCBox = QtWidgets.QComboBox(self)
        self.resolutionCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for resolution in VideoResolution:
            self.resolutionCBox.addItem(resolution.value)

        self.channelLabel = QLabel("Channels", self)
        self.channelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channelsCBox = QtWidgets.QComboBox(self)
        self.channelsCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for ch in Channels:
            self.channelsCBox.addItem(ch.value)

        self.qualityLabel = QLabel("Quality", self)
        self.qualityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qualityCBox = QtWidgets.QComboBox(self)
        self.qualityCBox.setCursor(Qt.CursorShape.PointingHandCursor)
        for q in Quality:
            self.qualityCBox.addItem(q.value)
        
        spacers = [QtWidgets.QSpacerItem(20, 20) for i in range(4)]
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addWidget(self.outputLabel)
        self.mainLayout.addWidget(self.outputFormatCBox)
        self.mainLayout.addSpacerItem(spacers[0])
        
        self.mainLayout.addWidget(self.resolutionLabel)
        self.mainLayout.addWidget(self.resolutionCBox)
        self.mainLayout.addSpacerItem(spacers[1])
        
        self.mainLayout.addWidget(self.channelLabel)
        self.mainLayout.addWidget(self.channelsCBox)
        self.mainLayout.addSpacerItem(spacers[2])
        
        self.mainLayout.addWidget(self.qualityLabel)
        self.mainLayout.addWidget(self.qualityCBox)
        self.mainLayout.addSpacerItem(spacers[3])

        self.outputFormatCBox.currentIndexChanged.connect(self.updateOutputFormat)
        self.resolutionCBox.currentIndexChanged.connect(self.updateResolution)
        self.channelsCBox.currentIndexChanged.connect(self.updateChannels)
        self.qualityCBox.currentIndexChanged.connect(self.updateQuality)

        self.updateAllSettings()

    def updateOutputFormat(self) -> None:
        self.fileManager.currentVideoSettings[VideoOutputFormat]    = self.outputFormatCBox.currentText()

    def updateResolution(self) -> None:
        self.fileManager.currentVideoSettings[VideoResolution]      = self.resolutionCBox.currentText()

    def updateChannels(self) -> None:
        self.fileManager.currentVideoSettings[Channels]             = self.channelsCBox.currentText()

    def updateQuality(self) -> None:
        self.fileManager.currentVideoSettings[Quality]              = self.qualityCBox.currentText()

    def updateAllSettings(self) -> None:
        self.updateOutputFormat()
        self.updateResolution()
        self.updateChannels()
        self.updateQuality()


class PlaceholderComponent(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.gif_label = QLabel(self)
        self.gif_movie = QtGui.QMovie(GRINCH)

        self.gif_label.setMovie(self.gif_movie)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_movie.start()

        layout = QVBoxLayout(self)
        layout.addWidget(self.gif_label)
        
    