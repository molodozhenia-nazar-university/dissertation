from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QTextEdit,
    QSplitter,
    QStyle,
)
from PyQt6.QtCore import Qt

from core.traffic_analysis_information import download_packets, get_details


class TrafficAnalysisInformationWindow(QWidget):

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setWindowTitle("Інформація")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setMinimumSize(800, 600)
        self.showMaximized()

        information_layout = QVBoxLayout(self)

        # SPLITTER
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(5)
        information_layout.addWidget(splitter)

        # PACKET LIST
        self.packet_list = QListWidget()
        splitter.addWidget(self.packet_list)

        # PACKET DETAILS
        self.packet_details = QTextEdit()
        self.packet_details.setReadOnly(True)
        splitter.addWidget(self.packet_details)

        # DOWNLOAD PACKETS
        self.packets = download_packets(file_path)
        self.packet_list.addItems(self.packets)

        # DOWNLOAD DETAILS
        self.packet_list.currentRowChanged.connect(self.download_details)

    def download_details(self, index):
        if index >= 0:
            details = get_details(index)
            self.packet_details.setText(details)
