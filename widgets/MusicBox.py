#A widget representing a entire music category

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QStackedLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
import json
import pafy
import random
import threading
import tempfile
import os
from Modules.AudioPlayer import AudioPlayer
import bidict

MUSIC_STATES = bidict.bidict({  "DOWNLOADING" : -1,
                                "NOT_PLAYED" : 0,
                                "PLAYING_QUIZ" : 1,
                                "PAUSE"         :  2,
                                "PLAYING_ANSWER" : 3,
                                "USED" : 4})

DIR_NAME = "Jepardy_" + str(random.randint(0,10000000))

#m4a sucks and create shitty delays and unreliable seeks, so don't use this
prefered_formats = ["ogg", "webm", "3gp", "mp4", "flv", "m4a"]

class MusicBox(QWidget):
    download_progress = pyqtSignal(float, float, float, float, float)
    def __init__(self, amount, song_info):
        super().__init__()
        self.amount = amount
        self.state = MUSIC_STATES["NOT_PLAYED"]
        self.download_dir = os.path.normpath(os.path.join(tempfile.gettempdir(), DIR_NAME))
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        self.song_info = song_info
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.audio_info = None
        self.fetch_thread = None
        self.audio_player = AudioPlayer()

        self.label = QLabel()
        self.playing_quiz_label = QLabel()
        self.playing_answer_label = QLabel()
        self.used_label = QLabel()
        self.pause_label = QLabel()
        self.download_progress_label = QLabel()
        self.download_progress_label.setText("Downloading... \n 0%")
        self.label.setText(str(amount))
        self.playing_quiz_label.setText("Playing Quiz")
        self.used_label.setText("Used")
        self.pause_label.setText("Paused")

        for label in [self.download_progress_label, self.label, self.playing_quiz_label, self.pause_label, self.playing_answer_label, self.used_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid grey");
            self.layout.addWidget(label)

        self.layout.setCurrentIndex(0)

        self.download_finished = False
        self.download_progress.connect(self.update_progress)
        self.answer_str = None
        try:
            self.answer_str = self.song_info["answer"]
        except KeyError:
            pass
        if self.song_info["type"] == "youtube":
            self.load_youtube()

    def load_youtube(self):
        self.video = pafy.new(self.song_info["url"], basic = False)
        self.fetch_thread = threading.Thread(target = self.fetch_info_thread)
        self.fetch_thread.start()

    def fetch_info_thread(self):
        self.audio_info = None
        while True:
            try:
                for audio_format in prefered_formats[::-1]:
                    best = 0
                    for a in self.video.streams:
                        if(a.extension == audio_format and a.get_filesize() > best):
                            self.audio_info = a
            except RuntimeError:
                continue
            break
        print("best: ", self.audio_info.bitrate, self.audio_info.extension, self.audio_info.get_filesize())

        self.file_path = os.path.normpath(os.path.join(self.download_dir, str(random.randint(0,10000000)) + self.video.title + "." + self.audio_info.extension))
        self.filename = self.audio_info.download(filepath = self.file_path, quiet = True, callback=self.download_callback)
        if self.answer_str == None:
            self.answer_str = self.video.title
        self.playing_answer_label.setText(self.answer_str)

    def download_callback(self, total, recvd, ratio, rate, eta):
        self.download_progress.emit(total, recvd, ratio, rate, eta)

    def update_progress(self, total, recvd, ratio, rate, eta):
        if(ratio == 1.0):
            self.layout.setCurrentIndex(1)
            self.download_finished = True
            self.state = MUSIC_STATES["NOT_PLAYED"]

        self.download_progress_label.setText("Downloading... \n %f %%" % (ratio * 100) )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_click_event(event)
        elif event.button() == Qt.RightButton:
            self.right_click_event(event)
    def left_click_event(self, event):
            if(self.download_finished == False):
                return
            if self.state == MUSIC_STATES["NOT_PLAYED"]:
                self.state = MUSIC_STATES["PLAYING_QUIZ"]
                self.audio_player.play_file(self.filename, int(self.song_info["start_time"]) )
                self.layout.setCurrentIndex(2)
            elif self.state == MUSIC_STATES["PLAYING_QUIZ"]:
                self.state = MUSIC_STATES["PAUSE"]
                self.audio_player.pause()
                self.layout.setCurrentIndex(3)
            elif self.state == MUSIC_STATES["PAUSE"]:
                self.state = MUSIC_STATES["PLAYING_ANSWER"]
                self.audio_player.play_file(self.filename, int(self.song_info["answer_time"]) )
                self.layout.setCurrentIndex(4)
            elif self.state == MUSIC_STATES["PLAYING_ANSWER"]:
                self.state = MUSIC_STATES["USED"]
                self.audio_player.stop()
                self.layout.setCurrentIndex(5)
            elif self.state == MUSIC_STATES["USED"]:
                self.state = MUSIC_STATES["NOT_PLAYED"]
                self.audio_player.stop()
                self.layout.setCurrentIndex(1)

            print(MUSIC_STATES.inv[self.state])

    def right_click_event(self, event):
        if self.state == MUSIC_STATES["PAUSE"]:
            self.state = MUSIC_STATES["PLAYING_QUIZ"]
            self.audio_player.play()
            self.layout.setCurrentIndex(2)
