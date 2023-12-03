import sys

# Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt

# Custom Components
from YoutubeComponents import YoutubePanel
from RightPanel import RightPanel
from LeftPanel import LeftPanel
from SettingsManager import SettingsManager, SignalManager
from styles import GLOBAL_STYLE


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self) -> None:

        self.fileManager    = SettingsManager()
        self.signalManager  = SignalManager()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainLayout = QtWidgets.QVBoxLayout(centralWidget)

        self.menu = QtWidgets.QTabBar(centralWidget)
        self.menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu.setObjectName("menu")
        
        self.menu.addTab("Convert")
        self.menu.addTab("Download from Youtube")
        self.menu.currentChanged.connect(self.handleTabChange)

        # Layout for the File Info And Converter Settings Layout
        self.leftPanel  = LeftPanel(centralWidget, self.fileManager, self.signalManager)
        self.rightPanel = RightPanel(centralWidget, self.fileManager, self.signalManager)

        self.converterLayout = QtWidgets.QHBoxLayout()
        self.converterLayout.addWidget(self.leftPanel, 2)
        self.converterLayout.addWidget(self.rightPanel, 1)

        # Layout for the Download from Youtube Option
        self.youtubePanel = YoutubePanel(centralWidget)

        self.youtubeLayout = QtWidgets.QHBoxLayout()
        self.youtubeLayout.addWidget(self.youtubePanel)

        self.mainLayout.addWidget(self.menu)
        self.mainLayout.addLayout(self.converterLayout)
        self.mainLayout.addLayout(self.youtubeLayout)
        
        self.youtubePanel.hide()
        self.setFixedSize(700, 600)

    def handleTabChange(self, index: int):
        
        if index == 0:  # Convert tab selected
            self.leftPanel.show()
            self.rightPanel.show()
            self.youtubePanel.hide()

        elif index == 1:  # Download from Youtube tab selected
            self.leftPanel.hide()
            self.rightPanel.hide()
            self.youtubePanel.show()

# =============================================================================================================
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLE)
    
    win = MainWindow()
    win.setWindowTitle("FFMPEG Converter")
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
        


