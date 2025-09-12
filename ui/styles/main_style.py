from PyQt6.QtGui import QFont

MAIN_WINDOW_STYLES = """

    QMainWindow {
        background-color: #f0f0f0;
        font-family: 'Segoe UI', Arial;
    }

    QSplitter::handle {
        background-color: #bdc3c7;
    }

    QSplitter::handle:hover {
        background-color: #95a5a6;
    }

"""

MENU_STYLES = """

    QFrame#menu_frame {
        padding: 5px;
        background-color: #2c3e50;
        border-bottom: 3px solid #34495e;
    }

    QPushButton.navigation-button {
        padding: 10px 15px;
        border: none;
        background-color: transparent;
        color: #ecf0f1;
        font-weight: bold;
        border-radius: 5px;
    }

    QPushButton.navigation-button:hover {
        background-color: #34495e;
    }

    QPushButton.navigation-button:checked {
        background-color: #3498db;
        color: white;
    }

"""

SYSTEM_STYLES = """

QLabel#system_title {
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
    padding: 40px 20px 20px 20px;
    background-color: transparent;
}

QFrame {
    background-color: transparent;
}

QPushButton#button_new_session,
QPushButton#button_open_session {
    margin: 10px;
    padding: 20px 30px;
    background-color: #3498db;
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    min-height: 70px;
    min-width: 300px;
}

QPushButton#button_new_session:hover,
QPushButton#button_open_session:hover {
    background-color: #2980b9;
}

QPushButton#button_new_session:pressed,
QPushButton#button_open_session:pressed {
    background-color: #21618c;
}

QPushButton#button_new_session:focus,
QPushButton#button_open_session:focus {
    outline: 2px solid #2c3e50;
    outline-offset: 2px;
}

/* Add styles */
QPushButton#button_new_session {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #3498db, stop: 1 #2980b9);
}

QPushButton#button_open_session {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                              stop: 0 #27ae60, stop: 1 #219653);
}

QPushButton#button_open_session:hover {
    background-color: #219653;
}

"""

CHAT_STYLES = """

    QFrame#chat_frame {
        background-color: #ffffff;
        border-right: 1px solid #bdc3c7;
    }

    QTextEdit#chat_message_box {
        padding: 15px;
        background-color: #ffffff;
        border: none;
        color: #2c3e50;
    }

    QTextEdit#chat_message_box:focus {
        border: none;
    }

"""

HISTORY_STYLES = """

    QFrame#history_frame {
        background-color: #f8f9fa;
        border-left: 1px solid #bdc3c7;
    }

    QLabel#history_title {
        font-weight: bold;
    }

    QLineEdit#history_search {
        padding: 10px 15px;
        background-color: #ffffff;
        border: 3px solid #bdc3c7;
        border-radius: 15px;
        color: #2c3e50;
    }

    QLineEdit#history_search:focus {
        border: 3px solid #3498db;
    }

    QListWidget#history_list {
        padding: 5px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;        
    }

"""


def apply_styles(app):

    # Глобальні стилі
    app.setStyle("Fusion")

    all_styles = (
        MAIN_WINDOW_STYLES + MENU_STYLES + SYSTEM_STYLES + CHAT_STYLES + HISTORY_STYLES
    )

    app.setStyleSheet(all_styles)

    # Глобальний шрифт
    font = QFont("Segoe UI", 14)
    app.setFont(font)
