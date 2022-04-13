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

    window.signal_get_next.connect(render.render_image)
    window.signal_write_score.connect(render.write_score)
    window.signal_update_value.connect(render.update_values)
    render.file_completed.connect(window.update_label)

    window.show()
    sys.exit(app.exec())
