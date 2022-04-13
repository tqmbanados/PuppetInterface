from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout)

from front_end.QPondWidgets import Metronome, ScoreLabel
from parameters import WINDOW_GEOMETRY


class PyPondWindow(QLabel):
    pass


class InstrumentWindow(QWidget):

    def __init__(self, beat_duration):
        super().__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.metronome = Metronome(beat_duration, parent=self)
        self.__next = 0
        self.score_labels = {}

        self.init_gui()

    def init_gui(self):
        self.setStyleSheet("background-color: white")
        score_box = QVBoxLayout()
        for i in range(4):
            new_label = ScoreLabel(i, parent=self)
            score_box.addWidget(new_label)
            score_box.addStretch()
            self.score_labels[i] = new_label

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(score_box)
        self.setLayout(main_hbox)

    @pyqtSlot()
    def update_label(self, time):
        pass


class ActorWindow(QWidget):
    signal_get_next = pyqtSignal(bool)
    signal_write_score = pyqtSignal()
    signal_update_value = pyqtSignal(dict)

    def __init__(self, beat_duration):
        super().__init__()
        self.acting_label = QLabel("", self)
        self.setGeometry(*WINDOW_GEOMETRY)
        self.init_gui()

    def init_gui(self):
        font = QFont()
        font.setPointSize(40)
        self.acting.setFont(font)
        self.setStyleSheet("background-color: white")

    @pyqtSlot(str, str, bool)
    def update_label(self, action, stage, change_stage):
        pass
