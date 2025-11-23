from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from core.wavelet_analysis import wavelet_analysis

from core.traffic_analysis_information import download_packets, get_details
from core.traffic_analysis_information import get_packet_layers, get_packet_hexdump


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

    finished_information = pyqtSignal(list)  # success information
    failed_information = pyqtSignal(str)  # defeat information

    @pyqtSlot()
    def information(self):

        try:
            results = download_packets(self.file_path)
            self.finished_information.emit(results)
        except Exception as e:
            self.failed_information.emit(str(e))
