import os

from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QStackedWidget,
    QFileDialog,  # new
    QComboBox,  # new
    QSpinBox,  # new
    QDoubleSpinBox,  # new
    QCheckBox,  # new
    QGroupBox,  # new
    QProgressBar,  # new
)
from PyQt6.QtCore import Qt, QTimer


def create_traffic_analysis_tab(main_window):

    traffic_analysis_widget = QWidget()
    traffic_analysis_layout = QVBoxLayout(traffic_analysis_widget)

    traffic_analysis_title = QLabel("Аналіз мережевого трафіку")
    traffic_analysis_title.setObjectName("traffic_analysis_title")
    traffic_analysis_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    buttons_container = QFrame()
    buttons_layout = QVBoxLayout(buttons_container)
    buttons_layout.setSpacing(30)
    buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Button Open File for Analysis
    button_open_file = QPushButton("📁 Аналіз файлу трафіку мережі")
    button_open_file.setObjectName("button_open_file")
    button_open_file.clicked.connect(lambda: show_analysis_interface("file"))

    # Button Live Analysis
    button_live_analysis = QPushButton(
        "🌐 Аналіз трафіку мережі в режимі реального часу"
    )
    button_live_analysis.setObjectName("button_live_analysis")
    button_live_analysis.clicked.connect(lambda: show_analysis_interface("live"))

    # Add objects to a buttons layout
    buttons_layout.addWidget(button_open_file)
    buttons_layout.addWidget(button_live_analysis)

    # STACKED WIDGET FOR DIFFERENT INTERFACES
    traffic_analysis_stacked_widget = QStackedWidget()

    # STRETCH
    stretch_page = QWidget()
    stretch_layout = QVBoxLayout(stretch_page)
    stretch_layout.addStretch()

    # Add STRETCH to STACKED and set index for STRETCH
    traffic_analysis_stacked_widget.insertWidget(0, stretch_page)
    traffic_analysis_stacked_widget.setCurrentIndex(0)

    # => Open File Interface
    file_analysis_widget = create_file_analysis_interface()
    traffic_analysis_stacked_widget.addWidget(file_analysis_widget)

    # => Live Analysis Interface
    live_analysis_widget = create_live_analysis_interface()
    traffic_analysis_stacked_widget.addWidget(live_analysis_widget)

    # BUTTON BACK
    button_back = QPushButton("Назад")
    button_back.setObjectName("button_back")
    button_back.clicked.connect(
        lambda: traffic_analysis_stacked_widget.setCurrentIndex(0)
    )

    # BUTTON BACK - status HIDE
    button_back.hide()

    # Add objects to a traffic analysis layout
    traffic_analysis_layout.addWidget(traffic_analysis_title)
    traffic_analysis_layout.addWidget(buttons_container)
    traffic_analysis_layout.addWidget(button_back)
    traffic_analysis_layout.addWidget(traffic_analysis_stacked_widget)

    def show_analysis_interface(type_analysis):
        if type_analysis == "file":
            traffic_analysis_stacked_widget.setCurrentIndex(1)
        elif type_analysis == "live":
            traffic_analysis_stacked_widget.setCurrentIndex(2)

        # BUTTON BACK - status SHOW
        button_back.show()
        # BUTTONS CONTAINER - status HIDE
        buttons_container.hide()

    def back_to_choice():
        traffic_analysis_stacked_widget.setCurrentIndex(0)
        # BUTTON BACK - status HIDE
        button_back.hide()
        # BUTTONS CONTAINER - status SHOW
        buttons_container.show()

    # BUTTON BACK - function
    button_back.clicked.connect(back_to_choice)

    main_window.stacked_widget.addWidget(traffic_analysis_widget)

    return traffic_analysis_widget


def create_file_analysis_interface():

    buffer_widget = QWidget()
    buffer_layout = QVBoxLayout(buffer_widget)

    # Plug
    label = QLabel("Вкладка в розробці")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    buffer_layout.addWidget(label)

    return buffer_widget


def create_live_analysis_interface():

    buffer_widget = QWidget()
    buffer_layout = QVBoxLayout(buffer_widget)

    # Plug
    label = QLabel("Вкладка в розробці")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    buffer_layout.addWidget(label)

    return buffer_widget
