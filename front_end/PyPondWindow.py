from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton)

from front_end.QPondWidgets import Metronome, ScoreLabel
from param import WINDOW_GEOMETRY, SCORE_IMAGE_PATH
from os import path


class PyPondWindow(QLabel):
    string_converter = {'Marioneta': 'actor',
                        'Flauta': 'flute',
                        'Oboe': 'oboe',
                        'Clarinete': 'clarinet'}
    signal_send_type = pyqtSignal(str)
    signal_render = pyqtSignal()

    def __init__(self, beat_duration, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path.join(*image_path)
        self.beat_duration = beat_duration
        self.setGeometry(100, 150, 300, 300)
        self.buttons = {}
        self.window = None

        self.init_gui()

    def init_gui(self):
        v_box = QVBoxLayout()
        for name in ['Marioneta', 'Flauta', 'Oboe', 'Clarinete']:
            new_button = QPushButton(name, parent=self)
            new_button.clicked.connect(self.create_puppet_slot(name))
            v_box.addWidget(new_button)
            v_box.addStretch()
            self.buttons[name] = new_button

        hbox_main = QHBoxLayout()
        hbox_main.addLayout(v_box)
        self.setLayout(hbox_main)

    def create_puppet_slot(self, text):
        def temp_slot():
            selected = self.string_converter[text]
            if selected == 'actor':
                self.open_actor()
            else:
                self.open_instrument(selected)
        return temp_slot

    def open_actor(self):
        self.window = ActorWindow(self.signal_render)
        self.window.show()
        self.hide()

    def open_instrument(self, instrument):
        self.window = InstrumentWindow(self.beat_duration, self.path, self.signal_render)
        self.signal_send_type.emit(instrument)
        self.window.show()
        self.hide()

    @pyqtSlot(int)
    def file_completed(self, measure_duration):
        self.signal_render.emit()

    @pyqtSlot(str, str, bool)
    def update_command(self, action, stage, new_stage):
        pass


class InstrumentWindow(QWidget):

    def __init__(self, beat_duration, image_path, signal_render):
        super().__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.metronome = Metronome(beat_duration, parent=self)
        self.__current = 0
        self.score_labels = {}
        self.image_path = image_path
        signal_render.connect(self.update_label)

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

    def __init__(self, signal_render):
        super().__init__()
        self.acting_label = QLabel("", self)
        self.setGeometry(*WINDOW_GEOMETRY)
        self.signal_render = signal_render

        self.init_gui()

    def init_gui(self):
        font = QFont()
        font.setPointSize(40)
        self.acting_label.setFont(font)
        self.setStyleSheet("background-color: white")

    @pyqtSlot(str, str, bool)
    def update_label(self, action, stage, change_stage):
        pass
