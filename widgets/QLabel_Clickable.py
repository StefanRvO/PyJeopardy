from PyQt5.QtWidgets import QStackedLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class QLabel_Clickable(QLabel):
    clicked = pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
    def mousePressEvent(self, event):
        self.clicked.emit()
