from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel


class MyWidget_HistoryReportInBubbleStyle(QWidget):

    def __init__(self, report: str, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Bubble Report (R3)

        bubble_report_frame = QFrame()
        bubble_report_frame.setObjectName("bubble_report_frame")

        bubble_report_layout = QVBoxLayout(bubble_report_frame)
        # bubble_report_layout.setContentsMargins(0, 0, 0, 0)

        bubble_report_label = QLabel(report)
        bubble_report_label.setWordWrap(True)

        # Add to local layout
        bubble_report_layout.addWidget(bubble_report_label)
        # Add to global layout
        layout.addWidget(bubble_report_frame)
