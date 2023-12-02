import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QStackedWidget, QFileDialog 
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QMouseEvent, QPixmap, QMovie
from PyQt6.QtCore import Qt, QMimeData, QEvent, pyqtSignal, QObject
from styles import *
import os
from FileManager import FileManager, FileCategory
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudioDevice, QMediaDevices
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl

# Left Panel ================================================================================

class SignalManager(QObject):
    fileDropped = pyqtSignal()

class FileDropFrame(QFrame):
    def __init__(self, fileManager: FileManager, signalManager: SignalManager):
        super().__init__()
        self.fileManager = fileManager
        self.signalManager = signalManager
        self.setFrameStyle(QFrame.Shape.Panel)
        self.setAcceptDrops(True)
        self.setStyleSheet(f"background-color: {Color.FILE_DROP_FRAME_DEFAULT.value}")
        self.label = QLabel("Drag and Drop File")

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data = event.mimeData()
        self.setStyleSheet(f"background-color: {Color.FILE_DROP_FRAME_DRAG.value}")
        if isinstance(mime_data, QMimeData) and mime_data.hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        mime_data = event.mimeData()
        if isinstance(mime_data, QMimeData) and mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        if isinstance(mime_data, QMimeData) and mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.fileManager.setNewFilePath(file_path)
            self.fileManager.updateFileInfo()
            self.setStyleSheet(f"background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};")
            self.signalManager.fileDropped.emit()


class FileUploader(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager):
        super().__init__(parent)

        # Title Label
        self.label = QLabel()
        self.label.setText("Upload File")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Drop and File Choose Components
        self.dragDrop = FileDropFrame(fileManager, signalManager)
        self.button = QtWidgets.QPushButton("Choose File")
        self.button.clicked.connect(self.chooseFile)

        # Layouts
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.fileUploadLayout = QHBoxLayout(self)
        self.fileUploadLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.fileUploadLayout)

        self.fileUploadLayout.addWidget(self.dragDrop, 3)
        self.fileUploadLayout.addWidget(self.button, 1)

    def chooseFile(self):
        
        file_dialog = QFileDialog(self)
        file_dialog.setOptions(QFileDialog.Option.DontConfirmOverwrite)
        file_paths, _ = file_dialog.getOpenFileNames(self, "Choose File", "", "All Files (*);;Audio Files (*.mp3 *.wav);;Video Files (*.mp4 *.avi)")

        if file_paths:
            chosen_file = file_paths[0]
            self.dragDrop.fileManager.setNewFilePath(chosen_file)
            self.dragDrop.fileManager.updateFileInfo()
            self.dragDrop.signalManager.fileDropped.emit()


class MultiMediaPlayer(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager):
        super().__init__(parent)

        # Create a QMediaPlayer instance
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        self.fileManager = fileManager
        self.signalManager = signalManager

        self.signalManager.fileDropped.connect(self.initialiseMediaPath)

        self.playButton = QtWidgets.QPushButton("Play", self)
        self.playButton.clicked.connect(self.playMedia)

        self.pauseButton = QtWidgets.QPushButton("Pause", self)
        self.pauseButton.clicked.connect(self.pauseMedia)

        self.seekSlider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.seekSlider.setRange(0, 10)
        self.seekSlider.setDisabled(True)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.pauseButton)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.videoWidget, 5)
        mainLayout.addWidget(self.seekSlider, 1)
        mainLayout.addLayout(buttonLayout)

        
        self.seekSlider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.updateSliderPosition)
        self.mediaPlayer.errorOccurred.connect(self.handleError)

    def initialiseMediaPath(self):
        mediaPath = self.fileManager.getCurrentFilePath()
        self.mediaPlayer.setSource(QUrl.fromLocalFile(mediaPath))

        # Update the seek slider range based on the media's duration
        duration = self.mediaPlayer.duration()
        self.seekSlider.setRange(0, duration)
        self.seekSlider.setEnabled(True)

    def playMedia(self):
        self.mediaPlayer.play()

    def pauseMedia(self):
        self.mediaPlayer.pause()

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def updateSliderPosition(self, position):
        self.seekSlider.setValue(position)

    def handleError(self, error):
        print(error)



class FileTextComponent(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager):
        super().__init__(parent)
        self.fileManager        = fileManager
        self.signalManager      = signalManager
        self.fileInformation    = fileManager.getCurrentFileInformation()
        
        self.fileNameLabel = QLabel("File Name")
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileName = QLabel(self.fileInformation["name"])
        self.fileName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileExtensionLabel = QLabel("Extension")
        self.fileExtensionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.fileExtension = QLabel(self.fileInformation["extension"])
        self.fileExtension.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileSizeLabel = QLabel("Size")
        self.fileSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileSize = QLabel(self.fileInformation["size"])
        self.fileSize.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileRateLabel = QLabel("Rate")
        self.fileRateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileRate = QLabel(self.fileInformation["rate"])
        self.fileRate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileResolutionLabel = QLabel("Resolution")
        self.fileResolutionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileResolution = QLabel(str(self.fileInformation["resolution"]))
        self.fileResolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileCodecsLabel = QLabel("Codecs")
        self.fileCodecsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileCodecs = QLabel(str(self.fileInformation["codecs"]))
        self.fileCodecs.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.fileChannelsLabel = QLabel("Channels")
        # self.fileChannelsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.fileChannels = QLabel(str(self.fileInformation["channels"]))
        # self.fileChannels.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.signalManager.fileDropped.connect(self.updateFileInformation)

        # Layout
        self.mainLayout = QtWidgets.QGridLayout(self)
        
        # Column 0
        self.mainLayout.addWidget(self.fileNameLabel, 0, 0)
        self.mainLayout.addWidget(self.fileName, 1, 0)

        self.mainLayout.addWidget(self.fileSizeLabel, 2, 0)
        self.mainLayout.addWidget(self.fileSize, 3, 0)

        # Column 1
        self.mainLayout.addWidget(self.fileExtensionLabel, 0, 1)
        self.mainLayout.addWidget(self.fileExtension, 1, 1)

        self.mainLayout.addWidget(self.fileRateLabel, 2, 1)
        self.mainLayout.addWidget(self.fileRate, 3, 1)

        # Column 2
        self.mainLayout.addWidget(self.fileResolutionLabel, 0, 2)
        self.mainLayout.addWidget(self.fileResolution, 1, 2)

        self.mainLayout.addWidget(self.fileCodecsLabel, 2, 2)
        self.mainLayout.addWidget(self.fileCodecs, 3, 2)

    def updateFileInformation(self):
        
        self.fileInformation = self.fileManager.getCurrentFileInformation()
        
        self.fileName.setText(str(self.fileInformation["name"]))
        self.fileExtension.setText(str(self.fileInformation["extension"]))
        self.fileSize.setText(str(self.fileInformation["size"]))
        self.fileResolution.setText(str(self.fileInformation["resolution"]))


class FileInformation(QWidget):
    
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager):
        super().__init__(parent)
        
        # Widgets
        self.label = QLabel()
        self.label.setText("File Information")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.player     = MultiMediaPlayer(self, fileManager, signalManager)
        self.filetext   = FileTextComponent(self, fileManager, signalManager)

        # Layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.label, 1)
        self.mainLayout.addWidget(self.player, 5)
        self.mainLayout.addWidget(self.filetext, 1)

    # def paintEvent(self, event: QtGui.QPaintEvent | None) -> None:
    #     painter = QtGui.QPainter(self)
    #     painter.setPen(QtGui.QPen(QtGui.QColor('white'), 2))
    #     painter.drawRect(self.label.geometry())
    #     painter.drawRect(self.player.geometry())


class LeftPanel(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager) -> None:
        super().__init__(parent)
        self.info       = FileInformation(self, fileManager, signalManager)
        self.fileUpload = FileUploader(self, fileManager, signalManager)
        self.initComponent()

    def initComponent(self) -> None:
    
        self.leftPanelLayout = QVBoxLayout(self)
        self.leftPanelLayout.addWidget(self.info, 5)
        self.leftPanelLayout.addWidget(self.fileUpload, 1)

    # def paintEvent(self, event: QtGui.QPaintEvent | None) -> None:
    #     painter = QtGui.QPainter(self)
    #     painter.setPen(QtGui.QPen(QtGui.QColor('white'), 2))
    #     painter.drawRect(self.info.geometry())
    #     painter.drawRect(self.fileUpload.geometry())
    
    
# Right Panel ================================================================================

class AudioSettings(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager) -> None:
        super().__init__(parent)
        self.outputLabel = QLabel("Output Format")
        self.outputLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.outputFormatCBox = QtWidgets.QComboBox(self)
        self.outputFormatCBox.addItem("mp3 (LAME)")
        self.outputFormatCBox.addItem("aac (Advanced Audio Codec)")
        self.outputFormatCBox.addItem("wav (Pulse Code Modulation)")
        self.outputFormatCBox.addItem("flac (Free Lossless Audio Codec)")
        self.outputFormatCBox.addItem("ogg (Vorbis)")
        self.outputFormatCBox.addItem("m4a (Advanced Audio Codec)")
        self.outputFormatCBox.addItem("ac3 (Dolby Digital)")
        self.outputFormatCBox.addItem("aiff (Pulse Code Modulation)")
        self.outputFormatCBox.addItem("amr (Adaptive Multi-Rate)")
        self.outputFormatCBox.addItem("mp2 (MPEG Audio Layer II)")

        self.rateLabel = QLabel("Sample Rate")
        self.rateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rateCBox = QtWidgets.QComboBox(self)
        self.rateCBox.addItem("22.05 kHz")
        self.rateCBox.addItem("32 kHz")
        self.rateCBox.addItem("44.1 kHz")
        self.rateCBox.addItem("48 kHz")
        self.rateCBox.addItem("96 kHz")
        self.rateCBox.addItem("192 kHz")

        self.channelLabel = QLabel("Channels")
        self.channelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channelsCBox = QtWidgets.QComboBox(self)
        self.channelsCBox.addItem("Mono")
        self.channelsCBox.addItem("Stereo")

        self.qualityLabel = QLabel("Quality")
        self.qualityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quality = QtWidgets.QComboBox(self)
        self.quality.addItem("Low")
        self.quality.addItem("Medium")
        self.quality.addItem("High")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.outputLabel)
        self.mainLayout.addWidget(self.outputFormatCBox)
        self.mainLayout.addWidget(self.rateLabel)
        self.mainLayout.addWidget(self.rateCBox)
        self.mainLayout.addWidget(self.channelLabel)
        self.mainLayout.addWidget(self.channelsCBox)
        self.mainLayout.addWidget(self.qualityLabel)
        self.mainLayout.addWidget(self.quality)
    
class VideoSettings(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager) -> None:
        super().__init__(parent)
        '''videoExtensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".ogv", ".3gp"]'''
        self.outputLabel = QLabel("Output Format")
        self.outputLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.outputFormatCBox = QtWidgets.QComboBox(self)
        self.outputFormatCBox.addItem("mp4 (H.264)")
        self.outputFormatCBox.addItem("avi (Xvid)")
        self.outputFormatCBox.addItem("mkv (H.264)")
        self.outputFormatCBox.addItem("mov (H.264)")
        self.outputFormatCBox.addItem("wmv (Windows Media Video)")
        self.outputFormatCBox.addItem("flv (H.264)")
        self.outputFormatCBox.addItem("webm (VP8)")
        self.outputFormatCBox.addItem("mpeg (MPEG-2)")
        self.outputFormatCBox.addItem("ogv (Theora)")
        self.outputFormatCBox.addItem("3gp (H.264)")

        self.resolutionLabel = QLabel("Resolution")
        self.resolutionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resolutionCBox = QtWidgets.QComboBox(self)
        self.resolutionCBox.addItem("640x480 (Standard Definition)")
        self.resolutionCBox.addItem("720x480 (Standard Definition)")
        self.resolutionCBox.addItem("1280x720 (High Definition)")
        self.resolutionCBox.addItem("1920x1080 (Full HD)")
        self.resolutionCBox.addItem("2048x1080 (2k)")
        self.resolutionCBox.addItem("2560x1440 (QHD)")
        self.resolutionCBox.addItem("3840x2160 (4k)")
        self.resolutionCBox.addItem("4096x2160 (4k)")

        self.channelLabel = QLabel("Channels")
        self.channelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channelsCBox = QtWidgets.QComboBox(self)
        self.channelsCBox.addItem("Mono")
        self.channelsCBox.addItem("Stereo")

        self.qualityLabel = QLabel("Quality")
        self.qualityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qualityCBox = QtWidgets.QComboBox(self)
        self.qualityCBox.addItem("Low")
        self.qualityCBox.addItem("Medium")
        self.qualityCBox.addItem("High")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.outputLabel)
        self.mainLayout.addWidget(self.outputFormatCBox)
        self.mainLayout.addWidget(self.resolutionLabel)
        self.mainLayout.addWidget(self.resolutionCBox)
        self.mainLayout.addWidget(self.channelLabel)
        self.mainLayout.addWidget(self.channelsCBox)
        self.mainLayout.addWidget(self.qualityLabel)
        self.mainLayout.addWidget(self.qualityCBox)


class PlaceholderComponent(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Create a QLabel to display the GIF
        self.gif_label = QLabel(self)
        self.gif_movie = QMovie("/Users/james/Downloads/output-onlinegiftools.gif")

        # Set the movie to the label
        self.gif_label.setMovie(self.gif_movie)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.gif_label.setFixedWidth(parent.width())
        self.gif_movie.start()

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.gif_label)
        
    
class RightPanel(QWidget):
    def __init__(self, parent: QWidget, fileManager: FileManager, signalManager: SignalManager) -> None:
        super().__init__(parent)
        self.fileManager = fileManager
        self.signalManager = signalManager

        self.signalManager.fileDropped.connect(self.settingsCallback)
        
        self.label = QLabel()
        self.label.setText("Conversion Settings")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.audioSettings  = AudioSettings(self, fileManager)
        self.videoSettings  = VideoSettings(self, fileManager)
        self.placeholder    = PlaceholderComponent(self)

        self.convertButton = QtWidgets.QPushButton("Convert")

        self.stackedWidget  = QStackedWidget(self)
        self.stackedWidget.addWidget(self.placeholder)
        self.stackedWidget.addWidget(self.audioSettings)
        self.stackedWidget.addWidget(self.videoSettings)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.label, 1)
        self.mainLayout.addWidget(self.stackedWidget, 5)
        self.mainLayout.addWidget(self.convertButton, 3)

    # def paintEvent(self, event: QtGui.QPaintEvent | None) -> None:
    #     painter = QtGui.QPainter(self)
    #     painter.setPen(QtGui.QPen(QtGui.QColor('white'), 2))
    #     painter.drawRect(self.stackedWidget.geometry())
    #     painter.drawRect(self.label.geometry())

    def settingsCallback(self) -> None:
        if self.fileManager.fileInfo["category"] == FileCategory.AUDIO_FILE.value:
            self.stackedWidget.setCurrentIndex(1)

        elif self.fileManager.fileInfo["category"] == FileCategory.VIDEO_FILE.value:
            self.stackedWidget.setCurrentIndex(2)

        else:
            self.stackedWidget.setCurrentIndex(0)
