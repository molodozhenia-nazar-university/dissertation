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

        # 1.3 Add status for button
        # NEED TO PROGRAM
        self.button_system.setCheckable(True)  # status checkable
        self.button_system.setChecked(True)  # status checked
        self.button_traffic_analysis.setCheckable(True)  # status checkable
        self.button_settings.setCheckable(True)  # status checkable

        # 1.4 Add objects to a layout
        menu_layout.addWidget(self.button_system)
        menu_layout.addWidget(self.button_traffic_analysis)
        menu_layout.addWidget(self.button_settings)
        menu_layout.addStretch()

        # 2. SEARCH_HISTORY WIDGET
        self.search_history_frame = QFrame()
        self.search_history_frame.setObjectName("search_history_frame")
        search_history_layout = QHBoxLayout(self.search_history_frame)
        search_history_layout.setContentsMargins(10, 5, 10, 5)

        # 2.1 Search line
        self.search_history_input = QLineEdit()
        self.search_history_input.setObjectName("search_history_input")
        self.search_history_input.setPlaceholderText("Пошук...")

        # 2.2 Add objects to a layout
        search_history_layout.addWidget(self.search_history_input)

        # 3. CHAT and HISTORY WIDGETS
        chat_and_history_frame = QFrame()
        chat_and_history_layout = QHBoxLayout(chat_and_history_frame)
        chat_and_history_layout.setSpacing(0)
        chat_and_history_layout.setContentsMargins(0, 0, 0, 0)

        # 3.1 Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 3.2.1 CHAT WIDGET
        self.chat_frame = QFrame()
        self.chat_frame.setObjectName("chat_frame")
        chat_layout = QVBoxLayout(self.chat_frame)

        # 3.2.2 Message box
        self.chat_message_box = QTextEdit()
        self.chat_message_box.setObjectName("chat_message_box")
        self.chat_message_box.setPlaceholderText("Діалог із експертною системою...")

        # 3.2.3 Add objects to a layout
        chat_layout.addWidget(self.chat_message_box)

        # 3.3.1 HISTORY WIDGET
        self.history_frame = QFrame()
        self.history_frame.setObjectName("history_frame")
        history_layout = QVBoxLayout(self.history_frame)

        # 3.3.2 History title and list

        history_title = QLabel("Історія запитів:")
        history_title.setObjectName("section_title")

        self.history_list = QListWidget()
        self.history_list.setObjectName("history_list")

        # 3.3.3 Add objects to a layout
        history_layout.addWidget(history_title)
        history_layout.addWidget(self.history_list)

        # 3.4 Add objects to a layout
        splitter.addWidget(self.chat_frame)
        splitter.addWidget(self.history_frame)
        splitter.setSizes([600, 400])

        # 3.4 Add objects to a layout
        chat_and_history_layout.addWidget(splitter)

        # 4. SEND_FIELD WIDGET
        self.send_field_frame = QFrame()
        self.send_field_frame.setObjectName("send_field_frame")
        send_field_layout = QHBoxLayout(self.send_field_frame)

        # 4.1 Send line and button

        self.send_field_input = QLineEdit()
        self.send_field_input.setObjectName("send_field_input")
        self.send_field_input.setPlaceholderText("Введіть ваш запит...")

        self.send_field_button = QPushButton("Надіслати")
        self.send_field_button.setObjectName("send_field_button")

        # 4.2 Add objects to a layout
        send_field_layout.addWidget(self.send_field_input)
        send_field_layout.addWidget(self.send_field_button)

        # 0.1 Add objects to a layout
        central_layout.addWidget(self.menu_frame)
        central_layout.addWidget(self.search_history_frame)
        central_layout.addWidget(chat_and_history_frame, 1)
        central_layout.addWidget(self.send_field_frame)
