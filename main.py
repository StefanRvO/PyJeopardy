#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication, QWidget
from widgets.MainWindow import MainWindow
import codecs

import sys
def _main():

    app = QApplication(sys.argv)

    w = MainWindow()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
