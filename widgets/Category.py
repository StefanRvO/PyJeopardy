#A widget representing a entire music category

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from .MusicBox import MusicBox
from .QLabel_Clickable import QLabel_Clickable
from widgets import MainWindow
import json
import random
import traceback

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

class Category(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.title = QLabel_Clickable()
        self.title.setStyleSheet("border: 5px solid black");
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Click to load Category")
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title.clicked.connect(self.choose_file)
        self.layout.addWidget(self.title, QtCore.Qt.AlignCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

    def choose_file(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Category or Game",
        ",", "Json Files (*.json)")[0]
        if fileName == "": return
        try:
            self.set_category(fileName)
        except:
            traceback.print_exc()
            clearLayout(self.layout)
            self.title = QLabel_Clickable()
            self.title.setStyleSheet("border: 5px solid black");
            self.title.setAlignment(QtCore.Qt.AlignCenter)
            self.title.setText("Error loading Category")
            self.title.clicked.connect(self.choose_file)
            self.layout.addWidget(self.title, QtCore.Qt.AlignCenter)

    def set_category(self, file_name):
        #Clear current layout
        clearLayout(self.layout)
        self.title = QLabel_Clickable()
        self.title.setStyleSheet("border: 5px solid black");
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.clicked.connect(self.choose_file)
        self.layout.addWidget(self.title, QtCore.Qt.AlignCenter)

        try:
            self.settings = json.load(open(file_name))
            if(self.settings["type"] == "game"):
                m_window = MainWindow.MainWindow()
                m_window.emit_game_loaded(file_name)
                return
            if( not self.settings["type"] == "category"):
                self.title.setText("%s is not a category config" % file_name)
                return
            self.title.setText(self.settings["title"])
            self.music_boxes = []
            self.urls = []
            for sub_cat in sorted(self.settings["subcategories"].keys()):
                song_list = self.settings["subcategories"][sub_cat]
                next_choice = song_list[random.choice(list(song_list.keys()))]
                while next_choice["url"]  in self.urls:
                    next_choice = song_list[random.choice(list(song_list.keys()))]

                new_box = MusicBox(sub_cat, next_choice)
                self.music_boxes.append(new_box)
                self.layout.addWidget(new_box, QtCore.Qt.AlignCenter)
        except:
            traceback.print_exc()
            self.title.setText("Error loading category!")
