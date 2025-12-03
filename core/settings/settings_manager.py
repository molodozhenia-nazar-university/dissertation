from PyQt6.QtWidgets import QCheckBox
from typing import Optional


class SettingsManager:

    def __init__(self) -> None:
        self.bayes_checkbox: Optional[QCheckBox] = None

    def set_bayes_checkbox(self, checkbox: QCheckBox) -> None:
        self.bayes_checkbox = checkbox

    def is_bayes_enabled(self) -> bool:
        return bool(self.bayes_checkbox and self.bayes_checkbox.isChecked())


settings_manager = SettingsManager()
