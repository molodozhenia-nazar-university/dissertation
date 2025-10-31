from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt

from core.knowledge_base import ChatManager


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

    # Add objects to a system layout
    system_layout.addStretch(1)
    system_layout.addWidget(system_title)
    system_layout.addStretch(1)
    system_layout.addWidget(buttons_container)
    system_layout.addStretch(1)

    main_window.stacked_widget.addWidget(system_widget)

    return system_widget


def new_session(system_widget):

    clear_layout(system_widget.layout())

    # CHAT and HISTORY WIDGETS
    chat_and_history_frame = QFrame()
    chat_and_history_layout = QHBoxLayout(chat_and_history_frame)
    chat_and_history_layout.setSpacing(0)
    chat_and_history_layout.setContentsMargins(0, 0, 0, 0)

    # SPLITTER
    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setHandleWidth(5)

    # CHAT WIDGET
    chat_frame = QFrame()
    chat_frame.setObjectName("chat_frame")
    chat_layout = QVBoxLayout(chat_frame)

    # System - Action Title
    system_title = QLabel()
    system_title.setObjectName("system_title")

    # Description
    system_description = QLabel()
    system_description.setObjectName("system_description")

    # Question
    question_title = QLabel()
    question_title.setObjectName("question_title")

    # Container for answers
    answers_container = QFrame()
    answers_layout = QVBoxLayout(answers_container)

    # Add objects to a chat layout
    chat_layout.addWidget(system_title)
    chat_layout.addWidget(system_description)
    chat_layout.addWidget(question_title)
    chat_layout.addWidget(answers_container)

    system_widget.layout().addWidget(chat_frame)

    # CHAT_MANAGER START

    chat_manager = ChatManager(
        system_title, system_description, question_title, answers_layout
    )

    def next_chat(next_chat_id):
        chat_manager.handle_chat(next_chat_id, next_chat)

    chat_manager.generate_chat_content(next_chat)

    # CHAT_MANAGER END

    # HISTORY WIDGET
    history_frame = QFrame()
    history_frame.setObjectName("history_frame")
    history_layout = QVBoxLayout(history_frame)

    # Search line and history title and list

    history_search = QLineEdit()
    history_search.setObjectName("history_search")
    history_search.setPlaceholderText("Пошук...")

    history_title = QLabel("Історія запитів:")
    history_title.setObjectName("history_title")
    history_list = QListWidget()
    history_list.setObjectName("history_list")

    # Add objects to a history layout
    history_layout.addWidget(history_search)
    history_layout.addWidget(history_title)
    history_layout.addWidget(history_list)

    # Add objects to a splitter layout
    splitter.addWidget(chat_frame)
    splitter.addWidget(history_frame)
    splitter.setSizes([700, 300])

    # Add objects to a chat and history layout
    chat_and_history_layout.addWidget(splitter)

    # Add objects to a system layout
    system_widget.layout().addWidget(chat_and_history_frame)


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
