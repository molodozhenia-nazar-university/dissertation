from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QScreen
from ui.styles.main_style import MAIN_WINDOW_STYLES


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Експертна система")
        self.setFixedSize(500, 500)
        self.center_window()
        self.setStyleSheet(MAIN_WINDOW_STYLES)

        # self.setup_ui()

    def center_window(self):

        # Отримуємо геометрію екрана
        screen_geometry = QApplication.primaryScreen().geometry()

        # Розраховуємо центр екрана
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Встановлюємо позицію
        self.move(x, y)
