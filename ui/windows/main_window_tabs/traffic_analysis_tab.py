from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


def create_traffic_analysis_tab(main_window):

    traffic_analysis_widget = QWidget()
    traffic_analysis_layout = QVBoxLayout(traffic_analysis_widget)

    # Plug
    label = QLabel("Аналіз трафіку - вкладка в розробці")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    traffic_analysis_layout.addWidget(label)

    main_window.stacked_widget.addWidget(traffic_analysis_widget)

    return traffic_analysis_widget
