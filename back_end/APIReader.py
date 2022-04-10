from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QTimer
from pypond.PondFile import PondDoc, PondRender
from pypond.PondCommand import PondHeader, PondPaper
from backend.pypond_extensions import LilypondScripts
from back_end.pond_request import get_score, get_actor
from os import path


class APIReader(QObject):
    signal_file_completed = pyqtSlot()

    def __init__(self, beat_duration, url="localhost"):
        super().__init__()
        self.render = PondRender()
        self.pond_doc = PondDoc()
        self.advance_bar = False
        self.timer = QTimer(parent=self)
        self.measure_number = 0
        self.command = 'mirar al frente'
        self.beat_duration = beat_duration
        self.api_url = url
        self.instrument = 'flute'

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

    def measure_duration(self, beat_number):
        return self.beat_duration * beat_number

    def render_image(self, render=True):
        response = get_score('flute')
        data = response.json()
        score = data['score_data']
        duration = data['duration']

        if render:
            time = duration
            self.timer.setInterval(self.measure_duration(time))
            print(f"Rendering measure {self.measure_number}\n"
                  f"    Volume: {self.composer.volume}\n"
                  f"    Stage: {self.composer.stage}-{self.composer.direction}")
            self.measure_number += 1
            self.pond_doc.score = score
            self.render.update(self.pond_doc.create_file())
            self.render.write()
            self.render.render()
            self.signal_file_completed.emit(time)
