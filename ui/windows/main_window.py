from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QStyle,
)

from ui.windows.main_window_tabs.system_tab import create_system_tab
from ui.windows.main_window_tabs.traffic_analysis_tab import create_traffic_analysis_tab
from ui.windows.main_window_tabs.settings_tab import create_settings_tab


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Експертна система")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.setup_ui()

    def setup_ui(self):

        # 0. CENTRAL WIDGET
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setSpacing(0)
        central_layout.setContentsMargins(0, 0, 0, 0)

        # 1. MENU WIDGET
        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("menu_frame")
        menu_layout = QHBoxLayout(self.menu_frame)

        # 1.1 Button navigation
        self.button_system = QPushButton("Система")
        self.button_traffic_analysis = QPushButton("Аналіз трафіку")
        self.button_settings = QPushButton("Налаштування")

        # 1.2 Add class for button navigation
        self.button_system.setProperty("class", "navigation-button")
        self.button_traffic_analysis.setProperty("class", "navigation-button")
        self.button_settings.setProperty("class", "navigation-button")

        # 1.3 Add objects to a layout
        menu_layout.addWidget(self.button_system)
        menu_layout.addWidget(self.button_traffic_analysis)
        menu_layout.addWidget(self.button_settings)
        menu_layout.addStretch()

        # 2 STACKED WIDGET

        self.stacked_widget = QStackedWidget()

        # 0.1 Add objects to a layout
        central_layout.addWidget(self.menu_frame)
        central_layout.addWidget(self.stacked_widget)

        # Methods
        create_system_tab(self)
        create_traffic_analysis_tab(self)
        create_settings_tab(self)
        self.setup_navigation_buttons()

    def setup_navigation_buttons(self):

        # Status checkable
        self.button_system.setCheckable(True)
        self.button_traffic_analysis.setCheckable(True)
        self.button_settings.setCheckable(True)

        # Set system tab as default
        self.button_system.setChecked(True)
        self.stacked_widget.setCurrentIndex(0)

        # Connect signals
        self.button_system.clicked.connect(lambda: self.switch_tab(0))
        self.button_traffic_analysis.clicked.connect(lambda: self.switch_tab(1))
        self.button_settings.clicked.connect(lambda: self.switch_tab(2))

    def switch_tab(self, index):

        # Reset all buttons
        self.button_system.setChecked(False)
        self.button_traffic_analysis.setChecked(False)
        self.button_settings.setChecked(False)

        # Activate the desired button
        if index == 0:
            self.button_system.setChecked(True)
        elif index == 1:
            self.button_traffic_analysis.setChecked(True)
        elif index == 2:
            self.button_settings.setChecked(True)

        # Switch the tab
        self.stacked_widget.setCurrentIndex(index)
