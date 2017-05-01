from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QLayout, QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5 import QtGui
from .PointBox import PointBox
from .Category import Category
from Modules.AudioPlayer import AudioPlayer
import json
import os
import traceback

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()


class MainWindow:
    class _MainWindow(QWidget):
        game_loaded = pyqtSignal(str)
        def __init__(self):
            super().__init__()

            self.timer = QTimer()
            self.timer.start(100)
            self.timer.timeout.connect(self.dummy)
            self.layout = QHBoxLayout()
            self.setLayout(self.layout)
            palette = QtGui.QPalette()

            palette.setColor(QtGui.QPalette.Background,Qt.blue)
            self.setPalette(palette)
            #Create a some widgets for the audioplayer so it does not pop up if playing video
            #We create 50 as a buffer..
            self.videoframe = [ QFrame(None) for q in range(50)]

            try:
                AudioPlayer(self.videoframe)
            except:
                self.showVLCError()
                return
            self.layout.addStretch()
            self.categories = []
            self.game_loaded.connect(self.load_game)
            for i in range(5):
                self.categories.append(Category())
                self.categories[-1].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                self.layout.addWidget(self.categories[-1], Qt.AlignCenter)

            self.layout.setSpacing(0)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.addStretch()
        def showVLCError(self):
                traceback.print_exc()
                error_str = "VLC Media Player is not installed!\nIt is required to run this software, so please install it."
                print(error_str)
                self.error_label = QLabel()
                self.error_label.setText(error_str)
                self.error_label.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(self.error_label, Qt.AlignCenter)
                return

        def load_game(self, file_name):
            self.tmp_cat = None
            try:
                self.game_settings = json.load(open(file_name))
                if not self.game_settings["type"] == "game":
                    return
                self.tmp_cat = self.categories
                self.categories = []
                for category in sorted(self.game_settings["categories"].keys()):
                    cat_dict = self.game_settings["categories"][category]
                    #Construct full path to category file
                    dirname = os.path.dirname(file_name)
                    cat_file = os.path.join(dirname, cat_dict["file"])
                    self.categories.append(Category())
                    self.categories[-1].set_category(cat_file)

                    print(cat_dict["file"])
                self.tmp_cat = []
                clearLayout(self.layout)
                for c in self.categories:
                    self.layout.addWidget(c, Qt.AlignCenter)
            except:
                self.categories = self.tmp_cat
                traceback.print_exc()

        def emit_game_loaded(self, str):
            self.game_loaded.emit(str)

        def dummy(self):
            pass

    instance = None
    def __init__(self):
        if MainWindow.instance == None:
            MainWindow.instance = MainWindow._MainWindow()
    def __getattr__(self, name):
        return getattr(self.instance, name)
