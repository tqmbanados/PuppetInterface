from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel)

from front_end.QPondWidgets import Metronome
from parameters import WINDOW_GEOMETRY


class PyPondWindow(QWidget):
    signal_get_next = pyqtSignal(bool)
    signal_write_score = pyqtSignal()
    signal_update_value = pyqtSignal(dict)

    def __init__(self, beat_duration):
        super().__init__()
        self.music_label = QLabel("", self)
        self.acting_label = QLabel("", self)
        self.setGeometry(*WINDOW_GEOMETRY)
        self.metronome = Metronome(beat_duration, parent=self)
        self.init_gui()

    def init_gui(self):
        font = QFont()
        font.setPointSize(40)
        self.acting.setFont(font)

        self.setStyleSheet("background-color: white")

    def update_label(self, update_data):
        pass

