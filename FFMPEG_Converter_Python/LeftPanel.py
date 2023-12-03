# Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsDropShadowEffect

# Custom Imports
from SettingsManager import SettingsManager, SignalManager
from MultiMediaPlayer import MultiMediaPlayer
from styles import *

# Left Panel ================================================================================
class LeftPanel(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager, signalManager: SignalManager) -> None:
        super().__init__(parent)
        self.info       = FileInformation(self, settingsManager, signalManager)
        self.fileUpload = FileUploader(self, settingsManager, signalManager)
        self.initComponent()


    def initComponent(self) -> None:
        self.leftPanelLayout = QVBoxLayout(self)
        #self.leftPanelLayout.addWidget(self.label, 1)
        self.leftPanelLayout.addWidget(self.info, 10)
        self.leftPanelLayout.addWidget(self.fileUpload, 1)

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        painter = QtGui.QPainter(self)

        painter.setBrush(QtGui.QColor(Color.BACKGROUND_COLOR_SECONDARY.value))

        borderColour = QtGui.QColor(Color.ACCENT_COLOR_PRIMARY_DARK.value)
        painter.setPen(borderColour)
        pen = QtGui.QPen(borderColour)
        pen.setWidth(BORDER_WIDTH)  
        painter.setPen(pen)

        infoRect        = self.info.geometry()
        fileUploadRect  = self.fileUpload.geometry()

        painter.drawRoundedRect(infoRect, BORDER_RADIUS, BORDER_RADIUS)
        painter.drawRoundedRect(fileUploadRect, BORDER_RADIUS, BORDER_RADIUS)

# INFO DISPLAY ==============================================================================
class FileInformation(QWidget):
    
    def __init__(self, parent: QWidget, settingsManager: SettingsManager, signalManager: SignalManager):
        super().__init__(parent)
        
        # Widgets
        self.player = MultiMediaPlayer(self, settingsManager, signalManager)
        self.filetext = FileTextComponent(self, settingsManager, signalManager)

        # Layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.player, 10)
        self.mainLayout.addWidget(self.filetext, 3)
        
class FileTextComponent(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager, signalManager: SignalManager):
        super().__init__(parent)
        self.fileManager        = settingsManager
        self.signalManager      = signalManager
        self.fileInformation    = settingsManager.getCurrentFileInformation()
        
        self.fileNameLabel = QLabel("File Name")
        self.fileNameLabel.setFont(Font.H2_FONT_Q.value)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileName = QLabel(self.fileInformation["name"])
        self.fileName.setFont(Font.H3_FONT_Q.value)
        self.fileName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileExtensionLabel = QLabel("Extension")
        self.fileExtensionLabel.setFont(Font.H2_FONT_Q.value)
        self.fileExtensionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileExtension = QLabel(self.fileInformation["extension"])
        self.fileExtension.setFont(Font.H3_FONT_Q.value)
        self.fileExtension.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileSizeLabel = QLabel("Size")
        self.fileSizeLabel.setFont(Font.H2_FONT_Q.value)
        self.fileSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileSize = QLabel(self.fileInformation["size"])
        self.fileSize.setFont(Font.H3_FONT_Q.value)
        self.fileSize.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileRateLabel = QLabel("Rate")
        self.fileRateLabel.setFont(Font.H2_FONT_Q.value)
        self.fileRateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileRate = QLabel(self.fileInformation["rate"])
        self.fileRate.setFont(Font.H3_FONT_Q.value)
        self.fileRate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileResolutionLabel = QLabel("Resolution")
        self.fileResolutionLabel.setFont(Font.H2_FONT_Q.value)
        self.fileResolutionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileResolution = QLabel(str(self.fileInformation["resolution"]))
        self.fileResolution.setFont(Font.H3_FONT_Q.value)
        self.fileResolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileCodecsLabel = QLabel("Codec")
        self.fileCodecsLabel.setFont(Font.H2_FONT_Q.value)
        self.fileCodecsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileCodecs = QLabel(str(self.fileInformation["codecs"]))
        self.fileCodecs.setFont(Font.H3_FONT_Q.value)
        self.fileCodecs.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.signalManager.fileDropped.connect(self.updateFileInformation)

        # Layout
        self.mainLayout = QtWidgets.QGridLayout(self)
        # Row 0
        self.mainLayout.addWidget(self.fileNameLabel, 0, 0)
        self.mainLayout.addWidget(self.fileExtensionLabel, 0, 1)
        self.mainLayout.addWidget(self.fileResolutionLabel, 0, 2)

        # Row 1
        self.mainLayout.addWidget(self.fileName, 1, 0)
        self.mainLayout.addWidget(self.fileExtension, 1, 1)
        self.mainLayout.addWidget(self.fileResolution, 1, 2)

        spacerItem = QtWidgets.QSpacerItem(20, 20)
        self.mainLayout.addItem(spacerItem, 2, 0, 1, 3)

        # Row 2
        self.mainLayout.addWidget(self.fileSizeLabel, 3, 0)
        self.mainLayout.addWidget(self.fileRateLabel, 3, 1)
        self.mainLayout.addWidget(self.fileCodecsLabel, 3, 2)

        # Row 3
        self.mainLayout.addWidget(self.fileSize, 4, 0)
        self.mainLayout.addWidget(self.fileRate, 4, 1)
        self.mainLayout.addWidget(self.fileCodecs, 4, 2)

    def updateFileInformation(self):
        self.fileInformation = self.fileManager.getCurrentFileInformation()
    
        self.fileName.setText(str(self.fileInformation["name"]))
        self.fileExtension.setText(str(self.fileInformation["extension"]))
        self.fileSize.setText(str(self.fileInformation["size"]))
        self.fileResolution.setText(str(self.fileInformation["resolution"]))
        self.fileRate.setText(str(self.fileInformation["rate"]))
        self.fileCodecs.setText(str(self.fileInformation["codecs"]))


class FileUploader(QWidget):
    def __init__(self, parent: QWidget, settingsManager: SettingsManager, signalManager: SignalManager):
        super().__init__(parent)

        # Drop and File Choose Components
        self.dragDrop = FileDropFrame(settingsManager, signalManager)
        self.button = QtWidgets.QPushButton("Choose File")
        self.button.setObjectName("chooseFile")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.chooseFile)

        # Layouts
        self.mainLayout = QtWidgets.QGridLayout(self)

        # Add the dragDrop widget to the grid layout
        self.mainLayout.addWidget(self.dragDrop, 0, 0, 4, 3)  # Takes 4 rows

        # Add the button to the grid layout
        self.mainLayout.addWidget(self.button, 2, 3, 2, 1, Qt.AlignmentFlag.AlignCenter)  # Takes 1 row

    def chooseFile(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setOptions(QtWidgets.QFileDialog.Option.DontConfirmOverwrite)
        file_paths, _ = file_dialog.getOpenFileNames(self, "Choose File", "", "All Files (*);;Audio Files (*.mp3 *.wav);;Video Files (*.mp4 *.avi)")

        if file_paths:
            chosen_file = file_paths[0]
            self.dragDrop.fileManager.setNewInputFilePath(chosen_file)
            self.dragDrop.fileManager.updateFileInfo()
            self.dragDrop.signalManager.fileDropped.emit()

class FileDropFrame(QtWidgets.QFrame):
    def __init__(self, settingsManager: SettingsManager, signalManager: SignalManager):
        super().__init__()
        self.fileManager = settingsManager
        self.signalManager = signalManager
        #self.setFrameStyle(QtWidgets.QFrame.Shape.Panel)
        self.setAcceptDrops(True)
        self.setStyleSheet(
            f"background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};"
            f"border-radius: {BORDER_RADIUS}px;"
            )
        # Create a QLabel for displaying text
        self.textLabel = QLabel("Drop files here", self)
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        # Center the text label within the frame when the frame is resized
        self.textLabel.setGeometry(
            (self.width() - self.textLabel.width()) // 2,
            (self.height() - self.textLabel.height()) // 2,
            self.textLabel.width(),
            self.textLabel.height(),
        )

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        mime_data = event.mimeData()
        self.setStyleSheet(
            f"background-color: {Color.FILE_DROP_FRAME_DRAG.value};"
            f"border-radius: {BORDER_RADIUS}px;")
        
        if isinstance(mime_data, QtCore.QMimeData) and mime_data.hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        mime_data = event.mimeData()
        if isinstance(mime_data, QtCore.QMimeData) and mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        mime_data = event.mimeData()
        if isinstance(mime_data, QtCore.QMimeData) and mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.fileManager.setNewInputFilePath(file_path)
            self.fileManager.updateFileInfo()
            self.setStyleSheet(
                f"background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};"
                f"border-radius: {BORDER_RADIUS}px"
                )
            self.signalManager.fileDropped.emit()



