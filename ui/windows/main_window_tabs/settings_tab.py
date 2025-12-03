from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox

from core.settings.settings_manager import settings_manager


def create_settings_tab(main_window):

    settings_widget = QWidget()
    settings_layout = QVBoxLayout(settings_widget)

    bayes_checkbox = QCheckBox("Bayes Mode")
    bayes_checkbox.setObjectName("bayes_checkbox")
    bayes_checkbox.setChecked(False)
    settings_layout.addWidget(bayes_checkbox)

    settings_manager.set_bayes_checkbox(bayes_checkbox)

    settings_layout.addStretch()

    main_window.stacked_widget.addWidget(settings_widget)

    return settings_widget
