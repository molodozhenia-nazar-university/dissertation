from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


def create_settings_tab(main_window):

    settings_widget = QWidget()
    settings_layout = QVBoxLayout(settings_widget)

    # Plug
    label = QLabel("Налаштування - вкладка в розробці")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    settings_layout.addWidget(label)

    main_window.stacked_widget.addWidget(settings_widget)

    return settings_widget
