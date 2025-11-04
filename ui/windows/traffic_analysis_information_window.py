from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QSplitter,
    QStyle,
    QTreeWidget,
    QTreeWidgetItem,
)
from PyQt6.QtCore import Qt

from core.traffic_analysis_information import download_packets, get_details

from core.traffic_analysis_information import get_packet_layers, get_packet_hexdump


from PyQt6.QtWidgets import QHeaderView


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

        # TABLE
        self.table_packets = QTableWidget()
        self.table_packets.setObjectName("table_packets")

        # START TABLE SETTINGS
        self.table_packets.setColumnCount(7)
        self.table_packets.setHorizontalHeaderLabels(
            ["№", "Time", "Source", "Destination", "Protocol", "Length", "Information"]
        )

        header = self.table_packets.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive)

        self.table_packets.setColumnWidth(0, 100)
        self.table_packets.setColumnWidth(1, 200)
        self.table_packets.setColumnWidth(2, 200)
        self.table_packets.setColumnWidth(3, 200)
        self.table_packets.setColumnWidth(4, 125)
        self.table_packets.setColumnWidth(5, 100)
        self.table_packets.horizontalHeader().setStretchLastSection(True)

        self.table_packets.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table_packets.verticalHeader().setVisible(False)
        # END TABLE SETTINGS

        splitter.addWidget(self.table_packets)

        # PACKET DETAILS
        splitter_details = QSplitter(Qt.Orientation.Horizontal)
        splitter_details.setHandleWidth(5)
        splitter.addWidget(splitter_details)  # splitter plus details splitter

        self.packet_tree = QTreeWidget()
        self.packet_tree.setHeaderHidden(True)
        splitter_details.addWidget(self.packet_tree)

        self.packet_hexdump = QTextEdit()
        self.packet_hexdump.setReadOnly(True)
        splitter_details.addWidget(self.packet_hexdump)

        # DOWNLOAD PACKETS
        packets = download_packets(file_path)
        self.load_packets(packets)

        # DOWNLOAD DEFAULT DETAILS
        self.download_details(0)
        self.table_packets.selectRow(0)

        # DOWNLOAD DETAILS
        self.table_packets.cellClicked.connect(self.download_details)

    def load_packets(self, packets):
        self.table_packets.setRowCount(len(packets))
        for row, packet in enumerate(packets):
            self.table_packets.setItem(row, 0, QTableWidgetItem(str(packet["№"])))
            self.table_packets.setItem(row, 1, QTableWidgetItem(packet["Time"]))
            self.table_packets.setItem(row, 2, QTableWidgetItem(packet["Source"]))
            self.table_packets.setItem(row, 3, QTableWidgetItem(packet["Destination"]))
            self.table_packets.setItem(row, 4, QTableWidgetItem(packet["Protocol"]))
            self.table_packets.setItem(row, 5, QTableWidgetItem(str(packet["Length"])))
            self.table_packets.setItem(row, 6, QTableWidgetItem(packet["Information"]))

    def download_details_old(self, index):
        if index >= 0:
            details = get_details(index)
            self.packet_details.setText(details)

    def download_details(self, index):
        if index < 0:
            return

        self.packet_tree.clear()
        layers = get_packet_layers(index)
        for layer_name, fields in layers.items():
            parent = QTreeWidgetItem([layer_name])
            for key, value in fields.items():
                QTreeWidgetItem(parent, [f"{key}: {value}"])
            self.packet_tree.addTopLevelItem(parent)

        self.packet_hexdump.setText(get_packet_hexdump(index))
