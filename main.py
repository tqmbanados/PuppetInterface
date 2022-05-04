import sys

from PyQt5.QtWidgets import QApplication

from param import url, SCORE_IMAGE_PATH, BEAT_DURATION_MS
from back_end.APIReader import APIReader
from front_end.PyPondWindow import PyPondWindow

if __name__ == "__main__":
    def hook(type_, value, traceback):
        print(value, type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    window = PyPondWindow(BEAT_DURATION_MS, SCORE_IMAGE_PATH)
    render = APIReader(BEAT_DURATION_MS, url)

    window.signal_send_type.connect(render.set_instrument)
    window.signal_start.connect(render.begin)
    render.signal_file_completed.connect(window.file_completed)

    window.show()
    sys.exit(app.exec())
