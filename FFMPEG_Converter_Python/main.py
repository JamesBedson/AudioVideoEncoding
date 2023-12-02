from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPaintEvent, QPainter
import sys
from YoutubeComponents import *
from ConverterComponents import *
from styles import *

# MAIN WINDOW ===============================================================================================
class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.initUI()


    def initUI(self) -> None:

        self.fileManager    = FileManager()
        self.signalManager  = SignalManager()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainLayout = QtWidgets.QVBoxLayout(centralWidget)

        self.menu = QtWidgets.QTabBar(centralWidget)
        self.menu.addTab("Convert")
        self.menu.addTab("Download from Youtube")
        self.menu.currentChanged.connect(self.handleTabChange)

        # Layout for the File Info And Converter Settings Layout
        self.leftPanel      = LeftPanel(centralWidget, self.fileManager, self.signalManager)
        self.convSettings   = RightPanel(centralWidget, self.fileManager, self.signalManager)

        self.converterLayout = QtWidgets.QHBoxLayout()
        #self.converterLayout.setContentsMargins(0,0,0,0)
        self.converterLayout.addWidget(self.leftPanel, 2)
        self.converterLayout.addWidget(self.convSettings, 1)

        # Layout for the Download from Youtube Option
        self.youtubePanel = YoutubePanel(centralWidget)

        self.youtubeLayout = QtWidgets.QHBoxLayout()
        self.youtubeLayout.addWidget(self.youtubePanel)

        self.mainLayout.addWidget(self.menu)
        self.mainLayout.addLayout(self.converterLayout)
        self.mainLayout.addLayout(self.youtubeLayout)

        # Setting initial visibility:
        self.youtubePanel.hide()

        self.setFixedSize(700, 550)

    def handleTabChange(self, index: int):
        
        if index == 0:  # Convert tab selected
            self.leftPanel.show()
            self.convSettings.show()
            self.youtubePanel.hide()

        elif index == 1:  # Download from Youtube tab selected
            self.leftPanel.hide()
            self.convSettings.hide()
            self.youtubePanel.show()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor('white'), 2))
        
        if not self.youtubePanel.isVisible():
            painter.drawRect(self.leftPanel.geometry())
            painter.drawRect(self.convSettings.geometry())
        else:
            painter.drawRect(self.youtubePanel.geometry())

        super().paintEvent(event)

# =============================================================================================================
def main():
    app = QApplication(sys.argv)

    
    win = MainWindow()
    #win.setGeometry(0, 0, 100, 100)
    win.setWindowTitle("FFMPEG Converter")
    win.setStyleSheet(BUTTON_STYLE)
    win.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
        


