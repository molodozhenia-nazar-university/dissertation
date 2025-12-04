from PyQt6.QtCore import QObject, pyqtSignal


class LiveSignals(QObject):

    log = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
