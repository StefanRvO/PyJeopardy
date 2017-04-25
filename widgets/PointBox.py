from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class PointBox(QWidget):
    def __init__(self, amounts):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.labels = []
        self.amounts = amounts
        i = 0
        self.empty_label = QLabel()
        self.empty_label.setStyleSheet("border: 1px solid grey");
        self.layout.addWidget(self.empty_label, Qt.AlignCenter)
        for amount in amounts:
            new_label = QLabel()
            new_label.setStyleSheet("border: 1px solid grey");
            new_label.setText(str(amount))
            new_label.setAlignment(Qt.AlignCenter)
            self.labels.append(new_label)
            self.layout.addWidget(new_label, Qt.AlignCenter)
            i += 1
