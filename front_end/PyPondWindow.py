from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy)

from front_end.QPondWidgets import Metronome, ScoreLabel
from parameters import WINDOW_GEOMETRY
from os import path


class PyPondWindow(QLabel):

    def __init__(self, beat_duration, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path.join(*image_path)
        self.beat_duration = beat_duration


class InstrumentWindow(QWidget):

    def __init__(self, beat_duration, image_path):
        super().__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.metronome = Metronome(beat_duration, parent=self)
        self.__current = 0
        self.score_labels = {}
        self.image_path = image_path

        self.init_gui()

    def init_gui(self):
        self.setStyleSheet("background-color: white")
        score_box = QVBoxLayout()
        for i in range(4):
            new_label = ScoreLabel(i, parent=self)
            size_policy = QSizePolicy()
            size_policy.setRetainSizeWhenHidden(True)
            new_label.setSizePolicy(size_policy)
            score_box.addWidget(new_label)
            score_box.addStretch()
            self.score_labels[i] = new_label

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(score_box)
        self.setLayout(main_hbox)

    def get_current_label(self):
        current = self.__current
        hide = current - 2
        if hide < 0:
            hide = 4 + hide

        self.__current += 1
        if self.__current > 3:
            self.__current = 0
        return current, hide

    @pyqtSlot()
    def update_label(self, time):
        current, hide = self.get_current_label()
        self.score_labels[current].update_label(self.image_path)
        self.score_labels[hide].hide()


class ActorWindow(QWidget):
    signal_get_next = pyqtSignal(bool)
    signal_write_score = pyqtSignal()
    signal_update_value = pyqtSignal(dict)

    def __init__(self):
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
