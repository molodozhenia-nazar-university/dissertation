from PyQt6.QtWidgets import (
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


def create_system_tab(main_window):

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
    main_window.chat_frame = QFrame()
    main_window.chat_frame.setObjectName("chat_frame")
    chat_layout = QVBoxLayout(main_window.chat_frame)

    # Message box
    main_window.chat_message_box = QTextEdit()
    main_window.chat_message_box.setObjectName("chat_message_box")
    main_window.chat_message_box.setPlaceholderText("Діалог із експертною системою...")

    # Add objects to a chat layout
    chat_layout.addWidget(main_window.chat_message_box)

    # HISTORY WIDGET
    main_window.history_frame = QFrame()
    main_window.history_frame.setObjectName("history_frame")
    history_layout = QVBoxLayout(main_window.history_frame)

    # Search line and history title and list

    main_window.history_search = QLineEdit()
    main_window.history_search.setObjectName("history_search")
    main_window.history_search.setPlaceholderText("Пошук...")

    main_window.history_title = QLabel("Історія запитів:")
    main_window.history_title.setObjectName("history_title")

    main_window.history_list = QListWidget()
    main_window.history_list.setObjectName("history_list")

    # Add objects to a history layout
    history_layout.addWidget(main_window.history_search)
    history_layout.addWidget(main_window.history_title)
    history_layout.addWidget(main_window.history_list)

    # Add objects to a splitter layout
    splitter.addWidget(main_window.chat_frame)
    splitter.addWidget(main_window.history_frame)
    splitter.setSizes([700, 300])

    # 2.4 Add objects to a chat_and_history layout
    chat_and_history_layout.addWidget(splitter)

    system_layout.addWidget(chat_and_history_frame)

    main_window.stacked_widget.addWidget(system_widget)

    return system_widget
