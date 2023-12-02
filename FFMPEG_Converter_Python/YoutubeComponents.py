from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

class YoutubePanel(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.initComponent()

    def initComponent(self) -> None:
        self.label = QtWidgets.QLabel()
        self.label.setText("Download From Youtube")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        return