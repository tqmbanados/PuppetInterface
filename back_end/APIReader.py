from PyQt5.QtCore import QObject, pyqtSlot, QTimer, pyqtSignal

from back_end.pond_request import get_score
from back_end.pypond_extensions import LilypondScripts
from pypond.PondCommand import PondHeader
from pypond.PondFile import PondDoc, PondRender


class APIReader(QObject):
    signal_file_completed = pyqtSignal(int)
    signal_update_command = pyqtSignal(str, str, bool)

    def __init__(self, beat_duration, url="localhost"):
        super().__init__()
        self.render = PondRender()
        self.pond_doc = PondDoc()
        self.advance_bar = False
        self.measure_number = 0
        self.timer = QTimer()
        self.command = 'mirar al frente'
        self.beat_duration = beat_duration
        self.api_url = url
        self.instrument = 'flute'
        self.stage = '0-0'

        self.init_doc()

    def init_doc(self):
        self.pond_doc.header = PondHeader()
        for name, function in LilypondScripts.commands_dict().items():
            self.pond_doc.add_function(name, function)
        self.timer.timeout.connect(self.render_image)
        self.timer.setInterval(self.measure_duration(6))

    @pyqtSlot()
    def begin(self):
        self.timer.start()

    @pyqtSlot(str)
    def set_instrument(self, instrument):
        self.instrument = instrument

    def measure_duration(self, beat_number):
        return self.beat_duration * beat_number

    @pyqtSlot()
    def render_image(self):
        if self.instrument == 'actor':
            response = get_score(self.instrument)
            data = response.json()
            action = data['action']
            stage = data['stage']
            new_stage = False
            if stage != self.stage:
                self.stage = stage
                new_stage = True
            time = 4
            self.signal_update_command.emit(action, stage, new_stage)

        else:
            response = get_score(self.instrument)
            data = response.json()
            score = data['score_data']
            duration = data['duration']

            time = self.measure_duration(duration)
            self.measure_number += 1
            self.pond_doc.score = score
            self.render.update(self.pond_doc.create_file())
            self.render.write()
            self.render.render()
            self.signal_file_completed.emit(time)
        QTimer.singleShot(time, self.render_image)
