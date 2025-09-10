from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStyle
from ui.styles.main_style import MAIN_WINDOW_STYLES


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Експертна система")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setStyleSheet(MAIN_WINDOW_STYLES)
        self.setMinimumSize(800, 600)
        self.showMaximized()
