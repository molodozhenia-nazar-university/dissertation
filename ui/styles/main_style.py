from PyQt6.QtGui import QFont

MAIN_WINDOW_STYLES = """

    QMainWindow {
        background-color: #f0f0f0;
        font-family: 'Segoe UI', Arial;
    }

    QSplitter::handle {
        background-color: #bdc3c7;
        width: 3px;
    }

    QSplitter::handle:hover {
        background-color: #95a5a6;
    }

    QLabel.section-title {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        padding: 10px 0;
        background-color: transparent;
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

SEARCH_HISTORY_STYLES = """

    QFrame#search_history_frame {
        background-color: #ecf0f1;
        border-top: 1px solid #bdc3c7;
        border-bottom: 1px solid #bdc3c7;
    }

    QLineEdit#search_history_input {
        padding: 10px 15px;
        background-color: #ffffff;
        border: 3px solid #bdc3c7;
        border-radius: 15px;
        color: #2c3e50;
    }

    QLineEdit#search_history_input:focus {
        border: 3px solid #3498db;
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

    QListWidget#history_list {
        padding: 5px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;        
    }

"""

SEND_FIELD_STYLES = """

    QFrame#send_field_frame {
        padding: 10px;
        background-color: #ffffff;
        border-top: 1px solid #bdc3c7;
    }
    
    QLineEdit#send_field_input {
        padding: 10px 15px;
        background-color: #ffffff;
        border: 3px solid #bdc3c7;
        border-radius: 15px;
        color: #2c3e50;
    }

    QLineEdit#send_field_input:focus {
        border: 3px solid #3498db;
    }

    QPushButton#send_field_button {
        padding: 15px 25px;
        background-color: #3498db;
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: bold;
    }

    QPushButton#send_field_button:hover {
        background-color: #2980b9;
    }

"""


def apply_styles(app):

    # Глобальні стилі
    app.setStyle("Fusion")

    all_styles = (
        MAIN_WINDOW_STYLES
        + MENU_STYLES
        + SEARCH_HISTORY_STYLES
        + CHAT_STYLES
        + HISTORY_STYLES
        + SEND_FIELD_STYLES
    )

    app.setStyleSheet(all_styles)

    # Глобальний шрифт
    font = QFont("Segoe UI", 14)
    app.setFont(font)
