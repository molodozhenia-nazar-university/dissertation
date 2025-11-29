from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QListWidget,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFileDialog,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt

from core.expert_system.chat_manager import ChatManager
from core.expert_system.history_manager import HistoryManager


def create_system_tab(main_window):

    # STACKED WIDGET FOR SYSTEM AND PAGES
    system_and_pages_stacked_widget = QStackedWidget()

    system_widget = QWidget()
    system_layout = QVBoxLayout(system_widget)

    system_title = QLabel("Експертна система")
    system_title.setObjectName("system_title")
    system_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    buttons_container = QFrame()
    buttons_layout = QVBoxLayout(buttons_container)
    buttons_layout.setSpacing(30)
    buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # PAGE
    system_page_widget = QWidget()
    system_page_layout = QVBoxLayout(system_page_widget)

    # Button New Session
    button_new_session = QPushButton("📂 Нова сесія")
    button_new_session.setObjectName("button_new_session")
    button_new_session.clicked.connect(
        lambda: new_session(system_and_pages_stacked_widget, system_page_widget)
    )

    # Button Open Session
    button_open_session = QPushButton("📂 Відкрити сесію")
    button_open_session.setObjectName("button_open_session")
    button_open_session.clicked.connect(
        lambda: open_session(system_and_pages_stacked_widget, system_page_widget)
    )

    # Add objects to a buttons layout
    buttons_layout.addWidget(button_new_session)
    buttons_layout.addWidget(button_open_session)

    # Add objects to a system layout
    system_layout.addStretch(1)
    system_layout.addWidget(system_title)
    system_layout.addStretch(1)
    system_layout.addWidget(buttons_container)
    system_layout.addStretch(1)

    # Add object to a system and pages stacked layout
    system_and_pages_stacked_widget.addWidget(system_widget)
    system_and_pages_stacked_widget.addWidget(system_page_widget)

    system_and_pages_stacked_widget.setCurrentIndex(0)

    main_window.stacked_widget.addWidget(system_and_pages_stacked_widget)

    return system_and_pages_stacked_widget


def new_session(system_and_pages_stacked_widget, system_page_widget):
    generate_session(
        system_and_pages_stacked_widget, system_page_widget, session_file=None
    )


def open_session(system_and_pages_stacked_widget, system_page_widget):

    session_file, _ = QFileDialog.getOpenFileName(
        None,
        "Оберіть файл сесії експертної системи",
        # "D:\\",
        "sessions",
        "Файли сесії (*session.es.json);;Усі файли (*)",
    )

    if not session_file:
        system_and_pages_stacked_widget.setCurrentIndex(0)
        return

    generate_session(
        system_and_pages_stacked_widget, system_page_widget, session_file=session_file
    )


def generate_session(
    system_and_pages_stacked_widget, system_page_widget, session_file: str | None = None
):

    clear_layout(system_page_widget.layout())

    # CHAT and HISTORY WIDGETS
    chat_and_history_frame = QFrame()
    chat_and_history_layout = QVBoxLayout(chat_and_history_frame)
    chat_and_history_layout.setSpacing(0)
    chat_and_history_layout.setContentsMargins(0, 0, 0, 0)

    # MENU ADDITIONAL WIDGET
    menu_frame = QFrame()
    menu_layout = QHBoxLayout(menu_frame)
    menu_frame.setObjectName("menu_frame_additional")

    button_save_session = QPushButton("📘 Зберегти сесію")
    button_save_session.setObjectName("button_save_session")

    button_reload_session = QPushButton("📘 Розпочати заново")
    button_reload_session.setObjectName("button_reload_session")

    button_end_session = QPushButton("📘 Завершити")
    button_end_session.setObjectName("button_end_session")
    button_end_session.setVisible(False)

    menu_layout.addWidget(button_save_session, 1)
    menu_layout.addWidget(button_reload_session, 1)
    menu_layout.addWidget(button_end_session, 1)

    # SPLITTER
    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setHandleWidth(5)

    # CHAT WIDGET
    chat_frame = QFrame()
    chat_frame.setObjectName("chat_frame")
    chat_layout = QVBoxLayout(chat_frame)
    chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # System - Action Title
    action_title = QLabel()
    action_title.setObjectName("action_title")
    action_title.setWordWrap(True)
    action_title.setVisible(False)

    # Description
    description_title = QLabel()
    description_title.setObjectName("description_title")
    description_title.setWordWrap(True)
    description_title.setVisible(False)

    # Question
    question_title = QLabel()
    question_title.setObjectName("question_title")
    question_title.setWordWrap(True)

    # Recommendation
    recommendation_title = QLabel()
    recommendation_title.setObjectName("recommendation_title")
    recommendation_title.setWordWrap(True)
    recommendation_title.setVisible(False)

    # Container for answers
    answers_container = QFrame()
    answers_container.setObjectName("answers_container")
    answers_layout = QVBoxLayout(answers_container)

    # Result
    result_title = QLabel()
    result_title.setObjectName("result_title")
    result_title.setWordWrap(True)
    result_title.setVisible(False)

    # Result
    report_title = QLabel()
    report_title.setObjectName("report_title")
    report_title.setWordWrap(True)
    report_title.setVisible(False)

    # Add objects to a chat layout
    chat_layout.addWidget(action_title)
    chat_layout.addWidget(description_title)
    chat_layout.addWidget(question_title)
    chat_layout.addWidget(recommendation_title)
    chat_layout.addWidget(answers_container)
    chat_layout.addWidget(result_title)
    chat_layout.addWidget(report_title)

    # SCROLL AREA WIDGET
    chat_scroll = QScrollArea()
    chat_scroll.setObjectName("chat_scroll")
    chat_scroll.setWidget(chat_frame)
    chat_scroll.setMinimumWidth(500)
    chat_scroll.setWidgetResizable(True)
    chat_scroll.setFrameShape(QFrame.Shape.NoFrame)
    chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    chat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # HISTORY WIDGET
    history_frame = QFrame()
    history_frame.setObjectName("history_frame")
    history_frame.setMinimumWidth(500)
    history_layout = QVBoxLayout(history_frame)

    # History title and list

    history_title = QLabel("Історія діалогу:")
    history_title.setObjectName("history_title")

    history_list = QListWidget()
    history_list.setObjectName("history_list")
    history_list.setSpacing(25)
    history_list.setWordWrap(True)
    history_list.setUniformItemSizes(False)
    history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    history_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    history_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    history_list.verticalScrollBar().setSingleStep(10)

    # Add objects to a history layout
    history_layout.addWidget(history_title)
    history_layout.addWidget(history_list)

    # Add objects to a splitter layout
    splitter.addWidget(chat_scroll)
    splitter.addWidget(history_frame)
    splitter.setSizes([700, 300])

    # Add objects to a chat and history layout
    chat_and_history_layout.addWidget(menu_frame)
    chat_and_history_layout.addWidget(splitter)

    # Add objects to a system layout
    system_page_widget.layout().addWidget(chat_and_history_frame)

    # HISTORY MANAGER

    history_manager = HistoryManager(history_list)

    # TYPE SESSION
    if session_file is None:
        history_manager.start_session(start_chat_id="START")
        current_chat_id = "START"
    else:
        last_chat_id = history_manager.load_session(session_file)
        if not last_chat_id:
            last_chat_id = "START"
        current_chat_id = last_chat_id

    # MENU ADDITIONAL SIGNALS

    def end_session():
        if history_manager is not None:
            history_manager.save_to_file()
        system_and_pages_stacked_widget.setCurrentIndex(0)

    button_save_session.clicked.connect(lambda: history_manager.save_to_file())
    button_reload_session.clicked.connect(
        lambda: system_and_pages_stacked_widget.setCurrentIndex(0)
    )
    button_end_session.clicked.connect(lambda: end_session())

    # CHAT_MANAGER START

    chat_manager = ChatManager(
        action_title,
        description_title,
        question_title,
        recommendation_title,
        answers_layout,
        result_title,
        report_title,
        button_end_session,
        history_manager,
    )

    def next_chat(next_chat_id):
        chat_manager.handle_chat(next_chat_id, next_chat)

    chat_manager.current_chat_id = current_chat_id
    chat_manager.generate_chat_content(next_chat)

    # CHAT_MANAGER END

    system_and_pages_stacked_widget.setCurrentIndex(1)


def clear_layout(layout):

    if layout is None:
        return

    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
