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

    system_title = QLabel("Експертна система")
    system_title.setObjectName("system_title")
    system_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    buttons_container = QFrame()
    buttons_layout = QVBoxLayout(buttons_container)
    buttons_layout.setSpacing(30)
    buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Button New Session
    button_new_session = QPushButton("📂 Нова сесія")
    button_new_session.setObjectName("button_new_session")
    button_new_session.clicked.connect(lambda: new_session(system_widget))

    # Button Open Session
    button_open_session = QPushButton("📂 Відкрити сесію")
    button_open_session.setObjectName("button_open_session")
    button_open_session.clicked.connect(lambda: open_session(system_widget))

    # Add objects to a buttons layout
    buttons_layout.addWidget(button_new_session)
    buttons_layout.addWidget(button_open_session)

    # Add objects to a buttons layout
    system_layout.addStretch(1)
    system_layout.addWidget(system_title)
    system_layout.addStretch(1)
    system_layout.addWidget(buttons_container)
    system_layout.addStretch(1)

    main_window.stacked_widget.addWidget(system_widget)

    return system_widget


def new_session(system_widget):

    clear_layout(system_widget.layout())

    # Plug
    label = QLabel("new_session")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    system_widget.layout().addWidget(label)


def open_session(system_widget):

    clear_layout(system_widget.layout())

    # Plug
    label = QLabel("open_session")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    system_widget.layout().addWidget(label)


def clear_layout(layout):

    if layout is None:
        return

    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


"""
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

    # Add objects to a chat and history layout
    chat_and_history_layout.addWidget(splitter)

    # Add objects to a system layout
    system_layout.addWidget(chat_and_history_frame)

    main_window.stacked_widget.addWidget(system_widget)
    """
