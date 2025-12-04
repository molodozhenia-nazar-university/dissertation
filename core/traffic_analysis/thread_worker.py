from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from core.traffic_analysis.wavelet_analysis import wavelet_analysis


class ThreadWorker(QObject):

    finished = pyqtSignal(dict)  # success
    failed = pyqtSignal(str)  # defeat

    def __init__(
        self, file_path, wavelet_type="db4", level=6, interval_sec=1, parent=None
    ):
        super().__init__(parent)
        self.file_path = file_path
        self.wavelet_type = wavelet_type
        self.level = level
        self.interval_sec = interval_sec

    @pyqtSlot()
    def run(self):

        try:
            results = wavelet_analysis(
                self.file_path, self.wavelet_type, self.level, self.interval_sec
            )
            self.finished.emit(results)
        except Exception as e:
            self.failed.emit(str(e))
