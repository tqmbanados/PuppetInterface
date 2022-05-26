from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton)
from PyQt5.QtMultimedia import QSound

from front_end.QPondWidgets import ScoreLabel
from param import WINDOW_GEOMETRY
from os import path


class PyPondWindow(QLabel):
    string_converter = {'Marioneta': 'actor',
                        'Flauta': 'Flute',
                        'Oboe': 'Oboe',
                        'Clarinete': 'Clarinet'}
    signal_send_type = pyqtSignal(str)
    signal_render = pyqtSignal()
    signal_start = pyqtSignal()
    signal_update = pyqtSignal(str, str, bool)

    def __init__(self, beat_duration, image_path, audio_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path = image_path
        self.audio_path = audio_path
        self.beat_duration = beat_duration
        self.setGeometry(100, 150, 300, 300)
        self.buttons = {}
        self.window = None

        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Menú')
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
        self.window = ActorWindow(self.signal_start, self.audio_path)
        self.signal_update.connect(self.window.update_label)
        self.signal_send_type.emit('actor')
        self.window.show()
        self.hide()

    def open_instrument(self, instrument):
        self.window = InstrumentWindow(instrument, self.image_path, self.signal_start)
        self.signal_render.connect(self.window.update_label)
        self.signal_send_type.emit(instrument)
        self.window.show()
        self.hide()

    @pyqtSlot()
    def file_completed(self):
        self.signal_render.emit()

    @pyqtSlot(str, str, bool)
    def update_command(self, action, stage, new_stage):
        self.signal_update.emit(action, stage, new_stage)


class InstrumentWindow(QWidget):

    def __init__(self, instrument, image_path, signal_start):
        super().__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.__current = 0
        self.score_labels = {}
        self.instrument = instrument
        self.image_path = image_path
        self.signal_start = signal_start
        self.buttons = {}

        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(f'Marioneta - {self.instrument}')
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

        new_button = QPushButton('Empezar', parent=self)
        new_button.clicked.connect(self.start)
        self.buttons['start'] = new_button
        vbox_button = QVBoxLayout()
        vbox_button.addWidget(new_button)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(score_box)
        main_hbox.addLayout(vbox_button)
        self.setLayout(main_hbox)

    @pyqtSlot()
    def start(self):
        self.signal_start.emit()
        self.buttons['start'].hide()

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
    def update_label(self):
        current, hide = self.get_current_label()
        self.score_labels[current].update_label(self.image_path)
        self.score_labels[current].show()
        self.score_labels[hide].hide()


class ActorWindow(QWidget):

    def __init__(self, signal_start, audio_path):
        super().__init__()
        self.acting_label = QLabel("inerte", self)
        self.stage_label = QLabel("0", self)
        self.boton_empezar = QPushButton('Empezar', self)
        self.setGeometry(*WINDOW_GEOMETRY)
        self.audio_path = audio_path
        self.signal_start = signal_start

        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Marioneta')
        self.setStyleSheet("background-color: white")

        font = QFont()
        font.setPointSize(100)
        self.acting_label.setFont(font)
        new_font = QFont()
        new_font.setPointSize(40)
        self.stage_label.setFont(new_font)
        self.boton_empezar.clicked.connect(self.start)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.acting_label)
        vbox.addStretch()
        vbox.addWidget(self.stage_label)
        vbox.addStretch()
        vbox.addWidget(self.boton_empezar)
        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()
        self.setLayout(hbox)

    @pyqtSlot()
    def start(self):
        self.signal_start.emit()
        self.boton_empezar.hide()

    @pyqtSlot(str, str, bool)
    def update_label(self, action, stage, change_stage):
        self.acting_label.setText(action)
        self.stage_label.setText(stage)
        if change_stage:
            self.play_audio(stage)
        self.play_audio(action)

    def play_audio(self, audio_name):
        audio_path = path.join(self.audio_path, audio_name + '.wav')
        try:
            QSound.play(audio_path)
        except FileNotFoundError as error:
            print(error)
