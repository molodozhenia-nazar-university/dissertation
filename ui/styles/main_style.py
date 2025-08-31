from PyQt6.QtGui import QFont

# Стилі для головного вікна
MAIN_WINDOW_STYLES = """

    QMainWindow {
        background-color: #f0f0f0;
        font-family: 'Segoe UI', Arial;
    }

"""


def apply_styles(app):

    # Глобальні стилі
    app.setStyle("Fusion")

    # Глобальний шрифт
    font = QFont("Segoe UI", 14)
    app.setFont(font)
