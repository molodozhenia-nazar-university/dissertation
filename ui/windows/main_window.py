from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QStackedWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyle


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Експертна система")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.setup_ui()

    def setup_ui(self):

        # 0. CENTRAL WIDGET
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setSpacing(0)
        central_layout.setContentsMargins(0, 0, 0, 0)

        # 1. MENU WIDGET
        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("menu_frame")
        menu_layout = QHBoxLayout(self.menu_frame)

        # 1.1 Button navigation
        self.button_system = QPushButton("Система")
        self.button_traffic_analysis = QPushButton("Аналіз трафіку")
        self.button_settings = QPushButton("Налаштування")

        # 1.2 Add class for button navigation
        self.button_system.setProperty("class", "navigation-button")
        self.button_traffic_analysis.setProperty("class", "navigation-button")
        self.button_settings.setProperty("class", "navigation-button")

        # 1.3 Add objects to a layout
        menu_layout.addWidget(self.button_system)
        menu_layout.addWidget(self.button_traffic_analysis)
        menu_layout.addWidget(self.button_settings)
        menu_layout.addStretch()

        # 2 STACKED WIDGET

        self.stacked_widget = QStackedWidget()

        # 0.1 Add objects to a layout
        central_layout.addWidget(self.menu_frame)
        central_layout.addWidget(self.stacked_widget)

        # Methods
        self.create_system_tab()
        self.create_traffic_analysis_tab()
        self.create_settings_tab()
        self.setup_navigation_buttons()

    def setup_navigation_buttons(self):

        # Status checkable
        self.button_system.setCheckable(True)
        self.button_traffic_analysis.setCheckable(True)
        self.button_settings.setCheckable(True)

        # Set system tab as default
        self.button_system.setChecked(True)
        self.stacked_widget.setCurrentIndex(0)

        # Connect signals
        self.button_system.clicked.connect(lambda: self.switch_tab(0))
        self.button_traffic_analysis.clicked.connect(lambda: self.switch_tab(1))
        self.button_settings.clicked.connect(lambda: self.switch_tab(2))

    def switch_tab(self, index):

        # Reset all buttons
        self.button_system.setChecked(False)
        self.button_traffic_analysis.setChecked(False)
        self.button_settings.setChecked(False)

        # Activate the desired button
        if index == 0:
            self.button_system.setChecked(True)
        elif index == 1:
            self.button_traffic_analysis.setChecked(True)
        elif index == 2:
            self.button_settings.setChecked(True)

        # Switch the tab
        self.stacked_widget.setCurrentIndex(index)

    def create_system_tab(self):

        system_widget = QWidget()
        system_layout = QVBoxLayout(system_widget)

        # CHAT and HISTORY WIDGETS
        chat_and_history_frame = QFrame()
        chat_and_history_layout = QHBoxLayout(chat_and_history_frame)
        chat_and_history_layout.setSpacing(0)
        chat_and_history_layout.setContentsMargins(0, 0, 0, 0)

        # SPLITTER
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(5)

        # CHAT WIDGET
        self.chat_frame = QFrame()
        self.chat_frame.setObjectName("chat_frame")
        chat_layout = QVBoxLayout(self.chat_frame)

        # Message box
        self.chat_message_box = QTextEdit()
        self.chat_message_box.setObjectName("chat_message_box")
        self.chat_message_box.setPlaceholderText("Діалог із експертною системою...")

        # Add objects to a chat layout
        chat_layout.addWidget(self.chat_message_box)

        # HISTORY WIDGET
        self.history_frame = QFrame()
        self.history_frame.setObjectName("history_frame")
        history_layout = QVBoxLayout(self.history_frame)

        # Search line and history title and list

        self.history_search = QLineEdit()
        self.history_search.setObjectName("history_search")
        self.history_search.setPlaceholderText("Пошук...")

        self.history_title = QLabel("Історія запитів:")
        self.history_title.setObjectName("history_title")

        self.history_list = QListWidget()
        self.history_list.setObjectName("history_list")

        # Add objects to a history layout
        history_layout.addWidget(self.history_search)
        history_layout.addWidget(self.history_title)
        history_layout.addWidget(self.history_list)

        # Add objects to a splitter layout
        splitter.addWidget(self.chat_frame)
        splitter.addWidget(self.history_frame)
        splitter.setSizes([700, 300])

        # 2.4 Add objects to a chat_and_history layout
        chat_and_history_layout.addWidget(splitter)

        system_layout.addWidget(chat_and_history_frame)

        self.stacked_widget.addWidget(system_widget)

    def create_traffic_analysis_tab(self):

        traffic_analysis_widget = QWidget()
        traffic_analysis_layout = QVBoxLayout(traffic_analysis_widget)

        # Plug
        label = QLabel("Аналіз трафіку - вкладка в розробці")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        traffic_analysis_layout.addWidget(label)

        self.stacked_widget.addWidget(traffic_analysis_widget)

    def create_settings_tab(self):

        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Plug
        label = QLabel("Налаштування - вкладка в розробці")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(label)

        self.stacked_widget.addWidget(settings_widget)
