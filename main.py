import sys
from PyQt6.QtWidgets import QApplication
from ui.styles.main_style import apply_styles
from ui.windows.main_window import MainWindow


def main():

    app = QApplication(sys.argv)
    apply_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
