from PyQt6.QtGui import QFont

from ui.styles.traffic_analysis_style import TRAFFIC_ANALYSIS_STYLES
from ui.styles.traffic_analysis_information_style import (
    TRAFFIC_ANALYSIS_INFORMATION_STYLES,
)
from ui.styles.traffic_analysis_visualization_style import (
    TRAFFIC_ANALYSIS_VISUALIZATION_STYLES,
)

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
        border-radius: 5px;
        background-color: transparent;
        font-weight: bold;
        color: #ecf0f1;
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
        padding: 40px 20px 20px 20px;
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }

    QPushButton#button_new_session,
    QPushButton#button_open_session {
        width: 500px;
        padding: 25px 30px;
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        border: none;
        border-radius: 10px;
    }

    QPushButton#button_new_session {
        background-color: #3498db;
    }

    QPushButton#button_open_session {
        background-color: #27ae60;
    }

    QPushButton#button_new_session:hover {
        background-color: #2980b9;
    }

    QPushButton#button_open_session:hover {
        background-color: #219653;
    }

"""

MENU_ADDITIONAL_STYLES = """

    QFrame#menu_frame_additional {
        max-height: 80px;
        background-color: #ffffff;
        border-bottom: 5px solid #bdc3c7;
    }

    QPushButton#button_save_session,
    QPushButton#button_reload_session,
    QPushButton#button_end_session {
        padding: 10px 15px;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        background-color: #3498db;
    }

    QPushButton#button_save_session:hover,
    QPushButton#button_reload_session:hover,
    QPushButton#button_end_session:hover {
        background-color: #2980b9;
    }

"""

CHAT_STYLES = """

    QFrame#chat_frame {
        background-color: #ffffff;
        border: none;
    }

    QLabel#action_title {
        background-color: #ffffff;
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

    QLabel#description_title {
        font-size: 20px;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

    QLabel#question_title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

    QLabel#recommendation_title {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

    QFrame#answers_container {
        background-color: transparent;
        margin: 0px 0px 0px 0px;
    }

    MyWidget_AnswerButton#button_answer {
        padding: 10px 15px;
        background-color: #3498db;
        border: none;
        border-radius: 5px;
    }

    MyWidget_AnswerButton#button_answer QLabel {
        text-align: left;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
    }

    MyWidget_AnswerButton#button_answer:hover {
        background-color: #2980b9;
    }

    QLabel#result_title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

    QLabel#report_title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        padding: 0px 20px 0px 20px;
    }

"""

HISTORY_STYLES = """

    QFrame#history_frame {
        background-color: #f8f9fa;
        border: none;
    }

    QLabel#history_title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
    }

    QListWidget#history_list {
        padding: 10px 0px 10px 10px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }

    QListWidget#history_list::item {
        margin-bottom: 25px;
        margin-right: 10px;
        text-align: left;
        font-size: 20px;
        color: #000000;
        border: 1px solid transparent;
    }

    QListWidget#history_list::item:selected {
        margin-bottom: 25px;
        margin-right: 10px;
        background-color: #e6f2ff;
        border: 1px solid #4a90e2;
    }

"""


def apply_styles(app):

    # Глобальні стилі
    app.setStyle("Fusion")

    all_styles = (
        MAIN_WINDOW_STYLES
        + MENU_STYLES
        + SYSTEM_STYLES
        + MENU_ADDITIONAL_STYLES
        + CHAT_STYLES
        + HISTORY_STYLES
        + TRAFFIC_ANALYSIS_STYLES
        + TRAFFIC_ANALYSIS_INFORMATION_STYLES
        + TRAFFIC_ANALYSIS_VISUALIZATION_STYLES
    )

    app.setStyleSheet(all_styles)

    # Глобальний шрифт
    font = QFont("Segoe UI", 14)
    app.setFont(font)
